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


def normalize_org(org):
    """Internal function to normalize an org reference to a URN."""
    if org.startswith('psc:org:'):
        return org
    return f"psc:org:{org}"


class Grant(MutableBaseModel):
    """Represents a grant of access to the Carbon Black Cloud."""
    urlobject = "/access/v2/orgs/{0}/grants"
    urlobject_single = "/access/v2/orgs/{0}/grants/{1}"
    primary_key = "principal"
    swagger_meta_file = "platform/models/grant.yaml"

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
            raw_profiles = initial_data.get('profiles', [])
            if raw_profiles:
                self._profiles = [Grant.Profile(cb, self, prof.get('profile_uuid', None), prof)
                                  for prof in raw_profiles]
            else:
                self._profiles = []
        else:
            self._profiles = []
        if model_unique_id is not None and initial_data is None:
            self._refresh()

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
            Throws an error, since Profile data cannot be refreshed.

            Raises:
                ApiError: Always.
            """
            raise ApiError("Profile cannot be refreshed")

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
                grant (Grant/GrantBuilder): The grant or GrantBuilder the new profile will be attached to.
            """
            if isinstance(grant, Grant.GrantBuilder):
                self._grantbuilder = grant
                self._grant = None
                self._cb = grant._cb
            else:
                self._grant = grant
                self._grantbuilder = None
                self._cb = grant._cb
            self._orgs = {'allow': []}
            self._roles = []
            self._conditions = {'expiration': 0, 'disabled': False}
            self._can_manage = False

        def set_orgs(self, orgs_list):
            """
            Set the list of organizations to which the new profile is allowed access.

            Args:
                orgs_list (list): List of organization keys or URNs.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['allow'] = [normalize_org(org) for org in orgs_list]
            return self

        def add_org(self, org):
            """
            Adds the specified organization to the list of organizations for which the new profile is allowed.

            Args:
                org (str): Organization key or URN of the organization to be added.

            Returns:
                ProfileBuilder: This object.
            """
            self._orgs['allow'].append(normalize_org(org))
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

        def build(self):
            """
            Builds the new Profile object from the entered data.

            Returns:
                Profile: The new Profile object.
            """
            data = {'orgs': self._orgs, 'roles': self._roles, 'conditions': self._conditions}
            profile = Grant.Profile(self._cb, self._grant, None, data)
            if self._grant:
                profile._update_object()
                self._grant._profiles.append(profile)
            else:
                self._grantbuilder._profiles.append(profile)
            return profile

    class GrantBuilder:
        """Auxiliary object used to construct a new grant."""
        def __init__(self, cb, principal):
            """
            Creates the empty GrantBuilder object.

            Args:
                cb (CBCloudAPI): The reference to the API object that accesses the server.
                principal (str): The URN for the principal.
            """
            self._cb = cb
            self._principal = principal
            self._roles = []
            self._org_ref = ''
            self._principal_name = ''
            self._profiles = []

        def set_roles(self, roles):
            """
            Sets the roles to be associated with the new grant.

            Args:
                roles (list): List of role URNs.

            Returns:
                GrantBuilder: This object.
            """
            self._roles = roles
            return self

        def add_role(self, role):
            """
            Adds a role to be associated with the new grant.

            Args:
                role (str): URN of the role to be added.

            Returns:
                GrantBuilder: This object.
            """
            self._roles.append(role)
            return self

        def set_org(self, org):
            """
            Sets the organization reference to be associated with the new grant.

            Args:
                org (str): Organization key or URN of the organization.

            Returns:
                GrantBuilder: This object.
            """
            self._org_ref = normalize_org(org)
            return self

        def set_principal_name(self, name):
            """
            Sets the principal name to be associated with the new object.

            Args:
                name (str): Principal name to be used.

            Returns:
                GrantBuilder: This object.
            """
            self._principal_name = name
            return self

        def create_profile(self, template=None):
            """
            Returns either a new Profile, or a ProfileBuilder to begin the process of adding profile to the new grant.

            Args:
                template (dict): Optional template to use for creating the profile object.

            Returns:
                Profile: If a template was specified, return the new Profile object.
                ProfileBuilder: If template was None, returns a ProfileBuilder object.  Call methods on it to set
                                up the new profile, and then call build() to create the new profile.
            """
            if template:
                t = copy.deepcopy(template)
                if 'profile_uuid' in t:
                    del t['profile_uuid']
                profile = Grant.Profile(self._cb, None, None, t)
                self._profiles.append(profile)
                return profile
            return Grant.ProfileBuilder(self)

        def build(self):
            """
            Builds the new Grant object from the entered data.

            Returns:
                Grant: The new Grant object.
            """
            data = {'principal': self._principal, 'roles': self._roles, 'profiles': [], 'org_ref': self._org_ref,
                    'principal_name': self._principal_name}
            grant = Grant(self._cb, self._principal, data)
            for profile in self._profiles:
                profile._grant = grant
            grant._profiles = self._profiles
            grant._update_object()  # causes new grant to be immediately pushed to the server
            return grant

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
        raw_profiles = resp.get('profiles', [])
        if raw_profiles:
            self._profiles = [Grant.Profile(self._cb, self, prof.get('profile_uuid', None), prof)
                              for prof in raw_profiles]
        else:
            self._profiles = []
        self._full_init = True
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
        is_update = all([key in save_info for key in ['created_by', 'updated_by', 'create_time', 'update_time']])

        if is_update:
            log.debug("Updating the Grant object for principal {0:s}".format(save_info['principal']))
            save_info['profiles'] = [copy.deepcopy(prof._info)
                                     for prof in self._profiles if 'profile_uuid' in prof._info]
            url = self.urlobject_single.format(self._cb.credentials.org_key, save_info['principal'])
            ret = self._cb.put_object(url, save_info)
        else:
            log.debug("Creating a new Grant object for principal {0:s}".format(save_info['principal']))
            save_info['profiles'] = []
            for profile in self._profiles:
                # presumed to be all new profiles, so create UUIDs for them
                profile._info['profile_uuid'] = str(uuid.uuid4())
                save_info['profiles'].append(copy.deepcopy(profile._info))
            url = self.urlobject.format(self._cb.credentials.org_key)
            ret = self._cb.post_object(url, save_info)
        update_return = self._refresh_if_needed(ret)

        # for update, add all profiles not yet part of grant (for which UUIDs have yet to be assigned)
        if is_update:
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
    def create(cls, cb, template=None, **kwargs):
        """
        Returns either a new Grant, or a GrantBuilder to begin the process of creating a new grant.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            template (dict): Optional template to use for creating the grant object.
            kwargs (dict): Additional arguments to be used to specify the principal, if template is None.
                           The arguments to be used are 'org_key' and 'userid' for the two parts of the ID.

        Returns:
            Grant: The new grant object, if the template is specified.
            GrantBuilder: If template was None, returns a GrantBuilder object.  Call methods on it to set
                            up the new grant, and then call build() to create the new grant.

        Raises:
            ApiError: If the principal is inadequately specified (whether for the Grant or GrantBuilder).
        """
        if template:
            if 'principal' not in template:
                raise ApiError('principal must be specified in Grant template')
            t = copy.deepcopy(template)
            grant = Grant(cb, t['principal'], t)
            grant._update_object()
            return grant
        if not all([key in kwargs for key in ['org_key', 'userid']]):
            raise ApiError('orgid and userid must be specified as keyword arguments to create')
        return Grant.GrantBuilder(cb, f"psc:user:{kwargs['org_key']}:{kwargs['userid']}")

    @property
    def profiles_(self):
        """
        Return the profiles associated with this grant.

        Returns:
            list: The profiles associated with this grant, each represented as a Profile object.
        """
        return self._profiles

    def create_profile(self, template=None):
        """
        Returns either a new Profile, or a ProfileBuilder to begin the process of adding a new profile to this grant.

        Args:
            template (dict): Optional template to use for creating the profile object.

        Returns:
            Profile: If a template was specified, return the new Profile object.
            ProfileBuilder: If template was None, returns a ProfileBuilder object.  Call methods on it to set
                            up the new profile, and then call build() to create the new profile.
        """
        if template:
            t = copy.deepcopy(template)
            if 'profile_uuid' in t:
                del t['profile_uuid']
            profile = Grant.Profile(self._cb, self, None, t)
            profile._update_object()
            return profile
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
