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

"""Model and Query Classes for Users"""
from cbc_sdk.base import MutableBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin
from cbc_sdk.errors import ApiError, ServerError, ObjectNotFoundError
from cbc_sdk.platform.grants import Grant, normalize_org
import time
import copy
import logging

log = logging.getLogger(__name__)

"""User Models"""


def normalize_profile_list(profile_templates):
    """Internal function to normalize a list of profile templates."""
    return_profiles = None
    if profile_templates:
        return_profiles = []
        for template in profile_templates:
            return_profiles.append({'orgs': {'allow': [normalize_org(org) for org in template['orgs']['allow']]},
                                    'roles': template['roles']})
    return return_profiles


class User(MutableBaseModel):
    """Represents a user in the Carbon Black Cloud."""
    urlobject = "/appservices/v6/orgs/{0}/users"
    urlobject_single = "/appservices/v6/orgs/{0}/users/{1}"
    primary_key = "login_id"
    swagger_meta_file = "platform/models/user.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the User object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): Login ID of this user.
            initial_data (dict): Initial data used to populate the user.
        """
        super(User, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            if not self._refresh():
                raise ObjectNotFoundError(f"user with login ID {model_unique_id} not found")

    class UserBuilder:
        """Auxiliary object used to construct a new User."""
        def __init__(self, cb):
            """
            Create the empty UserBuilder object.

            Args:
                cb (BaseAPI): Reference to API object used to communicate with the server.
            """
            self._cb = cb
            self._creation_data = {'org_id': 0, 'role': 'DEPRECATED', 'auth_method': 'PASSWORD'}

        def set_email(self, email):
            """
            Sets the E-mail address for the new user.

            Args:
                email (str): The E-mail address for the new user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['email'] = email
            return self

        def set_phone(self, phone):
            """
            Sets the phone number for the new user.

            Args:
                phone (str): The phone number for the new user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['phone'] = phone
            return self

        def set_role(self, role):
            """
            Sets the role URN for the new user.

            Args:
                role (str): The URN of the role to set for the user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['role_urn'] = role
            return self

        def set_first_name(self, first_name):
            """
            Sets the first name for the new user.

            Args:
                first_name (str): The first name for the new user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['first_name'] = first_name
            return self

        def set_last_name(self, last_name):
            """
            Sets the last name for the new user.

            Args:
                last_name (str): The last name for the new user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['last_name'] = last_name
            return self

        def set_auth_method(self, method):
            """
            Sets the authentication method for the new user.  The default is 'PASSWORD'.

            Args:
                method (str): The authentication method for the new user.

            Returns:
                UserBuilder: This object.
            """
            self._creation_data['auth_method'] = method
            return self

        def add_grant_profile(self, orgs, roles):
            """
            Adds a grant profile for the new user.

            Args:
                orgs (list[str]): List of organizations to be allowed, specified as keys or URNs.
                roles (list[str]): List of roles to be granted, specified as URNs.

            Returns:
                UserBuilder: This object.
            """
            new_profile = {'orgs': {'allow': [normalize_org(org) for org in orgs]}, 'roles': roles}
            if 'profiles' in self._creation_data:
                self._creation_data['profiles'].append(new_profile)
            else:
                self._creation_data['profiles'] = [new_profile]
            return self

        def build(self):
            """
            Builds the new user.

            Notes:
                The new user will not be "findable" by other API functions until it has been activated and its initial
                password has been set.
            """
            User._create_user(self._cb, self._creation_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for Users.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            UserQuery: The query object for users.
        """
        return UserQuery(cls, cb)

    @classmethod
    def _create_user(cls, cb, user_data):
        """
        Creates a new user from template data.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            user_data (dict): The user data to be used to create the new user.

        Raises:
            ServerError: If the user registration was unsuccessful.

        Notes:
            The new user will not be "findable" by other API functions until it has been activated and its initial
            password has been set.
        """
        url = User.urlobject.format(cb.credentials.org_key)
        result = cb.post_object(url, user_data)
        resp = result.json()
        if resp['registration_status'] != 'SUCCESS':
            raise ServerError(500, f"registration return was unsuccessful: {resp['registration_status']} - "
                                   f"{resp['message']}", uri=url)
        # N.B.: new user is not "findable" until activated and initial password set

    def _refresh(self):
        """
        Rereads the user data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        userdata = self._cb.get_object(self.urlobject.format(self._cb.credentials.org_key))
        rawdata = [user for user in userdata.get('users', []) if user.get('login_id', 0) == self._model_unique_id]
        if len(rawdata) == 0:
            return False
        self._info = rawdata[0]
        self._full_init = True
        self._last_refresh_time = time.time()
        return True

    def _update_object(self):
        """
        Updates the user data on the server.

        Returns:
            int: The user ID for this user.
        """
        if 'login_id' not in self._info:
            raise ApiError("user should have already been created")
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        self._cb.put_object(url, self._info)
        return self._model_unique_id

    def _delete_object(self):
        """Deletes the user."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        self._cb.delete_object(url)
        return self._model_unique_id

    @property
    def urn(self):
        """
        Returns the URN for this user (used in accessing Grants).

        Returns:
            str: URN for this user.
        """
        return f"psc:user:{self._cb.credentials.org_key}:{self._info['login_id']}"

    @property
    def org_urn(self):
        """
        Returns the URN for this user's organization (used in accessing Grants).

        Returns:
            str: URN for this user's organization.
        """
        return f"psc:org:{self._cb.credentials.org_key}"

    def grant(self):
        """
        Locates the access grant for this user.

        Returns:
            Grant: Access grant for this user, or None if the user has none.
        """
        query = self._cb.select(Grant).add_principal(self.urn, self.org_urn)
        try:
            return query.one()
        except ObjectNotFoundError:
            return None

    @classmethod
    def create(cls, cb, template=None):
        """
        Creates a new user.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            template (dict): Optional template data for creating the new user.

        Returns:
            UserBuilder: If template is None, returns an instance of this object. Call methods on the object to set
                         the values associated with the new user, and then call build() to create it.
        """
        try:
            if cb.__class__.__name__ != 'CBCloudAPI':
                raise Exception
        except:
            raise ApiError("Unable to create User without CBCloudAPI")

        if template:
            my_templ = copy.deepcopy(template)
            my_templ['org_id'] = 0
            my_templ['role'] = 'DEPRECATED'
            if 'auth_method' not in my_templ:
                my_templ['auth_method'] = 'PASSWORD'
            User._create_user(cb, my_templ)
            return None
        return User.UserBuilder(cb)

    def reset_google_authenticator_registration(self):
        """Forces Google Authenticator registration to be reset for this user."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + "/google-auth"
        self._cb.delete_object(url)

    @classmethod
    def bulk_create(cls, cb, user_templates, profile_templates):
        """
        Creates a series of new users.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            user_templates (list[dict]): List of templates for users to be created.
            profile_templates (list[dict]): List of profile templates to be applied to each user.
        """
        my_profiles = normalize_profile_list(profile_templates)
        for template in user_templates:
            my_templ = copy.deepcopy(template)
            my_templ['org_id'] = 0
            my_templ['role'] = 'DEPRECATED'
            if 'auth_method' not in my_templ:
                my_templ['auth_method'] = 'PASSWORD'
            if 'profiles' in my_templ:
                del my_templ['profiles']
            if my_profiles:
                my_templ['profiles'] = my_profiles
            User._create_user(cb, my_templ)

    @classmethod
    def bulk_add_profiles(cls, users, profile_templates):
        """
        Add the specified profiles to the specified users' grants.

        Args:
            users (list[User]): List of User objects specifying users to be modified.
            profile_templates (list[dict]): List of profile templates to be added to the users.
        """
        my_profiles = normalize_profile_list(profile_templates)
        if my_profiles:
            for user in users:
                user._internal_add_profiles(my_profiles)

    @classmethod
    def bulk_disable_profiles(cls, users, profile_templates):
        """
        Disable the specified profiles in the specified users' grants.

        Args:
            users (list[User]): List of User objects specifying users to be modified.
            profile_templates (list[dict]): List of profile templates to be disabled.
        """
        my_profiles = normalize_profile_list(profile_templates)
        if my_profiles:
            for user in users:
                user._internal_disable_profiles(my_profiles)

    @classmethod
    def bulk_disable_all_access(cls, users):
        """
        Disables all access profiles held by the listed users.

        Args:
            users (list[User]): List of User objects specifying users to be disabled.
        """
        for user in users:
            user._disable_all_access()

    @classmethod
    def bulk_delete(cls, users):
        """
        Deletes all the listed users.

        Args:
            users (list[User]): List of User objects specifying users to be deleted.
        """
        for user in users:
            user.delete()

    def _disable_all_access(self):
        """
        Disables all access profiles held by ths user.

        Returns:
            bool: True if this user was a "legacy" user (no grant), False otherwise.
        """
        grant = self.grant()
        if grant:
            for profile in grant.profiles_:
                profile.set_disabled(True)
                grant.touch()
            grant.save()
            return False
        else:
            return True

    def disable_all_access(self):
        """
        Disables all access profiles held by ths user.

        Raises:
            ApiError: If the user is a "legacy" user that has no grant.
        """
        if self._disable_all_access():
            raise ApiError("legacy user has no grant")

    def change_role(self, role_urn, org=None):
        """
        Add the specified role to the user (either to the grant or the profiles).

        Args:
            role_urn (str): URN of the role to be added.
            org (str): If specified, only profiles that match this organization will have the role added.  Organization
                       may be specified as either an org key or a URN.

        Raises:
            ApiError: If the user is a "legacy" user that has no grant.
        """
        my_org = None if org is None else normalize_org(org)
        grant = self.grant()
        if grant:
            prof_list = grant.profiles_
            if len(prof_list) > 0:
                for profile in prof_list:
                    add_role = True
                    if my_org and my_org not in profile.allowed_orgs:
                        add_role = False
                    if add_role and role_urn not in profile.roles:
                        profile.roles += [role_urn]
                        grant.touch()
            elif role_urn not in grant.roles:
                grant.roles += [role_urn]
                grant.touch()
            grant.save()
        else:
            raise ApiError("legacy user has no grant")

    def _internal_add_profiles(self, profile_templates):
        """
        Add the specified profiles to the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be added to the user.  Must be normalized.
        """
        grant = self.grant()
        if grant:
            create_templates = []
            for template in profile_templates:
                need_create = True
                for profile in grant.profiles_:
                    if profile.matches_template(template) and profile.conditions['disabled']:
                        profile.set_disabled(False)
                        grant.touch()
                        need_create = False
                        break
                if need_create:
                    create_templates.append(template)
            grant.save()
            for template in create_templates:
                grant.create_profile(template)
        else:
            grant_template = {'principal': self.urn, 'org_ref': self.org_urn, 'roles': [],
                              'principal_name': f"{self.first_name} {self.last_name}", 'profiles': profile_templates}
            Grant.create(self._cb, grant_template)

    def _internal_disable_profiles(self, profile_templates):
        """
        Disable the specified profiles in the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be disabled.  Must be normalized.

        Returns:
            bool: True if this user was a "legacy" user (no grant), False otherwise.
        """
        grant = self.grant()
        if grant:
            for profile in grant.profiles_:
                for template in profile_templates:
                    if profile.matches_template(template):
                        profile.set_disabled(True)
                        grant.touch()
                        break
            grant.save()
            return False
        else:
            return True

    def _internal_set_profile_expiration(self, profile_templates, expiration_date):
        """
        Set the expiration time for the specified profiles in the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be reset.  Must be normalized.
            expiration_date (str): New expiration date, in ISO 8601 format.

        Returns:
            bool: True if this user was a "legacy" user (no grant), False otherwise.
        """
        grant = self.grant()
        if grant:
            for profile in grant.profiles_:
                for template in profile_templates:
                    if profile.matches_template(template):
                        profile.set_expiration(expiration_date)
                        grant.touch()
                        break
            grant.save()
            return False
        else:
            return True

    def add_profiles(self, profile_templates):
        """
        Add the specified profiles to the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be added to the user.
        """
        my_profiles = normalize_profile_list(profile_templates)
        if my_profiles:
            self._internal_add_profiles(my_profiles)

    def disable_profiles(self, profile_templates):
        """
        Disable the specified profiles in the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be disabled.

        Raises:
            ApiError: If the user is a "legacy" user that has no grant.
        """
        my_profiles = normalize_profile_list(profile_templates)
        if my_profiles:
            if self._internal_disable_profiles(my_profiles):
                raise ApiError("legacy user has no grant")

    def set_profile_expiration(self, profile_templates, expiration_date):
        """
        Set the expiration time for the specified profiles in the user's grant.

        Args:
            profile_templates (list[dict]): List of profile templates to be reset.
            expiration_date (str): New expiration date, in ISO 8601 format.

        Raises:
            ApiError: If the user is a "legacy" user that has no grant.
        """
        my_profiles = normalize_profile_list(profile_templates)
        if my_profiles:
            if self._internal_set_profile_expiration(my_profiles, expiration_date):
                raise ApiError("legacy user has no grant")

    def delete(self):
        """Delete this object."""
        grant = self.grant()  # CBAPI-3122 - remove grant first if present
        if grant:
            grant.delete()
        return self._delete_object()


"""User Queries"""


class UserQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    """Query for retrieving users in bulk."""
    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(UserQuery, self).__init__(None)
        self._doc_class = doc_class
        self._cb = cb
        self._valid_emails = None
        self._valid_userids = None
        self._count_valid = False
        self._total_results = 0

    def email_addresses(self, addrs):
        """
        Limit the query to users with the specified E-mail addresses.  Call multiple times to add multiple addresses.

        Args:
            addrs (list[str]): List of addresses to be added to the query.

        Returns:
            UserQuery: This object.
        """
        addr_set = set(addrs)
        self._valid_emails = addr_set if self._valid_emails is None else addr_set.union(self._valid_emails)
        return self

    def user_ids(self, userids):
        """
        Limit the query to users with the specified user IDs.  Call multiple times to add multiple user IDs.

        Args:
            userids (list[str]): List of user IDs to be added to the query.

        Returns:
            UserQuery: This object.
        """
        id_set = set(userids)
        self._valid_userids = id_set if self._valid_userids is None else id_set.union(self._valid_userids)
        return self

    def _include_user(self, userdata):
        """
        Predicate to determine if a user's data should be included in the query result.

        Args:
            userdata (dict): Raw user data.

        Returns:
            bool: True if this data should be included, False if not.
        """
        if self._valid_emails is not None and userdata['email'] not in self._valid_emails:
            return False
        if self._valid_userids is not None and userdata['login_id'] not in self._valid_userids:
            return False
        return True

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Returns:
            list[dict]: The raw results of the query, as a list of dicts.
        """
        rawdata = self._cb.get_object("/appservices/v6/orgs/{0}/users".format(self._cb.credentials.org_key))
        return rawdata.get('users', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if not self._count_valid:
            return_data = self._execute()
            filtered_data = [item for item in return_data if self._include_user(item)]
            self._total_results = len(filtered_data)
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
        filtered_data = [item for item in return_data if self._include_user(item)]
        self._total_results = len(filtered_data)
        self._count_valid = True
        for item in filtered_data:
            yield User(self._cb, item['login_id'], item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used; always None.

        Returns:
            list[User]: Result of the async query, as a list of User objects.
        """
        return_data = self._execute()
        output = [User(self._cb, item['login_id'], item) for item in return_data if self._include_user(item)]
        self._total_results = len(output)
        self._count_valid = True
        return output
