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

"""Model and Query Classes for Endpoint Standard"""

from cbc_sdk.base import (MutableBaseModel, CreatableModelMixin, NewBaseModel, PaginatedQuery,
                          QueryBuilder, QueryBuilderSupportMixin, IterableQueryMixin)
from cbc_sdk.platform import PSCQueryBase
from cbc_sdk.utils import convert_query_params
from copy import deepcopy
import logging
import json
import time
import sys

from cbc_sdk.errors import ServerError

log = logging.getLogger(__name__)


"""Defense Models"""


class DefenseMutableModel(MutableBaseModel):
    _change_object_http_method = "PATCH"
    _change_object_key_name = None

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        super(DefenseMutableModel, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                                  force_init=force_init, full_doc=full_doc)
        if not self._change_object_key_name:
            self._change_object_key_name = self.primary_key

    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))

    def _parse(self, obj):
        if type(obj) == dict and self.info_key in obj:
            return obj[self.info_key]

    def _update_object(self):
        if self._change_object_http_method != "PATCH":
            return self._update_entire_object()
        else:
            return self._patch_object()

    def _update_entire_object(self):
        if self.__class__.primary_key in self._dirty_attributes.keys() or self._model_unique_id is None:
            new_object_info = deepcopy(self._info)
            try:
                if not self._new_object_needs_primary_key:
                    del(new_object_info[self.__class__.primary_key])
            except Exception:
                pass
            log.debug("Creating a new {0:s} object".format(self.__class__.__name__))
            ret = self._cb.api_json_request(self.__class__._new_object_http_method, self.urlobject,
                                            data={self.info_key: new_object_info})
        else:
            log.debug("Updating {0:s} with unique ID {1:s}".format(self.__class__.__name__, str(self._model_unique_id)))
            ret = self._cb.api_json_request(self.__class__._change_object_http_method,
                                            self._build_api_request_uri(), data={self.info_key: self._info})

        return self._refresh_if_needed(ret)

    def _patch_object(self):
        if self.__class__.primary_key in self._dirty_attributes.keys() or self._model_unique_id is None:
            log.debug("Creating a new {0:s} object".format(self.__class__.__name__))
            ret = self._cb.api_json_request(self.__class__._new_object_http_method, self.urlobject,
                                            data=self._info)
        else:
            updates = {}
            for k in self._dirty_attributes.keys():
                updates[k] = self._info[k]
            log.debug("Updating {0:s} with unique ID {1:s}".format(self.__class__.__name__, str(self._model_unique_id)))
            ret = self._cb.api_json_request(self.__class__._change_object_http_method,
                                            self._build_api_request_uri(), data=updates)

        return self._refresh_if_needed(ret)

    def _refresh_if_needed(self, request_ret):
        refresh_required = True

        if request_ret.status_code not in range(200, 300):
            try:
                message = json.loads(request_ret.text)[0]
            except Exception:
                message = request_ret.text

            raise ServerError(request_ret.status_code, message,
                              result="Did not update {} record.".format(self.__class__.__name__))
        else:
            try:
                message = request_ret.json()
                log.debug("Received response: %s" % message)
                if not isinstance(message, dict):
                    raise ServerError(request_ret.status_code, message,
                                      result="Unknown error updating {0:s} record.".format(self.__class__.__name__))
                else:
                    if message.get("success", False):
                        if isinstance(message.get(self.info_key, None), dict):
                            self._info = message.get(self.info_key)
                            self._full_init = True
                            refresh_required = False
                        else:
                            if self._change_object_key_name in message.keys():
                                # if all we got back was an ID, try refreshing to get the entire record.
                                log.debug("Only received an ID back from the server, forcing a refresh")
                                self._info[self.primary_key] = message[self._change_object_key_name]
                                refresh_required = True
                    else:
                        # "success" is False
                        raise ServerError(request_ret.status_code, message.get("message", ""),
                                          result="Did not update {0:s} record.".format(self.__class__.__name__))
            except Exception:
                raise

        self._dirty_attributes = {}
        if refresh_required:
            self.refresh()
        return self._model_unique_id


class Device(DefenseMutableModel):
    urlobject = "/integrationServices/v3/device"
    urlobject_single = "/integrationServices/v3/device/{}"
    primary_key = "deviceId"
    info_key = "deviceInfo"
    swagger_meta_file = "defense/models/deviceInfo.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Device, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))

    def lr_session(self):
        """
        Retrieve a Live Response session object for this Device.

        :return: Live Response session object
        :rtype: :py:class:`cbc_sdk.defense.cblr.LiveResponseSession`
        :raises ApiError: if there is an error establishing a Live Response session for this Device

        """
        return self._cb._request_lr_session(self._model_unique_id)


