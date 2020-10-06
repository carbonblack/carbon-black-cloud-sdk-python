Concepts
================================

Queries
----------------------------------------

Generally, to retrieve information from your Carbon Black Cloud instance:

1. `Create a Query <#create-queries-with-cbcloudapi-select>`_
2. `Refine the Query <#refine-queries-with-where-and-and-or>`_
3. `Execute the Query <#execute-a-query>`_

Create Queries with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data is retrieved from the Carbon Black Cloud with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>` statements.
A ``select()`` statement creates a ``query``, which can be further `refined with parameters or criteria <#refine-queries-with-where-and-and-or>`_, and then `executed <#refine-queries-with-where-and-and-or>`_.

::

  # Create a query for devices
  >>> device_query = api.select(endpoint_standard.Device).where('hostName:Win7x64')

  # The query has not yet been executed
  >>> type(device_query)
  <class cbc_sdk.endpoint_standard.Query>

This query will search for Endpoint Standard Devices with a hostname containing ``Win7x64``.


Refine Queries with :func:`where() <cbc_sdk.base.QueryBuilder.where>`, :func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and :func:`or_() <cbc_sdk.base.QueryBuilder.or_>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Queries can be refined during or after declaration with
:func:`where() <cbc_sdk.base.QueryBuilder.where>`,
:func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and
:func:`or_() <cbc_sdk.base.QueryBuilder.or_>`.

::

  # Create a query for events
  >>> event_query = api.select(endpoint_standard.Event).where(hostName='Win10').and_(ipAddress='10.0.0.1')

  # Refine the query
  >>> event_query.and_(applicationName='googleupdate.exe')
  >>> event_query.and_(eventType='REGISTRY_ACCESS')
  >>> event_query.and_(ownerNameExact='DevRel')

This query will search for Endpoint Standard Events created by the application
``googleupdate.exe`` accessing the registry on a device with a hostname containing
``Win10``, an IP Address of ``10.0.0.1``, and owned by ``DevRel``.

Be Consistent When Refining Queries
"""""""""""""""""""""""""""""""""""

All queries are of type :meth:`QueryBuilder() <cbc_sdk.base.QueryBuilder>`, with support for either
raw string-based queries , or keyword arguments.

::

  # Equivalent queries
  >>> string_query = api.select(Device).where("hostName:Win7x64")
  >>> keyword_query = api.select(Device).where(hostName="Win7x64").

Queries must be
consistent in their use of strings or keywords; do not mix strings and keywords.

::

  # Not allowed
  >>> mixed_query = api.select(Device).where(hostName='Win7x').and_("ipAddress:10.0.0.1")
  cbc_sdk.errors.ApiError: Cannot modify a structured query with a raw parameter

Execute a Query
^^^^^^^^^^^^^^^

A query is not executed on the server until it's accessed, either as an iterator
(where it will generate results on demand as they're requested) or as a list
(where it will retrieve the entire result set and save to a list).

::

  # Execute the query by accessing as a list
  >>> matching_devices = [device for device in device_query]

  >>> print(f"First matching device ID: {matching_devices[0].deviceId}")
  First matching device ID: 1234

  # Or as an iterator
  >>> for matching_device in device_query:
  ...   print(f"Matching device ID: {matching_device.deviceId})
  Matching device ID: 1234
  Matching device ID: 5678

You can also call the Python built-in ``len()`` on this object
to retrieve the total number of items matching the query.

::

  # Retrieve total number of matching devices
  >>> len(device_query)
  2

Query Parameters vs Criteria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For queries, some Carbon Black Cloud APIs use ``GET`` requests with parameters,
and some use ``POST`` requests with criteria.

Parameters
""""""""""

Parameters modify a query. When modifying a query with
:func:`where() <cbc_sdk.base.QueryBuilder.where>`,
:func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and
:func:`or_() <cbc_sdk.base.QueryBuilder.or_>`, those modifications become query
parameters when sent to Carbon Black Cloud.

::

  >>> device_query = api.select(endpoint_standard.Device).where(hostName='Win7').and_(ipAddress='10.0.0.1')

Executing this query results in an API call similar to ``GET /integrationServices/v3/device?hostName='Win7'&ipAddress='10.0.0.1'``

Criteria
""""""""

Criteria also modify a query, and can be used with our without parameters.
When using CBC SDK, there are API-specific methods you can use to add criteria to queries.

::

  # Create a query for alerts
  >>> alert_query = api.select(cbc_sdk.Platform.Alert)

  # Refine the query with parameters
  >>> alert_query.where(alert_severity=9).or_(alert_severity=10)

  # Refine the query with criteria
  >>> alert_query.set_device_os(["MAC"]).set_device_os_versions(["10.14.6"])


Executing this query results in an API call to ``POST /appservices/v6/orgs/{org_key}/alerts/_search``
with this JSON Request Body:

.. code-block:: json

  {
    "query": "alert_severity:9 OR alert_severity:10",
    "criteria": {
      "device_os": ["MAC"],
      "device_os_version": ["10.14.6"]
    }
  }

The query parameters are sent in ``"query"``, and the criteria are sent in ``"criteria"``.
Not all APIs support criteria. See the list of supported modules below.

Modules with Support for Criteria
"""""""""""""""""""""""""""""""""

:mod:`Run <cbc_sdk.audit_remediation.base.Run>`
  - :meth:`cbc_sdk.audit_remediation.base.RunQuery.device_ids`
  - :meth:`cbc_sdk.audit_remediation.base.RunQuery.device_types`
  - :meth:`cbc_sdk.audit_remediation.base.RunQuery.policy_id`

:mod:`Result <cbc_sdk.audit_remediation.base.Result>` and :mod:`Device Summary <cbc_sdk.audit_remediation.base.DeviceSummary>`


  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_device_ids`
  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_device_names`
  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_device_os`
  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_policy_ids`
  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_policy_names`
  - :meth:`cbc_sdk.audit_remediation.base.ResultQuery.set_status`

