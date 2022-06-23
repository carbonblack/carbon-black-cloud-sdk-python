#!/usr/bin/env python3

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

"""Manages the CBC SDK connection to the server."""

from __future__ import absolute_import

import pkgutil
import cbc_sdk
import requests
import sys
from requests.adapters import HTTPAdapter, DEFAULT_POOLBLOCK, DEFAULT_RETRIES, DEFAULT_POOLSIZE, DEFAULT_POOL_TIMEOUT


try:
    from requests.packages.urllib3.util.ssl_ import create_urllib3_context
    REQUESTS_HAS_URLLIB_SSL_CONTEXT = True
except ImportError:
    REQUESTS_HAS_URLLIB_SSL_CONTEXT = False

import ssl


# Older versions of requests (such as the one packaged with Splunk) do not have a Retry object
# in the packaged version of urllib3. Fall back gracefully.
try:
    from requests.packages.urllib3 import Retry
    MAX_RETRIES = Retry(total=5, status_forcelist=[502, 504], backoff_factor=0.5)
except ImportError:
    MAX_RETRIES = 5

import logging
import json

import urllib

from .credentials import Credentials
from .credential_providers.default import default_credential_provider
from .errors import ClientError, QuerySyntaxError, ServerError, TimeoutError, ApiError, ObjectNotFoundError, \
    UnauthorizedError, ConnectionError, ModelNotFound
from . import __version__

from .cache.lru import lru_cache_function
from .base import CreatableModelMixin, NewBaseModel
from .utils import convert_query_params

log = logging.getLogger(__name__)
DEFAULT_STREAM_BUFFER_SIZE = 1024


def try_json(resp):
    """
    Return a parsed JSON representation of the input.

    Args:
        resp (Response): Input to be parsed.

    Returns:
        object: The parsed JSON result, or an empty dict if the value is not valid JSON.
    """
    try:
        return resp.json()
    except ValueError:
        return dict()


def check_python_tls_compatibility():
    """
    Verify which level of TLS/SSL that this version of the code is compatible with.

    Returns:
        str: The maximum level of TLS/SSL that this version is compatible with.
    """
    try:
        CBCSDKSessionAdapter(force_tls_1_2=True)
    except Exception:
        ret = "TLSv1.1"

        if "OP_NO_TLSv1_1" not in ssl.__dict__:
            ret = "TLSv1.0"
        elif "OP_NO_TLSv1" not in ssl.__dict__:
            ret = "SSLv3"
        elif "OP_NO_SSLv3" not in ssl.__dict__:
            ret = "SSLv2"
        else:
            ret = "Unknown"
    else:
        ret = "TLSv1.2"

    return ret


class CBCSDKSessionAdapter(HTTPAdapter):
    """Adapter object used to handle TLS connections to the CB server."""

    def __init__(self, verify_hostname=True, force_tls_1_2=False, max_retries=DEFAULT_RETRIES, **pool_kwargs):
        """
        Initialize the CBCSDKSessionManager.

        Args:
            verify_hostname (boolean): True if we want to verify the hostname.
            force_tls_1_2 (boolean): True to force the use of TLS 1.2.
            max_retries (int): Maximum number of retries.
            **pool_kwargs: Additional arguments.

        Raises:
            ApiError: If the library versions are too old to force the use of TLS 1.2.
        """
        self._cbc_sdk_verify_hostname = verify_hostname
        self._cbc_sdk_force_tls_1_2 = force_tls_1_2

        if force_tls_1_2 and not REQUESTS_HAS_URLLIB_SSL_CONTEXT:
            raise ApiError("Cannot force the use of TLS1.2: Python, urllib3, and requests versions are too old.")

        super(CBCSDKSessionAdapter, self).__init__(max_retries=max_retries, **pool_kwargs)

    def init_poolmanager(self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs):
        """
        Initialize the connection pool manager.

        Args:
            connections (int): Initial number of connections to be used.
            maxsize (int): Maximum size of the connection pool.
            block (object): Blocking policy.
            **pool_kwargs: Additional arguments for the connection pool.

        Returns:
            None
        """
        if self._cbc_sdk_force_tls_1_2 and REQUESTS_HAS_URLLIB_SSL_CONTEXT:
            # Force the use of TLS v1.2 when talking to this Cb Response server.
            context = create_urllib3_context(ciphers=('TLSv1.2:!aNULL:!eNULL:!MD5'))
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            pool_kwargs['ssl_context'] = context

        if not self._cbc_sdk_verify_hostname:
            # Provide the ability to validate a Carbon Black server's SSL certificate without validating the hostname
            # (by default Carbon Black certificates are "issued" as CN=Self-signed Carbon Black Enterprise Server
            # HTTPS Certificate)
            pool_kwargs["assert_hostname"] = False

        return super(CBCSDKSessionAdapter, self).init_poolmanager(connections, maxsize, block, **pool_kwargs)


