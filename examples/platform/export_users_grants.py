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

"""Export users with their grant information"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User, Grant


def main():
    parser = build_cli_parser('Export User and Grant Information')

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    # Obtain a list of users paired with their grants.
    user_query = cb.select(User);
    all_users = {user.urn: user for user in user_query}
    grant_query = cb.select(Grant)
    for user in all_users.values():
        grant_query.add_principal(user.urn, user.org_urn)
    paired_user_grants = [(all_users[g.principal], g) for g in grant_query if g.principal in all_users]

    # TODO: filter by role

    # TODO: sort?

    # TODO: extract data and give result

    return 0


if __name__ == "__main__":
    sys.exit(main())

