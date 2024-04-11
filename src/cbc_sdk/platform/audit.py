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

"""Model and Query Classes for Platform Auditing"""

from cbc_sdk.base import (UnrefreshableModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)


"""Model Class"""


class AuditLogRecord(UnrefreshableModel):
    """Model class which represents audit log events. Mostly for future implementation."""
    urlobject = "/audit_log/v1/orgs/{0}/logs"
    swagger_meta_file = "platform/models/audit_log_record.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Creates a new ``AuditLogRecord``.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): Not used.
            initial_data (dict): Initial data to fill in the audit log record details.
        """
        super(AuditLogRecord, self).__init__(cb, model_unique_id, initial_data)

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for the ``AuditLogRecord`` type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.
        """
        return AuditLogRecordQuery(cls, cb)

    @staticmethod
    def get_auditlogs(cb):
        """
        Retrieve queued audit logs from the Carbon Black Cloud server.

        Required Permissions:
            org.audits (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            list[dict]: List of dictionary objects representing the audit logs, or an empty list if none available.
        """
        res = cb.get_object("/integrationServices/v3/auditlogs")
        return res.get("notifications", [])


"""Query Class"""


class AuditLogRecordQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                          IterableQueryMixin, AsyncQueryMixin):
    """
    Query object that is used to locate ``AuditLogRecord`` objects.

    The ``AuditLogRecordQuery`` is constructed via SDK functions like the ``select()`` method on ``CBCloudAPI``.
    The user would then add a query and/or criteria to it before iterating over the results.
    """
    def __init__(self, doc_class, cb):
        """
        Initialize the ``AuditLogRecordQuery``.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(AuditLogRecordQuery, self).__init__()

        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._time_filter = {}
        self._exclusions = {}
        self._sortcriteria = {}
        self._search_after = None
        self.num_remaining = None
        self.num_found = None
        self.max_rows = -1
    