#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
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
import argparse
from types import MappingProxyType

# Internal library imports
from cbc_sdk.errors import ApiError
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.workload import VCenterComputeResource, AWSComputeResource


DOWNLOAD_MENU = MappingProxyType({
    '1': {'name': 'Comma-separated values (CSV) format', 'value': 'CSV'},
    '2': {'name': 'JSON format', 'value': 'JSON'}
})

CRITERIA_VCENTER = {
    'appliance-uuid': 'UUID of the appliance the VM is associated with',
    'cluster-name': 'Name of the cluster (group of hosts)',
    'datacenter-name': 'Name of the underlying datacenter (common container)',
    'esx-host-name': 'Name of the ESX host on which the VM is deployed',
    'esx-host-uuid': 'UUID of the ESX host on which VM is deployed',
    'vcenter-name': 'Name of the vcenter the VM is associated with',
    'vcenter-host-url': 'Hostname or IP address of the vcenter the VM is associated with',
    'vcenter-uuid': '128-bit SMBIOS UUID of a vcenter represented as a hexadecimal string',
    'name': 'Name of the compute resource',
    'host-name': 'DNS name associated with the compute resource',
    'ip-address': 'Current ip address assigned to the compute resource',
    'device-guid': 'Device GUID',
    'registration-id': 'Registration ID',
    'eligibility': 'Status indicator indicating whether a compute resource is capable of installing a CBC sensor',
    'eligibility-code': 'Reason messages for why a compute resource is not eligible',
    'installation-status': 'Current state of installing the Carbon Black Cloud sensor on the compute resource',
    'installation-type': 'Installation type',
    'uuid': 'Universally unique identifier for a compute resource',
    'os-description': 'Operating system, version, and architecture',
    'os-type': 'Type of operating system',
    'os-architecture': "Compute resource’s operating system architecture",
    'vmwaretools-version': 'Current version of VMware Tools installed in the compute resource'
}

CRITERIA_AWS = {
    'auto-scaling-group-name': 'Auto scaling group name',
    'availability-zone': 'AWS availability zone',
    'cloud-provider-account-id': 'Account id of the cloud provider',
    'cloud-provider-resource-id': 'Resource id assigned by cloud provider',
    'cloud-provider-tags': 'Cloud provider tags',
    'id': 'Identifier for the compute resource',
    'installation-status': 'Current state of installing the Carbon Black Cloud sensor on the compute resource',
    'name': 'Name of the compute resource',
    'platform': 'Platform',
    'platform-details': 'Platform details',
    'region': 'AWS region',
    'subnet-id': 'Subnet ID',
    'virtual-private-cloud-id': 'Virtual private cloud ID'
}

FACET_FIELDS_VCENTER = ('eligibility', 'installation_status', 'vmwaretools_version', 'os_type')
FACET_FIELDS_AWS = ('auto_scaling_group_name', 'cloud_provider_tags', 'platform', 'platform_details',
                    'virtual_private_cloud_id')

SUMMARY_FIELDS_AWS = ('availability_zone', 'region', 'subnet_id', 'virtual_private_cloud_id', 'security_group_id')


def resource_class_for_mode(mode):
    """Returns the correct resource class for the mode."""
    if mode == 'VCENTER':
        return VCenterComputeResource
    elif mode == 'AWS':
        return AWSComputeResource
    else:
        raise NotImplementedError(f"mode {mode} not implemented!")


def criteria_dict_for_mode(mode):
    """Returns the correct criteria dictionary for the mode."""
    if mode == 'VCENTER':
        return MappingProxyType(CRITERIA_VCENTER)
    elif mode == 'AWS':
        return MappingProxyType(CRITERIA_AWS)
    else:
        raise NotImplementedError(f"mode {mode} not implemented!")


def facet_fields_for_mode(mode):
    """Returns the correct list of facet fields for the mode."""
    if mode == 'VCENTER':
        return FACET_FIELDS_VCENTER
    elif mode == 'AWS':
        return FACET_FIELDS_AWS
    else:
        raise NotImplementedError(f"mode {mode} not implemented!")


def summary_fields_for_mode(mode):
    """Returns the correct list of summary fields for the mode."""
    if mode == 'VCENTER':
        raise NotImplementedError("vCenter mode does not implement the summarize() function")
    elif mode == 'AWS':
        return SUMMARY_FIELDS_AWS
    else:
        raise NotImplementedError(f"mode {mode} not implemented!")


def print_available_criteria(mode):
    """Prints the available search criteria for each mode."""
    print('\n' + '-' * 21)
    print('Available criteria filters:\n')
    for flag, descr in criteria_dict_for_mode(mode).items():
        print(f"  {flag} - {descr}")
    print('\nFor each flag X, use the option --X to include values of that field,')
    print('  or use the option --exclude-X to exclude values of that field.')
    print('Each criteria flag accepts one or more space separated values.',
          'Example: --name ABCD --appliance-uuid 1234 5678')
    print('-' * 21)


