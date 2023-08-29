Concepts
================================

Facets
------

Facet search queries return statistical information indicating the relative weighting of the requested values as per the specified criteria.
There are two types of criteria that can be set, one is the ``range`` type which is used to specify discrete values (integers or timestamps - specified both as seconds since epoch and also as ISO 8601 strings).
The results are then grouped by occurence within the specified range.
The other type is the ``term`` type which allow for one or more fields to use as a criteria on which to return weighted results.

Setting ranges
^^^^^^^^^^^^^^

Ranges are configured via the ``add_range()`` method which accepts a dictionary of range settings or a list of range dictionaries:

    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> query = api.select(EnrichedEventFacet).where(process_pid=1000).add_range(range)

The range settings are as follows:

* ``field`` - the field to return the range for, should be a discrete one (integer or ISO 8601 timestamp)
* ``start`` - the value to begin grouping at
* ``end`` - the value to end grouping at
* ``bucket_size``- how large of a bucket to group results in. If grouping an ISO 8601 property, use a string like '-3DAYS'

Multiple ranges can be configured per query by passing a list of range dictionaries.

Setting terms
^^^^^^^^^^^^^

Terms are configured via the ``add_facet_field()`` method:

    >>> query = api.select(EnrichedEventFacet).where(process_pid=1000).add_facet_field("process_name")

The argument to add_facet_field method is the name of the field to be summarized.

Getting facet results
^^^^^^^^^^^^^^^^^^^^^

