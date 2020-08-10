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

"""Model and Query Classes for Platform"""

from cbc_sdk.errors import ApiError, MoreThanOneResultError
import functools
from solrq import Q


from cbc_sdk.base import MutableBaseModel
from cbc_sdk.errors import ServerError

from copy import deepcopy
import logging
import json

log = logging.getLogger(__name__)


"""Platform Models"""


class PSCMutableModel(MutableBaseModel):
    _change_object_http_method = "PATCH"
    _change_object_key_name = None

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        super(PSCMutableModel, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                              force_init=force_init, full_doc=full_doc)
        if not self._change_object_key_name:
            self._change_object_key_name = self.primary_key

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
                pass

        self._dirty_attributes = {}
        if refresh_required:
            self.refresh()
        return self._model_unique_id


"""Platform Queries"""


# class QueryBuilder(object):
#     """
#     Provides a flexible interface for building prepared queries for the CB
#     PSC backend.
#
#     This object can be instantiated directly, or can be managed implicitly
#     through the :py:meth:`select` API.
#     """
#
#     def __init__(self, **kwargs):
#         if kwargs:
#             self._query = Q(**kwargs)
#         else:
#             self._query = None
#         self._raw_query = None
#
#     def _guard_query_params(func):
#         """Decorates the query construction methods of *QueryBuilder*, preventing
#         them from being called with parameters that would result in an internally
#         inconsistent query.
#         """
#
#         @functools.wraps(func)
#         def wrap_guard_query_change(self, q, **kwargs):
#             if self._raw_query is not None and (kwargs or isinstance(q, Q)):
#                 raise ApiError("Cannot modify a raw query with structured parameters")
#             if self._query is not None and isinstance(q, str):
#                 raise ApiError("Cannot modify a structured query with a raw parameter")
#             return func(self, q, **kwargs)
#
#         return wrap_guard_query_change
#
#     @_guard_query_params
#     def where(self, q, **kwargs):
#         """Adds a conjunctive filter to a query.
#
#         :param q: string or `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: QueryBuilder object
#         :rtype: :py:class:`QueryBuilder`
#         """
#         if isinstance(q, str):
#             if self._raw_query is None:
#                 self._raw_query = []
#             self._raw_query.append(q)
#         elif isinstance(q, Q) or kwargs:
#             if self._query is not None:
#                 raise ApiError("Use .and_() or .or_() for an extant solrq.Q object")
#             if kwargs:
#                 q = Q(**kwargs)
#             self._query = q
#         else:
#             raise ApiError(".where() only accepts strings or solrq.Q objects")
#
#         return self
#
#     @_guard_query_params
#     def and_(self, q, **kwargs):
#         """Adds a conjunctive filter to a query.
#
#         :param q: string or `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: QueryBuilder object
#         :rtype: :py:class:`QueryBuilder`
#         """
#         if isinstance(q, str):
#             self.where(q)
#         elif isinstance(q, Q) or kwargs:
#             if kwargs:
#                 q = Q(**kwargs)
#             if self._query is None:
#                 self._query = q
#             else:
#                 self._query = self._query & q
#         else:
#             raise ApiError(".and_() only accepts strings or solrq.Q objects")
#
#         return self
#
#     @_guard_query_params
#     def or_(self, q, **kwargs):
#         """Adds a disjunctive filter to a query.
#
#         :param q: `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: QueryBuilder object
#         :rtype: :py:class:`QueryBuilder`
#         """
#         if kwargs:
#             q = Q(**kwargs)
#
#         if isinstance(q, Q):
#             if self._query is None:
#                 self._query = q
#             else:
#                 self._query = self._query | q
#         else:
#             raise ApiError(".or_() only accepts solrq.Q objects")
#
#         return self
#
#     @_guard_query_params
#     def not_(self, q, **kwargs):
#         """Adds a negative filter to a query.
#
#         :param q: `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: QueryBuilder object
#         :rtype: :py:class:`QueryBuilder`
#         """
#         if kwargs:
#             q = ~Q(**kwargs)
#
#         if isinstance(q, Q):
#             if self._query is None:
#                 self._query = q
#             else:
#                 self._query = self._query & q
#         else:
#             raise ApiError(".not_() only accepts solrq.Q objects")
#
#     def _collapse(self):
#         """The query can be represented by either an array of strings
#         (_raw_query) which is concatenated and passed directly to Solr, or
#         a solrq.Q object (_query) which is then converted into a string to
#         pass to Solr. This function will perform the appropriate conversions to
#         end up with the 'q' string sent into the POST request to the
#         PSC-R query endpoint."""
#         if self._raw_query is not None:
#             return " ".join(self._raw_query)
#         elif self._query is not None:
#             return str(self._query)
#         else:
#             return None  # return everything


