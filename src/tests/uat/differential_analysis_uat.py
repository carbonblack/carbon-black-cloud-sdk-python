#!/usr/bin/env python3
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
To execute, a profile must be provided using the standard CBC Credentials and newer_run_id.

Altho optional, older_run_id must be provided in some cases as well.

Example: python3 differential_analysis_uat.py --profile LiveQuery --newer_run_id abcd

Differential Analysis:
https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/differential-analysis-api/
"""

import sys
import json
import requests
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.audit_remediation import Differential


def extract_data(data):
    """Extract the device data from the response"""
    extracted_data = {}
    for item in data['diff_results']:
        device_id = item['device_id']
        extracted_data[device_id] = {}
        for nested_item in item:
            if nested_item == 'changes':
                continue
            extracted_data[device_id][nested_item] = item[nested_item]

    return extracted_data


def compare_data(sdk_resp, api_resp):
    """Compare the data between the sdk and api response"""
    sdk = sdk_resp[0]._info
    api = api_resp.json()
    api = api['results'][0]

    test_pass = True

    # Check if all devices have completed their queries
    for item in api:
        if item in ['newer_run_not_responded_devices', 'older_run_not_responded_devices']:
            api_resp = set(api[item])
            sdk_resp = set(sdk[item])
            if api_resp != sdk_resp:
                test_pass = False
                print(f'TEST FAILED: DIFF between {item} content of SDK and API Results')
                print(f'SDK content of {item}:\n', *sdk_resp)
                print(f'API content of {item}:\n', *api_resp)
                print(58 * '-')

    # Check if diff_results content length is the same
    devices_api = extract_data(sdk)
    devices_sdk = extract_data(api)
    if len(devices_sdk) != len(devices_api):
        print('TEST FAILED: DIFF between diff_results content of SDK and API Results')
        print('SDK content:\n', *devices_sdk)
        print('API content:\n', *devices_api)
        print(58 * '-')
        test_pass = False

    # Check if there are missing device ids
    api_device_ids = set(devices_api.keys())
    sdk_device_ids = set(devices_sdk.keys())
    if api_device_ids != sdk_device_ids:
        test_pass = False
        print('TEST FAILED: DIFF between device ids of SDK and API Results')
        print('SDK content:\n', *sdk_device_ids)
        print('API content:\n', *api_device_ids)
        print(58 * '-')

    # Check if there are differances between the content of devices
    for device in devices_api:
        for item in devices_api[device]:
            if devices_api[device][item] != devices_sdk[device][item]:
                test_pass = False
                print('TEST FAILED: DIFF between diff_results content of SDK and API Results')
                print('SDK content:\n', *devices_sdk)
                print('API content:\n', *devices_api)
                print(58 * '-')

    if test_pass:
        print('\nTEST PASSED')
        print(58 * '-')


def differential_analysis_sdk(cb, args):
    """Get Config Template call via SDK"""
    resp = cb.select(Differential).newer_run_id(args.newer_run_id)
    if args.older_run_id:
        resp.older_run_id(args.older_run_id)

    if resp[0]._info:
        print('SDK Response: OK')
    return resp


def differential_analysis_api(cb, args):
    """Get Sensor Kit and Configuration via raw API"""
    req_headers = {'Content-Type': 'application/json', 'X-AUTH-TOKEN': cb.credentials.token}
    uri = f'{cb.credentials.url}livequery/v1/orgs/{cb.credentials.org_key}/differential/runs/_search'

    parameter_block = {"newer_run_id": args.newer_run_id}
    if args.older_run_id:
        parameter_block["older_run_id"] = args.older_run_id
    req_body_json = json.dumps(parameter_block)
    resp = requests.post(url=uri, headers=req_headers, data=req_body_json)

    if resp.status_code == 200:
        print('API Response: OK')
    return resp


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument('--newer_run_id', required=True)
    parser.add_argument('--older_run_id', required=False)
    args = parser.parse_args()

    cb = get_cb_cloud_object(args)

    print(58 * '-')
    print('Differential Analysis - Query Comparison')
    sdk_resp = differential_analysis_sdk(cb, args)
    api_resp = differential_analysis_api(cb, args)
    compare_data(sdk_resp, api_resp)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
