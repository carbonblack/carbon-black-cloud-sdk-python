#!/usr/bin/env python
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

"""
The following script verifies CSP OAuth authentication in a CSP enabled Carbon Black Cloud instance.

To execute, ensure you have the following:
* Carbon Black Cloud URL
* CSP API Token
* CSP OAuth App ID
* CSP OAuth App Secret
* Organization Key

If you don't have CSP credentials follow this [guide](TBD)
"""

import sys

from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Device

url = ''
csp_api_token = ''
csp_oauth_app_id = ''
csp_oauth_app_secret = ''
csp_url_override = None
org_key = ''
proxy = ''


def main():
    """Script entry point"""
    cb_api_token = CBCloudAPI(url=url,
                              csp_api_token=csp_api_token,
                              csp_url_override=csp_url_override,
                              org_key=org_key,
                              ssl_verify=False)

    cb_oauth_app = CBCloudAPI(url=url,
                              csp_oauth_app_id=csp_oauth_app_id,
                              csp_oauth_app_secret=csp_oauth_app_secret,
                              org_key=org_key,
                              ssl_verify=False)

    assert type(cb_api_token.select(Device).first()) is Device
    print("Successfully fetched Device using CSP API Token!")

    assert type(cb_oauth_app.select(Device).first()) is Device
    print("Successfully fetched Device using CSP OAuth App!")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
