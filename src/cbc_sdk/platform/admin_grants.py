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
from cbc_sdk.errors import ApiError
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

        def __init__(self, cb, model_unique_id, initial_data=None, grant=None):
            super(Grant.Profile, self).__init__(cb, model_unique_id, initial_data)
            self._grant = grant
            if model_unique_id is not None and initial_data is None:
                self._refresh()

        @classmethod
        def _query_implementation(cls, cb, **kwargs):
            raise ApiError("Profiles cannot be queried directly")

        def _refresh(self):
            url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                               self._model_unique_id)
            resp = self._cb.get_object(url)
            self._info = resp
            self._last_refresh_time = time.time()
            return True

        def _update_object(self):
            if 'profile_uuid' not in self._info:
                self._info['profile_uuid'] = str(uuid.uuid4())
                log.debug("Creating a Profile object with UUID {0:s} for Grant with ID {1:s}"
                          .format(self._model_unique_id, self._grant._model_unique_id))
                url = self.urlobject.format(self._cb.credentials.org_key, self._grant._model_unique_id)
                verb = 'POST'
            else:
                log.debug("Updating Profile object with UUID {0:s} for Grant with ID {1:s}"
                          .format(self._model_unique_id, self._grant._model_unique_id))
                url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                                   self._model_unique_id)
                verb = 'PUT'
            ret = self._cb.api_json_request(verb, url, data=self._info)
            return self._refresh_if_needed(ret)

        def _delete_object(self):
            url = self.urlobject_single.format(self._cb.credentials.org_key, self._grant._model_unique_id,
                                               self._model_unique_id)
            ret = self._cb.api_json_request('DELETE', url)
            self._refresh_if_needed(ret)

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Grant, self).__init__(cb, model_unique_id, initial_data)
        if initial_data:
            self._profiles = [Grant.Profile(cb, prof.get('profile_uuid', None), prof, self)
                              for prof in initial_data.get('profiles', [])]
        else:
            self._profiles = []
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return GrantQuery(cls, cb)

    def _refresh(self):
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._profiles = [Grant.Profile(self._cb, prof.get('profile_uuid', None), prof, self)
                          for prof in resp.get('profiles', [])]
        self._last_refresh_time = time.time()
        return True

    def _update_object(self):
        save_info = copy.deepcopy(self._info)
        if 'principal' not in save_info:
            raise ApiError("principal must be specified for a Grant object")
        save_info['profiles'] = [copy.deepcopy(prof._info) for prof in self._profiles if 'profile_uuid' in prof]
        if all([key in save_info for key in ['created_by', 'updated_by', 'create_time', 'update_time']]):
            log.debug("Updating the Grant object for principal {0:s}".format(save_info['principal']))
            url = self.urlobject_single.format(self._cb.credentials.org_key, save_info['principal'])
            verb = 'PUT'
        else:
            log.debug("Creating a new Grant object for principal {0:s}".format(save_info['principal']))
            url = self.urlobject.format(self._cb.credentials.org_key)
            verb = 'POST'
        ret = self._cb.api_json_request(verb, url, data=save_info)
        update_return = self._refresh_if_needed(ret)
        for profile in self._profiles:
            if 'profile_uuid' not in profile._info:
                profile._update_object()
        return update_return

    def _delete_object(self):
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        ret = self._cb.api_json_request('DELETE', url)
        self._refresh_if_needed(ret)

    @property
    def profiles_(self):
        return self._profiles


class GrantQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(GrantQuery, self).__init__(doc_class, cb, None)
        self._criteria = []

    def add_principal(self, principal_urn, org_urn):
        self._criteria.append({'principal': principal_urn, 'org_ref': org_urn})
        return self
