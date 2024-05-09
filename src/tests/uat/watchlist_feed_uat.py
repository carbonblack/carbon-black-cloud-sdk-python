# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Test script for watchlists and feeds."""

import sys
from datetime import datetime
from cbc_sdk.enterprise_edr import Report, IOC_V2, Watchlist, Feed
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


CURRENT_DATE = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def create_report_in_watchlist(api):
    """
    Create_report_in_watchlist creates a report creates a watchlist and adds the report

    The report is then set to ignore, then un-ignored
    validation of correct behaviour is by review of the printed results
    script executed successfully on release candidate 1.3.5
    """
    print("Testing create_report_in_watchlist...")
    builder = Report.create(api, "SDK Test v36wl Unsigned Browsers",
                            "Unsigned processes impersonating browsers", 5)
    builder.add_tag("compliance").add_tag("unsigned_browsers")
    builder.add_ioc(IOC_V2.create_query(api, "unsigned-chrome",
                                        "process_name:chrome.exe "
                                        "NOT process_publisher_state:FILE_SIGNATURE_STATE_SIGNED"))
    watchlist_report = builder.build()
    watchlist_report.save_watchlist()
    print("Report:")
    print(watchlist_report)
    builder = Watchlist.create(api, f"SDK Testing {CURRENT_DATE} v36")
    builder.set_description("Description for SDK testing").add_reports([watchlist_report])
    watchlist = builder.build()
    watchlist.save()
    print("Watchlist:")
    print(watchlist)
    watchlist.enable_alerts()
    print('ignore the watchlist report ')
    watchlist_report.ignore()
    print(f'watchlist_report ignored value: {watchlist_report.ignored}')
    print('un-ignore the watchlist report ')
    watchlist_report.unignore()
    print(f'watchlist_report ignored value, should be ignored = False: {watchlist_report.ignored}')
    print('create_report_in_watchlist.............................Check UI to validate')
    return watchlist.id


def create_report_in_feed(api):
    """
    Create_report_in_feed creates a report, creates a feed and adds the report to that feed.

    The feed id is returned for later manipulation.
    the report is then set to ignore, then un-ignored
    validation of correct behaviour is by review of the printed results
    script executed successfully on release candidate 1.3.5
    """
    print("Testing create_report_in_feed...")
    report_builder = Report.create(api, "Report for Feed v36", "Feed - Unsigned processes impersonating browsers", 5)
    report_builder.add_tag("compliance").add_tag("unsigned_browsers")
    report_builder.add_ioc(IOC_V2.create_query(api, "unsigned-chrome",
                                               "process_name:chrome.exe "
                                               "NOT process_publisher_state:FILE_SIGNATURE_STATE_SIGNED"))
    report_builder.set_visibility("visible")
    report = report_builder.build()
    print("Newly created report:")
    print(report)
    feed_builder = Feed.create(api, f'SDK Testing - Feed - {CURRENT_DATE} v36',
                               'http://example.com/location',
                               'Any signs of suspicious applications running on our endpoints', 'external_threat_intel')
    feed_builder.set_source_label('Where the info is coming from')
    feed_builder.add_reports([report])
    feed = feed_builder.build()
    feed.save()
    print("Newly saved feed:")
    print(feed)
    for r in feed.reports:
        print("Report in Feed")
        print(r)
        print(f'feed_report ignored value, should be ignored = False: {r.ignored}')

    saved_report = feed.reports[0]
    print("Working with this report:")
    print(saved_report)
    print(saved_report.ignored)

    print('check ignoring the report while the feed is not in a watchlist')
    saved_report.ignore()
    print(f'feed_report ignored value: {saved_report.ignored}')
    print('un-ignore the feed report ')
    saved_report.unignore()
    print(f'feed_report ignored value, should be ignored = False: {saved_report.ignored}')
    print('create_report_in_feed.............................Check UI to validate')

    return feed.id


