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

"""Example script retrieving process events."""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.endpoint_standard import EnrichedEvent


def parse_key_value_pairs(kvlist):
    """Parse the key=value strings into a dict of lists of values"""
    output = {}
    if kvlist:
        for kvpair in kvlist:
            (key, value) = kvpair.split('=')
            if not (key and value):
                raise RuntimeError(f"invalid exclusion specified: {kvpair}")
            if key in output:
                output[key].append(value)
            else:
                output[key] = [value]
    return output


def main():
    """Main function of the process events script."""
    parser = build_cli_parser()
    parser.add_argument("--query", "-q", type=str, help="Query string for the search", default=None)
    parser.add_argument("--include", "-i", action='append', type=str,
                        help="Specifies included event field values, as key=value")
    parser.add_argument("--exclude", "-x", action='append', type=str,
                        help="Specifies excluded event field values, as key=value")
    parser.add_argument("--fields", "-f", action='append', type=str, help="Specifies names of fields to include")
    parser.add_argument("--numrows", "-n", type=int, help="Maximum number of rows to be returned", default=None)
    parser.add_argument("--group", "-g", type=str, help="Field to group by, either device_id or process_sha256",
                        default=None)
    parser.add_argument("--timeout", "-T", type=int, help="Timeout for the search in milliseconds", default=None)

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    query = cb.select(EnrichedEvent)
    if args.query:
        query.where(args.query)
    inclusions = parse_key_value_pairs(args.include)
    for (key, value) in inclusions:
        query.update_criteria(key, value)
    exclusions = parse_key_value_pairs(args.exclude)
    for (key, value) in exclusions:
        query.add_exclusion(key, value)
    if args.fields:
        query.set_fields(args.fields)
    if args.numrows:
        query.set_rows(args.numrows)
    if args.group:
        query.aggregation(args.group)
    if args.timeout:
        query.timeout(args.timeout)

    separator = False
    for event in query:
        if separator:
            print("------------------------------------------------------------------------\n")
        separator = True
        print(f"{event}\n")


if __name__ == "__main__":
    sys.exit(main())
