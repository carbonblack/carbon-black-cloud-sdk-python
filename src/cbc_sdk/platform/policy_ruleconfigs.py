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

"""Policy rule configuration implementation as part of Platform API"""

import copy
import jsonschema
from cbc_sdk.base import MutableBaseModel
from cbc_sdk.errors import ApiError, InvalidObjectError


class PolicyRuleConfig(MutableBaseModel):
    """
    Represents a rule configuration in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule configuration to the policy. This requires the org.policies(UPDATE) permission.

    To update a PolicyRuleConfig, change the values of its property fields, then call its save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing PolicyRuleConfig, call its delete() method. This requires the org.policies(DELETE) permission.

    """
    urlobject = "/policyservice/v1/orgs/{0}/policies"
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}/rule_configs"
    primary_key = "id"
    swagger_meta_file = "platform/models/policy_ruleconfig.yaml"

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the PolicyRuleConfig object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            model_unique_id (str): ID of the rule configuration.
            initial_data (dict): Initial data used to populate the rule configuration.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(PolicyRuleConfig, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                               force_init=force_init, full_doc=full_doc)
        self._parent = parent
        self._params_changed = False
        if model_unique_id is None:
            self.touch(True)

    def _refresh(self):
        """
        Refreshes the rule configuration object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.
        """
        rc = False
        if self._model_unique_id is not None:
            rc = self._parent._refresh()
            if rc:
                newobj = self._parent.object_rule_configs.get(self.id, None)
                if newobj:
                    self._info = newobj._info
                    self._params_changed = False
        return rc

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        raise NotImplementedError("update not defined for this category of rule configuration")

    def _update_object(self):
        """
        Updates the rule configuration object on the policy on the server.

        Required Permissions:
            org.policies(UPDATE)
        """
        self._update_ruleconfig()
        self._full_init = True
        self._params_changed = False
        self._parent._on_updated_rule_config(self)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        raise NotImplementedError("delete not defined for this category of rule configuration")

    def _delete_object(self):
        """
        Deletes this rule configuration object from the policy on the server.

        Required Permissions:
            org.policies(DELETE)
        """
        self._delete_ruleconfig()
        self._parent._on_deleted_rule_config(self)

    def _mark_changed(self, flag=True):
        """
        Marks this object as changed.

        Args:
            flag (bool): Changed flag, default is True.
        """
        self._params_changed = flag

    def is_dirty(self):
        """
        Returns whether or not any fields of this object have been changed.

        Returns:
            bool: True if any fields of this object have been changed, False if not.
        """
        return self._params_changed or super(PolicyRuleConfig, self).is_dirty()

    @property
    def parameter_names(self):
        """
        Returns a list of parameter names in this rule configuration.

        Returns:
            list[str]: A list of parameter names in this rule configuration.
        """
        if 'parameters' not in self._info:
            self.refresh()
        params = self._info['parameters']
        return list(params.keys())

    def get_parameter(self, name, default_value=None):
        """
        Returns a parameter value from the rule configuration.

        Args:
            name (str): The parameter name.
            default_value (Any): The default value to return if there's no parameter by that name. Default is None.

        Returns:
            Any: The parameter value, or None if there is no value.
        """
        if 'parameters' not in self._info:
            self.refresh()
        params = self._info['parameters']
        return params.get(name, default_value)

    def set_parameter(self, name, value):
        """
        Sets a parameter value into the rule configuration.

        Args:
            name (str): The parameter name.
            value (Any): The new value to be set.
        """
        if 'parameters' not in self._info:
            self.refresh()
        params = self._info['parameters']
        old_value = params.get(name, None)
        if old_value != value:
            if 'parameters' not in self._dirty_attributes:
                self._dirty_attributes['parameters'] = params
                new_params = copy.deepcopy(params)
            else:
                new_params = params
            new_params[name] = value
            self._info['parameters'] = new_params

    def validate(self):
        """
        Validates this rule configuration against its constraints.

        Raises:
            InvalidObjectError: If the rule object is not valid.
        """
        super(PolicyRuleConfig, self).validate()

        if self._parent is not None:
            # set high-level fields
            valid_configs = self._parent.valid_rule_configs()
            data = valid_configs.get(self._model_unique_id, {})
            self._info.update(data)
            if 'inherited_from' not in self._info:
                self._info['inherited_from'] = 'psc:region'

        # validate parameters
        if self._parent is None:
            parameter_validations = self._cb.get_policy_ruleconfig_parameter_schema(self._model_unique_id)
        else:
            parameter_validations = self._parent.get_ruleconfig_parameter_schema(self._model_unique_id)
        my_parameters = self._info.get('parameters', {})
        try:
            jsonschema.validate(instance=my_parameters, schema=parameter_validations)
        except jsonschema.ValidationError as e:
            raise InvalidObjectError(f"parameter error: {e.message}", e)
        except jsonschema.exceptions.SchemaError as e:
            raise ApiError(f"internal error: {e.message}", e)
        self._info['parameters'] = my_parameters


