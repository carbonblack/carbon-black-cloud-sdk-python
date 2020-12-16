#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""The Live Response API and associated objects."""

from __future__ import absolute_import

import json
import random
import string
import threading
import time
import logging
from collections import defaultdict

import shutil

from cbc_sdk.errors import TimeoutError, ObjectNotFoundError, ApiError
from concurrent.futures import _base, wait
from cbc_sdk import winerror

import queue

OS_LIVE_RESPONSE_ENUM = {
    "WINDOWS": 1,
    "LINUX": 2,
    "MAC": 4
}

log = logging.getLogger(__name__)


class LiveResponseError(Exception):
    """Exception raised for errors with Live Response."""

    def __init__(self, details):
        """
        Initialize the LiveResponseError.

        Args:
            details (object): Details of the specific error.
        """
        message_list = []

        self.details = details
        self.win32_error = None
        self.decoded_win32_error = ""

        # Details object:
        # {u'status': u'error', u'username': u'admin', u'device_id': 9, u'name': u'kill',
        # u'completion': 1464319733.190924, u'object': 1660, u'session_id': 7, u'result_type': u'WinHresult',
        # u'create_time': 1464319733.171967, u'result_desc': u'', u'id': 22, u'result_code': 2147942487}

        if self.details.get("status") == "error" and self.details.get("result_type") == "WinHresult":
            # attempt to decode the win32 error
            win32_error_text = "Unknown Win32 error code"
            try:
                self.win32_error = int(self.details.get("result_code"))
                win32_error_text = "Win32 error code 0x%08X" % (self.win32_error,)
                self.decoded_win32_error = winerror.decode_hresult(self.win32_error)
                if self.decoded_win32_error:
                    win32_error_text += " ({0})".format(self.decoded_win32_error)
            except Exception:
                pass
            finally:
                message_list.append(win32_error_text)

        self.message = ": ".join(message_list)

    def __str__(self):
        """
        Return the string equivalent of this exception (the exception's message).

        Returns:
            str: The exception's message.
        """
        return self.message


