# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model Class for NetworkThreatMetadata"""

from cbc_sdk.base import NewBaseModel
from cbc_sdk.errors import ApiError


class NetworkThreatMetadata(NewBaseModel):
    """Represents a NetworkThreatMetadata"""

    primary_key = "tms_rule_id"
    swagger_meta_file = "platform/models/network_threat_metadata.yaml"
    urlobject = "/threatmetadata/v1/orgs/{0}/detectors/{1}"

    def __init__(
        self,
        cb,
        model_unique_id=None,
        initial_data=None,
        force_init=False,
        full_doc=True,
    ):
        """
        Initialize the NetworkThreatMetadata object.

        Required Permissions:
            org.xdr.metadata (READ)

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): Not used, retained for compatibility.
            force_init (bool): False to not force object initialization.
            full_doc (bool): True to mark the object as fully initialized.

        Raises:
            ApiError: if model_unique_id is not provided
        """
        self._info = None
        if not model_unique_id:
            raise ApiError("model_unique_id is required.")

        url = NetworkThreatMetadata.urlobject.format(cb.credentials.org_key, model_unique_id)
        data = cb.get_object(url)
        data[NetworkThreatMetadata.primary_key] = model_unique_id

        super(NetworkThreatMetadata, self).__init__(
            cb,
            model_unique_id=model_unique_id,
            initial_data=data,
            force_init=force_init,
            full_doc=full_doc,
        )

    @classmethod
    def _query_implementation(self, cb, **kwargs):
        """
        Raises NotImplementedError, because the resource doesn't allow querying.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.
        """
        raise NotImplementedError("Resource does not allow query")
