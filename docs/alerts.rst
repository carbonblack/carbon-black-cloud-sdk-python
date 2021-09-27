Alerts
======

Alerts can be used to notify you about important App Control-monitored activities, such as the
appearance or spread of risky files on your endpoints. The Carbon Black Cloud Python SDK provides
all of the functionalities you might need to use them efficiently.
You can use all of the operations shown in the API such as retrieving, filtering, dismissing, creating and updating.
The full list of operations and attributes that are available and can be used, can be found in the :py:mod:`BaseAlert() <cbc_sdk.platform.alerts.BaseAlert>` class.

For more information see
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/>`_

Retrieving of Alerts
--------------------

In the example below we can retrieve alerts with the minimum severity of ``7``.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(BaseAlert).set_minimum_severity(7)[:5]
    >>> print(alerts[0].id, alerts[0].device_os, alerts[0].device_name, alerts[0].category)
    d689e626-5d6a-<truncated> WINDOWS Alert-WinTest THREAT


Filtering
^^^^^^^^^

Alerts can filtered, based on their fields. You can find more about those fields in the
`official API schemas <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/#alert-search>`_.

You can use the ``where`` method to filter the alerts. The ``where`` supports strings as well as ``solrq`` query objects
for more complex searches. The example below will search for alerts where the ``category`` would be
either ``THREAT`` or ``INFO``. The ``^2`` simply means that it would prioritize the alerts within the ``INFO`` category.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> from solrq import Q
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(BaseAlert).where((Q(category='INFO')^2) | Q(category='THREAT'))[:5]
    >>> for alert in alerts:
    ...     print(alert.id, alert.device_os, alert.device_name, alert.category)
    179a5c6f-e343-<truncated> WINDOWS TEST-WIN INFO
    c025b8ff-a8f4-<truncated> WINDOWS TEST-WIN INFO
    dfb26aa6-3d0a-<truncated> WINDOWS TEST-WIN THREAT
    b574dd6b-fc0f-<truncated> WINDOWS TEST-WIN THREAT
    99c7b1f9-6a11-<truncated> WINDOWS TEST-WIN THREAT

.. tip::
    More information about the ``solrq`` and what exactly those ``Q`` objects are doing can be found in the
    their `documentation <https://solrq.readthedocs.io/en/latest/index.html>`_.

We can also filter on different kind of **TTPs** (*Tools Techniques Procedures*) and *Policy Actions**.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(BaseAlert).where(ttp='UNKNOWN_APP', sensor_action='TERMINATE', policy_name='Standard')[:5]
    >>> for alert in alerts:
    ...     print(alert.original_document['threat_indicators'])
    [{'process_name': 'notepad.exe', 'sha256': '<truncated>', 'ttps': ['POLICY_TERMINATE', 'UNKNOWN_APP']}]
    [{'process_name': 'test_file.exe', 'sha256': '<truncated>', 'ttps': ['POLICY_DENY', 'POLICY_TERMINATE', 'UNKNOWN_APP']}]
    [{'process_name': 'notepad.exe', 'sha256': '<truncated>', 'ttps': ['POLICY_TERMINATE', 'UNKNOWN_APP']}]
    ...


Retrieving of Carbon Black Analytics Alerts (CBAnalyticsAlert)
--------------------------------------------------------------

