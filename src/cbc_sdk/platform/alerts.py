#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Platform Alerts and Workflows"""
import time
import datetime

from cbc_sdk.errors import ApiError, ObjectNotFoundError, NonQueryableModel, FunctionalityDecommissioned
from cbc_sdk.platform import PlatformModel
from cbc_sdk.base import (BaseQuery,
                          QueryBuilder,
                          QueryBuilderSupportMixin,
                          IterableQueryMixin,
                          CriteriaBuilderSupportMixin,
                          ExclusionBuilderSupportMixin
                          )
from cbc_sdk.platform.observations import Observation
from cbc_sdk.platform.processes import AsyncProcessQuery, Process
from cbc_sdk.platform.legacy_alerts import LegacyAlertSearchQueryCriterionMixin
from cbc_sdk.platform.jobs import Job

from backports._datetime_fromisoformat import datetime_fromisoformat

"""Alert Models"""

MAX_RESULTS_LIMIT = 10000


class Alert(PlatformModel):
    """Represents a basic alert."""
    REMAPPED_ALERTS_V6_TO_V7 = {
        "alert_classification.user_feedback": "determination_value",
        "cluster_name": "k8s_cluster",
        "create_time": "backend_timestamp",
        "created_by_event_id": "primary_event_id",
        "first_event_time": "first_event_timestamp",
        "last_event_time": "last_event_timestamp",
        "last_update_time": "backend_update_timestamp",
        "legacy_alert_id": "id",
        "namespace": "k8s_namespace",
        "notes_present": "alert_notes_present",
        "policy_id": "device_policy_id",
        "policy_name": "device_policy",
        "port": "netconn_local_port",
        "protocol": "netconn_protocol",
        "remote_domain": "netconn_remote_domain",
        "remote_ip": "netconn_remote_ip",
        "remote_namespace": "remote_k8s_namespace",
        "remote_replica_id": "remote_k8s_pod_name",
        "remote_workload_kind": "remote_k8s_kind",
        "remote_workload_name": "remote_k8s_workload_name",
        "replica_id": "k8s_pod_name",
        "rule_id": "rule_id ",
        "run_state": "run_state",
        "target_value": "device_target_value",
        "threat_cause_actor_certificate_authority": "process_issuer",
        "threat_cause_actor_name": "process_name",
        "threat_cause_actor_publisher": "process_publisher",
        "threat_cause_actor_sha256": "process_sha256",
        "threat_cause_cause_event_id": "primary_event_id",
        "threat_cause_md5": "process_md5",
        "threat_cause_parent_guid": "parent_guid",
        "threat_cause_reputation": "process_reputation",
        "threat_indicators": "ttps",
        "watchlists": "watchlists.id",
        "workflow.last_update_time": "workflow.change_timestamp",
        "workflow.state": "workflow.status",
        "workload_kind": "k8s_kind",
        "workload_name": "k8s_workload_name"
    }

    REMAPPED_ALERTS_V7_TO_V6 = {
        "alert_notes_present": "notes_present",
        "backend_timestamp": "create_time",
        "backend_update_timestamp": "last_update_time",
        "determination_value": "alert_classification.user_feedback",
        "device_policy": "policy_name",
        "device_policy_id": "policy_id",
        "device_target_value": "target_value",
        "first_event_timestamp": "first_event_time",
        "k8s_cluster": "cluster_name",
        "k8s_kind": "workload_kind",
        "k8s_namespace": "namespace",
        "k8s_pod_name": "replica_id",
        "k8s_workload_name": "workload_name",
        "last_event_timestamp": "last_event_time",
        "netconn_local_port": "port",
        "netconn_protocol": "protocol",
        "netconn_remote_domain": "remote_domain",
        "netconn_remote_ip": "remote_ip",
        "parent_guid": "threat_cause_parent_guid",
        "primary_event_id": "threat_cause_cause_event_id",
        "process_guid": "threat_cause_process_guid",
        "process_issuer": "threat_cause_actor_certificate_authority",
        "process_md5": "threat_cause_actor_md5",
        "process_name": "threat_cause_actor_name",
        "process_publisher": "threat_cause_actor_publisher",
        "process_reputation": "threat_cause_reputation",
        "process_sha256": "threat_cause_actor_sha256",
        "remote_k8s_kind": "remote_workload_kind",
        "remote_k8s_namespace": "remote_namespace",
        "remote_k8s_pod_name": "remote_replica_id",
        "remote_k8s_workload_name": "remote_workload_name",
        "rule_id ": "rule_id",
        "run_state": "run_state",
        "ttps": "threat_indicators",
        "watchlists.id": "watchlists",
        "workflow.change_timestamp": "workflow.last_update_time",
        "workflow.status": "workflow.state"
    }

    DEPRECATED_FIELDS_NOT_IN_V7 = [
        "category",
        "group_details",
        "alert_classification.classification",
        "alert_classification.global_prevalence",
        "alert_classification.org_prevalence",
        # CB Analytics Fields
        "blocked_threat_category",
        "kill_chain_status",
        "not_blocked_threat_category",
        "threat_activity_c2",
        "threat_activity_dlp",
        "threat_activity_phish",
        # CB Analytics and Host Based Firewall and Device Control and Watchlist
        "threat_cause_threat_category",
        # CB Analytics and Device Control and Watchlist
        "threat_cause_vector",
        # Container Runtime Fields
        "workload_id",
        # Watchlists Fields
        "count",
        "document_guid",
        "threat_indicators",
        "workflow.comment"
    ]

    REMAPPED_CONTAINER_ALERTS_V7_TO_V6 = {
        "k8s_policy_id": "policy_id",
        "k8s_policy": "policy_name",
        "k8s_rule_id": "rule_id",
        "k8s_rule": "rule_name"
    }

    REMAPPED_CONTAINER_ALERTS_V6_TO_V7 = {
        "policy_id": "k8s_policy_id",
        "policy_name": "k8s_policy",
        "rule_id": "k8s_rule_id",
        "rule_name": "k8s_rule"
    }

    # these fields are deprecated from container runtime but mapped to a new field for other alert types
    DEPRECATED_FIELDS_NOT_IN_V7_CONTAINER_ONLY = [
        "target_value"
    ]

    REMAPPED_WORKFLOWS_V7_TO_V6 = {
        "change_timestamp": "last_update_time",
        "status": "state",
        "closure_reason": "remediation"
    }

    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    urlobject_single = "/api/alerts/v7/orgs/{0}/alerts/{1}"
    threat_urlobject_single = "/api/alerts/v7/orgs/{0}/threats/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/alert.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Alert object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(Alert, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    def get_process(self, async_mode=False):
        """
        Gets the process corresponding with the alert.

        Args:
            async_mode: True to request process in an asynchronous manner.

        Returns:
            Process: The process corresponding to the alert.
        """
        process_guid = self._info.get("process_guid")
        if not process_guid:
            raise ApiError(f"Trying to get process details on an invalid process_id {process_guid}")
        if async_mode:
            return self._cb._async_submit(self._get_process)
        return self._get_process()

    def _get_process(self, *args, **kwargs):
        """
        Implementation of the get_process.

        Returns:
            Process: The process corresponding to the alert. May return None if no process is found.
        """
        process_guid = self._info.get("process_guid")
        try:
            process = AsyncProcessQuery(Process, self._cb).where(process_guid=process_guid).one()
        except ObjectNotFoundError:
            return None
        return process

    def get_observations(self, timeout=0):
        """Requests observations that are associated with the Alert.

         Uses Observations bulk get details.

        Returns:
            list: Observations associated with the alert

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.
        """
        alert_id = self.get("id")
        if not alert_id:
            raise ApiError("Trying to get observations on an invalid alert_id {}".format(alert_id))

        obs = Observation.bulk_get_details(self._cb, alert_id=alert_id, timeout=timeout)
        return obs

    def get_history(self, threat=False):
        """
        Get the actions taken on an Alert such as Notes added and workflow state changes.

        Args:
            threat (bool): Whether to return the Alert or Threat history

        Returns:
            list: The dicts of each determination, note or workflow change

        """
        if threat:
            url = Alert.threat_urlobject_single.format(self._cb.credentials.org_key, self.threat_id)
        else:
            url = Alert.urlobject_single.format(self._cb.credentials.org_key, self._info[self.primary_key])

        url = f"{url}/history"
        resp = self._cb.get_object(url)
        return resp.get("history", [])

    def get_threat_tags(self):
        """
        Gets the threat's tags

        Required Permissions:
            org.alerts.tags (READ)

        Returns:
            (list[str]): The list of current tags
        """
        url = Alert.threat_urlobject_single.format(self._cb.credentials.org_key, self.threat_id)
        url = f"{url}/tags"
        resp = self._cb.get_object(url)
        return resp.get("list", [])

    def add_threat_tags(self, tags):
        """
        Adds tags to the threat

        Required Permissions:
            org.alerts.tags (CREATE)

        Args:
            tags (list[str]): List of tags to add to the threat

        Raises:
            ApiError: If tags is not a list of strings

        Returns:
            (list[str]): The list of current tags
        """
        if not isinstance(tags, list) or not isinstance(tags[0], str):
            raise ApiError("Tags must be a list of strings")

        url = Alert.threat_urlobject_single.format(self._cb.credentials.org_key, self.threat_id)
        url = f"{url}/tags"
        resp = self._cb.post_object(url, {"tags": tags})
        resp_json = resp.json()
        return resp_json.get("tags", [])

    def delete_threat_tag(self, tag):
        """
        Delete a threat tag

        Required Permissions:
            org.alerts.tags (DELETE)

        Args:
            tag (str): The tag to delete

        Returns:
            (list[str]): The list of current tags
        """
        url = Alert.threat_urlobject_single.format(self._cb.credentials.org_key, self.threat_id)
        url = f"{url}/tags/{tag}"
        resp = self._cb.delete_object(url)
        resp_json = resp.json()
        return resp_json.get("tags", [])

    class Note(PlatformModel):
        """Represents a note within an alert."""
        REMAPPED_NOTES_V6_TO_V7 = {
            "create_time": "create_timestamp",
        }

        REMAPPED_NOTES_V7_TO_V6 = {
            "create_timestamp": "create_time",
        }

        urlobject = "/api/alerts/v7/orgs/{0}/alerts/{1}/notes"
        threat_urlobject = "/api/alerts/v7/orgs/{0}/threats/{1}/notes"
        primary_key = "id"
        swagger_meta_file = "platform/models/alert_note.yaml"
        _is_deleted = False

        def __init__(self, cb, alert, model_unique_id, threat_note=False, initial_data=None):
            """
            Initialize the Note object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                alert (Alert): The alert where the note is saved.
                model_unique_id (str): ID of the note represented.
                threat_note (bool): Whether the note is an Alert or Threat note
                initial_data (dict): Initial data used to populate the note.
            """
            super(Alert.Note, self).__init__(cb, model_unique_id, initial_data)
            self._alert = alert
            self._threat_note = threat_note
            if model_unique_id is not None and initial_data is None:
                self._refresh()

        def _refresh(self):
            """
            Rereads the alert data from the server.

            Returns:
                bool: True if refresh was successful, False if not.
            """
            _exists_in_list = False
            if self._is_deleted:
                raise ApiError("Cannot refresh a deleted Note")

            if self._threat_note:
                if self._alert.threat_id:
                    url = Alert.Note.threat_urlobject.format(self._cb.credentials.org_key, self._alert.threat_id)
                else:
                    url = self.url
                    raise ObjectNotFoundError(url, "Cannot refresh: threat_id not found")
            else:
                url = Alert.Note.urlobject.format(self._cb.credentials.org_key, self._alert.id)

            resp = self._cb.get_object(url)
            item_list = resp.get("results", [])

            for item in item_list:
                if item["id"] == self.id:
                    _exists_in_list = True
                    return True

            if not _exists_in_list:
                raise ObjectNotFoundError(url, "Cannot refresh: Note not found")

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            Raises an error, as Notes cannot be queried directly.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                ApiError: Always.
            """
            raise NonQueryableModel("Notes cannot be queried directly")

        def delete(self):
            """Deletes a note from an alert."""
            if self._threat_note:
                url = self.threat_urlobject.format(self._cb.credentials.org_key, self._alert.threat_id)
            else:
                url = self.urlobject.format(self._cb.credentials.org_key, self._alert.id)

            url = f"{url}/{self.id}"
            self._cb.delete_object(url)
            self._is_deleted = True

        def __getitem__(self, item):
            """
            Return an attribute of this object.

            Args:
                item (str): Name of the attribute to be returned.

            Returns:
                Any: The returned attribute value.

            Raises:
                AttributeError: If the object has no such attribute.
            """
            try:
                return super(Alert.Note, self).__getattribute__(Alert.Note.REMAPPED_NOTES_V6_TO_V7.get(item, item))
            except AttributeError:
                raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                                  item))
                # fall through to the rest of the logic...

        def __getattr__(self, item):
            """
            Return an attribute of this object.

            Args:
                item (str): Name of the attribute to be returned.

            Returns:
                Any: The returned attribute value.

            Raises:
                AttributeError: If the object has no such attribute.
            """
            try:
                item = Alert.Note.REMAPPED_NOTES_V6_TO_V7.get(item, item)
                return super(Alert.Note, self).__getattr__(Alert.Note.REMAPPED_NOTES_V6_TO_V7.get(item, item))
            except AttributeError:
                raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                                  item))
                # fall through to the rest of the logic...

    def notes_(self, threat_note=False):
        """
        Retrieves all notes for an alert.

        Args:
            threat_note (bool): Whether to return the Alert notes or Threat notes
        """
        if threat_note:
            url = Alert.Note.threat_urlobject.format(self._cb.credentials.org_key, self.threat_id)
        else:
            url = Alert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])

        resp = self._cb.get_object(url)
        item_list = resp.get("results", [])
        return [Alert.Note(self._cb, self, item[Alert.Note.primary_key], threat_note, item)
                for item in item_list]

    def create_note(self, note, threat_note=False):
        """
        Creates a new note.

        Args:
            note (str): Note content to add
            threat_note (bool): Whether to add the note to the Alert or Threat
        """
        request = {"note": note}
        if threat_note:
            url = Alert.Note.threat_urlobject.format(self._cb.credentials.org_key, self.threat_id)
        else:
            url = Alert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])
        resp = self._cb.post_object(url, request)
        result = resp.json()
        return Alert.Note(self._cb, self, result["id"], threat_note, result)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the alert data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    @property
    def workflow_(self):
        """
        Returns the workflow associated with this alert.

        Returns:
            dict: The workflow associated with this alert.
        """
        return self.workflow

    def close(self, closure_reason=None, determination=None, note=None):
        """
        Closes this alert.

        Args:
            closure_reason (str): the closure reason for this alert, either "NO_REASON", "RESOLVED", \
            "RESOLVED_BENIGN_KNOWN_GOOD", "DUPLICATE_CLEANUP", "OTHER"
            determination (str): The determination status to set for the alert, either "TRUE_POSITIVE", \
            "FALSE_POSITIVE", or "NONE"
            note (str): The comment to set for the alert.

        Note:
            - This is an asynchronus call that returns a Job. If you want to wait and block on the results
              you can call await_completion() to get a Futre then result() on the future object to wait for
              completion and get the results.

        Example:
            >>> alert = cb.select(Alert, "708d7dbf-2020-42d4-9cbc-0cddd0ffa31a")
            >>> job = alert.close("RESOLVED", "FALSE_POSITIVE", "Normal behavior")
            >>> completed_job = job.await_completion().result()
            >>> alert.refresh()

        Returns:
            Job: The Job object for the alert workflow action.
        """
        job = self._cb.select(Alert).add_criteria("id", [self.get("id")]) \
                                    ._update_status("CLOSED", closure_reason, note, determination)

        self._last_refresh_time = time.time()
        return job

    def update(self, status, closure_reason=None, determination=None, note=None):
        """
        Update the Alert with optional closure_reason, determination, note, or status.

        Args:
            status (str): The status to set for this alert, either "OPEN", "IN_PROGRESS", or "CLOSED".
            closure_reason (str): the closure reason for this alert, either "NO_REASON", "RESOLVED", \
            "RESOLVED_BENIGN_KNOWN_GOOD", "DUPLICATE_CLEANUP", "OTHER"
            determination (str): The determination status to set for the alert, either "TRUE_POSITIVE", \
            "FALSE_POSITIVE", or "NONE"
            note (str): The comment to set for the alert.

        Note:
            - This is an asynchronus call that returns a Job. If you want to wait and block on the results
              you can call await_completion() to get a Futre then result() on the future object to wait for
              completion and get the results.

        Example:
            >>> alert = cb.select(Alert, "708d7dbf-2020-42d4-9cbc-0cddd0ffa31a")
            >>> job = alert.update("IN_PROGESS", "NO_REASON", "NONE", "Starting Investigation")
            >>> completed_job = job.await_completion().result()
            >>> alert.refresh()

        Returns:
            Job: The Job object for the alert workflow action.
        """
        job = self._cb.select(Alert).add_criteria("id", [self.get("id")]) \
                                    ._update_status(status, closure_reason, note, determination)

        self._last_refresh_time = time.time()
        return job

    def _update_threat_workflow_status(self, state, remediation, comment):
        """
        Updates the workflow status of all future alerts with the same threat ID.

        Args:
            state (str): The state to set for this alert, either "OPEN" or "DISMISSED".
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
        """
        request = {"state": state}
        if remediation:
            request["remediation_state"] = remediation
        if comment:
            request["comment"] = comment
        url = "/appservices/v6/orgs/{0}/threat/workflow/_criteria".format(self._cb.credentials.org_key)
        resp = self._cb.post_object(url, request)
        return resp.json()

    def dismiss_threat(self, remediation=None, comment=None):
        """
        Dismisses all future alerts assigned to the threat_id.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.

        Note:
            - If you want to dismiss all past and current open alerts associated to the threat use the following:
                >>> cb.select(Alert).add_criteria("threat_id", [alert.threat_id]).close(...)
        """
        return self._update_threat_workflow_status("DISMISSED", remediation, comment)

    def update_threat(self, remediation=None, comment=None):
        """
        Updates all future alerts assigned to the threat_id to the OPEN state.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.

        Note:
            - If you want to update all past and current alerts associated to the threat use the following:
                >>> cb.select(Alert).add_criteria("threat_id", [alert.threat_id]).update(...)
        """
        return self._update_threat_workflow_status("OPEN", remediation, comment)

    @staticmethod
    def search_suggestions(cb, query):
        """
        Returns suggestions for keys and field values that can be used in a search.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            query (str): A search query to use.

        Returns:
            list: A list of search suggestions expressed as dict objects.

        Raises:
            ApiError: if cb is not instance of CBCloudAPI
        """
        if cb.__class__.__name__ != "CBCloudAPI":
            raise ApiError("cb argument should be instance of CBCloudAPI.")
        query_params = {"suggest.q": query}
        url = "/api/alerts/v7/orgs/{0}/alerts/search_suggestions".format(cb.credentials.org_key)
        output = cb.get_object(url, query_params)
        return output["suggestions"]

    def __getitem__(self, item):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.

        Returns:
            Any: The returned attribute value.

        Raises:
            AttributeError: If the object has no such attribute.
        """
        try:
            return super(Alert, self).__getattribute__(Alert.REMAPPED_ALERTS_V6_TO_V7.get(item, item))
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))
            # fall through to the rest of the logic...

    def __getattr__(self, item):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.

        Returns:
            Any: The returned attribute value.

        Raises:
            AttributeError: If the object has no such attribute.
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        try:
            original_item = item
            if item in Alert.DEPRECATED_FIELDS_NOT_IN_V7:
                raise FunctionalityDecommissioned(
                    "Attribute '{0}' does not exist in object '{1}' because it was deprecated in "
                    "Alerts v7. In SDK 1.5.0 the".format(item, self.__class__.__name__))
            if item in Alert.DEPRECATED_FIELDS_NOT_IN_V7_CONTAINER_ONLY and self.type == "CONTAINER_RUNTIME":
                raise FunctionalityDecommissioned(
                    "Attribute '{0}' does not exist in object '{1}' because it was deprecated in "
                    "Alerts v7. In SDK 1.5.0 the".format(item, self.__class__.__name__))

            item = Alert.REMAPPED_ALERTS_V6_TO_V7.get(item, item)
            if self.get("type") == "CONTAINER_RUNTIME":
                item = Alert.REMAPPED_CONTAINER_ALERTS_V6_TO_V7.get(original_item, item)
            return super(Alert, self).__getattr__(item)
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))
            # fall through to the rest of the logic...

    def to_json(self, version="v7"):
        """
        Return a json object of the response.

        Args:
            version (str): version of json to return. Either v6 or v7. DEFAULT v7

        Returns:
            Any: The returned attribute value.
        """
        if version == "v6":
            modified_json = {}
            for key, value in self._info.items():
                if self.type == "CONTAINER_RUNTIME":
                    key = Alert.REMAPPED_CONTAINER_ALERTS_V7_TO_V6.get(key, key)
                modified_json[Alert.REMAPPED_ALERTS_V7_TO_V6.get(key, key)] = value
                if key == "id":
                    modified_json["legacy_alert_id"] = value
                if key == "process_name":
                    modified_json["process_name"] = value
                if key == "primary_event_id":
                    if self.type == "CB_ANALYTICS":
                        modified_json["created_by_event_id"] = value
                if key == "process_guid":
                    if self.type == "WATCHLIST":
                        modified_json["process_guid"] = value
                    if self.type == "CB_ANALYTICS":
                        modified_json["threat_cause_process_guid"] = value
                if key == "ttps":
                    ti = {"process_name": self._info.get("process_name"), "sha256": self._info.get("process_sha256"),
                          "ttps": value}
                    modified_json["threat_indicators"] = [ti]
                if key == "workflow":
                    wf = {}
                    for wf_key, wf_value in value.items():
                        if wf_key == "status" and wf_value == "CLOSED":
                            wf_value = "DISMISSED"
                        elif wf_key == "status" and wf_value == "IN_PROGRESS":
                            wf_value = "OPEN"
                        wf[Alert.REMAPPED_WORKFLOWS_V7_TO_V6.get(wf_key, wf_key)] = wf_value
                    modified_json[key] = wf
            return modified_json
        else:
            return self._info

    def get(self, item, default_val=None):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.
            default_val (Any): Default value to be used if the attribute is not set.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.

        Returns:
            Any: The returned attribute value, which may be defaulted.
        """
        if item in Alert.DEPRECATED_FIELDS_NOT_IN_V7:
            raise FunctionalityDecommissioned(
                "Attribute '{0}' does not exist in object '{1}' because it was deprecated in "
                "Alerts v7. In SDK 1.5.0 the".format(item, self.__class__.__name__))
        return super(Alert, self).get(item, default_val)


class WatchlistAlert(Alert):
    """Represents watch list alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    type = ["WATCHLIST"]
    swagger_meta_file = "platform/models/alert_watchlist.yaml"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["WATCHLIST"])


