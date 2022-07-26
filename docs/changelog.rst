Changelog
================================
CBC SDK 1.4.0 - Released July 26,2022
-------------------------------------

**Breaking Changes:**

* ``Policy`` object has been moved from ``cbc_sdk.endpoint_standard`` to ``cbc_sdk.platform``, as it now uses the new
  Policy Services API rather than the old APIs through Integration Services.

  - **N.B.:** This change means that you *must* use a custom API key with permissions under ``org.policies`` to manage
    policies, rather than an older "API key."
  - To enable time to update integration logic, the ``cbc_sdk.endpoint_standard Policy`` object may still be imported
    from the old package, and supports operations that are backwards-compatible with the old one.
  - When developing a new integration, or updating an existing one cbc_sdk.platform should be used. There is a utility
    class ``PolicyBuilder``, and as features are added to the Carbon Black Cloud, they will be added to this module.

* Official support for Python 3.6 has been dropped, since that version is now end-of-life.  Added explicit testing
  support for Python versions 3.9 and 3.10.  **N.B.:** End users should update their Python version to 3.7.x or
  greater.

New Features:

* Credentials handler now supports OAuth tokens.
* Added support for querying a single ``Report`` from a ``Feed``.
* Added support for alert notes (create, delete, get, refresh).

Updates:

* Removed the (unused) ``revoked`` property from ``Grant`` objects.
* Increased the asynchronous query thread pool to 3 threads by default.
* Required version of ``lxml`` is now 4.9.1.
* Added a user acceptance test script for Alerts.

Bug Fixes:

* Added ``max_rows`` to USB device query, fixing pagination.
* Fixed an off-by-one error in Alerts Search resulting un duplicate alerts showing up in results.
* Fixed an error in alert faceting operations due to sending excess input to the server.

Documentation:

* Watchlists, Feeds, and Reports guide has been updated with additional clarification and examples.
* Updated description for some ``Device`` fields that are never populated.
* Additional sensor states added to ``Device`` documentation.
* Fixed the description of ``BaseAlertSearchQuery.set_types`` so that it mentions all valid alert types.
* Threat intelligence example has been deprecated.

CBC SDK 1.3.6 - Released April 19, 2022
---------------------------------------

New Features:

* Support for Device Facet API.
* Dynamic reference of query classes--now you can do ``api.select("Device")`` in addition to ``api.select(Device)``.
* Support for Container Runtime Alerts.
* NSX Remediation functionality - set the NSX remediation state for workloads which support it.

Updates:

* Endpoint Standard specific ``Event``s have been decommissioned and removed.
* SDK now uses Watchlist Manager apis ``v3`` instead of ``v2``.  ``v2`` APIs are being decommissioned.

Documentation:

* Added a ``CONTRIBUTING`` link to the ``README.md`` file.
* Change to Watchlist/Report documentation to properly reflect how to update a ``Report`` in a ``Watchlist``.
* Cleaned up formatting.

CBC SDK 1.3.5 - Released January 26, 2022
-----------------------------------------

New Features:

* Added asynchronous query support to Live Query.
* Added the ability to export query results from Live Query, either synchronously or asynchronously (via the ``Job``
  object and the Jobs API).  Synchronous exports include full-file export, line-by-line export, and ZIP file export.
  Asynchronous exports include full-file export and line-by-line export.
* Added a ``CredentialProvider`` that uses AWS Secrets Manager to store credential information.

Updates:

* Added ``WatchlistAlert.get_process()`` method to return the ``Process`` of a ``WatchlistAlert``.
* Added several helpers to Live Query support to make it easier to get runs from a template, or results, device
  summaries, or facets from a run.
* Optimized API requests when performing query slicing.
* Updated pretty-printing of objects containing ``dict`` members.
* ``lxml`` dependency updated to version 4.6.5.

Bug Fixes:

* ``User.delete()`` now checks for an outstanding access grant on the user, and deletes it first if it exists.
* Fixed handling of URL when attaching a new IOC to a ``Feed``.
* Getting and setting of ``Report`` ignore status is now supported even if that ``Report`` is part of a ``Feed``.

Documentation:

* Information added about the target audience for the SDK.
* Improper reference to a credential property replaced in the Authentication guide.
* Broken example updated in Authentication guide.
* Added SDK guides for Vulnerabilities and Live Query APIs.
* Updated documentation for ``ProcessFacet`` model to better indicate support for full query string.

CBC SDK 1.3.4 - Released October 12, 2021
-----------------------------------------

New Features:

