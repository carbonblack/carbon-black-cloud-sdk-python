Alert Migration
===============

TO DO items:
* Add links to RTD sections
* set_ports sets netconn_local_ports. 
Note that in SDK 1.5.0, to align with Alerts API v7, the search field was updated from
        `port` to `netconn_local_port`.  It is possible to search on either `netconn_local_port`
        or `netconn_remote_port` using the `add_criteria(fieldname, [field values]) method.


This guide will help you update from SDK v1.4.3 or earlier which used Alerts v6 API to
SDK v1.5.0 or later which has been updated to use the Alerts v7 API.

We recommend that customers evaluate the new fields available in Alerts v7 API, and supported in SDK 1.5.0 onwards,
to maximise benefit from the new data. There is a lot of new metadata included in the Alert record, and you may be able
to simplify your integration.  For example, if you were previously getting process information to enrich the command
line, this will not be needed as the process commandline is included in the Alert record.

Resources
^^^^^^^^^

* `Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_
* `Alerts v7 Announcement <https://developer.carbonblack.com/2023/06/announcing-vmware-carbon-black-cloud-alerts-v7-api/>`_
* `Alert Search and Response Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields>`_

Attributes that have been renamed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This section outlines the fields that were deprecated from Alerts API v6 to v7 and the behaviour of this SDK.

Detail of all changes to API endpoints and fields are on the Developer Network in the
`Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_.

The following fields have a new name in Alert v7 and the new field name contains the same value.

Backwards compatibility has been built in such that calling legacy `set_<v6 field name>()` methods on the query object
and `get(<v6 field name>)` will return the expected results.


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
     - process_name. Note that `threat_cause_actor_name` was only the name of the executable.  `process_name` contains the full path.
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
     - k8s_workload_name"


Attributes that have been removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following attributes do not have an equivalent in Alert v7 API. If they are accessed using the
legacy *set_<v6 field name>()* methods on the query object or *get(<v6 field name>)* a
`FunctionalityDecommissioned` exception will be raised.

This code block which calls the decommissioned method set_blocked_threat_categories:

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alert_list = api.select(BaseAlert).set_blocked_threat_categories(["NON_MALWARE"])


Will generate the following exception:

.. code-block:: python

    cbc_sdk.errors.FunctionalityDecommissioned: The set_kill_chain_statuses method does not exist in in SDK v1.5.0
    because kill_chain_status is not a valid field on Alert v7 API.  The functionality has been decommissioned.


Similarly this code block which calls the get attribute function with the decommissioned attribute, blocked_threat_categories:

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alert_list = api.select(BaseAlert)
    >>> alert = alert_list.first()
    >>> alert.get("blocked_threat_category")


Will generate the following exception:

.. code-block:: python

    cbc_sdk.errors.FunctionalityDecommissioned:
    The Attribute 'blocked_threat_category' does not exist in object 'WatchlistAlert' because it was
    deprecated in Alerts v7. In SDK 1.5.0 the functionality has been decommissioned.


Deprecated Fields on CB Analytics Alerts:

* blocked_threat_category
* category
* group_details
* kill_chain_status
* not_blocked_threat_category
* threat_activity_dlp
* threat_activity_phish
* threat_cause_threat_category
* threat_cause_vector

Deprecated Fields on Watchlist Alerts

* category
* count
* document_guid
* group_details
* threat_cause_threat_category
* threat_cause_vector
* threat_indicators

Deprecated Fields on Device Control Alerts

* category
* group_details
* threat_cause_threat_category
* threat_cause_vector

Deprecated Fields on Container Runtime Alerts

* category
* group_details
* target_value
* threat_cause_threat_category
* workload_id

Deprecated Fields on Host Based Firewall Alerts

* category
* group_details
* threat_cause_threat_category

Workflow has changed significantly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The workflow feature for bulk closure of Alerts has changed significantly. The workflow fields do not have
backwards compatibility built in.  The new workflow is:

TO DO ADD EXAMPLE AFTER CHANGE IS IMPLEMENTED

#. Submit a job to update the status of Alerts.

    The request body is a search request and all alerts matching the request will be updated

    The status can be `OPEN`, `IN PROGRESS` or `CLOSED` (previously `DISMISSED`)

#. A Closure Reason may be included

#. The immediate API response confirms the job was successfully submitted

#. Use the Alert Search to see updated status of an alert

Helper Functions that have been removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CBAnalytics get_events() has been removed

* The Enriched Events that this method returns have been deprecated
* Instead, use `Observations <https://developer.carbonblack.com/2023/07/how-to-take-advantage-of-the-new-observations-api/>`_
* More information is on the Developer Network Blog, `How to Take Advantage of the New Observations API <https://developer.carbonblack.com/2023/07/how-to-take-advantage-of-the-new-observations-api/>`_

Instead of:

.. code-block:: python

    >>> cb = get_cb_cloud_object(args)
    >>> alert_list = cb.select(CBAnalyticsAlert)
    >>> alert = alert_list.first()
    >>> alert.get_events()

Use: TO DO VERIFY THIS IS ACCURATE AFTER get_observations is implemented.

.. code-block:: python

    >>> cb = get_cb_cloud_object(args)
    >>> alert_list = cb.select(Alert)
    >>> alert = alert_list.first()
    >>> alert.get_observations()


Also note that Observations can be retrieved for any type of Alert. It is not limited to CB Analytics Alerts.

New Helper Functions
^^^^^^^^^^^^^^^^^^^^

to_json(version)

* Should be used instead of accessing `_info` directly
* This is a new method that returns the json representation of the alert
* It defaults to the current API version, v7.
* "v6" can be passed as a parameter and the attribute names will be translated to the Alert v6 names
* It is intended to ease the update path if the `_info` attribute was being used.

.. code-block:: python

    >>> cb = get_cb_cloud_object(args)
    >>> alert_list = cb.select(Alert)
    >>> alert = alert_list.first()
    >>> v7_dict = alert.to_json()
    >>> v6_dict = alert.to_json("v6")

The returned object v7_dict will have a dictionary representation of the alert using v7 attribute names and structure.

The returned object v6_dict will have a dictionary representation of the alert using v6 attribute names and structure.
If the field does not exist in v7, then the field will also be missing from the json representation.
