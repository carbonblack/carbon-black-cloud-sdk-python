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
from cbc_sdk.platform import Alert, WatchlistAlert, GroupedAlert
from cbc_sdk.platform import Device

# To see the http requests being made, and the structure of the search requests enable debug logging
# import logging
# logging.basicConfig(level=logging.DEBUG)


def alert_workflow(api):
    """The workflow was simplified in SDK 1.5.0 to align with Alert v7 API.

    1. Use an Alert Search to specify the alerts that will have their status updated

    * The request body is a search request and all alerts matching the request will be updated.
    * Two common uses are to update one alert, or to update all alerts with a specific threat id.
    * Any search request can be used as the criteria to select alerts to update the alert status.

    2. Submit a job to update the status of Alerts.

    * The status can be ``OPEN``, ``IN PROGRESS`` or ``CLOSED`` (previously ``DISMISSED``).
    * A Closure Reason may be included.

    3. The immediate response confirms the job was successfully submitted.

    4. Use the :py:mod:`Job() cbc_sdk.platform.jobs.Job` class to determine when the update is complete.

    * Use job.await_completion().result()

    5. Refresh the Alert Search to get the updated alert data into the SDK.

    6. The future Alerts with the same threat id can be set to automatically close.
    """
    # This example closes a single alert.  Any alert search can be used.
    alert_query = api.select(Alert).set_rows(1)
    # get the first alert. This is not needed to modify the status, but it's useful to print info
    alert = alert_query.first()

    print("about to call update to closed")
    job = alert_query.update("CLOSED", "RESOLVED", "NONE", "Setting to closed for SDK demo")
    print("job.id = {}".format(job.id))
    # This is an asynchronous request meaning that HTTP response 200 means the request to change status was successful
    # Use the job object to determine when the work has been completed.
    job.await_completion().result()
    # refresh the alert to get the updated data from Carbon Black Cloud into the SDK
    alert.refresh()

    print("Status = {}, Expecting CLOSED. After job.await_completion().result() + alert.refresh()".format(
        alert.workflow["status"]))
    print("Status = {}, Expecting CLOSED".format(alert.workflow["status"]))
    # So we can run this script again, return the alert to OPEN
    job = alert_query.update("OPEN", "OTHER", "NONE", "Setting to open to reset after the SDK demo")
    job.await_completion().result()
    alert.refresh()
    print("Status = {}, Expecting return to OPEN at the end".format(
        alert.workflow["status"]))
    # view the history of changes on the alert
    print("printing the history of this alert")
    for h in alert.get_history():
        print(h)

    print("Dismissing all future alerts with the same threat id as the current threat")
    alert.dismiss_threat("threat remediation done", "testing dismiss_threat in the SDK")
    print("Future alerts with that threat Id will be Dismissed / Closed")

    print("Un-Dismissing future alerts with the same threat id")
    alert.update_threat("threat remediation un-done", "testing update_threat in the SDK")
    print("Future alerts with that threat Id will not be Dismissed / Closed")