class Connection(object):
    """Object that encapsulates the HTTP connection to the CB server."""

    def __init__(self,
                 credentials,
                 integration_name=None,
                 timeout=None,
                 max_retries=None,
                 proxy_session=None,
                 **pool_kwargs):
        """
        Initialize the Connection object.

        Args:
            credentials (object): The credentials to use for the connection.
            integration_name (str): The integration name being used.
            timeout (int): The timeout value to use for HTTP requests on this connection.
            max_retries (int): The maximum number of times to retry a request.
            proxy_session (requests.Session) custom session to be used
            **pool_kwargs: Additional arguments to be used to initialize connection pooling.

        Raises:
            ApiError: If there's an internal error initializing the connection.
            ConnectionError: If there's a problem with the credentials.
        """
        if not credentials.url or not credentials.url.startswith("https://"):
            raise ConnectionError("Server URL must be a URL: eg. https://localhost")

        if not credentials.token:
            raise ConnectionError("No API token provided")

        self.server = credentials.url.rstrip("/")
        self.ssl_verify = credentials.ssl_verify

        if not self.ssl_verify:
            try:
                from requests.packages.urllib3.exceptions import InsecureRequestWarning
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            except Exception:
                pass
        else:
            if credentials.ssl_cert_file:
                self.ssl_verify = credentials.ssl_cert_file

        user_agent = "CBC_SDK/{0:s} Python/{1:d}.{2:d}.{3:d}" \
            .format(__version__, sys.version_info[0], sys.version_info[1], sys.version_info[2])
        if integration_name:
            user_agent = f"{integration_name} {user_agent}"

        self.token = credentials.token
        self.token_header = {'X-Auth-Token': self.token, 'User-Agent': user_agent}
        if proxy_session:
            self.session = proxy_session
            credentials.use_custom_proxy_session = True
        else:
            self.session = requests.Session()
            credentials.use_custom_proxy_session = False

        self._timeout = timeout
        self.stream_buffer_size = DEFAULT_STREAM_BUFFER_SIZE

        if max_retries is None:
            max_retries = MAX_RETRIES

        try:
            tls_adapter = CBCSDKSessionAdapter(max_retries=max_retries, force_tls_1_2=credentials.ssl_force_tls_1_2,
                                               verify_hostname=credentials.ssl_verify_hostname, **pool_kwargs)
        except ssl.SSLError as e:
            raise ApiError("This version of Python and OpenSSL do not support TLSv1.2: {}".format(e),
                           original_exception=e)
        except Exception as e:
            raise ApiError("Unknown error establishing CBC SDK session: {0}: {1}".format(e.__class__.__name__, e),
                           original_exception=e)

        self.session.mount(self.server, tls_adapter)

        self.proxies = {}
        if credentials.use_custom_proxy_session:
            # get the custom session proxies
            self.proxies = self.session.proxies
        elif credentials.ignore_system_proxy:         # see https://github.com/kennethreitz/requests/issues/879
            # Unfortunately, requests will look for any proxy-related environment variables and use those anyway. The
            # only way to solve this without side effects, is passing in empty strings for 'http' and 'https':
            self.proxies = {
                'http': '',
                'https': '',
                'no': 'pass'
            }
        else:
            if credentials.proxy:
                self.proxies['http'] = credentials.proxy
                self.proxies['https'] = credentials.proxy

    def http_request(self, method, url, **kwargs):
        """
        Submit a HTTP request to the server.

        Args:
            method (str): The method name to use for the HTTP request.
            url (str): The URL to submit the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            object: Result of the HTTP request.

        Raises:
            ApiError: An unknown problem was detected.
            ClientError: The server returned an error code in the 4xx range, indicating a problem with the request.
            ConnectionError: A problem was seen with the HTTP connection.
            ObjectNotFoundError: The specified object was not found on the server.
            QuerySyntaxError: The query passed in had invalid syntax.
            ServerError: The server returned an error code in the 5xx range, indicating a problem on the server side.
            TimeoutError: The HTTP request timed out.
            UnauthorizedError: The stored credentials do not permit access to the specified request.
        """
        method = method.upper()

        verify_ssl = kwargs.pop('verify', None) or self.ssl_verify
        proxies = kwargs.pop('proxies', None) or self.proxies
        stream = kwargs.pop('stream', False)

        new_headers = kwargs.pop('headers', None)
        if new_headers:
            headers = self.token_header.copy()
            headers.update(new_headers)
        else:
            headers = self.token_header

        uri = self.server + url

        try:
            raw_data = kwargs.get("data", None)
            if raw_data:
                log.debug("Sending HTTP {0} {1} with {2}".format(method, url, raw_data))
            r = self.session.request(method, uri, headers=headers, verify=verify_ssl, proxies=proxies,
                                     timeout=self._timeout, stream=stream, **kwargs)
            log.debug('HTTP {0:s} {1:s} took {2:.3f}s (response {3:d})'.format(method, url,
                                                                               r.elapsed.total_seconds(),
                                                                               r.status_code))
        except requests.Timeout as timeout_error:
            raise TimeoutError(uri=uri, original_exception=timeout_error)
        except requests.ConnectionError as connection_error:
            raise ConnectionError("Received a network connection error from {0:s}: {1:s}"
                                  .format(self.server, str(connection_error)),
                                  original_exception=connection_error)
        except Exception as e:
            raise ApiError("Unknown exception when connecting to server: {0:s}".format(str(e)),
                           original_exception=e)
        else:
            if r.status_code >= 500:
                raise ServerError(error_code=r.status_code, message=r.text)
            elif r.status_code == 404:
                raise ObjectNotFoundError(uri=uri, message=r.text)
            elif r.status_code == 401:
                raise UnauthorizedError(uri=uri, action=method, message=r.text)
            elif r.status_code == 400 and try_json(r).get('reason') == 'query_malformed_syntax':
                raise QuerySyntaxError(uri=uri, message=r.text)
            elif r.status_code >= 400:
                raise ClientError(error_code=r.status_code, message=r.text)
            return r

    def get(self, url, **kwargs):
        """
        Submit a GET request on this connection.

        Args:
            url (str): The URL to submit the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            object: Result of the HTTP request.
        """
        return self.http_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        """
        Submit a POST request on this connection.

        Args:
            url (str): The URL to submit the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            object: Result of the HTTP request.
        """
        return self.http_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        """
        Submit a PUT request on this connection.

        Args:
            url (str): The URL to submit the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            object: Result of the HTTP request.
        """
        return self.http_request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        """
        Submit a DELETE request on this connection.

        Args:
            url (str): The URL to submit the request to.
            **kwargs: Additional arguments for the request.

        Returns:
            object: Result of the HTTP request.
        """
        return self.http_request("DELETE", url, **kwargs)


