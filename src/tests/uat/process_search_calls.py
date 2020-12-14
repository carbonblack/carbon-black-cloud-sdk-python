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

"""
The following API calls are tested in this script.
Validation is manual; either from information in the console or running an equivalent API call from postman

To execute, a profile must be provided using the standard CBC Credentials.

Processes:
* Process Search Validation (v1)
* Get a List of All Available Process Result Sets (v1)
* Start a Process Search (v2)
* Get the Status of a Process Search (v1)
* Retrieve Results for a Process Search (v2)
* Start a Facet Search on Processes (v2)
* Retrieve Results for a Process Facets Search (v2)

Process Events:
* Get Validation for Event Search (v1)
* Get Events Associated with a Given Process (v2)

Enriched Events
* Start an Enriched Events Search (v2)
* Get the Enriched Events Search Status (v1)
* Retrieve Results for an Enriched Events Search (v2)
* Retrieve Results for an Enriched Events Facet Search (v2)

The following calls will be added soon.  Work on the SDK is in progress.
* Get Events Facet Associated with a Process (v2)
* Start Aggregation Search on Enriched Events (v1)
* Retrieve Results for an Enriched Event Aggregation Search (v1)
* Request Details for Enriched Events (v2)
* Get the Enriched Events Detail Search Status (v2)
* Retrieve Results for an Enriched Event Detail Search (v2)

The following calls will be added when the API on CBC is complete
* Request Details of Processes (v2)
* Get the Status of a Process Detail Search (v2)
* Retrieve Results for a Process Detail Search (v2)
* Start a Process Summary Search (v2)
* Get the Status of Process Summary Search (v2)
* Retrieve Results for a Process Summary or Tree Search (v2)

The following calls are not planned to be included in the SDK.
If there is customer demand, this can be reviewed.
* Process Search Suggestions (v1)
* Get Time Limits for Available Data (v1)
* Get Suggestions for Event Searching (v1)
* Calls using Enterprise EDR Watchlist Features
* Evaluate Processes for a Watchlist (v1)
* Get Report Hits (v1)

"""

# Standard library imports
import sys
from pprint import pprint

# Internal library imports
from pprint import pprint
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object, CBCloudAPI
from cbc_sdk.platform import Process, Event, ProcessFacet, EventFacet
from cbc_sdk.endpoint_standard import EnrichedEvent, EnrichedEventFacet
from cbc_sdk.errors import ApiError


def run_process_invalid_search(cb, print_detail):
    """
    Tests that Process Search Validation is being called by putting an invalid field name in the where clause

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging

    Returns:
    """
    print("API Call: Process Search Validation (v1)")
    print("Executing request with Invalid Search field\n")
    process_query = cb.select(Process).where("enrichedBADFIELD:true")
    try:
        matching_processes = [process for process in process_query]
    except ApiError as e:
        print("Expected result: APIError generated")
        if print_detail:
            print(e)
    print(f"End: process_invalid_search")
    print("----------------------------------------------------------")


def run_process_event_invalid_search(cb, print_detail):
    """
    Tests that Event Search Validation is being called by putting an invalid field name in the where clause

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging

    Returns:
    """
    print("API Call Get Validation for Event Search (v1)")
    print("Executing request with Invalid Search field\n")
    event_query = cb.select(Event).where("enrichedBADFIELD:true")
    try:
        matching_events = [e for e in event_query]
    except ApiError as e:
        print("Expected result: APIError generated")
        if print_detail:
            print(e)
    print(f"End: run_process_event_invalid_search")
    print("----------------------------------------------------------")


def get_list_of_available_process_results(cb, print_details):
    """
    Executes Get a List of All Available Process Result Sets
    Compare to results of this route, no body, no parameters.
    {{base_url}}/api/investigate/v1/orgs/{{org_key}}/processes/search_jobs

    Args:
        cb:
        print_details:

    Returns:

    """
    print("API Call: Get a List of All Available Process Result Sets (v1)\n")
    process_queries = cb.fetch_process_queries()
    print(f"there were {len(process_queries)} process queries found")
    print("called fetch_process_queries")
    print("----------------------------------------------------------")