class CorePreventionRuleConfig(PolicyRuleConfig):
    """
    Represents a core prevention rule configuration in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule configuration to the policy. This requires the org.policies(UPDATE) permission.

    To update a CorePreventionRuleConfig, change the values of its property fields, then call its save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing CorePreventionRuleConfig, call its delete() method. This requires the org.policies(DELETE)
    permission.

    """
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}/rule_configs/core_prevention"
    swagger_meta_file = "platform/models/policy_ruleconfig.yaml"

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the CorePreventionRuleConfig object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            model_unique_id (str): ID of the rule configuration.
            initial_data (dict): Initial data used to populate the rule configuration.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(CorePreventionRuleConfig, self).__init__(cb, parent, model_unique_id, initial_data, force_init, full_doc)

    def _refresh(self):
        """
        Refreshes the rule configuration object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.

        Raises:
            InvalidObjectError: If the object is unparented or its ID is invalid.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        return_data = self._cb.get_object(url)
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid core prevention ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        body = {"id": self.id, "parameters": self.parameters}
        if "exclusions" in self._info:
            body["exclusions"] = self.exclusions
        self._cb.put_object(url, [body])

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id) + f"/{self.id}"
        self._cb.delete_object(url)
        self._info["parameters"] = copy.deepcopy({"WindowsAssignmentMode": "BLOCK"})  # mirror server side

    def get_assignment_mode(self):
        """
        Returns the assignment mode of this core prevention rule configuration.

        Returns:
            str: The assignment mode, either "REPORT" or "BLOCK".
        """
        return self.get_parameter("WindowsAssignmentMode")

    def set_assignment_mode(self, mode):
        """
        Sets the assignment mode of this core prevention rule configuration.

        Args:
            mode (str): The new mode to set, either "REPORT" or "BLOCK". The default is "BLOCK".
        """
        if mode not in ("REPORT", "BLOCK"):
            raise ApiError(f"invalid assignment mode: {mode}")
        self.set_parameter("WindowsAssignmentMode", mode)

    def replace_exclusions(self, exclusions):
        """
        Replaces all the exclusions for a bypasss rule configuration

        Args:
           exclusions(dict): The entire exclusion set to be replaced
        """
        self._mark_changed(True)
        self._info['exclusions'] = exclusions


class HostBasedFirewallRuleConfig(PolicyRuleConfig):
    """Represents a host-based firewall rule configuration in the policy."""
    urlobject = "/policyservice/v1/orgs/{0}/policies"
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}/rule_configs/host_based_firewall"
    swagger_meta_file = "platform/models/policy_ruleconfig.yaml"

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the HostBasedFirewallRuleConfig object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            model_unique_id (str): ID of the rule configuration.
            initial_data (dict): Initial data used to populate the rule configuration.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(HostBasedFirewallRuleConfig, self).__init__(cb, parent, model_unique_id, initial_data, force_init,
                                                          full_doc)
        self._rule_groups = []
        self._rule_groups_loaded = False

    class FirewallRuleGroup(MutableBaseModel):
        """Represents a group of related firewall rules."""
        swagger_meta_file = "platform/models/firewall_rule_group.yaml"

        def __init__(self, cb, parent, initial_data):
            """
            Initialize the FirewallRuleGroup object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the firewall rule group.
                parent (HostBasedFirewallRuleConfig): The parent rule configuration.
            """
            super(HostBasedFirewallRuleConfig.FirewallRuleGroup, self).__init__(cb, None, initial_data, False, True)
            self._parent = parent
            self._rules = [HostBasedFirewallRuleConfig.FirewallRule(cb, parent, d)
                           for d in initial_data.get("rules", [])]

        def _set(self, attrname, new_value):
            """
            Sets the value of an attribute on the object.

            Args:
                attrname (str): Name of the attribute.
                new_value (Any): Value of the attribute.
            """
            pristine = (attrname not in self._dirty_attributes)
            super(HostBasedFirewallRuleConfig.FirewallRuleGroup, self)._set(attrname, new_value)
            if self._parent and pristine and attrname in self._dirty_attributes:
                self._parent._mark_changed()

        @property
        def rules_(self):
            """
            Returns a list of the firewall rules within this rule group.

            Returns:
                list(HostBasedFirewallRuleConfig.FirewallRule): List of contained firewall rules.
            """
            return self._rules

        def append_rule(self, name, action, direction, protocol, remote_ip, **kwargs):
            """
            Creates a new FirewallRule object and appends it to this rule group.

            Args:
                name (str): The name for the new rule.
                action (str): The action to be taken by this rule. Valid values are "ALLOW," "BLOCK," and "BLOCK_ALERT."
                direction (str): The traffic direction this rule matches. Valid values are "IN," "OUT," and "BOTH."
                protocol (str): The network protocol this rule matches. Valid values are "TCP" and "UDP."
                remote_ip (str): The remote IP address this rule matches.
                kwargs (dict): Additional parameters which may be added to the new rule.

            Returns:
                FirewallRule: The new rule object.
            """
            if action not in ("ALLOW", "BLOCK", "BLOCK_ALERT"):
                raise ApiError(f"invalid rule action: {action}")
            if direction not in ("IN", "OUT", "BOTH"):
                raise ApiError(f"invalid rule direction: {direction}")
            if protocol not in ("TCP", "UDP"):
                raise ApiError(f"invalid rule protocol: {protocol}")
            # specify defaults for optional params, overlay kwargs, then add in the required params
            params = {"application_path": "*", "enabled": True, "local_ip_address": "*", "local_port_ranges": "*",
                      "remote_port_ranges": "*", "test_mode": False}
            specified_params = {k: v for k, v in kwargs.items() if k in params.keys()}
            params.update(specified_params)
            params.update({"action": action, "direction": direction, "name": name, "protocol": protocol,
                           "remote_ip_address": remote_ip})
            rule = HostBasedFirewallRuleConfig.FirewallRule(self._cb, self._parent, params)
            self._rules.append(rule)
            self._info['rules'].append(rule._info)
            if self._parent:
                self._parent._mark_changed()
            return rule

        def remove(self):
            """Removes this rule group from the rule configuration."""
            if self._parent:
                try:
                    location = self._parent.rule_groups.index(self)
                    del self._parent._info["parameters"]["rule_groups"][location]
                    self._parent._mark_changed()
                    self._parent = None
                except ValueError:
                    pass

    class FirewallRule(MutableBaseModel):
        """Represents a single firewall rule."""
        swagger_meta_file = "platform/models/firewall_rule.yaml"

        def __init__(self, cb, parent, initial_data):
            """
            Initialize the FirewallRule object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the firewall rule.
                parent (HostBasedFirewallRuleConfig): The parent rule configuration.
            """
            super(HostBasedFirewallRuleConfig.FirewallRule, self).__init__(cb, None, initial_data, False, True)
            self._parent = parent

        def _set(self, attrname, new_value):
            """
            Sets the value of an attribute on the object.

            Args:
                attrname (str): Name of the attribute.
                new_value (Any): Value of the attribute.
            """
            pristine = (attrname not in self._dirty_attributes)
            super(HostBasedFirewallRuleConfig.FirewallRule, self)._set(attrname, new_value)
            if self._parent and pristine and attrname in self._dirty_attributes:
                self._parent._mark_changed()

        def remove(self):
            """Removes this rule from the rule group that contains it."""
            if self._parent:
                group_list = [group for group in self._parent.rule_groups if self in group._rules]
                if group_list:
                    location = group_list[0]._rules.index(self)
                    group_list[0]._rules.remove(self)
                    del group_list[0]._info['rules'][location]
                    self._parent._mark_changed()
                    self._parent = None

    def _refresh(self):
        """
        Refreshes the rule configuration object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.

        Raises:
            InvalidObjectError: If the object is unparented or its ID is invalid.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        return_data = self._cb.get_object(url)
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._rule_groups = []
            self._rule_groups_loaded = False
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid host-based firewall ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        put_data = {"id": self.id, "parameters": {"enable_host_based_firewall": self.enabled,
                                                  "default_rule": self.get_parameter('default_rule'),
                                                  "rule_groups": self.get_parameter('rule_groups')}}
        resp = self._cb.put_object(url, [put_data])
        result = resp.json()
        success = [d for d in result.get("successful", []) if d.get("id", None) == self.id]
        if not success:
            raise ApiError("update of host-based firewall failed")
        self._info = success[0]
        self._rule_groups = []
        self._rule_groups_loaded = False
        self._mark_changed(False)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        my_id = self.id
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id) + f"/{my_id}"
        self._cb.delete_object(url)
        self._info = {"id": my_id}
        self._full_init = False  # forcing _refresh() next time we read an attribute
        self._rule_groups = []
        self._rule_groups_loaded = False
        self._mark_changed(False)

    @property
    def enabled(self):
        """
        Returns whether or not the host-based firewall is enabled.

        Returns:
            bool: True if the host-based firewall is enabled, False if not.
        """
        return self.get_parameter('enable_host_based_firewall')

    def set_enabled(self, flag):
        """
        Sets whether or not the host-based firewall is enabled.

        Args:
            flag (bool): True if the host-based firewall should be enabled, False if not.
        """
        self.set_parameter('enable_host_based_firewall', flag)

    @property
    def default_action(self):
        """
        Returns the default action of this rule configuration.

        Returns:
            str: The default action of this rule configuration, either "ALLOW" or "BLOCK."
        """
        default_rule = self.get_parameter('default_rule')
        return default_rule.get("action", "ALLOW")

    def set_default_action(self, action):
        """
        Sets the default action of this rule configuration.

        Args:
            action (str): The new default action of this rule configuration. Valid values are "ALLOW" and "BLOCK."
        """
        if action not in ("ALLOW", "BLOCK"):
            raise ApiError(f"invalid default action: {action}")
        default_rule = self.get_parameter('default_rule')
        default_rule['action'] = action
        self.set_parameter("default_rule", default_rule)

    @property
    def rule_groups(self):
        """
        Returns the list of rule groups in this rule configuration.

        Returns:
            list[FirewallRuleGroup]: The list of rule groups.
        """
        if not self._rule_groups_loaded:
            self._rule_groups = [HostBasedFirewallRuleConfig.FirewallRuleGroup(self._cb, self, d)
                                 for d in self.get_parameter("rule_groups", [])]
            self._rule_groups_loaded = True
        return self._rule_groups

    def append_rule_group(self, name, description):
        """
        Creates a new FirewallRuleGroup object and appends it to the list of rule groups in the rule configuration.

        Args:
            name (str): The name of the new rule group.
            description (str): The description of the new rule group.

        Returns:
            FirewallRuleGroup: The newly added rule group.
        """
        rule_group = HostBasedFirewallRuleConfig.FirewallRuleGroup(self._cb, self,
                                                                   {"name": name, "description": description,
                                                                    "rules": []})
        self.rule_groups.append(rule_group)
        if 'rule_groups' in self._info['parameters']:
            self._info['parameters']['rule_groups'].append(rule_group._info)
        else:
            self._info['parameters']['rule_groups'] = [rule_group._info]
        self._mark_changed()
        return rule_group

    def copy_rules(self, *args):
        """
        Copies the parameters for host-based firewall rule configurations to another policy or policies.

        Required Permissions:
            org.firewall.rules(UPDATE)

        Args:
            args (list[Any]): References to policies to copy to. May be Policy objects, integers, or
                              string representations of integers.

        Returns:
            dict: Result structure from copy operation.

        Raises:
            ApiError: If the parameters could not be converted to policy IDs.
        """
        from cbc_sdk.platform.policies import Policy
        target_ids = []
        for arg in args:
            if isinstance(arg, Policy):
                target_ids.append(arg.id)
            elif isinstance(arg, int):
                target_ids.append(arg)
            else:
                try:
                    target_ids.append(int(str(arg)))
                except ValueError:
                    raise ApiError(f"invalid policy ID or reference: {arg}")
        if not target_ids:
            raise ApiError("at least one policy ID or reference must be specified")
        url = self.urlobject.format(self._cb.credentials.org_key) + "/rule_configs/host_based_firewall/_copy"
        body = {"target_policy_ids": target_ids, "parameters": {"rule_groups": self.get_parameter("rule_groups", [])}}
        result = self._cb.post_object(url, body)
        return result.json()

    def export_rules(self, format="json"):
        """
        Exports the rules from this host-based firewall rule configuration.

        Required Permissions:
            org.firewall.rules(READ)

        Args:
            format (str): The format to return the rule data in. Valid values are "csv" and "json" (the default).

        Returns:
            str: The exported rule configuration data.
        """
        if format not in ("csv", "json"):
            raise ApiError(f"Invalid format: {format}")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)\
            + "/rules/_export"
        if format == "json":
            return self._cb.get_object(url, {"format": format})
        else:
            return self._cb.get_raw_data(url, {"format": format})


