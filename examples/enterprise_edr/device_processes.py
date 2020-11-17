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

import sys
import logging
import concurrent.futures
from cbc_sdk.helpers import eprint, build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from cbc_sdk.enterprise_edr import Process

log = logging.getLogger(__name__)


def main():
    parser = build_cli_parser()

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    query = cb.select(Device).where('1')
    devices = list(query)
    if args.verbose:
        print(f"Querying {len(devices)} device(s)...")
    active_queries = set()
    for device in devices:
        query = cb.select(Process).where(f"device_id:{device.id}").set_time_range(window='-6h')
        if args.verbose:
            print(f"Sending query for device ID {device.id}...")
        active_queries.add(query.execute_async())

    if args.verbose:
        print("Done sending queries, waiting for responses...")
    concurrent.futures.wait(active_queries)
    print("{0:16} {1:5} {2:60}".format("Device Name", "PID", "Process Name"))
    print("{0:16} {1:5} {2:60}".format("-----------", "---", "------------"))
    for future in active_queries:
        result = future.result()
        for process in result:
            print("{0:16} {1:5} {2:60}".format(process['device_name'], process['process_pid'][0],
                                               process['process_name']))

if __name__ == "__main__":
    sys.exit(main())
