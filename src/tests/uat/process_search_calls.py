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

Process Details:
* Request Details of Processes (v2)
* Get the Status of a Process Detail Search (v2)
* Retrieve Results for a Process Detail Search (v2)

Process Events:
* Get Validation for Event Search (v1)
* Get Events Associated with a Given Process (v2)

Enriched Events
* Start an Enriched Events Search (v2)
* Get the Enriched Events Search Status (v1)
* Retrieve Results for an Enriched Events Search (v2)
* Retrieve Results for an Enriched Events Facet Search (v2)

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
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Process, Event, ProcessFacet, EventFacet
from cbc_sdk.endpoint_standard import EnrichedEvent, EnrichedEventFacet
from cbc_sdk.errors import ApiError


def run_process_invalid_search(cb, print_detail):
    """
    Tests that Process Search Validation is being called by putting an invalid field name in the where clause

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
    """
    print("API Call: Process Search Validation (v1)")
    print("Executing request with Invalid Search field\n")
    process_query = cb.select(Process).where("enrichedBADFIELD:true")
    try:
        [process for process in process_query]
        print("Test FAILED")
    except ApiError as err:
        print("Expected result: APIError generated")
        if print_detail:
            print(err)
        print("Test PASSED")
    print("----------------------------------------------------------")


def run_process_event_invalid_search(cb, print_detail):
    """
    Tests that Event Search Validation is being called by putting an invalid field name in the where clause

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
    """
    print("API Call Get Validation for Event Search (v1)")
    print("Executing request with Invalid Search field\n")
    event_query = cb.select(Event).where("enrichedBADFIELD:true")
    try:
        [event for event in event_query]
        print("Test FAILED")
    except ApiError as err:
        print("Expected result: APIError generated")
        if print_detail:
            print(err)
        print("Test PASSED")
    print("----------------------------------------------------------")


def get_list_of_available_process_results(cb):
    """
    Executes Get a List of All Available Process Result Sets.

    Args:
        cb (CBCloudAPI): API object
    """
    print("API Call: Get a List of All Available Process Result Sets (v1)\n")
    process_queries = cb.fetch_process_queries()
    print(f"there were {len(process_queries)} process queries found")
    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def get_events_facet_associated_with_a_process(cb, process_guid):
    """
    Text

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        process_guid (string): process_guid
    """
    print("API Call: Get Events Facet Associated with a Process (v2)\n")
    facet_query = cb.select(EventFacet).where(process_guid=process_guid)
    facet_query.add_facet_field(["event_type"]).timeout(60000)
    facet_query.set_rows(10)

    future = facet_query.execute_async()
    while not future.done():
        pass

    results = future.result()
    pprint(results._info, sort_dicts=False)

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


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


def get_process_details_for_single_process(cb, guid):
    """
    Start API calls for getting process details and print the response.

    Args:
        cb (CBCloudAPI): API object
        guid (str): GUID of process to have details retrieved
    """
    print("API Calls:")
    print("Request Details of Processes (v2)")
    print("Get the Status of a Process Detail Search (v2)")
    print("Retrieve Results for a Process Detail Search (v2)")
    print(f"process_guid: {guid}\n")

    process_query = cb.select(Process).where(process_guid=guid)
    pprint(process_query[0].get_details())

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def get_process_events_for_single_process(cb, print_detail, guid):
    """
    Text

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        guid: All events retrieved for this process guid
    """
    print("API Call: Get Events Associated with a Given Process (v2)\n")
    events_query = cb.select(Event).where(process_guid=guid)
    events_query.sort_by("backend_timestamp", direction="ASC")

    events = [ev for ev in events_query]
    pretty_response = {"num_found": len(events_query),
                       "num_available": events_query._total_results,
                       "total_segments": events_query._total_segments,
                       "processed_segments": events_query._processed_segments}
    pprint(pretty_response, sort_dicts=False)
    print(f"\nThere are {len(events)} to print.")
    print(f"First timestamp = {events[0].event_timestamp}")
    print(f"Last timestamp = {events[len(events) - 1].event_timestamp}")

    if print_detail:
        print(f"input process guid = {guid}")
        print("event.event_guid,event.event_hash,event.process_guid,event.backend_timestamp,event.event_timestamp")
        print("=========--=============")
        for event in events:
            print(f"{event.event_guid}, {event.event_hash}, {event.process_guid}, \
                    {event.backend_timestamp}, {event.event_timestamp}")

    print("\nCompare results manually with Postman")
    print("----------------------------------------------------------")


def get_process_facet(cb, window):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search
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
        pass

    results = future.result()
    pprint(results._info, sort_dicts=False)

    print("\nCompare results manually with postman")
    print("----------------------------------------------------------")


def get_event_facet():
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search
    """
    print("Start: get_event_facet")
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

    print("----------------------------------------------------------")


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
    pprint(events[0].get_details())

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
    parser = build_cli_parser()
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
        get_process_details_for_single_process(cb, process_guid)
        get_process_events_for_single_process(cb, print_detail, process_guid)
        run_process_invalid_search(cb, print_detail)
        run_process_event_invalid_search(cb, print_detail)
        get_process_facet(cb, window)
        get_list_of_available_process_results(cb)
        get_events_facet_associated_with_a_process(cb, process_guid)
    if do_enriched_events:
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
