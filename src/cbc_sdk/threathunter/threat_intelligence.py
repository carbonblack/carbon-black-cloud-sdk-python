#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model Classes for Enterprise Endpoint Detection and Response"""

from __future__ import absolute_import
from cbc_sdk.errors import ApiError, InvalidObjectError, NonQueryableModel
from cbc_sdk.base import CreatableModelMixin, MutableBaseModel, UnrefreshableModel, SimpleQuery

import logging
import time
import validators

log = logging.getLogger(__name__)


"""Models"""


class FeedModel(UnrefreshableModel, CreatableModelMixin, MutableBaseModel):
    """A common base class for models used by the Feed and Watchlist APIs.
    """
    pass


class Watchlist(FeedModel):
    """Represents a ThreatHunter watchlist.
    """
    # NOTE(ww): Not documented.
    urlobject = "/threathunter/watchlistmgr/v2/watchlist"
    urlobject_single = "/threathunter/watchlistmgr/v2/watchlist/{}"
    swagger_meta_file = "threathunter/models/watchlist.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return WatchlistQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        item = {}

        if initial_data:
            item = initial_data
        elif model_unique_id:
            item = cb.get_object(self.urlobject_single.format(model_unique_id))

        feed_id = item.get("id")

        super(Watchlist, self).__init__(cb, model_unique_id=feed_id, initial_data=item,
                                        force_init=False, full_doc=True)

    def save(self):
        """Saves this watchlist on the ThreatHunter server.

        :return: The saved watchlist
        :rtype: :py:class:`Watchlist`
        :raise InvalidObjectError: if :py:meth:`validate` fails
        """
        self.validate()

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists".format(
            self._cb.credentials.org_key
        )
        new_info = self._cb.post_object(url, self._info).json()
        self._info.update(new_info)
        return self

    def validate(self):
        """Validates this watchlist's state.

        :raise InvalidObjectError: if the watchlist's state is invalid
        """
        super(Watchlist, self).validate()

    def update(self, **kwargs):
        """Updates this watchlist with the given arguments.

        >>> watchlist.update(name="New Name")

        :param kwargs: The fields to update
        :type kwargs: dict(str, str)
        :raise InvalidObjectError: if `id` is missing or :py:meth:`validate` fails
        :raise ApiError: if `report_ids` is given *and* is empty
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        # NOTE(ww): Special case, according to the docs.
        if "report_ids" in kwargs and not kwargs["report_ids"]:
            raise ApiError("can't update a watchlist to have an empty report list")

        for key, value in kwargs.items():
            if key in self._info:
                self._info[key] = value

        self.validate()

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}".format(
            self._cb.credentials.org_key,
            self.id
        )
        new_info = self._cb.put_object(url, self._info).json()
        self._info.update(new_info)

    @property
    def classifier_(self):
        """Returns the classifier key and value, if any, for this watchlist.

        :rtype: tuple(str, str) or None
        """
        classifier_dict = self._info.get("classifier")

        if not classifier_dict:
            return None

        return (classifier_dict["key"], classifier_dict["value"])

    def delete(self):
        """Deletes this watchlist from the ThreatHunter server.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.delete_object(url)

    def enable_alerts(self):
        """Enable alerts for this watchlist. Alerts are not retroactive.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/alert".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.put_object(url, None)

    def disable_alerts(self):
        """Disable alerts for this watchlist.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/alert".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.delete_object(url)

    def enable_tags(self):
        """Enable tagging for this watchlist.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/tag".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.put_object(url, None)

    def disable_tags(self):
        """Disable tagging for this watchlist.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing Watchlist ID")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/watchlists/{}/tag".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.delete_object(url)

    @property
    def feed(self):
        """Returns the feed linked to this watchlist, if there is one.

        :return: the feed linked to this watchlist, if any
        :rtype: :py:class:`Feed` or None
        """
        if not self.classifier:
            return None
        if self.classifier["key"] != "feed_id":
            log.warning("Unexpected classifier type: {}".format(self.classifier["key"]))
            return None

        return self._cb.select(Feed, self.classifier["value"])

    @property
    def reports(self):
        """Returns a list of :py:class:`Report` instances associated with this watchlist.

        .. NOTE::
            If this watchlist is a classifier (i.e. feed-linked) watchlist,
            `reports` will be empty. To get the reports associated with the linked
            feed, use :py:attr:`feed` like:

            >>> for report in watchlist.feed.reports:
            ...     print(report.title)

        :return: A list of reports
        :rtype: list(:py:class:`Report`)
        """
        if not self.report_ids:
            return []

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}"
        reports_ = []
        for rep_id in self.report_ids:
            path = url.format(self._cb.credentials.org_key, rep_id)
            resp = self._cb.get_object(path)
            reports_.append(Report(self._cb, initial_data=resp, from_watchlist=True))

        return reports_


