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
from cbc_sdk.platform.devices import DeviceSearchQuery
from cbc_sdk.platform.processes import AsyncProcessQuery, Process

"""Alert Models"""

MAX_RESULTS_LIMIT = 10000
REMAPPED_ALERTS_V6 = {
    "alert_classification.classification": "ml_classification_final_verdict",
    "alert_classification.global_prevalence": "ml_classification_global_prevalence",
    "alert_classification.org_prevalence": "ml_classification_org_prevalence",
    "alert_classification.user_feedback": "determination_value",
    "cluster_name": "k8s_cluster",
    "create_time": "backend_timestamp",
    "create_time": "detection_timestamp",
    "first_event_time": "first_event_timestamp",
    "last_event_time": "last_event_timestamp",
    "last_update_time": "backend_update_timestamp",
    "last_update_time": "user_update_timestamp",
    "namespace": "k8s_namespace",
    "notes_present": "alert_notes_present",
    "policy_id": "device_policy_id",
    "policy_name": "device_policy",
    "port": "netconn_local_port",
    "port": "netconn_remote_port",
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
    "threat_cause_event_id": "primary_event_id",
    "threat_cause_md5": "process_md5",
    "threat_cause_parent_guid": "parent_guid",
    "threat_cause_reputation": "process_reputation",
    "threat_indicators": "ttps",
    "watchlists": "watchlists.id",
    "watchlists": "watchlists.name",
    "workflow.last_update_time": "workflow.change_timestamp",
    "workflow.comment": "workflow.note",
    "workflow.remediation": "workflow.closure_reason",
    "workflow.state": "workflow.status",
    "workload_kind": "k8s_kind",
    "workload_name": "k8s_workload_name"
}

REMAPPED_WORKFLOWS_V6 = {
    "workflow.last_update_time": "workflow.change_timestamp",
    "workflow.comment": "workflow.note",
    "workflow.remediation": "workflow.closure_reason",
    "workflow.state": "workflow.status",
}

REMAPPED_NOTES_V6 = {
    "last_update_time": "",

}


class BaseAlert(PlatformModel):
    """Represents a basic alert."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    urlobject_single = "/api/alerts/v7/orgs/{0}/alerts/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/base_alert.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the BaseAlert object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(BaseAlert, self).__init__(cb, model_unique_id, initial_data)
        self._info = self.to_json()
        self._workflow = Workflow(cb, initial_data.get("workflow", None) if initial_data else None)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    class Note(PlatformModel):
        """Represents a note within an alert."""
        urlobject = "/api/alerts/v7/orgs/{0}/alerts/{1}/notes"
        urlobject_single = "/api/alerts/v7/orgs/{0}/alerts/{1}/notes/{2}"
        primary_key = "id"
        swagger_meta_file = "platform/models/base_alert_note.yaml"
        _is_deleted = False

        def __init__(self, cb, alert, model_unique_id, initial_data=None):
            """
            Initialize the Note object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                alert (BaseAlert): The alert where the note is saved.
                model_unique_id (str): ID of the note represented.
                initial_data (dict): Initial data used to populate the note.
            """
            super(BaseAlert.Note, self).__init__(cb, model_unique_id, initial_data)
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

            url = BaseAlert.Note.urlobject.format(self._cb.credentials.org_key, self._alert.id)
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
                return super(BaseAlert, self).__getattribute__(REMAPPED_NOTES_V6.get(item, item))
            except AttributeError:
                raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                                  item))  # fall through to the rest of the logic...

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
                item = REMAPPED_NOTES_V6.get(item, item)
                return super(BaseAlert, self).__getattr__(item)
            except AttributeError:
                raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                                  item))  # fall through to the rest of the logic...

    def notes_(self):
        """Retrieves all notes for an alert."""
        url = BaseAlert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])
        resp = self._cb.get_object(url)
        item_list = resp.get("results", [])
        return [BaseAlert.Note(self._cb, self, item[BaseAlert.Note.primary_key], item)
                for item in item_list]

    def create_note(self, note):
        """Creates a new note."""
        request = {"note": note}
        url = BaseAlert.Note.urlobject.format(self._cb.credentials.org_key, self._info[self.primary_key])
        resp = self._cb.post_object(url, request)
        result = resp.json()
        return [BaseAlert.Note(self._cb, self, result["id"], result)]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            BaseAlertSearchQuery: The query object for this alert type.
        """
        return BaseAlertSearchQuery(cls, cb)

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
            request["remediation_state"] = remediation
        if comment:
            request["comment"] = comment
        url = self.urlobject_single.format(self._cb.credentials.org_key,
                                           self._model_unique_id) + "/workflow"
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
        url = "/appservices/v6/orgs/{0}/threat/{1}/workflow".format(self._cb.credentials.org_key,
                                                                    self.threat_id)
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
            return super(BaseAlert, self).__getattribute__(REMAPPED_ALERTS_V6.get(item, item))
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))  # fall through to the rest of the logic...

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
            item = REMAPPED_ALERTS_V6.get(item, item)
            return super(BaseAlert, self).__getattr__(item)
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))  # fall through to the rest of the logic...


    def to_json(self, version="v7"):
        if version == "v6":
            modified_json = {}
            #for item in self._info:
            #    self._info.get()

            #mapper function fields to v6 data schema

            return modified_json

        else:
            return self._info

