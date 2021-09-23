Alerts
======

Alerts can be used to notify you about important App Control-monitored activities, such as the
appearance or spread of risky files on your endpoints. The Carbon Black Cloud Python SDK provides
all of the functionalities of the alerts such as retrieving different kinds of alerts, dismissing alerts and threats,
creating, updating and deleting. The full list of operations and attributes that are available and can be used
for the alerts can be found in the :py:mod:`BaseAlert() <cbc_sdk.platform.alerts.BaseAlert>` class.

For more information see
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/>`_

Retrieving of Alerts
--------------------

In the example below we can retrieve alerts with the minimum severity of ``6``.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import BaseAlert
    >>> api = CBCloudAPI(profile='sample')
    >>> alert = api.select(BaseAlert).set_minimum_severity(6).first()
    >>> print(alert.id, alert.device_os, alert.device_name, alert.category)
    d689e626-5d6a-<truncated> WINDOWS Alert-WinTest THREAT


Retrieving of Carbon Black Analytics Alerts (CBAnalyticsAlert)
--------------------------------------------------------------

The Carbon Black Analytics Alerts can retrieve us information about different events
which are related to our alerts. Those events contain metadata such as ``process_name`` and ``process_cmdline``.
The full list of all the attributes can be found in the
:py:mod:`EnrichedEvent() <cbc_sdk.endpoint_standard.base.EnrichedEvent>` module.

::

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
The full list of attributes and methods can be seen :py:mod:`Process() <cbc_sdk.platform.processes.Process>`.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> api = CBCloudAPI(profile='sample')
    >>> alerts = api.select(WatchlistAlert)[:10]
    >>> for alert in alerts:
    ...     process = api.select(Process).where(process_guid=alert.original_document["process_guid"]).first()
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


::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import WatchlistAlert, Process
    >>> api = CBCloudAPI(profile='sample')
    >>> alert = api.select(WatchlistAlert).first()
    >>> process = api.select(Process).where(process_guid=alert.original_document["process_guid"]).first()
    >>> events = process.events()[:10]
    >>> print(events[0].original_document["event_description"]) # Note that I've striped the `<share>` and `<link>` tags which are also available in the response.
    'The application c:\\program files (x86)\\google\\chrome\\application\\chrome.exe attempted to modify the memory of "c:\\program files (x86)\\google\\chrome\\application\\chrome.exe", by calling the function "NtWriteVirtualMemory". The operation was successful.'
    ...


Device Control Alerts
---------------------

The Device Control Alerts are explained in the :doc:`device-control` guide.