class Feed(FeedModel):
    """Represents a ThreatHunter feed's metadata.
    """
    urlobject = "/threathunter/feedmgr/v2/orgs/{}/feeds"
    urlobject_single = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}"
    primary_key = "id"
    swagger_meta_file = "threathunter/models/feed.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return FeedQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        item = {}
        reports = []

        if initial_data:
            # NOTE(ww): Some endpoints give us the full Feed, others give us just the FeedInfo.
            if "feedinfo" in initial_data:
                item = initial_data["feedinfo"]
                reports = initial_data.get("reports", [])
            else:
                item = initial_data
        elif model_unique_id:
            url = self.urlobject_single.format(
                cb.credentials.org_key, model_unique_id
            )
            resp = cb.get_object(url)
            item = resp.get("feedinfo", {})
            reports = resp.get("reports", [])

        feed_id = item.get("id")

        super(Feed, self).__init__(cb, model_unique_id=feed_id, initial_data=item,
                                   force_init=False, full_doc=True)

        self._reports = [Report(cb, initial_data=report, feed_id=feed_id) for report in reports]

    def save(self, public=False):
        """Saves this feed on the ThreatHunter server.

        :param public:  Whether to make the feed publicly available
        :return: The saved feed
        :rtype: :py:class:`Feed`
        """
        self.validate()

        body = {
            'feedinfo': self._info,
            'reports': [report._info for report in self._reports],
        }

        url = "/threathunter/feedmgr/v2/orgs/{}/feeds".format(
            self._cb.credentials.org_key
        )
        if public:
            url = url + "/public"

        new_info = self._cb.post_object(url, body).json()
        self._info.update(new_info)
        return self

    def validate(self):
        """Validates this feed's state.

        :raise InvalidObjectError: if the feed's state is invalid
        """
        super(Feed, self).validate()

        if self.access not in ["public", "private"]:
            raise InvalidObjectError("access should be public or private")

        if not validators.url(self.provider_url):
            raise InvalidObjectError("provider_url should be a valid URL")

        for report in self._reports:
            report.validate()

    def delete(self):
        """Deletes this feed from the ThreatHunter server.

        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing feed ID")

        url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.delete_object(url)

    def update(self, **kwargs):
        """Update this feed's metadata with the given arguments.

        >>> feed.update(access="private")

        :param kwargs: The fields to update
        :type kwargs: dict(str, str)
        :raise InvalidObjectError: if `id` is missing or :py:meth:`validate` fails
        :raise ApiError: if an invalid field is specified
        """
        if not self.id:
            raise InvalidObjectError("missing feed ID")

        for key, value in kwargs.items():
            if key in self._info:
                self._info[key] = value

        self.validate()

        url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/feedinfo".format(
            self._cb.credentials.org_key,
            self.id,
        )
        new_info = self._cb.put_object(url, self._info).json()
        self._info.update(new_info)

        return self

    @property
    def reports(self):
        """Returns a list of :py:class:`Report` associated with this feed.

        :return: a list of reports
        :rtype: list(:py:class:`Report`)
        """
        return self._cb.select(Report).where(feed_id=self.id)

    def replace_reports(self, reports):
        """Replace this feed's reports with the given reports.

        :param reports: the reports to replace with
        :type reports: list(:py:class:`Report`)
        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing feed ID")

        rep_dicts = [report._info for report in reports]
        body = {"reports": rep_dicts}

        url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.post_object(url, body)

    def append_reports(self, reports):
        """Append the given reports to this feed's current reports.

        :param reports: the reports to append
        :type reports: list(:py:class:`Report`)
        :raise InvalidObjectError: if `id` is missing
        """
        if not self.id:
            raise InvalidObjectError("missing feed ID")

        rep_dicts = [report._info for report in reports]
        rep_dicts += [report._info for report in self.reports]
        body = {"reports": rep_dicts}

        url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.post_object(url, body)


