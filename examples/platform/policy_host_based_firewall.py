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

"""Example script which manipulates rules in the Host-Based Firewall component of policy.

There are two methods that demonstrate interactions with the Host-Based Firewall Policy.
The first prints summary information about each policy, and optionally iterates through each core
prevention and host-based firewall rules.
This is an example of the command line to execute.  --all_details True will include the rules.
> python examples/platform/policy_host_based_firewall.py --profile EXAMPLE_CREDENTIALS --all_details True

The second method creates new host-based firewall rules in a new rule group on an existing policy.
Command line prompts ask for required info and defaults are provided.
This is an example of the command line to execute. The script will prompt on the command line for Policy Id.
> python examples/platform/policy_host_based_firewall.py --profile EXAMPLE_CREDENTIALS create_rule
"""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Policy
from cbc_sdk.platform.policies import HostBasedFirewallRuleConfig


def list_policy_summaries(cb, args):
    """List all policies and their rules."""
    # the cb.select(Policy) with no parameters will get all the policies for the organization
    for p in cb.select(Policy):
        print(u"Policy id {0}: {1} {2}".format(p.id, p.name, "({0})".format(p.description) if p.description else ""))
        print("Rules:")
        # the command line argument of "--all_details" is used here
        if args.all_details:
            for r in p.rules:
                print("  {0}: {1} when {2} {3} is {4}".format(r.get("id"), r.get("action"),
                                                              r.get("application", {}).get("type"),
                                                              r.get("application", {}).get("value"),
                                                              r.get("operation")))
            print("Core Prevention")
            if p.core_prevention_rule_configs is None:
                print("No Core Prevention Rules")
            else:
                if args.all_details:
                    for cprc in p.core_prevention_rule_configs.values():
                        print(" {0}".format(cprc.name))
        else:
            print("Details not requested.")

        print("Host-Based Firewall")
        if p.host_based_firewall_rule_config is None:
            print("No Host-Based Firewall Rules")
        else:
            if args.all_details:
                hbfwr = p.host_based_firewall_rule_config
                print("Rule config name: {0}".format(hbfwr.name))
                if hbfwr.rule_groups is None:
                    print("No rule groups")
                else:
                    for rg in hbfwr.rule_groups:
                        print("Rule Group Name: {0}".format(rg.name))
                        if rg.rules is None:
                            print("No rules")
                        else:
                            for r in rg.rules:
                                print("rule: {0}".format(r))
            else:
                print("Details not requested.")

        print("")
        print("End of Policy Object")
        print("")


def add_hbfw_rule(cb):
    """Create a rule and add it to the rule group specified in the input args"""
    # prompt the user for a policy Id
    user_input = input("Enter the policy Id to add a rule group and rules to")
    policy = cb.select(Policy, user_input)
    print("Using policy id: {0}.  name: {1}".format(policy.id, policy.name))
    # If the policy does not yet have a host-based firewall section then create it
    if policy.host_based_firewall_rule_config is None:
        policy.host_based_firewall_rule_config = HostBasedFirewallRuleConfig(cb, policy)

    # get the rule config in a variable to work with
    rc = policy.host_based_firewall_rule_config
    # create a new rule group
    rule_group_name = "Demo Rule Group"
    rule_group_desc = "Description of Demo Rule Group"
    user_input = input("Creating a rule group.  Enter a name for the rule group or press Enter to use the default of {}"
                       .format(rule_group_name))
    if user_input:
        rule_group_name = user_input

    user_input = input("Enter a description for the rule group press Enter to use the default of {}"
                       .format(rule_group_desc))
    if user_input:
        rule_group_desc = user_input

    rg = rc.append_rule_group(rule_group_name, rule_group_desc)
    create_rule = True
    while create_rule:
        # prompt the user to enter rule config or use defaults
        # Set default values
        rule_name = "SDK Example Rule"
        rule_action = "ALLOW"
        direction = "IN"
        protocol = "TCP"
        application_path = "C:\\sdk\\example\\allow\\rule\\path"
        enabled = False
        remote_ip_address = "15.16.17.18"
        local_ip_address = "11.12.13.14"
        local_port_ranges = "1313"
        remote_port_ranges = "2121"

        # prompt user to enter values
        user_input = input("Enter Rule Name or press Enter to use the default of {}".format(rule_name))
        if user_input:
            rule_name = user_input

        user_input = input("Enter Rule Action (ALLOW or BLOCK) or press Enter to use the default of {}"
                           .format(rule_action))
        if user_input:
            rule_action = user_input.upper()

        user_input = input("Set Direction (IN or OUT)or press Enter to use the default of {}".format(direction))
        if user_input:
            direction = user_input.upper()

        user_input = input("Set Protocol or press Enter to use the default of {}".format(protocol))
        if user_input:
            protocol = user_input.upper()

        user_input = input("Enter the application path or press Enter use default of {}".format(application_path))
        if user_input:
            application_path = user_input

        user_input = input("Enter T for the rule to be enabled or press Enter to use the default of disabled")
        if user_input:
            enabled = True

        user_input = input("Enter the Remote IP Address or press Enter to use the default of {}"
                           .format(remote_ip_address))
        if user_input:
            remote_ip_address = user_input

        user_input = input("Enter the Local IP Address or press Enter to use the default of {}"
                           .format(local_ip_address))
        if user_input:
            local_ip_address = user_input

        user_input = input("Enter the Remote port range or press Enter to use the default of {}"
                           .format(remote_port_ranges))
        if user_input:
            remote_port_ranges = user_input

        user_input = input("Enter the Local port range or press Enter to use the default of {}"
                           .format(local_port_ranges))
        if user_input:
            local_port_ranges = user_input

        rule = rg.append_rule(rule_name, rule_action, direction, protocol, remote_ip_address)
        # then set the rest of the fields in the rule
        rule.application_path = application_path
        rule.enabled = enabled
        rule.local_ip_address = local_ip_address
        rule.local_port_ranges = local_port_ranges
        rule.remote_port_ranges = remote_port_ranges

        create_rule = False
        user_input = input("Enter Y to create another rule.  Press Enter to finish and save.")
        if user_input:
            if user_input == "Y":
                create_rule = True

    # There is a known issue in Carbon Black Cloud that requires the rule_configs to be saved explicitly.
    # There is no adverse impact to performing this call but in the future will be un-necessary
    # rc.save()
    # save the policy and all child elements.
    policy.save()
    print(rc)


def main():
    """Main function for Policy - Host-Based Firewall script."""
    parser = build_cli_parser("View or set host based firewall rules on a policy")
    subparsers = parser.add_subparsers(dest="command", required=True)

    policy_summaries = subparsers.add_parser("list_policies", help="List summary information about each policy")
    policy_summaries.add_argument("--all_details", help="Print core prevention and host-based firewall rules")

    subparsers.add_parser("create_rule", help="Create a new Host-Based Firewall rule")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.command == "list_policies":
        list_policy_summaries(cb, args)
    elif args.command == "create_rule":
        add_hbfw_rule(cb)
    else:
        raise NotImplementedError("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
