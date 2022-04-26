#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
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
* Get Events Facet Associated with a Process (v2)

The following calls will be added when the API on CBC is complete
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
import requests
import sys
import time
from datetime import datetime, timedelta
from pprint import pprint

# Internal library imports
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Process, Event, ProcessFacet, EventFacet
from cbc_sdk.errors import ApiError

HOSTNAME = ''
ORG_KEY = ''
HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}

START_PROCESS_SEARCH = '{}api/investigate/v2/orgs/{}/processes/search_jobs'
CHECK_SEARCH_PROGRESS = '{}api/investigate/v1/orgs/{}/processes/search_jobs/{}'
GET_SEARCH_RESULTS = '{}api/investigate/v2/orgs/{}/processes/search_jobs/{}/results?rows=10000'

START_DETAILS_SEARCH = '{}api/investigate/v2/orgs/{}/processes/detail_jobs'
CHECK_DETAILS_SEARCH_PROGRESS = '{}api/investigate/v2/orgs/{}/processes/detail_jobs/{}'
GET_DETAILS_RESULTS = '{}api/investigate/v2/orgs/{}/processes/detail_jobs/{}/results'

GET_PROCESS_EVENTS = '{}api/investigate/v2/orgs/{}/events/{}/_search'

PROCESS_SEARCH_VALIDATION = '{}api/investigate/v1/orgs/{}/processes/search_validation'
EVENT_SEARCH_VALIDATION = '{}api/investigate/v1/orgs/{}/events/search_validation'

START_PROCESS_FACET_SEARCH = '{}api/investigate/v2/orgs/{}/processes/facet_jobs'
GET_PROCESS_FACET_SEARCH_RESULTS = '{}api/investigate/v2/orgs/{}/processes/facet_jobs/{}/results'

GET_ALL_PROCESS_RESULTS_SETS = '{}api/investigate/v1/orgs/{}/processes/search_jobs'

EVENTS_FACET_FOR_A_PROCESS = '{}api/investigate/v2/orgs/{}/events/{}/_facet'


def run_process_invalid_search(cb, print_detail):
    """
    Tests that Process Search Validation is being called by putting an invalid field name in the where clause

    API Calls performed:
        Process Search Validation (v1)

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
    """
    invalid_process_search_url = PROCESS_SEARCH_VALIDATION.format(HOSTNAME, ORG_KEY) + '?q=enrichedBADFIELD:true'
    api_response = requests.get(invalid_process_search_url, headers=HEADERS)

    process_query = cb.select(Process).where("enrichedBADFIELD:true")

    try:
        [process for process in process_query]
        print("Test Failed - a process has been returned as a result of an invalid query")
    except ApiError as err:
        if api_response.json()['invalid_message'] in str(err) and api_response.status_code == 200:
            if print_detail:
                print("Expected validation error returned: {}".format(err))
            print('Process Search Validation...........................OK')
        else:
            print("Test Failed - Unexpected error returned: {}".format(err))


def run_process_event_invalid_search(cb, print_detail):
    """
    Tests that Event Search Validation is being called by putting an invalid field name in the where clause

    API Calls performed:
        Get Validation for Event Search (v1)

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
    """
    invalid_event_search_url = EVENT_SEARCH_VALIDATION.format(HOSTNAME, ORG_KEY) + '?q=enrichedBADFIELD:true'
    api_response = requests.get(invalid_event_search_url, headers=HEADERS)

    event_query = cb.select(Event).where("enrichedBADFIELD:true")

    try:
        [event for event in event_query]
        print("Test Failed - an event has been returned as a result of an invalid query")
    except ApiError as err:
        if api_response.json()['invalid_message'] in str(err) and api_response.status_code == 200:
            if print_detail:
                print("Expected validation error returned: {}".format(err))
            print('Event Search Validation.............................OK')
        else:
            print("Test Failed - Unexpected error returned: {}".format(err))


