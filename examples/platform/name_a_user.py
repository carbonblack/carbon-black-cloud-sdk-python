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

"""Example script which finds a user without a name and gives them one."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User
import sys
import random


def main():
    """Main function for the user renaming script"""
    parser = build_cli_parser('Name A User')
    parser.add_argument('first_name', help='New first name to give a (random) user')
    parser.add_argument('last_name', help='New last name to give a (random) user')

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    users = list(cb.select(User))
    print(f"Loaded {len(users)} users from server")
    filtered_users = [user for user in users if not (user.first_name or user.last_name)]
    print(f"{len(filtered_users)} users potentially eligible")
    target_user = random.sample(filtered_users, 1)[0]
    print(f"Selected the user with login ID {target_user.login_id} for modification")
    target_user.first_name = args.first_name
    target_user.last_name = args.last_name
    target_user.save()
    print(f"user with login ID {target_user.login_id} is now {target_user.first_name} {target_user.last_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
