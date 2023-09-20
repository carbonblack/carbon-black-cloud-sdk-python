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

from cbc_sdk.errors import ApiError, TimeoutError, ObjectNotFoundError, NonQueryableModel
from cbc_sdk.platform import PlatformModel
from cbc_sdk.base import (BaseQuery,
                          UnrefreshableModel,
                          QueryBuilder,
                          QueryBuilderSupportMixin,
                          IterableQueryMixin,
                          CriteriaBuilderSupportMixin)
from cbc_sdk.endpoint_standard.base import EnrichedEvent
from cbc_sdk.platform.processes import AsyncProcessQuery, Process
from cbc_sdk.platform.legacy_alerts import LegacyAlertSearchQueryCriterionMixin

"""Alert Models"""

MAX_RESULTS_LIMIT = 10000


class Alert(PlatformModel):
    """Represents a basic alert."""
    REMAPPED_ALERTS_V6_TO_V7 = {
        "alert_classification.classification": "ml_classification_final_verdict",
        "alert_classification.global_prevalence": "ml_classification_global_prevalence",
        "alert_classification.org_prevalence": "ml_classification_org_prevalence",
        "alert_classification.user_feedback": "determination_value",
        "cluster_name": "k8s_cluster",
        "create_time": "backend_timestamp",
        "first_event_time": "first_event_timestamp",
        "last_event_time": "last_event_timestamp",
        "last_update_time": "backend_update_timestamp",
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
        "workflow.comment": "workflow.note",
        "workflow.remediation": "workflow.closure_reason",
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
        "ml_classification_final_verdict": "alert_classification.classification",
        "ml_classification_global_prevalence": "alert_classification.global_prevalence",
        "ml_classification_org_prevalence": "alert_classification.org_prevalence",
        "netconn_local_port": "port",
        "netconn_protocol": "protocol",
        "netconn_remote_domain": "remote_domain",
        "netconn_remote_ip": "remote_ip",
        "parent_guid": "threat_cause_parent_guid",
        "primary_event_id": "created_by_event_id",
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
        "workflow.closure_reason": "workflow.remediation",
        "workflow.note": "workflow.comment",
        "workflow.status": "workflow.state"
    }

    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    urlobject_single = "/api/alerts/v7/orgs/{0}/alerts/{1}"
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
        self._workflow = Workflow(cb, initial_data.get("workflow", None) if initial_data else None)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    class Note(PlatformModel):
        """Represents a note within an alert."""
        REMAPPED_NOTES_V6_TO_V7 = {
            "create_time": "create_timestamp",

        }

        REMAPPED_NOTES_V7_TO_V6 = {
            "create_timestamp": "create_time",

        }

        urlobject = "/api/alerts/v7/orgs/{0}/alerts/{1}/notes"
        urlobject_single = "/api/alerts/v7/orgs/{0}/alerts/{1}/notes/{2}"
        primary_key = "id"
        swagger_meta_file = "platform/models/alert_note.yaml"
        _is_deleted = False

        def __init__(self, cb, alert, model_unique_id, initial_data=None):
            """
            Initialize the Note object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                alert (Alert): The alert where the note is saved.
                model_unique_id (str): ID of the note represented.
                initial_data (dict): Initial data used to populate the note.
            """
            super(Alert.Note, self).__init__(cb, model_unique_id, initial_data)
            self._alert = alert
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
            url = self.urlobject_single.format(self._cb.credentials.org_key, self._alert.id,
                                               self.id)
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

    def notes_(self):
        """Retrieves all notes for an alert."""
        url = Alert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])
        resp = self._cb.get_object(url)
        item_list = resp.get("results", [])
        return [Alert.Note(self._cb, self, item[Alert.Note.primary_key], item)
                for item in item_list]

    def create_note(self, note):
        """Creates a new note."""
        request = {"note": note}
        url = Alert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])
        resp = self._cb.post_object(url, request)
        result = resp.json()
        return [Alert.Note(self._cb, self, result["id"], result)]

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
        self._workflow = Workflow(self._cb, resp.get("workflow", None))
        self._last_refresh_time = time.time()
        return True

    @property
    def workflow_(self):
        """
        Returns the workflow associated with this alert.

        Returns:
            Workflow: The workflow associated with this alert.
        """
        return self._workflow

    def _update_workflow_status(self, state, remediation, comment):
        """
        Updates the workflow status of this alert.

        Args:
            state (str): The state to set for this alert, either "OPEN" or "DISMISSED".
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
        """
        request = {"status": state}
        if remediation:
            request["closure_reason"] = remediation
        if comment:
            request["note"] = comment
        url = self.urlobject.format(self._cb.credentials.org_key) + "/workflow"
        resp = self._cb.post_object(url, request)
        self._workflow = Workflow(self._cb, resp.json())
        self._last_refresh_time = time.time()

    def dismiss(self, remediation=None, comment=None):
        """
        Dismisses this alert.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
        """
        self._update_workflow_status("CLOSED", remediation, comment)

    def update(self, remediation=None, comment=None):
        """
        Updates this alert while leaving it open.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
        """
        self._update_workflow_status("OPEN", remediation, comment)

    def _update_threat_workflow_status(self, state, remediation, comment):
        """
        Updates the workflow status of all alerts with the same threat ID, past or future.

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
        url = "/api/alerts/v7/orgs/{0}/alerts/workflow".format(self._cb.credentials.org_key)
        resp = self._cb.post_object(url, request)
        return Workflow(self._cb, resp.json())

    def dismiss_threat(self, remediation=None, comment=None):
        """
        Dismisses all alerts with the same threat ID, past or future.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
        """
        return self._update_threat_workflow_status("DISMISSED", remediation, comment)

    def update_threat(self, remediation=None, comment=None):
        """
        Updates the status of all alerts with the same threat ID, past or future, while leaving them in OPEN state.

        Args:
            remediation (str): The remediation status to set for the alert.
            comment (str): The comment to set for the alert.
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
        """
        try:
            item = Alert.REMAPPED_ALERTS_V6_TO_V7.get(item, item)
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
                modified_json[Alert.REMAPPED_ALERTS_V7_TO_V6.get(key, key)] = value
                if key == "id":
                    modified_json["legacy_alert_id"] = value
                if key == "process_name":
                    modified_json["process_name"] = value
                if key == "primary_event_id":
                    modified_json["created_by_event_id"] = value
                    if self.type == "CB_ANALYTICS":
                        modified_json["threat_cause_cause_event_id"] = value
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
                        wf[self.REMAPPED_WORKFLOWS_V7_TO_V6.get(wf_key, wf_key)] = wf_value
                    modified_json[key] = wf
            return modified_json
        else:
            return self._info


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
        """Requests enriched events detailed results.

        Args:
            timeout (int): Event details request timeout in milliseconds.
            async_mode (bool): True to request details in an asynchronous manner.

        Returns:
            list: EnrichedEvents matching the legacy_alert_id

        Note:
            - When using asynchronous mode, this method returns a python future.
              You can call result() on the future object to wait for completion and get the results.
        """
        self._details_timeout = timeout
        alert_id = self._info.get("legacy_alert_id")
        if not alert_id:
            raise ApiError("Trying to get event details on an invalid alert_id {}".format(alert_id))
        if async_mode:
            return self._cb._async_submit(self._get_events_detailed_results)
        return self._get_events_detailed_results()

    def _get_events_detailed_results(self, *args, **kwargs):
        """
        Actual search details implementation.

        Returns:
            list[EnrichedEvent]: List of enriched events.

        Flow:
            1. Start the job by providing alert_id
            2. Check the status of the job - wait until contacted and complete are equal
            3. Retrieve the results - it is possible for num_found to be 0, because enriched events are
            kept for specific period, so return empty list in that case.
        """
        url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs".format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(url, body={"alert_id": self._info.get("legacy_alert_id")})
        job_id = query_start.json().get("job_id")
        timed_out = False
        submit_time = time.time() * 1000

        while True:
            status_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}".format(
                self._cb.credentials.org_key,
                job_id,
            )
            result = self._cb.get_object(status_url)
            searchers_contacted = result.get("contacted", 0)
            searchers_completed = result.get("completed", 0)
            if searchers_completed == searchers_contacted:
                break
            if searchers_contacted == 0:
                time.sleep(.5)
                continue
            if searchers_completed < searchers_contacted:
                if self._details_timeout != 0 and (time.time() * 1000) - submit_time > self._details_timeout:
                    timed_out = True
                    break

            time.sleep(.5)

        if timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        still_fetching = True
        result_url = "/api/investigate/v2/orgs/{}/enriched_events/detail_jobs/{}/results".format(
            self._cb.credentials.org_key,
            job_id
        )

        query_parameters = {}
        while still_fetching:
            result = self._cb.get_object(result_url, query_parameters=query_parameters)
            available_results = result.get('num_available', 0)
            found_results = result.get('num_found', 0)
            # if found is 0, then no enriched events
            if found_results == 0:
                return []
            if available_results != 0:
                results = result.get('results', [])
                return [EnrichedEvent(self._cb, initial_data=item) for item in results]


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


class Workflow(UnrefreshableModel):
    """Represents the workflow associated with alerts."""
    REMAPPED_WORKFLOWS_V6_TO_V7 = {
        "workflow.last_update_time": "workflow.change_timestamp",
        "workflow.comment": "workflow.note",
        "workflow.remediation": "workflow.closure_reason",
        "workflow.state": "workflow.status",
    }
    REMAPPED_WORKFLOWS_V7_TO_V6 = {
        "change_timestamp": "last_update_time",
        "note": "comment",
        "closure_reason": "remediation",
        "status": "state"
    }
    swagger_meta_file = "platform/models/workflow.yaml"

    def __init__(self, cb, initial_data=None):
        """
        Initialize the Workflow object.

        Args:
        cb (BaseAPI): Reference to API object used to communicate with the server.
        initial_data (dict): Initial data used to populate the workflow.
        """
        super(Workflow, self).__init__(cb, model_unique_id=None, initial_data=initial_data)

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
            return super(Workflow, self).__getattribute__(Workflow.REMAPPED_WORKFLOWS_V6_TO_V7.get(item, item))

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
            item = Workflow.REMAPPED_WORKFLOWS_V6_TO_V7.get(item, item)
            return super(Workflow, self).__getattr__(item)

        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))
            # fall through to the rest of the logic...


class WorkflowStatus(PlatformModel):
    """Represents the current workflow status of a request."""
    urlobject_single = "/jobs/v1/orgs/{0}/jobs/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/job.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Alert object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the request being processed.
            initial_data (dict): Initial data used to populate the status.
        """
        super(WorkflowStatus, self).__init__(cb, model_unique_id, initial_data)
        self._request_id = model_unique_id
        self._workflow = None
        if model_unique_id is not None:
            self._refresh()

    def _refresh(self):
        """
        Rereads the request status from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._request_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._workflow = Workflow(self._cb, resp.get("workflow", None))
        self._last_refresh_time = time.time()
        return True

    @property
    def id_(self):
        """
        Returns the request ID of the associated request.

        Returns:
            str: The request ID of the associated request.
        """
        return self._request_id

    @property
    def workflow_(self):
        """
        Returns the current workflow associated with this request.

        Returns:
            Workflow: The current workflow associated with this request.
        """
        return self._workflow

    @property
    def queued(self):
        """
        Returns whether this request has been queued.

        Returns:
            bool: True if the request is in "queued" state, False if not.
        """
        self._refresh()
        return self._info.get("status", "") == "QUEUED"

    @property
    def in_progress(self):
        """
        Returns whether this request is currently in progress.

        Returns:
            bool: True if the request is in "in progress" state, False if not.
        """
        self._refresh()
        return self._info.get("status", "") == "IN_PROGRESS"

    @property
    def finished(self):
        """
        Returns whether this request has been completed.

        Returns:
            bool: True if the request is in "finished" state, False if not.
        """
        self._refresh()
        return self._info.get("status", "") == "FINISHED"


"""Alert Queries"""


class AlertSearchQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, LegacyAlertSearchQueryCriterionMixin,
                       CriteriaBuilderSupportMixin):
    """Represents a query that is used to locate Alert objects."""
    VALID_CATEGORIES = ["THREAT", "MONITORED"]
    VALID_REPUTATIONS = ["KNOWN_MALWARE", "SUSPECT_MALWARE", "PUP", "NOT_LISTED", "ADAPTIVE_WHITE_LIST",
                         "COMMON_WHITE_LIST", "TRUSTED_WHITE_LIST", "COMPANY_BLACK_LIST"]
    VALID_ALERT_TYPES = ["CB_ANALYTICS", "DEVICE_CONTROL", "WATCHLIST", "CONTAINER_RUNTIME", "HOST_BASED_FIREWALL",
                         "INTRUSION_DETECTION_SYSTEM"]
    # TODO verify and update if needed
    VALID_WORKFLOW_VALS = ["OPEN", "DISMISSED"]

    # TODO verify and update if needed
    VALID_FACET_FIELDS = ["ALERT_TYPE", "CATEGORY", "REPUTATION", "WORKFLOW", "TAG", "POLICY_ID",
                          "POLICY_NAME", "DEVICE_ID", "DEVICE_NAME", "APPLICATION_HASH",
                          "APPLICATION_NAME", "STATUS", "RUN_STATE", "POLICY_APPLIED_STATE",
                          "POLICY_APPLIED", "SENSOR_ACTION"]

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
        super(AlertSearchQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filters = {}
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
        request = {"criteria": self._build_criteria()}
        request["query"] = self._query_builder._collapse()

        request["rows"] = self._batch_size
        if from_row > 0:
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
            fieldlist (list): List of facet field names. Valid names are "ALERT_TYPE", "CATEGORY", "REPUTATION",
                              "WORKFLOW", "TAG", "POLICY_ID", "POLICY_NAME", "DEVICE_ID", "DEVICE_NAME",
                              "APPLICATION_HASH", "APPLICATION_NAME", "STATUS", "RUN_STATE", "POLICY_APPLIED_STATE",
                              "POLICY_APPLIED", and "SENSOR_ACTION".
            max_rows (int): The maximum number of rows to return. 0 means return all rows.

        Returns:
            list: A list of facet information specified as dicts.
        """
        if not all((field in AlertSearchQuery.VALID_FACET_FIELDS) for field in fieldlist):
            raise ApiError("One or more invalid term field names")
        request = self._build_request(0, -1, False)
        del request['rows']
        request["terms"] = {"fields": fieldlist, "rows": max_rows}
        url = self._build_url("/_facet")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return result.get("results", [])

    def _update_status(self, status, remediation, comment):
        """
        Updates the status of all alerts matching the given query.

        Args:
            status (str): The status to put the alerts into, either "OPEN" or "DISMISSED".
            remediation (str): The remediation state to set for all alerts.
            comment (str): The comment to set for all alerts.

        Returns:
            str: The request ID, which may be used to select a WorkflowStatus object.
        """
        request = {"status": status, "criteria": self._build_criteria(), "query": self._query_builder._collapse()}
        if remediation is not None:
            request["closure_reason"] = remediation
        if comment is not None:
            request["note"] = comment
        resp = self._cb.post_object(self._bulkupdate_url.format(self._cb.credentials.org_key), body=request)
        output = resp.json()
        return output["request_id"]

    def update(self, remediation=None, comment=None):
        """
        Update all alerts matching the given query. The alerts will be left in an OPEN state after this request.

        Args:
            remediation (str): The remediation state to set for all alerts.
            comment (str): The comment to set for all alerts.

        Returns:
            str: The request ID, which may be used to select a WorkflowStatus object.
        """
        return self._update_status("OPEN", remediation, comment)

    def dismiss(self, remediation=None, comment=None):
        """
        Dismiss all alerts matching the given query. The alerts will be left in a DISMISSED state after this request.

        Args:
            remediation (str): The remediation state to set for all alerts.
            comment (str): The comment to set for all alerts.

        Returns:
            str: The request ID, which may be used to select a WorkflowStatus object.
        """
        return self._update_status("CLOSED", remediation, comment)
