#!/usr/bin/env python3
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

"""
To execute, a profile must be provided using the standard CBC Credentials.

Auth Events:
https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/auth-events-api
"""

import sys
import time
import requests

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.enterprise_edr import AuthEvent, AuthEventFacet

# ------------------------------ APIs ----------------------------------------------

# search job + grouped results
START_SEARCH_JOB = "{}api/investigate/v2/orgs/{}/auth_events/search_jobs"
# by default only 10 are returned
GET_SEARCH_RESULTS = "{}api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/results?start=0&rows=500"
GET_GROUPED_RESULTS = "{}api/investigate/v2/orgs/{}/auth_events/search_jobs/{}/group_results"
QUERY = "auth_username:Administrator"

# detail job
START_DETAILS_JOB = "{}api/investigate/v2/orgs/{}/auth_events/detail_jobs"
GET_DETAILS_RESULTS = "{}api/investigate/v2/orgs/{}/auth_events/detail_jobs/{}/results"

# facet job
START_FACET_JOB = "{}api/investigate/v2/orgs/{}/auth_events/facet_jobs"
GET_FACET_RESULTS = "{}api/investigate/v2/orgs/{}/auth_events/facet_jobs/{}/results"

# others
SEARCH_SUGGESTIONS = "{}api/investigate/v2/orgs/{}/auth_events/search_suggestions?suggest.q={}"
GET_DESCRIPTIONS = "{}api/investigate/v2/orgs/{}/auth_events/descriptions"

# ------------------------------ Formatters ------------------------------------------

HEADERS = {"X-Auth-Token": "", "Content-Type": "application/json"}
ORG_KEY = ""
HOSTNAME = ""
DELIMITER = "-"
SYMBOLS = 70
AUTH_EVENT_ID = 0
SECTION_TITLES = ["Auth Events"]
TITLES = [
    "Get Search Suggestions",
    "Get Auth Events Description",
    "Get Search Results",
    "Get Search Grouped Results",
    "Get Details Results",
    "Get Facet Data"
]

# ------------------------------ Helper functions -------------------------------------


def get_search_results():
    """Get search results - both groupped and not grouped"""
    global AUTH_EVENT_ID
    sdata = {"query": QUERY, "time_range": {"window": "-1d"}}
    gdata = {"fields": ["*"], "range": {}, "rows": 50}
    job_id = requests.post(START_SEARCH_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=sdata).json()["job_id"]
    time.sleep(2)
    results = requests.get(GET_SEARCH_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS).json()
    AUTH_EVENT_ID = results["results"][0]["event_id"]
    gresults = requests.post(
        GET_GROUPED_RESULTS.format(HOSTNAME, ORG_KEY, job_id),
        headers=HEADERS,
        json=gdata,
    ).json()
    return results["results"], gresults["group_results"]


def get_details_results(event_id):
    """Get details results"""
    ddata = {"event_ids": [event_id]}
    job_id = requests.post(START_DETAILS_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=ddata).json()["job_id"]
    time.sleep(0.5)
    results = requests.get(GET_DETAILS_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS)
    return results.json()["results"][0]


def get_facet_results():
    """Get facet results"""
    fdata = {
        "query": QUERY,
        "terms": {"fields": ["device_name"]},
    }
    job_id = requests.post(START_FACET_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=fdata).json()["job_id"]
    time.sleep(0.5)
    results = requests.get(GET_FACET_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS)
    return results.json()


def get_search_suggestions(q="auth"):
    """Get search suggestions"""
    results = requests.get(SEARCH_SUGGESTIONS.format(HOSTNAME, ORG_KEY, q), headers=HEADERS)
    return results.json()["suggestions"]


def get_descriptions():
    """Get descriptions"""
    results = requests.get(GET_DESCRIPTIONS.format(HOSTNAME, ORG_KEY), headers=HEADERS)
    return results.json()


# ------------------------------ Main -------------------------------------------------


def main():
    """Script entry point"""
    global ORG_KEY
    global HOSTNAME
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb = get_cb_cloud_object(args)
    HEADERS["X-Auth-Token"] = cb.credentials.token
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url

    print()
    print(f"{SECTION_TITLES[0]:^70}")
    print(SYMBOLS * DELIMITER)

    api_result = get_search_suggestions()
    sdk_result = AuthEvent.search_suggestions(cb, query="auth")
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[0] + "." * (SYMBOLS - len(TITLES[0]) - 2) + "OK")

    api_result = get_descriptions()
    sdk_result = AuthEvent.get_auth_events_descriptions(cb)
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[1] + "." * (SYMBOLS - len(TITLES[1]) - 2) + "OK")

    # check get search job
    sapi_result, gapi_result = get_search_results()
    sdk_r = cb.select(AuthEvent).where(QUERY).set_time_range(window="-1d")
    ssdk_result = [x._info for x in sdk_r]
    assert sapi_result == ssdk_result, f"Test Failed Expected: {sapi_result} Actual: {ssdk_result}"
    print(TITLES[2] + "." * (SYMBOLS - len(TITLES[2]) - 2) + "OK")

    # check get group results
    sdk_result = [y._info for x in sdk_r.group_results("device_name") for y in x.auth_events]
    api_result = []
    for group in gapi_result:
        api_result.extend(group["results"])
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[3] + "." * (SYMBOLS - len(TITLES[3]) - 2) + "OK")
    auth_event = sdk_r[0]
    # check get details job
    api_result = get_details_results(auth_event.event_id)
    sdk_result = auth_event.get_details()._info
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[4] + "." * (SYMBOLS - len(TITLES[4]) - 2) + "OK")

    # check get facet job
    api_result = get_facet_results()["terms"]
    xx = (
        cb.select(AuthEventFacet)
        .where(QUERY)
        .add_facet_field("device_name")
        .results
    )
    sdk_result = xx.terms
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[5] + "." * (SYMBOLS - len(TITLES[5]) - 2) + "OK")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
