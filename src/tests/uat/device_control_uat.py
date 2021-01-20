#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
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
# from pprint import pprint

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
# from cbc_sdk.errors import ApiError
from cbc_sdk.endpoint_standard.usb_device_control import USBDevice, \
    USBDeviceApproval, USBDeviceBlock

PRODUCT_VENDOR_URL = '{}device_control/v3/orgs/{}/products'
USB_DEVICE_APPROVAL = '{}device_control/v3/orgs/{}/approvals'
USB_DEVICE_BLOCKS = '{}device_control/v3/orgs/{}/blocks'
USB_DEVICES = '{}device_control/v3/orgs/{}/devices'
USB_DEVICES_FACETS = '{}device_control/v3/orgs/{}/devices/_facet'
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


def search_usb_devices_facets():
    """Facet USB Devices"""
    data = {"terms": {"fields": ["status"]}}
    usb_url = USB_DEVICES_FACETS.format(HOSTNAME, ORG_KEY)
    return requests.post(usb_url, json=data, headers=HEADERS)


""" Format Helper Functions """


def format_usb_approval_data(obj):
    """Format Approval Data Helper Function"""
    return {
        'id': obj.id,
        'vendor_id': obj.vendor_id,
        'vendor_name': obj.vendor_name,
        'product_id': obj.product_id,
        'product_name': obj.product_name,
        'serial_number': obj.serial_number,
        'notes': obj.notes,
        'approval_name': obj.approval_name,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at
    }


def format_usb_block_data(obj):
    """Format Block Data Helper Function"""
    return {
        'id': obj.id,
        'policy_id': obj.policy_id,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at
    }


def format_usb_device(obj):
    """Format Device Helper Function"""
    return {
        'id': obj.id,
        'first_seen': obj.first_seen,
        'last_seen': obj.last_seen,
        'vendor_name': obj.vendor_name,
        'vendor_id': obj.vendor_id,
        'product_name': obj.product_name,
        'product_id': obj.product_id,
        'serial_number': obj.serial_number,
        'last_endpoint_name': obj.last_endpoint_name,
        'last_endpoint_id': obj.last_endpoint_id,
        'last_policy_id': obj.last_policy_id,
        'endpoint_count': obj.endpoint_count,
        'device_friendly_name': obj.device_friendly_name,
        'device_name': obj.device_name,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'status': obj.status
    }


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

    # USB Device Approvals
    """USB Device Control Approval"""
    print('USB Device Control Approvals')
    print(SYMBOLS * DELIMITER)

    # create the usb device approval
    data = [{
        "vendor_id": "0x0781",
        "product_id": "0x5581",
        "serial_number": "4C531001331122115172",
        "notes": "A few notes",
        "approval_name": "Example Approval"}]
    sdk_result = USBDeviceApproval.bulk_create(cb, data)
    sdk_created_obj = sdk_result[0]

    sdk_obj = USBDeviceApproval(cb, sdk_created_obj.id)
    api_result = get_usb_device_approval_by_id_api(sdk_created_obj.id).json()
    dict_sdk_obj = format_usb_approval_data(sdk_obj)
    assert api_result == dict_sdk_obj, 'Get Approval by ID Failed - ' \
           'Expected: {}, Actual: {}'.format(api_result, dict_sdk_obj)
    print('Get Approval by ID............................OK')

    # get the USB Device Approval
    query = cb.select(USBDeviceApproval)
    sdk_results = []
    for approval in query:
        if approval.id == sdk_created_obj.id:
            print('Bulk Create Test..............................OK')
        sdk_results.append(format_usb_approval_data(approval))
    api_search = search_usb_device_approval().json()['results']
    assert sdk_results == api_search, 'Search Test Failed Expected: {}, ' \
        'Actual: {}'.format(api_search, sdk_results)
    print('Search Test...................................OK')

    # update the object
    sdk_created_obj.approval_name = 'Changed Approval'
    sdk_created_obj._update_object()
    sdk_created_new = None
    query = cb.select(USBDeviceApproval)
    sdk_created_new = query[0]
    assert sdk_created_new.approval_name == 'Changed Approval', 'Update Test '\
        'Failed - Excepted: {}, Actual: {}'.format(
            format_usb_approval_data(sdk_created_obj),
            format_usb_approval_data(sdk_created_new))
    print('Update Test...................................OK')

    # delete the usb approval
    if sdk_created_obj is not None:
        sdk_created_obj.delete()
    query = cb.select(USBDeviceApproval)
    assert query._total_results == 0, 'Delete Approval Test Failed - Record '\
        'was not deleted... {}'.format(query._total_results)
    print('Delete Approval...............................OK')
    print(NEWLINES * '\n')

    """USB Device Control Blocks"""
    print('USB Device Control Blocks')
    print(SYMBOLS * DELIMITER)

    # create the usb device block
    data = ["6997287"]
    sdk_result = USBDeviceBlock.bulk_create(cb, data)
    sdk_created_obj = sdk_result[0]

    api_result = get_usb_device_block_by_id_api(sdk_created_obj.id).json()
    block_obj = USBDeviceBlock(cb, sdk_created_obj.id)
    dict_block_obj = format_usb_block_data(block_obj)
    assert dict_block_obj == api_result, 'Get Block by ID Failed - Expected: '\
        '{}, Actual: {}'.format(api_result, dict_block_obj)
    print('Get Block by ID...............................OK')
    # get the USB Device Block
    query = cb.select(USBDeviceBlock)
    sdk_results = []
    for block in query:
        if block.id == sdk_created_obj.id:
            print('Bulk Create Test..............................OK')
        sdk_results.append(format_usb_block_data(block))
    api_search = search_usb_device_blocks().json()['results']
    assert sdk_results == api_search, 'Search Test Failed Expected: {}, ' \
        'Actual: {}'.format(api_search.json()['results'], sdk_results)
    print('Search Test...................................OK')

    # delete the usb approval
    if sdk_created_obj is not None:
        sdk_created_obj.delete()
    query = cb.select(USBDeviceBlock)
    assert query._total_results == 0, 'Delete Block Failed - Record was not '\
        'deleted... {}'.format(query._total_results)
    print('Delete Block..................................OK')
    print(NEWLINES * '\n')

    """USB Devices"""
    print('USB Devices')
    print(SYMBOLS * DELIMITER)

    query = cb.select(USBDevice)
    sdk_results = []
    for device in query:
        sdk_results.append(format_usb_device(device))
    api_search = search_usb_devices().json()
    assert api_search['num_found'] == query._total_results, 'Device Search ' \
           'Failed - Expected: {}, Actual: {}'.format(api_search['num_found'],
                                                      query._total_results)
    assert sdk_results == api_search['results'], 'Device Search Test Failed -'\
        'Expected: {}, Actual: {}'.format(api_search['results'], sdk_results)
    print('Device Search.................................OK')

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


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
