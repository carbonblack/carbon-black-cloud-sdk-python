Logging & Diagnostics
=====================

The cbc_sdk provides extensive logging facilities to track down issues communicating with the REST API and understand
potential performance bottlenecks.

Enabling Logging
----------------

The cbc_sdk uses Python's standard :py:mod:`logging` module for logging. To enable debug logging for the cbc_sdk, you
can do the following::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)

All REST API calls, including the API endpoint, any data sent via POST or PUT, and the time it took for the call
to complete::

    >>> devices = [ device for device in cb.select(Device) ]
    DEBUG:cbc_sdk.connection:Sending HTTP POST /appservices/v6/orgs/ABCD1234/devices/_search with {"criteria": {}, "exclusions": {}, "query": ""}
    DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): defense-eap01.conferdeploy.net:443
    DEBUG:urllib3.connectionpool:https://defense-eap01.conferdeploy.net:443 "POST /appservices/v6/orgs/ABCD1234/devices/_search HTTP/1.1" 200 None
    DEBUG:cbc_sdk.connection:HTTP POST /appservices/v6/orgs/ABCD1234/devices/_search took 0.409s (response 200)
