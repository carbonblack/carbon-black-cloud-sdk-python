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
import json

import pytest

from cbc_sdk.credential_providers.aws_sm_credential_provider import AWSCredentialProvider
from cbc_sdk.credentials import CredentialError


@mock.patch("boto3.session.Session")
def test_raising_exception_on_emtpy_secret(mock_session_class):
    """Test for raising the CredentialError."""
    mock_session_object = mock.Mock()
    mock_client = mock.Mock()
    mock_client.get_secret_value.return_value = {}
    mock_session_object.client.return_value = mock_client
    mock_session_class.return_value = mock_session_object
    with pytest.raises(CredentialError):
        AWSCredentialProvider(secret_arn="test").get_credentials()


@mock.patch("boto3.session.Session")
def test_aws_getting_credentials(mock_session_class):
    """Test for getting credentials."""
    test_data = {
        "url": "<URL>",
        "token": "<TOKEN>",
        "org_key": "<ORG_KEY>",
        "ssl_verify": True,
        "ssl_verify_hostname": True,
        "ssl_cert_file": "<FILE_PATH>",
        "ssl_force_tls_1_2": True,
        "proxy": "<NAME_OF_THE_PROXY_HOST>",
        "ignore_system_proxy": True,
        "integration": "<INTEGRATION_NAME>"
    }
    mock_session_object = mock.Mock()
    mock_client = mock.Mock()
    mock_client.get_secret_value.return_value = {"SecretString": json.dumps(test_data)}
    mock_session_object.client.return_value = mock_client
    mock_session_class.return_value = mock_session_object
    credentials = AWSCredentialProvider(secret_arn="test").get_credentials()
    assert credentials.to_dict() == test_data
