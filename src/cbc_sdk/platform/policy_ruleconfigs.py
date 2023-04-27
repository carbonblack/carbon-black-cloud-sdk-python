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

    def _base_url(self):
        """
        Calculates the base URL for these particular rule configs, including the org key and the parent policy ID.

        Returns:
            str: The base URL for these particular rule configs.

        Raises:
            InvalidObjectError: If the rule config object is unparented.
        """
        if self._parent is None:
            raise InvalidObjectError("no parent for rule config")
        return PolicyRuleConfig.urlobject.format(self._cb.credentials.org_key) \
            + f"/{self._parent._model_unique_id}/rule_configs"

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

    def get_parameter(self, name):
        """
        Returns a parameter value from the rule configuration.

        Args:
            name (str): The parameter name.

        Returns:
            Any: The parameter value, or None if there is no value.
        """
        if 'parameters' not in self._info:
            self.refresh()
        params = self._info['parameters']
        return params.get(name, None)

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

    def _base_url(self):
        """
        Calculates the base URL for these particular rule configs, including the org key and the parent policy ID.

        Returns:
            str: The base URL for these particular rule configs.

        Raises:
            InvalidObjectError: If the rule config object is unparented.
        """
        return super(CorePreventionRuleConfig, self)._base_url() + "/core_prevention"

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
        return_data = self._cb.get_object(self._base_url())
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid core prevention ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        body = [{"id": self.id, "parameters": self.parameters}]
        self._cb.put_object(self._base_url(), body)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        self._cb.delete_object(self._base_url() + f"/{self.id}")
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


