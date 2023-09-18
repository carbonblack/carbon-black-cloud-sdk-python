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

"""Example script which manipulates rules in the Data Collection component of policy.

There are three methods that demonstrate interactions with the Data Collection Policy.
The first prints summary information about each policy, and iterates through each data_collection rule
This is an example of the command line to execute.
> python examples/platform/policy_data_collection.py --profile EXAMPLE_CREDENTIALS list_policies

The second method enables Auth Event collection (a type of data collection rule) on an existing policy.
Command line prompts ask for required info and defaults are provided.
This is an example of the command line to execute. The script will prompt on the command line for Policy Id.
> python examples/platform/policy_data_collection.py --profile EXAMPLE_CREDENTIALS enable_auth_event_rule

To disable an Auth Event policy,
> python examples/platform/policy_data_collection.py --profile EXAMPLE_CREDENTIALS disable_auth_event_rule

The API specification for underlying APIs is available on the Developer Network:
https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/policy-service/#rule-config---data-collection
"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Policy


def list_policy_summaries(cb):
    """List all policies and their rules."""
    # the cb.select(Policy) with no parameters will get all the policies for the organization
    for p in cb.select(Policy):
        print(u"Policy id {0}: {1} {2}".format(p.id, p.name, "({0})".format(p.description) if p.description else ""))
        print("Data Collection Rules:")
        if p.data_collection_rule_configs is None:
            print("No Data Collection Rules")
        elif len(p.data_collection_rule_configs_list) == 0:
            print("No Data Collection Rules")
        else:
            for dcrc in p.data_collection_rule_configs_list:
                print(dcrc)
                print("the schema for this data collection")
                print(p.get_ruleconfig_parameter_schema(dcrc.id))

        print("")
        print("End of Policy Object")
        print("")


def set_auth_event_rule(cb, enable_auth_events):
    """Enable the rule to collect Auth Events from the sensor"""
    # prompt the user for a policy Id
    user_input = input("Enter the policy Id on which to change auth event collection setting")
    policy = cb.select(Policy, user_input)
    print("Using policy id: {0}.  name: {1}".format(policy.id, policy.name))
    # If the policy does not have a data collection section then fail
    if len(policy.data_collection_rule_configs_list) == 0:
        print("No data collection elements available to enable")
        exit()

    auth_event_rule_config = None
    for dcrc in policy.data_collection_rule_configs_list:
        if dcrc.name == 'Authentication Events':
            dcrc.set_parameter('enable_auth_events', enable_auth_events)
            print(f"Auth Event Collection {'Enabled' if enable_auth_events else 'Disabled'}")
            dcrc.save()
            auth_event_rule_config = dcrc

    if auth_event_rule_config is not None:
        print(auth_event_rule_config)
    else:
        print("Auth Event Rule Config Element Not Found")


def main():
    """Main function for Policy - Host-Based Firewall script."""
    parser = build_cli_parser("View or set host based firewall rules on a policy")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list_policies", help="List summary information about each policy")

    subparsers.add_parser("enable_auth_event_rule", help="Enable the data collection rule to get Auth Events")

    subparsers.add_parser("disable_auth_event_rule", help="Disable the data collection rule to get Auth Events")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.command == "list_policies":
        list_policy_summaries(cb)
    elif args.command == "enable_auth_event_rule":
        set_auth_event_rule(cb, True)
    elif args.command == "disable_auth_event_rule":
        set_auth_event_rule(cb, False)
    else:
        raise NotImplementedError("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
