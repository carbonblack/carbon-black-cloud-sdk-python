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

"""Model and Query Classes for Users"""
from cbc_sdk.base import MutableBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin
from cbc_sdk.errors import ApiError, ServerError, ObjectNotFoundError
import time
import copy


"""User Models"""


def normalize_org(org):
    """Internal function to normalize an org reference to a URN."""
    if org.startswith('psc:org:'):
        return org
    return f"psc:org:{org}"


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
            self._creation_data['email_id'] = email
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
                orgs (list): List of organizations to be allowed, specified as keys or URNs.
                roles (list): List of roles to be granted, specified as URNs.

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
            Builds the new user and returns it.

            Returns:
                User: The new user object from the server.
            """
            return User._create_user(self._cb, self._creation_data)

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

        Returns:
            User: The new user object from the server.

        Raises:
            ServerError: If the user registration was unsuccessful.
        """
        url = User.urlobject.format(cb.credentials.org_key)
        result = cb.post_object(url, user_data)
        resp = result.json()
        if resp['registration_type'] == 'SUCCESS':
            return User(cb, int(resp['login_id']))
        raise ServerError(500, f"registration return was unsuccessful: {resp['registration_type']}")

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

    @classmethod
    def create(cls, cb, template=None):
        """
        Creates a new user.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            template (dict): Optional template data for creating the new user.

        Returns:
            User: New user created, if template is specified.
            UserBuilder: If template is None, returns an instance of this object. Call methods on the object to set
                         the values associated with the new user, and then call build() to create it.
        """
        if template:
            my_templ = copy.deepcopy(template)
            my_templ['org_id'] = 0
            my_templ['role'] = 'DEPRECATED'
            if 'auth_method' not in my_templ:
                my_templ['auth_method'] = 'PASSWORD'
            return User._create_user(cb, my_templ)
        return User.UserBuilder(cb)

    def reset_google_authenticator_registration(self):
        """Forces Google Authenticator registration to be reset for this user."""
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + "/google-auth"
        self._cb.delete_object(url)


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
        self._count_valid = False
        self._total_results = 0

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Returns:
            list: The raw results of the query, as a list of dicts.
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
            yield User(self._cb, item['login_id'], item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used; always None.

        Returns:
            list: Result of the async query, as a list of User objects.
        """
        return_data = self._execute()
        self._total_results = len(return_data)
        self._count_valid = True
        return [User(self._cb, item['login_id'], item) for item in return_data]
