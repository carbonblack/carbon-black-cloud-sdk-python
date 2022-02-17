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
FACET_DEVICES = '{}appservices/v6/orgs/{}/devices/_facet'


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


def facet_devices_api_call():
    """Facet devices with direct API call"""
    facet_url = FACET_DEVICES.format(HOSTNAME, ORG_KEY)
    data = {
        'criteria': {},
        'query': '',
        'terms': {
            'fields': ['policy_id', 'status']
        }
    }
    return requests.post(facet_url, json=data, headers=HEADERS)


def normalize_results(result):
    """Helper function to sort dictionary values"""
    for item in result:
        if item.get('device_meta_data_item_list'):
            dl = item['device_meta_data_item_list']
            item['device_meta_data_item_list'] = sorted(dl, key=lambda i: (i.get('key_name')))


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

    normalize_results(api_search['results'])
    normalize_results(sdk_results)
    assert sdk_results == api_search['results'], 'Test Failed: SDK call returns different data. '\
        'Expected: {}, Actual: {}'.format(api_search['results'], sdk_results)

    print('Search Devices.................................OK')


def facet_devices(cb):
    """Verify that the SDK returns the same result for Facet Devices as the respective API call"""
    api_facet = facet_devices_api_call().json()

    query = cb.select(Device).where('')
    list_facets = query.facets(['policy_id', 'status'])

    api_results = api_facet['results']
    assert len(api_results) == len(list_facets), \
        f"Test failed: API call returned {len(api_results)}, but SDK call returned {len(list_facets)}"

    for api_facet, list_facet in zip(api_results, list_facets):
        assert api_facet['field'] == list_facet.field, \
            f"Test failed: field name from API {api_facet['field']} differs from SDK {list_facet.field}"
        assert len(api_facet['values']) == len(list_facet.values_), \
            f"Test failed: length of values for field {list_facet.field} differs - " \
            f"API says {len(api_facet['values'])} but SDK says {len(list_facet.values_)}"
        for vdict, val in zip(api_facet['values'], list_facet.values_):
            assert vdict == val._info, \
                f"Test failed: value differs: API is {vdict}, SDK is {val._info}"

    print('Facet Devices..................................OK')


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
    facet_devices(cb)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
