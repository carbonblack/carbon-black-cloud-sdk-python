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

"""Example script listing devices"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device


def main():
    """Main function of the List Devices script."""
    parser = build_cli_parser("List devices")
    parser.add_argument("-q", "--query", help="Query string for looking for devices")
    parser.add_argument("-A", "--ad_group_id", action="append", type=int, help="Active Directory Group ID")
    parser.add_argument("-p", "--policy_id", action="append", type=int, help="Policy ID")
    parser.add_argument("-s", "--status", action="append", help="Status of device")
    parser.add_argument("-P", "--priority", action="append", help="Target priority of device")
    parser.add_argument("-S", "--sort_by", help="Field to sort the output by")
    parser.add_argument("-R", "--reverse", action="store_true", help="Reverse order of sort")
    parser.add_argument("-Y", "--asynchronous", action="store_true", help="Use asynchronous execution of query")
    parser.add_argument("-d", "--deployment_type", action="append", help="Deployment Type")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    query = cb.select(Device)
    if args.query:
        query = query.where(args.query)
    if args.ad_group_id:
        query = query.set_ad_group_ids(args.ad_group_id)
    if args.policy_id:
        query = query.set_policy_ids(args.policy_id)
    if args.status:
        query = query.set_status(args.status)
    if args.priority:
        query = query.set_target_priorities(args.priority)
    if args.sort_by:
        direction = "DESC" if args.reverse else "ASC"
        query = query.sort_by(args.sort_by, direction)
    if args.deployment_type:
        query = query.set_deployment_type(args.deployment_type)

    if args.asynchronous:
        future = query.execute_async()
        devices = future.result()
    else:
        devices = list(query)
    print("{0:9} {1:40}{2:18}{3}".format("ID", "Hostname", "IP Address", "Last Checkin Time"))
    for device in devices:
        print("{0:9} {1:40s}{2:18s}{3}".format(device.id, device.name or "None",
                                               device.last_internal_ip_address or "Unknown",
                                               device.last_contact_time))


if __name__ == "__main__":
    sys.exit(main())
