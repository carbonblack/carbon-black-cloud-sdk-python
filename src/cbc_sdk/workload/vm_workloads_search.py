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

"""Model and Query Classes for VM Workloads Search API"""

import time
import logging
from cbc_sdk.errors import ApiError, NonQueryableModel
from cbc_sdk.base import (NewBaseModel, UnrefreshableModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)
from cbc_sdk.workload.sensor_lifecycle import SensorKit, _do_sensor_install_request
from cbc_sdk.platform.jobs import Job

log = logging.getLogger(__name__)

"""Workloads Search model"""


class BaseComputeResource(NewBaseModel):
    """Internal BaseComputeResource model"""
    urlobject = "/lcm/view/v2/orgs/{0}/compute_resources"
    urlobject_single = "/lcm/view/v2/orgs/{0}/compute_resources/{1}?deployment_type={2}"
    primary_key = "id"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the BaseComputeResource object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the compute resource represented.
            initial_data (dict): Initial data used to populate the resource object.
        """
        super(BaseComputeResource, self).__init__(cb, model_unique_id, initial_data)
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

        Raises:
            NonQueryableModel: Always, since BaseComputeResource cannot be queried directly.
        """
        raise NonQueryableModel("BaseComputeResource is not directly queryable")

    @classmethod
    def _get_default_deployment_type(cls):
        """
        Return the default deployment type.

        Returns:
            str: The default deployment type for this class.
        """
        raise NotImplementedError("this method is not implemented")

    def _build_api_request_uri(self, http_method="GET"):
        """
        Build the unique URL used to make requests for this object.

        Args:
            http_method (str): Not used; retained for compatibility.

        Returns:
            str: The URL used to make requests for this object.
        """
        return self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id,
                                            self._info.get('deployment_type', self._get_default_deployment_type()))

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
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")

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

        Raises:
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")

    @classmethod
    def bulk_install_by_id(cls, cb, compute_resources, sensor_kit_types, config_file=None):
        """
        Install a sensor on a list of compute resources, specified by ID.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            compute_resources (list): A list of dicts, each of which contains the keys 'vcenter_uuid' and
                                      'compute_resource_id', specifying the compute resources to install sensors on.
            sensor_kit_types (list): A list of SensorKit objects used to specify sensor types to choose from
                                     in installation.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.

        Raises:
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")


class VCenterComputeResource(BaseComputeResource):
    """Models a vCenter compute resource."""
    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the VCenterComputeResource object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(VCenterComputeResource, self).__init__(cb, model_unique_id, initial_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            VCenterComputeResourceQuery: The query object
        """
        return VCenterComputeResourceQuery(cls, cb)

    @classmethod
    def _get_default_deployment_type(cls):
        """
        Return the default deployment type.

        Returns:
            str: The default deployment type for this class.
        """
        return "WORKLOAD"

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
            list: List of dicts with the keys 'vcenter_uuid' and 'compute_resource_id', containing information extracted
                  from the ComputeResource objects.
        """
        return [{'resource_manager_id': resource.vcenter_uuid, 'compute_resource_id': resource.id}
                for resource in reslist]

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
        return _do_sensor_install_request(self._cb, VCenterComputeResource._build_compute_resource_list([self]),
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
        return _do_sensor_install_request(cb, VCenterComputeResource._build_compute_resource_list(compute_resources),
                                          sensor_kit_types, config_file)

    @classmethod
    def bulk_install_by_id(cls, cb, compute_resources, sensor_kit_types, config_file=None):
        """
        Install a sensor on a list of compute resources, specified by ID.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            compute_resources (list): A list of dicts, each of which contains the keys 'vcenter_uuid' and
                                      'compute_resource_id', specifying the compute resources to install sensors on.
            sensor_kit_types (list): A list of SensorKit objects used to specify sensor types to choose from
                                     in installation.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.
        """
        return _do_sensor_install_request(cb, compute_resources, sensor_kit_types, config_file)


class AWSComputeResource(BaseComputeResource):
    """Models an AWS compute resource."""
    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the AWSComputeResource object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(AWSComputeResource, self).__init__(cb, model_unique_id, initial_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            AWSComputeResourceQuery: The query object
        """
        return AWSComputeResourceQuery(cls, cb)

    @classmethod
    def _get_default_deployment_type(cls):
        """
        Return the default deployment type.

        Returns:
            str: The default deployment type for this class.
        """
        return "AWS"

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
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")

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

        Raises:
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")

    @classmethod
    def bulk_install_by_id(cls, cb, compute_resources, sensor_kit_types, config_file=None):
        """
        Install a sensor on a list of compute resources, specified by ID.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            compute_resources (list): A list of dicts, each of which contains the keys 'vcenter_uuid' and
                                      'compute_resource_id', specifying the compute resources to install sensors on.
            sensor_kit_types (list): A list of SensorKit objects used to specify sensor types to choose from
                                     in installation.
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.

        Raises:
            NotImplementedError: Always, for BaseComputeResource.
        """
        raise NotImplementedError("Resource does not allow sensor installation")


