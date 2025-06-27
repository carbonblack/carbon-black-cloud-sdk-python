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

"""
The model and query classes for referencing platform devices.

A *platform device* represents an endpoint registered with the Carbon Black Cloud that runs a sensor, which
communicates with Carbon Black analytics and the console.  Using these classes, you can search for devices using a
wide variety of filterable fields, such as policy ID, status, or operating system.  You can also perform actions on
individual devices such as quarantining/unquarantining them, enabling or disabling bypass, or upgrading them to a
new sensor version.

Typical usage example::

    # assume "cb" is an instance of CBCloudAPI
    query = cb.select(Device).where(os="WINDOWS").set_policy_ids([142857])
    for device in query:
        device.quarantine(True)
"""

from cbc_sdk.errors import ApiError, ServerError, NonQueryableModel
from cbc_sdk.platform import PlatformModel
from cbc_sdk.platform.jobs import Job
from cbc_sdk.platform.vulnerability_assessment import Vulnerability, VulnerabilityQuery
from cbc_sdk.base import (UnrefreshableModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)
from cbc_sdk.platform.previewer import DevicePolicyChangePreview
from cbc_sdk.workload import NSXRemediationJob

import logging
import time

log = logging.getLogger(__name__)


""""Device Models"""


class Device(PlatformModel):
    """
    Represents a device (endpoint) within the Carbon Black Cloud.

    ``Device`` objects are generally located through a search (using ``DeviceSearchQuery``) before they can be
    operated on.
    """
    urlobject = "/appservices/v6/orgs/{0}/devices"
    urlobject_single = "/appservices/v6/orgs/{0}/devices/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/device.yaml"

    """The valid values for the 'filter' parameter to get_asset_groups_for_devices()."""
    VALID_ASSETGROUP_FILTERS = ("ALL", "DYNAMIC", "MANUAL")

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the ``Device`` object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the device represented.
            initial_data (dict): Initial data used to populate the device.
        """
        super(Device, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the ``Device`` type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.
        """
        return DeviceSearchQuery(cls, cb)

    @property
    def deviceId(self):
        """
        Warn user that Platform Devices use 'id', not 'device_id'.

        Platform Device APIs return 'id' in API responses, where Endpoint Standard APIs return 'deviceId'.

        Raises:
            AttributeError: In all cases.
        """
        raise AttributeError("Platform Devices use .id property for device ID.")

    def _refresh(self):
        """
        Rereads the device data from the server.

        Required Permissions:
            device(READ)

        Returns:
            bool: ``True`` if refresh was successful, ``False`` if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def lr_session(self, async_mode=False):
        """
        Retrieve a Live Response session object for this ``Device``.

        Required Permissions:
            org.liveresponse.session(CREATE)

        Returns:
            LiveResponseSession: Live Response session for the ``Device``.

        Raises:
            ApiError: If there is an error establishing a Live Response session for this ``Device``.
        """
        return self._cb._request_lr_session(self._model_unique_id, async_mode=async_mode)

    def background_scan(self, flag):
        """
        Set the background scan option for this device.

        Required Permissions:
            device.bg-scan(EXECUTE)

        Args:
            flag (bool): ``True`` to turn background scan on, ``False`` to turn it off.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_background_scan([self._model_unique_id], flag)

    def bypass(self, flag):
        """
        Set the bypass option for this device.

        Required Permissions:
            device.bypass(EXECUTE)

        Args:
            flag (bool): ``True`` to enable bypass, ``False`` to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_bypass([self._model_unique_id], flag)

    def delete_sensor(self):
        """
        Delete this sensor device.

        Required Permissions:
            device.deregistered(DELETE)

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_delete_sensor([self._model_unique_id])

    def uninstall_sensor(self):
        """
        Uninstall this sensor device.

        Required Permissions:
            device.uninstall(EXECUTE)

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_uninstall_sensor([self._model_unique_id])

    def quarantine(self, flag):
        """
        Set the quarantine option for this device.

        Required Permissions:
            device.quarantine(EXECUTE)

        Args:
            flag (bool): ``True`` to enable quarantine, ``False`` to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_quarantine([self._model_unique_id], flag)

    def update_policy(self, policy_id):
        """
        Set the current policy for this device.

        Required Permissions:
            device.policy(UPDATE)

        Args:
            policy_id (int): ID of the policy to set for the device.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_update_policy([self._model_unique_id], policy_id)

    def update_sensor_version(self, sensor_version):
        """
        Update the sensor version for this device.

        Required Permissions:
            org.kits(EXECUTE)

        Args:
            sensor_version (dict): New version properties for the sensor.

        Returns:
            str: The JSON output from the request.
        """
        return self._cb.device_update_sensor_version([self._model_unique_id], sensor_version)

    def vulnerability_refresh(self):
        """
        Refresh vulnerability information for the device.

        Required Permissions:
            vulnerabilityAssessment.data(EXECUTE)
        """
        request = {"action_type": 'REFRESH'}
        url = "/vulnerability/assessment/api/v1/orgs/{}".format(self._cb.credentials.org_key)

        url += '/devices/{}/device_actions'.format(self._model_unique_id)

        resp = self._cb.post_object(url, body=request)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 204:
            return None
        else:
            raise ServerError(error_code=resp.status_code, message="Device action error: {0}".format(resp.content),
                              uri=url)

    def get_vulnerability_summary(self, category=None):
        """
        Get the vulnerabilities associated with this device.

        Required Permissions:
            vulnerabilityAssessment.data(READ)

        Args:
            category (string): (optional) Vulnerabilty category (OS, APP).

        Returns:
            dict: Summary of the vulnerabilities for this device.
        """
        VALID_CATEGORY = ["OS", "APP"]

        query_params = {}

        url = '/vulnerability/assessment/api/v1/orgs/{}'

        if category and category not in VALID_CATEGORY:
            raise ApiError("Invalid category provided")
        elif category:
            query_params["category"] = category

        req_url = url.format(self._cb.credentials.org_key) + '/devices/{}/vulnerabilities/summary'.format(self.id)
        return self._cb.get_object(req_url, query_params)

    def get_vulnerabilties(self):
        """
        Return a query to get an operating system or application vulnerability list for this device.

        Returns:
            VulnerabilityQuery: Query for searching for vulnerabilities on this device.
        """
        return VulnerabilityQuery(Vulnerability, self._cb, self)

    @property
    def nsx_available(self):
        """
        Returns whether NSX actions are available on this device.

        Returns:
            bool: ``True`` if NSX actions are available, ``False`` if not.
        """
        return self._info['deployment_type'] == 'WORKLOAD' and self._info['nsx_enabled']

    def nsx_remediation(self, tag, set_tag=True):
        """
        Start an NSX Remediation job on this device to change the tag.

        Required Permissions:
            appliances.nsx.remediation(EXECUTE)

        Args:
            tag (str): The NSX tag to apply to this device. Valid values are "CB-NSX-Quarantine",
                       "CB-NSX-Isolate", and "CB-NSX-Custom".
            set_tag (bool): ``True`` to toggle the specified tag on, ``False`` to toggle it off. Default ``True``.

        Returns:
            NSXRemediationJob: The object representing all running jobs.  ``None`` if the operation is a no-op.
        """
        if not self.nsx_available:
            raise ApiError("NSX actions are not available on this device")
        current = self._info['nsx_distributed_firewall_policy']
        if current is None:
            if not set_tag:
                return None  # clearing tag is a no-op if no tag is set
        elif current == tag:
            if set_tag:
                return None  # setting tag is a no-op if already set
        else:
            if set_tag:
                raise ApiError(f"NSX tag already set to {current}, cannot set another tag without clearing it")
            return None  # clearing tag is a no-op in this case
        return NSXRemediationJob.start_request(self._cb, self.id, tag, set_tag)

    def get_asset_group_ids(self, membership="ALL"):
        """
        Finds the list of asset group IDs that this device is a member of.

        Args:
            membership (str): Can restrict the types of group membership returned by this method.  Values are "ALL"
                              to return all groups, "DYNAMIC" to return only groups that each member belongs to via the
                              asset group query, or "MANUAL" to return only groups that the members were manually
                              added to. Default is "ALL".

        Returns:
            list[str]: A list of asset group IDs this device belongs to.
        """
        if membership not in Device.VALID_ASSETGROUP_FILTERS:
            raise ApiError(f"Invalid filter value: {membership}")
        if membership == "ALL":
            return [g['id'] for g in self._info['asset_group']]
        elif membership == "MANUAL":
            return [g['id'] for g in self._info['asset_group'] if g['membership_type'] == 'MANUAL']
        elif membership == "DYNAMIC":
            return [g['id'] for g in self._info['asset_group'] if g['membership_type'] == 'DYNAMIC']

    def get_asset_groups(self, membership="ALL"):
        """
        Finds the list of asset groups that this device is a member of.

        Required Permissions:
            group-management(READ)

        Args:
            membership (str): Can restrict the types of group membership returned by this method.  Values are "ALL"
                              to return all groups, "DYNAMIC" to return only groups that each member belongs to via the
                              asset group query, or "MANUAL" to return only groups that the members were manually
                              added to. Default is "ALL".

        Returns:
            list[AssetGroup]: A list of asset groups this device belongs to.
        """
        return [self._cb.select("AssetGroup", v) for v in self.get_asset_group_ids(membership)]

    def add_to_groups_by_id(self, group_ids):
        """
        Given a list of asset group IDs, adds this device to each one as a member.

        Args:
            group_ids (list[str]): The list of group IDs to add this device to.
        """
        actual_group_ids = set(group_ids).difference(self.get_asset_group_ids("MANUAL"))
        for group_id in actual_group_ids:
            url = f"/asset_groups/v1/orgs/{self._cb.credentials.org_key}/groups/{group_id}/members"
            self._cb.post_object(url, {"action": "CREATE", "external_member_ids": [str(self._model_unique_id)]})
        if len(actual_group_ids) > 0:
            self._refresh()

    def add_to_groups(self, groups):
        """
        Given a list of asset groups, adds this device to each one as a member.

        Args:
            groups (list[AssetGroup]): The list of groups to add this device to.
        """
        existing_ids = self.get_asset_group_ids("MANUAL")
        actual_groups = [g for g in groups if g.id not in existing_ids]
        for group in actual_groups:
            group.add_members(self)
        if len(actual_groups) > 0:
            self._refresh()

    def remove_from_groups_by_id(self, group_ids):
        """
        Given a list of asset group IDs, removes this device from each one as a member.

        Args:
            group_ids (list[str]): The list of group IDs to remove this device from.
        """
        actual_group_ids = set(group_ids).intersection(self.get_asset_group_ids("MANUAL"))
        for group_id in actual_group_ids:
            url = f"/asset_groups/v1/orgs/{self._cb.credentials.org_key}/groups/{group_id}/members"
            self._cb.post_object(url, {"action": "REMOVE", "external_member_ids": [str(self._model_unique_id)]})
        if len(actual_group_ids) > 0:
            self._refresh()

    def remove_from_groups(self, groups):
        """
        Given a list of asset groups, removes this device from each one as a member.

        Args:
            groups (list[AssetGroup]): The list of groups to remove this device from.
        """
        existing_ids = self.get_asset_group_ids("MANUAL")
        actual_groups = [g for g in groups if g.id in existing_ids]
        for group in actual_groups:
            group.remove_members(self)
        if len(actual_groups) > 0:
            self._refresh()

    def preview_remove_policy_override(self):
        """
        Previews changes to this device's effective policy which result from removing its policy override.

        Required Permissions:
            org.policies (READ)

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return Device.preview_remove_policy_override_for_devices(self._cb, [self])

    @classmethod
    def _collect_devices(cls, devices):
        """
        Collects a list of devices as IDs.

        Args:
            devices (list): A list of items, each of which may be either integer device IDs or ``Device`` objects.

        Returns:
            list[int]: A list of integer device IDs.
        """
        device_ids = []
        for d in devices:
            if isinstance(d, Device):
                device_ids.append(d.id)
            elif isinstance(d, int):
                device_ids.append(d)
        return device_ids

    @classmethod
    def get_asset_groups_for_devices(cls, cb, devices, membership="ALL"):
        """
        Given a list of devices, returns lists of asset groups that they are members of.

        Required Permissions:
            group-management(READ)

        Args:
            cls (class): Class associated with the ``Device`` object.
            cb (BaseAPI): Reference to API object used to communicate with the server.
            devices (int, Device, or list): The devices to find the group membership of. This may be an integer
                                            device ID, a ``Device`` object, or a list of either integers or
                                            ``Device`` objects.
            membership (str): Can restrict the types of group membership returned by this method.  Values are "ALL"
                              to return all groups, "DYNAMIC" to return only groups that each member belongs to via the
                              asset group query, or "MANUAL" to return only groups that the members were manually
                              added to. Default is "ALL".

        Returns:
            dict: A dict containing member IDs as keys, and lists of group IDs as values.
        """
        if membership not in Device.VALID_ASSETGROUP_FILTERS:
            raise ApiError(f"Invalid filter value: {membership}")
        if isinstance(devices, int):
            device_ids = [str(devices)]
        elif isinstance(devices, Device):
            device_ids = [str(devices.id)]
        else:
            device_ids = [str(v) for v in Device._collect_devices(devices)]
        if len(device_ids) > 0:
            postdata = {"external_member_ids": device_ids}
            if membership != "ALL":
                postdata["membership_type"] = [membership]
            rc = cb.post_object(f"/asset_groups/v1/orgs/{cb.credentials.org_key}/members", postdata)
            return {int(k): v for k, v in rc.json().items()}
        else:
            return {}

    @classmethod
    def preview_add_policy_override_for_devices(cls, cb, policy_id, devices):
        """
        Previews changes to the effective policies for devices which result from setting a policy override on them.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            policy_id (int): The ID of the policy to be added to the devices as an override.
            devices (list): The devices which will have their policies overridden. Each entry in this list is either
                an integer device ID or a ``Device`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview",
                             {"action": "ADD_POLICY_OVERRIDE", "asset_ids": Device._collect_devices(devices),
                              "policy_id": policy_id})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]

    @classmethod
    def preview_remove_policy_override_for_devices(cls, cb, devices):
        """
        Previews changes to the effective policies for devices which result from removing their policy override.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            devices (list): The devices which will have their policy overrides removed. Each entry in this list
                is either an integer device ID or a ``Device`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/asset-groups/preview",
                             {"action": "REMOVE_POLICY_OVERRIDE", "asset_ids": Device._collect_devices(devices)})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]


class DeviceFacet(UnrefreshableModel):
    """
    Represents a device field in a facet search.

    *Faceting* is a search technique that categorizes search results according to common attributes. This allows
    users to explore and discover information within a dataset, in this case, the set of devices.

    Example:
        >>> facets = api.select(Device).facets(['policy_id'])
        >>> for value in facets[0].values_:
        ...     print(f"Policy ID {value.id}: {value.total} device(s)")
    """
    urlobject = "/appservices/v6/orgs/{0}/devices/_facet"
    primary_key = "id"
    swagger_meta_file = "platform/models/device_facet.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the ``DeviceFacet`` object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): Not used.
            initial_data (dict): Initial data used to populate the facet.
        """
        super(DeviceFacet, self).__init__(cb, model_unique_id, initial_data, force_init=False, full_doc=True)
        self._values = [DeviceFacet.DeviceFacetValue(cb, self, item['id'], item) for item in initial_data['values']]

    class DeviceFacetValue(UnrefreshableModel):
        """
        Represents a value of a particular faceted field.

        *Faceting* is a search technique that categorizes search results according to common attributes. This allows
        users to explore and discover information within a dataset, in this case, the set of devices.
        """
        def __init__(self, cb, outer, model_unique_id, initial_data):
            """
            Initialize the ``DeviceFacetValue`` object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                outer (DeviceFacet): Reference to outer facet object.
                model_unique_id (str): Value ID.
                initial_data (dict): Initial data used to populate the facet value.
            """
            super(DeviceFacet.DeviceFacetValue, self).__init__(cb, model_unique_id, initial_data, force_init=False,
                                                               full_doc=True)
            self._outer = outer

        def query_devices(self):
            """
            Set up a device query to find all devices that match this facet value.

            Example:
                >>> facets = api.select(Device).facets(['policy_id'])
                >>> for value in facets[0].values_:
                ...     print(f"Policy ID = {value.id}:")
                ...     for dev in value.query_devices():
                ...         print(f"    {dev.name} ({dev.last_external_ip_address})")

            Returns:
                DeviceQuery: A new ``DeviceQuery`` set with the criteria, which may have additional criteria added
                    to it.
            """
            query = self._cb.select(Device)
            if self._outer.field == 'policy_id':
                query.set_policy_ids([int(self.id)])
            elif self._outer.field == 'status':
                query.set_status([self.id])
            elif self._outer.field == 'os':
                query.set_os([self.id.upper()])
            elif self._outer.field == 'ad_group_id':
                query.set_ad_group_ids([int(self.id)])
            elif self._outer.field == "cloud_provider_account_id":
                query.set_cloud_provider_account_id([self.id])
            elif self._outer.field == "auto_scaling_group_name":
                query.set_auto_scaling_group_name([self.id])
            elif self._outer.field == "virtual_private_cloud_id":
                query.set_virtual_private_cloud_id([self.id])
            elif self._outer.field == "deployment_type":
                query.set_deployment_type([self.id])
            return query

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the Device type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.
        """
        raise NonQueryableModel("use facets() on DeviceQuery to get DeviceFacet")

    def _subobject(self, name):
        """
        Returns the "subobject value" of the given attribute.

        Args:
            name (str): Name of the subobject value to be returned.

        Returns:
            Any: Subobject value for the attribute, or ``None`` if there is none.
        """
        if name == 'values':
            return self._values
        return super(DeviceFacet, self)._subobject(name)

    @property
    def values_(self):
        """Returns the list of facet values for this facet."""
        return self._values


############################################
# Device Queries

class DeviceSearchQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                        IterableQueryMixin, AsyncQueryMixin):
    """
    Query object that is used to locate ``Device`` objects.

    The ``DeviceSearchQuery`` is constructed via SDK functions like the ``select()`` method on ``CBCloudAPI``.
    The user would then add a query and/or criteria to it before iterating over the results.
    """
    VALID_OS = ["WINDOWS", "ANDROID", "MAC", "IOS", "LINUX", "OTHER"]
    VALID_STATUSES = ["PENDING", "REGISTERED", "UNINSTALLED", "DEREGISTERED",
                      "ACTIVE", "INACTIVE", "ERROR", "ALL", "BYPASS_ON",
                      "BYPASS", "QUARANTINE", "SENSOR_OUTOFDATE",
                      "DELETED", "LIVE"]
    VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH", "MISSION_CRITICAL"]
    VALID_DEPLOYMENT_TYPES = ["ENDPOINT", "WORKLOAD", "VDI", "AWS", "AZURE", "GCP"]
    VALID_FACET_FIELDS = ["policy_id", "status", "os", "ad_group_id", "cloud_provider_account_id",
                          "auto_scaling_group_name", "virtual_private_cloud_id", "deployment_type"]

    def __init__(self, doc_class, cb):
        """
        Initialize the ``DeviceSearchQuery``.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(DeviceSearchQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filter = {}
        self._exclusions = {}
        self._sortcriteria = {}
        self._search_after = None
        self.num_remaining = None
        self.num_found = None
        self.max_rows = -1

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
        """
        if not all((prio in DeviceSearchQuery.VALID_PRIORITIES) for prio in target_priorities):
            raise ApiError("One or more invalid target priority values")
        self._update_criteria("target_priority", target_priorities)
        return self

    def set_cloud_provider_account_id(self, account_ids):
        """
        Restricts the devices that this query is performed on to the specified cloud provider account IDs.

        Args:
            account_ids (list): List of account IDs to restrict search to.

        Returns:
            DeviceSearchQuery: This instance.
        """
        self._update_criteria("cloud_provider_account_id", account_ids)
        return self

    def set_auto_scaling_group_name(self, group_names):
        """
        Restricts the devices that this query is performed on to the specified auto scaling group names.

        Args:
            group_names (list): List of group names to restrict search to.

        Returns:
            DeviceSearchQuery: This instance.
        """
        self._update_criteria("auto_scaling_group_name", group_names)
        return self

    def set_virtual_private_cloud_id(self, cloud_ids):
        """
        Restricts the devices that this query is performed on to the specified virtual private cloud IDs.

        Args:
            cloud_ids (list): List of cloud IDs to restrict search to.

        Returns:
            DeviceSearchQuery: This instance.
        """
        self._update_criteria("virtual_private_cloud_id", cloud_ids)
        return self

    def set_exclude_sensor_versions(self, sensor_versions):
        """
        Restricts the devices that this query is performed on to exclude specified sensor versions.

        Args:
            sensor_versions (list): List of sensor versions to be excluded.

        Returns:
            DeviceSearchQuery: This instance.
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
        """
        if direction not in CriteriaBuilderSupportMixin.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def set_deployment_type(self, deployment_type):
        """
        Restricts the devices that this query is performed on to the specified deployment types.

        Args:
            deployment_type (list): List of deployment types to restrict search to.

        Returns:
            DeviceSearchQuery: This instance.
        """
        if not all((type in DeviceSearchQuery.VALID_DEPLOYMENT_TYPES) for type in deployment_type):
            raise ApiError("invalid deployment_type specified")
        self._update_criteria("deployment_type", deployment_type)
        return self

    def set_max_rows(self, max_rows):
        """
        Sets the max number of devices to fetch in a singular query

        Args:
            max_rows (integer): Max number of devices. Must be in the range (0, 10000).

        Returns:
            DeviceSearchQuery: This instance.
        """
        if max_rows < 0 or max_rows > 10000:
            raise ApiError("Max rows must be between 0 and 10000")
        self.max_rows = max_rows
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
        request = {}
        if mycrit:
            request["criteria"] = mycrit
        if self._exclusions:
            request["exclusions"] = self._exclusions
        query = self._query_builder._collapse()
        if query:
            request["query"] = query
        if from_row > 1:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        elif self.max_rows >= 0:
            request["rows"] = self.max_rows
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

        Required Permissions:
            device(READ)
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
            device(READ)

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Yields:
            Device: The individual devices which match the query.
        """
        url = self._build_url("/_search")
        current = from_row + 1
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

            from_row = current - 1
            if current >= self._total_results:
                still_querying = False
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query on devices.

        Required Permissions:
            device(READ)

        Args:
            context (object): The context returned by _init_async_query. May be ``None``.

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

    def facets(self, fieldlist, max_rows=0):
        """
        Return information about the facets for all matching devices, using the defined criteria.

        Example:
            >>> query = api.select(Device).where('')
            >>> facets = query.facets(['policy_id', 'status', 'os', 'ad_group_id'])
            >>> for f in facets:
            ...     print(f"Field {f.field} - {len(f.values_)} distinct values")

        Required Permissions:
            device(READ)

        Args:
            fieldlist (list[str]): List of facet field names. Valid names are "policy_id", "status", "os",
                                   "ad_group_id", "cloud_provider_account_id", "auto_scaling_group_name",
                                   and "virtual_private_cloud_id".
            max_rows (int): The maximum number of rows to return. 0 means return all rows.

        Returns:
            list[DeviceFacet]: A list of facet information.
        """
        if not fieldlist:
            raise ApiError("At least one term field must be specified")
        if not all((field in DeviceSearchQuery.VALID_FACET_FIELDS) for field in fieldlist):
            raise ApiError("One or more invalid term field names")
        request = self._build_request(-1, -1)
        if 'rows' in request:
            del request['rows']
        if 'sort' in request:
            del request['sort']
        terms = {'fields': fieldlist}
        if max_rows > 0:
            terms['rows'] = max_rows
        request['terms'] = terms
        url = self._build_url("/_facet")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return [DeviceFacet(self._cb, None, item) for item in result['results']]

    def download(self):
        """
        Uses the query parameters that have been set to download all device listings in CSV format.

        Deprecated:
            Use DeviceSearchQuery.export for increased export capabilities and limits

        Example:
            >>> cb.select(Device).set_status(["ALL"]).download()

        Required Permissions:
            device(READ)

        Returns:
            str: The CSV raw data as returned from the server.

        Raises:
            ApiError: If status values have not been set before calling this function.
        """
        log.warning("DeviceSearchQuery.download is deprecated, use DeviceSearchQuery.export instead")
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

    def export(self):
        """
        Starts the process of exporting Devices from the organization in CSV format.

        Example:
            >>> cb.select(Device).set_status(["ACTIVE"]).export()

        Required Permissions:
            device(READ)

        Returns:
            Job: The asynchronous job that will provide the export output when the server has prepared it.
        """
        request = self._build_request(0, -1)
        request["format"] = "CSV"
        url = self._build_url("/_export")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return Job(self._cb, result["id"], result)

    def scroll(self, rows=10000):
        """
        Iteratively paginate all Devices beyond the 10k max search limits.

        To fetch the next set of Devices repeatively call the scroll function until
        `DeviceSearchQuery.num_remaining == 0` or no results are returned.

        Example:
            >>> cb.select(Device).set_status(["ACTIVE"]).scroll(100)

        Required Permissions:
            device(READ)

        Args:
            rows (int): The number of rows to fetch

        Returns:
            list[Device]: The list of results
        """
        if self.num_remaining == 0:
            return []
        elif rows > 10000:
            rows = 10000

        url = self._build_url("/_scroll")

        # Sort by last_contact_time enforced
        self._sort = {}

        request = self._build_request(0, rows)

        if self._search_after is not None:
            request["search_after"] = self._search_after

        resp = self._cb.post_object(url, body=request)
        resp_json = resp.json()

        # Calculate num_remaining until backend provides in response
        if self._search_after is None:
            self.num_remaining = resp_json["num_found"] - len(resp_json["results"])
            self.num_found = resp_json["num_found"]
        elif self.num_found != resp_json["num_found"]:
            diff = resp_json["num_found"] - self.num_found
            self.num_remaining = self.num_remaining - len(resp_json["results"]) + diff
        else:
            self.num_remaining = self.num_remaining - len(resp_json["results"])

        if self.num_remaining < 0:
            self.num_remaining = 0

        # Capture latest state
        self._search_after = resp_json["search_after"]

        results = []
        for item in resp_json["results"]:
            results.append(self._doc_class(self._cb, item["id"], item))

        return results

    def _bulk_device_action(self, action_type, options=None):
        """
        Perform a bulk action on all devices matching the current search criteria.

        Required Permissions:
            Dependent on the action_type.

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

        Required Permissions:
            device.bg-scan(EXECUTE)

        Args:
            scan (bool): ``True`` to turn background scan on, ``False`` to turn it off.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("BACKGROUND_SCAN", self._cb._action_toggle(scan))

    def bypass(self, enable):
        """
        Set the bypass option for the specified devices.

        Required Permissions:
            device.bypass(EXECUTE)

        Args:
            enable (bool): ``True`` to enable bypass, ``False`` to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("BYPASS", self._cb._action_toggle(enable))

    def delete_sensor(self):
        """
        Delete the specified sensor devices.

        Required Permissions:
            device.deregistered(DELETE)

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("DELETE_SENSOR")

    def uninstall_sensor(self):
        """
        Uninstall the specified sensor devices.

        Required Permissions:
            device.uninstall(EXECUTE)

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UNINSTALL_SENSOR")

    def quarantine(self, enable):
        """
        Set the quarantine option for the specified devices.

        Required Permissions:
            device.quarantine(EXECUTE)

        Args:
            enable (bool): ``True`` to enable quarantine, ``False`` to disable it.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("QUARANTINE", self._cb._action_toggle(enable))

    def update_policy(self, policy_id):
        """
        Set the current policy for the specified devices.

        Required Permissions:
            device.policy(UPDATE)

        Args:
            policy_id (int): ID of the policy to set for the devices.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UPDATE_POLICY", {"policy_id": policy_id})

    def update_sensor_version(self, sensor_version):
        """
        Update the sensor version for the specified devices.

        Required Permissions:
            org.kits(EXECUTE)

        Args:
            sensor_version (dict): New version properties for the sensor.

        Returns:
            str: The JSON output from the request.
        """
        return self._bulk_device_action("UPDATE_SENSOR_VERSION", {"sensor_version": sensor_version})
