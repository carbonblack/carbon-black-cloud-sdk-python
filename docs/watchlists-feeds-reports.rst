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

Setting up a connection is documented here: :doc:`getting-started`

About the Objects
-----------------
An *indicator of compromise* (IOC) is a query, list of strings, or list of regular expressions which constitutes
actionable threat intelligence that the Carbon Black Cloud is set up to watch for.  Any activity that matches one of
these may indicate a compromise of an endpoint.

A *report* groups one or more IOCs together, which may reflect a number of possible conditions to look for, or a number
of conditions related to a particular target program or type of malware.  Reports can be used to organize IOCs.

A *watchlist* contains reports (either directly or through a feed) that the Carbon Black Cloud is matching against
events coming from the endpoints. A positive match will trigger a "hit," which may be logged or result in an alert.

A *feed* contains reports which have been gathered by a single source. They resemble "potential watchlists."
A watchlist may be easily subscribed to a feed, so that any reports in the feed act as if they were in the watchlist
itself, triggering logs or alerts as appropriate.

Setting Up a Basic Custom Watchlist
-----------------------------------
Creating a custom watchlist that can watch incoming events and/or generate alerts requires three steps:

1. Create a report including one or more Indicators of Compromise (IOCs).
2. Add that report to a watchlist.
3. Enable alerting on the watchlist.

Creating a Report
+++++++++++++++++
In this example, a report is created, adding one or more IOCs to it:

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

Reports should always be given a ``title`` that's sufficiently unique within your organization, so as to minimize
the chances of confusing two or more Reports with each other.  Carbon Black Cloud will generate unique ``id`` values
for each report, but does not enforce any uniqueness constraint on the ``title`` of reports.

Alternatively, we can update an existing report, adding more IOCs and/or replacing existing ones.  To find an existing
report associated with a watchlist, you must look in the watchlist's ``reports`` collection.

Adding the Report to a Watchlist
++++++++++++++++++++++++++++++++
Now, add the new Report to a new Watchlist:

::

    >>> from cbc_sdk.enterprise_edr import Watchlist
    >>> watchlist = Watchlist(api, None, {"alerts_enabled": False,
    ...                                   "classifier": None,
    ...                                   "description": "We are on the lookout for any signs of suspicious applications running on our endpoints",
    ...                                   "name": "Suspicious Applications",
    ...                                   "report_ids": [report.id],
    ...                                   "tags_enabled": True})
    >>> watchlist.save()

**Note:** ``classifier`` *must* be ``None``, unless the new watchlist is being subscribed to a feed.

If you already have an existing Watchlist you wish to enhance, you can add Reports to the existing Watchlist.

Enabling Alerting on a Watchlist
++++++++++++++++++++++++++++++++
When either the ``alerts_enabled`` or ``tags_enabled`` attributes of a watchlist are ``True``, that Watchlist will
create data you can act on - either alerts or hits, respectively; if both are ``False``, the Watchlist is effectively
disabled.

Once you have the Watchlist configured with the IOCs that are generating the kinds of hits (results) you are after,
you can enable Alerting for the Watchlist, which will allow matches against the reports in the watchlist to generate
alerts.  If a watchlist identifies suspicious behavior and known threats in your environment, you will want to enable
alerts to advise you of situations where you may need to take action or modify policies.

::

    >>> watchlist.enable_alerts()

A Closer Look at IOCs
---------------------
In this document, we will only discuss the "v2" IOCs; the "v1" IOCs are only provided for backwards compatibility
reasons. They are officially deprecated, and are converted, internally, to this type.

IOCs can be classified into two general types, depending on their ``match_type`` value:

*Query IOCs* are those with a ``match_type`` of ``query``; their ``values_list`` contains a single string that
specifies a query compatible with process searches.  For example, the following IOC looks for the process ``git.exe``
that does *not* connect to one of a specified list of IP addresses:

::

    {
        "id": "example_1",
        "match_type": "query",
        "values": ["process_name:git.exe NOT (netconn_ipv4:35.158.151.206 OR netconn_ipv4:1.1.244.78
                    OR netconn_ipv4:80.18.61.229 OR netconn_ipv4:80.18.61.228)"]
    }

Query IOCs must always use field-prefixed queries (key-value pairs); they do not support just searching for a value
without a field specified.  Values in query clauses that do not specify fields will be ignored.

:Wrong: ``process_name:chrome.exe AND 192.168.1.1``
:Right: ``process_name:chrome.exe AND netconn_ipv4:192.168.1.1``

Query IOCs may search on CIDR address ranges, e.g.: ``netconn_ipv4:192.168.0.0/16``.

Query IOCs are searched every 5 minutes by the Carbon Black Cloud, and are tested against a rolling window of the
last hour's worth of data for the organization.  (They will *not* generate hits or alerts for process attributes that
were reported more than an hour in the past.)  They may employ any searchable field as documented
`here <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/platform-search-fields/>`_,
and may employ complex query logic.

*Ingress IOCs* are those with a ``match_type`` of ``equality`` or ``regex``; they use the ``field`` element to specify
the name of a field to examine the value of, and the ``values_list`` element to specify a list of values to match
against (in the case of ``match_type`` being ``equality``) or regular expressions to match against (in the case of
``match_type`` being ``regex``).  For example, this IOC will match any process that initiates a connection to one of
two listed IP addresses:

::

    {
        "id": "example_2",
        "match_type": "equality",
        "field": "netconn_ipv4",
        "values": ["8.8.8.8", "1.160.120.15"]
    }

This IOC will match any process running with an executable name beginning with "quake":

::

    {
        "id": "example_3",
        "match_type": "regex",
        "field": "process_name",
        "values": ["quake.*\\.exe"]
    }

