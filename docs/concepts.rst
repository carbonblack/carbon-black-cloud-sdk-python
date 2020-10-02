Concepts
================================

Select
------

Data is retrieved from the Carbon Black Cloud with ``CBCloudAPI.select()`` statements.
A ``select()`` statement creates a Query. The Query is not executed on the server
until it's accessed, either as an iterator (where it will generate values on demand
as they're requested) or as a list (where it will retrieve the entire result set
and save to a list). You can also call the Python built-in ``len()`` on this object
to retrieve the total number of items matching the Query.

::

  # query for devices
  >>> devices = api.select(Device).where('deviceHostName:Win7x64').and_('ipAddress:10.0.0.1')
  >>> type(devices)
  ... cbc_sdk.endpoint_standard.DeviceSearchQuery
  # execute the query
  >>> for device in devices:
  ...   print(device._info)

The CBCloudAPI.select() method uses where(), and_(), and or_() to add filtering to a query.
The select statement is an abstraction of QueryBuilder(), with support for either
raw string-based queries ``api.select(Device).where("hostName:Win7x64")``, or
keyword arguments ``api.select(Device).where(hostName="Win7x64")``. Queries must be
consistent in their use of strings or keywords; do not mix strings and keywords,
pick one and stick to it.

Query vs Criteria
^^^^^^^^^^^^^^^^^

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
