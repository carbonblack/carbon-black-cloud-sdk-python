Porting Applications from CBAPI to Carbon Black Cloud SDK
=========================================================

This guide will help you migrate from CBAPI to the Carbon Black Cloud Python SDK.

This is necessary to take advantage of new functionality in Carbon Black Cloud and also to ensure
that functionality is not lost from your integrations when APIs are deactivated in July 2024.  Read more
about the new features in the `Developer Network Blogs <https://developer.carbonblack.com/blog/>`_.

.. note::

    CBAPI applications using Carbon Black EDR (Response) or Carbon Black App Control (Protection) cannot be ported,
    as support for on-premise products is not present in the CBC SDK. Continue to use CBAPI for these applications.

Overview
--------

CBC SDK has changes to package names, folder structure, and functions. Import statements will need to change for the
packages, modules, and functions listed in this guide.

Package Name Changes
--------------------

A number of packages have new name equivalents in the CBC SDK. Endpoint Standard and Enterprise EDR have had parts
replaced to use the most current API routes.

Top-level Package Name Change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The top-level package name has changed from CBAPI to CBC SDK.

+-----------------+--------------------+
| CBAPI Name (old)| CBC SDK Name (new) |
+=================+====================+
| ``cbapi.psc``   | ``cbc_sdk``        |
+-----------------+--------------------+

Product Name Changes
^^^^^^^^^^^^^^^^^^^^

Carbon Black Cloud product names have been updated in the SDK.

+----------------------------+-------------------------------+
| CBAPI Name (old)           | CBC SDK Name (new)            |
+============================+===============================+
| ``cbapi.psc.defense``      | ``cbc_sdk.endpoint_standard`` |
+----------------------------+-------------------------------+
| ``cbapi.psc.livequery``    | ``cbc_sdk.audit_remediation`` |
+----------------------------+-------------------------------+
| ``cbapi.psc.threathunter`` | ``cbc_sdk.enterprise_edr``    |
+----------------------------+-------------------------------+
| ``cbapi.psc``              | ``cbc_sdk.platform``          |
+----------------------------+-------------------------------+

Features for new products such as Container Security and Workload Security have also been added in the appropriate
namespace.

APIs that have been deprecated or deactivated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some modules made use of APIs that have been deactivated and are either no longer included in the Carbon Black Cloud,
or are planned for deprecation in the second half of 2024.  The following table shows
the original module, the replacement module, and where to find more information.

For a complete list of APIs that are deprecated and the associated migration information, see the
`Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/api-migration/>`_ on the
Developer Network.  This is important if you have integrations with Carbon Black Cloud that do not use the
Carbon Black Cloud Python SDK (this).

.. list-table:: Deprecated Modules and their replacements
   :widths: 25, 25, 50
   :header-rows: 1
   :class: longtable

   * - CBAPI module
     - Replacement CBC SDK Module
     - More Information
   * - cbapi.psc.defense Event
     - cbc_sdk.platform Observation
     - This was deactivated in January 2021. Review the Carbon Black Cloud User Guide to learn more about `Observations <https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-5EAF4BA6-601C-46AD-BA8E-D0BD05681ADF.html/>`_
   * - cbapi.psc.defense Policy
     - cbc_sdk.platform Policy
     - `IntegrationServices Policy v3 API Migration <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/policy-migration/>`_
   * - cbc_sdk.endpoint_standard EnrichedEvent
     - cbc_sdk.platform Observation
     - Enriched Events will remain available until July 2024. `Enriched Events API Migration <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/observations-migration/>`_
   * - cbc_sdk.platform Alert
     - Module path is unchanged. Attributes and methods will change
     - In SDK 1.5.0 the Alert module will be updated to use the new Alert v7 API.  A migration guide will be included with that release. Planned for October 2023.
   * - SIEM Notifications - cbc_sdk.rest_api CBCloudAPI get_notifications()
     - cbc_sdk.platform Alert or Alert Data Forwarder
     - `Notification Migration <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/notification-migration/>`_

Modules that have been moved and need new import statements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Import statements will need to change::

    # Endpoint Standard (Defense)

    # CBAPI
    from cbapi.psc.defense import Device

    # CBC SDK
    from cbc_sdk.platform import Device


    # Audit and Remediation (LiveQuery)

    # CBAPI
    from cbapi.psc.livequery import Run, RunHistory, Result, DeviceSummary

    # CBC SDK
    from cbc_sdk.audit_remediation import Run, RunHistory, Result, DeviceSummary


    # Enterprise EDR (ThreatHunter)

    # CBAPI
    from cbapi.psc.threathunter import Feed, Report, Watchlist

    # CBC SDK
    from cbc_sdk.enterprise_edr import Feed, Report, Watchlist

