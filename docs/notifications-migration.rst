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

.. _notifications-migration-guide:

Notifications to Alerts Migration
=================================

Use this guide to update from using ```get_notifications()```, which leverages the
```/integrationServices/v3/notification``` API to using Alerts in SDK v1.5.0 or higher with Alerts v7 API.

.. note::
    The /integrationServices/v3/notification API is deprecated, and deactivation is planned for 31 October 2024.

    The Access Level Type ```SIEM``` used to access the Notifications API is also deprecated. Deactivation of the legacy access level type ```SIEM``` is planned for 31 January 2025.

    For more information about migrating from the API and alternative solutions, see
    `IntegrationService notification v3 API Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/notification-migration/>`_


The key differences between Notifications and Alerts are:

* In Notifications, the criteria that defines when a notification is sent is defined in the Carbon Black Cloud console. When using the Alerts v7 API, the criteria is part of the API request

* Notifications work on a subscription-based principle and they require a SIEM authentication key.  By using that key, you are subscribing to a certain criteria of alerts.

* As the API Notification API is deprecated, new alert types such as Intrusion Detection System Alerts cannot be retrieved from the Notifications API.

* The Notifications endpoint is a read-once queue whereas the Alerts v7 is a search request. When calling the Alerts v7 API, the caller (your script) must manage state, keeping track of the timestamp of the last Alert retrieved and using that for the start timestamp on the next request. See the Alert Bulk Export guide for details on the polling algorithm.

We recommend that customers evaluate the new fields that are available in Alerts v7 API and supported in SDK 1.5.0 onwards
to maximize the benefits from the new data. A lot of new metadata is included in the Alert record that can help simplify your integration. For example, if you were previously getting process information to enrich the command
line, the process commandline is now included in the Alert record.

As at SDK 1.5.0, Notifications are deprecated and functional; there has not been a breaking change.
The underlying API will be deactivated on October 31, 2024 so you must move to Alerts in SDK 1.5.0 or newer which uses Alerts v7 API, or to the
`Data Forwarder <https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-E8D33F72-BABB-4157-A908-D8BBDB5AF349.html>`_ with Alert Schema 2.x before then.

Resources
---------

* `IntegrationServices Notification v3 API Migration <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/notification-migration/>`_
* `Carbon Black Cloud Syslog Connector 2.0 <https://developer.carbonblack.com/2023/10/announcing-the-carbon-black-cloud-syslog-connector-2.0.0-release/>`_
* `Alert Bulk Export <http://localhost:1313/reference/carbon-black-cloud/guides/alert-bulk-export/>`_
* `Alerts Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration>`_
* `Alerts v7 Announcement <https://developer.carbonblack.com/2023/06/announcing-vmware-carbon-black-cloud-alerts-v7-api/>`_
* `Alert Search and Response Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields>`_
* SDK 1.5.0 Alert Example Script `alerts_common_scenarios.py in GitHub Examples <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.
* Alerts Bulk Export Example Script `alerts_bulk_export.py in GitHub Examples <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

How to Update the SDK Usage
---------------------------

This screen shot shows the Notification configuration page in the Carbon Black Cloud console.

.. image:: _static/cbc_platform_notification_edit.png
   :alt: Editing a notification in the CBC Platform
   :align: center

You can replicate the settings shown in the screenshot by running the following search on Alerts:

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> alerts = api.select(Alert).set_minimum_severity(7).\
    >>>     add_criteria("type", ["CB_ANALYTICS", "DEVICE_CONTROL"]).\
    >>>     add_criteria("device_policy", "Standard")

An Alert contains a lot more information than a Notification, and most of the fields are available for searching.

The other modification required is that where the Notifications was a read one queue, Alerts are retrieved using a search.
An example script with the polling logic implemented is in the GitHub Repository, `alerts_bulk_export.py in GitHub Examples <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_.

There is also a guide to `Alert Bulk Export <http://localhost:1313/reference/carbon-black-cloud/guides/alert-bulk-export/>`_
on the developer network with a detailed explanation of the logic.
