# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Test code for the helper functions"""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


def test_argument_parser_default_values():
    """Tests the default credential values."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    assert args.cburl is None
    assert args.apitoken is None
    assert args.orgkey is None
    assert args.no_ssl_verify is False
    assert args.profile == 'default'
    assert args.verbose is False
    assert args.window == '3d'


def test_apicloudapi_object_with_command_line_arguments():
    """Tests the CBCloudAPI object with command line arguments."""
    parser = build_cli_parser("Test helpers.py")
    args = parser.parse_known_args()[0]

    args.cburl = 'https://example.com'
    args.apitoken = 'ABCDEFGH'
    args.orgkey = 'A1B2C3D4'
    args.no_ssl_verify = 'false'

    api = get_cb_cloud_object(args)

    assert api.credential_profile_name is None


# def test_apicloudapi_object_with_default_arguments():
#    """Tests the CBCloudAPI object with default arguments."""
#    parser = build_cli_parser("Test helpers.py")
#    args = parser.parse_known_args()[0]
#
#    api = get_cb_cloud_object(args)
#
#    assert api.credential_profile_name == 'default'
