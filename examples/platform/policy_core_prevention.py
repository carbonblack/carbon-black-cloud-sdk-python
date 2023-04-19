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

"""Example script which sends control messages to devices."""

import sys
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Policy


def list_core_prevention_status(policy):
    rule_configs = [config for config in policy.object_rule_configs_list if config.category == "core_prevention"]
    for config in sorted(rule_configs, key=lambda c: c.name):
        print(f"{config.name} = {config.get_assignment_mode()}")


def set_core_prevention_status(policy, config_name, mode):
    if mode not in ('BLOCK', 'REPORT'):
        raise RuntimeError(f"unknown assignment mode '{mode}'")
    match_name = config_name.casefold()
    rule_configs = [config for config in policy.object_rule_configs_list
                    if config.category == "core_prevention" and config.name.casefold().startswith(match_name)]
    if not rule_configs:
        raise RuntimeError(f"core prevention rule config '{config_name}' not found")
    elif len(rule_configs) > 1:
        raise RuntimeError(f"ambiguous core prevention rule config name '{config_name}', "
                           f"possible values are {[c.name for c in rule_configs]}")
    rule_configs[0].set_assignment_mode(mode)
    rule_configs[0].save()
    print(f"{rule_configs[0].name} = {mode}")


def main():
    """Main function for Device Actions script."""
    parser = build_cli_parser("View or set core prevention settings on a policy")
    parser.add_argument("-p", "--policy", type=int, required=True, help="The ID of the policy to be manipulated")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all core prevention statuses")

    set_command = subparsers.add_parser("set", help="Set a core prevention status")
    set_command.add_argument("config", help="The core prevention configuration to change")
    set_command.add_argument("mode", choices=["BLOCK", "REPORT"], help="The new assignment mode to set")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)
    policy = cb.select(Policy, args.policy)

    if args.command == "list":
        list_core_prevention_status(policy)
    elif args.command == "set":
        set_core_prevention_status(policy, args.config, args.mode)
    else:
        raise NotImplementedError("Unknown command")


if __name__ == "__main__":
    sys.exit(main())