:mod:`ResultFacet <cbc_sdk.audit_remediation.base.ResultFacet>`





Audit and Remediation
^^^^^^^^^^^^^^^^^^^^^
  - Result - ResultQuery to get Run Results
      POST /livequery/v1/orgs/{org_key}/runs/{id}/results/_search
      https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#get-query-run-results
      - has .criteria() method implemented (freeform, you supply the kwargs)
      Possible keyword arguments to .criteria():
      - device.id
      - device.name
      - device.os
      - device.policy_id
      - device.policy_name
      - status

  - DeviceSummary - ResultQuery to get Device Summaries
      POST /livequery/v1/orgs/{}/runs/{}/results/device_summaries/_search
      https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#get-device-summary-from-results
      - has .criteria() method implemented (freeform, you supply the kwargs)
      Possible keyword arguments to .criteria():
      - device.id
      - device.name
      - device.os
      - device.policy_id
      - device.policy_name
      - status

  - ResultFacet - FacetQuery to Get Facets From Live Query Results
      POST /livequery/v1/orgs/{}/runs/{}/results/_facet
      https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#get-facets-from-live-query-results
      - has .criteria() method implemented (freeform, you supply the kwargs)
      Possible keyword arguments to .criteria():
      - device.id
      - device.name
      - device.os
      - device.policy_id
      - device.policy_name
      - status

  - DeviceSummaryFacet - inherits ResultFacet -- has same .criteria() method
      POST /livequery/v1/orgs/{}/runs/{}/results/device_summaries/_facet
      https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#get-device-summary-facets
      Possible keyword arguments to .criteria():
      - device.id
      - device.name
      - device.os
      - device.policy_id
      - device.policy_name
      - status

  - RunHistory - RunHistoryQuery
      POST /livequery/v1/orgs/{}/runs/_search
      https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#get-query-history
      - does not yet have .criteria() method implemented

Enterprise EDR
^^^^^^^^^^^^^^

  - Event - enterprise_edr.Query to get Events associated with a Process
    POST /api/investigate/v2/orgs/{}/events/{}/_search
    https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/process-search-v2/#get-events-associated-with-a-given-process
    - does not have .criteria() method implemented

  - Process - AsyncProcessQuery to start a Process search job
    POST /api/investigate/v2/orgs/{}/processes/search_jobs
    https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/process-search-v2/#start-a-process-search-job
    - does not have .criteria() method implemented

Platform
^^^^^^^^

  - Alerts - BaseAlertSearchQuery, WatchlistAlertSearchQuery, CBAnalyticsAlertSearchQuery, VMwareAlertSearchQuery
    POST /appservices/v6/orgs/{0}/alerts/{1}
    POST /appservices/v6/orgs/{0}/alerts/watchlist
    POST /appservices/v6/orgs/{0}/alerts/cbanalytics
    POST /appservices/v6/orgs/{0}/alerts/vmware

    https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/#search-request
    See "Additional Supported ``criteria`` Parameter Values" on that page for accepted criteria
    of each type of Alert.

    - have methods for each possible criteria
