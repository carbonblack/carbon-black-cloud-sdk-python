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

Workload:
* NSX Remediation
  * https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/appliance-service/#nsx-remediation
"""

import sys
import random

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.workload import NSXRemediationJob
from cbc_sdk.errors import ApiError, ServerError, NSXJobError


def get_devices(cb, ids):
    """
    Gets the devices that can be tested with NSX Remediation.

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


def test_device(device):
    """
    Run a NSX test sequence on the specified device.

    Args:
        device (Device): The device under test.

    Returns:
        bool: True if the test completed (possibly with errors printed), False if the device was not suitable for test.
    """
    print(f"Beginning test on device #{device.id}")
    before_tags = device.nsx_tags
    pass1_toggles = [(False if tag_val in before_tags else True) for tag_val in NSXRemediationJob.VALID_TAGS]
    pass2_toggles = [not v for v in pass1_toggles]
    new_state = set(before_tags)
    for toggle_list in (pass1_toggles, pass2_toggles):
        for tag, toggle in zip(NSXRemediationJob.VALID_TAGS, toggle_list):
            if toggle:
                new_state.add(tag)
            else:
                new_state.remove(tag)
            try:
                job = device.nsx_remediation(tag, toggle)
                job.await_result()
                device.refresh()
                if device.nsx_tags != new_state:
                    print(f"ERROR: after ({tag}, {toggle}) set, expected {new_state}, got {device.nsx_tags}")
                else:
                    print(f"Setting ({tag}, {toggle}) on device #{device.id} OK")
                continue
            except NSXJobError:
                print(f"...Device #{device.id} not suitable for testing, try again")
                return False
            except ServerError as e:
                print(f"ERROR: setting ({tag}, {toggle}) on device #{device.id} failed: {e}")
                continue
            except ApiError as e:
                print(f"ERROR: setting ({tag}, {toggle}) on device #{device.id} failed: {e}")
                continue

    device.refresh()
    if device.nsx_tags != before_tags:
        print(f"ERROR: should have returned state of device #{device.id} to {before_tags}, but got {device.nsx_tags}")
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
    print(f"ERROR: no device found suitable for testing")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
