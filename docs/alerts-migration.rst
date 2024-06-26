..
    # *******************************************************
    # Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
    # SPDX-License-Identifier: MIT
    # *******************************************************
    # *
    # * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
    # * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
    # * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
    # * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
    # * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

.. _alert-migration-guide:

Alert Migration
===============

Use this guide to update from SDK v1.4.3 or earlier (using Alerts v6 API) to
SDK v1.5.0 or (Alerts v7 API).

We recommend that customers evaluate the new fields that are available in Alerts v7 API and supported in SDK 1.5.0 onwards
to maximize the benefits from the new data. A lot of new metadata is included in the Alert record that can help simplify your integration. For example, if you were previously getting process information to enrich the command
line, the process commandline is now included in the Alert record.

Resources
---------

* `Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_
* `Alerts v7 Announcement <https://developer.carbonblack.com/2023/06/announcing-vmware-carbon-black-cloud-alerts-v7-api/>`_
* `Alert Search and Response Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields>`_
* Example script showing breaking and compatibility features `alert_v6_v7_migration.py in GitHub Examples <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.
* SDK 1.5.0 Alert Example Script `alerts_common_scenarios.py in GitHub Examples <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

Overview
---------
In SDK 1.5.0, we balance backwards compatibility with making
breaking changes apparent to avoid silent integration failures. Such failures might lead to the perception that things continue to work
when they do not work.

* Breaking Changes

    * Default Search Time Period is reduced to two weeks. See `Default Search Time Period`_.
    * Fields that do not exist in Alert v7 API: FunctionalityDecommissioned exception is raised if called. See
      `SDK Treatment of Fields that have been removed`_.
    * ``get_events()`` method has been removed. See `Enriched Events have been Replaced by Observations`_.
    * Facet terms match the field names. See `Facet Terms`_.
    * Workflow is rebuilt. See `Streamlined Alert Workflow`_.
    * Create Note returns a single ``Note`` instance instead of a list. See `create_note() return type`_.

* Backwards compatibility:

    * Class name change: Alert replaces BaseAlert, but BaseAlert is retained. See `Class Name Changes`_.
    * Field name changes: The previous name is aliased to the new name on get, set, and access by property name. See `Field names aliased`_.
    * The single field port is separated into local and remote fields.  See `Port - split into local and remote`_.

New Features
------------
Enjoy all the new features!

See an example script that demonstrates the SDK 1.5.0 features in
`GitHub Examples, alerts_common_scenarios.py
<https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

* New metadata fields include command lines. View the new fields and identify which fields can be used in criteria, exclusions,
  and as a facet term on the `Developer Network Alerts Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_.
* ``add_exclusions()``: This new method exposes the exclusion element. Any records that match these values
  are excluded from the result set.
* ``get_observations()``: Gets the Observations that are related to the alert.  This feature is available for most Alert types.
* ``get_process()``: This method previously got the process related to a Watchlist Alert.  It is extended to get processes for other Alert Types if the Alert has a ``process_guid`` set.
* Notes can be added to an Alert or a Threat.
* Alert History can be retrieved.
* ``to_json(version)`` is a new method that returns the alert object in json format.

    * This method has been added to replace the use of the ``_info`` attribute because it is an internal representation.
    * If no version parameter is provided, the version will default to API version v7.
    * "v6" can be passed as a parameter and the attribute names will be translated to the Alert v6 names.
    * ``to_json("v6")`` translates field names from the v7 field name to v6 field names and returns a structure as
      close to v6 (SDK 1.4.3) as possible. The fields that do not have equivalents in the v7 API will be omitted.
    * The ``to_json`` method is intended to ease the update path if the ``_info`` attribute was being used.
    * Example method: ``show_to_json(api)``.


    The following code snippet shows how to call the ``to_json`` method for an alert:

    .. code-block:: python

        >>> cb = get_cb_cloud_object(args)
        >>> alert_query = cb.select(Alert)
        >>> alert = alert_query.first()
        >>> v7_dict = alert.to_json()
        >>> v6_dict = alert.to_json("v6")

    The returned object v7_dict will have a dictionary representation of the alert using v7 attribute names and structure.

    The returned object v6_dict will have a dictionary representation of the alert using v6 attribute names and structure.
    If the field does not exist in v7, the field will be omitted from the json representation.

Breaking Changes
----------------
The following changes require integration updates to avoid using functionality that is no longer available.

The "Example Method" refers to the example script `alert_v6_v7_migration.py in GitHub
<https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

Default Search Time Period
^^^^^^^^^^^^^^^^^^^^^^^^^^
The default search period was one month. The default search period is now two weeks.

* The SDK does not make any compensating changes for this change of time.
* Example method: ``base_class_and_default_time_range(api)``.

The following snippet shows how to set the search window to the previous month.  See the Developer Network for details on the
`Time Range Filter <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/#time-range-filter>`_

