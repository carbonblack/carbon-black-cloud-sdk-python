#!/usr/bin/env python
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

"""
The following script verifies CSP OAuth authentication in a CSP enabled Carbon Black Cloud instance.

To execute, ensure you have the following:
* Carbon Black Cloud URL
* CSP API Token
* CSP OAuth App ID
* CSP OAuth App Secret
* Organization Key

To send the args to the test use the following cli template

    python3 csp_oauth.py --cburl '' --csp-api-token '' --csp-oauth-app-id '' --csp-oauth-app-secret '' --orgkey ''

Optionally add the following override if you are not using CSP production (https://console.cloud.vmware.com)

    --csp-url-override ''

If you don't have CSP credentials follow this [guide](TBD)
"""

import sys

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Device


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb_api_token = get_cb_cloud_object(args)

    # Force second API object to use OAuth App
    args.csp_api_token = None

    cb_oauth_app = get_cb_cloud_object(args)

    assert type(cb_api_token.select(Device).first()) is Device and cb_api_token.credentials._token_type == "API_TOKEN"
    print("Successfully fetched Device using CSP API Token!")

    assert type(cb_oauth_app.select(Device).first()) is Device and cb_oauth_app.credentials._token_type == "OAUTH_APP"
    print("Successfully fetched Device using CSP OAuth App!")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