def main():
    """This script demonstrates how to use Alerts in the SDK and common operations to link to related objects.

    This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
    Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

    This is written for clarity of explanation, not perfect coding practices.
    """
    # CBCloudAPI is the connection to the cloud.  It holds the credentials for connectivity.
    # To execute this script, the profile must have an API key with the following permissions.
    # If you are restricted in the actions you're allowed to perform, expect a 403 response for missing permissions
    # Permissions are set on Settings -> API Access -> Access Level and then assigned to an API Key
    # Alerts - org.alerts - READ: For Alert searching and facets
    # Alerts - org.alerts.tags - CREATE, READ, DELETE
    # Search - org.search.events - CREATE, READ: For Process and Observation searches
    # Device - device - READ: For Device Searches
    # Alerts - org.alerts.close - EXECUTE:
    # Alerts - org.alerts.notes - CREATE, READ, UPDATE, DELETE
    # Alerts - ThreatMetadata - org.xdr.metadata - READ
    # Background tasks - Status - jobs.status - READ: To get the job status when closing alerts

    api = CBCloudAPI(profile="YOUR_PROFILE_HERE")

    # workflow is in a separate method.
    # alert_workflow(api)

    # To start, get some alerts that have a few interesting criteria set for selection.
    # All the fields that can be used are on the Developer Network
    # https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/

    # start by specifying Alert as the type of object to search
    alert_query = api.select(Alert)

    # add_criteria is used for all fields that are searchable arrays
    alert_query.add_criteria("device_os", "WINDOWS")
    # when the field is a single value, a set_xxx function is used.
    alert_query.set_minimum_severity(3)
    # and limit the time to the last day
    alert_query.set_time_range(range="-10d")
    # rows default to 100, let's override that
    alert_query.set_rows(1000)
    # and I think that Watchlist alerts are really noisy, so I'm going to exclude them from the results
    alert_query.add_exclusions("type", "WATCHLIST")
    # Wasn't that easier than crafting this json and making a curl request?
    # {
    #     "criteria": {
    #         "device_os": [
    #             "WINDOWS"
    #         ],
    #         "minimum_severity": 3
    #     },
    #     "exclusions": {
    #         "type": [
    #             "WATCHLIST"
    #         ]
    #     },
    #     "rows": 1000,
    #     "time_range": {
    #         "range": "-1d"
    #     }
    # }

    # Trigger the query to be executed on Carbon Black Cloud.  Any access the result set will trigger this.
    # Including, iterating through the results (for alert in alert_query: ...), first() and one() methods
    print("{} Alerts were returned".format(len(alert_query)))

    # Up to 25,000 Alerts can also be exported to a CSV.  This reuses the alert_query object set up for the search.
    job = alert_query.export()
    job.await_completion().result()
    csv_report = job.get_output_as_string()
    print(csv_report)

    # Get a single alert to work with.  This could be in an iterator
    alert = alert_query.first()
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
    print("Printing history of the alert")
    for h in history:
        print(h)
    # clean up our notes
    new_note.delete()
    new_threat_note.delete()

    # Here is how to call facets.
    # Facets generate statistics indicating the relative weighting of values for the specified terms.
    print("\nShowing a facet request and response\n")
    # This is an example of a field in v6 that is unchanged in v7.  This code snippet will continue to succeed.
    facet_list = api.select(Alert).facets(["policy_applied", "attack_technique"])
    # The base object (e.g. Alert) has pretty printing implemented.  We're working on other objects.  Sorry.
    print("This is a valid facet response: {}".format(json.dumps(facet_list, indent=4)))

    # Contextual information around the Alert
    # Observations
    observation_list = alert.get_observations()
    if observation_list is not None:
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

    # For watchlist alerts in particular sometimes we would like to know more obout the associated watchlists
    print("This is the list of watchlist id name pairs for this alert:")
    print(watchlist_alert.get("watchlists"))

    watchlist_objects = watchlist_alert.get_watchlist_objects()
    print("These objects are associated with this alerts watchlists:")
    for object in watchlist_objects:
        print(object)

    # Run a Grouped Alert Search to group our alerts by threat_id
    # Start by specifying a GroupedAlert as the type of object to search
    grouped_alert_search_query = api.select(GroupedAlert)
    # then much like our AlertSearchQuery define the search query
    grouped_alert_search_query = grouped_alert_search_query.set_time_range(range="-10d")\
        .add_criteria("type", "WATCHLIST").set_minimum_severity(1)
    # run the query to retrieve
    grouped_alert_search_query.all()
    # and iterate through our GroupAlert objects
    print([group_alert for group_alert in grouped_alert_search_query])

    # to retrieve only the first GroupAlert object
    group_alert = grouped_alert_search_query.first()
    # to view the most recent alert on the object
    print(group_alert.most_recent_alert_)

    # to create the alert search query for a given group alert
    alert_search_query = group_alert.get_alert_search_query()
    print([alert for alert in alert_search_query])

    # to convert an AlertSearchQuery to a GroupAlertSearchQuery, will not preserve sort order
    group_alert_search_query = alert_search_query.set_group_by("threat_id")

    # to convert a GroupAlertSearchQuery to an AlertSearchQuery, will not preserve sort order
    alert_search_query = group_alert_search_query.get_alert_search_query()

    # to create the facets on a grouped alert search query
    grouped_alert_facets = group_alert_search_query.facets(["type", "THREAT_ID"], 0, True)
    print(grouped_alert_facets)

    # to retrieve the Network Threat Metadata from an ids alert we first retrieve an ids alert
    alert_query = api.select(Alert)
    alert_query.add_criteria("type", "INTRUSION_DETECTION_SYSTEM").set_time_range(range="-6M")
    ids_alert = alert_query.first()

    # then just call the get_network_threat_metadata
    network_threat_metadata = ids_alert.get_network_threat_metadata()
    print(network_threat_metadata)


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
