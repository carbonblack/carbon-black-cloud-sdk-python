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

"""Model Classes for Enterprise Endpoint Detection and Response"""

from __future__ import absolute_import
from cbc_sdk.errors import ApiError, InvalidObjectError, NonQueryableModel
from cbc_sdk.base import UnrefreshableModel
from cbc_sdk.enterprise_edr.base import Query

import logging
import validators

log = logging.getLogger(__name__)


class Binary(UnrefreshableModel):
    """Represents a retrievable binary."""
    primary_key = "sha256"
    swagger_meta_file = "enterprise_edr/models/binary.yaml"
    urlobject_single = "/ubs/v1/orgs/{}/sha256/{}/metadata"

    class Summary(UnrefreshableModel):
        """Represents a summary of organization-specific information for a retrievable binary."""
        primary_key = "sha256"
        urlobject_single = "/ubs/v1/orgs/{}/sha256/{}/summary/device"

        def __init__(self, cb, model_unique_id):
            """
            Initialize the Summary object.

            Args:
                cb (CBCloudAPI): A reference to the CBCloudAPI object.
                model_unique_id (str): The SHA-256 of the binary being retrieved.
            """
            if not validators.sha256(model_unique_id):
                raise ApiError("model_unique_id must be a valid SHA256")

            url = self.urlobject_single.format(cb.credentials.org_key, model_unique_id)
            item = cb.get_object(url)

            super(Binary.Summary, self).__init__(cb, model_unique_id=model_unique_id,
                                                 initial_data=item, force_init=False,
                                                 full_doc=True)

        def _query_implementation(self, cb, **kwargs):
            return Query(self, cb, **kwargs)

    def __init__(self, cb, model_unique_id):
        """
        Initialize the Binary object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (str): The SHA-256 of the binary being retrieved.
        """
        if not validators.sha256(model_unique_id):
            raise ApiError("model_unique_id must be a valid SHA256")

        url = self.urlobject_single.format(cb.credentials.org_key, model_unique_id)
        item = cb.get_object(url)

        super(Binary, self).__init__(cb, model_unique_id=model_unique_id,
                                     initial_data=item, force_init=False,
                                     full_doc=True)

    def _query_implementation(self, cb, **kwargs):
        return Query(self, cb, **kwargs)

    @property
    def summary(self):
        """Returns organization-specific information about this binary."""
        return self._cb.select(Binary.Summary, self.sha256)

    @property
    def download_url(self, expiration_seconds=3600):
        """Returns a URL that can be used to download the file for this binary. Returns None if no download found.

        Arguments:
            expiration_seconds (int): How long the download should be valid for.

        Returns:
            URL (str): A pre-signed AWS download URL.
            None: If no download is found.

        Raises:
            InvalidObjectError: If the URL retrieval should be retried.
        """
        downloads = self._cb.select(Downloads, [self.sha256],
                                    expiration_seconds=expiration_seconds)

        if self.sha256 in downloads.not_found:
            return None
        elif self.sha256 in downloads.error:
            raise InvalidObjectError("{} should be retried".format(self.sha256))
        else:
            return next((item.url
                        for item in downloads.found
                        if self.sha256 == item.sha256), None)


class Downloads(UnrefreshableModel):
    """Represents download information for a list of process hashes."""
    urlobject = "/ubs/v1/orgs/{}/file/_download"

    class FoundItem(UnrefreshableModel):
        """Represents the download URL and process hash for a successfully located binary."""
        primary_key = "sha256"

        def __init__(self, cb, item):
            """
            Initialize the FoundItem object.

            Args:
                cb (CBCloudAPI): A reference to the CBCloudAPI object.
                item (dict): The values for a successfully-retrieved item.
            """
            super(Downloads.FoundItem, self).__init__(cb, model_unique_id=item["sha256"],
                                                      initial_data=item, force_init=False,
                                                      full_doc=True)

        def _query_implementation(self, cb, **kwargs):
            raise NonQueryableModel("IOC does not support querying")

    def __init__(self, cb, shas, expiration_seconds=3600):
        """
        Initialize the Downloads object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            shas (list): A list of SHA hash values for binaries.
            expiration_seconds (int): Number of seconds until this request expires.
        """
        body = {
            "sha256": shas,
            "expiration_seconds": expiration_seconds,
        }

        url = self.urlobject.format(cb.credentials.org_key)
        item = cb.post_object(url, body).json()

        super(Downloads, self).__init__(cb, model_unique_id=None,
                                        initial_data=item, force_init=False,
                                        full_doc=True)

    def _query_implementation(self, cb, **kwargs):
        return Query(self, cb, **kwargs)

    @property
    def found(self):
        """Returns a list of Downloads.FoundItem, one for each binary found in the binary store."""
        return [Downloads.FoundItem(self._cb, item) for item in self._info["found"]]