class Report(FeedModel):
    """Represents reports retrieved from a ThreatHunter feed.
    """
    urlobject = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports"
    primary_key = "id"
    swagger_meta_file = "threathunter/models/report.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return ReportQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None,
                 feed_id=None, from_watchlist=False):

        super(Report, self).__init__(cb, model_unique_id=initial_data.get("id"),
                                     initial_data=initial_data,
                                     force_init=False, full_doc=True)

        # NOTE(ww): Warn instead of failing since we allow Watchlist reports
        # to be created via create(), but we don't actually know that the user
        # intends to use them with a watchlist until they call save().
        if not feed_id and not from_watchlist:
            log.warning("Report created without feed ID or not from watchlist")

        self._feed_id = feed_id
        self._from_watchlist = from_watchlist

        if self.iocs:
            self._iocs = IOC(cb, initial_data=self.iocs, report_id=self.id)
        if self.iocs_v2:
            self._iocs_v2 = [IOC_V2(cb, initial_data=ioc, report_id=self.id) for ioc in self.iocs_v2]

    def save_watchlist(self):
        """Saves this report *as a watchlist report*.

        .. NOTE::
            This method **cannot** be used to save a feed report. To
            save feed reports, create them with `cb.create` and use
            :py:meth:`Feed.replace`.

        :raise InvalidObjectError: if :py:meth:`validate` fails
        """
        self.validate()

        # NOTE(ww): Once saved, this object corresponds to a watchlist report.
        # As such, we need to tell the model to route calls like update()
        # and delete() to the correct (watchlist) endpoints.
        self._from_watchlist = True

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports".format(
            self._cb.credentials.org_key
        )
        new_info = self._cb.post_object(url, self._info).json()
        self._info.update(new_info)
        return self

    def validate(self):
        """Validates this report's state.

        :raise InvalidObjectError: if the report's state is invalid
        """
        super(Report, self).validate()

        if self.link and not validators.url(self.link):
            raise InvalidObjectError("link should be a valid URL")

        if self.iocs_v2:
            [ioc.validate() for ioc in self._iocs_v2]

    def update(self, **kwargs):
        """Update this report with the given arguments.

        .. NOTE::
            The report's timestamp is always updated, regardless of whether
            passed explicitly.

        >>> report.update(title="My new report title")

        :param kwargs: The fields to update
        :type kwargs: dict(str, str)
        :return: The updated report
        :rtype: :py:class:`Report`
        :raises InvalidObjectError: if `id` is missing, or `feed_id` is missing
            and this report is a feed report, or :py:meth:`validate` fails
        """

        if not self.id:
            raise InvalidObjectError("missing Report ID")

        if self._from_watchlist:
            url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}".format(
                self._cb.credentials.org_key,
                self.id
            )
        else:
            if not self._feed_id:
                raise InvalidObjectError("missing Feed ID")
            url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports/{}".format(
                self._cb.credentials.org_key,
                self._feed_id,
                self.id
            )

        for key, value in kwargs.items():
            if key in self._info:
                self._info[key] = value

        # NOTE(ww): Updating reports on the watchlist API appears to require
        # updated timestamps.
        self.timestamp = int(time.time())
        self.validate()

        new_info = self._cb.put_object(url, self._info).json()
        self._info.update(new_info)
        return self

    def delete(self):
        """Deletes this report from the ThreatHunter server.

        >>> report.delete()

        :raises InvalidObjectError: if `id` is missing, or `feed_id` is missing
            and this report is a feed report
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")

        if self._from_watchlist:
            url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}".format(
                self._cb.credentials.org_key,
                self.id
            )
        else:
            if not self._feed_id:
                raise InvalidObjectError("missing Feed ID")
            url = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports/{}".format(
                self._cb.credentials.org_key,
                self._feed_id,
                self.id
            )

        self._cb.delete_object(url)

    @property
    def ignored(self):
        """Returns the ignore status for this report.

        Only watchlist reports have an ignore status.

        >>> if report.ignored:
        ...     report.unignore()

        :return: whether or not this report is ignored
        :rtype: bool
        :raises InvalidObjectError: if `id` is missing or this report is not from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")
        if not self._from_watchlist:
            raise InvalidObjectError("ignore status only applies to watchlist reports")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/ignore".format(
            self._cb.credentials.org_key,
            self.id
        )
        resp = self._cb.get_object(url)
        return resp["ignored"]

    def ignore(self):
        """Sets the ignore status on this report.

        Only watchlist reports have an ignore status.

        :raises InvalidObjectError: if `id` is missing or this report is not from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")

        if not self._from_watchlist:
            raise InvalidObjectError("ignoring only applies to watchlist reports")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/ignore".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.put_object(url, None)

    def unignore(self):
        """Removes the ignore status on this report.

        Only watchlist reports have an ignore status.

        :raises InvalidObjectError: if `id` is missing or this report is not from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")

        if not self._from_watchlist:
            raise InvalidObjectError("ignoring only applies to watchlist reports")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/ignore".format(
            self._cb.credentials.org_key,
            self.id
        )
        self._cb.delete_object(url)

    @property
    def custom_severity(self):
        """Returns the custom severity for this report.

        :return: The custom severity for this report, if it exists
        :rtype: :py:class:`ReportSeverity`
        :raise InvalidObjectError: if `id` is missing or this report is from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing report ID")
        if self._from_watchlist:
            raise InvalidObjectError("watchlist reports don't have custom severities")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/severity".format(
            self._cb.credentials.org_key,
            self.id
        )
        resp = self._cb.get_object(url)
        return ReportSeverity(self._cb, initial_data=resp)

    @custom_severity.setter
    def custom_severity(self, sev_level):
        """Sets or removed the custom severity for this report

        :param int sev_level: the new severity, or None to remove the custom severity
        :return: The new custom severity, or None if removed
        :rtype: :py:class:`ReportSeverity` or None
        :raise InvalidObjectError: if `id` is missing or this report is from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing report ID")
        if self._from_watchlist:
            raise InvalidObjectError("watchlist reports don't have custom severities")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/severity".format(
            self._cb.credentials.org_key,
            self.id
        )

        if sev_level is None:
            self._cb.delete_object(url)
            return

        args = {
            "report_id": self.id,
            "severity": sev_level,
        }

        resp = self._cb.put_object(url, args).json()
        return ReportSeverity(self._cb, initial_data=resp)

    @property
    def iocs_(self):
        """Returns a list of :py:class:`IOC_V2` associated with this report.

        >>> for ioc in report.iocs_:
        ...     print(ioc.values)

        :return: a list of IOCs
        :rtype: list(:py:class:`IOC_V2`)
        """
        if not self.iocs_v2:
            return []

        # NOTE(ww): This name is underscored because something in the model
        # hierarchy is messing up method resolution -- self.iocs and self.iocs_v2
        # are resolving to the attributes rather than the attribute-ified
        # methods.
        return self._iocs_v2


