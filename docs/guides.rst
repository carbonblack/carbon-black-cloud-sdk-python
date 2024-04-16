Guides
======

Here we've listed a collection of tutorials, recorded demonstrations and other resources we think will be useful
to get the most out of the Carbon Black Cloud Python SDK.

Audience for These Guides
-------------------------

In general, and unless otherwise indicated, these guides are directed at those that:

- Have a working knowledge of Python.
- Have a basic understanding of what the Carbon Black Cloud does, and its basic terminology such as events, alerts,
  and watchlists.
- Need information to update to new versions of the SDK when enhanced features are released.

Certain guides may be more geared towards audiences with more experience with the Carbon Black Cloud, such as
administrators.

Information about updating to new versions of the SDK to take advantage of new features in Carbon Black Cloud are
in `Migration Guides`_.

Feature Guides
--------------
.. toctree::
   :maxdepth: 2

   searching
   alerts
   asset-groups
   audit-log
   compliance
   developing-credential-providers
   devices
   device-control
   differential-analysis
   live-query
   live-response
   policy
   recommendations
   reputation-override
   unified-binary-store
   users-grants
   vulnerabilities
   watchlists-feeds-reports
   workload

* :doc:`searching` - Most operations in the SDK will require you to search for objects.
* :doc:`alerts` - Work and manage different types of alerts such as CB Analytics Alert, Watchlist Alerts and Device Control Alerts.
* :doc:`asset-groups` - Create and modify Asset Groups, and preview the impact changes to policy ranking or asset group definition will have.
* :doc:`alerts-migration` - Update from SDK 1.4.3 or earlier to SDK 1.5.0 or later to get the benefits of the Alerts v7 API.
* :doc:`audit-log` - Retrieve audit log events indicating various "system" events.
* :doc:`compliance` - Search and validate Compliance Benchmarks.
* :doc:`devices` - Search for, get information about, and act on endpoints.
* :doc:`device-control` - Control the blocking of USB devices on endpoints.
* :doc:`differential-analysis` - Provides the ability to compare and understand the changes between two Live Query runs
* :doc:`live-query` - Live Query allows operators to ask questions of endpoints
* :doc:`live-response` - Live Response allows security operators to collect information and take action on remote endpoints in real time.
* :doc:`notifications-migration` - Update from Notifications to Alerts in SDK 1.5.0 or later to get the benefits of the Alerts v7 API.
* :doc:`policy` - Use policies to define and prioritize rules for how applications can behave on groups of assets
* :doc:`recommendations` - Work with Endpoint Standard recommendations for reputation override.
* :doc:`reputation-override` - Manage reputation overrides for known applications, IT tools or certs.
* :doc:`unified-binary-store` - The unified binary store (UBS) is responsible for storing all binaries and corresponding metadata for those binaries.
* :doc:`users-grants` - Work with users and access grants.
* :doc:`vulnerabilities` - View asset (Endpoint or Workload) vulnerabilities to increase security visibility.
* :doc:`watchlists-feeds-reports` - Work with Enterprise EDR watchlists, feeds, reports, and Indicators of Compromise (IOCs).
* :doc:`workload` - Advanced protection purpose-built for securing modern workloads to reduce the attack surface and strengthen security posture.

Migration Guides
----------------
.. toctree::
   :maxdepth: 2

   alerts-migration
   live-response-v6-migration
   notifications-migration
   porting-guide
