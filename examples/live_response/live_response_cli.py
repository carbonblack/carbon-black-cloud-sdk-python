#!/usr/bin/env python

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Example command-line interface to Live Response."""

import sys
from datetime import datetime
import cmd
import logging
import ntpath
import shutil
import subprocess
from optparse import OptionParser

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device

FORMAT = '%Y-%m-%dT%H:%M:%SZ'

log = logging.getLogger(__name__)


class QuitException(Exception):
    """Exception raised when we want to quit the application."""
    pass


class CliArgsException(Exception):
    """Exception raised if there are errors in the arguments to a command."""
    pass


class CliHelpException(Exception):
    """Exception raised if we're invoking help."""
    pass


class CliAttachError(Exception):
    """Exception raised if we're not attached to a session."""
    pass


def split_cli(line):
    """
    Split the command line into individual tokens.

    we'd like to use shlex.split() but that doesn't work well for
    windows types of things.  for now we'll take the easy approach
    and just split on space. We'll then cycle through and look for leading
    quotes and join those lines
    """
    parts = line.split(' ')
    final = []

    while len(parts) > 0:

        tok = parts.pop(0)
        if (tok[:1] == '"'):
            tok = tok[1:]
            next = parts.pop(0)
            while (next[-1:] != '"' and len(parts) > 0):
                tok += ' ' + next
                next = parts.pop(0)

            if (next[-1:] == '"'):
                tok += ' ' + next[:-1]

        final.append(tok)
    return final


class CliArgs (OptionParser):
    """Command line arguments."""
    def __init__(self, usage=''):
        """Initialize the CliArgs object."""
        OptionParser.__init__(self, add_help_option=False, usage=usage)

        self.add_option('-h', '--help', action='store_true', help='Display this help message.')

    def parse_line(self, line):
        """Parse a command line entered from the input."""
        args = split_cli(line)
        return self.parse_args(args)

    def parse_args(self, args, values=None):
        """Parse the arguments to a command."""
        (opts, args) = OptionParser.parse_args(self, args=args, values=values)

        if (opts.help):
            self.print_help()
            raise CliHelpException()

        return (opts, args)

    def error(self, msg):
        """Raise an error message."""
        raise CliArgsException(msg)