class ReportSeverity(FeedModel):
    """Represents severity information for a watchlist report.
    """
    primary_key = "report_id"
    swagger_meta_file = "threathunter/models/report_severity.yaml"

    def __init__(self, cb, initial_data=None):
        if not initial_data:
            raise ApiError("ReportSeverity can only be initialized from initial_data")

        super(ReportSeverity, self).__init__(cb, model_unique_id=initial_data.get(self.primary_key),
                                             initial_data=initial_data, force_init=False,
                                             full_doc=True)

    def _query_implementation(self, cb, **kwargs):
        raise NonQueryableModel("IOC does not support querying")


class IOC(FeedModel):
    """Represents a collection of categorized IOCs.
    """
    swagger_meta_file = "threathunter/models/iocs.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, report_id=None):
        """Creates a new IOC instance.

        :raise ApiError: if `initial_data` is `None`
        """
        if not initial_data:
            raise ApiError("IOC can only be initialized from initial_data")

        super(IOC, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                  force_init=False, full_doc=True)

        self._report_id = report_id

    def _query_implementation(self, cb, **kwargs):
        raise NonQueryableModel("IOC does not support querying")

    def validate(self):
        """Validates this IOC structure's state.

        :raise InvalidObjectError: if the IOC structure's state is invalid
        """
        super(IOC, self).validate()

        for md5 in self.md5:
            if not validators(md5):
                raise InvalidObjectError("invalid MD5 checksum: {}".format(md5))
        for ipv4 in self.ipv4:
            if not validators(ipv4):
                raise InvalidObjectError("invalid IPv4 address: {}".format(ipv4))
        for ipv6 in self.ipv6:
            if not validators(ipv6):
                raise InvalidObjectError("invalid IPv6 address: {}".format(ipv6))
        for dns in self.dns:
            if not validators(dns):
                raise InvalidObjectError("invalid domain: {}".format(dns))
        for query in self.query:
            if not self._cb.validate(query["search_query"]):
                raise InvalidObjectError("invalid search query: {}".format(query["search_query"]))


