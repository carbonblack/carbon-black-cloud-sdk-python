#!/usr/bin/env python
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

"""
The following script verifies that an API call to a Carbon Black Cloud instance is able to route through a proxy.

To execute, ensure you have the following:
* Carbon Black Cloud URL
* API Token ({api_secret_key}/{api_id})
* Organization Key
* Proxy URL

If you don't have a proxy configured consider setting up a proxy server using tinyproxy

The following tinyproxy.conf file will allow all traffic to be accepted at port 8080

    User nobody
    Group nobody
    Port 8080
    Timeout 600
    DefaultErrorFile "/usr/local/share/tinyproxy/default.html"
    StatFile "/usr/local/share/tinyproxy/stats.html"
    LogLevel Info
    MaxClients 100
    ViaProxyName "tinyproxy"

    #
    # Optional Authentication
    # Proxy URL with authentication http://user:password@0.0.0.0:8080
    #
    # BasicAuth user password
"""

import sys

from cbc_sdk.platform import Device
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()

    cb = get_cb_cloud_object(args)

    assert type(cb.select(Device).first()) is Device
    print(f"Successfully fetched Device using proxy: {args.proxy}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