def add_feed_to_watchlist_and_ignore_report(api, feed_id):
    """
    Create_report_in_feed_in_watchlist expects to receive a feed_id of a feed

    containing one report, typically created in the previous method create_report_in_feed
    It subscribes that feed to a watchlist.
    the report is then set to ignore, then un-ignored
    validation of correct behaviour is by review of the printed results
    script executed successfully on release candidate 1.3.5
    """
    print("Testing add_feed_to_watchlist_and_ignore_report...")
    feed = api.select(Feed, feed_id)
    print("newly retrieved feed")
    print(feed)

    print('check only one report and that the ignored status on it is false')
    for r in feed.reports:
        print(r)
        print(r.ignored)

    print('put the feed in a watchlist')
    feed_watchlist = Watchlist.create_from_feed(feed, f"SDK Testing - Watchlist for Feed - {CURRENT_DATE} v36 ",
                                                "Subscription to the new feed")
    watchlist = feed_watchlist.save()

    print('re-select the feed and the report')
    report_to_manipulate = watchlist.feed.reports[0]

    print("Working with this report:")
    print(report_to_manipulate)
    print(f'ignored should be false: {report_to_manipulate.ignored}')

    print('check ignoring the report while the feed is not in a watchlist')
    report_to_manipulate.ignore()
    print(f'report_to_manipulate ignored value: {report_to_manipulate.ignored}')
    print('un-ignore the feed report ')
    report_to_manipulate.unignore()
    print(f'report_to_manipulate ignored value, should be ignored = False: {report_to_manipulate.ignored}')
    print('add_feed_to_watchlist_and_ignore_report.............................Check UI to validate')


def get_unsubscribed_feeds(api):
    """Get any feeds that aren't subscibed to by a watchlist"""
    feed_query = api.select(Feed)
    all_feeds = {}
    for feed in feed_query:
        all_feeds[feed.id] = feed.name
    print(f"Got {len(all_feeds)} feed name(s) from all feeds")
    wl_query = api.select(Watchlist)
    wl_classifs = [wl.classifier_ for wl in wl_query if wl.classifier_ is not None]
    wl_feed_ids = [cl[1] for cl in wl_classifs if cl[0] == 'feed_id']
    print(f"Got {len(wl_feed_ids)} feed ID(s) from watchlists")
    result = [id for id in all_feeds.keys() if id not in wl_feed_ids]

    print(f"Found {len(result)} feed(s)")
    for id in result:
        print(f"{id} - {all_feeds[id]}")


def get_reports_in_a_feed(api, feed_id):
    """Get all the reports within a feed"""
    feed = api.select(Feed, feed_id)
    print(f"[Reports for feed with ID:{feed_id}]")
    for report in feed.reports:
        print(f"{report.id} - {report.title}")


def add_new_report_to_existing_watchlist(api, watchlist_id):
    """Create a new report and add to existing watchlist"""
    builder = Report.create(api, "SDK UAT: Unsigned Browsers", "SDK UAT: Unsigned processes impersonating browsers", 5)
    builder.add_tag("compliance").add_tag("unsigned_browsers")
    builder.add_ioc(IOC_V2.create_query(api, "unsigned-chrome",
                                        "process_name:chrome.exe NOT "
                                        "process_publisher_state:FILE_SIGNATURE_STATE_SIGNED"))
    report = builder.build()
    report.save_watchlist()

    watchlist = api.select('Watchlist', watchlist_id)
    watchlist.add_reports([report])
    watchlist.save()


def main():
    """Entry function for testing"""
    parser = build_cli_parser()
    args = parser.parse_args()
    api = get_cb_cloud_object(args)

    watchlist_id = create_report_in_watchlist(api)
    add_new_report_to_existing_watchlist(api, watchlist_id)

    feed_id = create_report_in_feed(api)
    add_feed_to_watchlist_and_ignore_report(api, feed_id)
    # get_unsubscribed_feeds(api)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
