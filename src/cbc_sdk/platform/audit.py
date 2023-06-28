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

from cbc_sdk.base import UnrefreshableModel


class AuditLog(UnrefreshableModel):
    """Model class which represents audit log events. Mostly for future implementation."""

    def __init__(self, cb, model_unique_id, initial_data=None):
        """Creation of AuditLog objects is not yet implemented."""
        raise NotImplementedError("AuditLog creation will be in a future implementation")

    @staticmethod
    def get_auditlogs(cb):
        """
        Retrieve queued audit logs from the Carbon Black Cloud server.

        Notes:
            This can only be used with a 'API' key generated in the CBC console.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            list[dict]: List of dictionary objects representing the audit logs, or an empty list if none available.
        """
        res = cb.get_object("/integrationServices/v3/auditlogs")
        return res.get("notifications", [])