class IOC_V2(FeedModel):
    """Represents a collection of IOCs of a particular type, plus matching criteria and metadata.
    """
    primary_key = "id"
    swagger_meta_file = "threathunter/models/ioc_v2.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, report_id=None):
        """Creates a new IOC_V2 instance.

        :raise ApiError: if `initial_data` is `None`
        """
        if not initial_data:
            raise ApiError("IOC_V2 can only be initialized from initial_data")

        super(IOC_V2, self).__init__(cb, model_unique_id=initial_data.get(self.primary_key),
                                     initial_data=initial_data, force_init=False,
                                     full_doc=True)

        self._report_id = report_id

    def _query_implementation(self, cb, **kwargs):
        raise NonQueryableModel("IOC_V2 does not support querying")

    def validate(self):
        """Validates this IOC_V2's state.

        :raise InvalidObjectError: if the IOC_V2's state is invalid
        """
        super(IOC_V2, self).validate()

        if self.link and not validators.url(self.link):
            raise InvalidObjectError("link should be a valid URL")

    @property
    def ignored(self):
        """Returns whether or not this IOC is ignored

        >>> if ioc.ignored:
        ...     ioc.unignore()

        :return: the ignore status
        :rtype: bool
        :raise InvalidObjectError: if this IOC is missing an `id` or is not a watchlist IOC
        """
        if not self.id:
            raise InvalidObjectError("missing IOC ID")
        if not self._report_id:
            raise InvalidObjectError("ignore status only applies to watchlist IOCs")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/iocs/{}/ignore".format(
            self._cb.credentials.org_key,
            self._report_id,
            self.id
        )
        resp = self._cb.get_object(url)
        return resp["ignored"]

    def ignore(self):
        """Sets the ignore status on this IOC.

        Only watchlist IOCs have an ignore status.

        :raises InvalidObjectError: if `id` is missing or this IOC is not from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")
        if not self._report_id:
            raise InvalidObjectError("ignoring only applies to watchlist IOCs")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/iocs/{}/ignore".format(
            self._cb.credentials.org_key,
            self._report_id,
            self.id
        )
        self._cb.put_object(url, None)

    def unignore(self):
        """Removes the ignore status on this IOC.

        Only watchlist IOCs have an ignore status.

        :raises InvalidObjectError: if `id` is missing or this IOC is not from a watchlist
        """
        if not self.id:
            raise InvalidObjectError("missing Report ID")
        if not self._report_id:
            raise InvalidObjectError("ignoring only applies to watchlist IOCs")

        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/{}/iocs/{}/ignore".format(
            self._cb.credentials.org_key,
            self._report_id,
            self.id
        )
        self._cb.delete_object(url)


"""Queries"""


class FeedQuery(SimpleQuery):
    """Represents the logic for a :py:class:`Feed` query.

    >>> cb.select(Feed)
    >>> cb.select(Feed, id)
    >>> cb.select(Feed).where(include_public=True)
    """
    def __init__(self, doc_class, cb):
        super(FeedQuery, self).__init__(doc_class, cb)
        self._args = {}

    def where(self, **kwargs):
        self._args = dict(self._args, **kwargs)
        return self

    def prepare_query(self, args):
        request = args
        params = self._query_builder._collapse()
        if params is not None:
            for query in params.split(' '):
                # convert from str('key:value') to dict{'key': 'value'}
                key, value = query.split(':', 1)
                request[key] = value
        return request

    @property
    def results(self):
        log.debug("Fetching all feeds")
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key)
        resp = self._cb.get_object(url, query_parameters=self._args)
        results = resp.get("results", [])
        return [self._doc_class(self._cb, initial_data=item) for item in results]


class ReportQuery(SimpleQuery):
    """Represents the logic for a :py:class:`Report` query.

    >>> cb.select(Report).where(feed_id=id)

    .. NOTE::
        Only feed reports can be queried. Watchlist reports
        should be interacted with via :py:meth:`Watchlist.reports`.
    """
    def __init__(self, doc_class, cb):
        super(ReportQuery, self).__init__(doc_class, cb)
        self._args = {}

    def where(self, **kwargs):
        self._args = dict(self._args, **kwargs)
        return self

    @property
    def results(self):
        if "feed_id" not in self._args:
            raise ApiError("required parameter feed_id missing")

        feed_id = self._args["feed_id"]

        log.debug("Fetching all reports")
        url = self._doc_class.urlobject.format(
            self._cb.credentials.org_key,
            feed_id,
        )
        resp = self._cb.get_object(url)
        results = resp.get("results", [])
        return [self._doc_class(self._cb, initial_data=item, feed_id=feed_id) for item in results]


class WatchlistQuery(SimpleQuery):
    """Represents the logic for a :py:class:`Watchlist` query.

    >>> cb.select(Watchlist)
    """
    def __init__(self, doc_class, cb):
        super(WatchlistQuery, self).__init__(doc_class, cb)

    @property
    def results(self):
        log.debug("Fetching all watchlists")

        resp = self._cb.get_object(self._doc_class.urlobject)
        results = resp.get("results", [])
        return [self._doc_class(self._cb, initial_data=item) for item in results]