class ComputeResourceFacet(UnrefreshableModel):
    """Facet data returned by the facet() method of the query."""
    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the ComputeResourceFacet object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the facet represented.
            initial_data (dict): Initial data used to populate the facet.
        """
        super(ComputeResourceFacet, self).__init__(cb, model_unique_id, initial_data, force_init=False, full_doc=True)
        if initial_data:
            self._values = [ComputeResourceFacet.ComputeResourceFacetValue(cb, d["id"], d)
                            for d in initial_data.get("values", [])]
        else:
            self._values = []

    class ComputeResourceFacetValue(UnrefreshableModel):
        """Represents a single facet value inside a ComputeResourceFacet."""
        def __init__(self, cb, model_unique_id, initial_data=None):
            """
            Initialize the ComputeResourceFacetValue object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                model_unique_id (str): ID of the facet value represented.
                initial_data (dict): Initial data used to populate the facet value.
            """
            super(ComputeResourceFacet.ComputeResourceFacetValue, self).__init__(cb, model_unique_id, initial_data,
                                                                                 force_init=False, full_doc=True)

    def _subobject(self, name):
        """
        Returns the "subobject value" of the given attribute.

        Args:
            name (str): Name of the subobject value to be returned.

        Returns:
            Any: Subobject value for the attribute, or None if there is none.
        """
        if name == "values":
            return self._values
        return super(ComputeResourceFacet, self)._subobject(name)

    @property
    def values(self):
        """
        Returns the values for this particular facet.

        Returns:
            list[ComputeResourceFacet.ComputeResourceFacetValue]: The values of this facet.
        """
        return self._values


"""Query Classes"""


class BaseComputeResourceQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                               IterableQueryMixin, AsyncQueryMixin):
    """Base class for compute resource queries, not intended for direct use."""
    VALID_DEPLOYMENT_TYPE = ("WORKLOAD", "AWS")
    VALID_DOWNLOAD_FORMATS = ("JSON", "CSV")
    DEFAULT_FACET_ROWS = 20

    def __init__(self, doc_class, cb):
        """
        Initialize the BaseComputeResourceQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._criteria = {"deployment_type": [doc_class._get_default_deployment_type()]}
        self._exclusions = {}
        self._sortcriteria = {}
        self._total_results = 0

    def _update_exclusions(self, key, newlist):
        """
        Updates a list of exclusions being collected for a query, by appending items.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        if self._exclusions.get(key, None) is None:
            self._exclusions[key] = newlist
        else:
            self._exclusions[key].extend(newlist)

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(ComputeResource).sort_by("name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order.

        Returns:
            BaseComputeResourceQuery: This instance.
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
        request = {"rows": 100}
        query = self._query_builder._collapse()
        if self._criteria:
            request["criteria"] = self._criteria
        if query:
            request["query"] = query
        if self._exclusions != {}:
            request["exclusions"] = self._exclusions
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

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ

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

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ

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

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ

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

    def facet(self, fields, rows=None):
        """
        Facets all compute resources matching the specified criteria and returns the facet results.

        Example:
            >>> from cbc_sdk import CBCloudAPI
            >>> from cbc_sdk.workload import AWSComputeResource
            >>> cbc = CBCloudAPI()
            >>> query = cbc.select(AWSComputeResource)
            >>> facets = query.facet(['platform', 'virtual_private_cloud_id'])

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ

        Args:
            fields (list[str]): List of the fields to be faceted on.
            rows (int): Number of the top entries to return. Default is 20.

        Returns:
            list[ComputeResourceFacet]: The facet data.
        """
        url = self._build_url("/_facet")
        request = self._build_request(0, -1, False)
        if "rows" in request:
            del request["rows"]
        if "start" in request:
            del request["start"]
        request["terms"] = {"rows": rows if rows else BaseComputeResourceQuery.DEFAULT_FACET_ROWS, "fields": fields}
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return [ComputeResourceFacet(self._cb, d["field"], d) for d in result.get("terms", [])]

    def download(self, download_format=None):
        """
        Downloads all compute resources matching the specific criteria.

        Example:
            >>> from cbc_sdk import CBCloudAPI
            >>> from cbc_sdk.workload import VCenterComputeResource
            >>> cbc = CBCloudAPI()
            >>> query = cbc.select(VCenterComputeResource).set_os_type(["UBUNTU"]).set_eligibility(["ELIGIBLE"])
            >>> query.set_installation_status(["ERROR"])
            >>> job = query.download("CSV")
            >>> job.await_completion()
            >>> print(job.get_output_as_string())

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ, jobs.status(READ)

        Args:
            download_format (str): The download format to be used. Valid values are "JSON" (the default) and "CSV".

        Returns:
            Job: Asynchronous job which will supply the results of the download when they're complete.

        Raises:
             ApiError: If the format specified was not valid, or if the server did not properly return the job.
        """
        if download_format and download_format not in BaseComputeResourceQuery.VALID_DOWNLOAD_FORMATS:
            raise ApiError(f"download format {download_format} not supported")
        url = self._build_url("/_search/download")
        request = self._build_request(0, -1)
        request["format"] = download_format if download_format else BaseComputeResourceQuery.VALID_DOWNLOAD_FORMATS[0]
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        if "jobId" in result:
            return Job(self._cb, result["jobId"])
        raise ApiError("server did not send back a job ID")


class VCenterComputeResourceQuery(BaseComputeResourceQuery):
    """Represents a query that is used to locate ComputeResource objects."""
    VALID_OS_TYPE = ("WINDOWS", "RHEL", "UBUNTU", "SUSE", "SLES", "CENTOS", "OTHER", "AMAZON_LINUX", "ORACLE")
    VALID_ELIGIBILITY = ("ELIGIBLE", "NOT_ELIGIBLE", "UNSUPPORTED")
    VALID_OS_ARCHITECTURE = ("32", "64")
    VALID_INSTALLATION_STATUS = ("SUCCESS", "ERROR", "PENDING", "NOT_INSTALLED")

    def __init__(self, doc_class, cb):
        """
        Initialize the ComputeResourceQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super(VCenterComputeResourceQuery, self).__init__(doc_class, cb)

    def set_appliance_uuid(self, appliance_uuid):
        """
        Restricts the search that this query is performed on to the specified appliance uuid.

        Args:
            appliance_uuid (list): List of string appliance uuids.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in appliance_uuid):
            raise ApiError("One or more invalid appliance uuid")
        self._update_criteria("appliance_uuid", appliance_uuid)
        return self

    def set_cluster_name(self, cluster_name):
        """
        Restricts the search that this query is performed on to the specified cluster name.

        Args:
            cluster_name (list): List of string cluster names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cluster_name):
            raise ApiError("One or more invalid cluster name")
        self._update_criteria("cluster_name", cluster_name)
        return self

    def set_datacenter_name(self, datacenter_name):
        """
        Restricts the search that this query is performed on to the specified datacenter name.

        Args:
            datacenter_name (list): List of string datacenter names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in datacenter_name):
            raise ApiError("One or more invalid datacenter_name")
        self._update_criteria("datacenter_name", datacenter_name)
        return self

    def set_esx_host_name(self, esx_host_name):
        """
        Restricts the search that this query is performed on to the specified ESX host name.

        Args:
            esx_host_name (list): List of string ESX host names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in esx_host_name):
            raise ApiError("One or more invalid esx_host_name")
        self._update_criteria("esx_host_name", esx_host_name)
        return self

    def set_esx_host_uuid(self, esx_host_uuid):
        """
        Restricts the search that this query is performed on to the specified ESX host UUID.

        Args:
            esx_host_uuid (list): List of string ESX host UUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in esx_host_uuid):
            raise ApiError("One or more invalid esx_host_uuid")
        self._update_criteria("esx_host_uuid", esx_host_uuid)
        return self

    def set_vcenter_name(self, vcenter_name):
        """
        Restricts the search that this query is performed on to the specified vCenter name.

        Args:
            vcenter_name (list): List of string vCenter names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_name):
            raise ApiError("One or more invalid vcenter_name")
        self._update_criteria("vcenter_name", vcenter_name)
        return self

    def set_vcenter_host_url(self, vcenter_host_url):
        """
        Restricts the search that this query is performed on to the specified vCenter host URL.

        Args:
            vcenter_host_url (list): List of string vCenter host URLs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_host_url):
            raise ApiError("One or more invalid vcenter_host_url")
        self._update_criteria("vcenter_host_url", vcenter_host_url)
        return self

    def set_vcenter_uuid(self, vcenter_uuid):
        """
        Restricts the search that this query is performed on to the specified vCenter UUID.

        Args:
            vcenter_uuid (list): List of string vCenter UUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_uuid):
            raise ApiError("One or more invalid vcenter_uuid")
        self._update_criteria("vcenter_uuid", vcenter_uuid)
        return self

    def set_name(self, name):
        """
        Restricts the search that this query is performed on to the specified name.

        Args:
            name (list): List of string names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in name):
            raise ApiError("One or more invalid names")
        self._update_criteria("name", name)
        return self

    def set_host_name(self, host_name):
        """
        Restricts the search that this query is performed on to the specified host name.

        Args:
            host_name (list): List of string host names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in host_name):
            raise ApiError("One or more invalid host_names")
        self._update_criteria("host_name", host_name)
        return self

    def set_ip_address(self, ip_address):
        """
        Restricts the search that this query is performed on to the specified ip address.

        Args:
            ip_address (list): List of string ip addresses.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in ip_address):
            raise ApiError("One or more invalid ip address")
        self._update_criteria("ip_address", ip_address)
        return self

    def set_device_guid(self, device_guid):
        """
        Restricts the search that this query is performed on to the specified device GUID.

        Args:
            device_guid (list): List of string device GUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in device_guid):
            raise ApiError("One or more invalid device_guid")
        self._update_criteria("device_guid", device_guid)
        return self

    def set_registration_id(self, registration_id):
        """
        Restricts the search that this query is performed on to the specified registration ID.

        Args:
            registration_id (list): List of string registration IDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in registration_id):
            raise ApiError("One or more invalid registration_id")
        self._update_criteria("registration_id", registration_id)
        return self

    def set_eligibility(self, eligibility):
        """
        Restricts the search that this query is performed on to the specified eligibility.

        Args:
            eligibility (list): List of string eligibilities.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_ELIGIBILITY) for _ in eligibility):
            raise ApiError("One or more invalid eligibility")
        self._update_criteria("eligibility", eligibility)
        return self

    def set_eligibility_code(self, eligibility_code):
        """
        Restricts the search that this query is performed on to the specified eligibility code.

        Args:
            eligibility_code (list): List of string eligibility codes.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in eligibility_code):
            raise ApiError("One or more invalid eligibility_code")
        self._update_criteria("eligibility_code", eligibility_code)
        return self

    def set_installation_status(self, installation_status):
        """
        Restricts the search that this query is performed on to the specified installation status.

        Args:
            installation_status (list): List of string installation status.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_INSTALLATION_STATUS) for _ in installation_status):
            raise ApiError("One or more invalid installation status")
        self._update_criteria("installation_status", installation_status)
        return self

    def set_installation_type(self, installation_type):
        """
        Restricts the search that this query is performed on to the specified installation type.

        Args:
            installation_type (list): List of string installation types.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in installation_type):
            raise ApiError("One or more invalid installation_type")
        self._update_criteria("installation_type", installation_type)
        return self

    def set_uuid(self, uuid):
        """
        Restricts the search that this query is performed on to the specified uuid.

        Args:
            uuid (list): List of string uuid.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in uuid):
            raise ApiError("One or more invalid uuid")
        self._update_criteria("uuid", uuid)
        return self

    def set_os_description(self, os_description):
        """
        Restricts the search that this query is performed on to the specified os description.

        Args:
            os_description (list): List of string os description.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in os_description):
            raise ApiError("One or more invalid os_description")
        self._update_criteria("os_description", os_description)
        return self

    def set_os_type(self, os_type):
        """
        Restricts the search that this query is performed on to the specified os type.

        Args:
            os_type (list): List of string os type.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_OS_TYPE) for _ in os_type):
            raise ApiError("One or more invalid os type")
        self._update_criteria("os_type", os_type)
        return self

    def set_os_architecture(self, os_architecture):
        """
        Restricts the search that this query is performed on to the specified os architecture.

        Args:
            os_architecture (list): List of string os architecture.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_OS_ARCHITECTURE) for _ in os_architecture):
            raise ApiError("One or more invalid os architecture")
        self._update_criteria("os_architecture", os_architecture)
        return self

    def set_vmwaretools_version(self, vmwaretools_version):
        """
        Restricts the search that this query is performed on to the specified VMware Tools version.

        Args:
            vmwaretools_version (list): List of string VMware Tools versions.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vmwaretools_version):
            raise ApiError("One or more invalid vmwaretools_version")
        self._update_criteria("vmwaretools_version", vmwaretools_version)
        return self

    def exclude_appliance_uuid(self, appliance_uuid):
        """
        Excludes the specified appliance UUID from appearing in the search results.

        Args:
            appliance_uuid (list): List of string appliance uuids.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in appliance_uuid):
            raise ApiError("One or more invalid appliance uuid")
        self._update_exclusions("appliance_uuid", appliance_uuid)
        return self

    def exclude_cluster_name(self, cluster_name):
        """
        Excludes the specified cluster name from appearing in the search results.

        Args:
            cluster_name (list): List of string cluster names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cluster_name):
            raise ApiError("One or more invalid cluster_name")
        self._update_exclusions("cluster_name", cluster_name)
        return self

    def exclude_datacenter_name(self, datacenter_name):
        """
        Excludes the specified datacenter name from appearing in the search results.

        Args:
            datacenter_name (list): List of string datacenter names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in datacenter_name):
            raise ApiError("One or more invalid datacenter_name")
        self._update_exclusions("datacenter_name", datacenter_name)
        return self

    def exclude_esx_host_name(self, esx_host_name):
        """
        Excludes the specified ESX host name from appearing in the search results.

        Args:
            esx_host_name (list): List of string ESX host names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in esx_host_name):
            raise ApiError("One or more invalid esx_host_name")
        self._update_exclusions("esx_host_name", esx_host_name)
        return self

    def exclude_esx_host_uuid(self, esx_host_uuid):
        """
        Excludes the specified ESX host UUID from appearing in the search results.

        Args:
            esx_host_uuid (list): List of string ESX host UUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in esx_host_uuid):
            raise ApiError("One or more invalid esx_host_uuid")
        self._update_exclusions("esx_host_uuid", esx_host_uuid)
        return self

    def exclude_vcenter_name(self, vcenter_name):
        """
        Excludes the specified vCenter name from appearing in the search results.

        Args:
            vcenter_name (list): List of string vCenter names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_name):
            raise ApiError("One or more invalid vcenter_name")
        self._update_exclusions("vcenter_name", vcenter_name)
        return self

    def exclude_vcenter_host_url(self, vcenter_host_url):
        """
        Excludes the specified vCenter host URL from appearing in the search results.

        Args:
            vcenter_host_url (list): List of string vCenter host URLs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_host_url):
            raise ApiError("One or more invalid vcenter_host_url")
        self._update_exclusions("vcenter_host_url", vcenter_host_url)
        return self

    def exclude_vcenter_uuid(self, vcenter_uuid):
        """
        Excludes the specified vCenter UUID from appearing in the search results.

        Args:
            vcenter_uuid (list): List of string vCenter UUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vcenter_uuid):
            raise ApiError("One or more invalid vcenter_uuid")
        self._update_exclusions("vcenter_uuid", vcenter_uuid)
        return self

    def exclude_name(self, name):
        """
        Excludes the specified name from appearing in the search results.

        Args:
            name (list): List of string names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in name):
            raise ApiError("One or more invalid names")
        self._update_exclusions("name", name)
        return self

    def exclude_host_name(self, host_name):
        """
        Excludes the specified host name from appearing in the search results.

        Args:
            host_name (list): List of string host names.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in host_name):
            raise ApiError("One or more invalid host names")
        self._update_exclusions("host_name", host_name)
        return self

    def exclude_ip_address(self, ip_address):
        """
        Excludes the specified IP address from appearing in the search results.

        Args:
            ip_address (list): List of string IP addresses.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in ip_address):
            raise ApiError("One or more invalid IP addresses")
        self._update_exclusions("ip_address", ip_address)
        return self

    def exclude_device_guid(self, device_guid):
        """
        Excludes the specified device GUID from appearing in the search results.

        Args:
            device_guid (list): List of string device GUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in device_guid):
            raise ApiError("One or more invalid device_guid")
        self._update_exclusions("device_guid", device_guid)
        return self

    def exclude_registration_id(self, registration_id):
        """
        Excludes the specified registration ID from appearing in the search results.

        Args:
            registration_id (list): List of string registration IDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in registration_id):
            raise ApiError("One or more invalid registration_id")
        self._update_exclusions("registration_id", registration_id)
        return self

    def exclude_eligibility(self, eligibility):
        """
        Excludes the specified eligibility from appearing in the search results.

        Args:
            eligibility (list): List of string eligibilities.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_ELIGIBILITY) for _ in eligibility):
            raise ApiError("One or more invalid eligibility")
        self._update_exclusions("eligibility", eligibility)
        return self

    def exclude_eligibility_code(self, eligibility_code):
        """
        Excludes the specified eligibility code from appearing in the search results.

        Args:
            eligibility_code (list): List of string eligibility codes.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in eligibility_code):
            raise ApiError("One or more invalid eligibility_code")
        self._update_exclusions("eligibility_code", eligibility_code)
        return self

    def exclude_installation_status(self, installation_status):
        """
        Excludes the specified installation status from appearing in the search results.

        Args:
            installation_status (list): List of string installation statuses.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_INSTALLATION_STATUS) for _ in installation_status):
            raise ApiError("One or more invalid installation status")
        self._update_exclusions("installation_status", installation_status)
        return self

    def exclude_installation_type(self, installation_type):
        """
        Excludes the specified installation type from appearing in the search results.

        Args:
            installation_type (list): List of string installation types.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in installation_type):
            raise ApiError("One or more invalid installation_type")
        self._update_exclusions("installation_type", installation_type)
        return self

    def exclude_uuid(self, uuid):
        """
        Excludes the specified UUID from appearing in the search results.

        Args:
            uuid (list): List of string UUIDs.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in uuid):
            raise ApiError("One or more invalid uuid")
        self._update_exclusions("uuid", uuid)
        return self

    def exclude_os_description(self, os_description):
        """
        Excludes the specified OS description from appearing in the search results.

        Args:
            os_description (list): List of string OS descriptions.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in os_description):
            raise ApiError("One or more invalid os_description")
        self._update_exclusions("os_description", os_description)
        return self

    def exclude_os_type(self, os_type):
        """
        Excludes the specified OS type from appearing in the search results.

        Args:
            os_type (list): List of string OS types.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_OS_TYPE) for _ in os_type):
            raise ApiError("One or more invalid os type")
        self._update_exclusions("os_type", os_type)
        return self

    def exclude_os_architecture(self, os_architecture):
        """
        Excludes the specified OS architecture from appearing in the search results.

        Args:
            os_architecture (list): List of string OS architectures.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all((_ in VCenterComputeResourceQuery.VALID_OS_ARCHITECTURE) for _ in os_architecture):
            raise ApiError("One or more invalid os architecture")
        self._update_exclusions("os_architecture", os_architecture)
        return self

    def exclude_vmwaretools_version(self, vmwaretools_version):
        """
        Excludes the specified VMware Tools version from appearing in the search results.

        Args:
            vmwaretools_version (list): List of string VMware Tools versions.

        Returns:
            VCenterComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in vmwaretools_version):
            raise ApiError("One or more invalid vmwaretools_version")
        self._update_exclusions("vmwaretools_version", vmwaretools_version)
        return self


