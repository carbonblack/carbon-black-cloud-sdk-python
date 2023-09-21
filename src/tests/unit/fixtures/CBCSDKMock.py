# -*- coding: utf-8 -*-

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
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
import copy
import json
import cbc_sdk
import urllib


class CBCSDKMock:
    """Mock framework for unit tests that need to fetch Carbon Black Cloud data"""
    DEPRECATED_URL_PREFIXES = [
        "/integrationServices/v3/event"
    ]

    def __init__(self, monkeypatch, api):
        """Initializes monkey patch for HTTP VERB requests"""
        self.mocks = {}
        self.monkeypatch = monkeypatch
        self.api = api
        self._last_request_data = None
        self._all_request_data = list()
        monkeypatch.setattr(api, "get_object", self._self_get_object())
        monkeypatch.setattr(api, "get_raw_data", self._self_get_raw_data())
        monkeypatch.setattr(api, "api_request_stream", self._self_api_request_stream())
        monkeypatch.setattr(api, "api_request_iterate", self._self_api_request_iterate())
        post_func = self._self_post_object()
        monkeypatch.setattr(api, "post_object", post_func)
        monkeypatch.setattr(api, "post_multipart", self._self_post_multipart())
        put_func = self._self_put_object()
        monkeypatch.setattr(api, "put_object", put_func)
        monkeypatch.setattr(api, "delete_object", self._self_delete_object())
        monkeypatch.setattr(api, "api_json_request", self._self_patch_object(post_func, put_func))

    class StubResponse(object):
        """Stubbed response to object to support json function similar to requests package"""

        def __init__(self, contents, scode=200, text="", json_parsable=True, url=None):
            """Init default properties"""
            if isinstance(contents, CBCSDKMock.StubResponse):
                self.content = contents.content
                self.status_code = contents.status_code
                self.text = contents.text
                self.url = contents.url
                self._json_parsable = contents._json_parsable
            else:
                self.content = contents
                self.status_code = scode
                if json_parsable and not text:
                    self.text = json.dumps(contents)
                else:
                    self.text = text
                self.url = url
                self._json_parsable = json_parsable

        def json(self):
            """Mimics request package"""
            if self._json_parsable:
                return self.content
            else:
                raise cbc_sdk.errors.ServerError(200, "Cannot parse response as JSON: {0:s}".format(self.content))

    def get_mock_key(self, verb, url):
        """Algorithm for getting/setting mocked VERB + URL"""
        return "{}:{}".format(verb, url)

    def match_key(self, request):
        """Matches mocked requests against incoming request"""
        if request in self.mocks:
            return request
        # Removed regex as partial match hid invalid mocks
        for key in self.mocks.keys():
            if key == request:
                return key
        return None

    def clear_mocks(self):
        """Erase the self.mocks dictionary."""
        self.mocks = {}

    @classmethod
    def _check_for_decommission(self, url):
        for prefix in CBCSDKMock.DEPRECATED_URL_PREFIXES:
            if url.startswith(prefix):
                pytest.fail(f"decommissioned URL {url} called when it shouldn't be")

    def _capture_data(self, data):
        self._all_request_data.append(data)
        self._last_request_data = data

    def mock_request(self, verb, url, body):
        """
        Mocks the VERB + URL by defining the response for that particular request

        Args:
            verb (str): HTTP verb supported [ GET, RAW_GET, POST, POST_MULTIPART, PUT, DELETE, STREAM:methodname,
                                              ITERATE:methodname ]
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
            self._check_for_decommission(url)
            self._capture_data(query_parameters)
            if query_parameters:
                if isinstance(query_parameters, dict):
                    query_parameters = convert_query_params(query_parameters)
                    url += '?%s' % (urllib.parse.urlencode(sorted(query_parameters)))

            matched = self.match_key(self.get_mock_key("GET", url))
            if matched:
                if (isinstance(self.mocks[matched], Exception)
                        or getattr(self.mocks[matched], '__module__', None) == cbc_sdk.errors.__name__):
                    raise self.mocks[matched]
                elif callable(self.mocks[matched]):
                    return self.mocks[matched](url, query_parameters, default)
                else:
                    return self.mocks[matched]
            pytest.fail("GET called for %s when it shouldn't be" % url)

        return _get_object

    def _self_get_raw_data(self):
        def _get_raw_data(url, query_params=None, default=None, **kwargs):
            self._check_for_decommission(url)
            self._capture_data(query_params)
            matched = self.match_key(self.get_mock_key("RAW_GET", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.mocks[matched](url, query_params, default)
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("Raw GET called for %s when it shouldn't be" % url)

        return _get_raw_data

    def _self_api_request_stream(self):
        def _api_request_stream(method, uri, stream_output, **kwargs):
            self._check_for_decommission(uri)
            self._capture_data(kwargs)
            matched = self.match_key(self.get_mock_key(f"STREAM:{method}", uri))
            if matched:
                if callable(self.mocks[matched]):
                    result = self.mocks[matched](uri, kwargs.pop("data", {}), **kwargs)
                    return_data = self.StubResponse(result, 200, result, False)
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return_data = self.mocks[matched]
                if return_data.status_code < 400:
                    stream_output.write(bytes(return_data.text, 'utf-8'))
                return return_data
            pytest.fail(f"{method} called for {uri} when it shouldn't be")

        return _api_request_stream

    def _self_api_request_iterate(self):
        def _api_request_iterate(method, uri, **kwargs):
            self._check_for_decommission(uri)
            self._capture_data(kwargs)
            matched = self.match_key(self.get_mock_key(f"ITERATE:{method}", uri))
            if matched:
                if callable(self.mocks[matched]):
                    result = self.mocks[matched](uri, kwargs.pop("data", {}), **kwargs)
                    return_data = self.StubResponse(result, 200, result, False)
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return_data = self.mocks[matched]
                if return_data.status_code < 400:
                    return return_data.text.splitlines()
            pytest.fail(f"{method} called for {uri} when it shouldn't be")

        return _api_request_iterate

    def _self_post_object(self):
        def _post_object(url, body, **kwargs):
            self._check_for_decommission(url)
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("POST", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body, **kwargs))
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("POST called for %s when it shouldn't be" % url)

        return _post_object

    def _self_post_multipart(self):
        def _post_multipart(url, param_table, **kwargs):
            self._check_for_decommission(url)
            self._capture_data(kwargs)
            matched = self.match_key(self.get_mock_key("POST_MULTIPART", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, param_table, **kwargs))
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("Multipart POST called for %s when it shouldn't be" % url)

        return _post_multipart

    def _self_put_object(self):
        def _put_object(url, body, **kwargs):
            self._check_for_decommission(url)
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("PUT", url))
            if matched:
                response = self.mocks[matched]
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body, **kwargs))
                elif response.content is None:
                    response = copy.deepcopy(self.mocks[matched])
                    response.content = body
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                return response
            pytest.fail("PUT called for %s when it shouldn't be" % url)

        return _put_object

    def _self_delete_object(self):
        def _delete_object(url, body=None):
            self._check_for_decommission(url)
            self._capture_data(body)
            matched = self.match_key(self.get_mock_key("DELETE", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, body))
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("DELETE called for %s when it shouldn't be" % url)

        return _delete_object

    def _self_patch_object(self, post_func, put_func):
        def _patch_object(method, url, **kwargs):
            self._check_for_decommission(url)
            if method == 'POST':
                body = kwargs.pop('data', None)
                return post_func(url, body, **kwargs)
            if method == 'PUT':
                body = kwargs.pop('data', None)
                return put_func(url, body, **kwargs)
            if method != 'PATCH':
                pytest.fail(f"api_json_request called for method {method} on url {url} when it shouldn't be")
            matched = self.match_key(self.get_mock_key("PATCH", url))
            if matched:
                if callable(self.mocks[matched]):
                    return self.StubResponse(self.mocks[matched](url, None, **kwargs))
                elif isinstance(self.mocks[matched], Exception):
                    raise self.mocks[matched]
                else:
                    return self.mocks[matched]
            pytest.fail("PATCH called for %s when it shouldn't be" % url)

        return _patch_object


def convert_query_params(qd):
    """
    Expand a dictionary of query parameters by turning "list" values into multiple pairings of key with value.

    Args:
        qd (dict): A mapping of parameter names to values.

    Returns:
        list: A list of query parameters, each one a tuple containing name and value, after the expansion is applied.
    """
    o = []
    for k, v in iter(qd.items()):
        if isinstance(v, list):
            for item in v:
                o.append((k, item))
        else:
            o.append((k, v))

    return o
