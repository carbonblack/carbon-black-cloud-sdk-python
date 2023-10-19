Alerts
======

Use alerts to get notifications about important App Control-monitored activities, such as the
appearance or spread of risky files on your endpoints. The Carbon Black Cloud Python SDK provides
all of the functionalities you might need to use them efficiently.
You can use all of the operations shown in the API such as retrieving, filtering, closing, and adding notes to the
alert or the associated threat.
The full list of operations and attributes can be found in the :py:mod:`Alert() <cbc_sdk.platform.alerts.Alert>` class.

Resources
---------
* `API Documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/>`_ on Developer Network
* `Alert Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_ on Developer Network
* Example script in `GitHub <https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/develop/examples/platform>`_
* If you are updating from SDK version 1.4.3 or earlier, see the `alerts-migration`_ guide.

.. note::
    In Alerts v7, and therefore SDK 1.5.0 onwards, Observed Alerts are not emitted as an Alert. The field ``category``
    has been removed from Alert.  In other APIs where this field remains it will always have a value of ``THREAT``.
    More information is available
    `here <https://carbonblack.vmware.com/blog/announcing-alerts-v7-api-and-%E2%80%9Cobserved-alerts%E2%80%9D-become-%E2%80%9Cobservations%E2%80%9D>`_.

Retrieving of Alerts
--------------------

With the example below, you can retrieve the last 5 ``[:5]`` alerts with the minimum severity of ``7``.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(Alert).set_minimum_severity(7)[:5]
    >>> print(alerts[0].id, alerts[0].device_os, alerts[0].device_name, alerts[0].category)
    d689e626-5d6a-<truncated> WINDOWS Alert-WinTest THREAT


Filtering
^^^^^^^^^

Filter alerts using the fields described in the
`Alert Search Schema <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_.

Use the ``add_criteria()`` method to limit the alerts by setting required values for specific fields.  This should be
used for fields identified in the `Alert Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_
with "Searchable Array".
This snippet shows limiting to specific devices where the device_id is an integer, and then the device_target_value
which is a string.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(Alert).add_criteria("device_id", [123, 456])
    >>> alerts = api.select(Alert).add_criteria("device_target_value", ["MISSION_CRITICAL", "HIGH"])


Fields in the `Alert Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_
identified only with "Searchable" require the criteria to be a single value instead of a list of values.
The SDK has hand crafted methods to set the criteria for these fields.

The code snippet shows the methods for ``alert_notes_present`` and ``set_minimum_severity`` and the different number of
alerts that meet each criteria.

.. code-block:: python

    >>> alerts = api.select(Alert).set_alert_notes_present(True)
    >>> print(len(alerts))
    3
    >>> alerts = api.select(Alert).set_minimum_severity(9)
    >>> print(len(alerts))
    1072
    >>> alerts = api.select(Alert).set_minimum_severity(3)
    >>> print(len(alerts))
    69100
    >>>


You can also use the ``where`` method to filter the alerts. The ``where`` supports strings and solr like queries, alternatively you can use the ``solrq`` query objects
for more complex searches. The example below will search with a solr query search string for alerts
where the device_target_value is MISSION_CRITICAL or HIGH, and is the equivalent of the add_criteria clause above.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(Alert).where("device_target_value:MISSION_CRITICAL or device_target_value:HIGH")
    >>> for alert in alerts:
    ...     print(alert.id, alert.device_os, alert.device_name, alert.device_target_value)
    8aa6272a-17cb-31c0-9352-67e45c0251f3 WINDOWS jenkin MISSION_CRITICAL
    d987a112-8b7b-18c9-43d9-76ced09d9ded WINDOWS MYDEMOMACHINE\DESKTOP-04 MISSION_CRITICAL
    0f915c4d-5652-b3e5-50d8-f4dcfc632396 WINDOWS jenkin MISSION_CRITICAL
    1f13e581-840f-1207-f661-d9b176ee9d6c WINDOWS jenkin MISSION_CRITICAL
    6ae56007-1213-4ee1-a50c-d221066ce8c9 WINDOWS MYBUILDMACHINE\Desktop-01 HIGH
    ... truncated ...

.. tip::
    When filtering by fields that take a list parameter, an empty list will be treated as a wildcard and match everything.

For example, this snippet returns all types:

.. code-block:: python

    >>> alerts = cb.select(Alert).set_types([])

And it is equivalent to:
    >>> alerts = cb.select(Alert)

.. tip::
    More information about the ``solrq`` can be found in
    their `documentation <https://solrq.readthedocs.io/en/latest/index.html>`_.

Retrieving Alerts for Multiple Organizations
--------------------------------------------

With the example below, you can retrieve alerts for multiple organizations.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> org_list = ["org1", "org2"]
    >>> for org in org_list:
    ...     org = "".join(org)
    ...     api = CBCloudAPI(profile=org)
    ...     alerts = api.select(Alert).set_minimum_severity(7)[:5]
    ...     print("Results for Org {}".format(org))
    >>> for alert in alerts:
    ...     print(alert.id, alert.device_os, alert.device_name, alert.category)
    ...
    ...


You can also read from a csv file with values that match the profile names in your credentials.cbc file.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> import csv
    >>> file = open ("data.csv", "r", encoding="utf-8-sig")
    >>> org_list = list(csv.reader(file, delimiter=","))
    >>> file.close()
    >>> for org in org_list:
    ...     org = "".join(org)
    ...     api = CBCloudAPI(profile=org)
    ...     alerts = api.select(Alert).set_minimum_severity(7)[:5]
    ...     print("Results for Org {}".format(org))
    >>> for alert in alerts:
    ...     print(alert.id, alert.device_os, alert.device_name, alert.category)
    ...
    ...