class CblrCli(cmd.Cmd):
    """The primary command-line interpreter class for the Live Response CLI."""
    def __init__(self, cb, connect_callback):
        """
        Create a CbLR Command Line class

        Args:
            cb (CBCloudAPI): Connection to the Carbon Black Cloud SDK.
            connect_callback (func): Callable to get a device object from the ``connect`` command.
        """
        cmd.Cmd.__init__(self)

        # global variables
        # apply regardless of session state
        self.cb = cb
        self.connect_callback = connect_callback

        lr_session = None
        self.lr_session = lr_session

        self.reset()

    @property
    def prompt(self):
        """Display the command prompt."""
        if not self.lr_session:
            return "(unattached)> "
        else:
            return "{0}\\> ".format(self.cwd)

    def emptyline(self):
        """Called when we get an empty line of input."""
        pass

    def cmdloop(self, intro=None):
        """The main command loop of the application."""
        while True:
            try:
                cmd.Cmd.cmdloop(self, intro)
            except CliHelpException:
                pass
            except QuitException:
                break
            except KeyboardInterrupt:
                break
            except CliAttachError:
                print("You must attach to a session")
                continue
            except CliArgsException as e:
                print("Error parsing arguments!\n {}".format(e))
                continue
            except Exception as e:
                print("Error: {}".format(e))
                continue

        if self.lr_session:
            self.lr_session.close()

    def _quit(self):
        raise QuitException("quit")

    def _is_path_absolute(self, path):

        if path.startswith('\\\\'):
            return True

        if (path[0].isalpha() and path[1:3] == ':\\'):
            return True

        return False

    def _is_path_drive_relative(self, path):

        if path == '\\':
            return True

        if path[0] == '\\' and path[1] != '\\':
            return True

        return False

    def _file_path_fixup(self, path):
        """
        Fix up a file path.

        We have a pseudo-cwd that we use to
        base off all commands.  This means we
        need to figure out if a given path is relative,
        absolute, or file relative and calculate against
        the pseudo cwd.

        This function takes in a given file path arguemnt
        and performs the fixups.
        """
        if (self._is_path_absolute(path)):
            return path
        elif (self._is_path_drive_relative(path)):
            return self.cwd[:2] + path
        else:
            return ntpath.join(self.cwd + '\\', path)

    def _stat(self, path):
        """
        Look to see if a given path exists on the device and whether that is a file or directory.

        Args:
            path (str): A device path.

        Returns:
            str: None, "dir", or "file".
        """
        if path.endswith('\\'):
            path = path[:-1]

        ret = self.lr_session.list_directory(path)
        if not ret or not len(ret):
            return None

        if 'DIRECTORY' in ret[0]['attributes']:
            return "dir"
        else:
            return "file"

    ################################
    # pseudo commands and session commands
    #
    # they don't change state on the device
    # (except start a session)
    #####################

    def _needs_attached(self):
        if not self.lr_session:
            raise CliAttachError()

    def do_cd(self, line):
        """
        Pseudo Command: cd

        Description:
        Change the psuedo current working directory

        Note: The shell keeps a pseudo working directory
        that allows the user to change directory without
        changing the directory of the working process on device.

        Format:
        cd <Directory>
        """
        self._needs_attached()

        path = self._file_path_fixup(line)
        path = ntpath.abspath(path)
        type = self._stat(path)
        if (type != "dir"):
            print("Error: Path {} does not exist".format(path))
            return
        else:
            self.cwd = path

        # cwd never has a trailing \
        if self.cwd[-1:] == '\\':
            self.cwd = self.cwd[:-1]

        log.info("Changed directory to {0}".format(self.cwd))

    def do_cat(self, line):
        """
        Pseudo Command: cat

        Description:
        Displays the contents of a remote file (writes them to stdout).

        Format:
        cat <filename>
        """
        self._needs_attached()
        gfile = self._file_path_fixup(line)
        shutil.copyfileobj(self.lr_session.get_raw_file(gfile), sys.stdout.buffer)

    def do_pwd(self, line):
        """
        Pseudo Command: pwd

        Description:
        Print the pseudo current working directory

        Note: The shell keeps a pseudo working directory
        that allows the user to change directory without
        changing the directory of the working process on device.

        Format:
        pwd
        """
        self._needs_attached()

        if (len(self.cwd) == 2):
            # it's c: - put a slash on the end
            print(self.cwd + '\\')
        else:
            print(self.cwd)
        print()

    def do_connect(self, line):
        """
        Command: connect

        Description:
        Connect to a device given the device ID or the device hostname.

        Format:
        connect DEVICE_ID | DEVICE_HOSTNAME
        """
        if not line:
            raise CliArgsException("Need argument: device ID or hostname")

        device = self.connect_callback(self.cb, line)
        self.lr_session = device.lr_session()

        print("Session: {0}".format(self.lr_session.session_id))
        print("  Available Drives: {}".format(' '.join(self.lr_session.session_data.get('drives', []))))

        # look up supported commands
        print("  Supported Commands: {}".format(', '.join(self.lr_session.session_data.get('supported_commands', []))))
        print("  Working Directory: {}".format(self.cwd))

        log.info("Attached to device {0}".format(device._model_unique_id))

    def do_detach(self, line):
        """Detaches the current Live Response connection."""
        self.reset()

    def reset(self):
        """Closes the session and resets the idea of the current working directory."""
        self.cwd = "c:"

        if not self.lr_session:
            return

        self.lr_session.close()
        self.lr_session = None

    #############################
    # real commands
    #
    # these change state on the senesor
    ##############################

    def do_ps(self, line):
        """
        Command: ps

        Description:
        List the processes running on the device.

        Format:
        ps [OPTIONS]

        OPTIONS:
        -v  - Display verbose info about each process
        -p <Pid> - Display only the given pid
        """
        self._needs_attached()

        p = CliArgs(usage='ps [OPTIONS]')
        p.add_option('-v', '--verbose', default=False, action='store_true',
                     help='Display verbose info about each process')
        p.add_option('-p', '--pid', default=None, help='Display only the given pid')
        (opts, args) = p.parse_line(line)

        if opts.pid:
            opts.pid = int(opts.pid)

        processes = self.lr_session.list_processes()

        for p in processes:
            if (opts.pid and p['process_pid'] == opts.pid) or opts.pid is None:
                if opts.verbose:
                    print("Process: {:d5} : {}".format(p['process_pid'], ntpath.basename(p['process_path'])))
                    print("  CreateTime:  {} (GMT)".format(self._time_dir_gmt(p['process_create_time'])))
                    print("  ParentPid:   {}".format(p['parent_pid']))
                    print("  ParentGuid:  {}".format(p.get('parent_guid')))
                    print("  SID:         {}".format(p['sid'].upper()))
                    print("  UserName:    {}".format(p['process_username']))
                    print("  ExePath:     {}".format(p['process_path']))
                    print("  CommandLine: {}".format(p['process_cmdline']))
                    print()
                else:
                    print("{:5}  {:<30} {:<20}".format(p['process_pid'],
                                                       ntpath.basename(p['process_path']),
                                                       p['process_username']))

        if not opts.verbose:
            print()

    def do_exec(self, line):
        """
        Command: exec

        Description:
        Execute a process on the device.  This assumes the executable is
        already on the device.

        Format:
        exec [OPTS] [process command line and arguments]

        where OPTS are:
         -o <OutputFile> - Redirect standard out and standard error to
              the given file path.
         -d <WorkingDir> - Use the following directory as the process working
              directory
         -w - Wait for the process to complete execution before returning.
        """
        self._needs_attached()
        # note: option parsing is VERY specific to ensure command args are left
        # as untouched as possible

        OPTS = ['-o', '-d', '-w']
        optOut = None
        optWorkDir = None
        optWait = False

        parts = line.split(' ')
        doParse = True
        while (doParse):
            tok = parts.pop(0)
            if (tok in OPTS):
                if tok == '-w':
                    optWait = True
                if tok == '-o':
                    optOut = parts.pop(0)
                if tok == '-d':
                    optWorkDir = parts.pop(0)
            else:
                doParse = False

        exe = tok

        # ok - now the command (exe) is in tok
        # we need to do some crappy path manipulation
        # to see what we are supposed to execute
        if (self._is_path_absolute(exe)):
            pass
            # do nothing
        elif (self._is_path_drive_relative(exe)):
            # append the current dirve
            exe = self.cwd[:2] + exe
        else:
            # is relative (2 sub-cases)
            ret = self._stat(ntpath.join(self.cwd, exe))
            if (ret == "file"):
                # then a file exist in the current working
                # directory that matches the exe name - execute it
                exe = ntpath.join(self.cwd, exe)
            else:
                # the cwd + exe does not exist - let windows
                # resolve the path
                pass

        # re-format the list and put tok at the front
        if (len(parts) > 0):
            cmdline = exe + ' ' + ' '.join(parts)
        else:
            cmdline = exe

        if not optWorkDir:
            optWorkDir = self.cwd

        ret = self.lr_session.create_process(cmdline,
                                             wait_for_output=optWait,
                                             remote_output_file_name=optOut,
                                             working_directory=optWorkDir)

        if (optWait):
            print(ret)

    def do_get(self, line):
        """
        Command: get

        Description:
        Get (copy) a file, or parts of file, from the device.

        Format:
        get [OPTIONS] <RemotePath> <LocalPath>

        where OPTIONS are:
        -o, --offset : The offset to start getting the file at
        -b, --bytes : How many bytes of the file to get.  The default is all bytes.
        """
        self._needs_attached()

        p = CliArgs(usage='get [OPTIONS] <RemoteFile> <LocalFile>')
        (opts, args) = p.parse_line(line)

        if len(args) != 2:
            raise CliArgsException("Wrong number of args to get command")

        with open(args[1], "wb") as fout:
            gfile = self._file_path_fixup(args[0])
            shutil.copyfileobj(self.lr_session.get_raw_file(gfile), fout)

    def do_del(self, line):
        """
        Command: del

        Description:
        Delete a file on the device

        Format:
        del <FileToDelete>
        """
        self._needs_attached()

        if line is None or line == '':
            raise CliArgsException("Must provide argument to del command")

        path = self._file_path_fixup(line)
        self.lr_session.delete_file(path)

    def do_mkdir(self, line):
        """
        Command: mkdir

        Description:
        Create a directory on the device

        Format:
        mkdir <PathToCreate>
        """
        self._needs_attached()

        if line is None or line == '':
            raise CliArgsException("Must provide argument to mkdir command")

        path = self._file_path_fixup(line)
        self.lr_session.create_directory(path)

    def do_put(self, line):
        """
        Command: put

        Description
        Put a file onto the device

        Format:
        put <LocalFile> <RemotePath>
        """
        self._needs_attached()

        argv = split_cli(line)

        if len(argv) != 2:
            raise CliArgsException("Wrong number of args to put command (need 2)")

        with open(argv[0], "rb") as fin:
            self.lr_session.put_file(fin, argv[1])

    def _time_dir_gmt(self, date_to_format):
        global FORMAT
        date = datetime.strptime(date_to_format, FORMAT)
        return date.strftime("%m/%d/%Y %I:%M:%S %p")

    def do_dir(self, line):
        """
        Command: dir

        Description
        List the contents of the current directory.

        Format:
        dir <Path>
        """
        self._needs_attached()

        if line is None or line == '':
            line = self.cwd + "\\"

        path = self._file_path_fixup(line)

        if path.endswith('\\'):
            path += '*'

        ret = self.lr_session.list_directory(path)

        print("Directory: {}\n".format(path))
        for f in ret:
            timestr = self._time_dir_gmt(f['create_time'])
            if ('DIRECTORY' in f['attributes']):
                x = '<DIR>               '
            else:
                x = '     {:15}'.format(f['size'])
            print("{}\t{} {}".format(timestr, x, f['filename']))

        print()

    def do_kill(self, line):
        """
        Command: kill

        Description:
        Kill a process on the device

        Format:
        kill <Pid>
        """
        if line is None or line == '':
            raise CliArgsException("Invalid argument passed to kill ({})".format(line))

        self.lr_session.kill_process(line)

    # call the system shell
    def do_shell(self, line):
        """
        Command: shell

        Description:
        Run a command locally and display the output

        Format:
        shell <Arguments>
        """
        print(subprocess.Popen(line, shell=True, stdout=subprocess.PIPE).stdout.read())

    # quit handlers
    def do_exit(self, line):
        """Quit the application."""
        return self._quit()

    def do_quit(self, line):
        """Quit the application."""
        return self._quit()

    def do_EOF(self, line):
        """Quit the application."""
        return self._quit()


def connect_callback(cb, line):
    """Called back when the Live Response connection is made; selects the device."""
    try:
        device_id = int(line)
    except ValueError:
        device_id = None

    if not device_id:
        q = cb.select(Device).where("name:{0}".format(line))
        device = q.first()
    else:
        device = cb.select(Device, device_id)

    return device


def main():
    """Main function for Live Response CLI script."""
    parser = build_cli_parser("Carbon Black Cloud Live Response CLI")
    parser.add_argument("--log", help="Log activity to a file", default='')
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.log:
        file_handler = logging.FileHandler(args.log)
        file_handler.setLevel(logging.DEBUG)
        log.addHandler(file_handler)

    cli = CblrCli(cb, connect_callback)
    cli.cmdloop()


if __name__ == "__main__":
    sys.exit(main())
