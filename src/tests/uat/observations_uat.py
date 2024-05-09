#!/usr/bin/env python3
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
To execute, a profile must be provided using the standard CBC Credentials.

Observations:
https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/observations-api/
"""

import sys
import time
import requests
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Observation, NetworkThreatMetadata, ObservationFacet

# ------------------------------ APIs ----------------------------------------------

# search job + grouped results
START_SEARCH_JOB = "{}api/investigate/v2/orgs/{}/observations/search_jobs"
GET_SEARCH_RESULTS = "{}api/investigate/v2/orgs/{}/observations/search_jobs/{}/results"
GET_GROUPED_RESULTS = "{}api/investigate/v2/orgs/{}/observations/search_jobs/{}/group_results"

# detail job
START_DETAILS_JOB = "{}api/investigate/v2/orgs/{}/observations/detail_jobs"
GET_DETAILS_RESULTS = "{}api/investigate/v2/orgs/{}/observations/detail_jobs/{}/results"

# facet job
START_FACET_JOB = "{}api/investigate/v2/orgs/{}/observations/facet_jobs"
GET_FACET_RESULTS = "{}api/investigate/v2/orgs/{}/observations/facet_jobs/{}/results"

# others
SEARCH_SUGGESTIONS = "{}api/investigate/v2/orgs/{}/observations/search_suggestions?suggest.q={}"
GET_NETWORK_THREAT_METADATA = "{}threatmetadata/v1/orgs/{}/detectors/{}"

# ------------------------------ Formatters ------------------------------------------

HEADERS = {"X-Auth-Token": "", "Content-Type": "application/json"}
ORG_KEY = ""
HOSTNAME = ""
DELIMITER = "-"
SYMBOLS = 70
OBSERVATION_ID = 0
SECTION_TITLES = ["Observations", "Network Threat Metadata"]
TITLES = [
    "Get Search Suggestions",
    "Get Search Results",
    "Get Search Grouped Results",
    "Get Details Results",
    "Get Facet Data",
    "Get Network Threat Metadata",
]

# ------------------------------ Helper functions -------------------------------------


def get_search_results():
    """Get search results - both groupped and not grouped"""
    global OBSERVATION_ID
    sdata = {"query": "rule_id:* AND observation_type:TAU_INTELLIGENCE"}
    gdata = {"fields": ["device_name"], "range": {}, "rows": 50}
    job_id = requests.post(START_SEARCH_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=sdata).json()["job_id"]
    time.sleep(0.5)
    results = requests.get(GET_SEARCH_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS).json()
    OBSERVATION_ID = results["results"][0]["observation_id"]
    gresults = requests.post(
        GET_GROUPED_RESULTS.format(HOSTNAME, ORG_KEY, job_id),
        headers=HEADERS,
        json=gdata,
    ).json()
    return results["results"], gresults["group_results"]


def get_details_results(observation_id):
    """Get details results"""
    ddata = {"observation_ids": [observation_id]}
    job_id = requests.post(START_DETAILS_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=ddata).json()["job_id"]
    time.sleep(0.5)
    results = requests.get(GET_DETAILS_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS)
    return results.json()["results"][0]


def get_facet_results():
    """Get facet results"""
    fdata = {
        "query": "rule_id:* AND observation_type:TAU_INTELLIGENCE",
        "terms": {"fields": ["device_name"]},
    }
    job_id = requests.post(START_FACET_JOB.format(HOSTNAME, ORG_KEY), headers=HEADERS, json=fdata).json()["job_id"]
    time.sleep(0.5)
    results = requests.get(GET_FACET_RESULTS.format(HOSTNAME, ORG_KEY, job_id), headers=HEADERS)
    return results.json()


def get_seach_suggestions(q="device_id&suggest.count=1"):
    """Get search suggestions"""
    results = requests.get(SEARCH_SUGGESTIONS.format(HOSTNAME, ORG_KEY, q), headers=HEADERS)
    return results.json()["suggestions"]


def get_network_threat_metadata(rule_id):
    """Get network threat metadata"""
    results = requests.get(GET_NETWORK_THREAT_METADATA.format(HOSTNAME, ORG_KEY, rule_id), headers=HEADERS).json()
    results["tms_rule_id"] = rule_id
    return results


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

    api_result = get_seach_suggestions()
    sdk_result = Observation.search_suggestions(cb, query="device_id", count=1)
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[0] + "." * (SYMBOLS - len(TITLES[0]) - 2) + "OK")

    # check get search job
    sapi_result, gapi_result = get_search_results()
    sdk_r = cb.select(Observation).where("rule_id:* AND observation_type:TAU_INTELLIGENCE")
    ssdk_result = [x._info for x in sdk_r]
    assert sapi_result == ssdk_result, f"Test Failed Expected: {sapi_result} Actual: {ssdk_result}"
    print(TITLES[1] + "." * (SYMBOLS - len(TITLES[1]) - 2) + "OK")

    # check get group results
    sdk_result = [y._info for x in sdk_r.get_group_results("device_name") for y in x.observations]
    api_result = []
    for group in gapi_result:
        api_result.extend(group["results"])
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[2] + "." * (SYMBOLS - len(TITLES[2]) - 2) + "OK")

    # check get details job
    obs_id = sapi_result[0]["observation_id"]
    rule_id = sapi_result[0]["rule_id"]
    api_result = get_details_results(obs_id)
    sdk_result = cb.select(Observation, obs_id).get_details()._info
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[3] + "." * (SYMBOLS - len(TITLES[3]) - 2) + "OK")

    # check get facet job
    api_result = get_facet_results()["terms"]
    xx = (
        cb.select(ObservationFacet)
        .where("rule_id:* AND observation_type:TAU_INTELLIGENCE")
        .add_facet_field("device_name")
        .results
    )
    sdk_result = xx.terms
    assert api_result == sdk_result, f"Test Failed Expected: {api_result} Actual: {sdk_result}"
    print(TITLES[4] + "." * (SYMBOLS - len(TITLES[4]) - 2) + "OK")

    print()
    print(f"{SECTION_TITLES[1]:^70}")
    print(SYMBOLS * DELIMITER)
    api_result = get_network_threat_metadata(rule_id)
    osdk_result = cb.select(Observation, obs_id).get_network_threat_metadata()._info
    ntmsdk_result = cb.select(NetworkThreatMetadata, rule_id)._info
    assert (
        api_result == osdk_result == ntmsdk_result
    ), f"Test Failed Expected: {api_result} Actual: {osdk_result} other, {ntmsdk_result}"
    print(TITLES[5] + "." * (SYMBOLS - len(TITLES[5]) - 2) + "OK")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