def get_events_facet_associated_with_a_process(cb, print_detail, process_guid):
    """
    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging

    Returns:
    """
    print("API Call: Get Events Facet Associated with a Process (v2)\n")
    facet_query = cb.select(EventFacet).where(process_guid=process_guid)
    facet_query.add_facet_field(["event_type"]).timeout(60000)
    facet_query.set_rows(10)

    future = facet_query.execute_async()
    while not future.done():
        pass

    results = future.result()[0]
    pretty_response = {"ranges": results.ranges,
                        "terms": results.terms,
                        "num_found": results.num_found,
                        "total_segments": results.total_segments,
                        "processed_segments": results.processed_segments}
    pprint(pretty_response, sort_dicts=False)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def get_process_basic_window_enriched(cb, print_detail, window):
    """
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

    print(f"End: get_process_basic_window_enriched")
    print("----------------------------------------------------------")
    # return the first process id for use in future tests
    return matching_processes[6].process_guid


def get_process_events_for_single_process(cb, print_detail, guid):
    """

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        guid: All events retrieved for this process guid

    Returns:

    """
    print("API Call: Get Events Associated with a Given Process (v2)\n")
    events_query = cb.select(Event).where(process_guid=guid)
    events_query.sort_by("backend_timestamp", direction="ASC")
    events = [ev for ev in events_query]
    print(f"events_query has {len(events_query)} in len(events_query)")
    print(f"events_query has {events_query._total_results} in events_query._total_results")
    print(
        f"events_query._total_segments = {events_query._total_segments} and events_query._processed_segments = {events_query._processed_segments}")
    print(
        f"There are {len(events)} to print. First timestamp = {events[0].event_timestamp}.  Last timestamp = {events[len(events) - 1].event_timestamp}")
    if print_detail:
        print(f"input process guid = {guid}")
        print("event.event_guid,event.event_hash,event.process_guid,event.backend_timestamp,event.event_timestamp")
        print("=========--=============")
        for event in events:
            print(
                f"{event.event_guid},{event.event_hash},{event.process_guid},{event.backend_timestamp},{event.event_timestamp}")

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def get_process_facet(cb, print_detail, window):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
    """
    print("API Calls:")
    print("Start a Facet Search on Processes (v2)")
    print("Retrieve Results for a Process Facets Search (v2)\n")

    facet_query = cb.select(ProcessFacet).where("process_name:chrome.exe")
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
            print(f"{future.done()} - looping")

    results = future.result()[0]
    print(f"terms facets = ")
    pprint(results.terms_.facets)
    print(f"terms fields = {results.terms_.fields}")
    print(f"ranges facets = {results.ranges_.facets}")
    print(f"ranges fields = {results.ranges_.fields}")

    print(f"End: get_process_facet")
    print("----------------------------------------------------------")


def get_event_facet(cb, print_detail, window):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
    """
    print(f"Start: get_event_facet")
    print("Not implemented in SDK")
    # facet_query = cb.select(EventFacet).where("process_name:chrome.exe")
    # facet_query.add_range({"bucket_size": "+1DAY",
    #                        "start": "2020-11-01T00:00:00Z",
    #                        "end": "2020-11-30T00:00:00Z",
    #                        "field": "backend_timestamp"})
    # facet_query.add_facet_field(["alert_category", "device_external_ip", "backend_timestamp"]).timeout(60000)
    # facet_query.set_time_range(window=window)
    # facet_query.set_rows(5)
    # future = facet_query.execute_async()
    # while not future.done():
    #     if print_detail:
    #         print(f"{future.done()} - looping")
    #
    # results = future.result()[0]
    # print(f"terms facets = ")
    # pprint(results.terms_.facets)
    # print(f"terms fields = {results.terms_.fields}")
    # print(f"ranges facets = {results.ranges_.facets}")
    # print(f"ranges fields = {results.ranges_.fields}")

    print(f"End: get_event_facet")
    print("----------------------------------------------------------")


def get_enriched_events_for_single_process(cb, print_detail, guid):
    """

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        guid: All enriched events retrieved for this process guid

    Returns:

    """
    print("API Calls:")
    print("Start an Enriched Events Search (v2)")
    print("Get the Enriched Events Search Status (v1)")
    print("Retrieve Results for an Enriched Events Search (v2)\n")
    enriched_events_query = cb.select(EnrichedEvent).where(process_guid=guid)
    events = [ev for ev in enriched_events_query]
    print(f"enriched events_query has {len(enriched_events_query)} in len(enriched_events_query")
    print(f"enriched events_query has {enriched_events_query._total_results} in enriched_events_query._total_results")
    print("End: get_enriched_events_for_single_process")
    print("----------------------------------------------------------")


def get_enriched_event_facet(cb, print_detail, window):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
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
            print(f"{future.done()} - looping")

    results = future.result()[0]
    print(f"terms facets = ")
    pprint(results.terms_.facets)
    print(f"terms fields = {results.terms_.fields}")
    print(f"ranges facets = {results.ranges_.facets}")
    print(f"ranges fields = {results.ranges_.fields}")

    print(f"End: get_enriched_event_facet")
    print("----------------------------------------------------------")


def main():
    parser = build_cli_parser()  # args on command line will be applied to all tests called
    args = parser.parse_args()
    print_detail = args.verbose
    window = '-' + args.window

    do_process = True
    do_enriched_events = True

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    process_guid = ""
    cb = get_cb_cloud_object(args)
    if do_process:
        process_guid = get_process_basic_window_enriched(cb, print_detail, window)
        get_process_events_for_single_process(cb, print_detail, process_guid)
        run_process_invalid_search(cb, print_detail)
        run_process_event_invalid_search(cb, print_detail)
        get_process_facet(cb, print_detail, window)
        get_list_of_available_process_results(cb, print_detail)
        get_events_facet_associated_with_a_process(cb, print_detail, process_guid)
    if do_enriched_events:
        if not process_guid:
            process_guid = get_process_basic_window_enriched(cb, print_detail, window)
        get_enriched_events_for_single_process(cb, print_detail, process_guid)
        get_enriched_event_facet(cb, print_detail, window)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