class DataCollectionRuleConfig(PolicyRuleConfig):
    """
    Represents a data collection rule configuration in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule configuration to the policy. This requires the org.policies(UPDATE) permission.

    To update a DataCollectionRuleConfig, change the values of its property fields, then call its save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing DataCollectionRuleConfig, call its delete() method. This requires the org.policies(DELETE)
    permission.
    """
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}/rule_configs/data_collection"
    swagger_meta_file = "platform/models/policy_ruleconfig.yaml"

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the DataCollectionRuleConfig object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            model_unique_id (str): ID of the rule configuration.
            initial_data (dict): Initial data used to populate the rule configuration.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(DataCollectionRuleConfig, self).__init__(cb, parent, model_unique_id, initial_data, force_init, full_doc)

    def _refresh(self):
        """
        Refreshes the rule configuration object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.

        Raises:
            InvalidObjectError: If the object is unparented or its ID is invalid.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        return_data = self._cb.get_object(url)
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid data collection ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        body = [{"id": self.id, "parameters": self.parameters}]
        self._cb.put_object(url, body)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id) + f"/{self.id}"
        self._cb.delete_object(url)


class BypassRuleConfig(PolicyRuleConfig):
    """
    Represents a bypass rule configuration in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule configuration to the policy. This requires the org.policies(UPDATE) permission.

    To update a BypassRuleConfig, change the values of its property fields, then call its save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing BypassRuleConfig, call its delete() method. This requires the org.policies(DELETE)
    permission.
    """
    urlobject_single = "/policyservice/v1/orgs/{0}/policies/{1}/rule_configs/bypass"
    swagger_meta_file = "platform/models/policy_ruleconfig.yaml"

    def __init__(self, cb, parent, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the BypassRuleConfig object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            parent (Policy): The "parent" policy of this rule configuration.
            model_unique_id (str): ID of the rule configuration.
            initial_data (dict): Initial data used to populate the rule configuration.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(BypassRuleConfig, self).__init__(cb, parent, model_unique_id, initial_data, force_init, full_doc)

    def _refresh(self):
        """
        Refreshes the rule configuration object from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if the refresh was successful.

        Raises:
            InvalidObjectError: If the object is unparented or its ID is invalid.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        return_data = self._cb.get_object(url)
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid data collection ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        body = {"id": self.id}
        if "exclusions" in self._info:
            body["exclusions"] = self.exclusions

        self._cb.put_object(url, body)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._parent._model_unique_id)
        self._cb.delete_object(url)

    def replace_exclusions(self, exclusions):
        """
        Replaces all the exclusions for a bypasss rule configuration

        Args:
           exclusions(dict): The entire exclusion set to be replaced
        """
        self._mark_changed(True)
        self._info['exclusions'] = exclusions

    @property
    def parameter_names(self):
        """Not Supported"""
        raise Exception("Not Suppported")

    def get_parameter(self, name, default_value=None):
        """Not Supported"""
        raise Exception("Not Suppported")

    def set_parameter(self, name, value):
        """Not Supported"""
        raise Exception("Not Suppported")
