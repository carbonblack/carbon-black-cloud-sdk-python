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
