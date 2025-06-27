#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and query APIs for Recommendations"""

from cbc_sdk.base import (NewBaseModel, UnrefreshableModel, BaseQuery, CriteriaBuilderSupportMixin, IterableQueryMixin,
                          AsyncQueryMixin)
from cbc_sdk.errors import ApiError, NonQueryableModel
from cbc_sdk.platform.reputation import ReputationOverride
import logging


log = logging.getLogger(__name__)


"""Recommendation models"""


class Recommendation(NewBaseModel):
    """Represents a recommended proposed policy change for the organization."""
    urlobject = "/recommendation-service/v1/orgs/{0}/recommendation"
    urlobject_single = "/recommendation-service/v1/orgs/{0}/recommendation/{1}"
    primary_key = "recommendation_id"
    swagger_meta_file = "endpoint_standard/models/recommendation.yaml"

    class RecommendationImpact(UnrefreshableModel):
        """Represents metadata about a recommendation to be used in the decision to accept or reject it."""
        swagger_meta_file = "endpoint_standard/models/recommendation_impact.yaml"

        def __init__(self, cb, model_unique_id, initial_data=None):
            """
            Initialize the RecommendationImpact object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                model_unique_id (str): Should be None.
                initial_data (dict): Initial data used to populate the object.
            """
            super(Recommendation.RecommendationImpact, self).__init__(cb, model_unique_id, initial_data, full_doc=True)

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            This model is not queryable, raise an error.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                NonQueryableModel: Always.
            """
            raise NonQueryableModel('RecommendationImpact is not queryable')

    class RecommendationNewRule(UnrefreshableModel):
        """Represents the proposed change to an organization's policies from a recommendation."""
        swagger_meta_file = "endpoint_standard/models/recommendation_new_rule.yaml"

        def __init__(self, cb, model_unique_id, initial_data=None):
            """
            Initialize the RecommendationNewRule object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                model_unique_id (str): Should be None.
                initial_data (dict): Initial data used to populate the object.
            """
            super(Recommendation.RecommendationNewRule, self).__init__(cb, model_unique_id, initial_data,
                                                                       full_doc=True)
            self._application = Recommendation.RecommendationApplication(cb, None,
                                                                         initial_data.get('application', None)) \
                if initial_data and 'application' in initial_data else None

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            This model is not queryable, raise an error.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                NonQueryableModel: Always.
            """
            raise NonQueryableModel('RecommendationNewRule is not queryable')

        @property
        def application_(self):
            """
            Return the object representing the rule application of a proposed change to an organization's policies.

            Returns:
                RecommendationApplication: The object representing the rule application of a proposed change.
            """
            return self._application

    class RecommendationApplication(UnrefreshableModel):
        """Represents the rule application of a proposed change to an organization's policies."""
        swagger_meta_file = "endpoint_standard/models/recommendation_application.yaml"

        def __init__(self, cb, model_unique_id, initial_data=None):
            """
            Initialize the RecommendationApplication object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                model_unique_id (str): Should be None.
                initial_data (dict): Initial data used to populate the object.
            """
            super(Recommendation.RecommendationApplication, self).__init__(cb, model_unique_id, initial_data,
                                                                           full_doc=True)

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            This model is not queryable, raise an error.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                NonQueryableModel: Always.
            """
            raise NonQueryableModel('RecommendationApplication is not queryable')

    class RecommendationWorkflow(UnrefreshableModel):
        """Represents the lifecycle state of a recommendation."""
        swagger_meta_file = "endpoint_standard/models/recommendation_workflow.yaml"

        def __init__(self, cb, model_unique_id, initial_data=None):
            """
            Initialize the RecommendationWorkflow object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                model_unique_id (str): Should be None.
                initial_data (dict): Initial data used to populate the object.
            """
            super(Recommendation.RecommendationWorkflow, self).__init__(cb, model_unique_id, initial_data,
                                                                        full_doc=True)

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            This model is not queryable, raise an error.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                NonQueryableModel: Always.
            """
            raise NonQueryableModel('RecommendationWorkflow is not queryable')

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Recommendation object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the recommendation represented.
            initial_data (dict): Initial data used to populate the recommendation.
        """
        super(Recommendation, self).__init__(cb, model_unique_id, initial_data, full_doc=True)
        self._impact = Recommendation.RecommendationImpact(cb, None, initial_data.get('impact', None)) \
            if initial_data and 'impact' in initial_data else None
        self._new_rule = Recommendation.RecommendationNewRule(cb, None, initial_data.get('new_rule', None)) \
            if initial_data and 'new_rule' in initial_data else None
        self._workflow = Recommendation.RecommendationWorkflow(cb, None, initial_data.get('workflow', None)) \
            if initial_data and 'workflow' in initial_data else None

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            RecommendationQuery: The new query object.
        """
        return RecommendationQuery(cls, cb)

    def _refresh(self):
        """
        Reload the Recommendation from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        query = self._cb.select(Recommendation)
        query = query.set_statuses(RecommendationQuery.VALID_STATUSES)
        query = query.set_policy_types([self.rule_type])
        recs = [rec for rec in query if rec.recommendation_id == self.recommendation_id]
        if len(recs) == 1:
            self._info = recs[0]._info
            self._impact = recs[0]._impact
            self._new_rule = recs[0]._new_rule
            self._workflow = recs[0]._workflow
        return len(recs) == 1

    def _subobject(self, name):
        """
        Returns the "subobject value" of the given attribute.

        Args:
            name (str): Name of the subobject value to be returned.

        Returns:
            Any: Subobject value for the attribute, or None if there is none.
        """
        if name == 'impact':
            return self._impact
        if name == 'new_rule':
            return self._new_rule
        if name == 'workflow':
            return self._workflow
        return super(Recommendation, self)._subobject(name)

    @property
    def impact_(self):
        """
        Return the object representing metadata about the recommendation.

        Returns:
            RecommendationImpact: The object representing metadata about the recommendation.
        """
        return self._impact

    @property
    def new_rule_(self):
        """
        Return the object representing the proposed change to an organization's policies from the recommendation.

        Returns:
            RecommendationNewRule: The object representing the proposed change to an organization's policies.
        """
        return self._new_rule

    @property
    def workflow_(self):
        """
        Returns the object representing the lifecycle state of the recommendation.

        Returns:
            RecommendationWorkflow: The object representing the lifecycle state of the recommendation.
        """
        return self._workflow

    def _take_action(self, action, comment=None):
        """
        Take an action on a recommendation, either to accept it, reject it, or reset its state.

        Args:
            action (str): The action to take, either 'ACCEPT', 'REJECT', or 'RESET'.
            comment (str): Optional comment associated with the action.

        Returns:
            bool: True if we successfully refreshed this Recommendation's state, False if not.
        """
        req_body = {'action': action}
        if comment:
            req_body['comment'] = comment
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + '/workflow'
        self._cb.put_object(url, body=req_body)
        return self._refresh()

    def accept(self, comment=None):
        """
        Accept this recommendation, converting it into a reputation override.

        Args:
            comment (str): Optional comment associated with the action.

        Returns:
            bool: True if we successfully refreshed this Recommendation's state, False if not.
        """
        return self._take_action('ACCEPT', comment)

    def reject(self, comment=None):
        """
        Reject this recommendation.

        Args:
            comment (str): Optional comment associated with the action.

        Returns:
            bool: True if we successfully refreshed this Recommendation's state, False if not.
        """
        return self._take_action('REJECT', comment)

    def reset(self, comment=None):
        """
        Reset the recommendation, undoing any created reputation override and setting it back to NEW state.

        Args:
            comment (str): Optional comment associated with the action.

        Returns:
            bool: True if we successfully refreshed this Recommendation's state, False if not.
        """
        return self._take_action('RESET', comment)

    def reputation_override(self):
        """
        Returns the reputation override associated with the recommendation (if the recommendation was accepted).

        Returns:
            ReputationOverride: The associated reputation override, or None if there is none.
        """
        return self._cb.select(ReputationOverride, self._workflow.ref_id) \
            if self._workflow and self._workflow.ref_id else None


"""Recommendation Query"""


class RecommendationQuery(BaseQuery, CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """Query used to locate Recommendation objects."""
    VALID_POLICY_TYPES = ['reputation_override', 'sensor_policy']
    VALID_STATUSES = ['NEW', 'REJECTED', 'ACCEPTED']

    def __init__(self, doc_class, cb):
        """
        Initialize the RecommendationQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._criteria = {}
        self._sortcriteria = {}
        self._total_results = 0

    def set_policy_types(self, policy_types):
        """
        Restricts the recommendations that this query is performed on to the specified policy types.

        Args:
            policy_types (list): List of policy types to restrict the search to.

        Returns:
            RecommendationQuery: This instance.

        Raises:
            ApiError: If invalid values are passed in the list.
        """
        if not all((policy_type in RecommendationQuery.VALID_POLICY_TYPES) for policy_type in policy_types):
            raise ApiError("One or more invalid policy types")
        self._update_criteria("policy_type", policy_types)
        return self

    def set_statuses(self, statuses):
        """
        Restricts the recommendations that this query is performed on to the specified status values.

        Args:
            statuses (list): List of status values to restrict the search to.  If no statuses are specified, the search
                             defaults to NEW only.

        Returns:
            RecommendationQuery: This instance.

        Raises:
            ApiError: If invalid values are passed in the list.
        """
        if not all((status in RecommendationQuery.VALID_STATUSES) for status in statuses):
            raise ApiError("One or more invalid status values")
        self._update_criteria("status", statuses)
        return self

    def set_hashes(self, hashes):
        """
        Restricts the recommendations that this query is performed on to the specified hashes.

        Args:
            hashes (list): List of hashes to restrict the search to.

        Returns:
            RecommendationQuery: This instance.

        Raises:
            ApiError: If invalid values are passed in the list.
        """
        if not all(isinstance(hashval, str) for hashval in hashes):
            raise ApiError("One or more invalid hash values")
        self._update_criteria("hashes", hashes)
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(USBDevice).sort_by("product_name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            USBDeviceQuery: This instance.
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
        request = {"rows": 50}
        if self._criteria:
            request["criteria"] = self._criteria
        # Fetch 50 rows per page (instead of 10 by default) for better performance
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
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_found"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): The row to start the query at (default 0).
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
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item["recommendation_id"], item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            if current >= self._total_results:
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        self._total_results = result["num_found"]
        self._count_valid = True
        results = result.get("results", [])
        return [self._doc_class(self._cb, item["recommendation_id"], item) for item in results]
