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

"""Set a user's enable/disable status from the command line."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User
import sys


def get_status(user):
    """Returns True if user is enabled, False if disabled."""
    grant = user.grant()
    return not grant.revoked


def update_status(user, value):
    """Sets the enable/disable status of a user."""
    grant = user.grant()
    for profile in grant.profiles_:
        profile.set_disabled(not value)
    grant.revoked = not value
    grant.save()


def main():
    """Main function for the role changing script"""
    parser = build_cli_parser("Set User Enable/Disable")
    parser.add_argument('email', help='E-mail address of the user to set status of')
    parser.add_argument('-e', '--enable', action='store_true', help='Enable this user')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable this user')

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    user = cb.select(User).email_addresses([args.email]).one()
    if args.enable:
        update_status(user, True)
        status = True
    elif args.disable:
        update_status(user, False)
        status = False
    else:
        status = get_status(user)
    print(f"Current status: {'ENABLED' if status else 'DISABLED'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
