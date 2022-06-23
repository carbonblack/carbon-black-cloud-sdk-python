#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2021-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
To execute, a profile must be provided using the standard CBC Credentials.

Processes: Live Response
* Create sesssion
* File commands
    * Create directory
    * Create/Put file in a directory
    * List a directory
    * Walk a directory
    * Get a file
    * Delete a file
    * Delete a directory
    * Memdump
* Process commands
    * Create a process
    * List processes
    * Kill a process
* Registry commands
    * List registry keys and values
    * List registry values
    * Create registry key
    * Create registry value
    * Delete registry value
    * Delete registry key
* Close a session
"""

# Standard library imports
import os
import os.path
from os import path
from pprint import pprint
import sys

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.live_response_api import LiveResponseError, LiveResponseSessionManager
from cbc_sdk.errors import ApiError

# CONSTANTS
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
ORG_KEY = ''
HOSTNAME = ''
DEVICE_ID = 11457613

# Files constants
LOCAL_FILE = 'memdump.txt'
DIR = 'C:\\\\demo\\\\'
MEMDUMP_FILE = r"c:\memdump.txt"
FILE = r"c:\demo\test.txt"
FILE_CONTENT = 1000 * "This is just a test"

# Registry constants
KEY_PATH = 'HKCU\\Environment\\Test'
KEY_PATH_PARENT = 'HKCU\\Environment'

# Formatters
NEWLINES = 1
DELIMITER = '-'
SYMBOLS = 48


def flatten_response(response):
    """Helper function to extract only the filenames from the list directory command"""
    return [item['filename'] for item in response]


def flatten_processes_response(response):
    """Helper function to extract only pids and paths from the list processes command"""
    return [{item['process_pid']: item['process_path']} for item in response]


def flatten_processes_response_filter(response, process_name):
    """Helper function to extract only pids and paths from the list processes command"""
    return [item['process_pid'] for item in response if process_name in item['process_path']]


def asynchronous_version(cb):
    """Asynchronous commands"""
    print()
    print(11 * ' ' + 'Async Live Response Commands')
    print(SYMBOLS * DELIMITER)

    try:
        device = cb.select(Device, DEVICE_ID)
    except Exception:
        # if this is not run on dev01, pick a random active device
        devices = cb.select(Device).set_status(['ACTIVE'])
        device = devices[0]

    manager = LiveResponseSessionManager(cb)
    session_id, result = manager.request_session(device.id, async_mode=True)
    print(f'Created Session {session_id}...............OK')
    while True:
        status = manager.session_status(session_id)
        if status == 'ACTIVE':
            break
        print('Current status:', status)

    lr_session = result.result()
    print(f'Active Session {lr_session.session_id}................OK')
    print()

    print()
    print(10 * ' ' + 'Live Response Files Commands')
    print(SYMBOLS * DELIMITER)

    # those two command will not raise an exception, because they are async
    _, result1 = lr_session.create_directory(DIR, async_mode=True)
    _, result2 = lr_session.create_directory(DIR, async_mode=True)
    # create directory
    try:
        # upon getting the result, one of the commands will raise a LiveResponseError exception
        result1.result()
        result2.result()
    except LiveResponseError as ex:
        if 'ERROR_ALREADY_EXISTS' in str(ex):
            print('Command raised ERROR_ALREADY_EXISTS...........OK')
        else:
            raise
    print('Create Dir....................................OK')

    # show that test.txt is not present in that directory
    _, ldresult = lr_session.list_directory(DIR, async_mode=True)

    # upload the file on the server
    _, uresult = lr_session.put_file(open("test.txt", "r"), FILE, async_mode=True)
    uresult.result()
    print('PUT File......................................OK')

    directories = flatten_response(ldresult.result())
    assert 'test.txt' not in directories, f'Dirs: {directories}'

    # show that test.txt is present in that directory
    _, lresult = lr_session.list_directory(DIR, async_mode=True)
    directories = flatten_response(lresult.result())
    assert 'test.txt' in directories, f'Dirs: {directories}'

    # start a few commands one after the other
    _, gresult = lr_session.get_file(FILE, async_mode=True)
    g2command_id, g2result = lr_session.get_file(FILE, async_mode=True)
    _, dresult = lr_session.delete_file(FILE, async_mode=True)
    lr_session.cancel_command(g2command_id)
    print('Started async commands........................OK')

    gresult.result()
    print('GET File......................................OK')

    exc_raise = False
    try:
        g2result.result()
    except ApiError as ex:
        assert 'The command has been cancelled.' in str(ex)
        exc_raise = True
    finally:
        assert exc_raise

    # make sure the file is deleted before checking that it does not exist
    dresult.result()
    exc_raise = False
    _, result = lr_session.get_file(FILE, async_mode=True)
    try:
        result.result()
    except LiveResponseError as ex:
        assert 'ERROR_FILE_NOT_FOUND' in str(ex) or 'ERROR_PATH_NOT_FOUND' in str(ex), f'Other error {ex}'
        exc_raise = True
    finally:
        assert exc_raise

    print('DELETE File...................................OK')
    # delete the directory too
    lr_session.delete_file(DIR)
    print('DELETE Dir....................................OK')

    print()
    print(9 * ' ' + 'Live Response Process Commands')
    print(SYMBOLS * DELIMITER)

    # list processes
    _, lresult = lr_session.list_processes(async_mode=True)
    # create infinite ping, that could be killed afterwards
    _, cresult = lr_session.create_process(r'cmd.exe /c "ping.exe -t 127.0.0.1"',
                                           wait_for_completion=False,
                                           wait_for_output=False,
                                           async_mode=True)
    cresult.result()
    processes = lresult.result()

    pprint(flatten_processes_response(processes))
    print('List Processes................................OK')

    _, lresult = lr_session.list_processes(async_mode=True)
    processes = lresult.result()
    found = False
    for process in processes:
        if 'ping.exe' in process['process_path']:
            found = True

    # assert that indeed there is such a process
    assert found
    print('Create Process................................OK')

    # kill all of the processes that are for ping.exe
    for pid in flatten_processes_response_filter(processes, 'ping.exe'):
        print(f'Killing process with pid {pid}')
        _, result = lr_session.kill_process(pid, async_mode=True)
        result.result()

    print('Kill Process..................................OK')

    print()
    print(6 * ' ' + 'Live Response Registry Keys Commands')
    print(SYMBOLS * DELIMITER)

    _, kv_result = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT, async_mode=True)
    _, kv2_result = lr_session.list_registry_keys_and_values(KEY_PATH, async_mode=True)
    kvccommand_id, kvc_result = lr_session.create_registry_key(KEY_PATH, async_mode=True)

    result = kv_result.result()
    pprint(result)
    print('List Registry Keys and Values.................OK')

    found = False
    for item in result['values']:
        if item['registry_name'] == 'Test':
            found = True
            break
    # make sure the value for the key doesn't exist
    assert found is False

    exists = True
    try:
        result = kv2_result.result()
        print(result)
    except LiveResponseError as ex:
        # make sure such registry key does not exist
        exists = not ('ERROR_FILE_NOT_FOUND' in str(ex))
    assert exists is False
    print(f'Registry key with path {KEY_PATH} does not exist. Creating...')

    while True:
        status = lr_session.command_status(kvccommand_id)
        if status == 'COMPLETE':
            break

    result = kvc_result.result()

    exists = True
    try:
        _, result = lr_session.list_registry_keys_and_values(KEY_PATH, async_mode=True)
        result.result()
    except LiveResponseError as ex:
        exists = False
        assert 'ERROR_FILE_NOT_FOUND' in str(ex)
    # make sure that now the key exists
    assert exists
    print('Create Registry Key...........................OK')

    # create value for the key
    _, result = lr_session.set_registry_value(KEY_PATH, 1, async_mode=True)
    result.result()
    _, fresult = lr_session.get_registry_value(KEY_PATH, async_mode=True)
    result = fresult.result()
    assert result['registry_data'] == '1'
    assert result['registry_name'] == 'Test'
    print('Create Registry Value.........................OK')

    pprint(result)
    print('Get Registry Value............................OK')

    _, fresult = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT, async_mode=True)
    result = fresult.result()
    pprint(result)
    print('List Registry Keys and Values.................OK')

    found = False
    for item in result['values']:
        if item['registry_name'] == 'Test':
            found = True
            break
    # make sure the value for the key exists
    assert found is True

    _, fresult = lr_session.delete_registry_value(KEY_PATH, async_mode=True)
    fresult.result()

    # this will not raise an exception, because the result is not obtained
    _, dresult = lr_session.delete_registry_value(KEY_PATH, async_mode=True)
    fresult.result()
    deleted = False
    try:
        dresult.result()
    except LiveResponseError as ex:
        deleted = 'ERROR_FILE_NOT_FOUND' in str(ex)

    # make sure the value is deleted
    assert deleted
    print('Delete Registry Value.........................OK')

    _, fresult = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT, async_mode=True)
    result = fresult.result()
    found = False
    for item in result['values']:
        if item['registry_name'] == 'Test':
            found = True
            break
    # make sure the value for the key was deleted successfully
    assert found is False

    _, fresult = lr_session.delete_registry_key(KEY_PATH, async_mode=True)
    result = fresult.result()
    _, fresult = lr_session.list_registry_keys_and_values(KEY_PATH, async_mode=True)
    exists = True
    try:
        fresult.result()
    except LiveResponseError as ex:
        # make sure such registry key does not exist
        exists = False
        assert 'ERROR_FILE_NOT_FOUND' in str(ex)
    assert exists is False, 'Registry key was not properly deleted.'
    print('Delete Registry Key...........................OK')

    lr_session.close()
    print(f'Deleted the session {lr_session.session_id}...........OK')


def setup():
    """Setup Function"""
    # create the file that will be uploaded on the server,
    # will be deleted once we are done with the test
    fp = open("test.txt", "w")
    fp.write(FILE_CONTENT)
    fp.close()


def teardown():
    """Teardown Function"""
    # clean-up actions after the tests
    if path.exists(LOCAL_FILE):
        os.remove(LOCAL_FILE)
    if path.exists("test.txt"):
        os.remove("test.txt")


def main():
    """Script entry point"""
    global ORG_KEY
    global HOSTNAME
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"args provided {args}")

    cb = get_cb_cloud_object(args)
    HEADERS['X-Auth-Token'] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    # setup actions
    setup()

    # asynchronous version of the commands
    asynchronous_version(cb)

    # cleanup actions
    teardown()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