Moved Packages and Models
^^^^^^^^^^^^^^^^^^^^^^^^^

Some modules have been moved to a more appropriate location.

+-----------------------------+------------------------------+
| CBAPI Name (old)            | CBC SDK Name (new)           |
+=============================+==============================+
| ``cbapi.example_helpers``   | ``cbc_sdk.helpers``          |
+-----------------------------+------------------------------+
| ``cbapi.psc.alerts_query``  | ``cbc_sdk.platform``         |
+-----------------------------+------------------------------+
| ``cbapi.psc.devices_query`` | ``cbc_sdk.platform``         |
+-----------------------------+------------------------------+

Import statements will need to change::

    # Example Helpers

    # CBAPI
    from cbapi.example_helpers import build_cli_parser

    # CBC SDK
    from cbc_sdk.helpers import build_cli_parser

    # Alerts

    # CBAPI
    from cbapi.psc.alerts_query import *

    # CBC SDK
    from cbc_sdk.platform import *

    # Devices

    # CBAPI
    from cbapi.psc.devices_query import *

    # CBC SDK
    from cbc_sdk.platform import *

Replaced Modules
^^^^^^^^^^^^^^^^

In 2020, Carbon Black Cloud APIs were updated to provide a more consistent search
experience.  Platform search replaced Endpoint Standard Event searching, and Enterprise EDR Process and Event
searching.

For help beyond import statement changes, check out these resources:

* `Unified Platform Experience: What to Expect`_
* `Migration Guide: Carbon Black Cloud Events API`_
* `Advanced Search Tips for Carbon Black Cloud Platform Search`_

.. _`Unified Platform Experience: What to Expect`: https://community.carbonblack.com/t5/Carbon-Black-Cloud-Discussions/Unified-Platform-Experience-What-to-Expect/m-p/95699#M666
.. _`Migration Guide: Carbon Black Cloud Events API`: https://community.carbonblack.com/t5/Developer-Relations/Migration-Guide-Carbon-Black-Cloud-Events-API/m-p/95915/thread-id/2519
.. _`Advanced Search Tips for Carbon Black Cloud Platform Search`: https://community.carbonblack.com/t5/Carbon-Black-Cloud-Knowledge/Advanced-search-tips-for-Carbon-Black-Cloud-Platform-Search/ta-p/93230

