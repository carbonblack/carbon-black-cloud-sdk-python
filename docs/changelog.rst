Changelog
================================

CBC SDK 1.2.0 - Released March 9, 2021
--------------------------------------

New Features

* VMware Carbon Black Cloud Workload support for managing workloads:

  * Appliance Installation
  * Sensor Lifecycle Management
  * VM Workloads Search

* Add tutorial for Reputation Override

Bug Fixes

* Fix to initialization of ReputationOverride objects

CBC SDK 1.1.1 - Released February 2, 2021
-----------------------------------------

New Features

* Add easy way to add single approvals and blocks
* Add Device Control Alerts
* Add deployment_type support to the Device model

Bug Fixes

* Fix error when updating iocs in a Report model
* Set max_retries to None to use Connection init logic for retries


CBC SDK 1.1.0 - Released January 27, 2021
------------------------------------

New Features

* Reputation Overrides for Endpoint Standard with Enterprise EDR support coming soon
* Device Control for Endpoint Standard
* Live Query Templates/Scheduled Runs and Template History
* Add set_time_range for Alert query

Bug Fixes

* Refactored code base to reduce query inheritance complexity
* Limit Live Query results to 10k cap to prevent 400 Bad Request
* Add missing criteria for Live Query RunHistory to search on template ids
* Add missing args.orgkey to get_cb_cloud_object to prevent exception from being thrown
* Refactor add and update criteria to use CriteriaBuilderSupportMixin

CBC SDK 1.0.1 - Released December 17, 2020
------------------------------------

Bug Fixes

* Fix readme links
* Few ReadTheDocs fixes

CBC SDK 1.0.0 - Released December 16, 2020
------------------------------------

New Features

* Enriched Event searches for Endpoint Standard
* Aggregation search added for Enriched Event Query
* Add support for fetching additional details for an Enriched Event
* Facet query support for Enriched Events, Processes, and Process Events
* Addition of Python Futures to support asynchronous calls for customers who want to leverage that feature , while continuing to also provide the simplified experience which hides the multiple calls required.
* Added translation support for MISP threat intel to cbc_sdk threat intel example

Updates

* Improved information and extra calls for Audit and Remediation (Live Query)
* Great test coverage – create extensions and submit PRs with confidence
* Process and Process Event searches updated to latest APIs and moved to platform package
* Flake8 formatting applied to all areas of the code
* Converted old docstrings to use google format docstrings
* Migrated STIX/TAXII Threat Intel module from cbapi to cbc_sdk examples

Bug Fixes

* Fixed off by one error for process event pagination
* Added support for default profile using CBCloudAPI()
* Retry limit to Process Event search to prevent infinite loop
