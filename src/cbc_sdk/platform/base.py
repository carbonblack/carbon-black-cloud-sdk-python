#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Platform"""

from cbc_sdk.base import NewBaseModel

import logging

log = logging.getLogger(__name__)

"""Platform Models"""


class PlatformModel(NewBaseModel):
    """Represents the base of all Platform API model classes."""

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the PlatformModel object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        super(PlatformModel, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                            force_init=force_init, full_doc=full_doc)
