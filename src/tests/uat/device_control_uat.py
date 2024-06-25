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
The following API calls are tested in this script.

For the validation CBC API requests are used.

To execute, a profile must be provided using the standard CBC Credentials.

Processes:
Approvals
* Bulk Create Approvals
* Get Approval by ID
* Search Approvals
* Update Approval
* Delete Approval by ID

Blocks
* Bulk Create Blocks
* Get Block by ID
* Get Blocks
* Delete Block by ID

USB Devices
* Search USB Devices
* Facet USB Devices

Products
* Get USB Device Vendors and Products Seen

The following API calls were not covered:
* Get USB Device by ID
* Get Endpoints associated with a USB device
"""

# Standard library imports
import sys
import requests
import json

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.endpoint_standard.usb_device_control import USBDevice, \
    USBDeviceApproval, USBDeviceBlock

PRODUCT_VENDOR_URL = '{}device_control/v3/orgs/{}/products'
USB_DEVICE_APPROVAL = '{}device_control/v3/orgs/{}/approvals'
USB_DEVICE_BLOCKS = '{}device_control/v3/orgs/{}/blocks'
USB_DEVICES = '{}device_control/v3/orgs/{}/devices'
USB_DEVICES_FACETS = '{}device_control/v3/orgs/{}/devices/_facet'
JOB_OUTPUT = '{}jobs/v1/orgs/{}/jobs/{}/download'
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
ORG_KEY = ''
HOSTNAME = ''
# Formatters
NEWLINES = 1
DELIMITER = '-'
SYMBOLS = 48

"""
    API Helper Requests:
    1. Get USB Device Vendors and Products Seen
    2. Get Approval by ID
    3. Search Approvals
    4. Get Block by ID
    5. Get Blocks
    6. Search USB Devices
