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
    """A common base class for models used by the Feed and Watchlist APIs."""
    pass


class Watchlist(FeedModel):
    """Represents an Enterprise EDR watchlist."""
    # NOTE(ww): Not documented.
    urlobject = "/threathunter/watchlistmgr/v2/watchlist"
    urlobject_single = "/threathunter/watchlistmgr/v2/watchlist/{}"
    swagger_meta_file = "enterprise_edr/models/watchlist.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return WatchlistQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        """
        Initialize the Watchlist object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (str): The unique ID of the watch list.
            initial_data (dict): The initial data for the object.
        """
        item = {}

        if initial_data:
            item = initial_data
        elif model_unique_id:
            item = cb.get_object(self.urlobject_single.format(model_unique_id))

        feed_id = item.get("id")

        super(Watchlist, self).__init__(cb, model_unique_id=feed_id, initial_data=item,
                                        force_init=False, full_doc=True)

    def save(self):
        """Saves this watchlist on the Enterprise EDR server.

        Returns:
            Watchlist (Watchlist): The saved Watchlist.

        Raises:
            InvalidObjectError: If Watchlist.validate() fails.
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

        Raises:
            InvalidObjectError: If the Watchlist's state is invalid.
        """
        super(Watchlist, self).validate()

    def update(self, **kwargs):
        """Updates this watchlist with the given arguments.

        Arguments:
            **kwargs (dict(str, str)): The fields to update.

        Raises:
            InvalidObjectError: If `id` is missing or Watchlist.validate() fails.
            ApiError: If `report_ids` is given and is empty.

        Example:

        >>> watchlist.update(name="New Name")


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

        Returns:
            tuple(str, str): Watchlist's classifier key and value.
            None: If there is no classifier key and value.
        """
        classifier_dict = self._info.get("classifier")

        if not classifier_dict:
            return None

        return (classifier_dict["key"], classifier_dict["value"])

    def delete(self):
        """Deletes this watchlist from the Enterprise EDR server.

        Raises:
            InvalidObjectError: If `id` is missing.
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

        Raises:
            InvalidObjectError: If `id` is missing.
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

        Raises:
            InvalidObjectError: If `id` is missing.
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

        Raises:
            InvalidObjectError: If `id` is missing.
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

        Raises:
            InvalidObjectError: if `id` is missing.
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
        """Returns the Feed linked to this Watchlist, if there is one."""
        if not self.classifier:
            return None
        if self.classifier["key"] != "feed_id":
            log.warning("Unexpected classifier type: {}".format(self.classifier["key"]))
            return None

        return self._cb.select(Feed, self.classifier["value"])

    @property
    def reports(self):
        """Returns a list of Report objects associated with this watchlist.

        Returns:
            Reports ([Report]): List of Reports associated with the watchlist.

        Note:
            If this Watchlist is a classifier (i.e. feed-linked) Watchlist,
            `reports` will be empty. To get the reports associated with the linked
            Feed, use feed like:

            >>> for report in watchlist.feed.reports:
            ...     print(report.title)
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
    """Represents an Enterprise EDR feed's metadata."""
    urlobject = "/threathunter/feedmgr/v2/orgs/{}/feeds"
    urlobject_single = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}"
    primary_key = "id"
    swagger_meta_file = "enterprise_edr/models/feed.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return FeedQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None):
        """
        Initialize the Feed object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (str): The unique ID of the feed.
            initial_data (dict): The initial data for the object.
        """
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
        """Saves this feed on the Enterprise EDR server.

        Arguments:
            public (bool): Whether to make the feed publicly available.

        Returns:
            Feed (Feed): The saved Feed.
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

        Raises:
            InvalidObjectError: If the Feed's state is invalid.
        """
        super(Feed, self).validate()

        if self.access not in ["public", "private"]:
            raise InvalidObjectError("access should be public or private")

        if not validators.url(self.provider_url):
            raise InvalidObjectError("provider_url should be a valid URL")

        for report in self._reports:
            report.validate()

    def delete(self):
        """Deletes this feed from the Enterprise EDR server.

        Raises:
            InvalidObjectError: If `id` is missing.
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

        Arguments:
            **kwargs (dict(str, str)): The fields to update.

        Raises:
            InvalidObjectError: If `id` is missing or Feed.validate() fails.
            ApiError: If an invalid field is specified.

        Example:

        >>> feed.update(access="private")
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
        """Returns a list of Reports associated with this feed.

        Returns:
            Reports ([Report]): List of Reports in this Feed.
        """
        return self._cb.select(Report).where(feed_id=self.id)

    def replace_reports(self, reports):
        """Replace this Feed's Reports with the given Reports.

        Arguments:
            reports ([Report]): List of Reports to replace existing Reports with.

        Raises:
            InvalidObjectError: If `id` is missing.
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
        """Append the given Reports to this Feed's current Reports.

        Arguments:
            reports ([Report]): List of Reports to append to Feed.

        Raises:
            InvalidObjectError: If `id` is missing.
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
    """Represents reports retrieved from an Enterprise EDR feed."""
    urlobject = "/threathunter/feedmgr/v2/orgs/{}/feeds/{}/reports"
    primary_key = "id"
    swagger_meta_file = "enterprise_edr/models/report.yaml"

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        return ReportQuery(self, cb)

    def __init__(self, cb, model_unique_id=None, initial_data=None,
                 feed_id=None, from_watchlist=False):
        """
        Initialize the ReportSeverity object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): Unused.
            initial_data (dict): The initial data for the object.
            feed_id (str): The ID of the feed this report is for.
            from_watchlist (str): The ID of the watchlist this report is for.
        """
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

        Note:
            This method **cannot** be used to save a feed report. To
            save feed reports, create them with `cb.create` and use
            `Feed.replace`.

        Raises:
            InvalidObjectError: If Report.validate() fails.
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

        Raises:
            InvalidObjectError: If the report's state is invalid
        """
        super(Report, self).validate()

        if self.link and not validators.url(self.link):
            raise InvalidObjectError("link should be a valid URL")

        if self.iocs_v2:
            [ioc.validate() for ioc in self._iocs_v2]

    def update(self, **kwargs):
        """Update this Report with the given arguments.

        Arguments:
            **kwargs (dict(str, str)): The Report fields to update.

        Returns:
            Report (Report): The updated Report.

        Raises:
            InvalidObjectError: If `id` is missing, or `feed_id` is missing
                and this report is a Feed Report, or Report.validate() fails.

        Note:
            The report's timestamp is always updated, regardless of whether
            passed explicitly.

        >>> report.update(title="My new report title")
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
        """Deletes this report from the Enterprise EDR server.

        Raises:
            InvalidObjectError: If `id` is missing, or `feed_id` is missing
                and this report is a Feed Report.

        Example:

        >>> report.delete()
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

        Returns:
            (bool): True if this Report is ignored, False otherwise.

        Raises:
            InvalidObjectError: If `id` is missing or this Report is not from a Watchlist.

        Example:

        >>> if report.ignored:
        ...     report.unignore()
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

        Raises:
            InvalidObjectError: If `id` is missing or this Report is not from a Watchlist.
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

        Raises:
            InvalidObjectError: If `id` is missing or this Report is not from a Watchlist.
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

        Returns:
            ReportSeverity (ReportSeverity): The custom severity for this Report,
                if it exists.

        Raises:
            InvalidObjectError: If `id` ismissing or this Report is from a Watchlist.
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
        """Sets or removed the custom severity for this report.

        Arguments:
            sev_level (int): The new severity, or None to remove the custom severity.

        Returns:
            ReportSeverity (ReportSeverity): The new custom severity.
            None: If the custom severity was removed.

        Raises:
            InvalidObjectError: If `id` is missing or this Report is from a Watchlist.
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
        """Returns a list of IOC_V2's associated with this report.

        Returns:
            IOC_V2 ([IOC_V2]): List of IOC_V2's for associated with the Report.

        Example:

        >>> for ioc in report.iocs_:
        ...     print(ioc.values)
        """
        if not self.iocs_v2:
            return []

        # NOTE(ww): This name is underscored because something in the model
        # hierarchy is messing up method resolution -- self.iocs and self.iocs_v2
        # are resolving to the attributes rather than the attribute-ified
        # methods.
        return self._iocs_v2


class ReportSeverity(FeedModel):
    """Represents severity information for a Watchlist Report."""
    primary_key = "report_id"
    swagger_meta_file = "enterprise_edr/models/report_severity.yaml"

    def __init__(self, cb, initial_data=None):
        """
        Initialize the ReportSeverity object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            initial_data (dict): The initial data for the object.
        """
        if not initial_data:
            raise ApiError("ReportSeverity can only be initialized from initial_data")

        super(ReportSeverity, self).__init__(cb, model_unique_id=initial_data.get(self.primary_key),
                                             initial_data=initial_data, force_init=False,
                                             full_doc=True)

    def _query_implementation(self, cb, **kwargs):
        raise NonQueryableModel("IOC does not support querying")


class IOC(FeedModel):
    """Represents a collection of categorized IOCs."""
    swagger_meta_file = "enterprise_edr/models/iocs.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, report_id=None):
        """Creates a new IOC instance.

        Raises:
            ApiError: If `initial_data` is None.
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

        Raises:
            InvalidObjectError: If the IOC structure's state is invalid.
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
    """Represents a collection of IOCs of a particular type, plus matching criteria and metadata."""
    primary_key = "id"
    swagger_meta_file = "enterprise_edr/models/ioc_v2.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, report_id=None):
        """Creates a new IOC_V2 instance.

        Raises:
            ApiError: If `initial_data` is None.
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

        Raises:
            InvalidObjectError: If the IOC_V2's state is invalid.
        """
        super(IOC_V2, self).validate()

        if self.link and not validators.url(self.link):
            raise InvalidObjectError("link should be a valid URL")

    @property
    def ignored(self):
        """Returns whether or not this IOC is ignored

        Returns:
            (bool): True if the IOC is ignore, False otherwise.

        Raises:
            InvalidObjectError: If this IOC is missing an `id` or is not a Watchlist IOC.

        Example:

        >>> if ioc.ignored:
        ...     ioc.unignore()
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

        Raises:
            InvalidObjectError: If `id` is missing or this IOC is not from a Watchlist.
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

        Raises:
            InvalidObjectError: If `id` is missing or this IOC is not from a Watchlist.
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
    """Represents the logic for a Feed query.

    >>> cb.select(Feed)
    >>> cb.select(Feed, id)
    >>> cb.select(Feed).where(include_public=True)
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the FeedQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(FeedQuery, self).__init__(doc_class, cb)
        self._args = {}

    def where(self, **kwargs):
        """Add kwargs to self._args dictionary."""
        self._args = dict(self._args, **kwargs)
        return self

    @property
    def results(self):
        """Return a list of Feed objects matching self._args parameters."""
        log.debug("Fetching all feeds")
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key)
        resp = self._cb.get_object(url, query_parameters=self._args)
        results = resp.get("results", [])
        return [self._doc_class(self._cb, initial_data=item) for item in results]


class ReportQuery(SimpleQuery):
    """Represents the logic for a Report query.

    Note:
        Only feed reports can be queried. Watchlist reports should be interacted
            with via Watchlist.reports().

    Example:
    >>> cb.select(Report).where(feed_id=id)
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the ReportQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(ReportQuery, self).__init__(doc_class, cb)
        self._args = {}

    def where(self, **kwargs):
        """Add kwargs to self._args dictionary."""
        self._args = dict(self._args, **kwargs)
        return self

    @property
    def results(self):
        """Return a list of Report objects matching self._args['feed_id']."""
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
    """Represents the logic for a Watchlist query.

    >>> cb.select(Watchlist)
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the WatchlistQuery object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(WatchlistQuery, self).__init__(doc_class, cb)

    @property
    def results(self):
        """Return a list of all Watchlist objects."""
        log.debug("Fetching all watchlists")

        resp = self._cb.get_object(self._doc_class.urlobject)
        results = resp.get("results", [])
        return [self._doc_class(self._cb, initial_data=item) for item in results]
