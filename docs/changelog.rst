Changelog
================================

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