def criteria_parser_for_mode(mode):
    """Return a criteria parser object for the current mode."""
    parser = argparse.ArgumentParser(description=f"Criteria parser for {mode}")
    for flag, descr in criteria_dict_for_mode(mode).items():
        parser.add_argument(f"--{flag}", nargs='+', help=descr)
        parser.add_argument(f"--exclude-{flag}", nargs='+', help=f"Exclude: {descr}")
    return parser


def map_criteria_to_query(mode, query, args):
    """Map the parsed criteria arguments into the query depending on the mode."""
    parsed_values = vars(args)
    # This relies on the fact that each criteria name X has a set_X() and exclude_X() method on the query object,
    # with dashes in the criteria name replaced by underscores.  This allows us to reflect on the query class to find
    # the appropriate method to use.
    # The other way of doing this would be with a big sequence of if...elif...elif statements to check the value names,
    # but that would quickly become cumbersome with the number of attributes we have, and as new workload types are
    # added in the future.
    for value_name in [flag.replace('-', '_') for flag in criteria_dict_for_mode(mode).keys()]:
        if parsed_values[value_name]:
            f = getattr(query.__class__, f"set_{value_name}")
            f(query, parsed_values[value_name])
        if parsed_values[f"exclude_{value_name}"]:
            f = getattr(query.__class__, f"exclude_{value_name}")
            f(query, parsed_values[f"exclude_{value_name}"])


def build_main_menu(mode):
    """Create the main menu given the script operating mode."""
    menu = {
        '1': {'name': 'Fetch Compute Resource By ID',
              'function': lambda cbc, m: loop_calling_multiply(cbc, m, fetch_by_id, "Make another query?")},
        '2': {'name': 'Search for Compute Resources',
              'function': lambda cbc, m: loop_calling_multiply(cbc, m, search_resources, "Run another search?")},
        '3': {'name': 'Facet Compute Resources',
              'function': lambda cbc, m: loop_calling_multiply(cbc, m, facet_resources, "Run another faceting?")},
        '4': {'name': 'Download Compute Resources List',
              'function': lambda cbc, m: loop_calling_multiply(cbc, m, download_resources, "Download another list?")},
        '9': {'name': 'Quit', 'function': quit_script}
    }
    if mode == 'AWS':
        menu['5'] = {'name': 'Summarize Compute Resources',
                     'function': lambda cbc, m: loop_calling_multiply(cbc, m, summarize_resources,
                                                                      "Run another summary?")}
    return MappingProxyType(menu)


def fetch_by_id(cbc, mode):
    """Execute the "fetch resource by ID" function."""
    resource_id = None
    # prompt for the resource ID
    while not resource_id:
        resource_id = input(f"\nPlease provide ID for the {mode} compute resource: ").strip()
        try:
            resource_id = int(resource_id)
        except ValueError:
            resource_id = None
            print('\nERROR: ID must be integer!')

    try:
        # select the appropriate class (VCenterComputeResource or AWSComputeResource) with the resource ID
        print(cbc.select(resource_class_for_mode(mode), resource_id))
    except ApiError as e:
        print("\nERROR: Query of resource failed!")
        print(e)
    print('-' * 79)
    return True


def search_resources(cbc, mode):
    """Execute the "search resources" function."""
    print_available_criteria(mode)

    # set up a query on the appropriate class (VCenterComputeResource or AWSComputeResource)
    query = cbc.select(resource_class_for_mode(mode))

    # prompt for and apply criteria filters where desired
    use_filter = input('\nWould you like to use criteria filters?: Y/n\n')
    if use_filter.lower() in ('y', 'yes'):
        parser = criteria_parser_for_mode(mode)
        args = parser.parse_args(input("Enter criteria filters: ").split())
        try:
            map_criteria_to_query(mode, query, args)
        except ApiError as e:
            print("\nERROR: Mapping resources to criteria failed")
            print(e)
            return True

    try:
        # read in the query results and dump them to output
        for item in query:
            print(item)
            print('-' * 79)
        print(f"Total items returned: {query._count()}")
        print('-' * 79)
    except ApiError as e:
        print("\nERROR: Resource search failed")
        print(e)

    return True


def facet_resources(cbc, mode):
    """Execute the "facet resources" function."""
    print_available_criteria(mode)

    # set up a query on the appropriate class (VCenterComputeResource or AWSComputeResource)
    query = cbc.select(resource_class_for_mode(mode))

    # prompt for and apply criteria filters where desired
    use_filter = input('\nWould you like to use criteria filters?: Y/n\n')
    if use_filter.lower() in ('y', 'yes'):
        parser = criteria_parser_for_mode(mode)
        args = parser.parse_args(input("Enter criteria filters: ").split())
        try:
            map_criteria_to_query(mode, query, args)
        except ApiError as e:
            print("\nERROR: Mapping resources to criteria failed")
            print(e)
            return True

    print(f"\nAvailable facet fields: {facet_fields_for_mode(mode)}")
    print("Specify field names to use, separated by spaces. At least one must be specified.")

    # get the list of fields to facet on
    facet_fields = None
    while not facet_fields:
        facet_fields = list(input("Enter facet field names: ").split())
        if len(facet_fields) == 0:
            facet_fields = None
            print("\nERROR: At least one facet field must be specified")

    try:
        # facet and print results
        for facet_object in query.facet(facet_fields, 100):
            print(facet_object)
            print('-' * 79)
    except ApiError as e:
        print("\nERROR: Resource faceting failed")
        print(e)

    return True


