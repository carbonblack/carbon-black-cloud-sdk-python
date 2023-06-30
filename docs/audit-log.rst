Audit Log Notifications
=======================

In the Carbon Black Cloud, *audit log notifications* are notifications of various organization-wide events, such as:

* Log in attempts by users
* Updates to connectors
* Creation of connectors
* LiveResponse events

The Audit Log API allows these notifications to be retrieved in JSON format, sorted by time in ascending order
(oldest notifications come first). The API call returns only *new* audit log notifications that have been added since
the last time the call was made using the same API Key ID. Once notifications have been returned, they are *cleared*
and will not be included in future responses.

When reading audit log notifications using a *new* API key, the queue for reading audit logs will begin three days
earlier. This may lead to duplicate data if audit log notifications were previously read with a different API key.

.. note::
    Future versions of the Carbon Black Cloud and this SDK will support a more flexible API for finding and retrieving
    audit log notifications.  This Guide will be rewritten to cover this when it is incorporated into the SDK.

API Permissions
---------------

To call this API function, use a custom API key created with a role containing the ``READ`` permission on
``org.audits``.

Example of API Usage
--------------------

.. code-block:: python

    import time
    from cbc_sdk import CBCloudAPI
    from cbc_sdk.platform import AuditLog

    cb = CBCloudAPI(profile='yourprofile')
    running = True

    while running:
        events_list = AuditLog.get_auditlogs(cb)
        for event in events_list:
            print(f"Event {event['eventId']}:")
            for (k, v) in event.items():
                print(f"\t{k}: {v}")
        # omitted: decide whether running should be set to False
        if running:
            time.sleep(5)
