Audit Log Events
================

In the Carbon Black Cloud, *audit logs* are records of various organization-wide events, such as:

* Log in attempts by users
* Updates to connectors
* Creation of connectors
* LiveResponse events

The Audit Log API allows these records to be retrieved as objects, either by getting the most recent audit logs, or
through a flexible search API.

API Permissions
---------------

To call the Audit Log APIs, use a custom API key created with a role containing the ``READ`` permission on
``org.audits``.

Retrieving Queued Audit Log Events
----------------------------------

The Carbon Black Cloud maintains a queue of audit log events for each API key, which is initialized with the last three
days of audit logs when the API key is created.  This demonstrates how to read audit log events from the queue::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import AuditLog
    >>> api = CBCloudAPI(profile='sample')
    >>> events = AuditLog.get_queued_auditlogs(api)
    >>> for event in events:
    ...     print(f"{event.create_time}: {event.actor} {event.description}")

Once audit log events have been retrieved from the queue, they are "cleared" and will not be included in future
responses to a ``get_queued_auditlogs()`` call.

.. note::
    Reading queued audit log events using *different* API keys may lead to duplicate data.

Searching for Audit Log Events
------------------------------

Audit log events may be searched for in a manner similar to other objects within the SDK::

    # assume "api" contains our CBCloudAPI reference as above
    >>> query = api.select(AuditLog).where("description:Logged in")
    >>> query.sort_by("create_time")
    >>> for event in query:
    ...     print(f"{event.create_time}: {event.actor} {event.description}")

See also the :ref:`searching-guide` guide page for a more detailed discussion of searching.

Exporting Audit Log Events
--------------------------

Any search query may also be used to export audit log data, in either CSV or JSON format::

    # assume "api" contains our CBCloudAPI reference as above
    >>> query = api.select(AuditLog).where("description:Logged in")
    >>> query.sort_by("create_time")
    >>> job = query.export("csv")
    >>> result = job.await_completion().result()
    >>> print(result)

Note that the ``export()`` call returns a ``Job`` object, as exports can take some time to complete.  The results may
be obtained from the ``Job`` when the export process is completed.
