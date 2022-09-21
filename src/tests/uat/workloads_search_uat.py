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
The following API calls are tested in this script.

To execute, a profile must be provided using the standard CBC Credentials.

This requires an environment with BOTH vCenter workloads AND AWS workloads enrolled.  If your environment
has only one or the the other, use the --vcenter-only option to restrict testing to vCenter workloads only, or
the --aws-only option to restrict testing to AWS workloads only.  Omitting both of these flags causes both
to be tested.

Workloads Search API:
* https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/vm-workload-search/
* Fetch Compute Resource by ID
* Fetch AWS Compute Resource by ID
* Search Compute Resources
* Search AWS Compute Resources
* Facet Compute Resources
* Facet AWS Compute Resources
"""

# Standard library imports
import sys
import requests
import copy

# Internal library imports
from cbc_sdk.workload.vm_workloads_search import ComputeResource, AWSComputeResource
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


def search_compute_resources_api(cb):
    """Start API Call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/_search'
    count = 0
    api_results = []
    while True:
        response = requests.post(url, json={"rows": 200, "start": count, "criteria": {"deployment_type": ["WORKLOAD"]}},
                                 headers=header).json()
        count += len(response['results'])
        api_results.extend(response['results'])
        if count >= response['num_found']:
            break
    return api_results


def search_compute_resources_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Search Compute Resources")

    resource_id = None
    query = list(cb.select(ComputeResource))
    for resource in query:
        if not resource_id and resource.id and resource.uuid:
            resource_id = resource.id

    return query, resource_id


