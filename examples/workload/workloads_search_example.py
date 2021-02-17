#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Example script showing VM Workloads Search operations.

Docs: https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/vm-workload-search/
"""

# Standard library imports
import sys

# Internal library imports
from cbc_sdk.helpers import build_cli_parser
from cbc_sdk.helpers import get_cb_cloud_object
from cbc_sdk.workload.vm_workloads_search import ComputeResource


def generate_menu():
    """Define console menu"""
    menu_content = {'0': {'name': 'M A I N - M E N U\n',
                          'function_call': main},
                    '1': {'name': 'Fetch Compute Resource by ID',
                          'function_call': fetch_compute_resource_by_id},
                    '2': {'name': 'Search and Facet Compute Resources',
                          'function_call': search_and_facet_compute_resources},
                    '9': {'name': 'Quit',
                          'function_call': quit_script}
                    }

    return menu_content


def user_input(menu):
    """Prompt user for menu choice"""
    print('-' * 21)
    for item in menu:
        print(f'{item}. {menu[item]["name"]}')

    choice = input('\nEnter your choice: ')
    while choice not in str(menu.keys()):
        choice = input('Enter a valid choice: ')

    return choice


def quit_script(cbc, menu, parser):
    """Quits script"""
    sys.exit()


def fetch_compute_resource_by_id(cbc, menu, parser):
    """Creates Fetch Compute Resource by ID SDK call"""
    event_id = None
    while not event_id:
        event_id = input('\nPlease provide ID for the compute resource: ').strip()
        try:
            event_id = int(event_id)
        except ValueError:
            event_id = None
            print('\nERR: ID must be integer!')

    print(cbc.select(ComputeResource, event_id))
    print('-' * 79)
    new_query = input('\nMake anothery query? Y/n\n')
    if new_query.lower() in ['y', 'yes']:
        fetch_compute_resource_by_id(cbc, menu, parser)
    else:
        menu['0']['function_call']()


def search_and_facet_compute_resources(cbc, menu, parser):
    """Creates Search and Facet Compute Resources SDK call"""
    print('\n' + '-' * 21)
    print('Available criteria filters:\n')
    print(*('appliance_uuid', 'eligibility', 'cluster_name', 'name',
            'ip_address', 'installation_status', 'uuid', 'os_type',
            'os_architecture'), sep='\n')
    print('-' * 21)

    query = cbc.select(ComputeResource)

    use_filter = input('\nWould you like to use criteria filters?: Y/n\n')
    if use_filter.lower() in ['y', 'yes']:
        print('Each criteria accepts one or more space separated values.',
              'Exmaple: --name ABCD --appliance_uuid 1234 5678')
        args = parser.parse_args(input('Enter criteria filters: ').split())
        if args.name:
            query.set_name(args.name)
        if args.os_type:
            query.set_os_type(args.os_type)
        if args.appliance_uuid:
            query.set_appliance_uuid(args.appliance_uuid)
        if args.cluster_name:
            query.set_cluster_name(args.cluster_name)
        if args.ip_address:
            query.set_ip_address(args.ip_address)
        if args.installation_status:
            query.set_installation_status(args.installation_status)
        if args.uuid:
            query.set_uuid(args.uuid)
        if args.os_architecture:
            query.set_os_architecture(args.os_architecture)
        if args.eligibility:
            query.set_eligibility(args.eligibility)

    print(*query)
    new_query = input('\nMake anothery query? Y/n\n')
    if new_query.lower() in ['y', 'yes']:
        search_and_facet_compute_resources(cbc, menu, parser)
    else:
        menu['0']['function_call']()


def main(cbc=None, menu=None, parser=None):
    """Script entry point"""
    # Initiate argparser
    parser = build_cli_parser()
    parser.add_argument('--appliance_uuid', nargs='+')
    parser.add_argument('--eligibility', nargs='+')
    parser.add_argument('--cluster_name', nargs='+')
    parser.add_argument('--name', nargs='+')
    parser.add_argument('--ip_address', nargs='+')
    parser.add_argument('--installation_status', nargs='+')
    parser.add_argument('--uuid', nargs='+')
    parser.add_argument('--os_type', nargs='+')
    parser.add_argument('--os_architecture', nargs='+')
    args = parser.parse_args()

    # Create cbc Instance
    cbc = get_cb_cloud_object(args)

    # Generate menu
    menu = generate_menu()

    # Get user menu choice
    user_choice = user_input(menu)

    # Call user specified sdk call
    menu[user_choice]['function_call'](cbc, menu, parser)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