class CbLRSessionBase(object):
    """A Live Response session that interacts with a remote machine."""

    MAX_RETRY_COUNT = 5

    def __init__(self, cblr_manager, session_id, device_id, session_data=None):
        """
        Initialize the CbLRSessionBase.

        Args:
            cblr_manager (CbLRManagerBase): The Live Response manager governing this session.
            session_id (str): The ID of this session.
            device_id (int): The ID of the device (remote machine) we're connected to.
            session_data (dict): Additional session data.
        """
        self.session_id = session_id
        self.device_id = device_id
        self._cblr_manager = cblr_manager
        self._cb = cblr_manager._cb
        # TODO: refcount should be in a different object in the scheduler
        self._refcount = 1
        self._closed = False

        self.session_data = session_data
        self.os_type = None
        self.cblr_base = self._cblr_manager.cblr_base

    def __enter__(self):
        """Enter the Live Response session context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the Live Response session context.

        Args:
            exc_type (str): Exception type, if any.
            exc_val (Exception): Exception value, if any.
            exc_tb (str): Exception traceback, if any.
        """
        self.close()

    def close(self):
        """Close the Live Response session."""
        self._cblr_manager.close_session(self.device_id, self.session_id)
        self._closed = True

    def get_session_archive(self):
        """
        Get the archive data of the current session.

        Returns:
            object: Contains the archive data of the current session.
        """
        response = self._cb.session.get("{cblr_base}/session/{0}/archive".format(self.session_id,
                                                                                 cblr_base=self.cblr_base), stream=True)
        response.raw.decode_content = True
        return response.raw

    #
    # File operations
    #
    def get_raw_file(self, file_name, timeout=None, delay=None):
        """
        Retrieve contents of the specified file on the remote machine.

        Args:
            file_name (str): Name of the file to be retrieved.
            timeout (int): Timeout for the operation.
            delay (float): Delay in seconds to wait before command complete.

        Returns:
            object: Contains the data of the file.
        """
        data = {"name": "get file", "object": file_name}

        resp = self._lr_post_command(data).json()
        file_id = resp.get('file_id', None)
        command_id = resp.get('id', None)

        self._poll_command(command_id, timeout=timeout, delay=delay)
        response = self._cb.session.get("{cblr_base}/session/{0}/file/{1}/content".format(self.session_id,
                                                                                          file_id,
                                                                                          cblr_base=self.cblr_base),
                                        stream=True)
        response.raw.decode_content = True
        return response.raw

    def get_file(self, file_name, timeout=None, delay=None):
        """
        Retrieve contents of the specified file on the remote machine.

        Args:
            file_name (str): Name of the file to be retrieved.
            timeout (int): Timeout for the operation.
            delay (float): Delay in seconds to wait before command complete.

        Returns:
            str: Contents of the specified file.
        """
        fp = self.get_raw_file(file_name, timeout=timeout, delay=delay)
        content = fp.read()
        fp.close()

        return content

    def delete_file(self, filename):
        """
        Delete the specified file name on the remote machine.

        Args:
            filename (str): Name of the file to be deleted.
        """
        data = {"name": "delete file", "object": filename}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def put_file(self, infp, remote_filename):
        r"""
        Create a new file on the remote machine with the specified data.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     lr_session.put_file(open("test.txt", "rb"), r"c:\test.txt")

        Args:
            infp (object): Python file-like containing data to upload to the remote endpoint.
            remote_filename (str): File name to create on the remote endpoint.
        """
        data = {"name": "put file", "object": remote_filename}
        file_id = self._upload_file(infp)
        data["file_id"] = file_id

        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def list_directory(self, dir_name):
        r"""
        List the contents of a directory on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     pprint.pprint(lr_session.list_directory('C:\\\\temp\\\\'))
        [{u'attributes': [u'DIRECTORY'],
          u'create_time': 1471897244,
          u'filename': u'.',
          u'last_access_time': 1476390670,
          u'last_write_time': 1476390670,
          u'size': 0},
         {u'attributes': [u'DIRECTORY'],
          u'create_time': 1471897244,
          u'filename': u'..',
          u'last_access_time': 1476390670,
          u'last_write_time': 1476390670,
          u'size': 0},
         {u'attributes': [u'ARCHIVE'],
          u'create_time': 1476390668,
          u'filename': u'test.txt',
          u'last_access_time': 1476390668,
          u'last_write_time': 1476390668,
          u'size': 0}]

        Args:
            dir_name (str): Directory to list.  This parameter should end with the path separator.

        Returns:
            list: A list of dicts, each one describing a directory entry.
        """
        data = {"name": "directory list", "object": dir_name}
        resp = self._lr_post_command(data).json()
        command_id = resp.get("id")
        return self._poll_command(command_id).get("files", [])

    def create_directory(self, dir_name):
        """
        Create a directory on the remote machine.

        Args:
            dir_name (str): The new directory name.
        """
        data = {"name": "create directory", "object": dir_name}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def _pathsep(self):
        """
        Return the path separator used on the target node.

        Returns:
            str: Path separator used on the target node.
        """
        if self.os_type == 1:
            # Windows
            return "\\"
        # Unix/Mac
        return '/'

    def _path_compose(self, base, new_component, add_end=False):
        """
        Compose a new path based on a base and a new component.

        Args:
            base (str): The base path to be used.
            new_component (str): The new component to be appended.
            add_end (bool): True to add an extra path separator at the end. Default False.

        Returns:
            str: The composed path.
        """
        sep = self._pathsep()
        rc = [base]
        if not base.endswith(sep):
            rc.append(sep)
        rc.append(new_component)
        if add_end:
            rc.append(sep)
        return "".join(rc)

    def _path_islink(self, fi):
        """
        Determine if the path is a link. Not implemented.

        Args:
            fi (str): File to check.

        Returns:
            bool: True if the file is a link, False if not.
        """
        # TODO: implement
        return False

    def walk(self, top, topdown=True, onerror=None, followlinks=False):
        r"""
        Perform a full directory walk with recursion into subdirectories on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     for entry in lr_session.walk(directory_name):
        ...         print(entry)
        ('C:\\temp\\', [u'dir1', u'dir2'], [u'file1.txt'])

        Args:
            top (str): Directory to recurse on.
            topdown (bool): If True, start output from top level directory.
            onerror (func): Callback if an error occurs. This function is called with one argument (the exception
                that occurred).
            followlinks (bool): True to follow symbolic links.

        Returns:
            list: List of tuples containing directory name, subdirectory names, file names.
        """
        try:
            allfiles = self.list_directory(self._path_compose(top, '*'))
        except Exception as err:
            if onerror is not None:
                onerror(err)
            return

        dirnames = []
        filenames = []

        for fn in allfiles:
            if "DIRECTORY" in fn["attributes"]:
                if fn["filename"] not in (".", ".."):
                    dirnames.append(fn)
            else:
                filenames.append(fn)

        if topdown:
            yield top, [fn["filename"] for fn in dirnames], [fn["filename"] for fn in filenames]

        for name in dirnames:
            new_path = self._path_compose(top, name['filename'], True)
            if followlinks or not self._path_islink(new_path):
                for x in self.walk(new_path, topdown, onerror, followlinks):
                    yield x
        if not topdown:
            yield top, [fn["filename"] for fn in dirnames], [fn["filename"] for fn in filenames]

    #
    # Process operations
    #

    def kill_process(self, pid):
        """
        Terminate a process on the remote machine.

        Args:
            pid (int): Process ID to be terminated.

        Returns:
            bool: True if success, False if failure.
        """
        data = {"name": "kill", "object": pid}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        try:
            self._poll_command(command_id, timeout=10, delay=0.1)
        except TimeoutError:
            return False

        return True

    def create_process(self, command_string, wait_for_output=True, remote_output_file_name=None,
                       working_directory=None, wait_timeout=30, wait_for_completion=True):
        """
        Create a new process on the remote machine with the specified command string.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     print(lr_session.create_process(r'cmd.exe /c "ping.exe 192.168.1.1"'))
        Pinging 192.168.1.1 with 32 bytes of data:
        Reply from 192.168.1.1: bytes=32 time<1ms TTL=64

        Args:
            command_string (str): Command string used for the create process operation.
            wait_for_output (bool): True to block on output from the new process (execute in foreground).
                This will also set wait_for_completion (below).
            remote_output_file_name (str): The remote output file name used for process output.
            working_directory (str): The working directory of the create process operation.
            wait_timeout (int): Timeout used for this command.
            wait_for_completion (bool): True to wait until the process is completed before returning.

        Returns:
            str: The output of the process.
        """
        # process is:
        # - create a temporary file name
        # - create the process, writing output to a temporary file
        # - wait for the process to complete
        # - get the temporary file from the endpoint
        # - delete the temporary file

        if wait_for_output:
            wait_for_completion = True

        data = {"name": "create process", "object": command_string, "wait": wait_for_completion}

        if wait_for_output and not remote_output_file_name:
            randfilename = self._random_file_name()
            data["output_file"] = randfilename

        if working_directory:
            data["working_directory"] = working_directory

        if remote_output_file_name:
            data["output_file"] = remote_output_file_name

        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        if wait_for_completion:
            self._poll_command(command_id, timeout=wait_timeout)

        if wait_for_output:
            # now the file is ready to be read

            file_content = self.get_file(data["output_file"])
            # delete the file
            self._lr_post_command({"name": "delete file", "object": data["output_file"]})

            return file_content
        else:
            return None

    def list_processes(self):
        r"""
        List currently running processes on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     print(lr_session.list_processes()[0])
        {u'command_line': u'',
         u'create_time': 1476260500,
         u'parent': 0,
         u'parent_guid': u'00000001-0000-0000-0000-000000000000',
         u'path': u'',
         u'pid': 4,
         u'proc_guid': u'00000001-0000-0004-01d2-2461a85e4546',
         u'sid': u's-1-5-18',
         u'username': u'NT AUTHORITY\\SYSTEM'}

        Returns:
            list: A list of dicts describing the processes.
        """
        data = {"name": "process list"}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        return self._poll_command(command_id).get("processes", [])

    #
    # Registry operations
    #
    # returns dictionary with 2 entries ("values" and "sub_keys")
    #  "values" is a list containing a dictionary for each registry value in the key
    #  "sub_keys" is a list containing one entry for each sub_key
    def list_registry_keys_and_values(self, regkey):
        r"""
        Enumerate subkeys and values of the specified registry key on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        >>>   pprint.pprint(lr_session.list_registry_keys_and_values('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI'))
        {'sub_keys': [u'Parameters', u'Enum'],
         'values': [{u'value_data': 0,
                     u'value_name': u'Start',
                     u'value_type': u'REG_DWORD'},
                    {u'value_data': 1,
                     u'value_name': u'Type',
                     u'value_type': u'REG_DWORD'},
                    {u'value_data': 3,
                     u'value_name': u'ErrorControl',
                     u'value_type': u'REG_DWORD'},
                    {u'value_data': u'system32\\drivers\\ACPI.sys',
                     u'value_name': u'ImagePath',
                     u'value_type': u'REG_EXPAND_SZ'},
                    {u'value_data': u'Microsoft ACPI Driver',
                     u'value_name': u'DisplayName',
                     u'value_type': u'REG_SZ'},
                    {u'value_data': u'Boot Bus Extender',
                     u'value_name': u'Group',
                     u'value_type': u'REG_SZ'},
                    {u'value_data': u'acpi.inf_x86_neutral_ddd3c514822f1b21',
                     u'value_name': u'DriverPackageId',
                     u'value_type': u'REG_SZ'},
                    {u'value_data': 1,
                     u'value_name': u'Tag',
                     u'value_type': u'REG_DWORD'}]}

        Args:
            regkey (str): The registry key to enumerate.

        Returns:
            dict: A dictionary with two keys, 'sub_keys' (a list of subkey names) and 'values' (a list of dicts
                containing value data, name, and type).
        """
        data = {"name": "reg enum key", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        raw_output = self._poll_command(command_id)
        return {'values': raw_output.get('values', []), 'sub_keys': raw_output.get('sub_keys', [])}

    # returns a list containing a dictionary for each registry value in the key
    def list_registry_values(self, regkey):
        """
        Enumerate all registry values from the specified registry key on the remote machine.

        Args:
            regkey (str): The registry key to enumerate.

        Returns:
            list: List of values for the registry key.
        """
        data = {"name": "reg enum key", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        return self._poll_command(command_id).get("values", [])

    # returns a dictionary with the registry value
    def get_registry_value(self, regkey):
        r"""
        Return the associated value of the specified registry key on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        >>>     pprint.pprint(lr_session.get_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Start'))
        {u'value_data': 0, u'value_name': u'Start', u'value_type': u'REG_DWORD'}

        Args:
            regkey (str): The registry key to retrieve.

        Returns:
            dict: A dictionary with keys of: value_data, value_name, value_type.
        """
        data = {"name": "reg query value", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        return self._poll_command(command_id).get("value", {})

    def set_registry_value(self, regkey, value, overwrite=True, value_type=None):
        r"""
        Set a registry value on the specified registry key on the remote machine.

        Example:
        >>> with c.select(Device, 1).lr_session() as lr_session:
        ...     lr_session.set_registry_value('HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\services\\\\ACPI\\\\testvalue', 1)

        Args:
            regkey (str): The registry key to set.
            value (object): The value data.
            overwrite (bool): If True, any existing value will be overwritten.
            value_type (str): The type of value.  Examples: REG_DWORD, REG_MULTI_SZ, REG_SZ
        """
        real_value = value
        if value_type is None:
            if type(value) == int:
                value_type = "REG_DWORD"
            elif type(value) == list:
                value_type = "REG_MULTI_SZ"
                real_value = [str(item) for item in list(value)]
            else:
                value_type = "REG_SZ"
                real_value = str(value)

        data = {"name": "reg set value", "object": regkey, "overwrite": overwrite, "value_type": value_type,
                "value_data": real_value}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def create_registry_key(self, regkey):
        """
        Create a new registry key on the remote machine.

        Args:
            regkey (str): The registry key to create.
        """
        data = {"name": "reg create key", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def delete_registry_key(self, regkey):
        """
        Delete a registry key on the remote machine.

        Args:
            regkey (str): The registry key to delete.
        """
        data = {"name": "reg delete key", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    def delete_registry_value(self, regkey):
        """
        Delete a registry value on the remote machine.

        Args:
            regkey (str): The registry value to delete.
        """
        data = {"name": "reg delete value", "object": regkey}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')
        self._poll_command(command_id)

    #
    # Physical memory capture
    #
    def memdump(self, local_filename, remote_filename=None, compress=False):
        """
        Perform a memory dump operation on the remote machine.

        Args:
            local_filename (str): Name of the file the memory dump will be transferred to on the local machine.
            remote_filename (str): Name of the file the memory dump will be stored in on the remote machine.
            compress (bool): True to compress the file on the remote system.
        """
        dump_object = self.start_memdump(remote_filename=remote_filename, compress=compress)
        dump_object.wait()
        dump_object.get(local_filename)
        dump_object.delete()

    def start_memdump(self, remote_filename=None, compress=True):
        """
        Start a memory dump operation on the remote machine.

        Args:
            remote_filename (str): Name of the file the memory dump will be stored in on the remote machine.
            compress (bool): True to compress the file on the remote system.

        Returns:
            LiveResponseMemdump: Controlling object for the memory dump operation.
        """
        if not remote_filename:
            remote_filename = self._random_file_name()

        data = {"name": "memdump", "object": remote_filename, "compress": compress}
        resp = self._lr_post_command(data).json()
        command_id = resp.get('id')

        if compress:
            remote_filename += ".zip"

        return LiveResponseMemdump(self, command_id, remote_filename)

    def _random_file_name(self):
        randfile = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(12)])
        if self.os_type == 1:
            workdir = 'c:\\windows\\temp'
        else:
            workdir = '/tmp'

        return self._path_compose(workdir, f'cblr.{randfile}.tmp')

    def _poll_command(self, command_id, **kwargs):
        return poll_status(self._cb, "{cblr_base}/session/{0}/command/{1}".format(self.session_id, command_id,
                                                                                  cblr_base=self.cblr_base),
                           **kwargs)

    def _upload_file(self, fp):
        resp = self._cb.session.post("{cblr_base}/session/{0}/file".format(self.session_id, cblr_base=self.cblr_base),
                                     files={"file": fp}).json()
        return resp.get('id')

    def _lr_post_command(self, data):
        retries = self.MAX_RETRY_COUNT

        if "name" in data and data["name"] not in self.session_data["supported_commands"]:
            raise ApiError("Command {0} not supported by this device".format(data["name"]))

        while retries:
            try:
                data["session_id"] = self.session_id
                resp = self._cb.post_object("{cblr_base}/session/{0}/command".format(self.session_id,
                                                                                     cblr_base=self.cblr_base), data)
            except ObjectNotFoundError as e:
                if e.message.startswith("Device") or e.message.startswith("Session"):
                    self.session_id, self.session_data = self._cblr_manager._get_or_create_session(self.device_id)
                    retries -= 1
                    continue
                else:
                    try:
                        error_message = json.loads(e.message)
                        if error_message["status"] == "NOT_FOUND":
                            self.session_id, self.session_data = \
                                self._cblr_manager._get_or_create_session(self.device_id)
                            retries -= 1
                            continue
                    except Exception:
                        pass
                    raise ApiError("Received 404 error from server: {0}".format(e.message))
            else:
                return resp

        raise TimeoutError(message="Command {0} failed after {1} retries".format(data["name"], self.MAX_RETRY_COUNT))


class LiveResponseMemdump(object):
    """Object managing a memory dump on a remote machine."""

    def __init__(self, lr_session, memdump_id, remote_filename):
        """
        Initialize the LiveResponseMemdump.

        Args:
            lr_session (Session): The Live Response session to the machine doing the memory dump.
            memdump_id (str): The ID of the memory dump being performed.
            remote_filename (str): The file name the memory dump will be stored in on the remote machine.
        """
        self.lr_session = lr_session
        self.memdump_id = memdump_id
        self.remote_filename = remote_filename
        self._done = False
        self._error = None

    def get(self, local_filename):
        """
        Retrieve the remote memory dump to a local file.

        Args:
            local_filename (str): Filename locally that will receive the memory dump.
        """
        if not self._done:
            self.wait()
        if self._error:
            raise self._error
        src = self.lr_session.get_raw_file(self.remote_filename, timeout=3600, delay=5)
        dst = open(local_filename, "wb")
        shutil.copyfileobj(src, dst)

    def wait(self):
        """Wait for the remote memory dump to complete."""
        self.lr_session._poll_command(self.memdump_id, timeout=3600, delay=5)
        self._done = True

    def delete(self):
        """Delete the memory dump file."""
        self.lr_session.delete_file(self.remote_filename)


def jobrunner(callable, cb, device_id):
    """
    Wrap a callable object with a live response session.

    Args:
        callable (object): The object to be wrapped.
        cb (BaseAPI): The CBC SDK object reference.
        device_id (int): The device ID to use to get the session.

    Returns:
        object: The wrapped object.
    """
    from cbc_sdk.endpoint_standard import Device
    with cb.select(Device, device_id).lr_session() as sess:
        return callable(sess)


class WorkItem(object):
    """Work item for scheduling."""

    def __init__(self, fn, device_id):
        """
        Initialize the WorkItem.

        Args:
            fn (func): The function to be called to do the actual work.
            device_id (object): The device ID or Device object the work item is directed for.
        """
        self.fn = fn
        from cbc_sdk.endpoint_standard import Device
        if isinstance(device_id, Device):
            self.device_id = device_id.deviceId
        else:
            self.device_id = int(device_id)

        self.future = _base.Future()


class CompletionNotification(object):
    """The notification that an operation is complete."""

    def __init__(self, device_id):
        """
        Initialize the CompletionNotification.

        Args:
            device_id (int): The device ID this notification is for.
        """
        self.device_id = device_id


class WorkerStatus(object):
    """Holds the status of an individual worker."""

    def __init__(self, device_id, status="ready", exception=None):
        """
        Initialize the WorkerStatus.

        Args:
            device_id (int): The device ID this status is for.
            status (str): The current status value.
            exception (Exception): Any exception that happened.
        """
        self.device_id = device_id
        self.status = status
        self.exception = exception


class JobWorker(threading.Thread):
    """Thread object that executes individual Live Response jobs."""

    def __init__(self, cb, device_id, result_queue):
        """
        Initialize the JobWorker.

        Args:
            cb (BaseAPI): The CBC SDK object reference.
            device_id (int): The ID of the device being used.
            result_queue (Queue): The queue where results are placed.
        """
        super(JobWorker, self).__init__()
        self.cb = cb
        self.device_id = device_id
        self.job_queue = queue.Queue()
        self.lr_session = None
        self.result_queue = result_queue

    def run(self):
        """Execute the job worker."""
        try:
            self.lr_session = self.cb.live_response.request_session(self.device_id)
            self.result_queue.put(WorkerStatus(self.device_id, status="ready"))

            while True:
                work_item = self.job_queue.get(block=True)
                if not work_item:
                    self.job_queue.task_done()
                    return

                self.run_job(work_item)
                self.result_queue.put(CompletionNotification(self.device_id))
                self.job_queue.task_done()
        except Exception as e:
            self.result_queue.put(WorkerStatus(self.device_id, status="error", exception=e))
        finally:
            if self.lr_session:
                self.lr_session.close()
            self.result_queue.put(WorkerStatus(self.device_id, status="exiting"))

    def run_job(self, work_item):
        """
        Execute an individual WorkItem.

        Args:
            work_item (WorkItem): The work item to execute.
        """
        try:
            work_item.future.set_result(work_item.fn(self.lr_session))
        except Exception as e:
            work_item.future.set_exception(e)


class LiveResponseJobScheduler(threading.Thread):
    """Thread that schedules Live Response jobs."""

    daemon = True

    def __init__(self, cb, max_workers=10):
        """
        Initialize the LiveResponseJobScheduler.

        Args:
            cb (BaseAPI): The CBC SDK object reference.
            max_workers (int): Maximum number of JobWorker threads to use.
        """
        super(LiveResponseJobScheduler, self).__init__()
        self._cb = cb
        self._job_workers = {}
        self._idle_workers = set()
        self._unscheduled_jobs = defaultdict(list)
        self._max_workers = max_workers
        self.schedule_queue = queue.Queue()

    def run(self):
        """Execute the job scheduler."""
        log.debug("Starting Live Response Job Scheduler")

        while True:
            log.debug("Waiting for item on Scheduler Queue")
            item = self.schedule_queue.get(block=True)
            log.debug("Got item: {0}".format(item))
            if isinstance(item, WorkItem):
                # new WorkItem available
                self._unscheduled_jobs[item.device_id].append(item)
            elif isinstance(item, CompletionNotification):
                # job completed
                self._idle_workers.add(item.device_id)
            elif isinstance(item, WorkerStatus):
                if item.status == "error":
                    log.error("Error encountered by JobWorker[{0}]: {1}".format(item.device_id,
                                                                                item.exception))
                elif item.status == "exiting":
                    log.debug("JobWorker[{0}] has exited, waiting...".format(item.device_id))
                    self._job_workers[item.device_id].join()
                    log.debug("JobWorker[{0}] deleted".format(item.device_id))
                    del self._job_workers[item.device_id]
                    try:
                        self._idle_workers.remove(item.device_id)
                    except KeyError:
                        pass
                elif item.status == "ready":
                    log.debug("JobWorker[{0}] now ready to accept jobs, session established".format(item.device_id))
                    self._idle_workers.add(item.device_id)
                else:
                    log.debug("Unknown status from JobWorker[{0}]: {1}".format(item.device_id, item.status))
            else:
                log.debug("Received unknown item on the scheduler Queue, exiting")
                # exiting the scheduler if we get None
                # TODO: wait for all worker threads to exit
                return

            self._schedule_jobs()

    def _schedule_jobs(self):
        log.debug("Entering scheduler")

        # First, see if there are new jobs to schedule on idle workers.
        self._schedule_existing_workers()

        # If we have jobs scheduled to run on devices with no current associated worker, let's spawn new ones.
        if set(self._unscheduled_jobs.keys()) - self._idle_workers:
            self._cleanup_idle_workers()
            self._spawn_new_workers()
            self._schedule_existing_workers()

    def _cleanup_idle_workers(self, max=None):
        if not max:
            max = self._max_workers

        for device in list(self._idle_workers)[:max]:
            log.debug("asking worker for device id {0} to exit".format(device))
            self._job_workers[device].job_queue.put(None)

    def _schedule_existing_workers(self):
        log.debug("There are idle workers for device ids {0}".format(self._idle_workers))

        intersection = self._idle_workers.intersection(set(self._unscheduled_jobs.keys()))

        log.debug("{0} jobs ready to execute in existing execution slots".format(len(intersection)))

        for device in intersection:
            item = self._unscheduled_jobs[device].pop(0)
            self._job_workers[device].job_queue.put(item)
            self._idle_workers.remove(item.device_id)

        self._cleanup_unscheduled_jobs()

    def _cleanup_unscheduled_jobs(self):
        marked_for_deletion = []
        for k in self._unscheduled_jobs.keys():
            if len(self._unscheduled_jobs[k]) == 0:
                marked_for_deletion.append(k)

        for k in marked_for_deletion:
            del self._unscheduled_jobs[k]

    def submit_job(self, work_item):
        """
        Submit a new job to be processed.

        Args:
            work_item (WorkItem): New job to be processed.
        """
        self.schedule_queue.put(work_item)

    def _spawn_new_workers(self):
        if len(self._job_workers) >= self._max_workers:
            return

        schedule_max = self._max_workers - len(self._job_workers)

        from cbc_sdk.endpoint_standard import Device
        devices = [s for s in self._cb.select(Device) if s.deviceId in self._unscheduled_jobs
                   and s.deviceId not in self._job_workers and s.status == "Online"]  # noqa: W503
        devices_to_schedule = sorted(devices, key=lambda x: (
            int(x.num_storefiles_bytes) + int(x.num_eventlog_bytes), x.next_checkin_time
        ))[:schedule_max]

        log.debug("Spawning new workers to handle these devices: {0}".format(devices_to_schedule))
        for device in devices_to_schedule:
            log.debug("Spawning new JobWorker for device id {0}".format(device.deviceId))
            self._job_workers[device.deviceId] = JobWorker(self._cb, device.deviceId, self.schedule_queue)
            self._job_workers[device.deviceId].start()


class CbLRManagerBase(object):
    """Live Response manager object."""

    cblr_base = ""  # override in subclass for each product
    cblr_session_cls = NotImplemented  # override in subclass for each product

    def __init__(self, cb, timeout=30, keepalive_sessions=False):
        """
        Initialize the CbLRManagerBase object.

        Args:
            cb (BaseAPI): The CBC SDK object reference.
            timeout (int): Timeout to use for requests, in seconds.
            keepalive_sessions (bool): If True, "ping" sessions occasionally to ensure they stay alive.
        """
        self._timeout = timeout
        self._cb = cb
        self._sessions = {}
        self._session_lock = threading.RLock()
        self._keepalive_sessions = keepalive_sessions
        self._init_poll_delay = 1
        self._init_poll_timeout = 360

        if keepalive_sessions:
            self._cleanup_thread_running = True
            self._cleanup_thread_event = threading.Event()
            self._cleanup_thread = threading.Thread(target=self._session_keepalive_thread)
            self._cleanup_thread.daemon = True
            self._cleanup_thread.start()

        self._job_scheduler = None

    def submit_job(self, job, device):
        """
        Submit a new job to be executed as a Live Response.

        Args:
            job (object): The job to be scheduled.
            device (int): ID of the device to use for job execution.

        Returns:
            Future: A reference to the running job.
        """
        if self._job_scheduler is None:
            # spawn the scheduler thread
            self._job_scheduler = LiveResponseJobScheduler(self._cb)
            self._job_scheduler.start()

        work_item = WorkItem(job, device)
        self._job_scheduler.submit_job(work_item)
        return work_item.future

    def _maintain_sessions(self):
        delete_list = []
        with self._session_lock:
            for session in iter(self._sessions.values()):
                if not self._cleanup_thread_running:
                    break
                if session._refcount == 0:
                    delete_list.append(session.device_id)
                else:
                    try:
                        self._send_keepalive(session.session_id)
                    except ObjectNotFoundError:
                        log.debug("Session {0} for device {1} not valid any longer, removing from cache"
                                  .format(session.session_id, session.device_id))
                        delete_list.append(session.device_id)
                    except Exception:
                        log.debug(("Keepalive on session {0} (device {1}) failed with unknown error, "
                                   "removing from cache").format(session.session_id, session.device_id))
                        delete_list.append(session.device_id)

            for device_id in delete_list:
                self._close_session(self._sessions[device_id].session_id)
                del self._sessions[device_id]

    def _session_keepalive_thread(self):
        log.debug("Starting Live Response scheduler cleanup task")
        while self._cleanup_thread_running:
            self._cleanup_thread_event.wait(self._timeout)
            if self._cleanup_thread_running:
                self._maintain_sessions()
        log.debug("Ending Live Response scheduler cleanup task")

    def stop_keepalive_thread(self):
        """Stops the keepalive thread."""
        if self._keepalive_sessions:
            self._cleanup_thread_running = False
            self._cleanup_thread_event.set()

    def request_session(self, device_id):
        """
        Initiate a new Live Response session.

        Args:
            device_id (int): The device ID to use.

        Returns:
            CbLRSessionBase: The new Live Response session.
        """
        if self._keepalive_sessions:
            with self._session_lock:
                if device_id in self._sessions:
                    session = self._sessions[device_id]
                    self._sessions[device_id]._refcount += 1
                else:
                    session_id, session_data = self._get_or_create_session(device_id)
                    session = self.cblr_session_cls(self, session_id, device_id, session_data=session_data)
                    self._sessions[device_id] = session
        else:
            session_id, session_data = self._get_or_create_session(device_id)
            session = self.cblr_session_cls(self, session_id, device_id, session_data=session_data)

        return session

    def close_session(self, device_id, session_id):
        """
        Close the specified Live Response session.

        Args:
            device_id (int): ID of the device.
            session_id (int): ID of the session.
        """
        if self._keepalive_sessions:
            with self._session_lock:
                try:
                    self._sessions[device_id]._refcount -= 1
                except KeyError:
                    pass
        else:
            self._close_session(session_id)

    def _send_keepalive(self, session_id):
        log.debug("Sending keepalive message for session id {0}".format(session_id))
        self._cb.get_object("{cblr_base}/session/{0}/keepalive".format(session_id, cblr_base=self.cblr_base))


class LiveResponseSession(CbLRSessionBase):
    """Public face of the Live Response session object."""

    def __init__(self, cblr_manager, session_id, device_id, session_data=None):
        """
        Initializes the LiveResponseSession.

        Args:
            cblr_manager (LiveResponseSessionManager): Reference to the session manager.
            session_id (str): The ID of this session.
            device_id (int): The ID of the device (remote machine) we're connected to.
            session_data (dict): Additional session data.
        """
        super(LiveResponseSession, self).__init__(cblr_manager, session_id, device_id, session_data=session_data)
        from cbc_sdk.endpoint_standard import Device
        device_info = self._cb.select(Device, self.device_id)
        self.os_type = OS_LIVE_RESPONSE_ENUM.get(device_info.deviceType, None)


class LiveResponseSessionManager(CbLRManagerBase):
    """Session manager for Live Response sessions."""
    cblr_base = "/integrationServices/v3/cblr"
    cblr_session_cls = LiveResponseSession

    def submit_job(self, job, device):
        """
        Submit a job for execution by the job scheduler.

        Args:
            job (func): The job function to be executed.
            device (object): The device ID or Device object the job will be executed on.

        Returns:
            Future: A Future that will allow waiting until the job is complete.
        """
        if self._job_scheduler is None:
            # spawn the scheduler thread
            self._job_scheduler = LiveResponseJobScheduler(self._cb)
            self._job_scheduler.start()

        work_item = WorkItem(job, device)
        self._job_scheduler.submit_job(work_item)
        return work_item.future

    def _get_or_create_session(self, device_id):
        session_id = self._create_session(device_id)

        try:
            res = poll_status(self._cb, "{cblr_base}/session/{0}".format(session_id, cblr_base=self.cblr_base),
                              desired_status="ACTIVE", delay=self._init_poll_delay, timeout=self._init_poll_timeout)
        except Exception:
            # "close" the session, otherwise it will stay in a pending state
            self._close_session(session_id)

            # the Cb server will return a 404 if we don't establish a session in time, so convert this to a "timeout"
            raise TimeoutError(uri="{cblr_base}/session/{0}".format(session_id, cblr_base=self.cblr_base),
                               message="Could not establish session with device {0}".format(device_id),
                               error_code=404)
        else:
            return session_id, res

    def _close_session(self, session_id):
        try:
            self._cb.put_object("{cblr_base}/session".format(cblr_base=self.cblr_base),
                                {"session_id": session_id, "status": "CLOSE"})
        except Exception:
            pass

    def _create_session(self, device_id):
        response = self._cb.post_object("{cblr_base}/session/{0}".format(device_id, cblr_base=self.cblr_base),
                                        {"device_id": device_id}).json()
        session_id = response["id"]
        return session_id


class GetFileJob(object):
    """Object that retrieves a file via Live Response."""

    def __init__(self, file_name):
        """
        Initialize the GetFileJob.

        Args:
            file_name (str): The name of the file to be fetched.
        """
        self._file_name = file_name

    def run(self, session):
        """
        Execute the file transfer.

        Args:
            session (CbLRSessionBase): The Live Response session being used.

        Returns:
            str: The contents of the file being retrieved.
        """
        return session.get_file(self._file_name)


# TODO: adjust the polling interval and also provide a callback function to report progress
def poll_status(cb, url, desired_status="complete", timeout=None, delay=None):
    """
    Poll the status of a Live Response query.

    Args:
        cb (BaseAPI): The CBC SDK object reference.
        url (str): The URL to poll.
        desired_status (str): The status we're looking for.
        timeout (int): The timeout value in seconds.
        delay (float): The delay between attempts in seconds.

    Returns:
        object: The result of the Live Response query that has the desired status.

    Raises:
        LiveResponseError: If an error response was encountered.
    """
    start_time = time.time()
    status = None

    if not timeout:
        timeout = 120
    if not delay:
        delay = 0.5

    while status != desired_status and time.time() - start_time < timeout:
        res = cb.get_object(url)
        log.error(f"url: {url} -> status: {res['status']}")
        if res["status"] == desired_status:
            log.debug(json.dumps(res))
            return res
        elif res["status"] == "error":
            raise LiveResponseError(res)
        else:
            time.sleep(delay)

    raise TimeoutError(uri=url, message="timeout polling for Live Response")


if __name__ == "__main__":
    from cbc_sdk import CBCloudAPI
    from cbc_sdk.platform import Device
    import logging

    root = logging.getLogger()
    root.addHandler(logging.StreamHandler())

    logging.getLogger("cbc_sdk").setLevel(logging.DEBUG)

    c = CBCloudAPI()
    j = GetFileJob(r"c:\test.txt")
    with c.select(Device, 3).lr_session() as lr_session:
        file_contents = lr_session.get_file(r"c:\test.txt")

    future = c.live_response.submit_job(j.run, 3)
    wait([future, ])
    print(future.result())
