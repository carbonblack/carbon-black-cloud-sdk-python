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

"""List all the roles the api_key is permitted to assign to users."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Grant
import sys


def main():
    """Main function for the user listing script"""
    parser = build_cli_parser('List Permitted Roles')
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    roles = Grant.get_permitted_role_urns(cb)
    for index, role in enumerate(sorted(roles)):
        print(f"{index + 1}. {role}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
