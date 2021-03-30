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

"""Model and Query Classes for Administrative Grants and Profiles"""

from cbc_sdk.base import MutableBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin
from cbc_sdk.errors import ApiError, ServerError
import time
import copy
import uuid
import logging

log = logging.getLogger(__name__)

"""Grant and Profile Models"""


class Grant(MutableBaseModel):
    """Represents a grant of access to the Carbon Black Cloud."""
    urlobject = "/access/v2/orgs/{0}/grants"
    urlobject_single = "/access/v2/orgs/{0}/grants/{1}"
    primary_key = "principal"
    swagger_meta_file = "platform/models/grant.yaml"

    class Profile(MutableBaseModel):
        """Represents an access profile assigned to a grant."""
        urlobject = "/access/v2/orgs/{0}/grants/{1}/profiles"
        urlobject_single = "/access/v2/orgs/{0}/grants/{1}/profiles/{2}"
        primary_key = "profile_uuid"
        swagger_meta_file = "platform/models/profile.yaml"

        def __init__(self, cb, grant, model_unique_id, initial_data=None):
            """
            Initialize the Profile object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                grant (Grant): Reference to the Grant containing this Profile.
                model_unique_id (str): UUID of this profile.
                initial_data (dict): Initial data used to populate the profile.
            """
            super(Grant.Profile, self).__init__(cb, model_unique_id, initial_data, False, True)
            self._grant = grant
            if model_unique_id is not None and initial_data is None:
                self._refresh()

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            """
            Raises an error, as Profiles cannot be queried directly.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
                **kwargs (dict): Not used, retained for compatibility.

            Raises:
                ApiError: Always.
            """
            raise ApiError("Profiles cannot be queried directly")

        def _refresh(self):
            """
            Rereads the profile data from the server.

            Returns:
                bool: True if refresh was successful, False if not.
            """
            url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                               self._model_unique_id)
            resp = self._cb.get_object(url)
            self._info = resp
            self._last_refresh_time = time.time()
            return True

        def _update_object(self):
            """
            Updates the profile data on the server.

            Returns:
                str: The UUID of this profile object.
            """
            if 'profile_uuid' not in self._info:
                self._info['profile_uuid'] = str(uuid.uuid4())
                log.debug("Creating a Profile object with UUID {0:s} for Grant with ID {1:s}"
                          .format(self._model_unique_id, self._grant._model_unique_id))
                url = self.urlobject.format(self._cb.credentials.org_key, self._grant._model_unique_id)
                ret = self._cb.post_object(url, self._info)
            else:
                log.debug("Updating Profile object with UUID {0:s} for Grant with ID {1:s}"
                          .format(self._model_unique_id, self._grant._model_unique_id))
                url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                                   self._model_unique_id)
                ret = self._cb.put_object(url, self._info)
            return self._refresh_if_needed(ret)

        def _delete_object(self):
            """Deletes the profile from the enclosing grant."""
            url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                               self._model_unique_id)
            ret = self._cb.delete_object(url)
            self._refresh_if_needed(ret)

    class ProfileBuilder:
        """Auxiliary object used to construct a new profile on a grant."""
        def __init__(self, grant):
            """
            Create the empty ProfileBuilder object.

            Args:
                grant (Grant): The grant the new profile will be attached to.
            """
            self._grant = grant
            self._orgs = {'allow': [], 'deny': []}
            self._org_groups = []
            self._roles = []
            self._conditions = {'cidr': [], 'expiration': 0, 'disabled': False}
            self._can_manage = False

        def set_orgs(self, orgs_structure):
            """
            Set the organization allow and deny rules for the new profile.

            Args:
                orgs_structure (dict): The organization structure, with 'allow' and 'deny' members containing lists
                                       of organization URNs.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs = orgs_structure
            return self

        def set_allowed_orgs(self, orgs_list):
            """
            Set the list of organizations to which the new profile is allowed access.

            Args:
                orgs_list (list): List of organization URNs.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['allow'] = orgs_list
            return self

        def set_denied_orgs(self, orgs_list):
            """
            Set the list of organizations to which the new profile is denied access.

            Args:
                orgs_list (list): List of organization URNs.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['deny'] = orgs_list
            return self

        def add_allow(self, org):
            """
            Adds the specified organization to the list of organizations for which the new profile is allowed.

            Args:
                org (str): URN of the organization to be added.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['allow'].append(org)
            return self

        def add_deny(self, org):
            """
            Adds the specified organization to the list of organizations for which the new profile is denied.

            Args:
                org (str): URN of the organization to be added.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['deny'].append(org)
            return self

        def set_org_groups(self, groups_list):
            """
            Sets the list of organization groups associated with the new profile.

            Args:
                groups_list (list): A list of organization group identifiers.

            Returns:
                ProfileBuilder: This object.
            """
            self._org_groups = groups_list
            return self

        def add_org_group(self, org_group):
            """
            Adds an organization group identifier to the list of groups associated with the new profile.

            Args:
                org_group (str): Identifier of the organization group.

            Returns:
                ProfileBuilder: This object.
            """
            self._org_groups.append(org_group)
            return self

        def set_roles(self, roles_list):
            """
            Sets the list of roles associated with the new profile.

            Args:
                roles_list (list): A list of role URNs.

            Returns:
                ProfileBuilder: This object.
            """
            self._roles = roles_list
            return self

        def add_role(self, role):
            """
            Adds a role identifier to the list of roles associated with the new profile.

            Args:
                role (str): URN of the role to add.

            Returns:
                ProfileBuilder: This object.
            """
            self._roles.append(role)
            return self

        def set_conditions(self, conditions_structure):
            """
            Sets the access conditions associated with the new profile.

            Args:
                conditions_structure (dict): The conditions associated with the new profile, with 'cidr', 'expiration',
                                             and 'disabled' members.

            Returns:
                ProfileBuilder: This object.
            """
            self._conditions = conditions_structure
            return self

        def set_cidr(self, cidr_list):
            """
            Sets the list of CIDR access rules associated with the new profile.

            Args:
                cidr_list (list): List of CIDR access rules for the profile.

            Returns:
                ProfileBuilder: This object.
            """
            self._conditions['cidr'] = cidr_list
            return self

        def add_cidr(self, cidr):
            """
            Adds a CIDR access rule to the new profile.

            Args:
                cidr (str): CIDR access rule to be added.

            Returns:
                ProfileBuilder: This object.
            """
            self._conditions['cidr'].append(cidr)
            return self

        def set_expiration(self, expiration):
            """
            Sets the expiration time on the new profile.

            Args:
                expiration (str): The expiration time, specified as ISO 8601.

            Returns:
                ProfileBuilder: This object.
            """
            self._conditions['expiration'] = expiration
            return self

        def set_disabled(self, flag):
            """
            Sets whether or not the new profile is disabled.

            Args:
                flag (bool): True if this profile is disabled, False if noe.

            Returns:
                ProfileBuilder: This object.
            """
            self._conditions['disabled'] = flag
            return self

        def set_can_manage(self, flag):
            """
            Sets the management flag for the new profile.

            Args:
                flag (bool): New value of the management flag.

            Returns:
                ProfileBuilder: This object.
            """
            self._can_manage = flag
            return self

        def build(self):
            """
            Builds the new Profile object from the entered data.

            Returns:
                Profile: The new Profile object.
            """
            data = {'orgs': self._orgs, 'org_groups': self._org_groups, 'roles': self._roles,
                    'conditions': self._conditions, 'can_manage': self._can_manage}
            profile = Grant.Profile(self._grant._cb, self._grant, None, data)
            self._grant._profiles.append(profile)
            self._grant.touch()
            return profile

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Grant object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): URN of the principal associated with this grant.
            initial_data (dict): Initial data used to populate the grant.
        """
        super(Grant, self).__init__(cb, model_unique_id, initial_data)
        if initial_data:
            self._profiles = [Grant.Profile(cb, self, prof.get('profile_uuid', None), prof)
                              for prof in initial_data.get('profiles', [])]
        else:
            self._profiles = []
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for Grants.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            GrantQuery: The query object for this alert type.
        """
        return GrantQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the grant data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._profiles = [Grant.Profile(self._cb, self, prof.get('profile_uuid', None), prof)
                          for prof in resp.get('profiles', [])]
        self._last_refresh_time = time.time()
        return True

    def _update_object(self):
        """
        Updates the grant data on the server.

        Returns:
            str: The principal URN of this grant object.
        """
        save_info = copy.deepcopy(self._info)
        if 'principal' not in save_info:
            raise ApiError("principal must be specified for a Grant object")
        save_info['profiles'] = [copy.deepcopy(prof._info) for prof in self._profiles if 'profile_uuid' in prof._info]

        if all([key in save_info for key in ['created_by', 'updated_by', 'create_time', 'update_time']]):
            log.debug("Updating the Grant object for principal {0:s}".format(save_info['principal']))
            url = self.urlobject_single.format(self._cb.credentials.org_key, save_info['principal'])
            ret = self._cb.put_object(url, save_info)
        else:
            log.debug("Creating a new Grant object for principal {0:s}".format(save_info['principal']))
            url = self.urlobject.format(self._cb.credentials.org_key)
            ret = self._cb.post_object(url, save_info)
        update_return = self._refresh_if_needed(ret)

        # add all profiles not yet part of grant
        for profile in self._profiles:
            if 'profile_uuid' not in profile._info:
                profile._update_object()
        return update_return

    def _delete_object(self):
        """Deletes the grant from the principal."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        ret = self._cb.delete_object(url)
        self._refresh_if_needed(ret)

    @classmethod
    def new_grant(cls, cb, principal):
        """
        Create a new grant object for the specified principal.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            principal (str): The principal URN for the new grant object.

        Returns:
            Grant: The new grant object.
        """
        grant = Grant(cb, principal, {'principal': principal})
        grant._full_init = True
        return grant

    @property
    def profiles_(self):
        """
        Return the profiles associated with this grant.

        Returns:
            list: The profiles associated with this grant, each represented as a Profile object.
        """
        return self._profiles

    def new_profile(self):
        """
        Returns a ProfileBuilder to begin the process of adding a new profile to this grant.

        Returns:
            ProfileBuilder: The new ProfileBuilder object.
        """
        return Grant.ProfileBuilder(self)


class GrantQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    """Query for retrieving grants in bulk."""
    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(GrantQuery, self).__init__(None)
        self._doc_class = doc_class
        self._cb = cb
        self._criteria = []
        self._count_valid = False
        self._total_results = 0

    def add_principal(self, principal_urn, org_urn):
        """
        Add a new principal to the query.

        Args:
            principal_urn (str): URN of the principal to search for grants on.
            org_urn (str): URN of the organization to which the principal belongs.

        Returns:
            GrantQuery: This object.
        """
        self._criteria.append({'principal': principal_urn, 'org_ref': org_urn})
        return self

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Returns:
            list: The raw results of the query, as a list of dicts.

        Raises:
            ApiError: If criteria are not properly specified.
            ServerError: If a server error occurred in the query.
        """
        if len(self._criteria) == 0:
            raise ApiError("At least one principal must be specified for Grant query")
        ret = self._cb.post_object('/access/v2/grants/_fetch', self._criteria)
        if ret.status_code != 200:
            raise ServerError(ret.status_code,
                              ret.json().get('message', "Server error {0} occurred".format(ret.status_code)))
        return ret.json().get('additionalProp1', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if not self._count_valid:
            return_data = self._execute()
            self._total_results = len(return_data)
            self._count_valid = True
        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): Unused in this implementation, always 0.
            max_rows (int): Unused in this implementation, always -1.

        Returns:
            Iterable: The iterated query.
        """
        return_data = self._execute()
        self._total_results = len(return_data)
        self._count_valid = True
        for item in return_data:
            yield Grant(self._cb, item['principal'], item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used; always None.

        Returns:
            list: Result of the async query, as a list of Grant objects.
        """
        return_data = self._execute()
        self._total_results = len(return_data)
        self._count_valid = True
        return [Grant(self._cb, item['principal'], item) for item in return_data]
