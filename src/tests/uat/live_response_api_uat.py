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

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.live_response_api import LiveResponseError

# CONSTANTS
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
ORG_KEY = ''
HOSTNAME = ''
DEVICE_ID = 8612331
FILE_CONTENT = "This is just a test"
FILE_CONTENT_1 = b"This is just a test"

# Formatters
NEWLINES = 1
DELIMITER = '-'
SYMBOLS = 48


def flatten_response(response):
    """Helper function to extract only the filenames from the list directory command"""
    return [item['filename'] for item in response]


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

    print('LR Files')
    print(SYMBOLS * DELIMITER)
    device = cb.select(Device, DEVICE_ID)
    lr_session = device.lr_session()
    print(f'Created Session {lr_session.session_id}...............OK')

    # create the file that will be uploaded on the server,
    # will be deleted once we are done with the test
    fp = open("test.txt", "w")
    fp.write(FILE_CONTENT)
    fp.close()

    # create directory
    try:
        lr_session.create_directory('C:\\\\demo')
    except LiveResponseError as ex:
        if 'ERROR_ALREADY_EXISTS' in str(ex):
            print('Directory already exists, continue with the test.')
        else:
            raise

    # show that test.txt is not present in that directory
    response = lr_session.list_directory('C:\\\\demo\\\\')
    directories = flatten_response(response)
    assert 'test.txt' not in directories
    print(directories)

    # upload the file on the server
    lr_session.put_file(open("test.txt", "r"), r"c:\demo\test.txt")
    print('PUT File......................................OK')
    # show that test.txt is present in that directory
    response = lr_session.list_directory('C:\\\\demo\\\\')
    directories = flatten_response(response)
    assert 'test.txt' in directories
    print(directories)

    content = lr_session.get_file(r"c:\demo\test.txt")
    assert content == FILE_CONTENT_1, '{} {}'.format(content, FILE_CONTENT)
    print('GET File......................................OK')
    lr_session.delete_file(r"c:\demo\test.txt")
    try:
        content = lr_session.get_file(r"c:\demo\test.txt")
    except LiveResponseError as ex:
        assert 'ERROR_FILE_NOT_FOUND' in str(ex), f'Other error {ex}'

    print('DELETE File...................................OK')

    os.remove("test.txt")
    lr_session.close()
    print(f'Deleted the session {lr_session.session_id}...........OK')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
