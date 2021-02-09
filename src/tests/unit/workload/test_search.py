#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for ComputeResource"""

import pytest
import logging
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from cbc_sdk.workload import ComputeResource
from tests.unit.fixtures.workload.mock_search import (FETCH_COMPUTE_RESOURCE_BY_ID_RESP,
                                                      SEARCH_AND_FACET_COMPUTE_RESEOURCES)


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


# ==================================== UNIT TESTS BELOW ====================================
def test_compute_resource_by_id(cbcsdk_mock):
    """Tests a simple compute resource querry"""
    cbcsdk_mock.mock_request("GET", "/lcm/view/v1/orgs/test/compute_resources/1539610",
                             FETCH_COMPUTE_RESOURCE_BY_ID_RESP)
    api = cbcsdk_mock.api
    resource = ComputeResource(api, "15396109")
    assert resource._model_unique_id == "15396109"


def test_search_facet_async(cbcsdk_mock):
    """Tests running the async_querry."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['uuid'] == ['502277cc-0aa9-80b0-9ac8-6f540c11edaf']

        return SEARCH_AND_FACET_COMPUTE_RESEOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v1/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(ComputeResource).set_uuid(['502277cc-0aa9-80b0-9ac8-6f540c11edaf'])

    assert query._count() == 1
    results = [result for result in query._run_async_query(None)]
    assert len(results) == 1
    facet = results[0]
    assert facet.uuid == '502277cc-0aa9-80b0-9ac8-6f540c11edaf'


def test_search_facet_with_all_bells_and_whistles(cbcsdk_mock):
    """Tests running the query with all values set."""
    def post_validate(url, body, **kwargs):
        crits = body['criteria']
        assert crits['appliance_uuid'] == ['c89f183b-f201-4bca-bacc-80184b5b8823']
        assert crits['eligibility'] == ['NOT_ELIGIBLE']
        assert crits['cluster_name'] == ['launcher-cluster']
        assert crits['name'] == ['vsvv-2k8r2']
        assert crits['ip_address'] == ['192.168.1.1']
        assert crits['installation_status'] == ['NOT_INSTALLED']
        assert crits['uuid'] == ['502277cc-0aa9-80b0-9ac8-6f540c11edaf']
        assert crits['os_type'] == ['WINDOWS']
        assert crits['os_architecture'] == ['32']

        return SEARCH_AND_FACET_COMPUTE_RESEOURCES

    cbcsdk_mock.mock_request("POST", "/lcm/view/v1/orgs/test/compute_resources/_search",
                             post_validate)
    api = cbcsdk_mock.api
    query = api.select(ComputeResource).set_appliance_uuid(['c89f183b-f201-4bca-bacc-80184b5b8823']) \
                                       .set_eligibility(['NOT_ELIGIBLE']) \
                                       .set_cluster_name(['launcher-cluster']) \
                                       .set_name(['vsvv-2k8r2']) \
                                       .set_ip_address(['192.168.1.1']) \
                                       .set_installation_status(['NOT_INSTALLED']) \
                                       .set_uuid(['502277cc-0aa9-80b0-9ac8-6f540c11edaf']) \
                                       .set_os_type(['WINDOWS']) \
                                       .set_os_architecture(['32'])

    assert query._count() == 1
    results = [result for result in query._perform_query()]
    assert len(results) == 1
    facet = results[0]
    assert facet.appliance_uuid == 'c89f183b-f201-4bca-bacc-80184b5b8823'
    assert facet.eligibility == 'NOT_ELIGIBLE'
    assert facet.cluster_name == 'launcher-cluster'
    assert facet.name == 'vsvv-2k8r2'
    assert facet.ip_address == '192.168.1.1'
    assert facet.installation_status == 'NOT_INSTALLED'
    assert facet.uuid == '502277cc-0aa9-80b0-9ac8-6f540c11edaf'
    assert facet.os_type == 'WINDOWS'
    assert facet.os_architecture == '32'


def test_search_facet_with_all_bells_and_whistles_failures(cbcsdk_mock):
    """Testng all set methods"""
    query = cbcsdk_mock.api.select(ComputeResource)
    with pytest.raises(ApiError):
        query.set_uuid([1])
    with pytest.raises(ApiError):
        query.set_appliance_uuid([1])
    with pytest.raises(ApiError):
        query.set_eligibility([1])
    with pytest.raises(ApiError):
        query.set_cluster_name([1])
    with pytest.raises(ApiError):
        query.set_name([1])
    with pytest.raises(ApiError):
        query.set_ip_address([1])
    with pytest.raises(ApiError):
        query.set_installation_status([1])
    with pytest.raises(ApiError):
        query.set_os_type([1])
    with pytest.raises(ApiError):
        query.set_os_architecture([1])
