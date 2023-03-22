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

"""Create a new user from the command line."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User
import sys


def main():
    """Main function for the user creation script"""
    parser = build_cli_parser('Create a User')
    parser.add_argument('first_name', help='First name for the new user')
    parser.add_argument('last_name', help='Last name for the new user')
    parser.add_argument('email', help='E-mail address for the new user')
    parser.add_argument('phone', help='Phone number for the new user')
    parser.add_argument('role', help='Role URN to assign the new user')
    parser.add_argument('-P', '--accessprofiles', action='store_true',
                        help='Use access profiles when creating the user')

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    builder = User.create(cb).set_first_name(args.first_name).set_last_name(args.last_name).set_email(args.email)
    builder.set_phone(args.phone)
    if args.accessprofiles:
        builder.add_grant_profile([cb.org_urn], [args.role])
    else:
        builder.set_role(args.role)
    builder.build()
    print("New user created.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