.. code-block:: python

    >>> alerts = api.select(Alert).set_time_range(range="-1M")

SDK Treatment of Fields that have been removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Some fields from the Alert API v6 (SDK 1.4.3 and earlier) do not have an equivalent in
Alert v7 API (SDK 1.5.0+). A ``FunctionalityDecommissioned`` exception will be raised if they are used.

See `Removed Fields`_ for a list of these fields.

We recommend that you do the following:

* Review the fields that do not have an equivalent.
* After updating to the SDK 1.5.0, check your integrations for error logs that contain ``FunctionalityDecommissioned``
  exceptions.
* Review the new fields and determine what changes can enhance your use cases.
* Use the ``add_criteria`` method to search for alerts. This method replaces the hand-crafted ``set_<field_name>`` methods.
* Example method: ``set_methods_backwards_compatibility(api)``.

For `Removed Fields`_, the SDK 1.5.0+ has the following behavior:

* ``set_<v6 field name>()`` will raise a ``FunctionalityDecommissioned`` exception.
* ``get(<v6 field name>)`` will raise a ``FunctionalityDecommissioned`` exception.
* ``alert.field_name`` will raise a ``FunctionalityDecommissioned`` exception.
* Example method: ``get_methods_backwards_compatibility(api)`` and ``category_monitored_removed(api)``.

Details of all changes to API endpoints and fields are in the
`Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_ on the Developer Network.

The following code block calls the decommissioned method

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile="sample")
    >>> alert_query = api.select(BaseAlert).set_blocked_threat_categories(["NON_MALWARE"])


It generates the following exception:

.. code-block:: python

    cbc_sdk.errors.FunctionalityDecommissioned: The set_kill_chain_statuses method does not exist in in SDK v1.5.0
    because kill_chain_status is not a valid field on Alert v7 API. The functionality has been decommissioned.


Similarly, the following code block calls the get attribute function by using the decommissioned attribute: ``blocked_threat_categories``:

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile="sample")
    >>> alert_query = api.select(BaseAlert)
    >>> alert = alert_query.first()
    >>> alert.get("blocked_threat_category")


It generates the following exception:

.. code-block:: python

    cbc_sdk.errors.FunctionalityDecommissioned:
    The Attribute 'blocked_threat_category' does not exist in object 'WatchlistAlert' because it was
    deprecated in Alerts v7. In SDK 1.5.0 the functionality is decommissioned.

Removed Fields
^^^^^^^^^^^^^^

.. list-table:: Field that have been removed from Alert v7 API
   :widths: 50, 50
   :header-rows: 1
   :class: longtable

   * - Field Name
     - Alert Types
   * - blocked_threat_category
     - CB Analytics
   * - category
     - All
   * - count
     - Watchlist
   * - document_guid
     - Watchlist
   * - group_details
     - All
   * - kill_chain_status
     - CB Analytics
   * - not_blocked_threat_category
     - CB Analytics
   * - target_value
     - Container Runtime
   * - threat_activity_dlp
     - CB Analytics
   * - threat_activity_phish
     - CB Analytics
   * - threat_cause_threat_category
     - All
   * - threat_cause_vector
     - All
   * - threat_indicators
     - Watchlist
   * - workload_id
     - Container Runtime


Enriched Events have been Replaced by Observations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CBAnalytics get_events() is removed.

* The Enriched Events that this method returns have been deprecated.
* Instead, use `Observations <https://developer.carbonblack.com/2023/07/how-to-take-advantage-of-the-new-observations-api/>`_.
* More information is on the Developer Network Blog,
  `How to Take Advantage of the New Observations API <https://developer.carbonblack.com/2023/07/how-to-take-advantage-of-the-new-observations-api/>`_.

Instead of:

.. code-block:: python

    >>> cb = get_cb_cloud_object(args)
    >>> alert_query = cb.select(CBAnalyticsAlert)
    >>> alert = alert_query.first()
    >>> alert.get_events()


Use ``get_observations``. Observations are available for many Alert Types whereas Enriched Events were limited to
CB_Analytics Alerts. Watchlist Alerts do not have associated observations, so Alerts of type Watchlist
are excluded from the search.

.. code-block:: python

    >>> alert_query = cb.select(Alert).add_exclusions("type", "WATCHLIST")
    >>> alert = alert_query.first()
    >>> observations_list = alert.get_observations()
    >>> len(observations_list) # execute the query

* Example method: ``observation_replaces_enriched_event(api)``

Facet Terms
^^^^^^^^^^^

In Alerts v6 API and SDK 1.4.3, the terms available for use in facet requests
were very limited and the facet terms did not always match the field name upon which it operated.

