# -*- coding: utf-8 -*-

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

"""CBCSDK Mock Framework"""

import pytest
import re
import copy
import cbc_sdk.errors


class CBCSDKMock:
    """Mock framework for unit tests that need to fetch Carbon Black Cloud data"""
    def __init__(self, monkeypatch, api):
        """Initializes monkey patch for HTTP VERB requests"""
        self.mocks = {}
        self.monkeypatch = monkeypatch
        self.api = api
        self._last_request_data = None
        self._all_request_data = list()
        monkeypatch.setattr(api, "get_object", self._self_get_object())
        monkeypatch.setattr(api, "get_raw_data", self._self_get_raw_data())
        monkeypatch.setattr(api, "post_object", self._self_post_object())
        monkeypatch.setattr(api, "put_object", self._self_put_object())
        monkeypatch.setattr(api, "delete_object", self._self_delete_object())
        monkeypatch.setattr(api, "api_json_request", self._self_patch_object())

    class StubResponse(object):
        """Stubbed response to object to support json function similar to requests package"""
        def __init__(self, contents, scode=200, text=""):
            """Init default properties"""
            self._contents = contents
            self.status_code = scode
            self.text = text

        def json(self):
            """Mimics request package"""
            return self._contents

    def get_mock_key(self, verb, url):
        """Algorithm for getting/setting mocked VERB + URL"""
        return "{}:{}".format(verb, url)

    def match_key(self, request):
        """Matches mocked requests against incoming request"""
        if request in self.mocks:
            return request
        for key in self.mocks.keys():
            exp = key.replace("/", ".")
            matched = re.match(exp, request)
            if matched:
                return key
        return None

    def clear_mocks(self):
        """Erase the self.mocks dictionary."""
        self.mocks = {}

    def _capture_data(self, data):
        self._all_request_data.append(data)
        self._last_request_data = data

    def mock_request(self, verb, url, body):
        """
        Mocks the VERB + URL by defining the response for that particular request

        Args:
            verb (str): HTTP verb supported [ GET, RAW_GET, POST, PUT, DELETE ]
            url (str): The full path of to be mocked with support for regex
            body (?): Any value or object to be returned as mocked response

        Additional Details:
            When PUT body is None then respond with request body

        """
        if verb == "GET" or verb == "RAW_GET" or \
           callable(body) or \
           isinstance(body, self.StubResponse) or \
           body is Exception or body in Exception.__subclasses__() or \
           (getattr(body, '__module__', None) == cbc_sdk.errors.__name__):
            self.mocks["{}:{}".format(verb, url)] = body
        else:
            self.mocks["{}:{}".format(verb, url)] = self.StubResponse(body)

    """
        Factories for mocked API requests
    """
    def _self_get_object(self):
        def _get_object(url, query_parameters=None, default=None):
            self._capture_data(query_parameters)
            matched = self.match_key(self.get_mock_key("GET", url))
            if matched:
                if (self.mocks[matched] is Exception or
                        self.mocks[matched] in Exception.__subclasses__() or
                        getattr(self.mocks[matched], '__module__', None) == cbc_sdk.errors.__name__):
                    raise self.mocks[matched]
                elif callable(self.mocks[matched]):
                    return self.mocks[matched](url, query_parameters, default)
                else:
                    return self.mocks[matched]
            pytest.fail("GET called for %s when it shouldn't be" % url)
        return _get_object

    def _self_post_object(self):
        def _post_object(url, body, **kwargs):
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("POST", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body, **kwargs))
                elif self.mocks[matched] is Exception or self.mocks[matched] in Exception.__subclasses__():
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("POST called for %s when it shouldn't be" % url)
        return _post_object

    def _self_get_raw_data(self):
        def _get_raw_data(url, query_params, **kwargs):
            self._capture_data(query_params)
            matched = self.match_key(self.get_mock_key("RAW_GET", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.mocks[matched](url, query_params, **kwargs)
                elif self.mocks[matched] is Exception or self.mocks[matched] in Exception.__subclasses__():
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("Raw GET called for %s when it shouldn't be" % url)
        return _get_raw_data

    def _self_put_object(self):
        def _put_object(url, body, **kwargs):
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("PUT", url))
            if matched:
                response = self.mocks[matched]
                if response._contents is None:
                    response = copy.deepcopy(self.mocks[matched])
                    response._contents = body
                elif callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body, **kwargs))
                elif self.mocks[matched] is Exception or self.mocks[matched] in Exception.__subclasses__():
                    raise self.mocks[matched]
                return response
            pytest.fail("PUT called for %s when it shouldn't be" % url)
        return _put_object

    def _self_delete_object(self):
        def _delete_object(url, body=None):
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("DELETE", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body))
                elif self.mocks[matched] is Exception or self.mocks[matched] in Exception.__subclasses__():
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("DELETE called for %s when it shouldn't be" % url)
        return _delete_object

    def _self_patch_object(self):
        def _patch_object(method, url, **kwargs):
            matched = self.match_key(self.get_mock_key("PATCH", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, None, **kwargs))
                elif self.mocks[matched] is Exception or self.mocks[matched] in Exception.__subclasses__():
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("PATCH called for %s when it shouldn't be" % url)
        return _patch_object
