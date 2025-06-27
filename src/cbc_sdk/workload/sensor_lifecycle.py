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

"""Sensor Lifecycle Management for Workloads"""

from cbc_sdk.errors import ApiError
from cbc_sdk.base import (UnrefreshableModel, BaseQuery, CriteriaBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin)

import logging
import json

log = logging.getLogger(__name__)

_GET_SENSOR_KIT_TRANS_TABLE = {'sensor_url_request': {'filename': 'sensor.json', 'type': 'application/json'},
                               'configParams': {'filename': 'config.ini', 'type': 'text/plain'}}
_SENSOR_INSTALL_TRANS_TABLE = {'action_type': {},
                               'install_request': {'filename': 'request.json', 'type': 'application/json'},
                               'file': {'filename': 'config.ini', 'type': 'text/plain'}}


class SensorKit(UnrefreshableModel):
    """Represents the information about a sensor, including installation file URLs."""
    swagger_meta_file = "workload/models/sensorKit.yaml"

    VALID_DEVICE_TYPES = ["WINDOWS", "LINUX", "MAC"]
    VALID_ARCHITECTURES = ["32", "64", "OTHER"]
    VALID_TYPES = ["WINDOWS", "MAC", "RHEL", "UBUNTU", "SUSE", "AMAZON_LINUX"]
    COMPUTE_RESOURCE_MAP = {'SLES': 'SUSE', 'CENTOS': 'RHEL', 'ORACLE': 'RHEL'}

    def __init__(self, cb, initial_data=None):
        """
        Initialize the SensorKit object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the sensor kit data.
        """
        super(SensorKit, self).__init__(cb, None, initial_data)
        self._full_init = (initial_data is not None and not initial_data.get('_pseudo', False))

    @classmethod
    def from_type(cls, cb, device_type, architecture, sensor_type, version):
        """
        Helper method used to create a temporary SensorKit object from its four components.

        This method CANNOT be used to create an object that will be persisted to the server.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            device_type (str): Device type to be used.  Valid values are "WINDOWS", "LINUX", and "MAC".
            architecture (str): Architecture to be used.  Valid values are "32", "64", and "OTHER".
            sensor_type (str): Sensor type to be used.  Valid values are "WINDOWS", "MAC", "RHEL", "UBUNTU", "SUSE",
                               and "AMAZON_LINUX".
            version (str): Sensor version number to be used.

        Returns:
            SensorType: A SensorType object with those specified values.

        Raises:
            ApiError: If an invalid value was used for one of the three limited values.
        """
        sensor_type_data = {}
        if device_type is not None:
            if device_type not in SensorKit.VALID_DEVICE_TYPES:
                raise ApiError("invalid device_type specified for SensorKit")
            sensor_type_data['device_type'] = device_type
        if architecture is not None:
            if architecture not in SensorKit.VALID_ARCHITECTURES:
                raise ApiError("invalid architecture specified for SensorKit")
            sensor_type_data['architecture'] = architecture
        if sensor_type is not None:
            if sensor_type not in SensorKit.VALID_TYPES:
                raise ApiError("invalid type specified for SensorKit")
            sensor_type_data['type'] = sensor_type
        if version is not None:
            sensor_type_data['version'] = version
        return SensorKit(cb, {'sensor_type': sensor_type_data, '_pseudo': True})

    @classmethod
    def get_config_template(cls, cb):
        """
        Retrieve the sample config.ini file with the properties populated from the server.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            str: Text of the sample configuration file.
        """
        url = "/lcm/v1/orgs/{0}/sensor/config_template".format(cb.credentials.org_key)
        return cb.get_raw_data(url)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            USBDeviceQuery: The query object for this alert type.
        """
        return SensorKitQuery(cls, cb)


class SensorKitQuery(BaseQuery, CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """Query class used to read in SensorKit objects."""

    def __init__(self, doc_class, cb):
        """
        Initialize the SensorKitQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._criteria = {}
        self._expires = None
        self._config_params = None
        self._total_results = 0

    def add_sensor_kit_type(self, skit=None, **kwargs):
        """
        Add a sensor kit type to the request.

        Args:
            skit (SensorKit): The sensor kit type to be added to the request.
            **kwargs (dict): If skit is None, the keyword arguments 'device_type', 'architecture', 'sensor_type',
                             and 'version' are used to create the sensor kit type to be added.

        Returns:
            SensorKitQuery: Reference to this object.
        """
        my_skit = skit
        if my_skit is None:
            my_skit = SensorKit.from_type(self._cb, kwargs.pop('device_type', None), kwargs.pop('architecture', None),
                                          kwargs.pop('sensor_type', None), kwargs.pop('version', None))
        self._update_criteria('sensor_types', [my_skit.sensor_type])
        return self

    def expires(self, expiration_date_time):
        """
        Sets the expiration date and time for the sensor kit query request.

        Args:
            expiration_date_time (str): The time at which the sensor download link will expire, expressed
                                        as ISO 8601 UTC.

        Returns:
            SensorKitQuery: Reference to this object.
        """
        self._expires = expiration_date_time
        return self

    def config_params(self, params):
        """
        Sets the configuration parameters for the sensor kit query request.

        Args:
            params (str): The text of a config.ini file with a list of sensor properties to configure
                          on installation.

        Returns:
            SensorKitQuery: Reference to this object.
        """
        self._config_params = params
        return self

    def _submit_query(self):
        """
        Submits the current query to the server and returns the list of sensor kits.

        Returns:
            list: The list of sensor kits, each one expressed as a dict.
        """
        url = "/lcm/v1/orgs/{0}/sensor/_download".format(self._cb.credentials.org_key)
        request = {'sensor_types': self._criteria['sensor_types'], 'expires_at': self._expires}
        resp = self._cb.post_multipart(url, _GET_SENSOR_KIT_TRANS_TABLE, sensor_url_request=json.dumps(request),
                                       configParams=self._config_params)
        result = resp.json()
        return result.get('sensor_infos', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        self._total_results = len(self._submit_query())
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): Not used; retained for compatibility.
            max_rows (int): Not used; retained for compatibility.

        Returns:
            Iterable: The iterated query.
        """
        items_list = self._submit_query()
        self._total_results = len(items_list)
        self._count_valid = True
        for item in items_list:
            yield self._doc_class(self._cb, item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        items_list = self._submit_query()
        self._total_results = len(items_list)
        self._count_valid = True
        return [self._doc_class(self._cb, item) for item in items_list]


def _do_sensor_install_request(cb, compute_resources, sensor_kits, config_file):
    """
    Internal helper function that performs a sensor installation request.

    Not to be called directly by user code; use methods on the ComputeResource object to access this functionality.

    Args:
        cb (BaseAPI): Reference to API object used to communicate with the server.
        compute_resources (list): A list of dicts containing the keys 'resource_manager_id' and 'compute_resource_id',
                                  used to specify the compute resources to install on.
        sensor_kits (list): A list of SensorKit objects used to specify sensor types to choose from in installation.
        config_file (str): The text of a config.ini file with a list of sensor properties to configure on installation.

    Returns:
        dict: A dict with two members, 'type' and 'code', indicating the status of the installation.
    """
    request = {
        'compute_resources': compute_resources,
        'sensor_types': [kit.sensor_type for kit in sensor_kits]
    }

    url = "/lcm/v1/orgs/{0}/workloads/actions".format(cb.credentials.org_key)
    return_data = cb.post_multipart(url,
                                    _SENSOR_INSTALL_TRANS_TABLE,
                                    action_type='INSTALL',
                                    install_request=json.dumps(request),
                                    file=config_file)
    return return_data.json()
