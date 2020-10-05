Concepts
================================

Create Queries with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>`
-----------------------------------------------------------------------------------

Data is retrieved from the Carbon Black Cloud with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>` statements.
A ``select()`` statement creates a ``query``, which can be further refined with parameters or criteria, and then executed.

::

  # Create a query for devices
  >>> device_query = api.select(Device).where('deviceHostName:Win7x64')

  # Refine the query further
  >>> device_query = device_query.and_('ipAddress:10.0.0.1')

  # The query has not yet been executed
  >>> type(device_query)
  <class cbc_sdk.endpoint_standard.DeviceSearchQuery>

This query will search for devices with a hostname containing ``Win7x64``, and a reported
IP address of ``10.0.0.1``. The query is not executed on the server until it's accessed, either as an iterator (where it will generate values on demand
as they're requested) or as a list (where it will retrieve the entire result set
and save to a list).

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

Refine Queries with :func:`where() <cbc_sdk.base.QueryBuilder.where>`, :func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and :func:`or_() <cbc_sdk.base.QueryBuilder.or_>`
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Queries can be refined during or after declaration with
:func:`where() <cbc_sdk.base.QueryBuilder.where>`,
:func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and
:func:`or_() <cbc_sdk.base.QueryBuilder.or_>`.

::

  # NOT SUPPORTED. ONLY ONE GUID PER SEARCH
  >>> process_query = api.select(Process).where(process_guid='guid').or_(process_guid='anotherguid')


  # ALL PARAMS ARE 'AND' TOGETHER FOR DEVICE SEARCH
  >>> device_query = api.select(Device).where(ipAddress='10.0.0.1').and_(deviceId=1234).and_()

All queries are of type :meth:`QueryBuilder() <cbc_sdk.base.QueryBuilder>`, with support for either
raw string-based queries , or keyword arguments.

::

  # Equivalent queries
  >>> string_query = api.select(Device).where("hostName:Win7x64")
  >>> keyword_query = api.select(Device).where(hostName="Win7x64").

Queries must be
consistent in their use of strings or keywords; do not mix strings and keywords,
pick one and stick to it.

Query Parameters vs Criteria
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some Carbon Black Cloud APIs use GET requests with query parameters to filter search results,
and some APIs use POST requests with "criteria" and "query" keys in the JSON request body
to filter search results.

For APIs that use GET requests to retrieve data, using ``where()``, ``and_()``,
and ``or_()`` methods on ``select()`` will put the filtering parameters in
the query parameters of the GET request.

For APIs that use POST requests to retrieve data, the ``where()``, ``and_()``,
and ``or_()`` methods on ``select()`` will put the filtering parameters in
the JSON request body key ``query``. Filtering criteria can further narrow search
results, with the use of the ``.criteria()`` method and criteria keyword arguments.
Platform Alert and Device objects support individual filtering criteria methods,
like ``.set_device_os()``, ``.set_reputations()``, and more. These methods put
the filtering criteria in the JSON request body key ``criteria``.

::

  # query for Alerts
  >>> alerts = api.select(Alert).set_device_os(["MAC"]).set_device_os_versions(["10.14.6"])\
  ...                           .set_reputations(["COMPANY_BLACK_LIST"])

**APIs/Models with support for criteria:**

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