class CBAnalyticsAlert(Alert):
    """Represents CB Analytics alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    type = ["CB_ANALYTICS"]
    swagger_meta_file = "platform/models/alert_cb_analytic.yaml"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["CB_ANALYTICS"])

    def get_events(self, timeout=0, async_mode=False):
        """Removed in CBC SDK 1.5.0 because Enriched Events are deprecated.

        Previously requested enriched events detailed results.  Update to use get_observations() instead.
        See `Developer Network Observations Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/observations-migration>`_
        for more details.

        Args:
            timeout (int): Event details request timeout in milliseconds.
            async_mode (bool): True to request details in an asynchronous manner.

        Returns:
            list: EnrichedEvents matching the legacy_alert_id

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("get_events method does not exist in in SDK v1.5.0 "
                                          "because Enriched Events have been deprecated.  The")


class DeviceControlAlert(Alert):
    """Represents Device Control alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    swagger_meta_file = "platform/models/alert_device_control.yaml"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["DEVICE_CONTROL"])


class ContainerRuntimeAlert(Alert):
    """Represents Container Runtime alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    swagger_meta_file = "platform/models/alert_container_runtime.yaml"
    type = ["CONTAINER_RUNTIME"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["CONTAINER_RUNTIME"])


class HostBasedFirewallAlert(Alert):
    """Represents Host Based Firewall alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    swagger_meta_file = "platform/models/alert_host_based_firewall.yaml"
    type = ["HOST_BASED_FIREWALL"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["HOST_BASED_FIREWALL"])


class IntrusionDetectionSystemAlert(Alert):
    """Represents Intrusion Detection System alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    swagger_meta_file = "platform/models/alert_intrusion_detection_system.yaml"
    type = ["INTRUSION_DETECTION_SYSTEM"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AlertSearchQuery: The query object for this alert type.
        """
        return AlertSearchQuery(cls, cb).add_criteria("type", ["INTRUSION_DETECTION_SYSTEM"])


class GroupedAlert(PlatformModel):
    """Represents Grouped alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/grouped_alerts"
    swagger_meta_file = "platform/models/grouped_alert.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Grouped Alert object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(GroupedAlert, self).__init__(cb, model_unique_id, initial_data)
        self._most_recent_alert = None
        self._request = None

        most_recent_alert = initial_data["most_recent_alert"]
        if "type" in most_recent_alert:
            if most_recent_alert["type"] == "CB_ANALYTICS":
                self._most_recent_alert = CBAnalyticsAlert(cb, most_recent_alert["id"], most_recent_alert)
            elif most_recent_alert["type"] == "WATCHLIST":
                self._most_recent_alert = WatchlistAlert(cb, most_recent_alert["id"], most_recent_alert)
            elif most_recent_alert["type"] == "INTRUSION_DETECTION_SYSTEM":
                self._most_recent_alert = IntrusionDetectionSystemAlert(cb, most_recent_alert["id"], most_recent_alert)
            elif most_recent_alert["type"] == "DEVICE_CONTROL":
                self._most_recent_alert = DeviceControlAlert(cb, most_recent_alert["id"], most_recent_alert)
            elif most_recent_alert["type"] == "HOST_BASED_FIREWALL":
                self._most_recent_alert = HostBasedFirewallAlert(cb, most_recent_alert["id"], most_recent_alert)
            elif most_recent_alert["type"] == "CONTAINER_RUNTIME":
                self._most_recent_alert = ContainerRuntimeAlert(cb, most_recent_alert["id"], most_recent_alert)
            else:
                self._most_recent_alert = Alert(cb, most_recent_alert["id"], most_recent_alert)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            GroupAlertSearchQuery: The query object for this alert type.
        """
        return GroupedAlertSearchQuery(cls, cb)

    @property
    def most_recent_alert_(self):
        """
        Returns the most recent alert for a given group alert.

        Returns:
            Alert: the most recent alert in the Group Alert.
        """
        return self._most_recent_alert

    def get_alert_search_query(self):
        """
        Returns the Alert Search Query needed to pull all alerts for a given Group Alert.

        Returns:
            AlertSearchQuery: for all alerts associated with the calling group alert.
        """
        ignored_keys = ["_doc_class", "_cb", "_count_valid", "_total_results"]
        alert_search_query = self._cb.select(Alert)
        for key, value in vars(alert_search_query).items():
            if hasattr(self._request, key) and key not in ignored_keys:
                setattr(alert_search_query, key, self._request.__getattribute__(key))
        key = "_time_range"
        if hasattr(self._request, key):
            setattr(alert_search_query, key, self._request.__getattribute__(key))

        alert_search_query.add_criteria(self._request._group_by.lower(), self.most_recent_alert["threat_id"])
        return alert_search_query

    def get_alerts(self):
        """
        Returns the all alerts for a given Group Alert.

        Returns:
            list: alerts associated with the calling group alert.
        """
        return self.get_alert_search_query().all()


"""Alert Queries"""


class AlertSearchQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, LegacyAlertSearchQueryCriterionMixin,
                       CriteriaBuilderSupportMixin, ExclusionBuilderSupportMixin):
    """Represents a query that is used to locate Alert objects."""
    DEPRECATED_FACET_FIELDS = ["ALERT_TYPE", "CATEGORY", "REPUTATION", "WORKFLOW", "TAG", "POLICY_ID",
                               "POLICY_NAME", "APPLICATION_HASH", "APPLICATION_NAME", "STATUS", "POLICY_APPLIED_STATE"]

    def __init__(self, doc_class, cb):
        """
        Initialize the AlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        self._valid_criteria = False
        super(AlertSearchQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filters = {}
        self._exclusions = {}
        self._time_exclusion_filters = {}
        self._sortcriteria = {}
        self._bulkupdate_url = "/api/alerts/v7/orgs/{0}/alerts/workflow"
        self._count_valid = False
        self._total_results = 0
        self._batch_size = 100

    def set_rows(self, rows):
        """
        Sets the 'rows' query body parameter, determining how many rows of results to request.

        Args:
            rows (int): How many rows to request.
        """
        if not isinstance(rows, int):
            raise ApiError(f"Rows must be an integer. {rows} is a {type(rows)}.")
        self._batch_size = rows
        return self

    def set_time_range(self, *args, **kwargs):
        """
        For v7 Alerts:

        Sets the 'time_range' query body parameter, determining a time range based on 'backend_timestamp'.

        Args:
            *args: not used
            **kwargs (dict): Used to specify the period to search within

                * start= either timestamp ISO 8601 strings or datetime objects
                * end= either timestamp ISO 8601 strings or datetime objects
                * range= the period on which to execute the result search, ending on the current time.

                Range must be in the format "-<quantity><units>" where quantity is an integer, and units is one of:

                * M: month(s)
                * w: week(s)
                * d: day(s)
                * h: hour(s)
                * m: minute(s)
                * s: second(s)

        For v6 Alerts (backwards compatibility):

        Restricts the alerts that this query is performed on to the specified time range for a given key. Will set
        the 'time_range' as in the v7 usage if key is create_time and set a criteria value for any other valid key.

        Args:
            key (str): The key to use for criteria one of create_time, first_event_time, last_event_time
             or last_update_time. i.e. legacy field names from the Alert v6 API.
            **kwargs (dict): Used to specify the period to search within

                * start= either timestamp ISO 8601 strings or datetime objects
                * end= either timestamp ISO 8601 strings or datetime objects
                * range= the period on which to execute the result search, ending on the current time.

        Returns:
            AlertSearchQuery: This instance.

        Examples:
            >>> query_specify_start_and_end = api.select(Alert).
            ...     set_time_range(start="2020-10-20T20:34:07Z", end="2020-10-30T20:34:07Z")
            >>> query_specify_range = api.select(Alert).set_time_range(range='-3d')
            >>> query_legacy_use = api.select(Alert).set_time_range("create_time", range='-3d')

        """
        args_count = args.__len__()
        time_filter = self._create_valid_time_filter(kwargs)
        if args_count > 0:
            key = args[0]
            self._valid_criteria = self._is_valid_time_criteria_key_v6(key)
            if self._valid_criteria:
                key = Alert.REMAPPED_ALERTS_V6_TO_V7.get(key, key)
                # key has been converted so v6 values are not expected here
                if key in ["backend_timestamp"]:
                    self._time_range = time_filter
                else:
                    self.add_time_criteria(key, **kwargs)
        else:
            # everything before this is only for backwards compatibility, once v6 deprecates all the other
            # checks can be removed
            self._time_range = {}
            self._time_range = time_filter
        return self

    def add_time_criteria(self, key, **kwargs):
        """
        Restricts the alerts that this query is performed on to the specified time range for a given key.

        The time may either be specified as a start and end point or as a range.

        Args:
            key (str): The key to use for criteria one of create_time, first_event_time, last_event_time,
             backend_update_timestamp, or last_update_time
            **kwargs (dict): Used to specify:

                * start= for start time
                * end= for end time
                * range= for range
                * excludes= to set this as an exclusion rather than criteria. Defaults to False.

        Returns:
            AlertSearchQuery: This instance.

        Examples:
            >>> query = api.select(Alert).
            ...     add_time_criteria("detection_timestamp", start="2020-10-20T20:34:07Z", end="2020-10-30T20:34:07Z")
            >>> second_query = api.select(Alert).add_time_criteria("detection_timestamp", range='-3d')
            >>> third_query_legacy = api.select(Alert).set_time_range("create_time", range='-3d')
            >>> exclusions_query = api.add_time_criteria("detection_timestamp", range="-2h", exclude=True)

        """
        # this first if statement will be removed after v6 is deprecated
        if not self._valid_criteria:
            self._valid_criteria = self._is_valid_time_criteria_key(key)

        if self._valid_criteria:
            if kwargs.get("exclude", False):
                self._time_exclusion_filters[key] = self._create_valid_time_filter(kwargs)
            else:
                self._time_filters[key] = self._create_valid_time_filter(kwargs)
        return self

    def _is_valid_time_criteria_key(self, key):
        """
        Verifies that an alert criteria key is a valid searchable time range field

        Args:
            args (str): The key to use for criteria must be a valid v7 time range field; backend_update_timestamp,
            detection_timestamp, first_event_timestamp, last_event_timestamp, mdr_determination_change_timestamp,
            mdr_workflow_change_timestamp, user_update_timestamp, or workflow_change_timestamp

        Returns:
            boolean true
        """
        if key not in ["backend_update_timestamp", "detection_timestamp", "first_event_timestamp",
                       "last_event_timestamp", "mdr_determination_change_timestamp", "mdr_workflow_change_timestamp",
                       "user_update_timestamp", "workflow_change_timestamp"]:
            raise ApiError("key must be one of backend_update_timestamp, detection_timestamp, "
                           "first_event_timestamp, last_event_timestamp, mdr_determination_change_timestamp, "
                           "mdr_workflow_change_timestamp, user_update_timestamp, or workflow_change_timestamp")
        return True

    def _is_valid_time_criteria_key_v6(self, key):
        """
        Verifies that an alert criteria key has the timerange functionality for v6 sdk calls.

        Only v6 field names are valid.

        Args:
            args (str): The key to use for criteria one of create_time, first_event_time, last_event_time,
             backend_timestamp, backend_update_timestamp, or last_update_time

        Returns:
            boolean true
        """
        if key not in ["create_time", "first_event_time", "last_event_time", "last_update_time"]:
            raise ApiError("key must be one of create_time, first_event_time, last_event_time or last_update_time")
        return True

    def _create_valid_time_filter(self, kwargs):
        """
        Verifies that an alert criteria key has the timerange functionality

        Args:
            kwargs (dict): Used to specify start= for start time, end= for end time, and range= for range. Values are
            either timestamp ISO 8601 strings or datetime objects for start and end time. For range the time range to
            execute the result search, ending on the current time. Should be in the form "-2w",
            where y=year, w=week, d=day, h=hour, m=minute, s=second.

        Returns:
            filter object to be applied to the global time range or a specific field
        """
        time_filter = {}
        if kwargs.get("start", None) and kwargs.get("end", None):
            if kwargs.get("range", None):
                raise ApiError("cannot specify range= in addition to start= and end=")
            stime = kwargs["start"]
            etime = kwargs["end"]
            try:
                if isinstance(stime, str):
                    stime = datetime_fromisoformat(stime)
                if isinstance(etime, str):
                    etime = datetime_fromisoformat(etime)
                if isinstance(stime, datetime.datetime) and isinstance(etime, datetime.datetime):
                    time_filter = {"start": stime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                                   "end": etime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
            except:
                raise ApiError(f"Start and end time must be a string in ISO 8601 format or an object of datetime. "
                               f"Start time {stime} is a {type(stime)}. End time {etime} is a {type(etime)}.")
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            time_filter = {"range": kwargs["range"]}
        else:
            raise ApiError("must specify either start= and end= or range=")
        return time_filter

    def _build_criteria(self):
        """
        Builds the criteria object for use in a query.

        Returns:
            dict: The criteria object.
        """
        mycrit = self._criteria
        if self._time_filters:
            mycrit.update(self._time_filters)
        return mycrit

    def _build_exclusions(self):
        """
        Builds the exclusions object for use in a query.

        Returns:
            dict: The exclusions object.
        """
        myexclusions = self._exclusions
        if self._time_exclusion_filters:
            myexclusions.update(self._time_exclusion_filters)
        return myexclusions

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(Alert).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            AlertSearchQuery: This instance.
        """
        if direction not in CriteriaBuilderSupportMixin.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def _build_request(self, from_row, max_rows, add_sort=True):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.
            add_sort (bool): If True(default), the sort criteria will be added as part of the request.

        Returns:
            dict: The complete request body.
        """
        request = {}
        criteria = self._build_criteria()
        exclusions = self._build_exclusions()
        query = self._query_builder._collapse()
        if criteria:
            request["criteria"] = criteria
        if exclusions:
            request["exclusions"] = exclusions
        if query:
            request["query"] = query

        request["rows"] = self._batch_size
        if hasattr(self, "_time_range"):
            request["time_range"] = self._time_range
        if from_row > 1:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        if add_sort and self._sortcriteria != {}:
            request["sort"] = [self._sortcriteria]
        return request

    def _build_url(self, tail_end):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("/_search")
        request = self._build_request(1, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=1, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Alerts v6 API uses base 1 instead of 0.

        Args:
            from_row (int): The row to start the query at (default 1).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]

            # Prevent 500 Internal Server Error from retrieving behind MAX_RESULTS_LIMIT
            if self._total_results > MAX_RESULTS_LIMIT:
                self._total_results = MAX_RESULTS_LIMIT
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                alert = self._doc_class(self._cb, item["id"], item)
                if "type" in item:
                    if item["type"] == "CB_ANALYTICS":
                        alert.__class__ = CBAnalyticsAlert
                    elif item["type"] == "WATCHLIST":
                        alert.__class__ = WatchlistAlert
                    elif item["type"] == "INTRUSION_DETECTION_SYSTEM":
                        alert.__class__ = IntrusionDetectionSystemAlert
                    elif item["type"] == "DEVICE_CONTROL":
                        alert.__class__ = DeviceControlAlert
                    elif item["type"] == "HOST_BASED_FIREWALL":
                        alert.__class__ = HostBasedFirewallAlert
                    elif item["type"] == "CONTAINER_RUNTIME":
                        alert.__class__ = ContainerRuntimeAlert
                    else:
                        pass
                else:
                    alert.__class__ = Alert
                yield alert
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def facets(self, fieldlist, max_rows=0):
        """
        Return information about the facets for this alert by search, using the defined criteria.

        Args:
            fieldlist (list): List of facet field names.
            max_rows (int): The maximum number of rows to return. 0 means return all rows.

        Returns:
            list: A list of facet information specified as dicts.
            error: invalid enum

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
            ApiError: If the facet field is not valid
        """
        for field in fieldlist:
            if field in AlertSearchQuery.DEPRECATED_FACET_FIELDS:
                raise FunctionalityDecommissioned(
                    "Field '{0}' does is not a valid facet name because it was deprecated in "
                    "Alerts v7.".format(field))

        request = self._build_request(0, -1, False)
        del request['rows']
        request["terms"] = {"fields": fieldlist, "rows": max_rows}
        url = self._build_url("/_facet")
        resp = self._cb.post_object(url, body=request)
        if resp.status_code == 400:
            raise ApiError(resp.json())
        result = resp.json()
        return result.get("results", [])

    def _update_status(self, status, closure_reason, note, determination):
        """
        Updates the status of all alerts matching the given query.

        Args:
            status (str): The status to set for this alert, either "OPEN", "IN_PROGRESS", or "CLOSED".
            closure_reason (str): the closure reason for this alert, either "TRUE_POSITIVE", "FALSE_POSITIVE", or "NONE"
            note (str): The comment to set for the alert.
            determination (str): The determination status to set for the alert, either "NO_REASON", "RESOLVED", \
            "RESOLVED_BENIGN_KNOWN_GOOD", "DUPLICATE_CLEANUP", "OTHER"

        Returns:
            Job: The Job object for the bulk workflow action.
        """
        request = self._build_request(0, -1)
        del request["rows"]

        if status:
            request["status"] = status
        if closure_reason is not None:
            request["closure_reason"] = closure_reason
        if determination is not None:
            request["determination"] = determination
        if note is not None:
            request["note"] = note
        resp = self._cb.post_object(self._bulkupdate_url.format(self._cb.credentials.org_key), body=request)
        output = resp.json()
        return Job(self._cb, output["request_id"])

    def update(self, status, closure_reason=None, determination=None, note=None):
        """
        Update all alerts matching the given query.

        Args:
            status (str): The status to set for this alert, either "OPEN", "IN_PROGRESS", or "CLOSED".
            closure_reason (str): the closure reason for this alert, either "NO_REASON", "RESOLVED", \
            "RESOLVED_BENIGN_KNOWN_GOOD", "DUPLICATE_CLEANUP", "OTHER"
            determination (str): The determination status to set for the alert, either "TRUE_POSITIVE", \
            "FALSE_POSITIVE", or "NONE"
            note (str): The comment to set for the alert.

        Returns:
            Job: The Job object for the bulk workflow action.

        Note:
            - This is an asynchronus call that returns a Job. If you want to wait and block on the results
              you can call await_completion() to get a Futre then result() on the future object to wait for
              completion and get the results.

        Example:
            >>> alert_query = cb.select(Alert).add_criteria("threat_id", ["19261158DBBF00775959F8AA7F7551A1"])
            >>> job = alert_query.update("IN_PROGESS", "NO_REASON", "NONE", "Starting Investigation")
            >>> completed_job = job.await_completion().result()
        """
        return self._update_status(status, closure_reason, note, determination)

    def close(self, closure_reason=None, determination=None, note=None, ):
        """
        Close all alerts matching the given query. The alerts will be left in a CLOSED state after this request.

        Args:
            closure_reason (str): the closure reason for this alert, either "NO_REASON", "RESOLVED", \
            "RESOLVED_BENIGN_KNOWN_GOOD", "DUPLICATE_CLEANUP", "OTHER"
            determination (str): The determination status to set for the alert, either "TRUE_POSITIVE", \
            "FALSE_POSITIVE", or "NONE"
            note (str): The comment to set for the alert.

        Returns:
            Job: The Job object for the bulk workflow action.

        Note:
            - This is an asynchronus call that returns a Job. If you want to wait and block on the results
              you can call await_completion() to get a Futre then result() on the future object to wait for
              completion and get the results.

        Example:
            >>> alert_query = cb.select(Alert).add_criteria("threat_id", ["19261158DBBF00775959F8AA7F7551A1"])
            >>> job = alert_query.close("RESOLVED", "FALSE_POSITIVE", "Normal behavior")
            >>> completed_job = job.await_completion().result()
        """
        return self._update_status("CLOSED", closure_reason, note, determination)

    def set_minimum_severity(self, severity):
        """
        Restricts the alerts that this query is performed on to the specified minimum severity level.

        Args:
            severity (int): The minimum severity level for alerts.

        Returns:
            AlertSearchQuery: This instance.
        """
        self._criteria["minimum_severity"] = severity
        return self

    def set_threat_notes_present(self, is_present, exclude=False):
        """
        Restricts the alerts that this query is performed on to those with or without threat_notes.

        Args:
            is_present (bool): If true, returns alerts that have a note attached to the threat_id
            exclude (bool): If true, will set is_present in the exclusions. Otherwise adds to criteria
        Returns:
            AlertSearchQuery: This instance.
        """
        if not exclude:
            self._criteria["threat_notes_present"] = is_present
        else:
            self._exclusions["threat_notes_present"] = is_present
        return self

    def set_alert_notes_present(self, is_present, exclude=False):
        """
        Restricts the alerts that this query is performed on to those with or without notes.

        Args:
            is_present (bool): If true, returns alerts that have a note attached
            exclude (bool): If true, will set is_present in the exclusions. Otherwise adds to criteria

        Returns:
            AlertSearchQuery: This instance.
        """
        if not exclude:
            self._criteria["alert_notes_present"] = is_present
        else:
            self._exclusions["alert_notes_present"] = is_present
        return self

    def set_remote_is_private(self, is_private, exclude=False):
        """
        Restricts the alerts that this query is performed on based on matching the remote_is_private field.

        This field is only present on CONTAINER_RUNTIME alerts and so filtering will be ignored on other alert types.

        Args:
            is_private (boolean): Whether the remote information is private: true or false
            exclude (bool): If true, will set is_present in the exclusions. Otherwise adds to criteria

        Returns:
            AlertSearchQuery: This instance.
        """
        if not exclude:
            self._criteria["remote_is_private"] = is_private
        else:
            self._exclusions["remote_is_private"] = is_private
        return self


class GroupedAlertSearchQuery(AlertSearchQuery):
    """Represents a query that is used to group Alert objects by a given field."""
    def __init__(self, *args, **kwargs):
        """Initialize the GroupAlertSearchQuery."""
        super().__init__(*args, **kwargs)
        self._group_by = "THREAT_ID"

    def set_group_by(self, field):
        """
        Sets the 'group_by' query body parameter, determining which field to group the alerts by.

        Args:
            field (string): The field to group by
        """
        self._group_by = field
        return self

    def _build_request(self, from_row, max_rows, add_sort=True):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.
            add_sort (bool): If True(default), the sort criteria will be added as part of the request.

        Returns:
            dict: The complete request body.
        """
        request = super(GroupedAlertSearchQuery, self)._build_request(from_row, max_rows, add_sort=True)
        request["group_by"] = {"field": self._group_by}
        return request

    def _perform_query(self, from_row=1, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 1).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_found"]
            self._group_by_total_count = result["group_by_total_count"]

            # Prevent 500 Internal Server Error from retrieving behind MAX_RESULTS_LIMIT
            if self._total_results > MAX_RESULTS_LIMIT:
                self._total_results = MAX_RESULTS_LIMIT
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                grouped_alert = self._doc_class(self._cb, None, item)
                grouped_alert._request = self
                yield grouped_alert
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def close(self, closure_reason=None, determination=None, note=None, ):
        """
        Closing all alerts matching a grouped alert query is not implemented.

        Note:
            - Closing all alerts in all groups returned by a ``GroupedAlertSearchQuery`` can be done by
            getting the ``AlertSearchQuery`` and using close() on it as shown in the following example.

        Example:
            >>> alert_query = grouped_alert_query.get_alert_search_query()
            >>> alert_query.close(closure_reason, note, determination)
        """
        raise NotImplementedError("this method is not implemented")

    def update(self, status, closure_reason=None, determination=None, note=None):
        """
        Updating all alerts matching a grouped alert query is not implemented.

        Note:
            - Updating all alerts in all groups returned by a ``GroupedAlertSearchQuery`` can be done by
            getting the ``AlertSearchQuery`` and using update() on it as shown in the following example.

        Example:
            >>> alert_query = grouped_alert_query.get_alert_search_query()
            >>> job = alert_query.update("IN_PROGESS", "NO_REASON", "NONE", "Starting Investigation")
            >>> completed_job = job.await_completion().result()
        """
        raise NotImplementedError("this method is not implemented")
