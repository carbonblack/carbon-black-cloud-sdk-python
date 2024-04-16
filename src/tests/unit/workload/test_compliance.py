#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021-2024. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Unit test code for ComplianceBenchmark"""

import pytest
import logging
from cbc_sdk.rest_api import CBCloudAPI
from cbc_sdk.workload import ComplianceBenchmark
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock

from tests.unit.fixtures.workload.mock_compliance import (SEARCH_COMPLIANCE_BENCHMARKS,
                                                          COMPLIANCE_SCHEDULE,
                                                          GET_SECTIONS,
                                                          SEARCH_RULES,
                                                          GET_RULE,
                                                          RULE_COMPLIANCES,
                                                          DEVICE_SPECIFIC_RULE_COMPLIANCE,
                                                          RULE_COMPLIANCE_DEVICE_SEARCH)


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG, filename="log.txt")


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


def test_compliance_benchmark(cbcsdk_mock):
    """Tests a simple compliance benchmark query"""

    def post_validate(url, body, **kwargs):
        assert body == {
            "criteria": {"enabled": [True]},
            "query": "Windows Server",
            "rows": 1,
            "sort": [{"field": "name", "order": "DESC"}]
        }
        return SEARCH_COMPLIANCE_BENCHMARKS

    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             post_validate)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark) \
        .where("Windows Server") \
        .add_criteria("enabled", [True]) \
        .sort_by("name", "DESC").first()

    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"


def test_compliance_benchmark_async(cbcsdk_mock):
    """Test async compliance benchmark query"""

    def post_validate(url, body, **kwargs):
        assert body == {
            "criteria": {"enabled": [True]},
            "query": "Windows Server",
            "rows": 1000,
            "sort": [{"field": "name", "order": "DESC"}]
        }
        return SEARCH_COMPLIANCE_BENCHMARKS

    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             post_validate)

    api = cbcsdk_mock.api
    future_benchmark = api.select(ComplianceBenchmark) \
        .where("Windows Server") \
        .add_criteria("enabled", [True]) \
        .sort_by("name", "DESC").execute_async()

    benchmarks = future_benchmark.result()

    assert benchmarks[0].name == "CIS Compliance - Microsoft Windows Server"


def test_get_compliance_compliance(cbcsdk_mock):
    """Test get_compliance_schedule"""
    cbcsdk_mock.mock_request("GET", "/compliance/assessment/api/v1/orgs/test/settings",
                             COMPLIANCE_SCHEDULE)

    api = cbcsdk_mock.api
    assert ComplianceBenchmark.get_compliance_schedule(api) == COMPLIANCE_SCHEDULE


def test_set_compliance_compliance(cbcsdk_mock):
    """Test set_compliance_schedule"""

    def put_validate(url, body, **kwargs):
        assert body == COMPLIANCE_SCHEDULE
        return body

    cbcsdk_mock.mock_request("PUT", "/compliance/assessment/api/v1/orgs/test/settings",
                             put_validate)

    api = cbcsdk_mock.api
    assert ComplianceBenchmark.set_compliance_schedule(api,
                                                       COMPLIANCE_SCHEDULE["scan_schedule"],
                                                       COMPLIANCE_SCHEDULE["scan_timezone"]) == COMPLIANCE_SCHEDULE


def test_get_sections(cbcsdk_mock):
    """Test get_sections"""
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("GET", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/sections",
                             GET_SECTIONS)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.get_sections() == GET_SECTIONS


def test_get_rules(cbcsdk_mock):
    """Test get_rules"""
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/rules/_search",
                             SEARCH_RULES)
    cbcsdk_mock.mock_request("GET", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/rules/39D861A0-3631-442B-BF94-CC442C73C03E",
                             GET_RULE)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.get_rules() == SEARCH_RULES["results"]

    assert benchmark.get_rules("39D861A0-3631-442B-BF94-CC442C73C03E") == [GET_RULE]


def test_update_rules(cbcsdk_mock):
    """Test update_sections"""
    def put_validate(url, body, **kwargs):
        assert body == [{
            "rule_id": "39D861A0-3631-442B-BF94-CC442C73C03E",
            "enabled": True
        }]
        return [{
            "id": "39D861A0-3631-442B-BF94-CC442C73C03E",
            "rule_name": "(L1) Ensure 'Configure Offer Remote Assistance' is set to 'Disabled'",
            "enabled": True,
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance"
        }]

    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("PUT", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/rules",
                             put_validate)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.update_rules(["39D861A0-3631-442B-BF94-CC442C73C03E"], True)[0]["enabled"] is True


def test_execute_action(cbcsdk_mock):
    """Test execute_action"""
    def post_validate(url, body, **kwargs):
        assert body["action"] == "REASSESS"
        if "device_ids" in body:
            assert body["device_ids"] == [1]
            return {
                "status_code": "SUCCESS",
                "message": "Action Successful"
            }
        return {
            "status_code": "SUCCESS",
            "message": "Successfully triggered Reassess for BenchmarkSet: eee5e491-9c31-4a38-84d8-50c9163ef559"
        }

    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/actions",
                             post_validate)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/compliance/device_actions",
                             post_validate)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.execute_action("REASSESS")["status_code"] == "SUCCESS"
    assert benchmark.execute_action("REASSESS", [1])["status_code"] == "SUCCESS"


def test_get_rule_compliances(cbcsdk_mock):
    """Test get_rule_compliances"""
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/compliance/rules/_search",
                             RULE_COMPLIANCES)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.get_rule_compliances("Remote Assistance") == RULE_COMPLIANCES["results"]


def test_get_device_rule_compliances(cbcsdk_mock):
    """Test get_device_rule_compliances"""
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/compliance/devices/1/rules/_search",
                             DEVICE_SPECIFIC_RULE_COMPLIANCE)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.get_device_rule_compliances(1, "Remote Assistance") == DEVICE_SPECIFIC_RULE_COMPLIANCE["results"]


def test_get_rule_compliance_devices(cbcsdk_mock):
    """Test get_rule_compliance_devices"""
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/_search",
                             SEARCH_COMPLIANCE_BENCHMARKS)
    cbcsdk_mock.mock_request("POST", "/compliance/assessment/api/v1/orgs/test/benchmark_sets/"
                             "eee5e491-9c31-4a38-84d8-50c9163ef559/compliance/rules/"
                             "39D861A0-3631-442B-BF94-CC442C73C03E/devices/_search",
                             RULE_COMPLIANCE_DEVICE_SEARCH)

    api = cbcsdk_mock.api
    benchmark = api.select(ComplianceBenchmark, "eee5e491-9c31-4a38-84d8-50c9163ef559")
    assert benchmark.name == "CIS Compliance - Microsoft Windows Server"

    assert benchmark.get_rule_compliance_devices("39D861A0-3631-442B-BF94-CC442C73C03E", "Example") == \
        RULE_COMPLIANCE_DEVICE_SEARCH["results"]
