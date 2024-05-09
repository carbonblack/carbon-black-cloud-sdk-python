# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Stub object to be used for testing base object code"""

from cbc_sdk.base import MutableBaseModel


class StubObject(MutableBaseModel):
    """Stub object used for doing unit tests of lower level objects."""
    urlobject = "/testing_only/v1/stubobjects"
    urlobject_single = "/testing_only/v1/stubobjects/{0}"
    primary_key = "id"
    swagger_meta_file = "platform/models/stub.yaml"

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the stub object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): ID of the policy.
            initial_data (dict): Initial data used to populate the policy.
            force_init (bool): If True, forces the object to be refreshed after constructing.  Default False.
            full_doc (bool): If True, object is considered "fully" initialized. Default False.
        """
        super(StubObject, self).__init__(cb, model_unique_id=model_unique_id, initial_data=initial_data,
                                         force_init=force_init, full_doc=full_doc)


"""Mock responses for the objects"""
STUBOBJECT_GET_RESP = {
    "id": 30241,
    "name": "Stub One",
    "device": 42,
    "function": "ADD",
    "parameter": "XXVI"
}

STUBOBJECT_GET_PARTIAL = {
    "id": 30241,
    "name": "Stub One",
    "device": 42
}

STUBOBJECT_GET_RESP_1 = {
    "id": 30242,
    "name": "fakeName",
    "device": 66,
    "function": "CLAMP",
    "parameter": "409"
}

STUBOBJECT_GET_RESP_2 = {
    "id": 30243,
    "name": "StubThreeTM",
    "device": 101,
    "function": "DIVIDE",
    "parameter": "2"
}

STUBOBJECT_UPDATE_RESP = {
    "id": 30242,
    "name": "newFakeName",
    "device": 69,
    "function": "CLAMP",
    "parameter": "409"
}

STUBOBJECT_POST_RESP = {
    "id": 30241,
    "name": "fakeName",
    "device": 66,
    "function": "CLAMP",
    "parameter": "409"
}