Endpoint Standard
"""""""""""""""""

Endpoint Standard Events have been replaced with Platform Observations and the old event functionality has been
decommissioned::

    # Endpoint Standard Enriched Events

    # CBAPI
    from cbapi.psc.defense import Event

    # CBC SDK - decommissioned--do not use
    from cbc_sdk.endpoint_standard import Event

    # CBC SDK - deprecated--stop using before July 31st 2024
    from cbc_sdk.endpoint_standard import EnrichedEvent

    # CBC SDK - Observations.  Use this!
    from cbc_sdk.platform import Observation

Enterprise EDR
""""""""""""""

Enterprise EDR Processes and Events have been removed and replaced with Platform Processes and Events::

    # Enterprise EDR Process and Event

    # CBAPI
    from cbapi.psc.threathunter import Process, Event

    # CBC SDK
    from cbc_sdk.platform import Process, Event

Folder Structure Changes
------------------------

The directory structure for the SDK has been refined compared to CBAPI.

* Addition of the Platform folder
* Removal of Response and Protection folders
* Consolidation of model objects and query objects
* Product-specific ``rest_api.py`` files replaced with package level ``rest_api.py``

  * ``from cbapi.psc.threathunter import CbThreatHunterAPI`` becomes ``from cbc_sdk import CBCloudAPI``, etc.

Directory Tree Changes
^^^^^^^^^^^^^^^^^^^^^^

In general, each module's ``models.py`` and ``query.py`` files were combined into their respective ``base.py`` files.

CBAPI had the following abbreviated folder structure::

    src
    └── cbapi
        └── psc
            ├── defense
            │   ├── models.py
            │   │   ├── Device
            │   │   ├── Event
            │   │   └── Policy
            │   └── rest_api.py
            │       └── CbDefenseAPI
            ├── livequery
            │   ├── models.py
            │   │   ├── Run
            │   │   ├── RunHistory
            │   │   ├── Result
            │   │   ├── ResultFacet
            │   │   ├── DeviceSummary
            │   │   └── DeviceSummaryFacet
            │   └── rest_api.py
            │       └── CbLiveQueryAPI
            └── threathunter
                ├── models.py
                │   ├── Process
                │   ├── Event
                │   ├── Tree
                │   ├── Feed
                │   ├── Report
                │   ├── IOC
                │   ├── IOC_V2
                │   ├── Watchlist
                │   ├── ReportSeverity
                │   ├── Binary
                │   └── Downloads
                └── rest_api.py
                    └── CbThreatHunterAPI

Each product had a ``models.py`` and ``rest_api.py`` file.

CBC SDK has the following abbreviated folder structure::

    src
    └── cbc_sdk
        ├── audit_remediation
        │   └── base.py
        │       ├── Run
        │       ├── RunHistory
        │       ├── Result
        │       ├── ResultFacet
        │       ├── DeviceSummary
        │       └── DeviceSummaryFacet
        ├── endpoint_standard
        │   └── base.py
        │       ├── Device
        │       ├── Event
        │       ├── Policy
        │       ├── EnrichedEvent
        │       └── EnrichedEventFacet
        ├── enterprise_edr
        │   ├── base.py
        │   ├── threat_intelligence.py
        │   │   ├── Watchlist
        │   │   ├── Feed
        │   │   ├── Report
        │   │   ├── ReportSeverity
        │   │   ├── IOC
        │   │   └── IOC_V2
        │   └── ubs.py
        │       ├── Binary
        │       └── Downloads
        └── platform
        │   ├── alerts.py
        │   │    ├── WatchlistAlert
        │   │    ├── CBAnalyticsAlert
        │   │    ├── Workflow
        │   │    └── WorkflowStatus
        │   ├── processes.py
        │   │    ├── Process
        │   │    ├── ProcessFacet
        │   ├── events.py
        │   │    ├── Event
        │   │    └── EventFacet
        │   └── devices.py
        │       └── Device
        └── rest_api.py
            └── CBCloudAPI.py

Now, each product has either a ``base.py`` file with all of its objects, or categorized files like
``platform.alerts.py`` and ``platform.devices.py``.  The package level ``rest_api.py`` replaced each product-specific
``rest_api.py`` file.

Function Changes
----------------

**Helper Functions:**

+--------------------------------------------------------+-------------------------------------------+
| CBAPI Name (old)                                       | CBC SDK Name (new)                        |
+========================================================+===========================================+
| ``cbapi.example_helpers.get_cb_defense_object()``      | ``cbc_sdk.helpers.get_cb_cloud_object()`` |
| ``cbapi.example_helpers.get_cb_livequery_object()``    |                                           |
| ``cbapi.example_helpers.get_cb_threathunter_object()`` |                                           |
| ``cbapi.example_helpers.get_cb_psc_object()``          |                                           |
+--------------------------------------------------------+-------------------------------------------+

**Audit and Remediation Queries:**

+--------------------------------------+-----------------------------------------------+
| CBAPI Name (old)                     | CBC SDK Name (new)                            |
+======================================+===============================================+
| ``cb.query(sql_query)``              | ``cb.select(Run).where(sql=sql_query)``       |
+--------------------------------------+-----------------------------------------------+
| ``cb.query_history(query_string)``   | ``cb.select(RunHistory).where(query_string)`` |
+--------------------------------------+-----------------------------------------------+
| ``cb.query(sql_query).policy_ids()`` | ``cb.select(Run).policy_id()``                |
+--------------------------------------+-----------------------------------------------+

**API Objects:**

+----------------------------------------------+------------------------+
| CBAPI Name (old)                             | CBC SDK Name (new)     |
+==============================================+========================+
| ``cbapi.psc.defense.CbDefenseAPI``           | ``cbc_sdk.CBCloudAPI`` |
| ``cbapi.psc.livequery.CbLiveQueryAPI``       |                        |
| ``cbapi.psc.threathunter.CbThreatHunterAPI`` |                        |
| ``cbapi.psc.CbPSCBaseAPI``                   |                        |
+----------------------------------------------+------------------------+
