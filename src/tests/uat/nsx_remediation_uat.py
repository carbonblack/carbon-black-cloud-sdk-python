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
To execute, a profile must be provided using the standard CBC Credentials.

The following API calls are tested in this script:

Workload:
* NSX Remediation
  * https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/
            appliance-service/#nsx-remediation
"""

import sys
import random
import time

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.workload import NSXRemediationJob
from cbc_sdk.errors import ApiError, ServerError, NSXJobError


def get_devices(cb, ids):
    """
    Gets the devices that can be tested with NSX Remediation, i.e., for which nsx_available is True.

    Args:
        cb (CBCloudAPI): The API connection object.
        ids (list[int]: List of IDs explicitly selected. If empty, all devices will be selected in random order.

    Returns:
        list[Device]: A list of possible devices to use for the test.
    """
    query = cb.select(Device)
    base_devices = [d for d in query if d.nsx_available]
    devices = []
    if not base_devices:
        raise RuntimeError("ERROR: no devices in org with NSX available")
    print(f"{len(base_devices)} device(s) available for testing")
    if ids:
        for v in ids:
            devices.extend([d for d in base_devices if d.id == v])
    else:
        devices = random.sample(base_devices, k=len(base_devices))
    if not devices:
        raise RuntimeError("ERROR: no devices selected for testing")
    print(f"{len(devices)} device(s) selected for testing")
    return devices


def test_one_combo(device, tag, toggle):
    """
    Run an NSX remediation test on a specific combination of arguments.

    Args:
        device (Device): The device under test.
        tag (str): The NSX tag being set.
        toggle (bool): True if the tag is being set, False if it's being removed.

    Returns:
        bool: True if the test completed (possibly with errors printed), False if the device was not suitable for test.
    """
    print(f"Testing ({tag}, {toggle}) on device #{device.id}")
    try:
        job = device.nsx_remediation(tag, toggle)
        if job is None:
            print(f"Setting ({tag}, {toggle}) on device #{device.id} was a no-op")
            return True
        job.await_result()
        device.refresh()
        if toggle and device.nsx_distributed_firewall_policy != tag:
            print(f"ERROR: after ({tag}, {toggle}) set, expected {tag}, got {device.nsx_distributed_firewall_policy}")
        elif toggle is False and device.nsx_distributed_firewall_policy is not None:
            print(f"ERROR: after ({tag}, {toggle}) set, expected None, got {device.nsx_distributed_firewall_policy}")
        else:
            print(f"Setting ({tag}, {toggle}) on device #{device.id} OK")
    except NSXJobError:
        print(f"...Device #{device.id} not suitable for testing or erroneous state, try again")
        return False
    except ServerError as e:
        print(f"ERROR: setting ({tag}, {toggle}) on device #{device.id} failed: {e}")
    except ApiError as e:
        print(f"ERROR: setting ({tag}, {toggle}) on device #{device.id} failed: {e}")
    return True


def test_device(device):
    """
    Run a NSX test sequence on the specified device.

    Args:
        device (Device): The device under test.

    Returns:
        bool: True if the test completed (possibly with errors printed), False if the device was not suitable for test.
    """
    print(f"Beginning test on device #{device.id}")

    # if the device has a current policy, unset it
    before_tag = device.nsx_distributed_firewall_policy
    if before_tag:
        if not test_one_combo(device, before_tag, False):
            return False

    device.refresh()
    if device.nsx_distributed_firewall_policy is not None:
        print(f"ERROR: Device #{device.id} in invalid state pre-test")
        return True

    # set, then unset, each policy in turn
    for tag in NSXRemediationJob.VALID_TAGS:
        for toggle in (True, False):
            if not test_one_combo(device, tag, toggle):
                return False
            time.sleep(2)

    # if the device had a current policy when we started, restore it
    if before_tag:
        if not test_one_combo(device, before_tag, True):
            return False

    device.refresh()
    if device.nsx_distributed_firewall_policy != before_tag:
        print(f"ERROR: Device #{device.id} in invalid state post-test")
    return True


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument('-i', '--id', action='append', nargs='+', type=int,
                        help='IDs of devices to be used in testing')
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    devices = get_devices(cb, args.id)
    for device in devices:
        test_result = test_device(device)
        if test_result:
            print("Test completed")
            return 0
    print("ERROR: no device found suitable for testing")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