class BaseAPI(object):
    """The base API object used by all CBC SDK objects to communicate with the server."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the base API information.

        Args:
            *args: Unused.
            **kwargs: Additional arguments.
        """
        integration_name = kwargs.pop("integration_name", None)
        self.credential_provider = kwargs.pop("credential_provider", None)

        url, token = kwargs.get("url", None), kwargs.get("token", None)
        if url and token:
            self.credentials = Credentials(kwargs)
            self.credentials.integration = integration_name
            self.credential_profile_name = None
        else:
            credential_file = kwargs.pop("credential_file", None)
            self.credential_profile_name = kwargs.pop("profile", None)
            if not self.credential_provider:
                self.credential_provider = default_credential_provider(credential_file)
            self.credentials = self.credential_provider.get_credentials(self.credential_profile_name)
            if not integration_name:
                integration_name = self.credentials.integration

        timeout = kwargs.pop("timeout", DEFAULT_POOL_TIMEOUT)

        # must be None to use MAX_RETRIES in Connection __init__
        max_retries = kwargs.pop("max_retries", None)
        proxy_session = kwargs.pop("proxy_session", None)
        pool_connections = kwargs.pop("pool_connections", 1)
        pool_maxsize = kwargs.pop("pool_maxsize", DEFAULT_POOLSIZE)
        pool_block = kwargs.pop("pool_block", DEFAULT_POOLBLOCK)

        self.session = Connection(self.credentials,
                                  integration_name=integration_name,
                                  timeout=timeout,
                                  max_retries=max_retries,
                                  proxy_session=proxy_session,
                                  pool_connections=pool_connections,
                                  pool_maxsize=pool_maxsize,
                                  pool_block=pool_block)

    def raise_unless_json(self, ret, expected):
        """
        Raise a ServerError unless we got back an HTTP 200 response with JSON containing all the expected values.

        Args:
            ret (object): Return value to be checked.
            expected (dict): Expected keys and values that need to be found in the JSON response.

        Raises:
            ServerError: If the HTTP response is anything but 200, or if the expected values are not found.
        """
        if ret.status_code == 200:
            message = ret.json()
            for k, v in iter(expected.items()):
                if k not in message or message[k] != v:
                    raise ServerError(ret.status_code, message)
        else:
            raise ServerError(ret.status_code, "{0}".format(ret.content), )

    def get_object(self, uri, query_parameters=None, default=None):
        """
        Submit a GET request to the server and parse the result as JSON before returning.

        Args:
            uri (str): The URI to send the GET request to.
            query_parameters (object): Parameters for the query.
            default (object): What gets returned in the event of an empty response.

        Returns:
            object: Result of the GET request.
        """
        if query_parameters:
            if isinstance(query_parameters, dict):
                query_parameters = convert_query_params(query_parameters)
            uri += '?%s' % (urllib.parse.urlencode(sorted(query_parameters)))

        result = self.api_json_request("GET", uri)
        if result.status_code == 200:
            try:
                return result.json()
            except Exception:
                raise ServerError(result.status_code, "Cannot parse response as JSON: {0:s}".format(result.content))
        elif result.status_code == 204:
            # empty response
            return default
        else:
            raise ServerError(error_code=result.status_code, message="Unknown error: {0}".format(result.content))

    def get_raw_data(self, uri, query_parameters=None, default=None, **kwargs):
        """
        Submit a GET request to the server and return the result without parsing it.

        Args:
            uri (str): The URI to send the GET request to.
            query_parameters (object): Parameters for the query.
            default (object): What gets returned in the event of an empty response.
            **kwargs:

        Returns:
            object: Result of the GET request.
        """
        if query_parameters:
            if isinstance(query_parameters, dict):
                query_parameters = convert_query_params(query_parameters)
            uri += '?%s' % (urllib.parse.urlencode(sorted(query_parameters)))

        hdrs = kwargs.pop("headers", {})
        result = self.api_json_request("GET", uri, headers=hdrs)
        if result.status_code == 200:
            return result.text
        elif result.status_code == 204:
            # empty response
            return default
        else:
            raise ServerError(error_code=result.status_code, message="Unknown error: {0}".format(result.content))

    def api_json_request(self, method, uri, **kwargs):
        """
        Submit a request to the server.

        Args:
            method (str): HTTP method to use.
            uri (str): URI to submit the request to.
            **kwargs (dict): Additional arguments.

        Returns:
            object: Result of the operation.

        Raises:
             ServerError: If there's an error output from the server.
        """
        headers = kwargs.pop("headers", {})
        raw_data = None

        if method in ("POST", "PUT", "PATCH"):
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
                raw_data = kwargs.pop("data", {})
                raw_data = json.dumps(raw_data, sort_keys=True)
            elif headers["Content-Type"] == "multipart/form-data":
                del headers["Content-Type"]  # let the request library set it since we passed files=

        result = self.session.http_request(method, uri, headers=headers, data=raw_data, **kwargs)

        try:
            result_json = result.json()
        except ValueError:
            result_json = {}

        if "errorMessage" in result_json:
            raise ServerError(error_code=result.status_code, message=result_json["errorMessage"])

        return result

    def api_request_stream(self, method, uri, stream_output, **kwargs):
        """
        Submit a request to the specified URI and stream the results back into the given stream object.

        Args:
            method (str): HTTP method to use.
            uri (str): The URI to send the request to.
            stream_output (RawIOBase): The output stream to write the data to.
            **kwargs (dict): Additional arguments for the request.

        Returns:
            object: The return data from the request.
        """
        headers = kwargs.pop("headers", {})
        raw_data = None

        if method in ('POST', 'PUT', 'PATCH'):
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
                raw_data = json.dumps(kwargs.pop("data", {}), sort_keys=True)
        else:
            if 'data' in kwargs:
                del kwargs['data']

        with self.session.http_request(method, uri, headers=headers, data=raw_data, stream=True, **kwargs) as resp:
            for block in resp.iter_content(self.session.stream_buffer_size):
                stream_output.write(block)
        return resp

    def api_request_iterate(self, method, uri, **kwargs):
        """
        Submit a request to the specified URI and iterate over the response as lines of text.

        Should only be used for requests that can be expressed as large amounts of text that can be broken into lines.
        Since this is an iterator, call it with the 'yield from' syntax.

        Args:
            method (str): HTTP method to use.
            uri (str): The URI to send the request to.
            **kwargs (dict): Additional arguments for the request.

        Returns:
            iterable: An iterable that can be used to get each line of text in turn as a string.
        """
        headers = kwargs.pop("headers", {})
        raw_data = None

        if method in ('POST', 'PUT', 'PATCH'):
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
                raw_data = json.dumps(kwargs.pop("data", {}), sort_keys=True)
        else:
            if 'data' in kwargs:
                del kwargs['data']

        with self.session.http_request(method, uri, headers=headers, data=raw_data, stream=True, **kwargs) as resp:
            for line in resp.iter_lines(decode_unicode=True):
                yield line

    def post_object(self, uri, body, **kwargs):
        """
        Send a POST request to the specified URI.

        Args:
            uri (str): The URI to send the POST request to.
            body (object): The data to be sent in the body of the POST request.
            **kwargs (dict): Additional arguments for the HTTP POST.

        Returns:
            object: The return data from the POST request.
        """
        return self.api_json_request("POST", uri, data=body, **kwargs)

    @classmethod
    def _map_multipart_param(cls, table_entry, value):
        """
        Set up the tuple for a multipart request parameter.

        Args:
            table_entry (dict): Entry from the parameter table for the multipart method call.
            value (str): Parameter value.

        Returns:
            tuple: A tuple with three elements, containing the pseudo-filename, data, and MIME type.
        """
        return table_entry.get('filename', None), value, table_entry.get('type', None)

    def post_multipart(self, uri, param_table, **kwargs):
        """
        Send a POST request to the specified URI, with parameters sent as multipart form data.

        Args:
            uri (str): The URI to send the POST request to.
            param_table (dict): A dict of known parameters to the underlying method, each element of which is a
                                parameter name mapped to a dict, which contains elements 'filename' and 'type'
                                representing the pseudo-filename to be used for the data and the MIME type of the data.
            **kwargs (dict): Arguments to pass to the API. Except for "headers," these will all be added as parameters
                             to the form data sent.

        Returns:
            object: The return data from the POST request.
        """
        headers = kwargs.pop("headers", {})
        headers['Content-Type'] = 'multipart/form-data'
        files_body = {k: BaseAPI._map_multipart_param(param_table[k], v)
                      for (k, v) in kwargs.items() if k in param_table}
        return self.api_json_request("POST", uri, headers=headers, files=files_body)

    def put_object(self, uri, body, **kwargs):
        """
        Send a PUT request to the specified URI.

        Args:
            uri (str): The URI to send the PUT request to.
            body (object): The data to be sent in the body of the PUT request.
            **kwargs:

        Returns:
            object: The return data from the PUT request.
        """
        return self.api_json_request("PUT", uri, data=body, **kwargs)

    def delete_object(self, uri):
        """
        Send a DELETE request to the specified URI.

        Args:
            uri (str): The URI to send the DELETE request to.

        Returns:
            object: The return data from the DELETE request.
        """
        return self.api_json_request("DELETE", uri)

    def select(self, cls, unique_id=None, *args, **kwargs):
        """
        Prepare a query against the Carbon Black data store.

        Args:
            cls (class | str): The Model class (for example, Computer, Process, Binary, FileInstance) to query
            unique_id (optional): The unique id of the object to retrieve, to retrieve a single object by ID
            *args:
            **kwargs:

        Returns:
            object: An instance of the Model class if a unique_id is provided, otherwise a Query object
        """
        if isinstance(cls, str):
            cls = select_class_instance(cls)
        if unique_id is not None:
            return select_instance(self, cls, unique_id, *args, **kwargs)
        else:
            return self._perform_query(cls, **kwargs)

    def create(self, cls, data=None):
        """
        Create a new object.

        Args:
            cls (class): The Model class (only some models can be created, for example, Feed, Notification, ...)
            data (object): The data used to initialize the new object

        Returns:
            Model: An empty instance of the model class.

        Raises:
            ApiError: If the Model cannot be created.
        """
        if issubclass(cls, CreatableModelMixin):
            n = cls(self)
            if type(data) is dict:
                for k, v in iter(data.items()):
                    setattr(n, k, v)
            return n
        else:
            raise ApiError("Cannot create object of type {0:s}".format(cls.__name__))

    def _perform_query(self, cls, **kwargs):
        pass

    @property
    def url(self):
        """
        Return the connection URL.

        Returns:
            str: The connection URL.
        """
        return self.session.server