In Alerts v7 API and SDK 1.5.0, more fields are available and the facet term matches the field name.

* If the term used in v6 is the same as the field in v7, the facet term continues to work
* If the term used in v6 is not the same as v7, a ``FunctionalityDecommissioned`` exception is raised.

    * Raising the exception was a conscious decision to reduce the complexity and ongoing maintenance effort in the SDK,
      and to ensure visibility to customers that the Facet capability has significant improvements from which
      integrations will benefit.
    * Example method: ``facet_terms(api)``

The following snippet shows a pre-SDK 1.4.3 facet request and the ``FunctionalityDecommissioned`` exception that the
SDK 1.5.0 SDK generates.

.. code-block:: python

    >>> from cbc_sdk.errors import FunctionalityDecommissioned
    >>> try:
    ...     print("Calling facets with invalid term.")
    ...     facet_list = api.select(BaseAlert).facets(["ALERT_TYPE"])
    ... except FunctionalityDecommissioned as e:
    ...     print(e)
    ...
    Calling facets with invalid term.
    The Field 'ALERT_TYPE' is not a valid facet name because it was deprecated in Alerts v7. functionality has been decommissioned.

The following snippet shows a valid request and printed response.

.. code-block:: python

    >>> import json
    >>> facet_list = api.select(Alert).facets(["policy_applied", "attack_technique"])
    >>> print("This is a valid facet response: {}".format(json.dumps(facet_list, indent=4)))
    This is a valid facet response: [
        {
            "field": "attack_technique",
            "values": [
                {
                    "total": 2,
                    "id": "T1048.002",
                    "name": "T1048.002"
                },
                {
                    "total": 1,
                    "id": "T1490",
                    "name": "T1490"
                }
            ]
        },
        {
            "field": "policy_applied",
            "values": [
                {
                    "total": 69224,
                    "id": "NOT_APPLIED",
                    "name": "NOT_APPLIED"
                },
                {
                    "total": 450,
                    "id": "APPLIED",
                    "name": "APPLIED"
                }
            ]
        }
    ]



Streamlined Alert Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Alert Closure workflow is updated to be more streamlined and improves Alert lifecycle management.

The workflow leverages the alert search structure to specify the alerts to close and has the following status':

* **Open**, the initial status
* **In Progress**, a new intermediate status
* **Closed** which replaces *Dismissed*

As a result of the underlying change, the workflow does not have backwards compatibility built into it. The new workflow is:

1. Use an Alert Search to specify which Alerts will have their status updated.

    * The request body is a search request and all alerts matching the request will be updated.
    * Two common uses are to update one alert or to update all alerts that have a specific threat id.
    * Any search request can be used as the criteria to select alerts to update the alert status.

    .. code-block:: python

        >>> # This query selects only the alert that has the specified id:
        >>> ALERT_ID = "id of the alert to close"
        >>> alert_query = api.select(Alert).add_criteria("id", [ALERT_ID])
        >>> # This query selects all alerts that have the specified threat id.  It is not used again in this example
        >>> alert_query_for_threat = api.select(Alert).add_criteria("threat_id","CFED0B211ED09F8EC1C83D4F3FBF1709")

2. Submit a job to update the status of Alerts.

    * The status can be ``OPEN``, ``IN PROGRESS`` or ``CLOSED`` (previously ``DISMISSED``).
    * You can include a Closure Reason.

    .. code-block:: python
        >>> # by calling update on the alert_query, a request to change the status
        >>> # all alerts matching that criteria will be submitted
        >>> job = alert_query.update("CLOSED", "RESOLVED", "NONE", "Setting to closed for SDK demo")

3. The immediate response confirms that the job was successfully submitted.

    .. code-block:: python
        >>> print("job.id = {}".format(job.id))
        job.id = 1234567

4. Use the :py:mod:`Job() cbc_sdk.platform.jobs.Job` class to determine when the update is complete.

    Use the Job object to wait until the Job has completed.  Your python script will wait while
    the SDK manages the polling to determine when the job is complete.

    .. code-block:: python

        >>> job.await_completion().result()

5. Refresh the Alert Search to get the updated alert data into the SDK.

    .. code-block:: python

        >>> alert.refresh()
        >>> print("Status = {}, Expecting CLOSED".format(alert.workflow["status"]))

6. The Dismissal of Future Alerts for the same threat id has not changed.

    The following  sequence of calls updates future alerts that have the same threat id.  It is usually used in combination
    with the alert closure; that is, you can use it to dismiss future alerts call to close future occurrences and call
    alert closure to close current open alerts that have the threat id.

    .. code-block:: python

        >>> alert_threat_query = api.select(Alert).add_criteria("threat_id","CFED0B211ED09F8EC1C83D4F3FBF1709")
        >>> alert.dismiss_threat("threat remediation done", "testing dismiss_threat in the SDK")
        >>> # To undo the dismissal, call update
        >>> alert.update_threat("threat remediation un-done", "testing update_threat in the SDK")