* New CredentialProvider supporting Keychain storage of credentials (Mac OS only).
* Recommendations API - suggested reputation overrides for policy configuration.

Updates:

* Improved string representation of objects through ``__str__()`` mechanism.

Bug Fixes:

* Ensure proper ``TimeoutError`` is raised in several places where the wrong exception was being raised.
* Fix to allowed categories when performing alert queries.

Documentation Changes:

* Added guide page for alerts.
* Live Response documentation updated to note use of custom API keys.
* Clarified query examples in Concepts.
* Note that vulnerability assessment has been moved from ``workload`` to ``platform.``
* Small typo fixes in watchlists, feeds, UBS, and reports guide.

CBC SDK 1.3.3 - Released August 10, 2021
----------------------------------------

Bug Fixes:

* Dependency fix on schema library.

CBC SDK 1.3.2 - Released August 10, 2021
----------------------------------------

New Features:

* Added asynchronous query options to Live Response APIs.
* Added functionality for Watchlists, Reports, and Feeds to simplify developer interaction.

Updates:

* Added documentation on the mapping between permissions and Live Response commands.

Bug Fixes:

* Fixed an error using the STIX/TAXII example with Cabby.
* Fixed a potential infinite loop in getting detailed search results for enriched events and processes.
* Comparison now case-insensitive on UBS download.

CBC SDK 1.3.1 - Released June 15, 2021
--------------------------------------

New Features:

* Allow the SDK to accept a pre-configured ``Session`` object to be used for access, to get around unusual configuration requirements.

Bug Fixes:

* Fix functions in ``Grant`` object for adding a new access profile to a user access grant.

CBC SDK 1.3.0 - Released June 8, 2021
-------------------------------------

New Features

* Add User Management, Grants, Access Profiles, Permitted Roles
* Move Vulnerability models to Platform package in preparation for supporting Endpoints and Workloads
* Refactor Vulnerability models

  * ``VulnerabilitySummary.get_org_vulnerability_summary`` static function changed to ``Vulnerability.OrgSummary`` model with query class
  * ``VulnerabilitySummary`` model moved inside ``Vulnerability`` to ``Vulnerability.AssetView`` sub model
  * ``OrganizationalVulnerability`` and ``Vulnerability`` consolidated into a single model to include Carbon Black Cloud context and CVE information together
  * ``Vulnerability(cb, CVE_ID)`` returns Carbon Black Cloud context and CVE information
  * ``DeviceVulnerability.get_vulnerability_summary_per_device`` static function moved to ``get_vulnerability_summary`` function on ``Device`` model
  * ``affected_assets(os_product_id)`` function changed to ``get_affected_assets()`` function and no longer requires ``os_product_id``

* Add dashboard export examples
* Live Response migrated from v3 to v6 (:doc:`migration guide<live-response-v6-migration>`)

  * Live Response uses API Keys of type Custom

* Add function to get Enriched Events for Alert

Bug Fixes

* Fix validate query from dropping sort_by for Query class
* Fix the ability to set expiration for binary download URL
* Fix bug in helpers read_iocs functionality
* Fix install_sensor and bulk_install on ComputeResource to use id instead of uuid
* Fix DeviceSearchQuery from duplicating Device due to base index of 1

CBC SDK 1.2.3 - Released April 19, 2021
---------------------------------------

Bug Fixes

* Prevent alert query from retrieving past 10k limit

CBC SDK 1.2.3 - Released April 19, 2021
---------------------------------------

Bug Fixes

* Prevent alert query from retrieving past 10k limit

CBC SDK 1.2.2 - Released April 5, 2021
---------------------------------------

Bug Fixes

* Add support for full credential property loading through BaseAPI constructor


CBC SDK 1.2.1 - Released March 31, 2021
---------------------------------------

New Features

* Add `__str__` functions for Process.Tree and Process.Summary
* Add `get_details` for Process
* Add  `set_max_rows` to DeviceQuery

Bug Fixes

* Modify base class for EnrichedEventQuery to Query from cbc_sdk.base to support entire feature set for searching
* Document fixes for changelog and Workload
* Fix `_spawn_new_workers` to correctly find active devices for Carbon Black Cloud



CBC SDK 1.2.0 - Released March 9, 2021
--------------------------------------

New Features

* VMware Carbon Black Cloud Workload support for managing workloads:

  * Vulnerability Assessment
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
-----------------------------------------

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
------------------------------------------

Bug Fixes

* Fix readme links
* Few ReadTheDocs fixes

CBC SDK 1.0.0 - Released December 16, 2020
------------------------------------------

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
