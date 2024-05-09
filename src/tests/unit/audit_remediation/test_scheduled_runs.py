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

"""Test Scheduled Runs and Templates"""

import pytest
import logging
from cbc_sdk.audit_remediation import Template, TemplateHistory
from cbc_sdk.errors import ApiError
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.audit_remediation.mock_templates import (EXAMPLE_TEMPLATE,
                                                                  EXAMPLE_TEMPLATE_REFRESH,
                                                                  EXAMPLE_TEMPLATE_STOPPED,
                                                                  EXAMPLE_TEMPLATE_HISTORY)

log = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


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

def test_template_create_refresh(cbcsdk_mock):
    """Testing creation and refresh of a template"""
    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/templates", EXAMPLE_TEMPLATE)
    cbcsdk_mock.mock_request("GET",
                             "/livequery/v1/orgs/test/templates/xzllqfvlie2bzghqqfkxk9xizqniwcvr",
                             EXAMPLE_TEMPLATE_REFRESH)

    template = api.select(Template) \
        .name("CBC SDK") \
        .schedule("FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0", "America/New_York") \
        .where("SELECT name, VERSION, install_date FROM programs;") \
        .submit()

    assert template.id == "xzllqfvlie2bzghqqfkxk9xizqniwcvr"
    assert template.name == "CBC SDK"

    template.refresh()

    assert template._info == EXAMPLE_TEMPLATE_REFRESH


def test_template_stop(cbcsdk_mock):
    """Testing stop of template"""

    def _stop_template(url, body, **kwargs):
        assert body["schedule"]["status"] == "CANCELLED"
        return EXAMPLE_TEMPLATE_STOPPED

    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/templates", EXAMPLE_TEMPLATE)
    cbcsdk_mock.mock_request("PUT",
                             "/livequery/v1/orgs/test/templates/xzllqfvlie2bzghqqfkxk9xizqniwcvr",
                             _stop_template)

    template = api.select(Template) \
        .name("CBC SDK") \
        .schedule("FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0", "America/New_York") \
        .where("SELECT name, VERSION, install_date FROM programs;") \
        .submit()

    template.stop()

    assert template.schedule["cancelled_by"] == "ABCDE12345"


def test_template_delete(cbcsdk_mock):
    """Testing delete of template"""

    def _delete_template(url, body, **kwargs):
        assert url == "/livequery/v1/orgs/test/templates/xzllqfvlie2bzghqqfkxk9xizqniwcvr"
        assert body is None
        return None

    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/templates", EXAMPLE_TEMPLATE)
    cbcsdk_mock.mock_request("DELETE",
                             "/livequery/v1/orgs/test/templates/xzllqfvlie2bzghqqfkxk9xizqniwcvr",
                             _delete_template)

    template = api.select(Template) \
        .name("CBC SDK") \
        .schedule("FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0", "America/New_York") \
        .where("SELECT name, VERSION, install_date FROM programs;") \
        .submit()

    template.delete()
    assert template._is_deleted
    # Now ensure that certain operations that don't make sense on a deleted object raise ApiError
    with pytest.raises(ApiError):
        template.stop()
    with pytest.raises(ApiError):
        template.query_runs()


def test_template_history(cbcsdk_mock):
    """Testing search of existing templates"""

    def _search_template(url, body, **kwargs):
        assert body["query"] == "CBC SDK"
        return EXAMPLE_TEMPLATE_HISTORY

    api = cbcsdk_mock.api
    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/templates/_search", _search_template)

    template = api.select(TemplateHistory).where("CBC SDK").first()

    assert template.id == "xzllqfvlie2bzghqqfkxk9xizqniwcvr"


def test_template_history_async(cbcsdk_mock):
    """Testing search of existing templates done asynchronously."""
    def _search_template(url, body, **kwargs):
        assert body["query"] == "CBC SDK"
        return EXAMPLE_TEMPLATE_HISTORY

    cbcsdk_mock.mock_request("POST", "/livequery/v1/orgs/test/templates/_search", _search_template)
    api = cbcsdk_mock.api
    query = api.select(TemplateHistory).where("CBC SDK")
    future = query.execute_async()
    result = future.result()
    assert len(result) == 1
    assert result[0].id == "xzllqfvlie2bzghqqfkxk9xizqniwcvr"
