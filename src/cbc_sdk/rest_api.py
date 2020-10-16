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

from cbc_sdk.connection import BaseAPI
from cbc_sdk.errors import ApiError, CredentialError, ServerError
from cbc_sdk.live_response_api import LiveResponseSessionManager
from cbc_sdk.audit_remediation import Run, RunHistory
from cbc_sdk.enterprise_edr.threat_intelligence import ReportSeverity
import logging
import time

log = logging.getLogger(__name__)


class CBCloudAPI(BaseAPI):
    """The main entry point into the CBCloudAPI.

    :param str profile: (optional) Use the credentials in the named profile when connecting to the Carbon Black server.
        Uses the profile named 'default' when not specified.

    Usage::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile="production")
    """
    def __init__(self, *args, **kwargs):
        super(CBCloudAPI, self).__init__(*args, **kwargs)
        self._lr_scheduler = None

        if not self.credentials.org_key:
            raise CredentialError("No organization key specified")


    def _perform_query(self, cls, **kwargs):
        if hasattr(cls, "_query_implementation"):
            return cls._query_implementation(self, **kwargs)
        else:
            raise ApiError("All Carbon Black Cloud models must provide _query_implementation")

    # ---- LiveOps

    @property
    def live_response(self):
        if self._lr_scheduler is None:
            self._lr_scheduler = LiveResponseSessionManager(self)
        return self._lr_scheduler

    def _request_lr_session(self, sensor_id):
        return self.live_response.request_session(sensor_id)

    # ---- Audit and Remediation

    def audit_remediation(self, sql):
        return self.select(Run).where(sql=sql)

    def audit_remediation_history(self, query=None):
        return self.select(RunHistory).where(query)

    # ---- Notifications

    def notification_listener(self, interval=60):
        """Generator to continually poll the Cb Endpoint Standard server for notifications (alerts). Note that this can only
        be used with a 'SIEM' key generated in the Cb Endpoint Standard console.
        """
        while True:
            for notification in self.get_notifications():
                yield notification
            time.sleep(interval)

    def get_notifications(self):
        """Retrieve queued notifications (alerts) from the Cb Endpoint Standard server. Note that this can only be used
        with a 'SIEM' key generated in the Cb Endpoint Standard console.

        :returns: list of dictionary objects representing the notifications, or an empty list if none available.
        """
        res = self.get_object("/integrationServices/v3/notification")
        return res.get("notifications", [])

    # ---- Device API

    def _raw_device_action(self, request):
        """
        Invokes the API method for a device action.

        :param dict request: The request body to be passed as JSON to the API method.
        :return: The parsed JSON output from the request.
        :raises ServerError: If the API method returns an HTTP error code.
        """
        url = "/appservices/v6/orgs/{0}/device_actions".format(self.credentials.org_key)
        resp = self.post_object(url, body=request)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 204:
            return None
        else:
            raise ServerError(error_code=resp.status_code, message="Device action error: {0}".format(resp.content))

    def _device_action(self, device_ids, action_type, options=None):
        """
        Executes a device action on multiple device IDs.

        :param list device_ids: The list of device IDs to execute the action on.
        :param str action_type: The action type to be performed.
        :param dict options: Options for the bulk device action.  Default None.
        """
        request = {"action_type": action_type, "device_id": device_ids}
        if options:
            request["options"] = options
        return self._raw_device_action(request)

    def _action_toggle(self, flag):
        """
        Converts a boolean flag value into a "toggle" option.

        :param boolean flag: The value to be converted.
        :return: A dict containing the appropriate "toggle" element.
        """
        if flag:
            return {"toggle": "ON"}
        else:
            return {"toggle": "OFF"}

    def device_background_scan(self, device_ids, scan):
        """
        Set the background scan option for the specified devices.

        :param list device_ids: List of IDs of devices to be set.
        :param boolean scan: True to turn background scan on, False to turn it off.
        """
        return self._device_action(device_ids, "BACKGROUND_SCAN", self._action_toggle(scan))

    def device_bypass(self, device_ids, enable):
        """
        Set the bypass option for the specified devices.

        :param list device_ids: List of IDs of devices to be set.
        :param boolean enable: True to enable bypass, False to disable it.
        """
        return self._device_action(device_ids, "BYPASS", self._action_toggle(enable))

    def device_delete_sensor(self, device_ids):
        """
        Delete the specified sensor devices.

        :param list device_ids: List of IDs of devices to be deleted.
        """
        return self._device_action(device_ids, "DELETE_SENSOR")

    def device_uninstall_sensor(self, device_ids):
        """
        Uninstall the specified sensor devices.

        :param list device_ids: List of IDs of devices to be uninstalled.
        """
        return self._device_action(device_ids, "UNINSTALL_SENSOR")

    def device_quarantine(self, device_ids, enable):
        """
        Set the quarantine option for the specified devices.

        :param list device_ids: List of IDs of devices to be set.
        :param boolean enable: True to enable quarantine, False to disable it.
        """
        return self._device_action(device_ids, "QUARANTINE", self._action_toggle(enable))

    def device_update_policy(self, device_ids, policy_id):
        """
        Set the current policy for the specified devices.

        :param list device_ids: List of IDs of devices to be changed.
        :param int policy_id: ID of the policy to set for the devices.
        """
        return self._device_action(device_ids, "UPDATE_POLICY", {"policy_id": policy_id})

    def device_update_sensor_version(self, device_ids, sensor_version):
        """
        Update the sensor version for the specified devices.

        :param list device_ids: List of IDs of devices to be changed.
        :param dict sensor_version: New version properties for the sensor.
        """
        return self._device_action(device_ids, "UPDATE_SENSOR_VERSION", {"sensor_version": sensor_version})

    # ---- Alerts API

    def alert_search_suggestions(self, query):
        """
        Returns suggestions for keys and field values that can be used in a search.

        :param query str: A search query to use.
        :return: A list of search suggestions expressed as dict objects.
        """
        query_params = {"suggest.q": query}
        url = "/appservices/v6/orgs/{0}/alerts/search_suggestions".format(self.credentials.org_key)
        output = self.get_object(url, query_params)
        return output["suggestions"]

    def _bulk_threat_update_status(self, threat_ids, status, remediation, comment):
        """
        Update the status of alerts associated with multiple threat IDs, past and future.

        :param list threat_ids: List of string threat IDs.
        :param str status: The status to set for all alerts, either "OPEN" or "DISMISSED".
        :param str remediation: The remediation state to set for all alerts.
        :param str comment: The comment to set for all alerts.
        """
        if not all(isinstance(t, str) for t in threat_ids):
            raise ApiError("One or more invalid threat ID values")
        request = {"state": status, "threat_id": threat_ids}
        if remediation is not None:
            request["remediation_state"] = remediation
        if comment is not None:
            request["comment"] = comment
        url = "/appservices/v6/orgs/{0}/threat/workflow/_criteria".format(self.credentials.org_key)
        resp = self.post_object(url, body=request)
        output = resp.json()
        return output["request_id"]

    def bulk_threat_update(self, threat_ids, remediation=None, comment=None):
        """
        Update the alert status of alerts associated with multiple threat IDs.
        The alerts will be left in an OPEN state after this request.

        :param threat_ids list: List of string threat IDs.
        :param remediation str: The remediation state to set for all alerts.
        :param comment str: The comment to set for all alerts.
        :return: The request ID, which may be used to select a WorkflowStatus object.
        """
        return self._bulk_threat_update_status(threat_ids, "OPEN", remediation, comment)

    def bulk_threat_dismiss(self, threat_ids, remediation=None, comment=None):
        """
        Dismiss the alerts associated with multiple threat IDs.
        The alerts will be left in a DISMISSED state after this request.

        :param threat_ids list: List of string threat IDs.
        :param remediation str: The remediation state to set for all alerts.
        :param comment str: The comment to set for all alerts.
        :return: The request ID, which may be used to select a WorkflowStatus object.
        """
        return self._bulk_threat_update_status(threat_ids, "DISMISSED", remediation, comment)

    # ---- ThreathHunter

    def create(self, cls, data=None):
        """Creates a new model.

        >>> feed = cb.create(Feed, feed_data)

        :param cls: The model being created
        :param data: The data to pre-populate the model with
        :type data: dict(str, object)
        :return: an instance of `cls`
        """
        return cls(self, initial_data=data)

    def validate_process_query(self, query):
        """Validates the given IOC query.

        >>> cb.validate_query("process_name:chrome.exe") # True

        :param str query: the query to validate
        :return: whether or not the query is valid
        :rtype: bool
        """
        args = {"q": query}
        url = "/api/investigate/v1/orgs/{}/processes/search_validation".format(
            self.credentials.org_key
        )
        resp = self.get_object(url, query_parameters=args)

        return resp.get("valid", False)

    def convert_feed_query(self, query):
        """Converts a legacy CB Response query to a ThreatHunter query.

        :param str query: the query to convert
        :return: the converted query
        :rtype: str
        """
        args = {"query": query}
        resp = self.post_object("/threathunter/feedmgr/v2/query/translate", args).json()

        return resp.get("query")

    @property
    def custom_severities(self):
        """Returns a list of active :py:class:`ReportSeverity` instances

        :rtype: list[:py:class:`ReportSeverity`]
        """
        # TODO(ww): There's probably a better place to put this.
        url = "/threathunter/watchlistmgr/v3/orgs/{}/reports/severity".format(
            self.credentials.org_key
        )
        resp = self.get_object(url)
        items = resp.get("results", [])
        return [self.create(ReportSeverity, item) for item in items]

    def fetch_process_queries(self):
        """Retrieves a list of queries, active or complete, known by
        the ThreatHunter server.

        :return: a list of query ids
        :rtype: list(str)
        """
        url = "/api/investigate/v1/orgs/{}/processes/search_jobs".format(
            self.credentials.org_key
        )
        ids = self.get_object(url)
        return ids.get("query_ids", [])

    def process_limits(self):
        """Returns a dictionary containing API limiting information.

        Example:

        >>> cb.limits()
        {u'status_code': 200, u'time_bounds': {u'upper': 1545335070095, u'lower': 1542779216139}}

        :return: a dict of limiting information
        :rtype: dict(str, str)
        """
        url = "/api/investigate/v1/orgs/{}/processes/limits".format(
            self.credentials.org_key
        )
        return self.get_object(url)
