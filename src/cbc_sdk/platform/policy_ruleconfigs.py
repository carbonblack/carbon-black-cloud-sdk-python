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
        if self._model_unique_id is not None:
            rc = self._parent._refresh()
            if rc:
                newobj = self._parent.object_rule_configs.get(self.id, None)
                if newobj:
                    self._info = newobj._info
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

    def get_parameter(self, name):
        """
        Returns a parameter value from the rule configuration.

        Args:
            name (str): The parameter name.

        Returns:
            Any: The parameter value, or None if there is no value.
        """
        params = self._info['parameters']
        return params.get(name, None)

    def set_parameter(self, name, value):
        """
        Sets a parameter value into the rule configuration.

        Args:
            name (str): The parameter name.
            value (Any): The new value to be set.
        """
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
    pass
