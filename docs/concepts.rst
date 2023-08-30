Concepts
================================

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
