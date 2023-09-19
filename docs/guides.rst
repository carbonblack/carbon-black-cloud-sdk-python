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

Certain guides may be more geared towards audiences with more experience with the Carbon Black Cloud, such as
administrators.

Feature Guides
--------------
.. toctree::
   :maxdepth: 2

   searching
   alerts
   audit-log
   developing-credential-providers
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
* :doc:`audit-log` - Retrieve audit log events indicating various "system" events.
* :doc:`device-control` - Control the blocking of USB devices on endpoints.
* :doc:`differential-analysis` - Provides the ability to compare and understand the changes between two Live Query runs
* :doc:`live-query` - Live Query allows operators to ask questions of endpoints
* :doc:`live-response` - Live Response allows security operators to collect information and take action on remote endpoints in real time.
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

   porting-guide
   live-response-v6-migration
