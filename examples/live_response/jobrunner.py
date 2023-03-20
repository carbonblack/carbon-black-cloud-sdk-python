#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2021-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Example test for Live Response"""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device
from concurrent.futures import as_completed
import sys
from datetime import datetime, timedelta

FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument("--job", action="store", default="examplejob", required=True)

    args = parser.parse_args()

    cb = get_cb_cloud_object(args)

    device_query = cb.select(Device)

    # Retrieve the list of devices that are online
    # calculate based on devices that have checked in during the last five minutes
    now = datetime.utcnow()
    delta = timedelta(minutes=5)

    online_devices = []
    offline_devices = []
    for device in device_query:
        if now - datetime.strptime(device.last_contact_time, FORMAT) < delta:
            online_devices.append(device)
        else:
            offline_devices.append(device)

    print("The following devices are offline and will not be queried:")
    for device in offline_devices:
        print("  {0}: {1}".format(device.id, device.name))

    print("The following devices are online and WILL be queried:")
    for device in offline_devices:
        print("  {0}: {1}".format(device.id, device.name))

    # import our job object from the jobfile
    job = __import__(args.job)
    jobobject = job.getjob()

    completed_devices = []
    futures = {}

    # collect 'future' objects for all jobs
    for device in online_devices:
        f = cb.live_response.submit_job(jobobject.run, device)
        futures[f] = device.id

    # iterate over all the futures
    for f in as_completed(futures.keys(), timeout=100):
        if f.exception() is None:
            print("Device {0} had result:".format(futures[f]))
            print(f.result())
            completed_devices.append(futures[f])
        else:
            print("Device {0} had error:".format(futures[f]))
            print(f.exception())

    still_to_do = set([s.id for s in online_devices]) - set(completed_devices)
    print("The following devices were attempted but not completed or errored out:")
    for device in still_to_do:
        print("  {0}".format(device))


if __name__ == '__main__':
    sys.exit(main())
