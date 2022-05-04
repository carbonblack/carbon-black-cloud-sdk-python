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
The following API calls are tested in this script:
"""

import sys
import requests
import random
import json
from cbc_sdk.errors import ApiError, ServerError
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import BaseAlert, CBAnalyticsAlert, WatchlistAlert, DeviceControlAlert, ContainerRuntimeAlert

HEADERS = {'X-Auth-Token': '', 'Content-Type': 'application/json'}
ORG_KEY = ''
HOSTNAME = ''


def invoke_get(url):
    """
    Do a manual GET on the server.

    Args:
        url (str): The URL template to be used for the API call.

    Returns:
        dict: The JSON response to the GET.

    Raises:
        ServerError: If an error response was returned.
    """
    real_url = url.format(HOSTNAME, ORG_KEY)
    response = requests.get(real_url, headers=HEADERS)
    if response.status_code >= 400:
        raise ServerError(response.status_code, response.text)
    return response.json()


def invoke_post(url, body=None):
    """
    Do a manual POST on the server.

    Args:
        url (str): The URL template to be used for the API call.
        body (dict): The JSON body to be sent. Default is None (send an empty JSON body).

    Returns:
        dict: The JSON response to the POST.

    Raises:
        ServerError: If an error response was returned.
    """
    real_url = url.format(HOSTNAME, ORG_KEY)
    real_body = body if body else {}
    response = requests.post(real_url, json=real_body, headers=HEADERS)
    if response.status_code >= 400:
        raise ServerError(response.status_code, response.text)
    return response.json()


def compare_search_results(funcname, alerts, results):
    """
    Compares two search results to see if they're identical.

    Args:
        funcname (str):  Name of the function the comparison is being called from, for error messages.
        alerts (list[BaseAlert]): Output from the SDK function.
        results (list[dict]): Output from the raw HTTP response.

    Returns:
        bool: True if the two results are identical, False if not.
    """
    ok = True
    if len(alerts) != len(results):
        print(f"{funcname}: different lengths of results: {len(alerts)} vs. {len(results)}")
        ok = False
    list_count = min(len(alerts), len(results))
    for index, alert, result in zip(range(list_count), alerts, results):
        if alert._info != result:
            print(f"{funcname}: alert at index {index} differs")
            print(f"    alert = {json.dumps(alert._info, indent=2)}")
            print(f"    result = {json.dumps(result, indent=2)}")
            ok = False
    return ok


def select_arbitrary_alert(query):
    """
    Given a defined query, select an arbitrary alert from the query.

    Args:
        query (BaseAlertSearchQuery): Query that's been configured by the caller.

    Returns:
        BaseAlert: An arbitrary alert from the query results.  If there were no query results, returns None.
    """
    alerts = list(query)
    if alerts:
        return random.choice(alerts)
    return None


def test_search_normal(cb):
    """
    Tests search on BaseAlerts.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(BaseAlert).set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': '', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/_search', body)
        results = output['results']
        if compare_search_results('test_search_normal', alerts, results):
            print("test_search_normal: OK")
    except ApiError as e:
        print(f"test_search_normal: error in test: {e}")


def test_search_normal_with_query(cb):
    """
    Tests search on BaseAlerts with a query string.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(BaseAlert).where('run_state:RAN').set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': 'run_state:RAN', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/_search', body)
        results = output['results']
        if compare_search_results('test_search_normal_with_query', alerts, results):
            print("test_search_normal_with_query: OK")
    except ApiError as e:
        print(f"test_search_normal_with_query: error in test: {e}")


def test_search_analytics(cb):
    """
    Tests search on CBAnalyticsAlerts.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(CBAnalyticsAlert).set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': '', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/cbanalytics/_search', body)
        results = output['results']
        if compare_search_results('test_search_analytics', alerts, results):
            print("test_search_analytics: OK")
    except ApiError as e:
        print(f"test_search_analytics: error in test: {e}")


def test_search_watchlist(cb):
    """
    Tests search on WatchlistAlerts.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(WatchlistAlert).set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': '', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/watchlist/_search', body)
        results = output['results']
        if compare_search_results('test_search_watchlist', alerts, results):
            print("test_search_watchlist: OK")
    except ApiError as e:
        print(f"test_search_watchlist: error in test: {e}")


def test_search_device_control(cb):
    """
    Tests search on DeviceControlAlerts.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(DeviceControlAlert).set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': '', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/devicecontrol/_search', body)
        results = output['results']
        if compare_search_results('test_search_device_control', alerts, results):
            print("test_search_device_control: OK")
    except ApiError as e:
        print(f"test_search_device_control: error in test: {e}")


def test_search_container_runtime(cb):
    """
    Tests search on ContainerRuntimeAlerts.

    Args:
        cb (CBCloudAPI): API object to use.
    """
    try:
        query = cb.select(ContainerRuntimeAlert).set_create_time(range='-3d').sort_by('create_time')
        alerts = list(query)
        body = {'criteria': {'create_time': {'range': '-3d'}}, 'query': '', 'rows': 1000,
                'sort': [{'field': 'create_time', 'order': 'ASC'}]}
        output = invoke_post('{}/appservices/v6/orgs/{}/alerts/containerruntime/_search', body)
        results = output['results']
        if compare_search_results('test_search_container_runtime', alerts, results):
            print("test_search_container_runtime: OK")
    except ApiError as e:
        print(f"test_search_container_runtime: error in test: {e}")


def test_get_alert_by_id(cb):
    try:
        query = cb.select(BaseAlert).set_create_time(range='-3d')
        alert_to_use = select_arbitrary_alert(query)
        if alert_to_use:
            id_to_use = alert_to_use.id
            alert = cb.select(BaseAlert, id_to_use)
            output = invoke_get('{}/appservices/v6/orgs/{}/alerts/' + id_to_use)
            if alert._info != output:
                print(f"test_get_alert_by_id: alert with ID {id_to_use} differs")
                print(f"    alert = {json.dumps(alert._info, indent=2)}")
                print(f"    output = {json.dumps(output, indent=2)}")
            else:
                print("test_get_alert_by_id: OK")
        else:
            print("test_get_alert_by_id: unable to run test, no alerts matching query")
    except ApiError as e:
        print(f"test_get_alert_by_id: error in test: {e}")


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb = get_cb_cloud_object(args)
    global ORG_KEY, HOSTNAME, HEADERS
    ORG_KEY = cb.credentials.org_key
    HOSTNAME = cb.credentials.url
    HEADERS['X-Auth-Token'] = cb.credentials.token

    test_search_normal(cb)
    test_search_normal_with_query(cb)
    test_search_analytics(cb)
    test_search_watchlist(cb)
    test_search_device_control(cb)
    test_search_container_runtime(cb)
    test_get_alert_by_id(cb)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