Retrieving Observations To Provide Context About An Alert
---------------------------------------------------------

All alert types other than Watchlist Alerts have Observations associated with them which provide more information
about the interesting events that contributed to the identification of an Alert.

The Alert v7 object (supported in SDK 1.5.0 onwards) has significantly more metadata when compared to the earlier
Alerts v6 API (in the SDK version 1.4.3 and earlier) so the enrichment may not be required depending on your use case.
New fields include process, child process and parent process commandlines and ip addresses for network events. Find the
complete list of fields in the
`Alert Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_

Observations are part of
`Investigate Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/platform-search-fields/>`_.
Available fields are identified by the route "Observation".
Methods on the Observation Class can be found here :py:mod:`Observation() <cbc_sdk.platform.observations.Observation>`

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import CBAnalyticsAlert
    >>> api = CBCloudAPI(profile="sample")
    >>> alert = api.select(Alert).add_criteria("type", "CB_ANALYTICS").first()
    >>> observations = alert.get_observations()
    >>> observations
    [<cbc_sdk.platform.observations.Observation: id a5aa40856d5511ee8059132eb84e1d6d:470147c9-d79b-3f01-2083-b30bc0c0629f> @ https://defense.conferdeploy.net]
    >>> print(observations[0].get_details())
    Observation object, bound to https://defense.conferdeploy.net.
    ------------------------------------------------------------------------------
                                 alert_id: [list:1 item]:
                                           [0]: 470147c9-d79b-3f01-2083-b30bc0c0629f
                        backend_timestamp: 2023-10-18T01:28:59.900Z
             blocked_effective_reputation: KNOWN_MALWARE
                             blocked_hash: [list:1 item]:
                                           [0]: 659e469f8dadcb6c32ab1641817ee57c327003dffa443c3...
                             blocked_name: c:\windows\system32\fltlib.dll
           childproc_effective_reputation: KNOWN_MALWARE
    childproc_effective_reputation_source: HASH_REP
                           childproc_hash: [list:1 item]:
                                           [0]: 659e469f8dadcb6c32ab1641817ee57c327003dffa443c3...
    ... truncated ...


Retrieving Processes To Provide Context About An Alert
------------------------------------------------------

You can retrieve process details on each ``WatchlistAlert`` and some other alert types using the example below. You can use list slicing
to retrieve the first ``n`` results, in the example below ``10``. The ``get_details()`` method would give us metadata
very similar to the one we've received by ``Observation``.
The full list of attributes and methods can be seen in the :py:mod:`Process() <cbc_sdk.platform.processes.Process>` class.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(WatchlistAlert)[:10]
    >>> for alert in alerts:
    ...     process = alert.get_process()
    ...     print(process.get_details())
    {'alert_id': ['0a3c45bf-fce6-4a63', '12030b8f-ce3f-48bd'], 'attack_tactic': 'TA0002' <truncated>..}
    {'alert_id': ['02f6aecd-73d7-456d', 'e47c13dd-75a9-44de'], 'attack_tactic': 'TA0002' <truncated>..}
    ... truncated ...

Get Process Events
^^^^^^^^^^^^^^^^^^

We could also fetch every event which corresponds with our Process, we can do so by calling ``process.events()``.

.. note::
    Since calling the events could be really intensive task in the example below we are fetching just the first ``10``
    events. Be careful when calling ``all()``.


.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> api = CBCloudAPI(profile='sample')
    >>> alert = api.select(WatchlistAlert).first()
    >>> process = alert.get_process()
    >>> events = process.events()[:10]
    >>> print(events[0].event_description) # Note that I've striped the `<share>` and `<link>` tags which are also available in the response.
    'The application c:\\program files (x86)\\google\\chrome\\application\\chrome.exe attempted to modify the memory of "c:\\program files (x86)\\google\\chrome\\application\\chrome.exe", by calling the function "NtWriteVirtualMemory". The operation was successful.'
    ...

Device Control Alerts
---------------------

The Device Control Alerts are explained in the :doc:`device-control` guide.

Container Runtime Alerts
------------------------

These represent alerts for behavior noticed inside a Kubernetes container, which are based on network traffic and are
triggered by anomalies from the learned behavior of workloads or applications.  For these events, the ``type`` will be
``CONTAINER_RUNTIME``.  Additional fields such as ``connection_type`` and ``egress_group_name`` are available.

Filter Alert Types Supported to CONTAINER_RUNTIME on the
`Alert Search Fields <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/>`_
to see all available fields.

Migrating from Notifications to Alerts
--------------------------------------

.. note::
    The Notifications API has been deprecated and deactivation is planned for October 31st 2024.

    Information about migrating from the API and alternative solutions are in the
    `IntegrationService notification v3 API Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/notification-migration/>`_

The notifications work on a subscription based principle and they require a ``SIEM`` key of authentication.
With that key you are subscribing to a certain criteria of alerts, note that as this is deprecated, new alert types
cannot be retrieved from the notifications API.

Please refer to `the official notes <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-defense/latest/rest-api/#get-notifications>`_ in the Carbon Black's API website.

.. image:: _static/cbc_platform_notification_edit.png
   :alt: Editing a notification in the CBC Platform
   :align: center

Those settings shown in the screenshot can be replicated with the following search criteria on Alerts:

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Alert
    >>> alerts = api.select(Alert).set_minimum_severity(7).\
    >>>     add_criteria("type", ["CB_ANALYTICS", "DEVICE_CONTROL"]).\
    >>>     add_criteria("device_policy", "Standard")


High Volume and Streaming Solution for Alerts
---------------------------------------------

If you want near-real-time streaming of alerts we advise you to refer to our `Data Forwarder <https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-E8D33F72-BABB-4157-A908-D8BBDB5AF349.html/>`_.
