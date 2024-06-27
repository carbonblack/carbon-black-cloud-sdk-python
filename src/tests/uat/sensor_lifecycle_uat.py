#!/usr/bin/env python3
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
The following API calls are tested in this script.

To execute, a profile must be provided using the standard CBC Credentials.

Sensor Lifecycle Management:
* https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/sensor-lifecycle-management/
* Get Sensor Configuration Template
* Get Sensor Kit and Configuration Links
* Request Workload Sensor Installation
"""

import sys
import json
import requests
from datetime import datetime, timedelta
from validators.url import url
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.workload import SensorKit, ComputeResource


"""Hard coded sensor values to look for.  These may have to change with newer sensor releases."""

S_DEVICE_TYPE = 'WINDOWS'
S_ARCHITECTURE = '64'
S_TYPE = 'WINDOWS'
S_VERSION = '3.7.0.941'

"""Common work functions"""


def header_line():
    """Print a header line in the output"""
    print("----------------------------------------------------------")


def start_api_call(name):
    """Print the note at the start of an API call"""
    print(f"API Calls:\n{name}")


def base_compare(sdk_resp, api_resp, api_call):
    """Compare the data between the sdk and api response"""
    assert sdk_resp == api_resp, f'TEST FAILED\nDifferance between api and sdk response found for {api_call}'
    print('\nTEST PASSED')
    print("----------------------------------------------------------")


"""API test functions"""


def get_config_template_sdk(cb):
    """Get Config Template call via SDK"""
    return SensorKit.get_config_template(cb)


def get_config_template_api(cb):
    """Get Config Template call via raw API"""
    header = {'X-Auth-Token': cb.credentials.token}
    uri = f'{cb.credentials.url}lcm/v1/orgs/{cb.credentials.org_key}/sensor/config_template'
    return requests.get(uri, verify=cb.credentials.ssl_verify, headers=header).text


def get_sensor_kits_sdk(cb, expires_date):
    """Get Sensor Kit and Configuration via SDK"""
    query = cb.select(SensorKit).add_sensor_kit_type(device_type=S_DEVICE_TYPE, architecture=S_ARCHITECTURE,
                                                     sensor_type=S_TYPE, version=S_VERSION)
    return query.expires(expires_date).all()


def get_sensor_kits_api(cb, expires_date):
    """Get Sensor Kit and Configuration via raw API"""
    header = {'X-Auth-Token': cb.credentials.token}
    uri = f'{cb.credentials.url}lcm/v1/orgs/{cb.credentials.org_key}/sensor/_download'
    request_block = {'sensor_types': [{'device_type': S_DEVICE_TYPE, 'architecture': S_ARCHITECTURE,
                                       'type': S_TYPE, 'version': S_VERSION}],
                     'expires_at': expires_date}
    parameter_block = {'sensor_url_request': ('request.json', json.dumps(request_block), 'application/json'),
                       'configParams': ('config.ini', '', 'text/plain')}
    return requests.request("POST", uri, verify=cb.credentials.ssl_verify, headers=header,
                            files=parameter_block).json()


def sensorkit_validate_entry(sensorkit):
    """Validate a SensorKit entry"""
    result = url(sensorkit.get('sensor_url', None))
    assert result is True, f'TEST FAILED\ninvalid URL for Get Sensor Kit and Configuration Links--{result}'
    del sensorkit['sensor_url']
    result = url(sensorkit.get('sensor_config_url', None))
    assert result is True, f'TEST FAILED\ninvalid URL for Get Sensor Kit and Configuration Links--{result}'
    del sensorkit['sensor_config_url']
    return sensorkit


def sensorkit_compare(skit_sdk, skit_api):
    """Compare SensorKit entries except for the URLS which may differ"""
    data_sdk = list(map(sensorkit_validate_entry, [skit._info for skit in skit_sdk]))
    data_api = list(map(sensorkit_validate_entry, skit_api['sensor_infos']))
    base_compare(data_sdk, data_api, 'Get Sensor Kit and Configuration Links')


def lookup_compute_resource(cb):
    """Looks up a compute resource for use in the request install calls"""
    query = cb.select(ComputeResource).where('1').set_eligibility(['ELIGIBLE']).set_installation_status(['SUCCESS'])
    for resource in query:
        if resource.os_type == S_TYPE and resource.os_architecture == S_ARCHITECTURE:
            return resource
    raise RuntimeError("Unable to find suitable resource for testing purposes")


def request_install_sdk(resource):
    """Request Sensor Install via SDK"""
    return resource.install_sensor(S_VERSION)


def request_install_api(cb, resource):
    """Request Sensor Install via API"""
    header = {'X-Auth-Token': cb.credentials.token}
    uri = f'{cb.credentials.url}lcm/v1/orgs/{cb.credentials.org_key}/workloads/actions'
    request_block = {"compute_resources": [{"resource_manager_id": resource.vcenter_uuid,
                                            "compute_resource_id": resource.uuid}],
                     "sensor_types": [{'device_type': S_DEVICE_TYPE, 'architecture': S_ARCHITECTURE,
                                       'type': S_TYPE, 'version': S_VERSION}]}
    parameter_block = {"action_type": (None, "INSTALL", None),
                       "install_request": ("request.json", json.dumps(request_block), "application/json"),
                       "file": ("config.ini", '', "text/plain")}
    return requests.request("POST", uri, verify=cb.credentials.ssl_verify, headers=header,
                            files=parameter_block).json()


"""Main function of test"""


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()

    cb = get_cb_cloud_object(args)
    header_line()

    start_api_call('Get Sensor Configuration Template')
    templ_sdk = get_config_template_sdk(cb)
    templ_api = get_config_template_api(cb)
    base_compare(templ_sdk, templ_api, 'Get Sensor Configuration Template')

    start_api_call('Get Sensor Kit and Configuration Links')
    expires_date = (datetime.now() + timedelta(days=2)).isoformat() + "Z"
    kits_sdk = get_sensor_kits_sdk(cb, expires_date)
    kits_api = get_sensor_kits_api(cb, expires_date)
    sensorkit_compare(kits_sdk, kits_api)

    # We use an arbitrary resource to serve as the target for a sensor install.
    resource = lookup_compute_resource(cb)

    start_api_call('Request Workload Sensor Installation')
    result_sdk = request_install_sdk(resource)
    result_api = request_install_api(cb, resource)
    base_compare(result_sdk, result_api, 'Request Workload Sensor Installation')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
