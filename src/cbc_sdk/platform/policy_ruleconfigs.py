#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
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
from cbc_sdk.errors import ApiError, ServerError, InvalidObjectError


class PolicyRuleConfig(MutableBaseModel):
    """
    Represents a rule configuration in the policy.

    Create one of these objects, associating it with a Policy, and set its properties, then call its save() method to
    add the rule configuration to the policy. This requires the org.policies(UPDATE) permission.

    To update a PolicyRuleConfig, change the values of its property fields, then call its save() method.  This
    requires the org.policies(UPDATE) permission.

    To delete an existing PolicyRuleConfig, call its delete() method. This requires the org.policies(DELETE) permission.

    """
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

    def _update_object(self):
        """
        Updates the rule configuration object on the policy on the server.

        Required Permissions:
            org.policies(UPDATE)
        """
        self._parent._on_updated_rule_config(self)

    def _delete_object(self):
        """
        Deletes this rule configuration object from the policy on the server.

        Required Permissions:
            org.policies(DELETE)
        """
        was_deleted = False
        try:
            self._parent._on_deleted_rule_config(self)
            was_deleted = True
        finally:
            if was_deleted:
                self._parent = None

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

    @property
    def is_deleted(self):
        """Returns True if this rule configuration object has been deleted."""
        return self._parent is None
