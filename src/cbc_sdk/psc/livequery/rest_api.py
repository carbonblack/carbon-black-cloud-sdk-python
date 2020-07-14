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

from cbc_sdk.psc.livequery.models import Run, RunHistory
from cbc_sdk.psc.rest_api import CbPSCBaseAPI
from cbc_sdk.errors import CredentialError, ApiError
import logging

log = logging.getLogger(__name__)


class CbLiveQueryAPI(CbPSCBaseAPI):
    """The main entry point into the Carbon Black Cloud LiveQuery API.

    :param str profile: (optional) Use the credentials in the named profile when connecting to the Carbon Black server.
        Uses the profile named 'default' when not specified.

    Usage::

    >>> from cbc_sdk.psc.livequery import CbLiveQueryAPI
    >>> cb = CbLiveQueryAPI(profile="production")
    """
    def __init__(self, *args, **kwargs):
        super(CbLiveQueryAPI, self).__init__(*args, **kwargs)

        if not self.credentials.get("org_key", None):
            raise CredentialError("No organization key specified")

    def _perform_query(self, cls, **kwargs):
        if hasattr(cls, "_query_implementation"):
            return cls._query_implementation(self)
        else:
            raise ApiError("All LiveQuery models should provide _query_implementation")

    def query(self, sql):
        return self.select(Run).where(sql=sql)

    def query_history(self, query=None):
        return self.select(RunHistory).where(query)
