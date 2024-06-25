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
from cbc_sdk.live_response_api import LiveResponseError

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
FILE_CONTENT = "This is just a test"
FILE_CONTENT_BINARY = b"This is just a test"

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


def synchronous_version(cb):
    """Synchronous commands"""
    print(11 * ' ' + 'Sync Live Response Commands')
    print(SYMBOLS * DELIMITER)

    try:
        device = cb.select(Device, DEVICE_ID)
    except Exception:
        # if this is not run on dev01, pick a random active device
        devices = cb.select(Device).set_status(['ACTIVE'])
        device = devices[0]

    lr_session = device.lr_session()
    print(f'Created Session {lr_session.session_id}...............OK')
    print()

    print()
    print(10 * ' ' + 'Live Response Files Commands')
    print(SYMBOLS * DELIMITER)

    # create directory
    try:
        lr_session.create_directory(DIR)
    except LiveResponseError as ex:
        if 'ERROR_ALREADY_EXISTS' in str(ex):
            print('Directory already exists, continue with the test.')
        else:
            raise
    print('Create Dir....................................OK')

    # show that test.txt is not present in that directory
    response = lr_session.list_directory(DIR)
    directories = flatten_response(response)
    assert 'test.txt' not in directories, f'Dirs: {directories}'

    # upload the file on the server
    lr_session.put_file(open("test.txt", "r"), FILE)
    print('PUT File......................................OK')

    # show that test.txt is present in that directory
    response = lr_session.list_directory(DIR)
    directories = flatten_response(response)
    assert 'test.txt' in directories, f'Dirs: {directories}'

    # walk through the directories
    for entry in lr_session.walk(DIR):
        print(entry)
    print('WALK dir......................................OK')

    content = lr_session.get_file(FILE)
    assert content == FILE_CONTENT_BINARY, f'{content} {FILE_CONTENT}'
    print('GET File......................................OK')
    lr_session.delete_file(FILE)

    exc_raise = False
    try:
        content = lr_session.get_file(FILE)
    except LiveResponseError as ex:
        assert 'ERROR_FILE_NOT_FOUND' in str(ex) or 'ERROR_PATH_NOT_FOUND' in str(ex), f'Other error {ex}'
        exc_raise = True
    finally:
        assert exc_raise
    print('DELETE File...................................OK')
    # delete the directory too
    lr_session.delete_file(DIR)
    print('DELETE Dir....................................OK')

    # This command takes a lot of time!
    # uncomment only if this needs to be tested!
    """
    lr_session.memdump(LOCAL_FILE, MEMDUMP_FILE)
    assert path.exists(LOCAL_FILE)
    exc_raise = False
    try:
        content = lr_session.get_file(MEMDUMP_FILE)
    except LiveResponseError as ex:
        assert 'ERROR_FILE_NOT_FOUND' in str(ex), f'Other error {ex}'
        exc_raise = True
    finally:
        assert exc_raise
    print('Memdump.......................................OK')
    """

    print()
    print(9 * ' ' + 'Live Response Process Commands')
    print(SYMBOLS * DELIMITER)

    # list processes
    processes = lr_session.list_processes()
    pprint(flatten_processes_response(processes))
    print('List Processes................................OK')

    # create infinite ping, that could be killed afterwards
    lr_session.create_process(r'cmd.exe /c "ping.exe -t 127.0.0.1"',
                              wait_for_completion=False, wait_for_output=False)
    processes = lr_session.list_processes()
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
        lr_session.kill_process(pid)
    print('Kill Process..................................OK')

    print()
    print(6 * ' ' + 'Live Response Registry Keys Commands')
    print(SYMBOLS * DELIMITER)

    result = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT)
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
        result = lr_session.list_registry_keys_and_values(KEY_PATH)
        print(result)
    except LiveResponseError as ex:
        # make sure such registry key does not exist
        exists = not ('ERROR_FILE_NOT_FOUND' in str(ex))
    assert exists is False
    print(f'Registry key with path {KEY_PATH} does not exist. Creating...')

    lr_session.create_registry_key(KEY_PATH)
    exists = True
    try:
        result = lr_session.list_registry_keys_and_values(KEY_PATH)
    except LiveResponseError as ex:
        exists = False
        assert 'ERROR_FILE_NOT_FOUND' in str(ex)
    # make sure that now the key exists
    assert exists
    print('Create Registry Key...........................OK')

    # create value for the key
    lr_session.set_registry_value(KEY_PATH, 1)
    result = lr_session.get_registry_value(KEY_PATH)
    assert result['registry_data'] == '1'
    assert result['registry_name'] == 'Test'
    print('Create Registry Value.........................OK')

    pprint(result)
    print('Get Registry Value............................OK')

    result = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT)
    pprint(result)
    print('List Registry Keys and Values.................OK')

    found = False
    for item in result['values']:
        if item['registry_name'] == 'Test':
            found = True
            break
    # make sure the value for the key exists
    assert found is True

    result = lr_session.delete_registry_value(KEY_PATH)
    deleted = False
    try:
        result = lr_session.get_registry_value(KEY_PATH)
    except LiveResponseError as ex:
        deleted = 'ERROR_FILE_NOT_FOUND' in str(ex)
    # make sure the value is deleted
    assert deleted
    print('Delete Registry Value.........................OK')

    result = lr_session.list_registry_keys_and_values(KEY_PATH_PARENT)
    found = False
    for item in result['values']:
        if item['registry_name'] == 'Test':
            found = True
            break
    # make sure the value for the key was deleted successfully
    assert found is False

    result = lr_session.delete_registry_key(KEY_PATH)
    exists = True
    try:
        result = lr_session.list_registry_keys_and_values(KEY_PATH)
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

    # synchronous version of the commands
    synchronous_version(cb)

    # cleanup actions
    teardown()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