create_note() Return Type
^^^^^^^^^^^^^^^^^^^^^^^^^

``alert.create_note()`` returns a Note object instead of a list.

.. code-block:: python

    >>> alert_query = api.select(Alert)
    >>> alert = alert_query.first()
    >>> new_note = alert.create_note("Adding note from SDK with current timestamp: {}".format(time.time()))
    >>> print(type(new_note))
    <class 'cbc_sdk.platform.alerts.Alert.Note'>

Backwards Compatibility
-----------------------
The following changes have code in the SDK to map updated functionality to previous SDK functions. The SDK will continue
to work, but new features should be reviewed to enhance integration and automation.

The "Example Method" refers to the example script `alert_v6_v7_migration.py in GitHub
<https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

Class Name Changes
^^^^^^^^^^^^^^^^^^
* The base class for Alerts in the SDK has changed from ``BaseAlert`` to ``Alert``.

    * Backwards compatibility is retained.
    * Example method: ``base_class_and_default_time_range(api)``.

Field Names Aliased
^^^^^^^^^^^^^^^^^^^

To align with other parts of Carbon Black Cloud and industry conventions, many fields were deprecated
from Alerts API v6 and have equivalent fields using a different name in v7. In the SDK v1.5.0, aliases are in place
to minimize breaks.

Details of all changes to API endpoints and fields are in the
`Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_ on the Developer Network.

``set_<v6 field name>()`` on the query object translates to the new field name for the request.

    * Update to use `add_criteria(field_name, [field_value]).
    * You can use many new fields in criteria to search Alerts using add_criteria,
      but do not have set_<field_name> methods.
    * Example method: ``set_methods_backwards_compatibility(api)``.

``get(<v6 field name>)`` translates to the new field name to look up the value.

    * Example method: ``get_methods_backwards_compatibility(api)``.

``alert.field_name`` translates the field name to the new name and returns the matching value.

    * Example method: ``set_methods_backwards_compatibility(api)``.

The following fields have a new name in Alert v7 and the new field name contains the same value.

.. list-table:: Field mappings where the field has been renamed
   :widths: 50, 50
   :header-rows: 1
   :class: longtable

   * - Alert v6 API - SDK 1.4.3 or earlier
     - Alert v7 API - SDK 1.5.0 or later
   * - cluster_name
     - k8s_cluster
   * - create_time
     - backend_timestamp
   * - first_event_time
     - first_event_timestamp
   * - last_event_time
     - last_event_timestamp
   * - last_update_time
     - backend_update_timestamp
   * - namespace
     - k8s_namespace
   * - notes_present
     - alert_notes_present
   * - policy_id
     - device_policy_id
   * - policy_name
     - device_policy
   * - port
     - netconn_local_port
   * - protocol
     - netconn_protocol
   * - remote_domain
     - netconn_remote_domain
   * - remote_ip
     - netconn_remote_ip
   * - remote_namespace
     - remote_k8s_namespace
   * - remote_replica_id
     - remote_k8s_pod_name
   * - remote_workload_kind
     - remote_k8s_kind
   * - remote_workload_name
     - remote_k8s_workload_name
   * - replica_id
     - k8s_pod_name
   * - rule_id
     - rule_id
   * - run_state
     - run_state
   * - target_value
     - device_target_value
   * - threat_cause_actor_certificate_authority
     - process_issuer
   * - threat_cause_actor_name
     - process_name. Note that `threat_cause_actor_name` was only the name of the executable. `process_name` contains the full path.
   * - threat_cause_actor_publisher
     - process_publisher
   * - threat_cause_actor_sha256
     - process_sha256
   * - threat_cause_cause_event_id
     - primary_event_id
   * - threat_cause_md5
     - process_md5
   * - threat_cause_parent_guid
     - parent_guid
   * - threat_cause_reputation
     - process_reputation
   * - threat_indicators
     - ttps
   * - watchlists
     - watchlists.id
   * - workflow.last_update_time
     - workflow.change_timestamp
   * - workload_kind
     - k8s_kind
   * - workload_name
     - k8s_workload_name

Port - split into local and remote
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* In SDK 1.4.3 and earlier, there was a single field ``port``.
* In Alerts v7 API and SDK 1.5.0, there are two fields; ``netconn_local_port`` and ``netconn_remote_port``.
* The legacy method set_ports() sets the criteria for ``netconn_local_port``.

.. code-block:: python

    >>> # This legacy search request:
    >>> api.select(BaseAlert).set_ports(["NON_MALWARE"])
