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

"""Credentials provider that reads the credentials from the AWS Secrets Manager"""

import json
import boto3
from cbc_sdk.credentials import Credentials, CredentialProvider, CredentialError


class AWSCredentialProvider(CredentialProvider):
    """This credential provider reads from the AWS Secrets Manager"""
    def __init__(self, secret_arn, region_name="us-east-2", profile_name=None):
        """
        Initialize the AWSCredentialProvider.

        Args:
            secret_arn (str): The name of the secret in the AWS Secrets Manager.
            region_name (str): The region name
            profile_name (str): The credentials profile
        """
        self.secret_arn = secret_arn
        self.region_name = region_name
        self.profile_name = profile_name
        self._cached_credentials = None

    def _get_secret_from_aws(self):
        """
        Reading the credentials from the AWS Secrets Manager.

        Returns:
            dict: Dictionary containing the secrets.

        Raises:
            CredentialError: If the `SecretString` is empty.
        """
        session = boto3.session.Session(profile_name=self.profile_name)
        client = session.client(
            service_name="secretsmanager",
            region_name=self.region_name
        )
        secret_value_response = client.get_secret_value(SecretId=self.secret_arn)
        if "SecretString" in secret_value_response:
            secret = secret_value_response["SecretString"]
        else:
            raise CredentialError("The secret is empty.")
        return json.loads(secret)

    def get_credentials(self, section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (None): Since AWS deosn't support sections it is left
            to satisfy the Signature of `CredentialProvider`

        Returns:
            Credentials: The credentials retrieved from that source.
        """
        if self._cached_credentials:
            return self._cached_credentials
        credentials = self._get_secret_from_aws()
        self._cached_credentials = Credentials(credentials)
        return self._cached_credentials