def get_list_of_available_process_results(cb):
    """
    Get a List of All Available Process Result Sets via API and SDK. Compare the results.

    API Calls performed:
        Get a List of All Available Process Result Sets (v1)

    Args:
        cb (CBCloudAPI): API object
    """
    get_all_process_results_sets_url = GET_ALL_PROCESS_RESULTS_SETS.format(HOSTNAME, ORG_KEY)
    api_response = requests.get(get_all_process_results_sets_url, headers=HEADERS).json()

    process_queries = cb.fetch_process_queries()

    assert set(process_queries) == set(api_response['query_ids']), \
        'Test Failed: SDK call returns different process results sets. ' \
        'Expected: {}, Actual: {}'.format(api_response['query_ids'], process_queries)
    print('Get a List of All Available Process Result Sets.....OK')


def get_events_facet_associated_with_a_process(cb, print_detail, start_date, end_date, process_guid):
    """
    Get events facet associated with a process via API and SDK. Compare the results.

    API Calls performed:
        Get Events Facet Associated with a Process (v2)

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        start_date: the start date for the query timeframe
        end_date: the end date for the query timeframe
        process_guid (string): process_guid
    """
    events_facet_for_a_process_url = EVENTS_FACET_FOR_A_PROCESS.format(HOSTNAME, ORG_KEY, process_guid)
    data = {
        "query": "*:*",
        "ranges": [
            {
                "bucket_size": "+1DAY",
                "end": f"{end_date}",
                "field": "backend_timestamp",
                "start": f"{start_date}"
            }
        ],
        "terms": {
            "fields": [
                "event_type"
            ],
            "rows": 10
        },
        "time_range": {
            "end": f"{end_date}",
            "start": f"{start_date}"
        }
    }
    api_response = requests.post(events_facet_for_a_process_url, json=data, headers=HEADERS).json()
    while api_response['processed_segments'] != api_response['total_segments']:
        time.sleep(.5)
        api_response = requests.post(events_facet_for_a_process_url, json=data, headers=HEADERS).json()

    assert api_response['num_found'] > 0, \
        'Test Failed: No events returned for process {}.'.format(process_guid)

    facet_query = cb.select(EventFacet).where(process_guid=process_guid)
    facet_query.add_range({"bucket_size": "+1DAY",
                           "start": f"{start_date}",
                           "end": f"{end_date}",
                           "field": "backend_timestamp"})
    facet_query.add_facet_field(["event_type"]).timeout(60000)
    facet_query.set_rows(10)
    facet_query.set_time_range(start=start_date, end=end_date)

    future = facet_query.execute_async()
    while not future.done():
        pass
    sdk_results = future.result()

    if print_detail:
        print('Process guid: {}'.format(process_guid))
        pprint(sdk_results._info, sort_dicts=False)

    assert sdk_results.ranges_.fields[0] == api_response['ranges'][0]['field'], \
        'Test Failed: SDK call returns a different ranges field for events facet search. '\
        'Expected: {}\nActual: {}'.format(api_response['ranges'][0]['field'], sdk_results.ranges_.fields[0])

    api_normalized_ranges = '{{\'{}\': {}}}'\
        .format(api_response['ranges'][0]['field'], api_response['ranges'][0]['values'])
    if print_detail:
        print('SDK Ranges Facets: {}'.format(sdk_results.ranges_.facets))
    assert str(sdk_results.ranges_.facets) == api_normalized_ranges, \
        'Test Failed: SDK call returns different ranges values for events facet search. '\
        'Expected: {}\nActual: {}'.format(api_normalized_ranges, sdk_results.ranges_.facets)

    for index in range(len(sdk_results.terms_.fields)):
        assert sdk_results.terms_.fields[index] == api_response['terms'][index]['field'], \
            'Test Failed: SDK call returns different terms fields for events facet search. '\
            'Expected: {}\nActual: {}'.format(api_response['terms'][index]['field'], sdk_results.terms_.fields[index])

    api_normalized_terms = {}
    for item in api_response.get('terms'):
        key = item.get('field')
        values = item.get('values')
        api_normalized_terms[key] = sorted(values, key=lambda i: (i.get('total'), i.get('id')), reverse=True)
    sorted_sdk = {}
    for key, value in sdk_results.terms_.facets.items():
        sorted_sdk[key] = sorted(value, key=lambda i: (i.get('total'), i.get('id')), reverse=True)
    if print_detail:
        print('SDK Terms Facets: {}'.format(sorted_sdk))
    assert sorted_sdk == api_normalized_terms, \
        'Test Failed: SDK call returns different terms values for event facet search. '\
        'Expected: {}\nActual: {}'.format(api_normalized_terms, sorted_sdk)

    print('Get Events Facet Associated with a Process..........OK')


