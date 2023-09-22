Alert Migration: API v6 to v7, SDK v1.4.3 to v1.5.0
===================================================

TO DO items:
* Add links to RTD sections

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

+----------------------+--------------------+
| Alert v6 API         | Alert v7 API       |
| SDK 1.4.3 or earlier | SDK 1.5.0 or later |
+======================+====================+
| cluster_name | k8s_cluster |
| create_time | backend_timestamp |
| first_event_time | first_event_timestamp |
| last_event_time | last_event_timestamp |
| last_update_time | backend_update_timestamp |
| namespace | k8s_namespace |
| notes_present | alert_notes_present |
| policy_id | device_policy_id |
| policy_name | device_policy |
| port | netconn_local_port |
| protocol | netconn_protocol |
| remote_domain | netconn_remote_domain |
| remote_ip | netconn_remote_ip |
| remote_namespace | remote_k8s_namespace |
| remote_replica_id | remote_k8s_pod_name |
| remote_workload_kind | remote_k8s_kind |
| remote_workload_name | remote_k8s_workload_name |
| replica_id | k8s_pod_name |
| rule_id | rule_id  |
| run_state | run_state |
| target_value | device_target_value |
| threat_cause_actor_certificate_authority | process_issuer |
| threat_cause_actor_name | process_name |
|| Note that `threat_cause_actor_name` was only the name of the executable.  `process_name` contains the full path. |
| threat_cause_actor_publisher | process_publisher |
| threat_cause_actor_sha256 | process_sha256 |
| threat_cause_cause_event_id | primary_event_id |
| threat_cause_md5 | process_md5 |
| threat_cause_parent_guid | parent_guid |
| threat_cause_reputation | process_reputation |
| threat_indicators | ttps |
| watchlists | watchlists.id |
| workflow.last_update_time | workflow.change_timestamp |
| workload_kind | k8s_kind |
| workload_name | k8s_workload_name" |
+----------------------+--------------------+

Attributes that have been removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following attributes do not have an equivalent in Alert v7 API. If they are accessed using the
legacy set_`<v6 field name>()` methods on the query object or `get(<v6 field name>)` a
`FunctionalityDecommissioned` exception will be raised.

Fields on CB Analytics Alerts:
* blocked_threat_category
* category
* group_details
* kill_chain_status
* not_blocked_threat_category
* threat_activity_dlp
* threat_activity_phish
* threat_cause_threat_category
* threat_cause_vector

Fields on Watchlist Alerts
* category
* count
* document_guid
* group_details
* threat_cause_threat_category
* threat_cause_vector
* threat_indicators

Fields on Device Control Alerts
* category
* group_details
* threat_cause_threat_category
* threat_cause_vector

Fields on Container Runtime Alerts
* category
* group_details
* target_value
* threat_cause_threat_category
* workload_id

Fields on Host Based Firewall Alerts
* category
* group_details
* threat_cause_threat_category

Workflow has changed significantly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The workflow feature for bulk closure of Alerts has changed significantly. The workflow fields do not have
backwards compatibility built in.  The new workflow is:
1. Submit a job to update the status of Alerts.
    * The request body is a search request and all alerts matching the request will be updated
    * The status can be `OPEN`, `IN PROGRESS` or `CLOSED` (previously `DISMISSED`)
    * A Closure Reason may be included
2. The immediate API response confirms the job was successfully submiteed
3. Use the Alert Search to see updated status of an alert
The job is submitted. Bulk returns Success-the job was submitted, search Alerts to see results.


Helper Functions that have been removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CBAnalytics get_events() has been removed
* Because: the Enriched Events that this method returns have been deprecated
* Replaced with: Observations
* More information: Developer Network Blog, `How to Take Advantage of the New Observations API <https://developer.carbonblack.com/2023/07/how-to-take-advantage-of-the-new-observations-api/>`_

New Helper Functions
^^^^^^^^^^^^^^^^^^^^

to_json(version)
* Should be used instead of accessing `_info` directly
* This is a new method that returns the json representation of the alert
* It defaults to the current API version, v7.
* "v6" can be passed as a parameter and the attribute names will be translated to the Alert v6 names
* It is intended to ease the update path if the `_info` attribute was being used.
