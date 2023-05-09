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

The second method creates two new host-based firewall rules in a new rule group on an existing policy.
The name and description of the group are passed in on the command line, the rules are hard coded for
to make the example easier to read.
This is an example of the command line to execute where -p 12345678 specifies the policy to operate on
> python examples/platform/policy_host_based_firewall.py --profile EXAMPLE_CREDENTIALS -p 12345678 /
    create_rule --rule_group_name sdk_test_two --rule_group_desc sdk_test_two_desc
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


def add_hbfw_rule(cb, args):
    """Create a rule and add it to the rule group specified in the input args"""
    # get the policy specified in the input parameters
    policy = cb.select(Policy, args.policy)
    print("id: {0}.  name: {1}".format(policy.id, policy.name))
    # If the policy does not yet have a host-based firewall section then create it
    if policy.host_based_firewall_rule_config is None:
        policy.host_based_firewall_rule_config = HostBasedFirewallRuleConfig(cb, policy)

    # get the rule config in a variable to work with
    rc = policy.host_based_firewall_rule_config
    # create a new rule group
    rg = rc.new_rule_group(args.rule_group_name, args.rule_group_desc)
    # add the rule group to the rule config
    rc.append_rule_group(rg)  # to do remove this

    # create two rules
    # name = SDK Example Rule One, action = ALLOW, direction = IN, protocol = TCP, remote ip address = 15.16.17.18
    r1 = rc.new_rule("SDK Example Rule One", "ALLOW", "IN", "TCP", "15.16.17.18")
    # then set the rest of the fields in the rule
    r1.application_path = "C:\\sdk\\example\\allow\\rule\\path"
    r1.enabled = False
    r1.local_ip_address = "11.12.13.14"
    r1.local_port_ranges = "1313"
    r1.remote_port_ranges = "2121"
    # append the rule to the group
    rg.append_rule(r1)  # TO DO - remove this
    # create the second rule
    r2 = rc.new_rule("The second SDK Example Rule", "BLOCK", "OUT", "UDP", "5.6.7.8")
    # then set the rest of the fields in the rule
    r2.application_path = "C:\\another\\sdk\\example\\path"
    r2.enabled = True
    r2.local_ip_address = "1.2.3.4"
    r2.local_port_ranges = "3131"
    r2.remote_port_ranges = "1212"
    # append the rule to the group
    rg.append_rule(r2)  # TO DO - remove this
    # To do - either remove rc.save() if the policy.save() does the rules too or document that rule config must be saved
    rc.save()
    policy.save()
    print(rc)


def main():
    """Main function for Policy - Host-Based Firewall script."""
    parser = build_cli_parser("View or set host based firewall rules on a policy")
    parser.add_argument("-p", "--policy", type=int, required=False, help="The ID of the policy to be manipulated")
    subparsers = parser.add_subparsers(dest="command", required=True)

    policy_summaries = subparsers.add_parser("list_policies", help="List summary information about each policy")
    policy_summaries.add_argument("--all_details", help="Print core prevention and host-based firewall rules")

    create_rule = subparsers.add_parser("create_rule", help="Create a new Host-Based Firewall rule")
    create_rule.add_argument("--rule_group_name", help="The name of the rule group to hold the new rule")
    create_rule.add_argument("--rule_group_desc", help="The description of the new rule group")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.command == "list_policies":
        list_policy_summaries(cb, args)
    elif args.command == "create_rule":
        add_hbfw_rule(cb, args)
    else:
        raise NotImplementedError("Unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