def get_process_guid(cb, print_detail, start_date, end_date):
    """
    Compare the Process Search results retrieved by API and SDK calls. Get the GUID of the first retrieved process.

    API Calls performed:
        Start a Process Search (v2)
        Get the Status of a Process Search (v1)
        Retrieve Results for a Process Search (v2)

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        start_date (str): the start date for the query timeframe
        end_date (str): the end date for the query timeframe

    Returns:
        process_guid of the first process in the returned list
    """
    start_process_search_url = START_PROCESS_SEARCH.format(HOSTNAME, ORG_KEY)
    data = {
        "query": "enriched:true",
        "rows": 10000,
        "time_range": {
            "end": f"{end_date}",
            "start": f"{start_date}"
        }
    }
    job_id = requests.post(start_process_search_url, json=data, headers=HEADERS).json()['job_id']

    check_search_progress_url = CHECK_SEARCH_PROGRESS.format(HOSTNAME, ORG_KEY, job_id)
    search_progress = requests.get(check_search_progress_url, headers=HEADERS).json()
    while search_progress["contacted"] != search_progress["completed"]:
        time.sleep(.5)
        search_progress = requests.get(check_search_progress_url, headers=HEADERS).json()

    get_search_results_url = GET_SEARCH_RESULTS.format(HOSTNAME, ORG_KEY, job_id)
    api_response = requests.get(get_search_results_url, headers=HEADERS).json()

    process_query = cb.select(Process)\
        .where("enriched:true")\
        .set_rows(10000)\
        .set_time_range(start=start_date, end=end_date)
    matching_processes = [process for process in process_query]
    sdk_results = []
    for process in matching_processes:
        sdk_results.append(process._info)

    assert api_response['num_available'] == process_query._total_results, \
           'Test Failed: SDK call returns different number of available processes. ' \
           'Expected: {}\nActual: {}'.format(api_response['num_available'], process_query._total_results)

    sdk_results = sorted(sdk_results, key=lambda i: i['process_guid'], reverse=True)
    api_results = sorted(api_response['results'], key=lambda i: i['process_guid'], reverse=True)
    assert sdk_results == api_results, 'Test Failed: SDK returns different processes data. '\
        'Expected: {}\nActual: {}'.format(api_results, sdk_results)
    if print_detail:
        print('{} processes found for the period {} - {}'.format(len(matching_processes), start_date, end_date))
        print('Process GUID returned: {}'.format(matching_processes[0].process_guid))
    print('Process Search......................................OK')
    return matching_processes[0].process_guid


def remove_event_info(process_details):
    """Helper function to remove the event info from the process details"""
    TO_DELETE_FIELDS = ['document_guid', 'enriched', 'enriched_event_type',
                        'event_type', 'backend_timestamp', 'device_timestamp',
                        'ingress_time', 'netconn_count', 'event_threat_score',
                        'regmod_count', 'filemod_count']
    for key in process_details.copy():
        if key in TO_DELETE_FIELDS:
            process_details.pop(key)
    return process_details


def retrieve_process_name_from_process_details(cb, guid):
    """
    Get the process details for a single process via API and SDK. Compare the responses. Retrieve the process name.

    API Calls performed:
        Request Details of Processes (v2)
        Get the Status of a Process Detail Search (v2)
        Retrieve Results for a Process Detail Search (v2)

    Args:
        cb (CBCloudAPI): API object
        guid (str): GUID of process to have details retrieved

    Returns:
        process_name of the process
    """
    start_details_search_url = START_DETAILS_SEARCH.format(HOSTNAME, ORG_KEY)
    data = {
        "process_guids": [
            f"{guid}"
        ]
    }
    job_id = requests.post(start_details_search_url, json=data, headers=HEADERS).json()['job_id']

    check_search_progress_url = CHECK_DETAILS_SEARCH_PROGRESS.format(HOSTNAME, ORG_KEY, job_id)
    search_progress = requests.get(check_search_progress_url, headers=HEADERS).json()
    while search_progress['contacted'] != search_progress['completed']:
        time.sleep(.5)
        search_progress = requests.get(check_search_progress_url, headers=HEADERS).json()

    get_results_url = GET_DETAILS_RESULTS.format(HOSTNAME, ORG_KEY, job_id)
    api_response = requests.get(get_results_url, headers=HEADERS).json()
    api_response_normalized = list(map(remove_event_info, api_response['results']))

    process_details = cb.select(Process, guid)
    sdk_result_normalized = list(map(remove_event_info, [process_details.get_details()]))

    assert sdk_result_normalized == api_response_normalized, \
        'Test Failed: SDK call returns different process details. '\
        'Expected: {}\nActual: {}'.format(api_response_normalized, sdk_result_normalized)

    process_name_normalized = (str(process_details.process_name).rpartition('/'))[2]
    process_name_normalized = (str(process_name_normalized).rpartition('\\'))[2]
    print('Get Process Details.................................OK')
    return process_name_normalized