class WatchlistAlert(BaseAlert):
    """Represents watch list alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    type = ["WATCHLIST"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            WatchlistAlertSearchQuery: The query object for this alert type.
        """
        return WatchlistAlertSearchQuery(cls, cb)

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


class CBAnalyticsAlert(BaseAlert):
    """Represents CB Analytics alerts."""
    # urlobject = "/appservices/v6/orgs/{0}/alerts/cbanalytics"
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    type = ["CB_ANALYTICS"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            CBAnalyticsAlertSearchQuery: The query object for this alert type.
        """
        return CBAnalyticsAlertSearchQuery(cls, cb)

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


class DeviceControlAlert(BaseAlert):
    """Represents Device Control alerts."""
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            DeviceControlAlertSearchQuery: The query object for this alert type.
        """
        return DeviceControlAlertSearchQuery(cls, cb)


class ContainerRuntimeAlert(BaseAlert):
    """Represents Container Runtime alerts."""
    # urlobject = "/appservices/v6/orgs/{0}/alerts/containerruntime"
    urlobject = "/api/alerts/v7/orgs/{0}/alerts"
    type = ["CONTAINER_RUNTIME"]

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this alert type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            ContainerRuntimeAlertSearchQuery: The query object for this alert type.
        """
        return ContainerRuntimeAlertSearchQuery(cls, cb)


class Workflow(UnrefreshableModel):
    """Represents the workflow associated with alerts."""
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
            return super(BaseAlert, self).__getattribute__(REMAPPED_WORKFLOWS_V6.get(item, item))
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))  # fall through to the rest of the logic...

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
            item = REMAPPED_WORKFLOWS_V6.get(item, item)
            return super(BaseAlert, self).__getattr__(item)
        except AttributeError:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))  # fall through to the rest of the logic...



class WorkflowStatus(PlatformModel):
    """Represents the current workflow status of a request."""
    urlobject_single = "/appservices/v6/orgs/{0}/workflow/status/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/workflow_status.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the BaseAlert object.

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


class BaseAlertSearchQuery(BaseQuery, QueryBuilderSupportMixin, IterableQueryMixin, CriteriaBuilderSupportMixin):
    """Represents a query that is used to locate BaseAlert objects."""
    VALID_CATEGORIES = ["THREAT", "MONITORED"]
    VALID_REPUTATIONS = ["KNOWN_MALWARE", "SUSPECT_MALWARE", "PUP", "NOT_LISTED", "ADAPTIVE_WHITE_LIST",
                         "COMMON_WHITE_LIST", "TRUSTED_WHITE_LIST", "COMPANY_BLACK_LIST"]
    VALID_ALERT_TYPES = ["CB_ANALYTICS", "DEVICE_CONTROL", "WATCHLIST", "CONTAINER_RUNTIME"]
    VALID_WORKFLOW_VALS = ["OPEN", "DISMISSED"]
    VALID_FACET_FIELDS = ["ALERT_TYPE", "CATEGORY", "REPUTATION", "WORKFLOW", "TAG", "POLICY_ID",
                          "POLICY_NAME", "DEVICE_ID", "DEVICE_NAME", "APPLICATION_HASH",
                          "APPLICATION_NAME", "STATUS", "RUN_STATE", "POLICY_APPLIED_STATE",
                          "POLICY_APPLIED", "SENSOR_ACTION"]

    def __init__(self, doc_class, cb):
        """
        Initialize the BaseAlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseAlertSearchQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filters = {}
        self._sortcriteria = {}
        self._bulkupdate_url = "/appservices/v6/orgs/{0}/alerts/workflow/_criteria"
        self._count_valid = False
        self._total_results = 0

    def set_categories(self, categories):
        """
        Restricts the alerts that this query is performed on to the specified categories.

        Args:
            categories (list): List of categories to be restricted to. Valid categories are
                               "THREAT", "MONITORED", "INFO", "MINOR", "SERIOUS", and "CRITICAL."

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all((c in BaseAlertSearchQuery.VALID_CATEGORIES) for c in categories):
            raise ApiError("One or more invalid category values")
        self._update_criteria("category", categories)
        return self

    def set_create_time(self, *args, **kwargs):
        """
        Restricts the alerts that this query is performed on to the specified creation time.

        The time may either be specified as a start and end point or as a range.

        Args:
            *args (list): Not used.
            **kwargs (dict): Used to specify start= for start time, end= for end time, and range= for range.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if kwargs.get("start", None) and kwargs.get("end", None):
            if kwargs.get("range", None):
                raise ApiError("cannot specify range= in addition to start= and end=")
            stime = kwargs["start"]
            if not isinstance(stime, str):
                stime = stime.isoformat()
            etime = kwargs["end"]
            if not isinstance(etime, str):
                etime = etime.isoformat()
            self._time_filters["create_time"] = {"start": stime, "end": etime}
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            self._time_filters["create_time"] = {"range": kwargs["range"]}
        else:
            raise ApiError("must specify either start= and end= or range=")
        return self

    def set_device_ids(self, device_ids):
        """
        Restricts the alerts that this query is performed on to the specified device IDs.

        Args:
            device_ids (list): List of integer device IDs.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device_id", device_ids)
        return self

    def set_device_names(self, device_names):
        """
        Restricts the alerts that this query is performed on to the specified device names.

        Args:
            device_names (list): List of string device names.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device_name", device_names)
        return self

    def set_device_os(self, device_os):
        """
        Restricts the alerts that this query is performed on to the specified device operating systems.

        Args:
            device_os (list): List of string operating systems.  Valid values are "WINDOWS", "ANDROID",
                              "MAC", "IOS", "LINUX", and "OTHER."

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all((osval in DeviceSearchQuery.VALID_OS) for osval in device_os):
            raise ApiError("One or more invalid operating systems")
        self._update_criteria("device_os", device_os)
        return self

    def set_device_os_versions(self, device_os_versions):
        """
        Restricts the alerts that this query is performed on to the specified device operating system versions.

        Args:
            device_os_versions (list): List of string operating system versions.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in device_os_versions):
            raise ApiError("One or more invalid device OS versions")
        self._update_criteria("device_os_version", device_os_versions)
        return self

    def set_device_username(self, users):
        """
        Restricts the alerts that this query is performed on to the specified user names.

        Args:
            users (list): List of string user names.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(u, str) for u in users):
            raise ApiError("One or more invalid user names")
        self._update_criteria("device_username", users)
        return self

    def set_group_results(self, do_group):
        """
        Specifies whether or not to group the results of the query.

        Args:
            do_group (bool): True to group the results, False to not do so.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        self._criteria["group_results"] = True if do_group else False
        return self

    def set_alert_ids(self, alert_ids):
        """
        Restricts the alerts that this query is performed on to the specified alert IDs.

        Args:
            alert_ids (list): List of string alert IDs.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(v, str) for v in alert_ids):
            raise ApiError("One or more invalid alert ID values")
        self._update_criteria("id", alert_ids)
        return self

    def set_legacy_alert_ids(self, alert_ids):
        """
        Restricts the alerts that this query is performed on to the specified legacy alert IDs.

        Args:
            alert_ids (list): List of string legacy alert IDs.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(v, str) for v in alert_ids):
            raise ApiError("One or more invalid alert ID values")
        self._update_criteria("legacy_alert_id", alert_ids)
        return self

    def set_minimum_severity(self, severity):
        """
        Restricts the alerts that this query is performed on to the specified minimum severity level.

        Args:
            severity (int): The minimum severity level for alerts.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        self._criteria["minimum_severity"] = severity
        return self

    def set_policy_ids(self, policy_ids):
        """
        Restricts the alerts that this query is performed on to the specified policy IDs.

        Args:
            policy_ids (list): List of integer policy IDs.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(policy_id, int) for policy_id in policy_ids):
            raise ApiError("One or more invalid policy IDs")
        self._update_criteria("policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """
        Restricts the alerts that this query is performed on to the specified policy names.

        Args:
            policy_names (list): List of string policy names.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in policy_names):
            raise ApiError("One or more invalid policy names")
        self._update_criteria("policy_name", policy_names)
        return self

    def set_process_names(self, process_names):
        """
        Restricts the alerts that this query is performed on to the specified process names.

        Args:
            process_names (list): List of string process names.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in process_names):
            raise ApiError("One or more invalid process names")
        self._update_criteria("process_name", process_names)
        return self

    def set_process_sha256(self, shas):
        """
        Restricts the alerts that this query is performed on to the specified process SHA-256 hash values.

        Args:
            shas (list): List of string process SHA-256 hash values.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in shas):
            raise ApiError("One or more invalid SHA256 values")
        self._update_criteria("process_sha256", shas)
        return self

    def set_reputations(self, reps):
        """
        Restricts the alerts that this query is performed on to the specified reputation values.

        Args:
            reps (list): List of string reputation values.  Valid values are "KNOWN_MALWARE", "SUSPECT_MALWARE",
                         "PUP", "NOT_LISTED", "ADAPTIVE_WHITE_LIST", "COMMON_WHITE_LIST", "TRUSTED_WHITE_LIST",
                         and "COMPANY_BLACK_LIST".

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all((r in BaseAlertSearchQuery.VALID_REPUTATIONS) for r in reps):
            raise ApiError("One or more invalid reputation values")
        self._update_criteria("reputation", reps)
        return self

    def set_tags(self, tags):
        """
        Restricts the alerts that this query is performed on to the specified tag values.

        Args:
            tags (list): List of string tag values.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(tag, str) for tag in tags):
            raise ApiError("One or more invalid tags")
        self._update_criteria("tag", tags)
        return self

    def set_target_priorities(self, priorities):
        """
        Restricts the alerts that this query is performed on to the specified target priority values.

        Args:
            priorities (list): List of string target priority values.  Valid values are "LOW", "MEDIUM",
                               "HIGH", and "MISSION_CRITICAL".

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all((prio in DeviceSearchQuery.VALID_PRIORITIES) for prio in priorities):
            raise ApiError("One or more invalid priority values")
        self._update_criteria("target_value", priorities)
        return self

    def set_threat_ids(self, threats):
        """
        Restricts the alerts that this query is performed on to the specified threat ID values.

        Args:
            threats (list): List of string threat ID values.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in threats):
            raise ApiError("One or more invalid threat ID values")
        self._update_criteria("threat_id", threats)
        return self

    def set_time_range(self, key, **kwargs):
        """
        Restricts the alerts that this query is performed on to the specified time range.

        The time may either be specified as a start and end point or as a range.

        Args:
            key (str): The key to use for criteria one of create_time,
                       first_event_time, last_event_time, or last_update_time
            **kwargs (dict): Used to specify start= for start time, end= for end time, and range= for range.

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if key not in ["create_time", "first_event_time", "last_event_time", "last_update_time"]:
            raise ApiError("key must be one of create_time, first_event_time, last_event_time, or last_update_time")
        if kwargs.get("start", None) and kwargs.get("end", None):
            if kwargs.get("range", None):
                raise ApiError("cannot specify range= in addition to start= and end=")
            stime = kwargs["start"]
            if not isinstance(stime, str):
                stime = stime.isoformat()
            etime = kwargs["end"]
            if not isinstance(etime, str):
                etime = etime.isoformat()
            self._time_filters[key] = {"start": stime, "end": etime}
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            self._time_filters[key] = {"range": kwargs["range"]}
        else:
            raise ApiError("must specify either start= and end= or range=")
        return self

    def set_types(self, alerttypes):
        """
        Restricts the alerts that this query is performed on to the specified alert type values.

        Args:
            alerttypes (list): List of string alert type values.  Valid values are "CB_ANALYTICS",
                               "WATCHLIST", "DEVICE_CONTROL", and "CONTAINER_RUNTIME".

        Returns:
            BaseAlertSearchQuery: This instance.

        Note: - When filtering by fields that take a list parameter, an empty list will be treated as a wildcard and
        match everything.
        """
        if not all((t in BaseAlertSearchQuery.VALID_ALERT_TYPES) for t in alerttypes):
            raise ApiError("One or more invalid alert type values")
        self._update_criteria("type", alerttypes)
        return self

    def set_workflows(self, workflow_vals):
        """
        Restricts the alerts that this query is performed on to the specified workflow status values.

        Args:
            workflow_vals (list): List of string alert type values.  Valid values are "OPEN" and "DISMISSED".

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if not all((t in BaseAlertSearchQuery.VALID_WORKFLOW_VALS) for t in workflow_vals):
            raise ApiError("One or more invalid workflow status values")
        self._update_criteria("workflow", workflow_vals)
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
            >>> cb.select(BaseAlert).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            BaseAlertSearchQuery: This instance.
        """
        if direction not in DeviceSearchQuery.VALID_DIRECTIONS:
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
        # Fetch 100 rows per page (instead of 10 by default) for better performance
        request["rows"] = 100
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
        request = self._build_request(0, -1)
        resp = self._cb.rpost_object(url, body=request)
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
                #self.results_compatibility_mapping(item)
                # self.
                #grr = super(BaseALert, self._doc_class).__getattr__( "original_document")
                #test = self._doc_class(self._cb, item["id"], item)
                #grr = test.__getattr__("sensor_action")
                #item.mapper
                yield self._doc_class(self._cb, item["id"], item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def results_compatibility_mapping(self, results):
        v6_query = type(self)
        if v6_query is CBAnalyticsAlertSearchQuery:
            results["blah"] = results["id"]
            self._doc_class.original_document = results
            self._doc_class._info = {}
        elif v6_query is ContainerRuntimeAlertSearchQuery:
            results["blah"] = results["id"]
            return results
        elif v6_query is WatchlistAlertSearchQuery:
            results["blah"] = results["id"]
            return results
        elif v6_query is DeviceControlAlertSearchQuery:
            results["blah"] = results["id"]
            return results
        else:
            return results

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
        if not all((field in BaseAlertSearchQuery.VALID_FACET_FIELDS) for field in fieldlist):
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
        request = {"state": status, "criteria": self._build_criteria(), "query": self._query_builder._collapse()}
        if remediation is not None:
            request["remediation_state"] = remediation
        if comment is not None:
            request["comment"] = comment
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
        return self._update_status("DISMISSED", remediation, comment)


class WatchlistAlertSearchQuery(BaseAlertSearchQuery):
    """Represents a query that is used to locate WatchlistAlert objects."""
    VALID_ALERT_TYPES = ["WATCHLIST"]

    def __init__(self, doc_class, cb):
        """
        Initialize the WatchlistAlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super().__init__(doc_class, cb)
        self._criteria["type"] = ["WATCHLIST"]
        self._bulkupdate_url = "/appservices/v6/orgs/{0}/alerts/watchlist/workflow/_criteria"

    def set_watchlist_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified watchlist ID values.

        Args:
            ids (list): List of string watchlist ID values.

        Returns:
            WatchlistAlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in ids):
            raise ApiError("One or more invalid watchlist IDs")
        self._update_criteria("watchlist_id", ids)
        return self

    def set_watchlist_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified watchlist name values.

        Args:
            names (list): List of string watchlist name values.

        Returns:
            WatchlistAlertSearchQuery: This instance.
        """
        if not all(isinstance(name, str) for name in names):
            raise ApiError("One or more invalid watchlist names")
        self._update_criteria("watchlist_name", names)
        return self


class CBAnalyticsAlertSearchQuery(BaseAlertSearchQuery):
    """Represents a query that is used to locate CBAnalyticsAlert objects."""
    VALID_ALERT_TYPES = ["CB_ANALYTICS"]
    VALID_THREAT_CATEGORIES = ["UNKNOWN", "NON_MALWARE", "NEW_MALWARE", "KNOWN_MALWARE", "RISKY_PROGRAM"]
    VALID_LOCATIONS = ["ONSITE", "OFFSITE", "UNKNOWN"]
    VALID_KILL_CHAIN_STATUSES = ["RECONNAISSANCE", "WEAPONIZE", "DELIVER_EXPLOIT", "INSTALL_RUN",
                                 "COMMAND_AND_CONTROL", "EXECUTE_GOAL", "BREACH"]
    VALID_POLICY_APPLIED = ["APPLIED", "NOT_APPLIED"]
    VALID_RUN_STATES = ["DID_NOT_RUN", "RAN", "UNKNOWN"]
    VALID_SENSOR_ACTIONS = ["POLICY_NOT_APPLIED", "ALLOW", "ALLOW_AND_LOG", "TERMINATE", "DENY"]
    VALID_THREAT_CAUSE_VECTORS = ["EMAIL", "WEB", "GENERIC_SERVER", "GENERIC_CLIENT", "REMOTE_DRIVE",
                                  "REMOVABLE_MEDIA", "UNKNOWN", "APP_STORE", "THIRD_PARTY"]

    def __init__(self, doc_class, cb):
        """
        Initialize the CBAnalyticsAlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super().__init__(doc_class, cb)
        self._criteria["type"] = ["CB_ANALYTICS"]
        self._bulkupdate_url = "/appservices/v6/orgs/{0}/alerts/cbanalytics/workflow/_criteria"

    def set_blocked_threat_categories(self, categories):
        """
        Restricts the alerts that this query is performed on to the specified threat categories that were blocked.

        Args:
            categories (list): List of threat categories to look for.  Valid values are "UNKNOWN",
                               "NON_MALWARE", "NEW_MALWARE", "KNOWN_MALWARE", and "RISKY_PROGRAM".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((category in CBAnalyticsAlertSearchQuery.VALID_THREAT_CATEGORIES)
                   for category in categories):
            raise ApiError("One or more invalid threat categories")
        self._update_criteria("blocked_threat_category", categories)
        return self

    def set_device_locations(self, locations):
        """
        Restricts the alerts that this query is performed on to the specified device locations.

        Args:
            locations (list): List of device locations to look for. Valid values are "ONSITE", "OFFSITE",
                              and "UNKNOWN".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((location in CBAnalyticsAlertSearchQuery.VALID_LOCATIONS)
                   for location in locations):
            raise ApiError("One or more invalid device locations")
        self._update_criteria("device_location", locations)
        return self

    def set_kill_chain_statuses(self, statuses):
        """
        Restricts the alerts that this query is performed on to the specified kill chain statuses.

        Args:
            statuses (list): List of kill chain statuses to look for. Valid values are "RECONNAISSANCE",
                             "WEAPONIZE", "DELIVER_EXPLOIT", "INSTALL_RUN","COMMAND_AND_CONTROL", "EXECUTE_GOAL",
                             and "BREACH".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((status in CBAnalyticsAlertSearchQuery.VALID_KILL_CHAIN_STATUSES)
                   for status in statuses):
            raise ApiError("One or more invalid kill chain status values")
        self._update_criteria("kill_chain_status", statuses)
        return self

    def set_not_blocked_threat_categories(self, categories):
        """
        Restricts the alerts that this query is performed on to the specified threat categories that were NOT blocked.

        Args:
            categories (list): List of threat categories to look for.  Valid values are "UNKNOWN",
                               "NON_MALWARE", "NEW_MALWARE", "KNOWN_MALWARE", and "RISKY_PROGRAM".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((category in CBAnalyticsAlertSearchQuery.VALID_THREAT_CATEGORIES)
                   for category in categories):
            raise ApiError("One or more invalid threat categories")
        self._update_criteria("not_blocked_threat_category", categories)
        return self

    def set_policy_applied(self, applied_statuses):
        """
        Restricts the alerts that this query is performed on to the specified policy status values.

        Args:
            applied_statuses (list): List of status values to look for. Valid values are "APPLIED" and "NOT_APPLIED".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((s in CBAnalyticsAlertSearchQuery.VALID_POLICY_APPLIED)
                   for s in applied_statuses):
            raise ApiError("One or more invalid policy-applied values")
        self._update_criteria("policy_applied", applied_statuses)
        return self

    def set_reason_code(self, reason):
        """
        Restricts the alerts that this query is performed on to the specified reason codes (enum values).

        Args:
            reason (list): List of string reason codes to look for.

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in reason):
            raise ApiError("One or more invalid reason code values")
        self._update_criteria("reason_code", reason)
        return self

    def set_run_states(self, states):
        """
        Restricts the alerts that this query is performed on to the specified run states.

        Args:
            states (list): List of run states to look for. Valid values are "DID_NOT_RUN", "RAN", and "UNKNOWN".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((s in CBAnalyticsAlertSearchQuery.VALID_RUN_STATES)
                   for s in states):
            raise ApiError("One or more invalid run states")
        self._update_criteria("run_state", states)
        return self

    def set_sensor_actions(self, actions):
        """
        Restricts the alerts that this query is performed on to the specified sensor actions.

        Args:
            actions (list): List of sensor actions to look for. Valid values are "POLICY_NOT_APPLIED", "ALLOW",
                            "ALLOW_AND_LOG", "TERMINATE", and "DENY".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((action in CBAnalyticsAlertSearchQuery.VALID_SENSOR_ACTIONS)
                   for action in actions):
            raise ApiError("One or more invalid sensor actions")
        self._update_criteria("sensor_action", actions)
        return self

    def set_threat_cause_vectors(self, vectors):
        """
        Restricts the alerts that this query is performed on to the specified threat cause vectors.

        Args:
            vectors (list): List of threat cause vectors to look for.  Valid values are "EMAIL", "WEB",
                            "GENERIC_SERVER", "GENERIC_CLIENT", "REMOTE_DRIVE", "REMOVABLE_MEDIA", "UNKNOWN",
                            "APP_STORE", and "THIRD_PARTY".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((vector in CBAnalyticsAlertSearchQuery.VALID_THREAT_CAUSE_VECTORS)
                   for vector in vectors):
            raise ApiError("One or more invalid threat cause vectors")
        self._update_criteria("threat_cause_vector", vectors)
        return self

    def _results_compatibility_mapping(self, results):
        v6_query = type(self)
        if v6_query is CBAnalyticsAlertSearchQuery:
            results["blah"] = results.id
        elif v6_query is ContainerRuntimeAlertSearchQuery:
            results["blah"] = results.id
        elif v6_query is WatchlistAlertSearchQuery:
            results["blah"] = results.id
        elif v6_query is DeviceControlAlertSearchQuery:
            results["blah"] = results.id

        else:
            return results


class DeviceControlAlertSearchQuery(BaseAlertSearchQuery):
    """Represents a query that is used to locate DeviceControlAlert objects."""
    VALID_ALERT_TYPES = ["DEVICE_CONTROL"]

    def __init__(self, doc_class, cb):
        """
        Initialize the DeviceControlAlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super().__init__(doc_class, cb)
        self._criteria["type"] = ["DEVICE_CONTROL"]
        self._bulkupdate_url = "/appservices/v6/orgs/{0}/alerts/cbanalytics/devicecontrol/_criteria"

    def set_external_device_friendly_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified external device friendly names.

        Args:
            names (list): List of external device friendly names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid device name values")
        self._update_criteria("external_device_friendly_name", names)
        return self

    def set_external_device_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified external device IDs.

        Args:
            ids (list): List of external device IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid device ID values")
        self._update_criteria("external_device_id", ids)
        return self

    def set_product_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified product IDs.

        Args:
            ids (list): List of product IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid product ID values")
        self._update_criteria("product_id", ids)
        return self

    def set_product_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified product names.

        Args:
            names (list): List of product names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid product name values")
        self._update_criteria("product_name", names)
        return self

    def set_serial_numbers(self, serial_numbers):
        """
        Restricts the alerts that this query is performed on to the specified serial numbers.

        Args:
            serial_numbers (list): List of serial numbers to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in serial_numbers):
            raise ApiError("One or more invalid serial number values")
        self._update_criteria("serial_number", serial_numbers)
        return self

    def set_vendor_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified vendor IDs.

        Args:
            ids (list): List of vendor IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid vendor ID values")
        self._update_criteria("vendor_id", ids)
        return self

    def set_vendor_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified vendor names.

        Args:
            names (list): List of vendor names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid vendor name values")
        self._update_criteria("vendor_name", names)
        return self


class ContainerRuntimeAlertSearchQuery(BaseAlertSearchQuery):
    """Represents a query that is used to locate ContainerRuntimeAlert objects."""
    VALID_ALERT_TYPES = ["CONTAINER_RUNTIME"]

    def __init__(self, doc_class, cb):
        """
        Initialize the ContainerRuntimeAlertSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super().__init__(doc_class, cb)
        self._criteria["type"] = ["CONTAINER_RUNTIME"]
        self._bulkupdate_url = "/appservices/v6/orgs/{0}/alerts/containerruntime/_criteria"

    def set_cluster_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes cluster names.

        Args:
            names (list): List of Kubernetes cluster names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid cluster name values")
        self._update_criteria("cluster_name", names)
        return self

    def set_namespaces(self, namespaces):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes namespaces.

        Args:
            namespaces (list): List of Kubernetes namespaces to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in namespaces):
            raise ApiError("One or more invalid namespace values")
        self._update_criteria("namespace", namespaces)
        return self

    def set_workload_kinds(self, kinds):
        """
        Restricts the alerts that this query is performed on to the specified workload types.

        Args:
            kinds (list): List of workload types to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in kinds):
            raise ApiError("One or more invalid workload kind values")
        self._update_criteria("workload_kind", kinds)
        return self

    def set_workload_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified workload IDs.

        Args:
            ids (list): List of workload IDs to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid workload ID values")
        self._update_criteria("workload_id", ids)
        return self

    def set_workload_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified workload names.

        Args:
            names (list): List of workload names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid workload name values")
        self._update_criteria("workload_name", names)
        return self

    def set_replica_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified pod names.

        Args:
            ids (list): List of pod names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid replica ID values")
        self._update_criteria("replica_id", ids)
        return self

    def set_remote_ips(self, addrs):
        """
        Restricts the alerts that this query is performed on to the specified remote IP addresses.

        Args:
            addrs (list): List of remote IP addresses to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in addrs):
            raise ApiError("One or more invalid remote IP values")
        self._update_criteria("remote_ip", addrs)
        return self

    def set_remote_domains(self, domains):
        """
        Restricts the alerts that this query is performed on to the specified remote domains.

        Args:
            domains (list): List of remote domains to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in domains):
            raise ApiError("One or more invalid remote domain values")
        self._update_criteria("remote_domain", domains)
        return self

    def set_protocols(self, protocols):
        """
        Restricts the alerts that this query is performed on to the specified protocols.

        Args:
            protocols (list): List of protocols to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in protocols):
            raise ApiError("One or more invalid protocol values")
        self._update_criteria("protocol", protocols)
        return self

    def set_ports(self, ports):
        """
        Restricts the alerts that this query is performed on to the specified listening ports.

        Args:
            ports (list): List of listening ports to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, int) for n in ports):
            raise ApiError("One or more invalid port values")
        self._update_criteria("port", ports)
        return self

    def set_egress_group_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified egress group IDs.

        Args:
            ids (list): List of egress group IDs to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid egress group ID values")
        self._update_criteria("egress_group_id", ids)
        return self

    def set_egress_group_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified egress group names.

        Args:
            names (list): List of egress group names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid egress group name values")
        self._update_criteria("egress_group_name", names)
        return self

    def set_ip_reputations(self, reputations):
        """
        Restricts the alerts that this query is performed on to the specified IP reputation values.

        Args:
            reputations (list): List of IP reputation values to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, int) for n in reputations):
            raise ApiError("One or more invalid IP reputation values")
        self._update_criteria("ip_reputation", reputations)
        return self

    def set_rule_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes policy rule IDs.

        Args:
            ids (list): List of Kubernetes policy rule IDs to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid rule ID values")
        self._update_criteria("rule_id", ids)
        return self

    def set_rule_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes policy rule names.

        Args:
            names (list): List of Kubernetes policy rule names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid rule name values")
        self._update_criteria("rule_name", names)
        return self
