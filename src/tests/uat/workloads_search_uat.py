#!/usr/bin/env python3
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

To execute, a profile must be provided using the standard CBC Credentials.

Workloads Search API:
* https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/vm-workload-search/
* Fetch Compute Resource by ID
* Search and Facet Compute Resources
"""

# Standard library imports
import sys
import requests

# Internal library imports
from cbc_sdk.workload.vm_workloads_search import ComputeResource
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


def search_and_facet_compute_resources_api(cb):
    """Start API Call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v1/orgs/{cb.credentials.org_key}/compute_resources/_search'
    return requests.post(url, json={"rows": "10000"}, headers=header).json()['results']


def search_and_facet_compute_resources_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Search and Facet Compute Resources")

    event_id = None
    query = cb.select(ComputeResource)
    for event in query:
        if not event_id and event.id and event.uuid:
            event_id = event.id

    return query, event_id


def fetch_compute_resource_by_id_api(cb, event_id):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v1/orgs/{cb.credentials.org_key}/compute_resources/{event_id}'
    return requests.get(url, headers=header).json()


def fetch_compute_resource_by_id_sdk(cb, event_id):
    """Start SDK call"""
    print("API Calls:")
    print("Fetch Compute Resource by ID")

    return ComputeResource(cb, event_id)._info


def compare_data_facet(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    sdk_ids = sorted([_.id for _ in sdk_resp])
    api_ids = sorted([_['id'] for _ in api_resp])

    assert sdk_ids == api_ids, print(f'TEST FAILED\nDifferance between api and sdk response found for {api_call}')

    print('\nTEST PASSED')
    print("----------------------------------------------------------")


def compare_data_id(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    assert sdk_resp == api_resp, print(f'TEST FAILED\nDifferance between api and sdk response found for {api_call}')
    print('\nTEST PASSED')
    print("----------------------------------------------------------")


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()

    cb = get_cb_cloud_object(args)

    sdk_resp, event_id = search_and_facet_compute_resources_sdk(cb)
    api_resp = search_and_facet_compute_resources_api(cb)
    compare_data_facet(sdk_resp, api_resp, 'Search and Facet Compute Resources')

    sdk_resp = fetch_compute_resource_by_id_sdk(cb, event_id)
    api_resp = fetch_compute_resource_by_id_api(cb, event_id)
    compare_data_id(sdk_resp, api_resp, 'Fetch Compute Resource by ID')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
