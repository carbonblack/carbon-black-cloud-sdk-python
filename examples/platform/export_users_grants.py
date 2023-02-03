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
import copy
import json
import csv
from io import StringIO
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import User, Grant


CSV_FIELDNAMES = ["login_id", "login_name", "email", "phone", "first_name", "last_name", "urn",
                  "grant_created", "grant_updated", "grant_created_by", "grant_updated_by", "roles", "profiles"]


def matches_roles(grant, roles):
    """
    Determines if the given grant matches any of the specified roles.

    Args:
        grant (Grant): A grant to be tested.
        roles (set[str]): A set of roles to test against.

    Returns:
        bool: True if the grant has any of the specified roles, False if not.
    """
    if grant.roles:
        if not set(grant.roles).isdisjoint(roles):
            return True
    if grant.profiles:
        for profile in grant.profiles:
            if profile.roles:
                if not set(profile.roles).isdisjoint(roles):
                    return True
    return False


def extract_row(user, grant):
    """
    Folds data from a User and a Grant into a single dict full of information.

    Args:
        user (User): The user to extract data from.
        grant (Grant): The grant to extract data from.

    Returns:
        dict: The dictionary containing data extracted from the User and the Grant.
    """
    rc = {"login_id": user.login_id, "login_name": user.login_name, "email": user.email, "phone": user.phone,
          "first_name": user.first_name, "last_name": user.last_name, "urn": user.urn,
          "grant_created": grant.create_time, "grant_updated": grant.update_time, "grant_created_by": grant.created_by,
          "grant_updated_by": grant.updated_by}
    roles = []
    profiles = []
    if grant.roles:
        roles.extend(grant.roles)
    if grant.profiles:
        for profile in grant.profiles:
            profiles.append(profile.profile_uuid)
            if profile.roles:
                roles.extend(profile.roles)
    rc["roles"] = roles
    rc["profiles"] = profiles
    return rc


def flatten_row(row):
    """
    "Flattens" the given row by turning its "roles" and "profiles" arrays into pipe-delimited text strings.

    Args:
        row (dict): The row to be flattened.

    Returns:
        dict: The flattened row.
    """
    rc = copy.deepcopy(row)
    rc["roles"] = "|".join(row["roles"])
    rc["profiles"] = "|".join(row["profiles"])
    return rc


def main():
    parser = build_cli_parser('Export User and Grant Information')
    parser.add_argument('-r', '--role', action='append', nargs='+',
                        help="If specified, users returned will match at least one of these roles.")
    parser.add_argument('-o', '--output',
                        help="File to output the exported data to; if not specified, standard output is used.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-J', '--json', action='store_true', help="Specifies output in JSON format (default).")
    group.add_argument('-C', '--csv', action='store_true', help="Specifies output in CSV format.")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.json:
        output_type = 'JSON'
    elif args.csv:
        output_type = 'CSV'
    else:
        output_type = 'JSON'

    # Obtain a list of users paired with their grants.
    user_query = cb.select(User);
    all_users = {user.urn: user for user in user_query}
    grant_query = cb.select(Grant)
    for user in all_users.values():
        grant_query.add_principal(user.urn, user.org_urn)
    paired_user_grants = [(all_users[g.principal], g) for g in grant_query if g.principal in all_users]

    # If specified, filter the list by roles.
    if args.roles:
        roleset = set(args.roles)
        output_list = filter(lambda p: matches_roles(p[1], roleset), paired_user_grants)
    else:
        output_list = paired_user_grants

    # extract data to JSON format
    data_list = list(map(lambda p: extract_row(p[0], p[1]), output_list))

    if output_type == 'JSON':
        if args.output:
            with open(args.output, "w") as f:
                f.write(json.dumps(data_list, indent=4))
        else:
            print(json.dumps(data_list, indent=4))
        return 0

    # handle CSV output from here
    rows_list = map(flatten_row, data_list)
    if args.output:
        with open(args.output, "w", newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDNAMES, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows_list)
    else:
        with StringIO('', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_FIELDNAMES, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows_list)
            print(stream.getvalue())

    return 0


if __name__ == "__main__":
    sys.exit(main())

