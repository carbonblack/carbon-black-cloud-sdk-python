#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
This example shows how to use the SDK the poll for alerts.

The SDK documentation is published on Read The Docs.  An Alerts Guide is available there.
https://carbon-black-cloud-python-sdk.readthedocs.io

This example contains the supporting code for the Alert Bulk Export -v 7 API Guide on Developer Network.
https://developer.carbonblack.com/reference/carbon-black-cloud/guides/alert-bulk-export
"""

import sys
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Alert

from datetime import datetime, timedelta, timezone


def main():
    """This script demonstrates how to use Alerts in the SDK and common operations to link to related objects."""
    api = CBCloudAPI(profile="YOUR_PROFILE_HERE")

    # Time field and format to use
    time_field = "backend_timestamp"
    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    # Time window to fetch.
    # Uses current time - 30s to allow for Carbon Black Cloud asynchronous event processing completion
    end = datetime.now(timezone.utc) - timedelta(seconds=30)
    start = end - timedelta(minutes=5)

    # Fetch initial Alert batch
    # the time stamp can be set either as a datetime object:
    # alerts_time_as_object = list(api.select(Alert).set_time_range(start=start, end=end).sort_by(time_field, "ASC"))
    # or as ISO 8601 strings
    alerts = list(api.select(Alert).set_time_range(start=start.isoformat(), end=end.isoformat())
                  .sort_by(time_field, "ASC"))

    # Check if 10k limit was hit.
    # Iteratively fetch remaining alerts by increasing start time to the last alert fetched
    if len(alerts) >= 10000:
        last_alert = alerts[-1]
        while True:
            new_start = datetime.strptime(last_alert.create_time, time_format) + timedelta(milliseconds=1)
            overflow = list(api.select(Alert)
                            .set_time_range(start=new_start, end=end)
                            .sort_by(time_field, "ASC"))

            # Extend alert list with follow up alert batches
            alerts.extend(overflow)
            if len(overflow) >= 10000:
                last_alert = overflow[-1]
            else:
                break

    print(f"Fetched {len(alerts)} alert(s) from {start.strftime(time_format)} to {end.strftime(time_format)}")


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
