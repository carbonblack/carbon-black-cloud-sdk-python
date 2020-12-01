Concepts
================================

Platform Devices vs Endpoint Standard Devices
---------------------------------------------
For most use cases, Platform Devices are sufficient to access information about devices
and change that information. If you want to connect to a device using Live Response,
then you must use Endpoint Standard Devices and a Live Response API Key.

::

  # Device information is accessible with Platform Devices
  >>> api = CBCloudAPI(profile='platform')
  >>> platform_devices = api.select(platform.Device).set_os(["WINDOWS", "LINUX"])
  >>> for device in platform_devices:
  ...   print(
        f'''
        Device ID: {device.id}
        Device Name: {device.name}

        '''
  Device ID: 1234
  Device Name: Win10x64

  Device ID: 5678
  Device Name: UbuntuDev


  # Live Response is accessible with Endpoint Standard Devices
  >>> api = CBCloudAPI(profile='live_response')
  >>> endpoint_standard_device = api.select(endpoint_standard.Device, 1234)
  >>> endpoint_standard_device.lr_session()
  url: /integrationServices/v3/cblr/session/428:1234 -> status: PENDING
  [...]

Queries
----------------------------------------

Generally, to retrieve information from your Carbon Black Cloud instance you will:

1. `Create a Query <#create-queries-with-cbcloudapi-select>`_
2. `Refine the Query <#refine-queries-with-where-and-and-or>`_
3. `Execute the Query <#execute-a-query>`_

Create Queries with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data is retrieved from the Carbon Black Cloud with :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>` statements.
A ``select()`` statement creates a ``query``, which can be further `refined with parameters or criteria <#refine-queries-with-where-and-and-or>`_, and then `executed <#refine-queries-with-where-and-and-or>`_.

::

  # Create a query for devices
  >>> device_query = api.select(platform.Device).where('avStatus:AV_ACTIVE')

  # The query has not yet been executed
  >>> type(device_query)
  <class cbc_sdk.platform.devices.DeviceSearchQuery>

This query will search for Platform Devices with antivirus active.


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
  >>> string_query = api.select(platform.Device).where("avStatus:AV_ACTIVE")
  >>> keyword_query = api.select(platform.Device).where(avStatus="AV_ACTIVE").

Queries must be
consistent in their use of strings or keywords; do not mix strings and keywords.

::

  # Not allowed
  >>> mixed_query = api.select(platform.Device).where(avStatus='Win7x').and_("virtualMachine:true")
  cbc_sdk.errors.ApiError: Cannot modify a structured query with a raw parameter

Execute a Query
^^^^^^^^^^^^^^^

A query is not executed on the server until it's accessed, either as an iterator
(where it will generate results on demand as they're requested) or as a list
(where it will retrieve the entire result set and save to a list).

::

  # Create and Refine a query
  >>> device_query = api.select(platform.Device).where('avStatus:AV_ACTIVE').set_os(["WINDOWS"])

  # Execute the query by accessing as a list
  >>> matching_devices = [device for device in device_query]

  >>> print(f"First matching device ID: {matching_devices[0].id}")
  First matching device ID: 1234

  # Or as an iterator
  >>> for matching_device in device_query:
  ...   print(f"Matching device ID: {matching_device.id})
  Matching device ID: 1234
  Matching device ID: 5678

You can also call the Python built-in ``len()`` on this object
to retrieve the total number of items matching the query.

::

  # Retrieve total number of matching devices
  >>> len(device_query)
  2

In this example, the matching device ID's are accessed with ``device.id``. If using
Endpoint Standard Devices, the device ID's are accessed with ``device.deviceId``.

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

Criteria also modify a query, and can be used with or without parameters.
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

:mod:`ResultFacet <cbc_sdk.audit_remediation.base.ResultFacet>` and :mod:`DeviceSummaryFacet <cbc_sdk.audit_remediation.base.DeviceSummaryFacet>`


  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_device_ids`
  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_device_names`
  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_device_os`
  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_policy_ids`
  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_policy_names`
  - :meth:`cbc_sdk.audit_remediation.base.FacetQuery.set_status`

:mod:`Alert <cbc_sdk.platform.alerts.BaseAlert>`

  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_categories`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_create_time`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_device_ids`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_device_names`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_device_os`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_device_os_versions`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_device_username`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_group_results`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_alert_ids`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_legacy_alert_ids`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_minimum_severity`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_policy_ids`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_policy_names`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_process_names`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_process_sha256`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_reputations`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_tags`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_target_priorities`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_threat_ids`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_types`
  - :meth:`cbc_sdk.platform.alerts.BaseAlertSearchQuery.set_workflows`

:mod:`WatchlistAlert <cbc_sdk.platform.alerts.WatchlistAlert>`

  - :meth:`cbc_sdk.platform.alerts.WatchlistAlertSearchQuery.set_watchlist_ids`
  - :meth:`cbc_sdk.platform.alerts.WatchlistAlertSearchQuery.set_watchlist_names`

:mod:`CBAnalyticsAlert <cbc_sdk.platform.alerts.CBAnalyticsAlert>`

  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_blocked_threat_categories`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_device_locations`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_kill_chain_statuses`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_not_blocked_threat_categories`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_policy_applied`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_reason_code`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_run_states`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_sensor_actions`
  - :meth:`cbc_sdk.platform.alerts.CBAnalyticsAlertSearchQuery.set_threat_cause_vectors`

:mod:`VMwareAlert <cbc_sdk.platform.alerts.VMwareAlert>`

  - :meth:`cbc_sdk.platform.alerts.VMwareAlertSearchQuery.set_group_ids`

Modules not yet Supported for Criteria
""""""""""""""""""""""""""""""""""""""

:mod:`RunHistory <cbc_sdk.audit_remediation.base.RunHistory>`
:mod:`Event <cbc_sdk.enterprise_edr.base.Event>`
:mod:`Process <cbc_sdk.enterprise_edr.base.Process>`


Asynchronous queries
--------------------

A number of queries allow for asynchronous mode of operation. Those utilize python futures and the request itself is performed in a separate worker thread.
An internal thread pool is utilized to support multiple CBC queries executing in an asynchronous manner without blocking the main thread.

Execute an asynchronous query
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Running asynchronous queries is done by invoking the ``execute_async()`` method, e.g:

  >>> async_query = api.select(EnrichedEvent).where('process_name:chrome.exe').execute_async()

The ``execute_async()`` method returns a python future object that can be later on waited for results.

Fetching asynchronous queries' results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Results from asynchronous queries can be retrieved by using the result() method since they are actually futures:

  >>> print(async_query.result())

This would block the main thread until the query completes.

Modules with support for asynchronous queries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`Process <cbc_sdk.enterprise_edr.base.Process>`

:mod:`EnrichedEvent <cbc_sdk.endpoint_standard.base.EnrichedEvent>`

:mod:`EnrichedEventFacet <cbc_sdk.endpoint_standard.base.EnrichedEventFacet>`


Facets
------

Facet search queries return statistical information indicating the relative weighting of the requested values as per the specified criteria.
There are two types of criteria that can be set, one is the ``range`` type which is used to specify discrete values (integers or timestamps - specified both as seconds since epoch and also as ISO 8601 strings).
The results are then grouped by occurence within the specified range.
The other type is the ``term`` type which allow for one or more fields to use as a criteria on which to return weighted results.

Setting ranges
^^^^^^^^^^^^^^

Ranges are configured via the ``add_range()`` method which accepts a dictionary of range settings:

    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> query = api.select(EnrichedEventFacet).where(process_pid=1000).add_range(range)
    
The range settings are as follows:

* ``field`` - the field to return the range for, should be a discrete one (integer or ISO 8601 timestamp) 
* ``start`` - the value to begin grouping at
* ``end`` - the value to end grouping at
* ``bucket_size``- how large of a bucket to group results in. If grouping an ISO 8601 property, use a string like '-3DAYS'

Multiple ranges can be configured per query by passing a list of range dictionaries.

Setting terms
^^^^^^^^^^^^^

Terms are configured via the ``add_facet_field()`` method:

    >>> query = api.select(EnrichedEventFacet).where(process_pid=1000),add_facet_field("process_name")

The argument to add_facet_field method is the name of the field to be summarized.
    
Getting facet results
^^^^^^^^^^^^^^^^^^^^^

The query result for facet queries is a single object with two properties: ``terms`` and ``ranges`` that contain the facet search result weighted as per the criteria provided


Modules with support for facet searches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`ProcessFacet <cbc_sdk.enterprise_edr.base.ProcessFacet>`

:mod:`EnrichedEventFacet <cbc_sdk.endpoint_standard.base.EnrichedEventFacet>`