def search_aws_resources_api(cb):
    """Start API Call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/_search'
    count = 0
    api_results = []
    while True:
        response = requests.post(url, json={"rows": 200, "start": count, "criteria": {"deployment_type": ["AWS"]}},
                                 headers=header).json()
        count += len(response['results'])
        api_results.extend(response['results'])
        if count >= response['num_found']:
            break
    return api_results


def search_aws_resources_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Search AWS Resources")

    resource_id = None
    query = list(cb.select(AWSComputeResource))
    for resource in query:
        if not resource_id and resource.id and resource.image_id:
            resource_id = resource.id

    return query, resource_id


def fetch_compute_resource_by_id_api(cb, resource_id):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/{resource_id}' \
          '?deployment_type=WORKLOAD'
    return requests.get(url, headers=header).json()


def fetch_compute_resource_by_id_sdk(cb, resource_id):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Fetch Compute Resource by ID")

    return ComputeResource(cb, resource_id)._info


def fetch_aws_resource_by_id_api(cb, resource_id):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/{resource_id}' \
          '?deployment_type=AWS'
    return requests.get(url, headers=header).json()


def fetch_aws_resource_by_id_sdk(cb, resource_id):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Fetch AWS Compute Resource by ID")

    return AWSComputeResource(cb, resource_id)._info


def facet_compute_resource_api(cb):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/_facet'
    response = requests.post(url, json={"criteria": {"deployment_type": ["WORKLOAD"]},
                                        "terms": {"rows": 200,
                                                  "fields": ['eligibility', 'os_type', 'installation_status']}},
                             headers=header).json()
    return response['terms']


def facet_compute_resource_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Facet Compute Resource")

    facets = cb.select(ComputeResource).facet(['eligibility', 'os_type', 'installation_status'], 200)
    return_array = [copy.deepcopy(facet._info) for facet in facets]
    for item in return_array:
        item.pop("id", None)
    return return_array


def facet_aws_resource_api(cb):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/_facet'
    response = requests.post(url, json={"criteria": {"deployment_type": ["AWS"]},
                                        "terms": {"rows": 200,
                                                  "fields": ['installation_status', 'platform', 'region']}},
                             headers=header).json()
    return response['terms']


def facet_aws_resource_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Facet AWS Compute Resource")

    facets = cb.select(AWSComputeResource).facet(['installation_status', 'platform', 'region'], 200)
    return [facet._info for facet in facets]


def summarize_aws_api(cb):
    """Start API call"""
    header = {'X-Auth-Token': cb.credentials.token,
              'Content-Type': 'application/json'}
    url = f'{cb.credentials.url}lcm/view/v2/orgs/{cb.credentials.org_key}/compute_resources/_summarize'
    response = requests.post(url, json={"criteria": {"deployment_type": ["AWS"]},
                                        "summary_fields": ['installation_status', 'platform', 'region']},
                             headers=header).json()
    return response['summaries']


def summarize_aws_sdk(cb):
    """Start SDK call"""
    print("----------------------------------------------------------")
    print("API Calls:")
    print("Summarize AWS Compute Resources")

    return cb.select(AWSComputeResource).summarize(['installation_status', 'platform', 'region'])


def compare_data_search(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    sdk_ids = sorted([_.id for _ in sdk_resp])
    api_ids = sorted([_['id'] for _ in api_resp])

    assert sdk_ids == api_ids, f'TEST FAILED\nDifference between api and sdk response found for {api_call}'

    print('\nTEST PASSED')
    print("----------------------------------------------------------")


def compare_data_id(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    assert sdk_resp == api_resp, f'TEST FAILED\nDifference between api and sdk response found for {api_call}'
    print('\nTEST PASSED')
    print("----------------------------------------------------------")


def compare_data_summary(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    assert len(sdk_resp) == len(api_resp), f'TEST FAILED\nDifference between api and sdk response found for {api_call}'
    for block in api_resp:
        assert sdk_resp.get(block['field'], -1) == block['value'],\
            f'TEST FAILED\nDifference between api and sdk response found for {api_call}'
    print('\nTEST PASSED')
    print("----------------------------------------------------------")


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument('--vcenter-only', action='store_true', help='Run tests only on vCenter compute resources')
    parser.add_argument('--aws-only', action='store_true', help='Run tests only on AWS compute resources')
    args = parser.parse_args()

    run_vcenter = True
    run_aws = True
    if args.vcenter_only:
        if args.aws_only:
            print("Cannot specify both --vcenter-only and --aws-only options")
            return 1
        else:
            run_aws = False
    elif args.aws_only:
        run_vcenter = False

    cb = get_cb_cloud_object(args)

    if run_vcenter:
        sdk_resp, resource_id = search_compute_resources_sdk(cb)
        api_resp = search_compute_resources_api(cb)
        compare_data_search(sdk_resp, api_resp, 'Search Compute Resources')

        if resource_id is not None:
            sdk_resp = fetch_compute_resource_by_id_sdk(cb, resource_id)
            api_resp = fetch_compute_resource_by_id_api(cb, resource_id)
            compare_data_id(sdk_resp, api_resp, 'Fetch Compute Resource by ID')

    if run_aws:
        sdk_resp, resource_id = search_aws_resources_sdk(cb)
        api_resp = search_aws_resources_api(cb)
        compare_data_search(sdk_resp, api_resp, 'Search AWS Compute Resources')

        if resource_id is not None:
            sdk_resp = fetch_aws_resource_by_id_sdk(cb, resource_id)
            api_resp = fetch_aws_resource_by_id_api(cb, resource_id)
            compare_data_id(sdk_resp, api_resp, 'Fetch AWS Compute Resource by ID')

    if run_vcenter:
        sdk_resp = facet_compute_resource_sdk(cb)
        api_resp = facet_compute_resource_api(cb)
        compare_data_id(sdk_resp, api_resp, 'Facet Compute Resources')

    if run_aws:
        sdk_resp = facet_aws_resource_sdk(cb)
        api_resp = facet_aws_resource_api(cb)
        compare_data_id(sdk_resp, api_resp, 'Facet AWS Compute Resources')

        sdk_resp = summarize_aws_sdk(cb)
        api_resp = summarize_aws_api(cb)
        compare_data_summary(sdk_resp, api_resp, "Summarize AWS Compute Resources")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