Facet results can be retrieved synchronously with the ``.results`` property, or asynchronously with the ``.execute_async()` and ``.result()`` methods.

Create the query:

    >>> event_facet_query = api.select(EventFacet).add_facet_field("event_type")
    >>> event_facet_query.where(process_guid="WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> event_facet_query.add_range(range)

1. With the ``.results`` property:

    >>> synchronous_results = event_facet_query.results
    >>> print(synchronous_results)
    EventFacet object, bound to https://defense-eap01.conferdeploy.net.
    -------------------------------------------------------------------------------
               num_found: 16
      processed_segments: 1
                  ranges: [{'start': '2020-10-16T00:00:00Z', 'end': '2020...
                   terms: [{'values': [{'total': 14, 'id': 'modload', 'na...
          total_segments: 1

2. With the ``.execute_async()`` and ``.result()`` methods:

    >>> asynchronous_future = event_facet_query.execute_async()
    >>> asynchronous_result = asynchronous_future.result()
    >>> print(asynchronous_result)
    EventFacet object, bound to https://defense-eap01.conferdeploy.net.
    -------------------------------------------------------------------------------
               num_found: 16
      processed_segments: 1
                  ranges: [{'start': '2020-10-16T00:00:00Z', 'end': '2020...
                   terms: [{'values': [{'total': 14, 'id': 'modload', 'na...
          total_segments: 1


The result for facet queries is a single object with two properties: ``terms`` and ``ranges`` that contain the facet search result weighted as per the criteria provided.

    >>> print(synchronous_result.terms)
    [{'values': [{'total': 14, 'id': 'modload', 'name': 'modload'}, {'total': 2, 'id': 'crossproc', 'name': 'crossproc'}], 'field': 'event_type'}]
    >>> print(synchronous_result.ranges)
    [{'start': '2020-10-16T00:00:00Z', 'end': '2020-11-16T00:00:00Z', 'bucket_size': '+1DAY', 'field': 'device_timestamp', 'values': None}]


Modules with support for facet searches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`ProcessFacet <cbc_sdk.platform.base.ProcessFacet>`

:mod:`EventFacet <cbc_sdk.platform.base.EventFacet>`

:mod:`EnrichedEventFacet <cbc_sdk.endpoint_standard.base.EnrichedEventFacet>`


Enriched Events
---------------

We can return the details for the enriched event for a specific event or we could return the details for all enriched events per alert.

Get details per event
^^^^^^^^^^^^^^^^^^^^^

::

  >>> from cbc_sdk.endpoint_standard import EnrichedEvent
  >>> query = cb.select(EnrichedEvent).where(alert_category='THREAT')
  >>> # get the first event returned by the query
  >>> item = query[0]
  >>> details = item.get_details()
  >>> print(
  ...     f'''
  ...     Category: {details.alert_category}
  ...     Type: {details.enriched_event_type}
  ...     Alert Id: {details.alert_id}
  ...     ''')
  Category: ['THREAT'])
  Type: CREATE_PROCESS
  Alert Id: ['3F0D00A6']

Get details for all events per alert
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  # Alert information is accessible with Platform CBAnalyticsAlert
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import CBAnalyticsAlert
  >>> api = CBCloudAPI(profile='platform')
  >>> query = cb.select(CBAnalyticsAlert).set_create_time(range="-4w")
  >>> # get the first alert returned by the query
  >>> alert = query[0]
  >>> for event in alert.get_events():
  ...     print(
  ...         f'''
  ...         Category: {event.alert_category}
  ...         Type: {event.enriched_event_type}
  ...         Alert Id: {event.alert_id}
  ...         ''')
  Category: ['OBSERVED']
  Type: SYSTEM_API_CALL
  Alert Id: ['BE084638']

  Category: ['OBSERVED']
  Type: NETWORK
  Alert Id: ['BE084638']

Live Response with Platform Devices
---------------------------------------------
As of version 1.3.0 Live Response has been changed to support CUSTOM type API Keys which enables
the platform Device model and Live Response session to be used with a single API key. Ensure your
API key has the ``Device READ`` permission along with the desired :doc:`live-response` permissions

::

  # Device information is accessible with Platform Devices
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import Device
  >>> api = CBCloudAPI(profile='platform')
  >>> platform_devices = api.select(Device).set_os(["WINDOWS", "LINUX"])
  >>> for device in platform_devices:
  ...   print(
        f'''
        Device ID: {device.id}
        Device Name: {device.name}

        ''')
  Device ID: 1234
  Device Name: Win10x64

  Device ID: 5678
  Device Name: UbuntuDev


  # Live Response is accessible with Platform Devices
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import Device
  >>> api = CBCloudAPI(profile='platform')
  >>> platform_device = api.select(Device, 1234)
  >>> platform_device.lr_session()
  url: /appservices/v6/orgs/{org_key}/liveresponse/sessions/428:1234 -> status: PENDING
  [...]

For more examples on Live Response, check :doc:`live-response`

USB Devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that ``USBDevice`` is distinct from either the Platform API ``Device`` or the Endpoint Standard ``Device``. Access
to USB devices is through the Endpoint Standard package ``from cbc_sdk.endpoint_standard import USBDevice``.

::

  # USB device information is accessible with Endpoint Standard
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.endpoint_standard import USBDevice
  >>> api = CBCloudAPI(profile='endpoint_standard')
  >>> usb_devices = api.select(USBDevice).set_statuses(['APPROVED'])
  >>> for usb in usb_devices:
  ...     print(f'''
  ...         USB Device ID: {usb.id}
  ...         USB Device: {usb.vendor_name} {usb.product_name}
  ...         ''')
  USB Device ID: 774
  USB Device: SanDisk Ultra

  USB Device ID: 778
  USB Device: SanDisk Cruzer Mini

Static Methods
--------------

In version 1.4.2 we introduced static methods on some classes. They handle API requests that are not tied to a specific resource id, thus they cannot be instance methods, instead static helper methods. Because those methods are static, they need a CBCloudAPI object to be passed as the first argument.

Search suggestions
^^^^^^^^^^^^^^^^^^

::

  # Search Suggestions for Observation
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import Observation
  >>> api = CBCloudAPI(profile='platform')
  >>> suggestions = Observation.search_suggestions(api, query="device_id", count=2)
  >>> for suggestion in suggestions:
  ...     print(suggestion["term"], suggestion["required_skus_all"], suggestion["required_skus_some"])
  device_id [] ['threathunter', 'defense']
  netconn_remote_device_id ['xdr'] []


::

  # Search Suggestions for Alerts
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import BaseAlert
  >>> api = CBCloudAPI(profile='platform')
  >>> suggestions = BaseAlert.search_suggestions(api, query="device_id")
  >>> for suggestion in suggestions:
  ...     print(suggestion["term"], suggestion["required_skus_some"])
  device_id ['defense', 'threathunter', 'deviceControl']
  device_os ['defense', 'threathunter', 'deviceControl']
  ...
  workload_name ['kubernetesSecurityRuntimeProtection']


Bulk Get Details
^^^^^^^^^^^^^^^^

::

  # Observations get details per alert id
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import Observation
  >>> api = CBCloudAPI(profile='platform')
  >>> bulk_details = Observation.bulk_get_details(api, alert_id="4d49d171-0a11-0731-5172-d0963b77d422")
  >>> for obs in bulk_details:
  ...     print(
  ...         f'''
  ...         Category: {obs.alert_category}
  ...         Type: {obs.observation_type}
  ...         Alert Id: {obs.alert_id}
  ...         ''')
  Category: ['THREAT']
  Type: CB_ANALYTICS
  Alert Id: ['4d49d171-0a11-0731-5172-d0963b77d422']

::

  # Observations get details per observation_ids
  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.platform import Observation
  >>> api = CBCloudAPI(profile='platform')
  >>> bulk_details = Observation.bulk_get_details(api, observation_ids=["13A5F4E5-C4BD-11ED-A7AB-005056A5B601:13a5f4e4-c4bd-11ed-a7ab-005056a5b611", "13A5F4E5-C4BD-11ED-A7AB-005056A5B601:13a5f4e4-c4bd-11ed-a7ab-005056a5b622"])
  >>> for obs in bulk_details:
  ...     print(
  ...         f'''
  ...         Category: {obs.alert_category}
  ...         Type: {obs.observation_type}
  ...         Alert Id: {obs.alert_id}
  ...         ''')
  Category: ['THREAT']
  Type: CB_ANALYTICS
  Alert Id: ['4d49d171-0a11-0731-5172-d0963b77d422']

  Category: ['THREAT']
  Type: CB_ANALYTICS
  Alert Id: ['4d49d171-0a11-0731-5172-d0963b77d411']
  
