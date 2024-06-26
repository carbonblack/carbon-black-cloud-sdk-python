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
Example script illustrating retrieval of container runtime alerts.

Based on code written by Stephane List in the article "Carbon Black Container APIs Just got better! Get container
runtime alerts with CBC python SDK," VMware Carbon Black Tech Zone, June 20, 2022. (Permalink to article:
https://carbonblack.vmware.com/blog/carbon-black-container-apis-just-got-better-get-container-runtime-alerts-cbc-python-sdk)
Code modified and adapted for CBC SDK example script use by Amy Bowersox, Developer Relations.
"""

# Imports from the article's code
import sys
from cbc_sdk.platform import ContainerRuntimeAlert

# Additional imports to use the "helper" functions to perform command-line parsing and build a CBCloudAPI object from
# command-line arguments. Since we don't construct CBCloudAPI directly, we don't need to import it.
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


def main():
    """For convenience, all running code will be under this main function."""
    # Build a parser to parse standard command-line arguments for CBCloudAPI, and add some additional arguments.
    parser = build_cli_parser("Retrieve ContainerRuntimeAlerts from Carbon Black Cloud")
    parser.add_argument("-w", "--weeks", type=int, default=12,
                        help="Number of weeks to look back at alerts (default 12)")
    parser.add_argument("-f", "--find", default=None,
                        help="Find a specific string in alert reason, only print alerts with that reason")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--reason", action="store_true", help="Only show alert reason")
    group.add_argument("--ip", action="store_true", help="Only show alert remote IP address")

    # Parse the command line arguments and create a CBCloudAPI object. If you want to run against the "default"
    # credentials as written in the article, pass the command-line parameters "--profile default" to the script.
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    # Get Container Runtime alerts from the last however-many weeks.
    alerts = cb.select(ContainerRuntimeAlert).set_time_range('last_update_time', range=f"-{args.weeks}w")

    # This duplicates the main for-loop in the article's example code.
    for alert in alerts:
        # This complicated if allows us to bypass checking the alert reason if "find" was not specified.
        if not args.find or (args.find in alert.reason):
            # Based on the reason and ip flags, print out either the reason, the remote IP, or the whole alert.
            if args.reason:
                print(alert.reason)
            elif args.ip:
                print(alert.netconn_remote_ip)
            else:
                print(alert)

    return 0


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