class Event(NewBaseModel):
    urlobject = "/integrationServices/v3/event"
    primary_key = "eventId"
    info_key = "eventInfo"

    def _parse(self, obj):
        if type(obj) == dict and self.info_key in obj:
            return obj[self.info_key]

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Event, self).__init__(cb, model_unique_id, initial_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))


class Policy(DefenseMutableModel, CreatableModelMixin):
    urlobject = "/integrationServices/v3/policy"
    info_key = "policyInfo"
    swagger_meta_file = "defense/models/policyInfo.yaml"
    _change_object_http_method = "PUT"
    _change_object_key_name = "policyId"

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return Query(cls, cb, kwargs.get("query_string", None))
        # return Query(cls, cb)

    @property
    def rules(self):
        return dict([(r.get("id"), r) for r in self.policy.get("rules", [])])

    def add_rule(self, new_rule):
        self._cb.post_object("{0}/rule".format(self._build_api_request_uri()), {"ruleInfo": new_rule})
        self.refresh()

    def delete_rule(self, rule_id):
        self._cb.delete_object("{0}/rule/{1}".format(self._build_api_request_uri(), rule_id))
        self.refresh()

    def replace_rule(self, rule_id, new_rule):
        self._cb.put_object("{0}/rule/{1}".format(self._build_api_request_uri(), rule_id),
                            {"ruleInfo": new_rule})
        self.refresh()


"""Defense Queries"""


class Query(PaginatedQuery, PSCQueryBase, QueryBuilderSupportMixin, IterableQueryMixin):
    """Represents a prepared query to the Cb Defense server.

    This object is returned as part of a :py:meth:`CBCloudAPI.select`
    operation on models requested from the Cb Defense server. You should not have to create this class yourself.

    The query is not executed on the server until it's accessed, either as an iterator (where it will generate values
    on demand as they're requested) or as a list (where it will retrieve the entire result set and save to a list).
    You can also call the Python built-in ``len()`` on this object to retrieve the total number of items matching
    the query.

    Examples::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI()

    Notes:
        - The slicing operator only supports start and end parameters, but not step. ``[1:-1]`` is legal, but
          ``[1:2:-1]`` is not.
        - You can chain where clauses together to create AND queries; only objects that match all ``where`` clauses
          will be returned.
    """
    # def __init__(self, doc_class, cb, query=None):
    def __init__(self, doc_class, cb, query=None):
        super(Query, self).__init__(doc_class, cb, query)

        self._sort_by = None
        self._group_by = None
        self._batch_size = 100
        self._criteria = {}
        self._query_builder = QueryBuilder()


    def _clone(self):
        nq = self.__class__(self._doc_class, self._cb)
        # nq._query = self._query[::]
        nq._sort_by = self._sort_by
        nq._group_by = self._group_by
        nq._batch_size = self._batch_size
        nq._criteria = self._criteria
        return nq


    def prepare_query(self, args):
        request = args
        params = self._query_builder._collapse()
        if params is not None:
            for query in params.split(' '):
                # convert from str('key:value') to dict{'key': 'value'}
                key, value = query.split(':', 1)
                request[key] = value
        return request

    def _count(self):
        if self._count_valid:
            return self._total_results

        args = {'limit': 0}
        args = self.prepare_query(args)

        query_args = convert_query_params(args)
        self._total_results = int(self._cb.get_object(self._doc_class.urlobject, query_parameters=query_args)
                                  .get("totalResults", 0))
        self._count_valid = True
        return self._total_results

    def _search(self, start=0, rows=0):
        # iterate over total result set, 1000 at a time
        args = {}
        if start != 0:
            args['start'] = start
        args['rows'] = self._batch_size

        current = start
        numrows = 0

        args = self.prepare_query(args)
        still_querying = True

        while still_querying:
            query_args = convert_query_params(args)
            result = self._cb.get_object(self._doc_class.urlobject, query_parameters=query_args)

            self._total_results = result.get("totalResults", 0)
            self._count_valid = True

            results = result.get('results', [])

            if results is None:
                log.debug("Results are None")
                if current >= 100000:
                    log.info("Max result size exceeded. Truncated to 100k.")
                break

            for item in results:
                yield item
                current += 1
                numrows += 1
                if rows and numrows == rows:
                    still_querying = False
                    break

            args['start'] = current + 1     # as of 6/2017, the indexing on the Cb Defense backend is still 1-based

            if current >= self._total_results:
                break

            if not results:
                log.debug("server reported total_results overestimated the number of results for this query by {0}"
                          .format(self._total_results - current))
                log.debug("resetting total_results for this query to {0}".format(current))
                self._total_results = current
                break
