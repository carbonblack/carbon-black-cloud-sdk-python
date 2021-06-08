#!/usr/bin/env python3
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
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

The following API calls are tested in this script:

Devices:
* Search Devices
  * https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/devices-api/

"""

# Standard library imports
import requests
import sys

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device

HOSTNAME = ''
ORG_KEY = ''
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
SEARCH_DEVICES = '{}appservices/v6/orgs/{}/devices/_search'


def search_devices_api_call():
    """Search Devices with direct API call"""
    search_url = SEARCH_DEVICES.format(HOSTNAME, ORG_KEY)
    data = {
        "rows": 10000,
        "criteria": {
            "deployment_type": ["WORKLOAD"]
        },
        "sort": [
            {
                "field": "id",
                "order": "asc"
            }
        ]
    }
    return requests.post(search_url, json=data, headers=HEADERS)


def search_devices(cb):
    """Verify that the SDK returns the same result for Search Devices as the respective API call"""
    api_search = search_devices_api_call().json()

    query = cb.select(Device)\
        .set_deployment_type(["WORKLOAD"])\
        .sort_by("id", "ASC")

    sdk_results = []
    for device in query:
        sdk_results.append(device._info)

    assert api_search['num_found'] == query._total_results, \
           'Test Failed: SDK call returns different number of devices. ' \
           'Expected: {}, Actual: {}'.format(api_search['num_found'], query._total_results)

    assert sdk_results == api_search['results'], 'Test Failed: SDK call returns different data. '\
        'Expected: {}, Actual: {}'.format(api_search['results'], sdk_results)

    print('Search Devices.................................OK')


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()
    global ORG_KEY
    global HOSTNAME

    cb = get_cb_cloud_object(args)

    HEADERS['X-Auth-Token'] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    search_devices(cb)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