class AWSComputeResourceQuery(BaseComputeResourceQuery):
    """Represents a query that is used to locate AWSComputeResource objects."""
    VALID_INSTALLATION_STATUS = ("SUCCESS", "ERROR", "PENDING", "NOT_INSTALLED")

    def __init__(self, doc_class, cb):
        """
        Initialize the ComputeResourceQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super(AWSComputeResourceQuery, self).__init__(doc_class, cb)

    def set_auto_scaling_group_name(self, auto_scaling_group_name):
        """
        Restricts the search that this query is performed on to the specified auto scaling group name.

        Args:
            auto_scaling_group_name (list): List of string auto scaling group names.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in auto_scaling_group_name):
            raise ApiError("One or more invalid auto_scaling_group_name")
        self._update_criteria("auto_scaling_group_name", auto_scaling_group_name)
        return self

    def set_availability_zone(self, availability_zone):
        """
        Restricts the search that this query is performed on to the specified availability zone.

        Args:
            availability_zone (list): List of string availability zones.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in availability_zone):
            raise ApiError("One or more invalid availability_zone")
        self._update_criteria("availability_zone", availability_zone)
        return self

    def set_cloud_provider_account_id(self, cloud_provider_account_id):
        """
        Restricts the search that this query is performed on to the specified cloud provider account ID.

        Args:
            cloud_provider_account_id (list): List of string cloud provider account IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_account_id):
            raise ApiError("One or more invalid cloud_provider_account_id")
        self._update_criteria("cloud_provider_account_id", cloud_provider_account_id)
        return self

    def set_cloud_provider_resource_id(self, cloud_provider_resource_id):
        """
        Restricts the search that this query is performed on to the specified cloud provider resource ID.

        Args:
            cloud_provider_resource_id (list): List of string cloud provider resource IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_resource_id):
            raise ApiError("One or more invalid cloud_provider_resource_id")
        self._update_criteria("cloud_provider_resource_id", cloud_provider_resource_id)
        return self

    def set_cloud_provider_tags(self, cloud_provider_tags):
        """
        Restricts the search that this query is performed on to the specified cloud provider tags.

        Args:
            cloud_provider_tags (list): List of string cloud provider tags.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_tags):
            raise ApiError("One or more invalid cloud_provider_tags")
        self._update_criteria("cloud_provider_tags", cloud_provider_tags)
        return self

    def set_id(self, id_value):
        """
        Restricts the search that this query is performed on to the specified compute resource ID.

        Args:
            id_value (list): List of string compute resource IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in id_value):
            raise ApiError("One or more invalid IDs")
        self._update_criteria("id", id_value)
        return self

    def set_installation_status(self, installation_status):
        """
        Restricts the search that this query is performed on to the specified installation status.

        Args:
            installation_status (list): List of string installation statuses.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all((_ in AWSComputeResourceQuery.VALID_INSTALLATION_STATUS) for _ in installation_status):
            raise ApiError("One or more invalid installation_status")
        self._update_criteria("installation_status", installation_status)
        return self

    def set_name(self, name):
        """
        Restricts the search that this query is performed on to the specified compute resource name.

        Args:
            name (list): List of string compute resource names.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in name):
            raise ApiError("One or more invalid names")
        self._update_criteria("name", name)
        return self

    def set_platform(self, platform):
        """
        Restricts the search that this query is performed on to the specified platform.

        Args:
            platform (list): List of string platforms.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in platform):
            raise ApiError("One or more invalid platforms")
        self._update_criteria("platform", platform)
        return self

    def set_platform_details(self, platform_details):
        """
        Restricts the search that this query is performed on to the specified platform details.

        Args:
            platform_details (list): List of string platform details.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in platform_details):
            raise ApiError("One or more invalid platform_details")
        self._update_criteria("platform_details", platform_details)
        return self

    def set_region(self, region):
        """
        Restricts the search that this query is performed on to the specified region.

        Args:
            region (list): List of string regions.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in region):
            raise ApiError("One or more invalid regions")
        self._update_criteria("region", region)
        return self

    def set_subnet_id(self, subnet_id):
        """
        Restricts the search that this query is performed on to the specified subnet ID.

        Args:
            subnet_id (list): List of string subnet IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in subnet_id):
            raise ApiError("One or more invalid subnet_id")
        self._update_criteria("subnet_id", subnet_id)
        return self

    def set_virtual_private_cloud_id(self, virtual_private_cloud_id):
        """
        Restricts the search that this query is performed on to the specified virtual private cloud ID.

        Args:
            virtual_private_cloud_id (list): List of string virtual private cloud IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in virtual_private_cloud_id):
            raise ApiError("One or more invalid virtual_private_cloud_id")
        self._update_criteria("virtual_private_cloud_id", virtual_private_cloud_id)
        return self

    def exclude_auto_scaling_group_name(self, auto_scaling_group_name):
        """
        Excludes the specified auto scaling group name from appearing in the search results.

        Args:
            auto_scaling_group_name (list): List of string auto scaling group names.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in auto_scaling_group_name):
            raise ApiError("One or more invalid auto_scaling_group_name")
        self._update_exclusions("auto_scaling_group_name", auto_scaling_group_name)
        return self

    def exclude_availability_zone(self, availability_zone):
        """
        Excludes the specified availability zone from appearing in the search results.

        Args:
            availability_zone (list): List of string availability zones.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in availability_zone):
            raise ApiError("One or more invalid availability zones")
        self._update_exclusions("availability_zone", availability_zone)
        return self

    def exclude_cloud_provider_account_id(self, cloud_provider_account_id):
        """
        Excludes the specified cloud provider account ID from appearing in the search results.

        Args:
            cloud_provider_account_id (list): List of string cloud provider account IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_account_id):
            raise ApiError("One or more invalid cloud_provider_account_id")
        self._update_exclusions("cloud_provider_account_id", cloud_provider_account_id)
        return self

    def exclude_cloud_provider_resource_id(self, cloud_provider_resource_id):
        """
        Excludes the specified cloud provider resource ID from appearing in the search results.

        Args:
            cloud_provider_resource_id (list): List of string cloud provider resource IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_resource_id):
            raise ApiError("One or more invalid cloud_provider_resource_id")
        self._update_exclusions("cloud_provider_resource_id", cloud_provider_resource_id)
        return self

    def exclude_cloud_provider_tags(self, cloud_provider_tags):
        """
        Excludes the specified cloud provider tags from appearing in the search results.

        Args:
            cloud_provider_tags (list): List of string cloud provider tags.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in cloud_provider_tags):
            raise ApiError("One or more invalid cloud_provider_tags")
        self._update_exclusions("cloud_provider_tags", cloud_provider_tags)
        return self

    def exclude_id(self, id_value):
        """
        Excludes the specified compute resource ID from appearing in the search results.

        Args:
            id_value (list): List of string compute resource IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in id_value):
            raise ApiError("One or more invalid IDs")
        self._update_exclusions("id", id_value)
        return self

    def exclude_installation_status(self, installation_status):
        """
        Excludes the specified installation status from appearing in the search results.

        Args:
            installation_status (list): List of string installation statuses.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all((_ in AWSComputeResourceQuery.VALID_INSTALLATION_STATUS) for _ in installation_status):
            raise ApiError("One or more invalid installation_status")
        self._update_exclusions("installation_status", installation_status)
        return self

    def exclude_name(self, name):
        """
        Excludes the specified compute resource name from appearing in the search results.

        Args:
            name (list): List of string compute resource names.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in name):
            raise ApiError("One or more invalid names")
        self._update_exclusions("name", name)
        return self

    def exclude_platform(self, platform):
        """
        Excludes the specified platform from appearing in the search results.

        Args:
            platform (list): List of string platforms.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in platform):
            raise ApiError("One or more invalid platforms")
        self._update_exclusions("platform", platform)
        return self

    def exclude_platform_details(self, platform_details):
        """
        Excludes the specified platform details from appearing in the search results.

        Args:
            platform_details (list): List of string platform details.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in platform_details):
            raise ApiError("One or more invalid platform_details")
        self._update_exclusions("platform_details", platform_details)
        return self

    def exclude_region(self, region):
        """
        Excludes the specified region from appearing in the search results.

        Args:
            region (list): List of string regions.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in region):
            raise ApiError("One or more invalid regions")
        self._update_exclusions("region", region)
        return self

    def exclude_subnet_id(self, subnet_id):
        """
        Excludes the specified subnet ID from appearing in the search results.

        Args:
            subnet_id (list): List of string subnet IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in subnet_id):
            raise ApiError("One or more invalid subnet IDs")
        self._update_exclusions("subnet_id", subnet_id)
        return self

    def exclude_virtual_private_cloud_id(self, virtual_private_cloud_id):
        """
        Excludes the specified virtual private cloud ID from appearing in the search results.

        Args:
            virtual_private_cloud_id (list): List of string virtual private cloud IDs.

        Returns:
            AWSComputeResourceQuery: This instance.
        """
        if not all(isinstance(_, str) for _ in virtual_private_cloud_id):
            raise ApiError("One or more invalid virtual_private_cloud_id")
        self._update_exclusions("virtual_private_cloud_id", virtual_private_cloud_id)
        return self

    def summarize(self, summary_fields):
        """
        Get compute resource summaries on required fields of the resources with the specified criteria.

        Example:
            >>> from cbc_sdk import CBCloudAPI
            >>> from cbc_sdk.workload import AWSComputeResource
            >>> cbc = CBCloudAPI()
            >>> query = cbc.select(AWSComputeResource)
            >>> summary = query.summarize(['availability_zone', 'region', 'virtual_private_cloud_id'])

        Required Permissions:
            public.cloud.inventory(READ) or _API.Public.Cloud:Public.cloud.inventory:READ

        Args:
            summary_fields (list[str]): The fields to be summarized.

        Returns:
            map[str, int]: A mapping of field names to the number of resources with that field.
        """
        url = self._build_url("/_summarize")
        request = self._build_request(0, -1, False)
        if "rows" in request:
            del request["rows"]
        if "start" in request:
            del request["start"]
        request["summary_fields"] = summary_fields
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return {d["field"]: d["count"] for d in result.get("summaries", [])}
