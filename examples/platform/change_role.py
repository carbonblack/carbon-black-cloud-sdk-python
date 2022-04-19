#!/usr/bin/env python
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

"""Change a user's role from the command line."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User
import sys


def main():
    """Main function for the role changing script"""
    parser = build_cli_parser("Change User's Role")
    parser.add_argument('email', help='E-mail address of the user to change role of')
    parser.add_argument('role', help='New role URN for the user')

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    user = cb.select(User).email_addresses([args.email]).one()
    grant = user.grant()
    need_reset = True
    for profile in grant.profiles_:
        if profile.allowed_orgs == [cb.org_urn]:
            profile.roles = [args.role]
            profile.save()
            need_reset = False
    if need_reset:
        grant.roles = [args.role]
        grant.save()
    print("Role changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
