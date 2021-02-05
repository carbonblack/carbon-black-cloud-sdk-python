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

"""Sensor Lifecycle Management for Workloads"""

from cbc_sdk.errors import ApiError
from cbc_sdk.base import UnrefreshableModel

import logging
import json

log = logging.getLogger(__name__)


class SensorType(UnrefreshableModel):
    """Represents a sensor type in a request."""
    swagger_meta_file = "workload/models/sensorType.yaml"

    VALID_DEVICE_TYPES = ["WINDOWS", "LINUX", "MAC"]
    VALID_ARCHITECTURES = ["32", "64", "OTHER"]
    VALID_TYPES = ["WINDOWS", "MAC", "RHEL", "UBUNTU", "SUSE", "AMAZON_LINUX"]

    def __init__(self, cb, initial_data=None):
        """
        Initialize the SensorType object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the sensor type.
        """
        super(SensorType, self).__init__(cb, None, initial_data)
        if 'type' in self._info:
            self._info['sensor_type'] = self._info['type']
            del self._info['type']
        self._full_init = True

    @classmethod
    def create(cls, cb, device_type, architecture, sensor_type, version):
        """
        Helper method used to create a SensorType from its four components.

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
        if device_type not in SensorType.VALID_DEVICE_TYPES:
            raise ApiError("invalid device_type specified for SensorType")
        if architecture not in SensorType.VALID_ARCHITECTURES:
            raise ApiError("invalid architecture specified for SensorType")
        if sensor_type not in SensorType.VALID_TYPES:
            raise ApiError("invalid type specified for SensorType")
        return SensorType(cb, {'device_type': device_type, 'architecture': architecture, 'sensor_type': sensor_type,
                               'version': version})

    def _as_dict(self):
        """
        Returns a dictionary containing the SensorType values as they are to be submitted to the server.

        Returns:
            dict: A dictionary containing the SensorType values.
        """
        return {'device_type': self.device_type, 'architecture': self.architecture, 'type': self.sensor_type,
                'version': self.version}


class SensorInfo(UnrefreshableModel):
    """Represents information related tot he installation of a sensor."""
    swagger_meta_file = "workload/models/sensorInfo.yaml"

    def __init__(self, cb, initial_data=None):
        """
        Initialize the SensorInfo object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            initial_data (dict): Initial data used to populate the sensor information.
        """
        super(SensorInfo, self).__init__(cb, None, initial_data)
        self._full_init = True
        self._sensor_type = None

    @property
    def sensor_type_(self):
        """
        Returns the sensor type information in this information object, as a SensorType object.

        Returns:
            SensorType: The sensor type information.
        """
        if self._sensor_type is None:
            self._sensor_type = SensorType(self._cb, self._info['sensor_type'])
        return self._sensor_type


class SensorRequest:
    """Used to make a request for sensor information or installation."""
    def __init__(self, cb):
        """
        Initialize the SensorRequest object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._cb = cb
        self._compute_resources = []
        self._sensor_types = []

    def add_compute_resource(self, resource_manager_id, compute_resource_id):
        """
        Add a compute resource to the request.

        Args:
            resource_manager_id (str): The resource manager ID to be used.
            compute_resource_id (str): The compute resource ID to be used.

        Returns:
            SensorRequest: Reference to this object.
        """
        self._compute_resources.append({'resource_manager_id': resource_manager_id,
                                        'compute_resource_id': compute_resource_id})
        return self

    def add_sensor_type(self, stype=None, **kwargs):
        """
        Add a sensor type to the request.

        Args:
            stype (SensorType): The sensor type to be added to the request.
            **kwargs (dict): If stype is None, the keyword arguments 'device_type', 'architecture', 'sensor_type',
                             and 'version' are used to create the sensor type to be added.

        Returns:
            SensorRequest: Reference to this object.
        """
        my_stype = stype
        if my_stype is None:
            my_stype = SensorType.create(self._cb, kwargs.pop('device_type', None), kwargs.pop('architecture', None),
                                         kwargs.pop('sensor_type', None), kwargs.pop('version', None))
        self._sensor_types.append(my_stype)
        return self

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

    def get_sensor_info(self, expire_time, config_params):
        """
        Get sensor information and download links for the stored sensor types.

        Args:
            expire_time (str): The time at which the sensor download link will expire, expressed as ISO 8601 UTC.
            config_params (str): The text of a config.ini file with a list of sensor properties to configure
                                 on installation.

        Returns:
            list: A list of SensorInfo objects containing the download information.
        """
        request = {'sensor_types': [stype._as_dict() for stype in self._sensor_types], 'expires_at': expire_time}
        url = "/lcm/v1/orgs/{0}/sensor/_download".format(self._cb.credentials.org_key)
        return_data = self._cb.post_multipart(url, sensor_url_request=json.dumps(request), configParams=config_params)
        return_list = return_data.json().get('sensor_infos', [])
        return [SensorInfo(self._cb, info) for info in return_list]

    def request_sensor_install(self, config_file):
        """
        Start the installation of Carbon Black Cloud sensors on VMs as specified by the compute resources.

        Args:
            config_file (str): The text of a config.ini file with a list of sensor properties to configure
                               on installation.

        Returns:
            dict: A dict with two members, 'type' and 'code', indicating the status of the installation.
        """
        request = {'compute_resources': self._compute_resources,
                   'sensor_types': [stype._as_dict() for stype in self._sensor_types]}
        url = "/lcm/v1/orgs/{0}/workloads/actions".format(self._cb.credentials.org_key)
        return_data = self._cb.post_multipart(url, action_type='INSTALL', install_request=json.dumps(request),
                                              file=config_file)
        return return_data.json()
