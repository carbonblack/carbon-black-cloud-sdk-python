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

"""Model and Query Classes for Platform Devices"""

from cbc_sdk.errors import ApiError
from cbc_sdk.platform import PlatformModel, PlatformQueryBase
from cbc_sdk.base import QueryBuilder, QueryBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin

import time


""""Device Models"""


class Device(PlatformModel):
    """Represents a device (endpoint)."""
    urlobject = "/appservices/v6/orgs/{0}/devices"
    urlobject_single = "/appservices/v6/orgs/{0}/devices/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/device.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Device object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(Device, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the Device type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            DeviceSearchQuery: The query object for this alert type.
        """
        return DeviceSearchQuery(cls, cb)

    @property
    def deviceId(self):
        """Warn user that Platform Devices use 'id', not 'device_id'.

        Platform Device API's return 'id' in API responses, where Endpoint Standard
        API's return 'deviceId'.
        """
        raise AttributeError("Platform Devices use .id property for device ID.")

    def _refresh(self):
        """
        Rereads the device data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def lr_session(self):
        """
        Retrieve a Live Response session object for this Device.

        Returns:
            LiveResponseSession: Live Response session for the Device.

        Raises:
            ApiError: If there is an error establishing a Live Response session for this Device.
        """
        return self._cb._request_lr_session(self._model_unique_id)

    def background_scan(self, flag):
        """
        Set the background scan option for this device.

        Args:
            flag (bool): True to turn background scan on, False to turn it off.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_background_scan([self._model_unique_id], flag)

    def bypass(self, flag):
        """
        Set the bypass option for this device.

        Args:
            flag (bool): True to enable bypass, False to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_bypass([self._model_unique_id], flag)

    def delete_sensor(self):
        """
        Delete this sensor device.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_delete_sensor([self._model_unique_id])

    def uninstall_sensor(self):
        """
        Uninstall this sensor device.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_uninstall_sensor([self._model_unique_id])

    def quarantine(self, flag):
        """
        Set the quarantine option for this device.

        Args:
            flag (bool): True to enable quarantine, False to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_quarantine([self._model_unique_id], flag)

    def update_policy(self, policy_id):
        """
        Set the current policy for this device.

        Args:
            policy_id (int): ID of the policy to set for the devices.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_update_policy([self._model_unique_id], policy_id)

    def update_sensor_version(self, sensor_version):
        """
        Update the sensor version for this device.

        Args:
            sensor_version (dict): New version properties for the sensor.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_update_sensor_version([self._model_unique_id], sensor_version)


"""Device Queries"""


class DeviceSearchQuery(PlatformQueryBase, QueryBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate Device objects."""
    VALID_OS = ["WINDOWS", "ANDROID", "MAC", "IOS", "LINUX", "OTHER"]
    VALID_STATUSES = ["PENDING", "REGISTERED", "UNINSTALLED", "DEREGISTERED",
                      "ACTIVE", "INACTIVE", "ERROR", "ALL", "BYPASS_ON",
                      "BYPASS", "QUARANTINE", "SENSOR_OUTOFDATE",
                      "DELETED", "LIVE"]
    VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH", "MISSION_CRITICAL"]
    VALID_DIRECTIONS = ["ASC", "DESC"]

    def __init__(self, doc_class, cb):
        """
        Initialize the DeviceSearchQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        super().__init__(doc_class, cb)
        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filter = {}
        self._exclusions = {}
        self._sortcriteria = {}

    def _update_criteria(self, key, newlist):
        """
        Updates the criteria being collected for a query.

        Assumes the specified criteria item is defined as a list; the list passed in will be set as the value for
        this criteria item, or appended to the existing one if there is one.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._criteria.get(key, [])
        self._criteria[key] = oldlist + newlist

    def _update_exclusions(self, key, newlist):
        """
        Updates the exclusion criteria being collected for a query.

        Assumes the specified criteria item is defined as a list; the list passed in will be set as the value for this
        criteria item, or appended to the existing one if there is one.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._exclusions.get(key, [])
        self._exclusions[key] = oldlist + newlist

    def set_ad_group_ids(self, ad_group_ids):
        """
        Restricts the devices that this query is performed on to the specified AD group IDs.

        Args:
            ad_group_ids (list): List of AD group IDs to restrict the search to.

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid (non-int) values are passed in the list.
        """
        if not all(isinstance(ad_group_id, int) for ad_group_id in ad_group_ids):
            raise ApiError("One or more invalid AD group IDs")
        self._update_criteria("ad_group_id", ad_group_ids)
        return self

    def set_device_ids(self, device_ids):
        """
        Restricts the devices that this query is performed on to the specified device IDs.

        Args:
            device_ids (list): List of device IDs to restrict the search to.

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid (non-int) values are passed in the list.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("id", device_ids)
        return self

    def set_last_contact_time(self, *args, **kwargs):
        """
        Restricts the devices that this query is performed on to the specified last contact time.

        Args:
            *args (list): Not used, retained for compatibility.
            **kwargs (dict): Keyword arguments to this function.  The critical ones are "start" (the start time),
                             "end" (the end time), and "range" (the range value).

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If an invalid combination of keyword parameters are specified.
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
            self._time_filter = {"start": stime, "end": etime}
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            self._time_filter = {"range": kwargs["range"]}
        else:
            raise ApiError("must specify either start= and end= or range=")
        return self

    def set_os(self, operating_systems):
        """
        Restricts the devices that this query is performed on to the specified operating systems.

        Args:
            operating_systems (list): List of operating systems to restrict search to.  Valid values in this list are
                                      "WINDOWS", "ANDROID", "MAC", "IOS", "LINUX", and "OTHER".

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid operating system values are passed in the list.
        """
        if not all((osval in DeviceSearchQuery.VALID_OS) for osval in operating_systems):
            raise ApiError("One or more invalid operating systems")
        self._update_criteria("os", operating_systems)
        return self

    def set_policy_ids(self, policy_ids):
        """
        Restricts the devices that this query is performed on to the specified policy IDs.

        Args:
            policy_ids (list): List of policy IDs to restrict the search to.

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid (non-int) values are passed in the list.
        """
        if not all(isinstance(policy_id, int) for policy_id in policy_ids):
            raise ApiError("One or more invalid policy IDs")
        self._update_criteria("policy_id", policy_ids)
        return self

    def set_status(self, statuses):
        """
        Restricts the devices that this query is performed on to the specified status values.

        Args:
            statuses (list): List of statuses to restrict search to.  Valid values in this list are "PENDING",
                             "REGISTERED", "UNINSTALLED", "DEREGISTERED", "ACTIVE", "INACTIVE", "ERROR", "ALL",
                             "BYPASS_ON", "BYPASS", "QUARANTINE", "SENSOR_OUTOFDATE", "DELETED", and "LIVE".

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid status values are passed in the list.
        """
        if not all((stat in DeviceSearchQuery.VALID_STATUSES) for stat in statuses):
            raise ApiError("One or more invalid status values")
        self._update_criteria("status", statuses)
        return self

    def set_target_priorities(self, target_priorities):
        """
        Restricts the devices that this query is performed on to the specified target priority values.

        Args:
            target_priorities (list): List of priorities to restrict search to.  Valid values in this list are "LOW",
                                      "MEDIUM", "HIGH", and "MISSION_CRITICAL".

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid priority values are passed in the list.
        """
        if not all((prio in DeviceSearchQuery.VALID_PRIORITIES) for prio in target_priorities):
            raise ApiError("One or more invalid target priority values")
        self._update_criteria("target_priority", target_priorities)
        return self

    def set_exclude_sensor_versions(self, sensor_versions):
        """
        Restricts the devices that this query is performed on to exclude specified sensor versions.

        Args:
            sensor_versions (list): List of sensor versions to be excluded.

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If invalid (non-string) values are passed in the list.
        """
        if not all(isinstance(v, str) for v in sensor_versions):
            raise ApiError("One or more invalid sensor versions")
        self._update_exclusions("sensor_version", sensor_versions)
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(Device).sort_by("status")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            DeviceSearchQuery: This instance.

        Raises:
            ApiError: If an invalid direction value is passed.
        """
        if direction not in DeviceSearchQuery.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def _build_request(self, from_row, max_rows):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        mycrit = self._criteria
        if self._time_filter:
            mycrit["last_contact_time"] = self._time_filter
        request = {"criteria": mycrit, "exclusions": self._exclusions}
        request["query"] = self._query_builder._collapse()
        if from_row > 0:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        if self._sortcriteria != {}:
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

            from_row = current
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        url = self._build_url("/_search")
        self._total_results = 0
        self._count_valid = False
        output = []
        while not self._count_valid or len(output) < self._total_results:
            request = self._build_request(len(output), -1)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            if not self._count_valid:
                self._total_results = result["num_found"]
                self._count_valid = True

            results = result.get("results", [])
            output += [self._doc_class(self._cb, item["id"], item) for item in results]
        return output

    def download(self):
        """
        Uses the query parameters that have been set to download all device listings in CSV format.

        Example:
            >>> cb.select(Device).set_status(["ALL"]).download()

        Returns:
            str: The CSV raw data as returned from the server.

        Raises:
            ApiError: If status values have not been set before calling this function.
        """
        tmp = self._criteria.get("status", [])
        if not tmp:
            raise ApiError("at least one status must be specified to download")
        query_params = {"status": ",".join(tmp)}
        tmp = self._criteria.get("ad_group_id", [])
        if tmp:
            query_params["ad_group_id"] = ",".join([str(t) for t in tmp])
        tmp = self._criteria.get("policy_id", [])
        if tmp:
            query_params["policy_id"] = ",".join([str(t) for t in tmp])
        tmp = self._criteria.get("target_priority", [])
        if tmp:
            query_params["target_priority"] = ",".join(tmp)
        tmp = self._query_builder._collapse()
        if tmp:
            query_params["query_string"] = tmp
        if self._sortcriteria:
            query_params["sort_field"] = self._sortcriteria["field"]
            query_params["sort_order"] = self._sortcriteria["order"]
        url = self._build_url("/_search/download")
        return self._cb.get_raw_data(url, query_params)

    def _bulk_device_action(self, action_type, options=None):
        """
        Perform a bulk action on all devices matching the current search criteria.

        Args:
            action_type (str): The action type to be performed.
            options (dict): Any options for the bulk device action.

        Returns:
            str: The JSON output from the request.
        """
        request = {"action_type": action_type, "search": self._build_request(0, -1)}
        if options:
            request["options"] = options
        return self._cb._raw_device_action(request)

    def background_scan(self, scan):
        """
        Set the background scan option for the specified devices.

        Args:
            scan (bool): True to turn background scan on, False to turn it off.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("BACKGROUND_SCAN", self._cb._action_toggle(scan))

    def bypass(self, enable):
        """
        Set the bypass option for the specified devices.

        Args:
            enable (bool): True to enable bypass, False to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("BYPASS", self._cb._action_toggle(enable))

    def delete_sensor(self):
        """
        Delete the specified sensor devices.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("DELETE_SENSOR")

    def uninstall_sensor(self):
        """
        Uninstall the specified sensor devices.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UNINSTALL_SENSOR")

    def quarantine(self, enable):
        """
        Set the quarantine option for the specified devices.

        Args:
            enable (bool): True to enable quarantine, False to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("QUARANTINE", self._cb._action_toggle(enable))

    def update_policy(self, policy_id):
        """
        Set the current policy for the specified devices.

        Args:
            policy_id (int): ID of the policy to set for the devices.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UPDATE_POLICY", {"policy_id": policy_id})

    def update_sensor_version(self, sensor_version):
        """
        Update the sensor version for the specified devices.

        Args:
            sensor_version (dict): New version properties for the sensor.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UPDATE_SENSOR_VERSION", {"sensor_version": sensor_version})