class HostBasedFirewallRuleConfig(PolicyRuleConfig):
    """Represents a host-based firewall rule configuration in the policy."""
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
        super(HostBasedFirewallRuleConfig, self).__init__(cb, parent, model_unique_id, initial_data, force_init,
                                                          full_doc)
        self._rule_groups = []
        self._rule_groups_valid = False

    class FirewallRuleGroup(MutableBaseModel):
        """Represents a group of related firewall rules."""
        swagger_meta_file = "platform/models/firewall_rule_group.yaml"

        def __init__(self, cb, initial_data):
            """
            Initialize the FirewallRuleGroup object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the firewall rule group.
            """
            super(HostBasedFirewallRuleConfig.FirewallRuleGroup, self).__init__(cb, None, initial_data, False, True)
            self._parent = None
            self._rules = [HostBasedFirewallRuleConfig.FirewallRule(cb, d)
                           for d in initial_data.get("rules", [])]

        def _init_parent(self, parent):
            """
            Initialize the parent of this group and its rules.

            Args:
                parent (HostBasedFirewallRuleConfig): The parent to be set.
            """
            self._parent = parent
            for rule in self._rules:
                rule._parent = parent

        def _field_updated(self, attrname):
            """Method called whenever a field is updated."""
            if self._parent:
                self._parent._mark_changed()

        def _flatten(self):
            """
            Turns this rule group into a dict for transferral to the server.

            Returns:
                dict: The information defining the rule group and its constituent rules.
            """
            rc = copy.deepcopy(self._info)
            rc['rules'] = [rule._flatten() for rule in self._rules]
            return rc

        @property
        def rules_(self):
            """
            Returns a list of the firewall rules within this rule group.

            Returns:
                list(HostBasedFirewallRuleConfig.FirewallRule): List of contained firewall rules.
            """
            return self._rules

        def append_rule(self, rule):
            """
            Appends a new rule to this rule group.

            Args:
                rule (HostBasedFirewallRuleConfig.FirewallRule): The new rule.
            """
            rule._parent = self._parent
            self._rules.append(rule)
            if self._parent:
                self._parent._mark_changed()

        def remove(self):
            """Removes this rule group from the rule configuration."""
            if self._parent and self in self._parent.rule_groups:
                self._parent.rule_groups.remove(self)
                self._parent._mark_changed()
                self._parent = None

    class FirewallRule(MutableBaseModel):
        """Represents a single firewall rule."""
        swagger_meta_file = "platform/models/firewall_rule.yaml"

        def __init__(self, cb, initial_data):
            """
            Initialize the FirewallRule object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                initial_data (dict): Initial data used to populate the firewall rule.
            """
            super(HostBasedFirewallRuleConfig.FirewallRule, self).__init__(cb, None, initial_data, False, True)
            self._parent = None

        def _field_updated(self, attrname):
            """Method called whenever a field is updated."""
            if self._parent:
                self._parent._mark_changed()

        def _flatten(self):
            """
            Turns this rule into a dict for transferral to the server.

            Returns:
                dict: The information defining the rule.
            """
            return copy.deepcopy(self._info)

        def remove(self):
            """Removes this rule from the rule group that contains it."""
            if self._parent:
                group_list = [group for group in self._parent.rule_groups if self in group._rules]
                if group_list:
                    group_list[0]._rules.remove(self)
                    self._parent._mark_changed()
                    self._parent = None

    def _base_url(self):
        """
        Calculates the base URL for these particular rule configs, including the org key and the parent policy ID.

        Returns:
            str: The base URL for these particular rule configs.

        Raises:
            InvalidObjectError: If the rule config object is unparented.
        """
        return super(HostBasedFirewallRuleConfig, self)._base_url() + "/host_based_firewall"

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
        return_data = self._cb.get_object(self._base_url())
        ruleconfig_data = [d for d in return_data.get("results", []) if d.get("id", "") == self._model_unique_id]
        if ruleconfig_data:
            self._info = ruleconfig_data[0]
            self._rule_groups = []
            self._rule_groups_valid = False
            self._mark_changed(False)
        else:
            raise InvalidObjectError(f"invalid host-based firewall ID: {self._model_unique_id}")
        return True

    def _update_ruleconfig(self):
        """Perform the internal update of the rule configuration object."""
        put_data = {"id": self.id, "parameters": {"enable_host_based_firewall": self.enabled,
                                                  "default_rule": self.get_parameter('default_rule')}}
        if self._rule_groups_valid:
            put_data['parameters']['rule_groups'] = [group._flatten() for group in self._rule_groups]
        else:
            put_data['parameters']['rule_groups'] = self.get_parameter('rule_groups')
        resp = self._cb.put_object(self._base_url(), [put_data])
        result = resp.json()
        success = [d for d in result.get("successful", []) if d.get("id", None) == self.id]
        if not success:
            raise ApiError("update of host-based firewall failed")
        self._info = success[0]
        self._rule_groups = []
        self._rule_groups_valid = False
        self._mark_changed(False)

    def _delete_ruleconfig(self):
        """Perform the internal delete of the rule configuration object."""
        my_id = self.id
        self._cb.delete_object(self._base_url() + f"/{my_id}")
        self._info = {"id": my_id}
        self._full_init = False  # forcing _refresh() next time we read an attribute
        self._rule_groups = []
        self._rule_groups_valid = False
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
        if not self._rule_groups_valid:
            rg_param = self.get_parameter("rule_groups")
            if rg_param is not None:
                self._rule_groups = [HostBasedFirewallRuleConfig.FirewallRuleGroup(self._cb, d) for d in rg_param]
                for group in self._rule_groups:
                    group._init_parent(self)
            else:
                self._rule_groups = []
            self._rule_groups_valid = True
        return self._rule_groups

    def new_rule_group(self, name, description):
        """
        Creates a new FirewallRuleGroup object.

        Args:
            name (str): The name of the new rule group.
            description (str): The description of the new rule group.

        Returns:
            FirewallRuleGroup: The new rule group object.  Add it to this rule configuration with append_rule_group.
        """
        return HostBasedFirewallRuleConfig.FirewallRuleGroup(self._cb, {"name": name, "description": description,
                                                                        "rules": []})

    def append_rule_group(self, rule_group):
        """
        Appends a rule group to the list of rule groups in the rule configuration.

        Args:
            rule_group (FirewallRuleGroup): The rule group to be added.
        """
        self.rule_groups.append(rule_group)
        rule_group._parent = self
        self._mark_changed()

    def new_rule(self, name, action, direction, protocol, remote_ip):
        """
        Creates a new FirewallRule object.

        Args:
            name (str): The name for the new rule.
            action (str): The action to be taken by this rule. Valid values are "ALLOW," "BLOCK," and "BLOCK_ALERT."
            direction (str): The traffic direction this rule matches. Valid values are "IN," "OUT," and "BOTH."
            protocol (str): The network protocol this rule matches. Valid values are "TCP" and "UDP."
            remote_ip (str): The remote IP address this rule matches.

        Returns:
            FirewallRule: The new firewall rule. Append it to a rule group using the group's append_rule method.
        """
        if action not in ("ALLOW", "BLOCK", "BLOCK_ALERT"):
            raise ApiError(f"invalid rule action: {action}")
        if direction not in ("IN", "OUT", "BOTH"):
            raise ApiError(f"invalid rule direction: {direction}")
        if protocol not in ("TCP", "UDP"):
            raise ApiError(f"invalid rule protocol: {protocol}")
        return HostBasedFirewallRuleConfig.FirewallRule(self._cb, {"action": action, "application_path": "*",
                                                                   "direction": direction, "enabled": True,
                                                                   "name": name,
                                                                   "protocol": protocol, "local_ip_address": "*",
                                                                   "local_port_ranges": "*",
                                                                   "remote_ip_address": remote_ip,
                                                                   "remote_port_ranges": "*",
                                                                   "test_mode": False})
