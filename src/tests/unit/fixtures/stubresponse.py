"""Stub responses for use in mock testing"""

import pytest
import json


class StubElapsed(object):
    """Stub for the "elapsed" member of the response class."""
    def total_seconds(self):
        """Return the total number of seconds elapsed."""
        return 0


class StubResponse(object):
    """Stub for an HTTP response object."""
    def __init__(self, contents, scode=200, text=None):
        """Initialize the StubResponse object."""
        self._contents = contents
        self.status_code = scode
        self.text = text or json.dumps(contents)
        self.content = self.text
        self.elapsed = StubElapsed()

    def json(self):
        """Return the JSON contents of the response."""
        return self._contents or json.loads(self.text)


def _failing_get_object(url, parms=None, default=None):
    pytest.fail("GET called for %s when it shouldn't be" % url)


def _failing_get_raw_data(url, query_params, **kwargs):
    pytest.fail("Raw GET called for %s when it shouldn't be" % url)


def _failing_post_object(url, body, **kwargs):
    pytest.fail("POST called for %s when it shouldn't be" % url)


def _failing_put_object(url, body, **kwargs):
    pytest.fail("PUT called for %s when it shouldn't be" % url)


def _failing_delete_object(url):
    pytest.fail("DELETE called for %s when it shouldn't be" % url)


def patch_cbapi(monkeypatch, api, **kwargs):
    """Patch an API instance with our "failing" stub functions."""
    monkeypatch.setattr(api, "get_object", kwargs.get('GET', _failing_get_object))
    monkeypatch.setattr(api, "get_raw_data", kwargs.get('RAW_GET', _failing_get_raw_data))
    monkeypatch.setattr(api, "post_object", kwargs.get('POST', _failing_post_object))
    monkeypatch.setattr(api, "put_object", kwargs.get('PUT', _failing_put_object))
    monkeypatch.setattr(api, "delete_object", kwargs.get('DELETE', _failing_delete_object))
