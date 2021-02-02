#!/usr/bin/env python3
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
Validation is manual; either from information in the console or running an equivalent API call from postman

To execute, a profile must be provided using the standard CBC Credentials.

The following API calls are tested in this script:

Devices:
* Search Devices
  * https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/devices-api/

"""

# Standard library imports
import sys
from pprint import pprint

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.errors import ApiError


def search_devices(cb):
    """Start SDK call and print out response"""
    print("API Calls:")
    print("Search Devices")

    query = cb.select(Device).set_deployment_type(["WORKLOAD"])
    for event in query:
        pprint(event._info)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()

    do_devices = True

    cb = get_cb_cloud_object(args)
    if do_devices:
        search_devices(cb)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
