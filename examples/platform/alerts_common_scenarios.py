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
This example shows how to use the Alerts API and relate Alerts to other objects such as Processes and Observations.

The SDK documentation is published on Read The Docs.  An Alerts Guide is available there.
https://carbon-black-cloud-python-sdk.readthedocs.io

If you are using SDK version 1.4.3 or earlier, see the related example script, alert_v6_v7_migration.py,
also in examples/platform and the Alert Migration Guide on Read the Docs on the changes that are needed.
SDK v1.5.0 does have breaking changes.
"""

import sys
import time
import json
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Alert, WatchlistAlert
from cbc_sdk.platform import Device

# To see the http requests being made, and the structure of the search requests enable debug logging
# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    """This script demonstrates how to use Alerts in the SDK and common operations to link to related objects.

    This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
    Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

    This is written for clarity of explanation, not perfect coding practices.
    """
    # CBCloudAPI is the connection to the cloud.  It holds the credentials for connectivity.
    # api = CBCloudAPI(profile="YOUR PROFILE HERE")
    api = CBCloudAPI(profile="TECH_AL")

    # To start, get some alerts that have a few interesting criteria set for selection.
    # All the fields that can be used are on the Developer Network
    # https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/

    # start by specifying Alert as the type of object to search
    alert_list = api.select(Alert)
    # add_criteria is used for all fields that are searchable arrays
    alert_list.add_criteria("device_os", "WINDOWS")
    # when the field is a single value, a set_xxx function is used.
    alert_list.set_minimum_severity(3)
    # and limit the time to the last day
    alert_list.set_time_range(range="-1d")
    # rows default to 100, let's override that
    alert_list.set_rows(1000)
    # and I think that Watchlist alerts are really noisy so I'm going to exclude them from the results
    alert_list.add_exclusions("type", "WATCHLIST")
    # Wasn't that easier than crafting this json and making a curl request?
    # {
    #     "criteria": {
    #         "device_os": [
    #             "WINDOWS"
    #         ],
    #         "minimum_severity": 7
    #     },
    #     "rows": 1000,
    #     "time_range": {
    #         "range": "-1d"
    #     }
    # }

    # Trigger the query to be executed on Carbon Black Cloud.  Any access the result set will trigger this.
    # Including, iterating through the results (for alert in alert_list: ...), first() and one() methods
    print("{} Alerts were returned".format(len(alert_list)))

    # Get a single alert to work with.  This could be in an iterator
    alert = alert_list.first()
    # here's the ID of the alert.  Use this to follow along in the console
    print("Alert id = {}".format(alert.id))

    # Check if there are any notes on the alert
    print("There are {} notes on the alert".format(alert.notes_()))
    # add a new note
    new_note = alert.create_note("Adding note from SDK with current timestamp: {}".format(time.time()))
    # notes can also be associated with the threat instead of the note
    new_threat_note = alert.create_note("Adding note to the threat from SDK, current timestamp: {}".format(time.time()))
    # print the history of what has happened on the alert
    history = alert.get_history()
    print("printing history of the alert")
    for h in history:
        print(h)
    # clean up our notes
    new_note.delete()
    new_threat_note.delete()

    # To do: Add facets

    # Contextual information around the Alert
    # Observations
    observation_list = alert.get_observations()
    len(observation_list)  # force the query execution
    print("There are {} related observations".format(len(observation_list)))

    # Which device was this alert on?
    device = api.select(Device, alert.device_id)
    print("Device Id:{}, Device Name:{}".format(device.id, device.name))

    # To get an export of the raw json alert, there's a to_json method.  Use this instead of the internal _info
    print("This is the json representation of the alert. There's a lot of useful data available.")
    print(json.dumps(alert.to_json(), indent=2))

    # Some information is only available for particular alert types
    # Processes
    # Get a Watchlist Alert.  select(WatchlistAlert) is equivalent to select(Alert).add_criteria("type", "WATCHLIST")
    watchlist_alert = api.select(WatchlistAlert).first()

    process = watchlist_alert.get_process()
    print("This is the process for the watchlist alert")
    print(process)


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