# by default, set expiration to 1 minute and max_size to 1k elements
# TODO: how does this interfere with mutable objects?
@lru_cache_function(max_size=1024, expiration=1 * 60)
def select_instance(api, cls, unique_id, *args, **kwargs):
    """
    Return a new instance of the specified class, given the unique id to fetch the data.

    Args:
        api (CBCloudAPI): Instance of the CBCloudAPI object.
        cls (class): Class of the object being created.
        unique_id (Any): Unique ID associated with that particular object.
        *args (list): Additional arguments for creation.
        **kwargs (dict): Additional arguments for creation.

    Returns:
        object: New object instance.
    """
    return cls(api, unique_id, *args, **kwargs)


def select_class_instance(cls: str):
    """
    Selecting the appropriate class based on the passed string.

    Args:
        cls: The class name represented in a string.

    Returns:
        Object[]:
    """
    # Walk through all the packages contained in the `cbc_sdk`, ensures the loading
    # of all the needed packages.
    _ = [i for i in pkgutil.walk_packages(cbc_sdk.__path__, f"{cbc_sdk.__name__}.")]

    subclasses = set()
    base_subclasses = NewBaseModel.__subclasses__().copy()
    while base_subclasses:
        parent = base_subclasses.pop()
        subclasses.add(parent)
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                base_subclasses.append(child)

    # https://www.python.org/dev/peps/pep-3155/#rationale
    lookup_dict = {klass.__qualname__: klass for klass in subclasses}
    if cls in lookup_dict.keys():
        return lookup_dict[cls]
    raise ModelNotFound()
