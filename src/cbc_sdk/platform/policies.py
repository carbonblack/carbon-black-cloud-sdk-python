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

"""Policy implementation as part of Platform API"""
import copy
import json
from types import MappingProxyType
from cbc_sdk.base import MutableBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin
from cbc_sdk.platform.devices import Device
from cbc_sdk.platform.policy_ruleconfigs import (PolicyRuleConfig, CorePreventionRuleConfig,
                                                 HostBasedFirewallRuleConfig, DataCollectionRuleConfig,
                                                 BypassRuleConfig)
from cbc_sdk.platform.previewer import DevicePolicyChangePreview
from cbc_sdk.errors import ApiError, ServerError, InvalidObjectError


SPECIFIC_RULECONFIGS = MappingProxyType({
    "core_prevention": CorePreventionRuleConfig,
    "host_based_firewall": HostBasedFirewallRuleConfig,
    "data_collection": DataCollectionRuleConfig,
    "bypass": BypassRuleConfig
})


class Policy(MutableBaseModel):
    """
    Represents a policy within the organization.

    Create one of these objects (either directly or with the CBCloudAPI.create() method) and set its properties,
    then call its save() method to create the policy on the server. This requires the org.policies(CREATE) permission.

    Alternatively, you may call Policy.create() to get a PolicyBuilder, use its methods to set the properties of the
    new policy, call its build() method to build the populated Policy, then call the policy save() method.

    To update a Policy, change the values of its property fields, then call the policy's save() method.  This requires
    the org.policies(UPDATE) permission.

    To delete an existing Policy, call its delete() method. This requires the org.policies(DELETE) permission.

    For information on values for policy settings including enumeration values, see the Policy Service API page:
    https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/policy-service/#fields
    """
    urlobject = "/policyservice/v1/orgs/{0}/policies"
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/policy.yaml"
    VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH", "MISSION_CRITICAL"]
    VALID_SENSOR_SETTINGS = ["SHOW_UI", "ALLOW_UNINSTALL", "ALLOW_UPLOAD", "QUARANTINE_DEVICE", "ENABLE_FORENSICS",
                             "LOGGING_LEVEL", "QUARANTINE_DEVICE_MESSAGE", "ENABLE_THREAT_SHARING", "SET_SENSOR_MODE",
                             "SENSOR_RESET", "BLOCK_REMOVABLE_MEDIA", "POLICY_ACTION_OVERRIDE", "BACKGROUND_SCAN",
                             "RATE_LIMIT", "QUEUE_SIZE", "DROP_CONNECTION_TIME", "CONNECTION_LIMIT", "LEARNING_MODE",
                             "SET_AV_MODE", "SCAN_NETWORK_DRIVE", "BYPASS_AFTER_RESTART_MINS",
                             "BYPASS_AFTER_LOGIN_MINS", "HELP_MESSAGE", "SHOW_FULL_UI", "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                             "DELAY_EXECUTE", "ALLOW_INLINE_BLOCKING", "PRESERVE_SYSTEM_MEMORY_SCAN", "HASH_MD5",
                             "SCAN_LARGE_FILE_READ", "SECURITY_CENTER_OPT", "CB_LIVE_RESPONSE", "UNINSTALL_CODE",
                             "ALLOW_EXPEDITED_SCAN", "UBS_OPT_IN", "DISABLE_MALWARE_SERVICES"]
    VALID_SCAN_MODES = ["NORMAL", "AGGRESSIVE"]
    VALID_SCAN_OPTIONS = ["AUTOSCAN", "DISABLED"]
    VALID_DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the Policy object.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): ID of the policy.
            initial_data (dict): Initial data used to populate the policy.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(Policy, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                     force_init=force_init if initial_data else True, full_doc=full_doc)
        self._object_rules = None
        self._object_rules_need_load = True
        self._object_rule_configs = None
        self._object_rule_configs_need_load = True
        self._ruleconfig_presentation = None
        if "version" not in self._info:
            self._info["version"] = 2
        if model_unique_id is None:
            self.touch(True)

    class PolicyBuilder:
        """
        Builder object to simplify the creation of new Policy objects.

        To use, call Policy.create() to get a PolicyBuilder, use its methods to set the properties of the
        new policy, call its build() method to build the populated Policy, then call the policy save() method.
        The org.policy(CREATE) permission is required.

        Examples:
            >>> builder = Policy.create(api)
            >>> builder.set_name("New Policy").set_priority("MEDIUM").set_description("New policy description")
            >>> # more calls here to set up rules, sensor settings, etc.
            >>> policy = builder.build()
            >>> policy.save()
        """
        def __init__(self, cb):
            """
            Initialize the PolicyBuilder object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
            """
            self._cb = cb
            self._new_policy_data = {"org_key": cb.credentials.org_key, "priority_level": "MEDIUM", "is_system": False}
            self._sensor_settings = {}
            self._new_rules = []
            self._new_rule_configs = []

        def set_name(self, name):
            """
            Set the new policy name.

            Args:
                name (str): The new policy name.

            Returns:
                PolicyBuilder: This object.
            """
            self._new_policy_data["name"] = name
            return self

        def set_priority(self, priority):
            """
            Set the new policy's priority. Default is MEDIUM.

            Args:
                priority (str): The priority, either "LOW", "MEDIUM", "HIGH", or "MISSION_CRITICAL".

            Returns:
                PolicyBuilder: This object.

            Raises:
                ApiError: If an invalid priority value is passed in.
            """
            if priority in Policy.VALID_PRIORITIES:
                self._new_policy_data["priority_level"] = priority
            else:
                raise ApiError(f"invalid priority level: {priority}")
            return self

        def set_description(self, descr):
            """
            Set the new policy description.

            Args:
                descr (str): The new policy description.

            Returns:
                PolicyBuilder: This object.
            """
            self._new_policy_data["description"] = descr
            return self

        def set_auto_deregister_interval(self, interval):
            """
            Set the time in milliseconds after a VDI goes inactive to deregister it.

            Args:
                interval (int): The desired interval in milliseconds.

            Returns:
                PolicyBuilder: This object.
            """
            self._new_policy_data["auto_deregister_inactive_vdi_interval_ms"] = interval
            return self

        def set_auto_delete_bad_hash_delay(self, delay):
            """
            Set the delay in milliseconds after which known malware will be deleted.

            Args:
                delay (int): The desired delay interval in milliseconds.

            Returns:
                PolicyBuilder: This object.
            """
            self._new_policy_data["auto_delete_known_bad_hashes_delay"] = delay
            return self

        def set_avira_protection_cloud(self, enabled, max_exe_delay=None, max_file_size=None, risk_level=None):
            """
            Set the settings for third-party unknown binary reputation analysis.

            Args:
                enabled (bool): True to enable unknown binary reputation analysis.
                max_exe_delay (int): Time before sending unknown binary for analysis, in seconds.
                max_file_size (int): Maximum size of file to send for analysis, in megabytes.
                risk_level (int): Risk level to send for analysis (0-7).

            Returns:
                PolicyBuilder: This object.
            """
            apc = {"enabled": enabled}
            if max_exe_delay is not None:
                apc["max_exe_delay"] = max_exe_delay
            if max_file_size is not None:
                apc["max_file_size"] = max_file_size
            if risk_level is not None:
                apc["risk_level"] = risk_level
            av_settings = self._new_policy_data.get("av_settings", {})
            av_settings["avira_protection_cloud"] = apc
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_on_access_scan(self, enabled, mode="NORMAL"):
            """
            Sets the local scan settings.

            Args:
                enabled (bool): True to enable local scan.
                mode (str): The mode to operate in, either "NORMAL" or "AGGRESSIVE".

            Returns:
                PolicyBuilder: This object.

            Raises:
                ApiError: If an invalid value is passed for the "mode" parameter.
            """
            if mode not in Policy.VALID_SCAN_MODES:
                raise ApiError(f"invalid scan mode: {mode}")
            av_settings = self._new_policy_data.get("av_settings", {})
            av_settings["on_access_scan"] = {"enabled": enabled, "mode": mode}
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_on_demand_scan(self, enabled, profile="NORMAL", scan_usb="AUTOSCAN", scan_cd_dvd="AUTOSCAN"):
            """
            Sets the background scan settings.

            Args:
                enabled (bool): True to enable background scan.
                profile (str): The background scan mode, either "NORMAL" or "AGGRESSIVE".
                scan_usb (str): Either "AUTOSCAN" to scan USB devices, or "DISABLED" to not do so.
                scan_cd_dvd (str): Either "AUTOSCAN" to scan CDs and DVDs, or "DISABLED" to not do so.

            Returns:
                PolicyBuilder: This object.

            Raises:
                ApiError: If an invalid value is passed for any parameter.
            """
            if profile not in Policy.VALID_SCAN_MODES:
                raise ApiError(f"invalid scan mode: {profile}")
            if scan_usb not in Policy.VALID_SCAN_OPTIONS:
                raise ApiError(f"invalid USB scan option: {scan_usb}")
            if scan_cd_dvd not in Policy.VALID_SCAN_OPTIONS:
                raise ApiError(f"invalid CD/DVD scan option: {scan_cd_dvd}")
            av_settings = self._new_policy_data.get("av_settings", {})
            ods = av_settings.get("on_demand_scan", {})
            ods["enabled"] = enabled
            ods["profile"] = profile
            ods["scan_usb"] = scan_usb
            ods["scan_cd_dvd"] = scan_cd_dvd
            av_settings["on_demand_scan"] = ods
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_on_demand_scan_schedule(self, days, start_hour, range_hours, recover_if_missed=True):
            """
            Sets the schedule for when background scans will be performed.

            Args:
                days (list[str]): The days on which to perform background scans.
                start_hour (int): The hour of the day at which to perform the scans.
                range_hours (int): The range of hours over which to perform the scans.
                recover_if_missed (bool): True if the background scan should be performed ASAP if it's been missed.

            Returns:
                PolicyBuilder: This object.

            Raises:
                ApiError: If an invalid value is passed for a day of the week.
            """
            if not all([v in Policy.VALID_DAYS for v in days]):
                raise ApiError("invalid day(s) of the week")
            av_settings = self._new_policy_data.get("av_settings", {})
            ods = av_settings.get("on_demand_scan", {})
            ods["schedule"] = {"days": days, "start_hour": start_hour, "range_hours": range_hours,
                               "recovery_scan_if_missed": recover_if_missed}
            av_settings["on_demand_scan"] = ods
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_signature_update(self, enabled):
            """
            Set the enable status for signature updates.

            Args:
                enabled (bool): True to enable signature updates.

            Returns:
                PolicyBuilder: This object.
            """
            av_settings = self._new_policy_data.get("av_settings", {})
            sigupdate = av_settings.get("signature_update", {})
            sigupdate["enabled"] = enabled
            av_settings["signature_update"] = sigupdate
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_signature_update_schedule(self, full_interval_hours, initial_random_delay_hours, interval_hours):
            """
            Set the signature update schedule.

            Args:
                full_interval_hours (int): The interval in hours between signature updates.
                initial_random_delay_hours (int): The initial delay in hours before the first signature update.
                interval_hours (int): The interval in hours between signature updates.

            Returns:
                PolicyBuilder: This object.
            """
            av_settings = self._new_policy_data.get("av_settings", {})
            sigupdate = av_settings.get("signature_update", {})
            sigupdate["schedule"] = {"full_interval_hours": full_interval_hours,
                                     "initial_random_delay_hours": initial_random_delay_hours,
                                     "interval_hours": interval_hours}
            av_settings["signature_update"] = sigupdate
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_update_servers_override(self, names):
            """
            Sets the list of update servers to override offsite/onsite settings.

            Args:
                names (list[str]): The server names to use, as a list of URIs.

            Returns:
                PolicyBuilder: This object.
            """
            av_settings = self._new_policy_data.get("av_settings", {})
            servers = av_settings.get("update_servers", {})
            servers["servers_override"] = names
            av_settings["update_servers"] = servers
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_update_servers_onsite(self, names, preferred_servers=None):
            """
            Sets the list of update servers for internal devices.

            Args:
                names (list[str]): The list of available update servers, as URIs.
                preferred_servers (list[str]): The list of update servers to be considered "preferred," as URIs.

            Returns:
                PolicyBuilder: This object.
            """
            if preferred_servers is None:
                preferred_servers = []
            av_settings = self._new_policy_data.get("av_settings", {})
            servers = av_settings.get("update_servers", {})
            servers["servers_for_onsite_devices"] = [{"server": uri,
                                                      "preferred": True if uri in preferred_servers else False}
                                                     for uri in names]
            servers["servers_for_onsite_devices"].extend([{"server": uri, "preferred": True}
                                                          for uri in preferred_servers if uri not in names])
            av_settings["update_servers"] = servers
            self._new_policy_data["av_settings"] = av_settings
            return self

        def set_update_servers_offsite(self, names):
            """
            Sets the list of update servers for offsite devices.

            Args:
                names (list[str]): The list of update servers, as URIs.

            Returns:
                PolicyBuilder: This object.
            """
            av_settings = self._new_policy_data.get("av_settings", {})
            servers = av_settings.get("update_servers", {})
            servers["servers_for_offsite_devices"] = names
            av_settings["update_servers"] = servers
            self._new_policy_data["av_settings"] = av_settings
            return self

        def add_directory_action_rule(self, path, file_upload, protection):
            """
            Add a directory action rule to the new policy.

            Args:
                path (str): Path to the file or directory.
                file_upload (bool): True to allow the deployed sensor to upload from that path.
                protection (bool): True to deny the deployed sensor to upload from that path.

            Returns:
                PolicyBuilder: This object.
            """
            da_rules = self._new_policy_data.get("directory_action_rules", [])
            da_rules.append({"path": path, "file_upload": file_upload, "protection": protection})
            self._new_policy_data["directory_action_rules"] = da_rules
            return self

        def _add_rule(self, rule_data):
            """
            Add rule data to the new policy.

            Args:
                rule_data (dict): Rule data specified as a dictionary.

            Raises:
                InvalidObjectError: If the rule data passed in is not valid.
            """
            new_rule = PolicyRule(self._cb, parent=None, model_unique_id=None, initial_data=rule_data, force_init=False,
                                  full_doc=True)
            new_rule.validate()
            self._new_rules.append(new_rule)

        def _add_rule_config(self, rule_config_data):
            """
            Add rule configuration data to the new policy.

            Args:
                rule_config_data (dict): Rule configuration data specified as a dictionary.

            Raises:
                InvalidObjectError: If the rule configuration data passed in is not valid.
            """
            new_rule_config = Policy._create_rule_config(self._cb, None, rule_config_data)
            new_rule_config.validate()
            self._new_rule_configs.append(new_rule_config)

        def add_rule_copy(self, rule):
            """
            Adds a copy of an existing rule to this new policy.

            Args:
                rule (PolicyRule): The rule to copy and add to this object.

            Returns:
                PolicyBuilder: This object.

            Raises:
                InvalidObjectError: If the rule data passed in is not valid.
            """
            ruledata = copy.deepcopy(rule._info)
            if "id" in ruledata:
                del ruledata["id"]
            self._add_rule(ruledata)
            return self

        def add_rule(self, app_type, app_value, operation, action, required=True):
            """
            Add a new rule as discrete data elements to the new policy.

            Args:
                app_type (str): Specifies "NAME_PATH", "SIGNED_BY", or "REPUTATION".
                app_value (str): Value of the attribute specified by `app_type` to be matched.
                operation (str): The type of behavior the application is performing.
                action (str): The action the sensor will take when the application performs the specified action.
                required (bool): True if this rule is required, False if not.

            Returns:
                PolicyBuilder: This object.

            Raises:
                InvalidObjectError: If the rule data passed in is not valid.
            """
            ruledata = {"required": required, "action": action, "application": {"type": app_type, "value": app_value},
                        "operation": operation}
            self._add_rule(ruledata)
            return self

        def add_rule_config_copy(self, rule_config):
            """
            Adds a copy of an existing rule configuration to this new policy.

            Args:
                rule_config (PolicyRuleConfig): The rule configuration to copy and add to this object.

            Returns:
                PolicyBuilder: This object.

            Raises:
                InvalidObjectError: If the rule configuration data passed in is not valid.
            """
            ruleconfigdata = copy.deepcopy(rule_config._info)
            self._add_rule_config(ruleconfigdata)
            return self

        def add_rule_config(self, config_id, name, category, **kwargs):
            """
            Add a new rule configuration as discrete data elements to the new policy.

            Args:
                config_id (str): ID of the rule configuration object (a GUID).
                name (str): Name of the rule configuration object.
                category (str): Category of the rule configuration object.
                **kwargs (dict): Parameter values for the rule configuration object.

            Returns:
                PolicyBuilder: This object.

            Raises:
                InvalidObjectError: If the rule configuration data passed in is not valid.
            """
            ruleconfigdata = {"id": config_id, "name": name, "category": category, "inherited_from": "",
                              "parameters": copy.deepcopy(kwargs)}
            self._add_rule_config(ruleconfigdata)
            return self

        def add_sensor_setting(self, name, value):
            """
            Add a sensor setting to the policy.

            Args:
                name (str): Sensor setting name.
                value (str): Sensor setting value.

            Returns:
                PolicyBuilder: This object.

            Raises:
                ApiError: If the sensor setting name is not a valid one.
            """
            if name in Policy.VALID_SENSOR_SETTINGS:
                self._sensor_settings[name] = value
            else:
                raise ApiError(f"invalid sensor setting: {name}")
            return self

        def set_managed_detection_response_permissions(self, policy_mod, quarantine):
            """
            Set the permissions for managed detection and response.

            Args:
                policy_mod (bool): True to allow MDR team to modify the policy.
                quarantine (bool): True to allow MDR team to quarantine endpoints/workloads associated with the policy.

            Returns:
                PolicyBuilder: This object.
            """
            self._new_policy_data["managed_detection_response_permissions"] = {"policy_modification": policy_mod,
                                                                               "quarantine": quarantine}
            return self

        def build(self):
            """
            Build a new Policy object using the contents of this builder.

            The new policy must have `save()` called on it to be saved to the server.

            Returns:
                Policy: The new Policy object.
            """
            new_policy = copy.deepcopy(self._new_policy_data)
            settings = [{"name": name, "value": value} for name, value in self._sensor_settings.items()]
            settings.sort(key=lambda item: item["name"])
            new_policy["sensor_settings"] = settings
            new_policy["rules"] = [copy.deepcopy(r._info) for r in self._new_rules]
            new_policy["rule_configs"] = [copy.deepcopy(rcfg._info) for rcfg in self._new_rule_configs]
            return Policy(self._cb, None, new_policy, False, True)

    def _subobject(self, name):  # pragma: no cover
        """
        Returns the "subobject value" of the given attribute.

        Args:
            name (str): Name of the subobject value to be returned.

        Returns:
            Any: Subobject value for the attribute, or None if there is none.
        """
        if name == 'rules':
            return list(self.object_rules.values())
        if name == 'rule_configs':
            return list(self.object_rule_configs.values())
        return super(Policy, self)._subobject(name)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            Query: The query object for this alert type.
        """
        return PolicyQuery(cls, cb)

    def _build_api_request_uri(self, http_method="GET"):
        """
        Create the URL to be used to access instances of Policy.

        Args:
            http_method (str): Unused.

        Returns:
            str: The actual URL
        """
        uri = Policy.urlobject.format(self._cb.credentials.org_key)
        if self._model_unique_id is not None:
            return f"{uri}/{self._model_unique_id}"
        return uri

    def _refresh(self):
        """
        Refreshes the policy object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            True if the refresh was successful.
        """
        rc = super(Policy, self)._refresh()
        self._object_rules_need_load = True
        self._object_rule_configs_need_load = True
        return rc

    def is_dirty(self):
        """
        Returns whether or not any fields of this object have been changed.

        Returns:
            bool: True if any fields of this object have been changed, False if not.
        """
        if super(Policy, self).is_dirty():
            return True
        # we need to check the rules and rule configs as well
        if not self._object_rules_need_load:
            if any(rule.is_dirty() for rule in self._object_rules.values()):
                return True
        if not self._object_rule_configs_need_load:
            if any(rule_config.is_dirty() for rule_config in self._object_rule_configs.values()):
                return True
        return False

    @property
    def rules(self):
        """
        Returns a dictionary of rules and rule IDs for this Policy.

        Returns:
            dict: A dictionary with rule IDs as keys and rule data as values.
        """
        return dict([(r.get("id"), copy.deepcopy(r)) for r in self._info.get("rules", [])])

    @property
    def object_rules(self):
        """
        Returns a dictionary of rule objects and rule IDs for this Policy.

        Returns:
            dict: A dictionary with rule IDs as keys and PolicyRule objects as values.
        """
        if self._object_rules_need_load:
            ruleobjects = [PolicyRule(self._cb, self, r.get("id"), r, False, True)
                           for r in self._info.get("rules", [])]
            self._object_rules = dict([(robj.id, robj) for robj in ruleobjects])
            self._object_rules_need_load = False
        return self._object_rules

    @property
    def object_rule_configs(self):
        """
        Returns a dictionary of rule configuration IDs and objects for this Policy.

        Returns:
            dict: A dictionary with rule configuration IDs as keys and PolicyRuleConfig objects as values.
        """
        if self._object_rule_configs_need_load:
            cfgs = self._info.get("rule_configs", [])
            ruleconfigobjects = [self._create_rule_config(self._cb, self, cfg) for cfg in cfgs]
            self._object_rule_configs = dict([(rconf.id, rconf) for rconf in ruleconfigobjects])
            self._object_rule_configs_need_load = False
        return self._object_rule_configs

    @property
    def object_rule_configs_list(self):
        """
        Returns a list of rule configuration objects for this Policy.

        Returns:
            list: A list of PolicyRuleConfig objects.
        """
        return [rconf for rconf in self.object_rule_configs.values()]

    @property
    def bypass_rule_configs(self):
        """
        Returns a dictionary of bypass rule configuration IDs and objects for this Policy.

        Returns:
            dict: A dictionary with bypass rule configuration IDs as keys and BypassRuleConfig objects
                  as values.
        """
        return {key: rconf for (key, rconf) in self.object_rule_configs.items()
                if isinstance(rconf, BypassRuleConfig)}

    @property
    def bypass_rule_configs_list(self):
        """
        Returns a list of bypass rule configuration objects for this Policy.

        Returns:
            list: A list of BypassRuleConfig objects.
        """
        return [rconf for rconf in self.object_rule_configs.values() if isinstance(rconf, BypassRuleConfig)]

    @property
    def core_prevention_rule_configs(self):
        """
        Returns a dictionary of core prevention rule configuration IDs and objects for this Policy.

        Returns:
            dict: A dictionary with core prevention rule configuration IDs as keys and CorePreventionRuleConfig objects
                  as values.
        """
        return {key: rconf for (key, rconf) in self.object_rule_configs.items()
                if isinstance(rconf, CorePreventionRuleConfig)}

    @property
    def core_prevention_rule_configs_list(self):
        """
        Returns a list of core prevention rule configuration objects for this Policy.

        Returns:
            list: A list of CorePreventionRuleConfig objects.
        """
        return [rconf for rconf in self.object_rule_configs.values() if isinstance(rconf, CorePreventionRuleConfig)]

    @property
    def host_based_firewall_rule_config(self):
        """
        Returns the host-based firewall rule configuration for this policy.

        Returns:
            HostBasedFirewallRuleConfig: The host-based firewall rule configuration, or None.

        Raises:
            InvalidObjectError: If there's more than one host-based firewall rule configuration (should not happen).
        """
        tmp = [rconf for rconf in self.object_rule_configs.values() if isinstance(rconf, HostBasedFirewallRuleConfig)]
        if not tmp:
            return None
        if len(tmp) > 1:
            raise InvalidObjectError("found multiple host-based firewall rule configurations")
        return tmp[0]

    @property
    def data_collection_rule_configs(self):
        """
        Returns a dictionary of data collection rule configuration IDs and objects for this Policy.

        Returns:
            dict: A dictionary with data collection rule configuration IDs as keys and DataCollectionRuleConfig objects
                  as values.
        """
        return {key: rconf for (key, rconf) in self.object_rule_configs.items()
                if isinstance(rconf, DataCollectionRuleConfig)}

    @property
    def data_collection_rule_configs_list(self):
        """
        Returns a list of data collection rule configuration objects for this Policy.

        Returns:
            list: A list of DataCollectionRuleConfig objects.
        """
        return [rconf for rconf in self.object_rule_configs.values() if isinstance(rconf, DataCollectionRuleConfig)]

    def valid_rule_configs(self):
        """
        Returns a dictionary identifying all valid rule configurations for this policy.

        Returns:
            dict: A dictionary mapping string ID values (UUIDs) to dicts containing entries for name, description,
                  and category.
        """
        if self._ruleconfig_presentation is None and self._model_unique_id is not None:
            uri = Policy.urlobject.format(self._cb.credentials.org_key) + \
                f"/{self._model_unique_id}/configs/presentation"
            result = self._cb.get_object(uri)
            self._ruleconfig_presentation = {cfg['id']: cfg for cfg in result.get('configs', [])}
        return {k: {'name': v['name'], 'description': v['description'], 'category': v['presentation']['category']}
                for k, v in self._ruleconfig_presentation.items()}

    @classmethod
    def _create_rule_config(cls, cb, parent, data):
        """
        Creates a PolicyRuleConfig object, or specialized subclass thereof, from a block of data in the policy.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            data (dict): Initial data used to populate the rule configuration.

        Returns:
            PolicyRuleConfig: The new object.
        """
        newclass = SPECIFIC_RULECONFIGS.get(data.get("category", None), PolicyRuleConfig)
        return newclass(cb, parent, data.get("id", None), data, False, True)

    def get_ruleconfig_parameter_schema(self, ruleconfig_id):
        """
        Returns the parameter schema for a specified rule configuration.

        Uses cached rule configuration presentation data if present.

        Args:
            ruleconfig_id (str): The rule configuration ID (UUID).

        Returns:
            dict: The parameter schema for this particular rule configuration (a JSON schema).

        Raises:
            InvalidObjectError: If the rule configuration ID is not valid.
        """
        if self._ruleconfig_presentation is not None:
            block = self._ruleconfig_presentation.get(ruleconfig_id, None)
            if block is None:
                raise InvalidObjectError(f"invalid rule config ID {ruleconfig_id}")
            param_items = block.get("parameters", [])
            # morph the parameter presentation into a parameter schema
            schema = {}
            for item in param_items:
                schema_item = {'default': item['default'], 'description': item['description']}
                for validation in item.get('validations', []):
                    val_type = validation.get('type', None)
                    if val_type == 'enum':
                        schema_item['type'] = 'string'
                        schema_item['enum'] = validation.get('values', [])
                    else:
                        # other item types may be defined later
                        schema_item['type'] = val_type
                if 'type' not in schema_item:  # fallback to string if nothing specified
                    schema_item['type'] = 'string'
                schema[item['name']] = schema_item
            return {'type': 'object', 'properties': schema}
        else:
            return self._cb.get_policy_ruleconfig_parameter_schema(ruleconfig_id)

    def _on_updated_rule(self, rule):
        """
        Called when a rule object is added or updated.

        Args:
            rule (PolicyRule): The rule being updated.
        """
        if rule._parent is not self:
            raise ApiError("internal error: updated rule does not belong to this policy")
        existed = rule.id in self.object_rules
        self._object_rules[rule.id] = rule
        raw_rules = self._info.get("rules", [])
        if existed:
            for index, raw_rule in enumerate(raw_rules):
                if raw_rule['id'] == rule.id:
                    raw_rules[index] = copy.deepcopy(rule._info)
                    break
        else:
            raw_rules.append(copy.deepcopy(rule._info))
        self._info["rules"] = raw_rules

    def _on_deleted_rule(self, rule):
        """
        Called when a rule object is deleted.

        Args:
            rule (PolicyRule): The rule being deleted.
        """
        if rule._parent is not self:
            raise ApiError("internal error: updated rule does not belong to this policy")
        if rule.id in self._object_rules:
            del self._object_rules[rule.id]
        else:
            raise ApiError("internal error: updated rule does not belong to this policy")
        new_raw_rules = [raw_rule for raw_rule in self._info.get("rules", []) if raw_rule['id'] != rule.id]
        self._info["rules"] = new_raw_rules

    def _on_updated_rule_config(self, rule_config):
        """
        Called when a rule configuration object is added or updated.

        Args:
            rule_config (PolicyRuleConfig): The rule configuration being added or updated.
        """
        if rule_config._parent is not self:
            raise ApiError("internal error: updated rule configuration does not belong to this policy")
        if rule_config.id not in self.object_rule_configs:
            raise ApiError(f"internal error: unvalid rule configuration ID {rule_config.id}")
        self._object_rule_configs[rule_config.id] = rule_config
        raw_rule_configs = self._info.get("rule_configs", [])
        location = [index for (index, item) in enumerate(raw_rule_configs) if item['id'] == rule_config.id]
        if location:
            raw_rule_configs[location[0]] = copy.deepcopy(rule_config._info)
            self._info['rule_configs'] = raw_rule_configs

    def _on_deleted_rule_config(self, rule_config):
        """
        Called when a rule configuration object is deleted.

        Args:
            rule_config (PolicyRuleConfig): The rule configuration being deleted.
        """
        if rule_config._parent is not self:
            raise ApiError("internal error: updated rule configuration does not belong to this policy")
        rconfs = self._info.get("rule_configs", [])
        location = [index for (index, item) in enumerate(rconfs) if item['id'] == rule_config.id]
        if location:
            rconfs[location[0]] = copy.deepcopy(rule_config._info)
            self._info['rule_configs'] = rconfs

    def add_rule(self, new_rule):
        """Adds a rule to this Policy.

        Arguments:
            new_rule (dict(str,str)): The new rule to add to this Policy.

        Notes:
            - The new rule must conform to this dictionary format:

                {"action": "ACTION",
                "application": {"type": "TYPE", "value": "VALUE"},
                "operation": "OPERATION",
                "required": "REQUIRED"}

            - The dictionary keys have these possible values:

                "action": ["IGNORE", "ALLOW", "DENY", "TERMINATE_PROCESS",
                "TERMINATE_THREAD", "TERMINATE"]

                "type": ["NAME_PATH", "SIGNED_BY", "REPUTATION"]

                "value": Any string value to match on

                "operation": ["BYPASS_ALL", "INVOKE_SCRIPT", "INVOKE_SYSAPP",
                "POL_INVOKE_NOT_TRUSTED", "INVOKE_CMD_INTERPRETER",
                "RANSOM", "NETWORK", "PROCESS_ISOLATION", "CODE_INJECTION",
                "MEMORY_SCRAPE", "RUN_INMEMORY_CODE", "ESCALATE", "RUN"]

                "required": [True, False]
        """
        new_obj = PolicyRule(self._cb, self, None, new_rule, False, True)
        new_obj.touch()
        new_obj.save()

    def delete_rule(self, rule_id):
        """
        Deletes a rule from this Policy.

        Args:
            rule_id (int): The ID of the rule to be deleted.

        Raises:
            ApiError: If the rule ID does not exist in this policy.
        """
        old_rule = self.object_rules.get(rule_id, None)
        if old_rule:
            old_rule.delete()
        else:
            raise ApiError(f"rule #{rule_id} not found in policy")

    def replace_rule(self, rule_id, new_rule):
        """
        Replaces a rule in this policy.

        Args:
            rule_id (int): The ID of the rule to be replaced.
            new_rule (dict): The data for the new rule.

        Raises:
            ApiError: If the rule ID does not exist in this policy.
        """
        old_rule = self.object_rules.get(rule_id, None)
        if old_rule:
            new_rule_info = copy.deepcopy(new_rule)
            new_rule_info["id"] = rule_id
            saved_rule_info = old_rule._info
            old_rule._info = new_rule_info
            old_rule.touch()
            restore_rule = True
            try:
                old_rule.save()
                restore_rule = False
            finally:
                if restore_rule:
                    old_rule._info = saved_rule_info
                    old_rule._dirty_attributes = {}
        else:
            raise ApiError(f"rule #{rule_id} not found in policy")

    def delete_rule_config(self, rule_config_id):
        """
        Deletes a rule configuration from this Policy.

        Args:
            rule_config_id (str): The ID of the rule configuration to be deleted.

        Raises:
            ApiError: If the rule configuration ID does not exist in this policy.
        """
        old_rule_config = self.object_rule_configs.get(rule_config_id, None)
        if old_rule_config:
            old_rule_config.delete()
        else:
            raise ApiError(f"rule configuration '{rule_config_id}' not found in policy")

    def replace_rule_config(self, rule_config_id, new_rule_config):
        """
        Replaces a rule configuration in this policy.

        Args:
            rule_config_id (str): The ID of the rule configuration to be replaced.
            new_rule_config (dict): The data for the new rule configuration.

        Raises:
            ApiError: If the rule configuration ID does not exist in this policy.
        """
        old_rule_config = self.object_rule_configs.get(rule_config_id, None)
        if old_rule_config:
            new_rule_config_info = copy.deepcopy(new_rule_config)
            new_rule_config_info['id'] = rule_config_id
            saved_rule_config_info = old_rule_config._info
            old_rule_config._info = new_rule_config_info
            old_rule_config.touch(True)
            restore_rule_config = True
            try:
                old_rule_config.save()
                restore_rule_config = False
            finally:
                if restore_rule_config:
                    old_rule_config._info = saved_rule_config_info
                    old_rule_config._dirty_attributes = {}
        else:
            raise ApiError(f"rule configuration '{rule_config_id}' not found in policy")

    def set_data_collection(self, parameter, value):
        """
        Sets a data collection parameter value on any data collection rule configurations in the policy that have it.

        As a safety check, this method also validates that the type of the existing value of that parameter is the
        same as the type of the new value we want to set for that parameter.

        Args:
            parameter (str): The name of the parameter to set.
            value (Any): The value of the parameter to set.

        Raises:
            ApiError: If the parameter setting operation failed.
        """
        rconf_blocks = [block for block in self.rule_configs
                        if block['category'] == 'data_collection' and parameter in block['parameters']]
        if len(rconf_blocks) > 0:
            url = f"/policyservice/v1/orgs/{self._cb.credentials.org_key}/policies/{self.id}" \
                  "/rule_configs/data_collection"
            for rconf_block in rconf_blocks:
                if type(rconf_block['parameters'][parameter]) is type(value):
                    body = {"id": rconf_block['id'], "parameters": {parameter: value}}
                    return_data = self._cb.put_object(url, body)
                    fail_blocks = [block for block in return_data.json()['failed'] if block['id'] == rconf_block['id']]
                    if len(fail_blocks) > 0:
                        raise ApiError(fail_blocks[0]['message'])
                    rconf_block['parameters'][parameter] = value

    def set_xdr_collection(self, flag):
        """
        Sets XDR collection to be enabled or disabled on this policy.

        Args:
            flag (bool): ``True`` to enable XDR data collection, ``False`` to disable it.

        Raises:
            ApiError: If the parameter setting operation failed.
        """
        self.set_data_collection("enable_network_data_collection", flag)

    def set_auth_event_collection(self, flag):
        """
        Sets auth event collection to be enabled or disabled on this policy.

        Args:
            flag (bool): ``True`` to enable auth event data collection, ``False`` to disable it.

        Raises:
            ApiError: If the parameter setting operation failed.
        """
        self.set_data_collection("enable_auth_events", flag)

    def preview_rank_change(self, new_rank):
        """
        Previews a change in the ranking of this policy, and determines how this will affect asset groups.

        Args:
            new_rank (int): The new rank to give this policy.  Ranks are limited to values in the range [1.._N_],
                            where _N_ is the total number of policies in the organization.

        Returns:
            list[DevicePolicyChangePreview]: A list of objects containing data previewing the policy changes.
        """
        return Policy.preview_policy_rank_changes(self._cb, [(self._model_unique_id, new_rank)])

    def preview_add_policy_override(self, devices):
        """
        Previews changes to the effective policies for devices which result from setting this policy override on them.

        Required Permissions:
            org.policies (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            devices (list): The devices which will have their policies overridden. Each entry in this list is either
                an integer device ID or a ``Device`` object.

        Returns:
            list[DevicePolicyChangePreview]: A list of ``DevicePolicyChangePreview`` objects representing the assets
                that change which policy is effective as the result of this operation.
        """
        return Device.preview_add_policy_override_for_devices(self._cb, self._model_unique_id, devices)

    # --- BEGIN policy v1 compatibility methods ---

    @property
    def priorityLevel(self):
        """Returns the priority level of this policy (compatibility method)."""
        return self.priority_level

    @priorityLevel.setter
    def priorityLevel(self, level):
        """Sets the priority level of this policy (compatibility method)."""
        self.priority_level = level

    @property
    def systemPolicy(self):
        """Returns whether or not this is a systsem policy (compatibility method)."""
        return self.is_system

    @systemPolicy.setter
    def systemPolicy(self, flag):
        """Sets whether or not this is a systsem policy (compatibility method)."""
        self.is_system = flag

    @property
    def latestRevision(self):
        """Returns the latest revision of this policy (compatibility method)."""
        return 2

    @property
    def policy(self):
        """Returns the contents of this policy [compatibility method]."""
        rc = {"version": 2, "name": self._info.get("name", None), "description": self._info.get("description", None)}
        if "sensor_settings" in self._info:
            rc["sensorSettings"] = copy.deepcopy(self._info["sensor_settings"])
        av_settings = self._info.get("av_settings", None)
        if av_settings:
            new_av = {}
            subobj = av_settings.get("avira_protection_cloud", None)
            if subobj:
                new_av["apc"] = {"enabled": subobj["enabled"], "maxExeDelay": subobj["max_exe_delay"],
                                 "maxFileSize": subobj["max_file_size"], "riskLevel": subobj["risk_level"]}
            features = []
            subobj = av_settings.get("on_access_scan", None)
            if subobj:
                new_av["onAccessScan"] = {"profile": subobj["mode"]}
                features.append({"enabled": subobj["enabled"], "name": "ONACCESS_SCAN"})
            subobj = av_settings.get("on_demand_scan", None)
            if subobj:
                new_av["onDemandScan"] = {"profile": subobj["profile"], "scanUsb": subobj["scan_usb"],
                                          "scanCdDvd": subobj["scan_cd_dvd"]}
                sched = subobj["schedule"]
                if sched:
                    new_av["onDemandScan"]["schedule"] = {"days": sched.get("days", None),
                                                          "startHour": sched.get("start_hour", None),
                                                          "rangeHours": sched.get("range_hours", None),
                                                          "recoveryScanIfMissed":
                                                              sched.get("recovery_scan_if_missed", None)}
                features.append({"enabled": subobj["enabled"], "name": "ONDEMAND_SCAN"})
            subobj = av_settings.get("signature_update", None)
            if subobj:
                new_av["signatureUpdate"] = \
                    {"schedule": {"intervalHours": subobj["schedule"]["interval_hours"],
                                  "fullIntervalHours": subobj["schedule"]["full_interval_hours"],
                                  "initialRandomDelayHours": subobj["schedule"]["initial_random_delay_hours"]}}
                features.append({"enabled": subobj["enabled"], "name": "SIGNATURE_UPDATE"})
            new_av["features"] = features
            subobj = av_settings.get("update_servers", None)
            if subobj:
                new_av["updateServers"] = {"serversForOffSiteDevices": subobj["servers_for_offsite_devices"],
                                           "servers": [{"server": [entry["server"]], "flags": 0, "regId": None}
                                                       for entry in subobj["servers_for_onsite_devices"]]}
                if subobj["servers_override"]:
                    new_av["updateServers"]["serversOverride"] = subobj["servers_override"]
            rc["avSettings"] = new_av
        if "directory_action_rules" in self._info:
            rc["directoryActionRules"] = [{"actions": {"FILE_UPLOAD": dar["file_upload"],
                                                       "PROTECTION": dar["protection"]}, "path": dar["path"]}
                                          for dar in self._info["directory_action_rules"]]
        if "rules" in self._info:
            rc["rules"] = copy.deepcopy(self._info["rules"])
        return rc

    @policy.setter
    def policy(self, oldpolicy):
        """Sets the contents of this policy from a dict (compatibility method)."""
        newpolicy = copy.deepcopy(self._info)
        newpolicy["org_key"] = self._cb.credentials.org_key  # in case this is a new object
        if "sensorSettings" in oldpolicy:
            newpolicy["sensor_settings"] = copy.deepcopy(oldpolicy["sensorSettings"])
        oldav = oldpolicy.get("avSettings", None)
        if oldav:
            newav = {}
            feature_flags = {}
            if "features" in oldav:
                for d in oldav["features"]:
                    feature_flags[d["name"]] = d["enabled"]
            subobj = oldav.get("apc", None)
            if subobj:
                newav["avira_protection_cloud"] = {"enabled": subobj.get("enabled", False),
                                                   "max_exe_delay": subobj.get("maxExeDelay", 0),
                                                   "max_file_size": subobj.get("maxFileSize", 0),
                                                   "risk_level": subobj.get("riskLevel", 0)}
            subobj = oldav.get("onAccessScan", {})
            if subobj or "ONACCESS_SCAN" in feature_flags:
                newav["on_access_scan"] = {"enabled": feature_flags.get("ONACCESS_SCAN", False),
                                           "mode": subobj.get("profile", "NORMAL")}
            subobj = oldav.get("onDemandScan", {})
            if subobj or "ONDEMAND_SCAN" in feature_flags:
                newav["on_demand_scan"] = {"enabled": feature_flags.get("ONDEMAND_SCAN", False),
                                           "profile": subobj.get("profile", "NORMAL"),
                                           "scan_usb": subobj.get("scanUsb", "AUTOSCAN"),
                                           "scan_cd_dvd": subobj.get("scanCdDvd", "AUTOSCAN")}
                sched = subobj.get("schedule", {})
                if sched:
                    newav["on_demand_scan"]["schedule"] = {"days": sched.get("days", None),
                                                           "start_hour": sched.get("startHour", None),
                                                           "range_hours": sched.get("rangeHours", None),
                                                           "recovery_scan_if_missed":
                                                               sched.get("recoveryScanIfMissed", None)}
            subobj = oldav.get("signatureUpdate", {})
            if subobj or "SIGNATURE_UPDATE" in feature_flags:
                newav["signature_update"] = {"enabled": feature_flags.get("SIGNATURE_UPDATE", False)}
                sched = subobj.get("schedule", {})
                if sched:
                    newav["signature_update"]["schedule"] = {"interval_hours": sched.get("intervalHours", None),
                                                             "full_interval_hours":
                                                                 sched.get("fullIntervalHours", None),
                                                             "initial_random_delay_hours":
                                                                 sched.get("initialRandomDelayHours", None)}
            subobj = oldav.get("updateServers", None)
            if subobj:
                newav["update_servers"] = {"servers_for_offsite_devices": subobj.get("serversForOffSiteDevices", []),
                                           "servers_override": subobj.get("serversOverride", [])}
                if "servers" in subobj:
                    server_lists = [d.get("server", []) for d in subobj["servers"]]
                    servers = [name for server_list in server_lists for name in server_list]
                    newav["update_servers"]["servers_for_onsite_devices"] = \
                        [{"server": name, "preferred": False} for name in servers]
            newpolicy["av_settings"] = newav
        if "directoryActionRules" in oldpolicy:
            newpolicy["directory_action_rules"] = [{"path": dar.get("path", None),
                                                    "file_upload": dar.get("actions", {}).get("FILE_UPLOAD", False),
                                                    "protection": dar.get("actions", {}).get("PROTECTION", False)}
                                                   for dar in oldpolicy["directoryActionRules"]]
        if "rules" in oldpolicy:
            newpolicy["rules"] = copy.deepcopy(oldpolicy["rules"])
        self._info = newpolicy

    # --- END policy v1 compatibility methods ---

    @classmethod
    def create(cls, cb):
        """
        Begins creating a policy by returning a PolicyBuilder.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            PolicyBuilder: The new policy builder object.
        """
        return Policy.PolicyBuilder(cb)

    @classmethod
    def preview_policy_rank_changes(cls, cb, changes_list):
        """
        Previews changes in the ranking of policies, and determines how this will affect asset groups.

        Example::

            >>> cb = CBCloudAPI(profile='sample')
            >>> changes = Policy.preview_policy_rank_changes(cb, [(667251, 1)])
            >>> # also: changes = Policy.preview_policy_rank_changes(cb, [{"id": 667251, "position": 1}])
            >>> len(changes)
            2
            >>> changes[0].current_policy_id
            660578
            >>> changes[0].new_policy_id
            667251

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            changes_list (list): The list of proposed changes in the ranking of policies.  Each change may be in
                the form of a dict, in which case the "id" and "position" members are used to designate the policy ID
                and the new position, or in the form of a list or tuple, in which case the first element specifies
                the policy ID, and the second element specifies the new position.  In all cases, "position" values are
                limited to values in the range [1.._N_], where _N_ is the total number of policies in the organization.

        Returns:
            list[DevicePolicyChangePreview]: A list of objects containing data previewing the policy changes.
        """
        submit_list = []
        for change in changes_list:
            if isinstance(change, dict):
                submit_list.append({"id": change["id"], "position": change["position"]})
            elif isinstance(change, list) or isinstance(change, tuple):
                submit_list.append({"id": change[0], "position": change[1]})
        ret = cb.post_object(f"/policy-assignment/v1/orgs/{cb.credentials.org_key}/policies/preview",
                             {"policies": submit_list})
        return [DevicePolicyChangePreview(cb, p) for p in ret.json()["preview"]]


class PolicyRule(MutableBaseModel):
    """
    Represents a rule in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule to the policy. This requires the org.policies(UPDATE) permission.

    To update a PolicyRule, change the values of its property fields, then call the rule's save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing PolicyRule, call its delete() method. This requires the org.policies(UPDATE) permission.

    """
    primary_key = "id"
    swagger_meta_file = "platform/models/policy_rule.yaml"
    VALID_ACTIONS = ["IGNORE", "ALLOW", "TERMINATE_PROCESS", "TERMINATE_THREAD", "TERMINATE", "DENY"]
    VALID_APP_KEYS = {"type", "value"}
    VALID_APP_TYPES = ["NAME_PATH", "SIGNED_BY", "REPUTATION"]
    VALID_REPUTATIONS = ["ADAPTIVE_WHITE_LIST", "ADWARE", "COMMON_WHITE_LIST", "COMPANY_BLACK_LIST",
                         "COMPANY_WHITE_LIST", "HEURISTIC", "IGNORE", "KNOWN_MALWARE", "LOCAL_WHITE", "NOT_LISTED",
                         "PUP", "RESOLVING", "SUSPECT_MALWARE", "TRUSTED_WHITE_LIST"]
    VALID_OPERATIONS = ["BYPASS_ALL", "BYPASS_API", "INVOKE_SCRIPT", "INVOKE_SYSAPP", "POL_INVOKE_NOT_TRUSTED",
                        "INVOKE_CMD_INTERPRETER", "RANSOM", "NETWORK", "PROCESS_ISOLATION", "CODE_INJECTION",
                        "MEMORY_SCRAPE", "RUN_INMEMORY_CODE", "ESCALATE", "RUN"]

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the PolicyRule object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule.
            model_unique_id (int): ID of the rule.
            initial_data (dict): Initial data used to populate the rule.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(PolicyRule, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                         force_init=force_init, full_doc=full_doc)
        self._parent = parent
        if model_unique_id is None:
            self.touch(True)

    def _refresh(self):
        """
        Refreshes the rule object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.
        """
        if self._model_unique_id is not None:
            rc = self._parent._refresh()
            if rc:
                newobj = self._parent.object_rules.get(self.id, None)
                if newobj:
                    self._info = newobj._info
            return rc

    def _update_object(self):
        """
        Updates the rule object on the policy on the server.

        Required Permissions:
            org.policies(UPDATE)
        """
        if "id" in self._dirty_attributes.keys() or self._model_unique_id is None:
            new_object_info = copy.deepcopy(self._info)
            if "id" in new_object_info:
                del new_object_info["id"]
            url = self._parent._build_api_request_uri() + "/rules"
            ret = self._cb.post_object(url, new_object_info)
        else:
            url = self._parent._build_api_request_uri() + f"/rules/{self.id}"
            ret = self._cb.put_object(url, self._info)
        if ret.status_code not in range(200, 300):
            try:
                result = json.loads(ret.text)[0]
            except Exception:
                result = ret.text
            raise ServerError(ret.status_code, "Unable to update policy rule", result=result, uri=url)
        self._info = json.loads(ret.text)
        self._full_init = True
        self._parent._on_updated_rule(self)

    def _delete_object(self):
        """
        Deletes this rule object from the policy on the server.

        Required Permissions:
            org.policies(UPDATE)
        """
        if self._model_unique_id is None:
            raise ApiError("new rule cannot be deleted")
        self._cb.delete_object(self._parent._build_api_request_uri() + f"/rules/{self.id}")
        self._parent._on_deleted_rule(self)
        self._parent = None

    @property
    def is_deleted(self):
        """Returns True if this rule object has been deleted."""
        return self._parent is None

    def validate(self):
        """
        Validates this rule against its constraints.

        Raises:
            InvalidObjectError: If the rule object is not valid.
        """
        super(PolicyRule, self).validate()
        if not isinstance(self._info["required"], bool):
            raise InvalidObjectError("'required' field not valid type")
        if self._info["action"] not in PolicyRule.VALID_ACTIONS:
            raise InvalidObjectError("'action' field value not valid")
        if not isinstance(self._info["application"], dict) \
           or set(self._info["application"].keys()) != PolicyRule.VALID_APP_KEYS:
            raise InvalidObjectError("'application' field not valid type/structure")
        if self._info["application"]["type"] not in PolicyRule.VALID_APP_TYPES:
            raise InvalidObjectError("'application' 'type' value not valid")
        if not isinstance(self._info["application"]["value"], str):
            raise InvalidObjectError("'application' 'value' not valid type")
        if self._info["application"]["type"] == "REPUTATION" \
           and self._info["application"]["value"] not in PolicyRule.VALID_REPUTATIONS:
            raise InvalidObjectError("'application' 'value' not valid value for type REPUTATION")
        if self._info["operation"] not in PolicyRule.VALID_OPERATIONS:
            raise InvalidObjectError("'operation' field value not valid")
        return True


"""Query Class"""


class PolicyQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    """Query for retrieving policies (summary info only)."""
    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(PolicyQuery, self).__init__(None)
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        self._total_results = 0
        self._policy_ids = []
        self._system = False
        self._system_set = False
        self._names = []
        self._descriptions = []
        self._priorities = []

    def add_policy_ids(self, ids):
        """
        Add policy ID(s) to the list to search for.

        Args:
            ids (int/list): Either a single policy ID or a list of IDs.

        Returns:
            PolicyQuery: This object instance.

        Raises:
            ApiError: If not supplied with an int or a list of ints.
        """
        if isinstance(ids, int):
            self._policy_ids.append(ids)
        elif hasattr(ids, '__iter__'):
            if all([isinstance(v, int) for v in ids]):
                self._policy_ids.extend(ids)
            else:
                raise ApiError("non-integer items in iterable")
        else:
            raise ApiError("supplied item is of invalid type")
        return self

    def set_system(self, system):
        """
        Set to look for either system or non-system policies.

        Args:
            system (bool): True to look for system policies, False to look for non-system policies.

        Returns:
            PolicyQuery: This object instance.

        Raises:
            ApiError: If not supplied with a Boolean.
        """
        if isinstance(system, bool):
            self._system = system
            self._system_set = True
        else:
            raise ApiError("system flag is of invalid type")
        return self

    def add_names(self, names):
        """
        Add policy name(s) to the list to search for.

        Args:
            names (str/list): Either a single policy name or a list of names.

        Returns:
            PolicyQuery: This object instance.

        Raises:
            ApiError: If not supplied with a string or a list of strings.
        """
        if isinstance(names, str):
            self._names.append(names)
        elif hasattr(names, '__iter__'):
            if all([isinstance(v, str) for v in names]):
                self._names.extend(names)
            else:
                raise ApiError("non-string items in iterable")
        else:
            raise ApiError("supplied name is of invalid type")
        return self

    def add_descriptions(self, descrs):
        """
        Add policy description(s) to the list to search for.

        Args:
            descrs (str/list): Either a single policy description or a list of descriptions.

        Returns:
            PolicyQuery: This object instance.

        Raises:
            ApiError: If not supplied with a string or a list of strings.
        """
        if isinstance(descrs, str):
            self._descriptions.append(descrs)
        elif hasattr(descrs, '__iter__'):
            if all([isinstance(v, str) for v in descrs]):
                self._descriptions.extend(descrs)
            else:
                raise ApiError("non-string items in iterable")
        else:
            raise ApiError("supplied description is of invalid type")
        return self

    def add_priorities(self, priorities):
        """
        Add policy priority/priorities to the list to search for.

        Args:
            priorities (str/list): Either a single policy priority value or a list of priority values.

        Returns:
            PolicyQuery: This object instance.

        Raises:
            ApiError: If not supplied with a string priority value or a list of string priority values.
        """
        if isinstance(priorities, str):
            if priorities in Policy.VALID_PRIORITIES:
                self._priorities.append(priorities)
            else:
                raise ApiError(f"invalid priority: {priorities}")
        elif hasattr(priorities, '__iter__'):
            if all([v in Policy.VALID_PRIORITIES for v in priorities]):
                self._priorities.extend(priorities)
            else:
                raise ApiError("invalid priority items in iterable")
        else:
            raise ApiError("supplied priority is of invalid type")
        return self

    def _include_policy(self, policydata):
        """
        Predicate to determine if a policy's data should be included in the query result.

        Args:
            policydata (dict): Raw policy data.

        Returns:
            bool: True if this data should be included, False if not.
        """
        if self._policy_ids and policydata['id'] not in self._policy_ids:
            return False
        if self._system_set and policydata['is_system'] != self._system:
            return False
        if self._names and all([n not in policydata['name'] for n in self._names]):
            return False
        if self._descriptions and all([n not in policydata['description'] for n in self._descriptions]):
            return False
        if self._priorities and policydata['priority_level'] not in self._priorities:
            return False
        return True

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Required Permissions:
            org.policies(READ)

        Returns:
            list[dict]: The raw results of the query, as a list of dicts.
        """
        url = "/policyservice/v1/orgs/{0}/policies/summary".format(self._cb.credentials.org_key)
        rawdata = self._cb.get_object(url)
        return rawdata.get('policies', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Required Permissions:
            org.policies(READ)

        Returns:
            int: The number of results from the run of this query.
        """
        if not self._count_valid:
            return_data = self._execute()
            filtered_data = [item for item in return_data if self._include_policy(item)]
            self._total_results = len(filtered_data)
            self._count_valid = True
        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Required Permissions:
            org.policies(READ)

        Args:
            from_row (int): Unused in this implementation, always 0.
            max_rows (int): Unused in this implementation, always -1.

        Returns:
            Iterable: The iterated query.
        """
        return_data = self._execute()
        filtered_data = [item for item in return_data if self._include_policy(item)]
        self._total_results = len(filtered_data)
        self._count_valid = True
        for item in filtered_data:
            yield Policy(self._cb, item['id'], item, False, False)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Required Permissions:
            org.policies(READ)

        Args:
            context (object): Not used; always None.

        Returns:
            list[Policy]: Result of the async query, as a list of Policy objects.
        """
        return_data = self._execute()
        output = [Policy(self._cb, item['id'], item, False, False) for item in return_data
                  if self._include_policy(item)]
        self._total_results = len(output)
        self._count_valid = True
        return output