(Note the use of the backslash to escape the '.' that separates the file extension from the name.  It must be doubled
to escape it in Python itself.)

Ingress IOCs are searched as soon as the data is received from any endpoint, and may use any process field
(as documented
`here <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/platform-search-fields/>`_;
the fields tagged with ``PROCESS``)
in their ``field`` element, whether searchable or not.  For the searches they are capable of, they are more efficient
than query IOCs, and also easier to add additional search target values to.  They can, however, only search on a single
field at a time.

**Note:** Ingress IOCs cannot be edited in the Carbon Black Cloud console UI at this time, due to a UI limitation
on editing two properties of an IOC at the same time.

You *can* include more than one entry (query or match element) in an individual IOC, but in order to ignore or disable
one of those entries, you would either have to edit the IOC or disable it entirely (thus disabling *all* entries in
that IOC).  It is recommended to use only one entry per IOC, for ease of management, unless you have already vetted the
entries and don't expect to have to disable them individually.

Both IOCs and reports may include a ``link`` property, which is used by the Carbon Black Cloud console UI as a hint
to indicate that this IOC or report is being managed outside of the console.  If this property is not ``None``,
the console UI will disable the ability to edit the IOC or report, but they can still be edited via the API.

Tips for Using IOCs
+++++++++++++++++++
* You can safely ignore certain fields in an IOC.  For example, fields like ``alert_id`` and ``process_guid`` will
  always uniquely identify just a single record in your organization's data, whereas a field like ``org_id`` will be
  a constant across *all* your organization's data.
* Timestamp fields such as ``backend_timestamp`` are useful in ad-hoc queries, to look for data occurring before or
  after a certain date, but are of limited usefulness over the span of time a watchlist may be running.
* A list of hashes (such as with ``process_sha256``) can be of limited value.  They are inconvenient to keep current,
  especially as software (whether legitimate or malicious) gets updated over time, but are definitely easier to manage
  with ``equality`` IOCs.
* Counter fields (such as ``netconn_count``) can be useful with range queries to locate processes that are using a
  large number of resources.  For example, the query ``netconn_count:[500 TO *]`` will match only processes that make
  a large number of network connections.
* When using ingress IOCs, be careful of errant characters in the ``values`` list, such as leading or trailing
  whitespace or embedded newline characters.  These errant characters may cause the IOCs to fail to match, leading to
  false negative results.
* ``equality`` IOCs for IPv4 fields (e.g. ``netconn_remote_ipv4``) cannot support CIDR notation; full IP addresses
  must be used.
* ``equality`` IOCs for IPv6 fields (e.g. ``netconn_remote_ipv6``) do not support standard or CIDR notation at this
  time. All IPv6 addresses must omit colon characters, spell out all zeroes in the address, and represent all
  alphabetic characters in uppercase. For example, "ff02::fb" becomes "FF0200000000000000000000000000FB".

Feeds
-----
Another way of managing reports is to attach them to a *feed.* Feeds can contain multiple reports, and a feed can be
attached to a watchlist, effectively making the contents of the watchlist equivalent to the contents of the feed.

Feeds are in effect “potentially-subscribable Watchlists”. A Feed has no effect on your organization until it is
subscribed to, by creating a Watchlist containing that feed. Once subscribed (and until it’s disabled or unsubscribed),
a watchlist will generate hits (and alerts if you have enabled them) for any matches against any of the IOCs in any of
that feed’s enabled reports.

**Note:** The feeds that are created by these examples are *private feeds,* meaning they are only visible within an
organization and can be created by anyone with sufficient privileges in the organization.  There are additional types
of feeds; *reserved feeds* can only be created by MSSPs, and *public feeds* can only be created or edited by
VMware Carbon Black.

A new feed may be created as follows (assuming the new report for that feed is stored in the ``report`` variable):

::

    >>> from cbc_sdk.enterprise_edr import Feed
    >>> feed_data = {'feedinfo': {
    ...                 'name': 'Suspicious Applications',
    ...                 'provider_url': 'http://example.com/location',
    ...                 'summary': 'Any signs of suspicious applications running on our endpoints',
    ...                 'category': 'external_threat_intel',
    ...                 'source_label': 'Where the info is coming from'},
    ...              'reports': [report._info]}
    >>> feed = api.create(Feed, feed_data)

If you have an existing feed, a new report may be added to it as follows (assuming the new report is stored in the
``report`` variable):

::

    >>> from cbc_sdk.enterprise_edr import Feed
    >>> feed = cb.select(Feed, 'ABCDEFGHIJKLMNOPQRSTUVWX')
    >>> feed.append_reports([report])

To update or delete an existing report in a feed, look for it in the feed's ``reports`` collection, then call the
``update()`` method on the report to replace its contents, or the ``delete()`` method on the report to delete it
entirely.

To subscribe to a feed, a new watchlist must be created around it:

::

    >>> watchlist = Watchlist(api, None, {"alerts_enabled": True,
    ...                                   "classifier": {"feed_id": feed.id},
    ...                                   "description": "Subscription to the new feed",
    ...                                   "name": "Subscribed feed",
    ...                                   "tags_enabled": True})
    >>> watchlist.save()

Limitations of Reports and Watchlists
-------------------------------------
Individual reports may contain no more than 10,000 IOCs.  Reports containing more than 1,000 IOCs will not be editable
via the Carbon Black Cloud console UI, but may still be managed using APIs.

Individual watchlists may contain no more than 10,000 reports.  Any more than that may lead to timeouts when managing
the watchlist through the Carbon Black Cloud console UI, and possibly when managing it through APIs as well.
