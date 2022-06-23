# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the AWSCredentialProvider"""
import json

import pytest

from boto3.session import Session

from cbc_sdk.credential_providers.aws_sm_credential_provider import AWSCredentialProvider
from cbc_sdk.credentials import CredentialError


class ClientMock:  # noqa: D101
    def __init__(self, *args, **kwargs):  # noqa: D107
        pass

    def get_secret_value(self, *args, **kwargs):  # noqa: D102
        pass


def test_raising_exception_on_emtpy_secret(monkeypatch):
    """Test for raising the CredentialError."""
    monkeypatch.setattr(Session, "client", ClientMock)
    monkeypatch.setattr(ClientMock, "get_secret_value", lambda *args, **kwargs: {})
    with pytest.raises(CredentialError):
        AWSCredentialProvider(secret_arn="test").get_credentials()


def test_aws_getting_credentials(monkeypatch):
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

    monkeypatch.setattr(Session, "client", ClientMock)
    monkeypatch.setattr(ClientMock, "get_secret_value", lambda *args, **kwargs: {"SecretString": json.dumps(test_data)})
    credentials = AWSCredentialProvider(secret_arn="test").get_credentials()
    assert credentials.to_dict() == test_data
