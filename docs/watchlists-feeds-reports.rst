Watchlists, Feeds, Reports, and IOCs
====================================
Watchlists are a powerful feature of Carbon Black Cloud Enterprise EDR. They allow an organization to set-and-forget
searches on their endpoints' incoming events data, providing the administrator the opportunity to sift through high
volumes of activity and focus attention on those that matter.

**Note:** Use of these APIs requires that the organization be enabled for Enterprise EDR.  Verify this by logging into
the Carbon Black Cloud Console, opening the menu in the upper right corner, and checking for an ``ENABLED`` flag
against the "Enterprise EDR" entry.

All examples here assume that a Carbon Black Cloud SDK connection has been set up, such as with the following code:

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')

Setting Up a Basic Custom Watchlist
-----------------------------------
Creating a custom watchlist that can watch and/or generate alerts requires three steps:

1. Create a report including one or more Indications of Compromise (IOCs).
2. Add that report to a watchlist.
3. Enable alerting on the watchlist.

Creating a Report
+++++++++++++++++

TK

::

    >>> from cbc_sdk.enterprise_edr import Report
    >>> report = Report(api, None, {"description": "Unsigned processes impersonating browsers",
    ...                             "iocs_v2": [{
    ...                                 "id": "unsigned-chrome",
    ...                                 "match_type": "query",
    ...                                 "values": [("process_name:chrome.exe NOT process_publisher_state:FILE_SIGNATURE_STATE_SIGNED")]
    ...                                 }],
    ...                             "link": None,
    ...                             "severity": 5,
    ...                             "tags": ["compliance", "unsigned browsers"],
    ...                             "timestamp": 1601326338,
    ...                             "title": "Unsigned Browsers"})
    >>> report.save_watchlist()

Adding the Report to a Watchlist
++++++++++++++++++++++++++++++++

TK

::

    >>> from cbc_sdk.enterprise_edr import Watchlist
    >>> watchlist = Watchlist(api, None, {"alerts_enabled": False,
    ...                                   "classifier": None,
    ...                                   "description": "We are on the lookout for any signs of suspicious applications running on our endpoints",
    ...                                   "name": "Suspicious Applications",
    ...                                   "report_ids": [report.id],
    ...                                   "tags_enabled": True})
    >>> watchlist.save()

Enabling Alerting on a Watchlist
++++++++++++++++++++++++++++++++

TK

::

    >>> watchlist.enable_alerts()

A Closer Look at IOCs
=====================

