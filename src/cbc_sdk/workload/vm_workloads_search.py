#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for VM Workloads Search API"""

import time
import logging
from cbc_sdk.errors import ApiError
from cbc_sdk.base import (NewBaseModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)
from cbc_sdk.workload.sensor_lifecycle import SensorKit, _do_sensor_install_request

log = logging.getLogger(__name__)

""" Workloads Search model: """


class ComputeResource(NewBaseModel):
    """ComputeResource Model"""
    urlobject = "/lcm/view/v1/orgs/{0}/compute_resources"
    urlobject_single = "/lcm/view/v1/orgs/{0}/compute_resources/{1}"
    primary_key = "id"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the ComputeResource object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(ComputeResource, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            ComputeResourceQuery: The query object
        """
        return ComputeResourceQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the object data from the server.

        Returns:
           bool: True if refresh was successful, False if not.
        """
        resp = self._cb.get_object(self._build_api_request_uri())
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def _build_api_request_uri(self, http_method="GET"):
        """
        Build the unique URL used to make requests for this object.

        Args:
            http_method (str): Not used; retained for compatibility.

        Returns:
            str: The URL used to make requests for this object.
        """
        return self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)

    def _get_sensor_type(self):
        """
        Calculates the sensor type that should be installed on this compute resource.

        May also raise errors if the compute resource is ineligible or has an invalid type.

        Returns:
            str: The sensor type to be used for this compute resource.

        Raises:
            ApiError: If the compute node is not eligible or is of an invalid type.
        """
        if self.eligibility != 'ELIGIBLE':
            raise ApiError(f"device {self.name} does not allow sensor installation ({self.eligibility})")
        my_type = self.os_type
        if my_type in SensorKit.COMPUTE_RESOURCE_MAP:
            my_type = SensorKit.COMPUTE_RESOURCE_MAP[my_type]
        if my_type not in SensorKit.VALID_TYPES:
            raise ApiError(f"device {self.name} type {self.os_type} not supported for sensor installation")
        return my_type

    def _build_desired_sensorkit(self, version):
        """
        Builds a SensorKit to be used to specify the sensor to be installed on this compute resource.

        May also raise errors if the compute resource is ineligible or has an invalid type.

        Args:
            version (str): The version number of the sensor to be used.

        Returns:
            SensorKit: A SensorKit object configured with the right sensor type values.

        Raises:
            ApiError: If the compute node is not eligible or is of an invalid type.
        """
        my_type = self._get_sensor_type()
        if my_type in ('WINDOWS', 'MAC'):
            my_device_type = my_type
        else:
            my_device_type = 'LINUX'
        return SensorKit.from_type(self._cb, my_device_type, self.os_architecture, my_type, version)

    @classmethod
    def _build_compute_resource_list(cls, reslist):
        """
        Given a list of ComputeResource objects, returns a list of dicts to feed to _do_sensor_install_request.

        Args:
            reslist (list): A list of ComputeResource objects.

        Returns:
            list: List of dicts with the keys 'vcenter_id' and 'compute_resource_id', containing information extracted
                  from the ComputeResource objects.
        """
        return [{'vcenter_id': resource.vcenter_uuid, 'compute_resource_id': resource.uuid} for resource in reslist]

    def install_sensor(self, sensor_version, config_file=None):
        """
        Install a sensor on this compute resource.

        Args:
            sensor_version (str): The version number of the sensor to be used.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.

        Raises:
            ApiError: If the compute node is not eligible or is of an invalid type.
        """
        sensorkit = self._build_desired_sensorkit(sensor_version)
        return _do_sensor_install_request(self._cb, ComputeResource._build_compute_resource_list([self]),
                                          [sensorkit], config_file)

    @classmethod
    def bulk_install(cls, cb, compute_resources, sensor_kit_types, config_file=None):
        """
        Install a sensor on a list of compute resources.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            compute_resources (list): A list of ComputeResource objects used to specify compute resources to install
                                      sensors on.
            sensor_kit_types (list): A list of SensorKit objects used to specify sensor types to choose from
                                     in installation.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.
        """
        return _do_sensor_install_request(cb, ComputeResource._build_compute_resource_list(compute_resources),
                                          sensor_kit_types, config_file)

    @classmethod
    def bulk_install_by_id(cls, cb, compute_resources, sensor_kit_types, config_file=None):
        """
        Install a sensor on a list of compute resources, specified by ID.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            compute_resources (list): A list of dicts, each of which contains the keys 'vcenter_id' and
                                      'compute_resource_id', specifying the compute resources to install sensors on.
            sensor_kit_types (list): A list of SensorKit objects used to specify sensor types to choose from
                                     in installation.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.
        """
        return _do_sensor_install_request(cb, compute_resources, sensor_kit_types, config_file)


class ComputeResourceQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                           IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate ComputeResource objects."""
    VALID_OS_TYPE = ("WINDOWS", "RHEL", "UBUNTU", "SUSE", "SLES", "CENTOS", "OTHER", "AMAZON_LINUX", "ORACLE")
    VALID_DIRECTIONS = ("ASC", "DESC")
    VALID_ELIGIBILITY = ("ELIGIBLE", "NOT_ELIGIBLE", "UNSUPPORTED")
    VALID_OS_ARCHITECTURE = ("32", "64")
    VALID_INSTALLATION_STATUS = ("SUCCESS", "ERROR", "PENDING", "NOT_INSTALLED")

    def __init__(self, doc_class, cb):
        """
        Initialize the ComputeResource.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sortcriteria = {}
        self._total_results = 0

    def set_appliance_uuid(self, appliance_uuid):
        """
        Restricts the search that this query is performed on to the specified appliance uuid.

        Args:
            appliance_uuid (list): List of string appliance uuids.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in appliance_uuid):
            raise ApiError("One or more invalid appliance uuid")
        self._update_criteria("appliance_uuid", appliance_uuid)
        return self

    def set_eligibility(self, eligibility):
        """
        Restricts the search that this query is performed on to the specified eligibility.

        Args:
            eligibility (list): List of string eligibilities.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all((_ in ComputeResourceQuery.VALID_ELIGIBILITY) for _ in eligibility):
            raise ApiError("One or more invalid eligibility")
        self._update_criteria("eligibility", eligibility)
        return self

    def set_cluster_name(self, cluster_name):
        """
        Restricts the search that this query is performed on to the specified cluster name.

        Args:
            cluster_name (list): List of string cluster names.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cluster_name):
            raise ApiError("One or more invalid cluster name")
        self._update_criteria("cluster_name", cluster_name)
        return self

    def set_name(self, name):
        """
        Restricts the search that this query is performed on to the specified name.

        Args:
            name (list): List of string names.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in name):
            raise ApiError("One or more invalid names")
        self._update_criteria("name", name)
        return self

    def set_ip_address(self, ip_address):
        """
        Restricts the search that this query is performed on to the specified ip address.

        Args:
            ip_address (list): List of string ip addresses.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in ip_address):
            raise ApiError("One or more invalid ip address")
        self._update_criteria("ip_address", ip_address)
        return self

    def set_installation_status(self, installation_status):
        """
        Restricts the search that this query is performed on to the specified installation status.

        Args:
            installation_status (list): List of string installation status.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all((_ in ComputeResourceQuery.VALID_INSTALLATION_STATUS) for _ in installation_status):
            raise ApiError("One or more invalid installation status")
        self._update_criteria("installation_status", installation_status)
        return self

    def set_uuid(self, uuid):
        """
        Restricts the search that this query is performed on to the specified uuid.

        Args:
            uuid (list): List of string uuid.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in uuid):
            raise ApiError("One or more invalid uuid")
        self._update_criteria("uuid", uuid)
        return self

    def set_os_type(self, os_type):
        """
        Restricts the search that this query is performed on to the specified os type.

        Args:
            os_type (list): List of string os type.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all((_ in ComputeResourceQuery.VALID_OS_TYPE) for _ in os_type):
            raise ApiError("One or more invalid os type")
        self._update_criteria("os_type", os_type)
        return self

    def set_os_architecture(self, os_architecture):
        """
        Restricts the search that this query is performed on to the specified os architecture.

        Args:
            os_architecture (list): List of string os architecture.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if not all((_ in ComputeResourceQuery.VALID_OS_ARCHITECTURE) for _ in os_architecture):
            raise ApiError("One or more invalid os architecture")
        self._update_criteria("os_architecture", os_architecture)
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(ComputeResource).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order.

        Returns:
            ComputeResourceQuery: This instance.
        """
        if direction not in ComputeResourceQuery.VALID_DIRECTIONS:
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
        request = {"criteria": self._criteria, "query": self._query_builder._collapse(), "rows": 100}
        # Fetch 100 rows per page (instead of 10 by default) for better performance
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
                yield self._doc_class(self._cb, item["id"], item)
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
        return [self._doc_class(self._cb, item["id"], item) for item in results]
