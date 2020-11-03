"""Validates result dictionaries, creates Reports, validates Reports, and sends them to an Enterprise EDR Feed.

Also allows for conversion from result dictionaries into Enterprise EDR `Report` objects.
"""

import logging
import json
from cbc_sdk import CBCloudAPI
from cbc_sdk.enterprise_edr import Report
from cbc_sdk.errors import ApiError
from cbc_sdk.enterprise_edr import Feed
from schema import SchemaError
try:
    from schemas import ReportSchema
    from results import AnalysisResult
# allow for using ThreatIntel on it's own
except ImportError:
    from .schemas import ReportSchema
    from .results import AnalysisResult

log = logging.getLogger(__name__)


class ThreatIntel:
    def __init__(self):
        self.cb = CBCloudAPI(timeout=200)

    def verify_feed_exists(self, feed_id):
        """Verify that a Feed exists."""
        try:
            feed = self.cb.select(Feed, feed_id)
            return feed
        except ApiError:
            raise ApiError

    def push_to_cb(self, feed_id, results):
        """Send result.AnalysisResult Reports or a Report dictionary to a Feed."""
        feed = self.verify_feed_exists(feed_id)  # will raise an ApiError if the feed cannot be found
        if not feed:
            return
        report_list_to_send = []
        reports = []
        malformed_reports = []

        for result in results:
            report_dict = {}
            # convert to a dictionary if necessary
            if isinstance(result, AnalysisResult):
                try:
                    report_dict = {
                        "id": str(result.id),
                        "timestamp": int(result.timestamp.timestamp()),
                        "title": str(result.title),
                        "description": str(result.description),
                        "severity": int(result.severity),
                        "iocs_v2": [ioc_v2.as_dict() for ioc_v2 in result.iocs_v2]
                    }
                except Exception as e:
                    log.error(f"Failed to create a report dictionary from result object. {e}")
            # no conversion to dictionary needed
            elif isinstance(result, dict):
                report_dict = result
            try:
                ReportSchema.validate(report_dict)
                # create Enterprise EDR Report object
                report = Report(self.cb, initial_data=report_dict, feed_id=feed_id)
                report_list_to_send.append(report)
                reports.append(report_dict)
            except SchemaError as e:
                log.warning(f"Report Validation failed. Saving report to file for reference. Error: {e}")
                malformed_reports.append(report_dict)


        log.debug(f"Num Reports: {len(report_list_to_send)}")
        try:
            with open('reports.json', 'w') as f:
                json.dump(reports, f, indent=4)
        except Exception as e:
            log.error(f"Failed to write reports to file: {e}")

        log.debug("Sending results to Carbon Black Cloud.")

        if report_list_to_send:
            try:
                feed.append_reports(report_list_to_send)
                log.info(f"Appended {len(report_list_to_send)} reports to Enterprise EDR Feed {feed_id}")
            except Exception as e:
                log.debug(f"Failed sending {len(report_list_to_send)} reports: {e}")

        if malformed_reports:
            log.warning("Some report(s) failed validation. See malformed_reports.json for reports that failed.")
            try:
                with open('malformed_reports.json', 'w') as f:
                    json.dump(malformed_reports, f, indent=4)
            except Exception as e:
                log.error(f"Failed to write malformed_reports to file: {e}")