def download_resources(cbc, mode):
    """Execute the "download resources" function."""
    print_available_criteria(mode)

    # set up a query on the appropriate class (VCenterComputeResource or AWSComputeResource)
    query = cbc.select(resource_class_for_mode(mode))

    # prompt for and apply criteria filters where desired
    use_filter = input('\nWould you like to use criteria filters?: Y/n\n')
    if use_filter.lower() in ('y', 'yes'):
        parser = criteria_parser_for_mode(mode)
        args = parser.parse_args(input("Enter criteria filters: ").split())
        try:
            map_criteria_to_query(mode, query, args)
        except ApiError as e:
            print("\nERROR: Mapping resources to criteria failed")
            print(e)
            return True

    # get the download format to use
    print("\n\n--------------------Download Format:\n")
    for key in sorted(DOWNLOAD_MENU.keys()):
        print(f"{key}. {DOWNLOAD_MENU[key]['name']}")
    print('\n')

    choice = input('\nEnter your choice: ')
    while choice not in str(DOWNLOAD_MENU.keys()):
        choice = input('Enter a valid choice: ')

    try:
        # set up the download job
        job = query.download(DOWNLOAD_MENU[choice]['value'])
        # wait for the download job to finish and then print its results
        print("Waiting for job to complete...")
        job.await_completion()
        print(job.get_output_as_string())
        print('-' * 79)
    except ApiError as e:
        print("\nERROR: Download operation failed")
        print(e)
    return True


def summarize_resources(cbc, mode):
    """Execute the "summarize resources" function."""
    print_available_criteria(mode)

    # set up a query on the appropriate class (VCenterComputeResource or AWSComputeResource)
    # N.B.: only AWSComputeResource implements summarize at this time
    query = cbc.select(resource_class_for_mode(mode))

    # prompt for and apply criteria filters where desired
    use_filter = input('\nWould you like to use criteria filters?: Y/n\n')
    if use_filter.lower() in ('y', 'yes'):
        parser = criteria_parser_for_mode(mode)
        args = parser.parse_args(input("Enter criteria filters: ").split())
        try:
            map_criteria_to_query(mode, query, args)
        except ApiError as e:
            print("\nERROR: Mapping resources to criteria failed")
            print(e)
            return True

    print(f"\nAvailable summary fields: {summary_fields_for_mode(mode)}")
    print("Specify field names to use, separated by spaces. At least one must be specified.")

    # get the list of fields to summarize on
    summary_fields = None
    while not summary_fields:
        summary_fields = list(input("Enter summary field names: ").split())
        if len(summary_fields) == 0:
            summary_fields = None
            print("\nERROR: At least one summary field must be specified")

    try:
        # run the summary and print the results
        for field, count in query.summarize(summary_fields).items():
            print(f"{field}: {count} total")
    except ApiError as e:
        print("\nERROR: Resource summary failed")
        print(e)

    return True


def loop_calling_multiply(cbc, mode, subfunction, prompt):
    """Run a particular menu function multiple times, prompting to run again after each one."""
    rc = True
    is_running = True
    while is_running:
        rc = subfunction(cbc, mode)
        if rc:
            new_query = input(f"\n{prompt} Y/n\n")
            if new_query.lower() not in ('y', 'yes'):
                is_running = False
        else:
            is_running = False
    return rc


def quit_script(cbc, mode):
    """Function which quits the script."""
    print("Bye")
    return False


def main():
    """Ye Olde Main Function"""
    # Initiate argparser
    parser = build_cli_parser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--vcenter', action='store_true', help='Work with vCenter compute resources (default)')
    group.add_argument('--aws', action='store_true', help='Work with AWS compute resources')
    args = parser.parse_args()

    if args.vcenter:
        mode = 'VCENTER'
    elif args.aws:
        mode = 'AWS'
    else:
        mode = 'VCENTER'

    # Create cbc Instance
    cbc = get_cb_cloud_object(args)

    menu = build_main_menu(mode)

    is_running = True
    while is_running:
        # Print the menu
        print("\n\n--------------------Main Menu:\n")
        for key in sorted(menu.keys()):
            print(f"{key}. {menu[key]['name']}")
        print('\n')

        # Get choice
        choice = input('\nEnter your choice: ')
        while choice not in str(menu.keys()):
            choice = input('Enter a valid choice: ')

        # Execute choice
        is_running = menu[choice]['function'](cbc, mode)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
