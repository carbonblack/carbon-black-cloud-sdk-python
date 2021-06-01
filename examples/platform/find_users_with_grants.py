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

"""Find users that have "interesting" grants (with profiles) and list them."""

from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User
import sys


def has_grant(user):
    """Returns True if the user is "interesting" (has a grant with profiles)."""
    grant = user.grant()
    if grant:
        return len(grant.profiles_) > 0
    else:
        return False


def main():
    """Main function for the user listing script"""
    parser = build_cli_parser('Find Users With Grants')
    parser.add_argument('-n', '--number', type=int, default=0,
                        help="Maximum number of users to find (default no limit)")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    users = cb.select(User)
    result_list = []
    count = 0
    for user in users:
        if has_grant(user):
            result_list.append(user)
            if 0 < args.number == len(result_list):
                break
        count = count + 1
        if count % 100 == 0:
            print(f"Processed {count} users")

    print(f"Found {len(result_list)} 'interesting' users (that have profiles) out of {count}")
    for user in result_list:
        grant = user.grant()
        print(f"{user.login_id} - '{user.first_name} {user.last_name}' - {len(grant.profiles_)} profile(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