def get_process_events_for_single_process(cb, guid, start_date, end_date, print_detail):
    """
    Get the events associated with a given process via API and SDK. Compare the responses.

    API Calls performed:
        Get Events Associated with a Given Process (v2)

    Args:
        cb (CBCloudAPI): API object
        guid (str): All events retrieved for this process guid
        start_date (str): the start date for the query timeframe
        end_date (str): the end date for the query timeframe
        print_detail (bool): whether to print full info to the console, useful for debugging
    """
    get_process_events_url = GET_PROCESS_EVENTS.format(HOSTNAME, ORG_KEY, guid)
    data = {
        "fields": ["*"],
        "query": "*:*",
        "rows": 10000,
        "sort": [
            {
                "field": "backend_timestamp",
                "order": "asc"
            }
        ],
        "time_range": {
            "end": f"{end_date}",
            "start": f"{start_date}"
        }
    }
    api_response = requests.post(get_process_events_url, json=data, headers=HEADERS).json()
    while api_response['processed_segments'] != api_response['total_segments']:
        time.sleep(.5)
        api_response = requests.post(get_process_events_url, json=data, headers=HEADERS).json()

    events_query = cb.select(Event).where(process_guid=guid)\
                                   .sort_by("backend_timestamp", "asc")\
                                   .set_rows(10000)\
                                   .set_time_range(start=start_date, end=end_date)

    sdk_results = []
    for event in events_query:
        sdk_results.append(event._info)

    assert api_response['num_available'] == events_query._total_results, \
           'Test Failed: SDK call returns different number of associated events. ' \
           'Expected: {}\nActual: {}'.format(api_response['num_available'], events_query._total_results)

    assert sdk_results == api_response['results'], \
        'Test Failed: SDK call returns different data for associated events. '\
        'Expected: {},\nActual: {}'.format(api_response['results'], sdk_results)

    if print_detail:
        pretty_response = {"num_available": events_query._total_results,
                           "total_segments": events_query._total_segments,
                           "processed_segments": events_query._processed_segments}
        print("Events information:")
        pprint(pretty_response, sort_dicts=False)
    print('Get Events associated with a Process................OK')


