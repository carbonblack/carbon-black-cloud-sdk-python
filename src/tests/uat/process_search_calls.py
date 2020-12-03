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
Command-line example that retrieves all processes within the last six hours from all active devices.
Uses asynchronous querying to generate the queries for each device's processes so that they run in parallel.
"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object, CBCloudAPI
from cbc_sdk.enterprise_edr import Process, Event, ProcessFacet
from cbc_sdk.errors import ApiError


def print_test_coverage():
    print("Following API calls are not tested in UAT set:")
    print("  * Process Search Suggestions (v1) - Primarily for UI, not included in SDK")
    print("\n")
    print("Following API calls are covered in UAT:")
    print("  * Process Search Validation (v1) ")


def process_invalid_search(cb, print_detail=False):
    '''
    Tests that Process Search Validation is being called by putting an invalid field name in the where clause

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging

    Returns:
    '''
    print(f"Executing process_invalid_search")
    process_query = cb.select(Process).where("enrichedBADFIELD:true")
    try:
        matching_processes = [process for process in
                              process_query._perform_query(process_query._perform_query(numrows=10))]
    except ApiError as e:
        print("Expected result: APIError generated")
        if(print_detail):
            print(e)
    print(f"End: process_invalid_search")

def get_list_of_process_results(cb, print_details=False):
    '''
    Executes Get a List of All Available Process Result Sets
    Compare to results of this route, no body, no parameters.
    {{base_url}}/api/investigate/v1/orgs/{{org_key}}/processes/search_jobs

    Args:
        cb:
        print_details:

    Returns:

    '''
    process_queries = cb.fetch_process_queries()
    print(f"there were {len(process_queries)} process queries found")
    print("called fetch_process_queries")



def process_basic_window_enriched(cb, print_detail=False,window="-3d"):
    '''
    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
        process_guid of the first process in the returned list
    '''
    print(f"Executing process_basic_window_enriched")
    process_query = cb.select(Process).where("enriched:true")
    process_query.set_time_range(window=window)
    matching_processes = [process for process in process_query._perform_query(numrows=10000)]
    print(f"There are {len(matching_processes)} found in {window} of processes")
    if print_detail:
        for process in matching_processes:
            print("{0:16} {1:5} {2:20}".format(process.device_name, process.process_pids[0], process.process_guid))

    print(f"End: process_basic_window_enriched")
    # return the first process id for use in future tests
    return matching_processes[10].process_guid


def process_events_for_single_process(cb, print_detail, guid):
    '''

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        guid: All events retrieved for this process guid

    Returns:

    '''
    events_query = cb.select(Event).where(process_guid=guid)
    events_query.sort_by("backend_timestamp", direction="ASC")
    events = [ev for ev in events_query._perform_query(numrows=10000)]
    print(f"\n events_query has {len(events_query)} in events_query._total_results")
    print(f"events_query._total_segments = {events_query._total_segments} and vents_query._processed_segments = {events_query._processed_segments}")
    print(
        f"There are {len(events)} to print. First timestamp = {events[0].event_timestamp}.  Last timestamp = {events[len(events) - 1].event_timestamp}")
    if print_detail:
        print(f"input process guid = {guid}")
        print("event.event_guid,event.event_hash,event.process_guid,event.backend_timestamp,event.event_timestamp")
        print("=========--=============")
        for event in events:
            print(
                f"{event.event_guid},{event.event_hash},{event.process_guid},{event.backend_timestamp},{event.event_timestamp}")

    print(f"Function End")

def process_facet(cb, print_details=False,window="-3d"):
    """
    Exercises Process Facet search; start and get results.

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        window (str): period to search

    Returns:
    """
    print(f"process_facet Start")
    facet_query = cb.select(ProcessFacet).where("process_name:svchost.exe")
    facet_query.add_range({"bucket_size": "+1DAY",
               "start": "2020-11-01T00:00:00Z",
               "end": "2020-11-30T00:00:00Z",
               "field": "backend_timestamp"})
    facet_query.add_facet_field(["alert_category","device_external_ip","backend_timestamp"]).timeout(60000)
    facet_query.set_time_range(window=window)
    # TODO - figure out how to call facets and get results
    #  facets = facet_query._perform_query()

    print(f"INCOMPLETE process_facet End")

def main():
    parser = build_cli_parser()  # args on command line will be applied to all tests called
    args = parser.parse_args()
    print_detail = args.verbose
    window = "-3d"
    cb = get_cb_cloud_object(args)
    if print_detail:
        print(f"profile being used is {args.__dict__}")
    process_invalid_search(cb,print_detail)
    get_list_of_process_results(cb,print_detail)
    # TO DO test not complete.  process_facet(cb,print_detail,window)
    process_guid = process_basic_window_enriched(cb, print_detail,window)
    print(f"process guid being used is {process_guid}")
    process_events_for_single_process(cb, print_detail, process_guid)


if __name__ == "__main__":
    sys.exit(main())
