Concepts
================================

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