def get_process_facet(cb, print_detail, process_name, start_date, end_date):
    """
    Perform Facet Search on Processes via API and SDK. Compare the results.

    API Calls performed:
        Start a Facet Search on Processes (v2)
        Retrieve Results for a Process Facets Search (v2)

    Args:
        cb (CBCloudAPI): API object
        print_detail (bool): whether to print full info to the console, useful for debugging
        process_name (str): the process name to be used in the queries
        start_date: the start date for the query timeframe
        end_date: the end date for the query timeframe
    """
    start_process_facet_search_url = START_PROCESS_FACET_SEARCH.format(HOSTNAME, ORG_KEY)
    data = {
        "query": f"process_name:{process_name}",
        "ranges": [
            {
                "bucket_size": "+1DAY",
                "end": f"{end_date}",
                "field": "backend_timestamp",
                "start": f"{start_date}"
            }
        ],
        "terms": {
            "fields": [
                "alert_category",
                "device_external_ip",
                "backend_timestamp"
            ],
            "rows": 5
        },
        "time_range": {
            "end": f"{end_date}",
            "start": f"{start_date}"
        }
    }
    job_id = requests.post(start_process_facet_search_url, json=data, headers=HEADERS).json()['job_id']

    get_process_facet_search_results_url = GET_PROCESS_FACET_SEARCH_RESULTS.format(HOSTNAME, ORG_KEY, job_id)
    api_response = requests.get(get_process_facet_search_results_url, headers=HEADERS).json()
    while api_response['contacted'] != api_response['completed']:
        time.sleep(.5)
        api_response = requests.get(get_process_facet_search_results_url, headers=HEADERS).json()

    assert api_response['num_found'] > 0, \
        'Test Failed: No facets returned for {} processes.'.format(process_name)

    facet_query = cb.select(ProcessFacet).where(f"process_name:{process_name}")
    facet_query.add_range({"bucket_size": "+1DAY",
                           "start": f"{start_date}",
                           "end": f"{end_date}",
                           "field": "backend_timestamp"})
    facet_query.add_facet_field(["alert_category", "device_external_ip", "backend_timestamp"]).timeout(60000)
    facet_query.set_time_range(start=start_date, end=end_date)
    facet_query.set_rows(5)

    future = facet_query.execute_async()
    while not future.done():
        pass
    sdk_results = future.result()

    if print_detail:
        print('Processes filtered by process_name {}'.format(process_name))
        pprint(sdk_results._info, sort_dicts=False)

    assert sdk_results.ranges_.fields[0] == api_response['ranges'][0]['field'], \
        'Test Failed: SDK call returns a different ranges field for process facet search. '\
        'Expected: {}\nActual: {}'.format(api_response['ranges'][0]['field'], sdk_results.ranges_.fields[0])
    api_normalized_ranges = '{{\'{}\': {}}}'\
        .format(api_response['ranges'][0]['field'], api_response['ranges'][0]['values'])
    if print_detail:
        print('SDK Ranges Facets: {}'.format(sdk_results.ranges_.facets))
    assert str(sdk_results.ranges_.facets) == api_normalized_ranges, \
        'Test Failed: SDK call returns different ranges values for process facet search. '\
        'Expected: {}\nActual: {}'.format(api_normalized_ranges, sdk_results.ranges_.facets)

    for index in range(len(sdk_results.terms_.fields)):
        assert sdk_results.terms_.fields[index] == api_response['terms'][index]['field'], \
            'Test Failed: SDK call returns different terms fields for process facet search. '\
            'Expected: {}\nActual: {}'.format(api_response['terms'][index]['field'], sdk_results.terms_.fields[index])

    api_normalized_terms = {}
    for item in api_response.get('terms'):
        key = item.get('field')
        values = item.get('values')
        api_normalized_terms[key] = sorted(values, key=lambda i: (i.get('total'), i.get('id')), reverse=True)
    sorted_sdk = {}
    for key, value in sdk_results.terms_.facets.items():
        sorted_sdk[key] = sorted(value, key=lambda i: (i.get('total'), i.get('id')), reverse=True)
    if print_detail:
        print('SDK Terms Facets: {}'.format(sorted_sdk))
    assert sorted_sdk == api_normalized_terms, \
        'Test Failed: SDK call returns different terms values for process facet search. '\
        'Expected: {}\nActual: {}'.format(api_normalized_terms, sorted_sdk)
    print('Facet Search on Processes...........................OK')


def main():
    """Script entry point"""
    parser = build_cli_parser()
    parser.add_argument("--window", help="Define search window", default='3d')

    args = parser.parse_args()
    global ORG_KEY
    global HOSTNAME

    print_detail = False

    cb = get_cb_cloud_object(args)

    HEADERS['X-Auth-Token'] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    start_date = (datetime.now() + timedelta(days=-2)).isoformat() + "Z"
    end_date = (datetime.now() + timedelta(days=-1)).isoformat() + "Z"
    if print_detail:
        print("Start date: {}\nEnd date: {}".format(start_date, end_date))

    run_process_invalid_search(cb, print_detail)
    run_process_event_invalid_search(cb, print_detail)
    get_list_of_available_process_results(cb)
    process_guid = get_process_guid(cb, print_detail, start_date, end_date)
    process_name = retrieve_process_name_from_process_details(cb, process_guid)
    get_process_facet(cb, print_detail, process_name, start_date, end_date)
    get_process_events_for_single_process(cb, process_guid, start_date, end_date, print_detail)
    get_events_facet_associated_with_a_process(cb, print_detail, start_date, end_date, process_guid)
    print('END OF TEST')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
