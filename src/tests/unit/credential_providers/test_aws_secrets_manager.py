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

"""Tests for the AWSCredentialProvider"""

from unittest import mock

import pytest

from cbc_sdk.credential_providers.aws_sm_credential_provider import AWSCredentialProvider
from cbc_sdk.credentials import CredentialError


@mock.patch("boto3.session.Session.client")
def test_raising_exception_on_emtpy_secret(client):
    """Test for raising the CredentialError."""
    client = mock.Mock()
    client.get_secret_value.return_value = {}
    with pytest.raises(CredentialError):
        AWSCredentialProvider(secret_arn="test").get_credentials()
