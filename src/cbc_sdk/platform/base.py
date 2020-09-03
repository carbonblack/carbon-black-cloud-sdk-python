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


from cbc_sdk.base import NewBaseModel

import logging

log = logging.getLogger(__name__)


"""Platform Models"""


class PlatformModel(NewBaseModel):
    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        super(PlatformModel, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                           force_init=force_init, full_doc=full_doc)


"""Platform Queries"""


class PlatformQueryBase:
    """
    Represents the base of all LiveQuery query classes.
    """

    def __init__(self, doc_class, cb):
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