"""


def get_products_n_vendors_api():
    """Getting the result from the CBC API"""
    url = PRODUCT_VENDOR_URL.format(HOSTNAME, ORG_KEY)
    return requests.get(url, headers=HEADERS)


def get_usb_device_approval_by_id_api(approval_id):
    """Get Approval by ID"""
    url = USB_DEVICE_APPROVAL.format(HOSTNAME, ORG_KEY)
    url += '/' + approval_id
    return requests.get(url, headers=HEADERS)


def search_usb_device_approval():
    """Search USB Device Approval"""
    usb_url = USB_DEVICE_APPROVAL.format(HOSTNAME, ORG_KEY)
    usb_url += '/_search'
    return requests.post(usb_url, json={}, headers=HEADERS)


def export_usb_device_approvals():
    """Export USB Device Approvals"""
    usb_url = USB_DEVICE_APPROVAL.format(HOSTNAME, ORG_KEY)
    usb_url += '/_export'
    job_ref = requests.post(usb_url, json={"format": "CSV"}, headers=HEADERS).json()
    job_url = JOB_OUTPUT.format(HOSTNAME, ORG_KEY, job_ref['job_id'])
    resp = requests.get(job_url, headers=HEADERS)
    return resp.text


def get_usb_device_block_by_id_api(block_id):
    """Get Block by ID"""
    url = USB_DEVICE_BLOCKS.format(HOSTNAME, ORG_KEY)
    url += '/' + block_id
    return requests.get(url, headers=HEADERS)


def search_usb_device_blocks():
    """Search USB Device Blocks"""
    usb_url = USB_DEVICE_BLOCKS.format(HOSTNAME, ORG_KEY)
    return requests.get(usb_url, headers=HEADERS)


def search_usb_devices():
    """Search USB Devices"""
    usb_url = USB_DEVICES.format(HOSTNAME, ORG_KEY)
    usb_url += '/_search'
    return requests.post(usb_url, json={}, headers=HEADERS)


def export_usb_devices():
    """Export USB Devices"""
    usb_url = USB_DEVICES.format(HOSTNAME, ORG_KEY)
    usb_url += '/_export'
    job_ref = requests.post(usb_url, json={"format": "CSV"}, headers=HEADERS).json()
    job_url = JOB_OUTPUT.format(HOSTNAME, ORG_KEY, job_ref['job_id'])
    resp = requests.get(job_url, headers=HEADERS)
    return resp.text


def search_usb_devices_facets():
    """Facet USB Devices"""
    data = {"terms": {"fields": ["status"]}}
    usb_url = USB_DEVICES_FACETS.format(HOSTNAME, ORG_KEY)
    return requests.post(usb_url, json=data, headers=HEADERS)


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
    if not HOSTNAME.endswith('/'):
        HOSTNAME += '/'
    if print_detail:
        print(f"{HOSTNAME=} {ORG_KEY=}")

    # USB Device Approvals
    """USB Device Control Approval"""
    print('USB Device Control Approvals')
    print(SYMBOLS * DELIMITER)

    # create the usb device approval
    data = [{
        "vendor_id": "0x0781",
        "product_id": "0x5581",
        "serial_number": "4C531001331122115172",
        "notes": "Added by UAT - please remove",
        "approval_name": "Example Approval"}]
    sdk_result = USBDeviceApproval.bulk_create(cb, data)
    sdk_created_obj = sdk_result[0]

    try:
        sdk_obj = USBDeviceApproval(cb, sdk_created_obj.id)
        api_result = get_usb_device_approval_by_id_api(sdk_created_obj.id).json()
        dict_sdk_obj = sdk_obj._info
        assert api_result == dict_sdk_obj, 'Get Approval by ID Failed - ' \
               'Expected: {}, Actual: {}'.format(api_result, dict_sdk_obj)
        print('Get Approval by ID............................OK')

        # get the USB Device Approval
        query = cb.select(USBDeviceApproval)
        sdk_results = []
        for approval in query:
            if approval.id == sdk_created_obj.id:
                print('Bulk Create Test..............................OK')
            sdk_results.append(approval._info)
        api_search = search_usb_device_approval().json()['results']
        assert sdk_results == api_search, 'Search Test Failed\nExpected:\n{}\n' \
            'Actual:\n{}'.format(json.dumps(api_search, indent=4, sort_keys=True),
                                 json.dumps(sdk_results, indent=4, sort_keys=True))
        print('Search Test...................................OK')

        # export device approvals
        query = cb.select(USBDeviceApproval)
        job = query.export('CSV')
        sdk_results = job.get_output_as_string()
        api_results = export_usb_device_approvals()
        assert sdk_results == api_results, 'Export Test Failed\nExpected:\n{}\n' \
            'Actual:\n{}'.format(api_results, sdk_results)
        print('Export Test...................................OK')

        # update the object
        sdk_created_obj.approval_name = 'Changed Approval'
        sdk_created_obj._update_object()
        query = cb.select(USBDeviceApproval)
        sdk_created_new = query[0]
        assert sdk_created_new.approval_name == 'Changed Approval', 'Update Test '\
            'Failed - Excepted: {}, Actual: {}'.format(
                sdk_created_obj._info,
                sdk_created_new._info)
        print('Update Test...................................OK')

        # delete the usb approval
        if sdk_created_obj is not None:
            sdk_created_obj.delete()
            sdk_created_obj = None
        query = cb.select(USBDeviceApproval)
        assert query._total_results == 0, 'Delete Approval Test Failed - Record '\
            'was not deleted... {}'.format(query._total_results)
        print('Delete Approval...............................OK')
        print(NEWLINES * '\n')
    finally:
        if sdk_created_obj is not None:
            sdk_created_obj.delete()

    """USB Device Control Blocks"""
    print('USB Device Control Blocks')
    print(SYMBOLS * DELIMITER)

    # create the usb device block
    data = ["6997287"]
    sdk_result = USBDeviceBlock.bulk_create(cb, data)
    sdk_created_obj = sdk_result[0]
    try:
        api_result = get_usb_device_block_by_id_api(sdk_created_obj.id).json()
        block_obj = USBDeviceBlock(cb, sdk_created_obj.id)
        dict_block_obj = block_obj._info
        assert dict_block_obj == api_result, 'Get Block by ID Failed - Expected: '\
            '{}, Actual: {}'.format(api_result, dict_block_obj)
        print('Get Block by ID...............................OK')
        # get the USB Device Block
        query = cb.select(USBDeviceBlock)
        sdk_results = []
        for block in query:
            if block.id == sdk_created_obj.id:
                print('Bulk Create Test..............................OK')
            sdk_results.append(block._info)
        api_search = search_usb_device_blocks().json()['results']
        assert sdk_results == api_search, 'Search Test Failed Expected: {}, ' \
            'Actual: {}'.format(api_search.json()['results'], sdk_results)
        print('Search Test...................................OK')

        # delete the usb approval
        if sdk_created_obj is not None:
            sdk_created_obj.delete()
            sdk_created_obj = None
        query = cb.select(USBDeviceBlock)
        assert query._total_results == 0, 'Delete Block Failed - Record was not '\
            'deleted... {}'.format(query._total_results)
        print('Delete Block..................................OK')
        print(NEWLINES * '\n')
    finally:
        if sdk_created_obj is not None:
            sdk_created_obj.delete()

    """USB Devices"""
    print('USB Devices')
    print(SYMBOLS * DELIMITER)

    # Search USB Devices
    query = cb.select(USBDevice)
    sdk_results = []
    for device in query:
        sdk_results.append(device._info)
    api_search = search_usb_devices().json()
    assert api_search['num_available'] == query._total_results, 'Device Search ' \
           'Failed - Expected: {}, Actual: {}'.format(api_search['num_available'],
                                                      query._total_results)
    short_sdk_results = sdk_results[0:api_search['num_found']]
    assert short_sdk_results == api_search['results'], 'Device Search Test Failed -'\
        'Expected: {}, Actual: {}'.format(api_search['results'], short_sdk_results)
    print('Device Search.................................OK')

    # Export USB Devices
    query = cb.select(USBDevice)
    job = query.export('CSV')
    sdk_results = job.get_output_as_string()
    api_results = export_usb_devices()
    assert sdk_results == api_results, 'Export Test Failed\nExpected: {}\n' \
                                       'Actual: {}'.format(api_results, sdk_results)
    print('Export Test...................................OK')

    # Facet USB Devices
    query = cb.select(USBDevice).facets(["status"])
    api_search = search_usb_devices_facets().json()
    assert query == api_search['terms'], 'Facet USB Devices Failed - Expected'\
        ': {}, Actual: {}'.format(api_search['terms'], query)
    print('Facet USB Devices.............................OK')
    print(NEWLINES * '\n')

    # vendors and products
    print('Testing Get USB Device Vendors and Products Seen')
    print(SYMBOLS * DELIMITER)
    api_result = get_products_n_vendors_api()
    sdk_result = USBDevice.get_vendors_and_products_seen(cb)
    api_results = api_result.json()['results']
    assert api_results == sdk_result, 'Get USB Device Vendors and Products '\
        'Failed - Expected: {}, Actual: {}'.format(api_results, sdk_result)
    print('Get USB Device Vendors and Products Seen......OK')

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
