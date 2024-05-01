#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2024. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
This script identifies silent devices in the current organization.

A "silent device" is one which has checked in with the Carbon Black Cloud Server during a recent period of time,
the "checkin window," but has not sent any events within a certain period of time, the "event threshold."  The script
allows configuration of the checkin window (in days) and the event threshold (in minutes), as well as specifying to
only report on devices running selected operating systems.
"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from dateutil import parser


def main():
    """Main function for the script."""
    cmdparser = build_cli_parser("Identify silent devices")
    cmdparser.add_argument("-w", "--window", type=int, default=1,
                           help="The checkin window for devices (specified in days, default 1)")
    cmdparser.add_argument("-t", "--threshold", type=int, default=60,
                           help="The event threshold for devices (specified in minutes, default 60)")
    cmdparser.add_argument("-o", "--os", action='append', nargs='+',
                           help="Restrict query to these operating systems (multiple values permitted)")

    args = cmdparser.parse_args()
    cb = get_cb_cloud_object(args)

    device_query = cb.select(Device).set_last_contact_time(range=f"-{args.window}d").set_status(["ACTIVE"])
    if args.os:
        for sublist in args.os:
            device_query.add_criteria("os", sublist)
    devices = list(device_query)
    print(f"{len(devices)} device(s) have checked in during the last {args.window} day(s)")

    for device in devices:
        delta = parser.parse(device.last_contact_time) - parser.parse(device.last_reported_time)
        delta_minutes = round(delta.total_seconds() / 60)
        if delta_minutes >= args.threshold:
            print(f"Device {device.name} (ID={device.id}, OS={device.os}) "
                  f"last checked in = '{device.last_contact_time}', last reported data = '{device.last_reported_time}, "
                  f"delta = {delta_minutes} minutes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