class PSCQueryBase:
    """
    Represents the base of all LiveQuery query classes.
    """

    def __init__(self, doc_class, cb):
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False


# class QueryBuilderSupportMixin:
#     """
#     A mixin that supplies wrapper methods to access the _query_builder.
#     """
#     def where(self, q=None, **kwargs):
#         """Add a filter to this query.
#
#         :param q: Query string, :py:class:`QueryBuilder`, or `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: Query object
#         :rtype: :py:class:`Query`
#         """
#
#         if not q:
#             return self
#         if isinstance(q, QueryBuilder):
#             self._query_builder = q
#         else:
#             self._query_builder.where(q, **kwargs)
#         return self
#
#     def and_(self, q=None, **kwargs):
#         """Add a conjunctive filter to this query.
#
#         :param q: Query string or `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: Query object
#         :rtype: :py:class:`Query`
#         """
#         if not q and not kwargs:
#             raise ApiError(".and_() expects a string, a solrq.Q, or kwargs")
#
#         self._query_builder.and_(q, **kwargs)
#         return self
#
#     def or_(self, q=None, **kwargs):
#         """Add a disjunctive filter to this query.
#
#         :param q: `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: Query object
#         :rtype: :py:class:`Query`
#         """
#         if not q and not kwargs:
#             raise ApiError(".or_() expects a solrq.Q or kwargs")
#
#         self._query_builder.or_(q, **kwargs)
#         return self
#
#     def not_(self, q=None, **kwargs):
#         """Adds a negated filter to this query.
#
#         :param q: `solrq.Q` object
#         :param kwargs: Arguments to construct a `solrq.Q` with
#         :return: Query object
#         :rtype: :py:class:`Query`
#         """
#
#         if not q and not kwargs:
#             raise ApiError(".not_() expects a solrq.Q, or kwargs")
#
#         self._query_builder.not_(q, **kwargs)
#         return self
#
#
# class IterableQueryMixin:
#     """
#     A mix-in to provide iterability to a query.
#     """
#     def all(self):
#         """
#         Returns all the items of a query as a list.
#
#         :return: List of query items
#         """
#         return self._perform_query()
#
#     def first(self):
#         """
#         Returns the first item that would be returned as the result of a query.
#
#         :return: First query item
#         """
#         allres = list(self)
#         res = allres[:1]
#         if not len(res):
#             return None
#         return res[0]
#
#     def one(self):
#         """
#         Returns the only item that would be returned by a query.
#
#         :return: Sole query return item
#         :raises MoreThanOneResultError: If the query returns zero items, or more than one item
#         """
#         allres = list(self)
#         res = allres[:2]
#         if len(res) == 0:
#             raise MoreThanOneResultError(
#                 message="0 results for query {0:s}".format(self._query)
#             )
#         if len(res) > 1:
#             raise MoreThanOneResultError(
#                 message="{0:d} results found for query {1:s}".format(
#                     len(self), self._query
#                 )
#             )
#         return res[0]
#
#     def __len__(self):
#         return self._count()
#
#     def __getitem__(self, item):
#         return None
#
#     def __iter__(self):
#         return self._perform_query()
