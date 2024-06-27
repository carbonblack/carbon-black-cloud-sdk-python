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
The following API calls are tested in this script.

For the validation CBC API requests are used.

To execute, a profile must be provided using the standard CBC Credentials.

Processes:
- Get alert and get the enriched events for that alert
"""

# Standard library imports
import datetime
from pprint import pprint
import requests
import sys
import time

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.endpoint_standard import EnrichedEvent, EnrichedEventFacet
from cbc_sdk.platform.alerts import CBAnalyticsAlert
from cbc_sdk.platform import Process


HEADERS = {"X-Auth-Token": "", "Content-Type": "application/json"}
ORG_KEY = ""
HOSTNAME = ""

# Formatters
NEWLINES = 1
DELIMITER = "-"
SYMBOLS = 60
TIMEOUT_MINS = 2

# URLS
START_JOB = "{}api/investigate/v2/orgs/{}/enriched_events/detail_jobs"
STATUS_JOB = "{}api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}"
GET_RESULTS = "{}api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}/results"


def start_search_job(alert_id):
    """Start a search job"""
    url = START_JOB.format(HOSTNAME, ORG_KEY)
    result = requests.post(url, json={"alert_id": alert_id}, headers=HEADERS)
    return result.json().get("job_id")


def get_status_search_job(job_id):
    """Check the status of a search job"""
    url = STATUS_JOB.format(HOSTNAME, ORG_KEY, job_id)
    return requests.get(url, headers=HEADERS)


def wait_till_job_ready(job_id):
    """Checking status of the job, till ready"""
    timeout_time = datetime.datetime.now() + datetime.timedelta(minutes=TIMEOUT_MINS)
    while True:
        result = get_status_search_job(job_id).json()
        searchers_contacted = result.get("contacted", 0)
        searchers_completed = result.get("completed", 0)
        if searchers_completed == searchers_contacted:
            break
        if searchers_contacted == 0:
            time.sleep(0.5)
            continue
        if searchers_completed < searchers_contacted:
            if timeout_time < datetime.datetime.now():
                break

        time.sleep(0.5)


def get_results_search_job(job_id):
    """Get the results of a search job"""
    url = GET_RESULTS.format(HOSTNAME, ORG_KEY, job_id)
    result = requests.get(url, headers=HEADERS).json()
    found_results = result.get("num_found", 0)
    if found_results == 0:
        return []
    return result.get("results", [])


# TODO rewrite the functons below
def get_process_basic_window_enriched(cb, print_detail, window):
    """
    Text

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
        process_guid of the first process in the returned list
    """
    print("\n----------------------------------------------------------")
    print("API Calls:")
    print("Start a Process Search (v2)")
    print("Get the Status of a Process Search (v1)")
    print("Retrieve Results for a Process Search (v2)\n")
    process_query = cb.select(Process).where("enriched:true")
    process_query.set_time_range(window=window)
    matching_processes = [process for process in process_query]
    print(f"There are {len(matching_processes)} found in {window} of processes")
    if print_detail:
        for process in matching_processes:
            print("{0:16} {1:5} {2:20}".format(process.device_name, process.process_pids[0], process.process_guid))

    try:
        print(f"process guid being used is {matching_processes[6].process_guid}")
        print("Test PASSED")
    except IndexError:
        print("Test FAILED")
    print("----------------------------------------------------------")

    return matching_processes[6].process_guid


def get_enriched_events_for_single_process(cb, guid):
    """
    Start SDK call and print out response

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        guid: All enriched events retrieved for this process guid
    """
    print("API Calls:")
    print("Start an Enriched Events Search (v2)")
    print("Get the Enriched Events Search Status (v1)")
    print("Retrieve Results for an Enriched Events Search (v2)\n")
    enriched_events_query = cb.select(EnrichedEvent).where(process_guid=guid)
    print(f"enriched events_query has {len(enriched_events_query)} in len(enriched_events_query")
    print(f"enriched events_query has {enriched_events_query._total_results} in enriched_events_query._total_results")

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")

    events = [_ for _ in enriched_events_query]

    return events[0].event_id


def get_enriched_event_facet(cb, print_detail, window):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search
    """
    print("API Calls:")
    print("Start a Facet Search on Enriched Events (v2)")
    print("Retrieve Results for an Enriched Events Facet Search (v2)\n")
    facet_query = cb.select(EnrichedEventFacet).where("process_name:chrome.exe")
    facet_query.add_range({"bucket_size": "+1DAY",
                           "start": "2020-11-01T00:00:00Z",
                           "end": "2020-11-30T00:00:00Z",
                           "field": "backend_timestamp"})
    facet_query.add_facet_field(["alert_category", "device_external_ip", "backend_timestamp"]).timeout(60000)
    facet_query.set_time_range(window=window)
    facet_query.set_rows(5)
    future = facet_query.execute_async()
    while not future.done():
        if print_detail:
            pass

    results = future.result()
    pprint(results._info, sort_dicts=False)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def enriched_events_details(cb, event_id):
    """Start SDK call and print out response"""
    print("API Calls:")
    print("Request Details for Enriched Events (v2)")
    print("Retrieve Results for an Enriched Event Detail Search (v2)")
    print(f"event_id: {event_id}\n")

    events = cb.select(EnrichedEvent).where(event_id=event_id)
    pprint(events[0].get_details()._info)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def enriched_events_aggregation(cb):
    """Start SDK call and print out response"""
    print("API Calls:")
    print("Start Aggregation Search on Enriched Events (v1)")
    print("Retrieve Results for an Enriched Event Aggregation Search (v1)\n")

    query = cb.select(EnrichedEvent).where("process_name:svchost.exe").aggregation("device_id")

    pretty_response = {"results": []}
    for event in query:
        pretty_response["results"].append(event._info)

    pprint(pretty_response)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def main():
    """Script entry point"""
    global ORG_KEY
    global HOSTNAME
    parser = build_cli_parser()
    parser.add_argument("--window", help="Define search window", default='3d')

    args = parser.parse_args()
    print_detail = args.verbose
    window = '-' + args.window

    if print_detail:
        print("args provided {}".format(args))

    cb = get_cb_cloud_object(args)
    HEADERS["X-Auth-Token"] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    print()
    print(17 * " ", "Enriched Events For Alerts")
    print(SYMBOLS * DELIMITER)
    # get alert created in the last four weeks, because enriched events are kept for some time
    query = cb.select(CBAnalyticsAlert).set_create_time(range="-4w")
    if len(query) == 0:
        return

    item = query[0]
    alert_id = item._info["legacy_alert_id"]
    eevents = [event._info for event in item.get_events()]

    job_id = start_search_job(alert_id)
    wait_till_job_ready(job_id)
    records = get_results_search_job(job_id)
    assert records == eevents, "Actual: {}, Expected: {}".format(records, eevents)
    print("Get events for CBAnalyticsAlert...........................OK")
    async_eevents = [event._info for event in item.get_events(async_mode=True).result()]
    assert records == async_eevents, "Actual: {}, Expected: {}".format(records, async_eevents)
    print("Get async events for CBAnalyticsAlert.....................OK")

    # TODO rewrite the functionality below
    process_guid = ""
    if not process_guid:
        process_guid = get_process_basic_window_enriched(cb, print_detail, window)
    event_id = get_enriched_events_for_single_process(cb, process_guid)
    get_enriched_event_facet(cb, print_detail, window)
    enriched_events_details(cb, event_id)
    enriched_events_aggregation(cb)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