The Carbon Black Analytics Alerts can retrieve us information about different events
which are related to our alerts. Those events contain metadata such as ``process_name`` and ``process_cmdline``.
The full list of all the attributes can be found in the
:py:mod:`EnrichedEvent() <cbc_sdk.endpoint_standard.base.EnrichedEvent>` class.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import CBAnalyticsAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alert = api.select(CBAnalyticsAlert).first()
    >>> events = alert.get_events()
    >>> events
    [<cbc_sdk.endpoint_standard.base.EnrichedEvent: id <truncated> @ https://<truncated>, <cbc_sdk.endpoint_standard.base.EnrichedEvent: id <truncated>> @ https://<truncated>, ...]
    >>> print(events[0].get_details())
    ...
    EnrichedEvent object, bound to <truncated>
    -------------------------------------------------------------------------------

              alert_category: ['OBSERVED']
                    alert_id: ['<truncated>']
         associated_alert_id: ['<truncated>']
           backend_timestamp: 2021-09-20T10:06:06.728Z
          device_external_ip: <truncated>
             device_group_id: 0
                   device_id: <truncated>
         device_installed_by: bit9qa
          device_internal_ip: <truncated>
             device_location: OFFSITE
                 device_name: <truncated>
                   device_os: WINDOWS
           device_os_version: Windows 10 x64
               device_policy: perf_events_do_not_delete_policy
            device_policy_id: <truncated>
        device_target_priority: MEDIUM
            device_timestamp: 2021-09-20T10:04:02.290Z
               document_guid: <truncated>
                    enriched: True
         enriched_event_type: NETWORK
           event_description: <truncated>
                    event_id: <truncated>
    event_network_inbound: False
    event_network_local_ipv4: <truncated>
    event_network_location: San Jose,CA,United States
    event_network_protocol: TCP
    event_network_remote_ipv4: <truncated>
    event_network_remote_port: <truncated>
       event_report_code: SUB_RPT_NONE
      event_threat_score: [0]
              event_type: netconn
            ingress_time: 1632132315179
                  legacy: True
          netconn_domain: <truncated>
         netconn_inbound: False
            netconn_ipv4: <truncated>
      netconn_local_ipv4: <truncated>
      netconn_local_port: <truncated>
        netconn_location: San Jose,CA,United States
            netconn_port: <truncated>
        netconn_protocol: PROTO_TCP
                  org_id: <truncated>
    parent_effective_reputation: LOCAL_WHITE
    parent_effective_reputation_source: CERT
             parent_guid: <truncated>-<truncated>-00000280-00000000-1d79a95c52...
             parent_hash: ['<truncated>...
             parent_name: c:\windows\system32\services.exe
              parent_pid: 640
       parent_reputation: NOT_LISTED
         process_cmdline: ['C:\\Windows\\System32\\svchost.exe -k utcsvc ...
    process_cmdline_length: [44]
    process_effective_reputation: TRUSTED_WHITE_LIST
    process_effective_reputation_source: APPROVED_DATABASE
            process_guid: <truncated>-<truncated>-00000b44-00000000-1d79a95c67...
            process_hash: ['<truncated>', '<truncated>...
            process_name: c:\windows\system32\svchost.exe
             process_pid: [2884]
      process_reputation: ADAPTIVE_WHITE_LIST
          process_sha256: <truncated>...
      process_start_time: 2021-08-26T6:16:50.162Z
        process_username: ['NT AUTHORITY\\SYSTEM']
      triggered_alert_id: ['<truncated>-<truncated>-8af4-d6d0-e4bbe7917dff']
                     ttp: ['PORTSCAN', 'MITRE_T1046_NETWORK_SERVICE_SCANN...
    ...


Watchlist Alerts
----------------

Process Details
^^^^^^^^^^^^^^^

You can retrieve each process details on each ``WatchlistAlert`` by using the example below. You can use list slicing
to retrieve the first ``n`` results, in the example below ``10``. The ``get_details()`` method would give us metadata
very similar to the one we've received by ``EnrichedEvent``.
The full list of attributes and methods can be seen in the :py:mod:`Process() <cbc_sdk.platform.processes.Process>` class.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(WatchlistAlert)[:10]
    >>> for alert in alerts:
    ...     process = api.select(Process).where(process_guid=alert.original_document['process_guid']).first()
    ...     print(process.get_details())
    {'alert_category': ['OBSERVED', 'THREAT'], 'alert_id': ['06eca427-1e64-424<truncated>..}
    {'alert_category': ['OBSERVED', 'THREAT'], 'alert_id': ['2307bf6e-fd39-4b6<truncated>..}
    ...

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
    >>> process = api.select(Process).where(process_guid=alert.original_document['process_guid']).first()
    >>> events = process.events()[:10]
    >>> print(events[0].original_document['event_description']) # Note that I've striped the `<share>` and `<link>` tags which are also available in the response.
    'The application c:\\program files (x86)\\google\\chrome\\application\\chrome.exe attempted to modify the memory of "c:\\program files (x86)\\google\\chrome\\application\\chrome.exe", by calling the function "NtWriteVirtualMemory". The operation was successful.'
    ...


Device Control Alerts
---------------------

The Device Control Alerts are explained in the :doc:`device-control` guide.


Migrating from Notifications to Alerts
--------------------------------------

The notifications are working on a subscription based principle and they require a ``SIEM`` key of authentication.
With that key you are subscribing to a certain criteria of alerts, note that only CB Analytics and Watchlist alerts
can be retrieved from the notifications API.

Please referer to `the official notes <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-defense/latest/rest-api/#get-notifications>`_ in the Carbon Black's API website.

.. image:: _static/cbc_platform_notification_edit.png
   :alt: Editing a notification in the CBC Platform
   :align: center

Those settings shown in the screenshot can be replicated with the following code:


.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> from solrq import Q
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(BaseAlert).where((Q(category='INFO') | Q(category='THREAT')), policy_name='Standard').set_minimum_severity(7)[:5]


Advanced usage of alerts
------------------------

If you want near-real-time streaming of an alerts we advice you to referer our `Data Forwarded <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/data-forwarder-config-api/>`_.