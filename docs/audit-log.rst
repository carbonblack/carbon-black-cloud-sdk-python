Audit Log Events
================

In the Carbon Black Cloud, *audit logs* are records of various organization-wide events, such as:

* Log in attempts by users
* Updates to connectors
* Creation of connectors
* LiveResponse events

The Audit Log API allows these records to be retrieved as objects, either by getting the most recent audit logs, or
through a flexible search API.

<!-- this is queue behavior, apply o specific queue section -->
The API call returns only *new* audit log records that have been added since
the last time the call was made using the same API Key ID. Once records have been returned, they are *cleared*
and will not be included in future responses.

When reading audit log records using a *new* API key, the queue for reading audit logs will begin three days
earlier. This may lead to duplicate data if audit log records were previously read with a different API key.

<!-- take this note out, this IS the future version -->
.. note::
    Future versions of the Carbon Black Cloud and this SDK will support a more flexible API for finding and retrieving
    audit log records.  This Guide will be rewritten to cover this when it is incorporated into the SDK.

API Permissions
---------------

To call the Audit Log APIs, use a custom API key created with a role containing the ``READ`` permission on
``org.audits``.

Retrieving Queued Audit Log Events
----------------------------------

TK

Searching for Audit Log Events
------------------------------

TK

Exporting Audit Log Events
--------------------------

TK
