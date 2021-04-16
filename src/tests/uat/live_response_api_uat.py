#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
The following API calls are tested in this script.

For the validation CBC API requests are used.

To execute, a profile must be provided using the standard CBC Credentials.

Processes: Live Response

"""

# Standard library imports
import sys
import os
import os.path
from os import path
from pprint import pprint

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.live_response_api import LiveResponseError

# CONSTANTS
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
ORG_KEY = ''
HOSTNAME = ''
DEVICE_ID = 8612331
LOCAL_FILE = 'memdump.txt'
DIR = 'C:\\\\demo\\\\'
MEMDUMP_FILE = r"c:\demo\memdump.txt"
FILE = r"c:\demo\test.txt"
FILE_CONTENT = "This is just a test"
FILE_CONTENT_1 = b"This is just a test"

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


def main():
    """Script entry point"""
    global ORG_KEY
    global HOSTNAME
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb = get_cb_cloud_object(args)
    HEADERS['X-Auth-Token'] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    print(13 * ' ' + 'Live Response Commands')
    print(SYMBOLS * DELIMITER)
    device = cb.select(Device, DEVICE_ID)
    lr_session = device.lr_session()
    print(f'Created Session {lr_session.session_id}...............OK')
    print()

    # create the file that will be uploaded on the server,
    # will be deleted once we are done with the test
    fp = open("test.txt", "w")
    fp.write(FILE_CONTENT)
    fp.close()

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
    print('walk dir......................................OK')

    content = lr_session.get_file(FILE)
    assert content == FILE_CONTENT_1, '{} {}'.format(content, FILE_CONTENT)
    print('GET File......................................OK')
    lr_session.delete_file(FILE)

    exc_raise = False
    try:
        content = lr_session.get_file(FILE)
    except LiveResponseError as ex:
        assert 'ERROR_FILE_NOT_FOUND' in str(ex), f'Other error {ex}'
        exc_raise = True
    finally:
        assert exc_raise
    print('DELETE File...................................OK')

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

    print(9 * ' ' + 'Live Response Process Commands')
    print(SYMBOLS * DELIMITER)
    processes = lr_session.list_processes()
    pprint(flatten_processes_response(processes))
    print('List Processes................................OK')
    # lr_session.create_process(r'cmd.exe /c "ping.exe -t 192.168.1.1"',
    #                          wait_for_completion=False, wait_for_output=False)
    processes = lr_session.list_processes()
    found = False
    for process in processes:
        if 'ping.exe' in process['process_path']:
            found = True
            print(process)
    assert found
    print('Create Process................................OK')
    for pid in flatten_processes_response_filter(processes, 'ping.exe'):
        print(f'Killing process with pid {pid}')
        lr_session.kill_process(pid)
    print('Kill Process..................................OK')

    # clean-up actions after the tests
    if path.exists(LOCAL_FILE):
        os.remove(LOCAL_FILE)
    if path.exists("test.txt"):
        os.remove("test.txt")
    lr_session.close()
    print(f'Deleted the session {lr_session.session_id}...........OK')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
