#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Registry setup helper script"""

import sys
import argparse
import winreg
from cbc_sdk.credentials import CredentialValue


DEFAULT_KEYPATH = 'Software\\VMware Carbon Black\\Cloud Credentials'


# Set up the argument parser
cmdline_parser = argparse.ArgumentParser()

group_location = cmdline_parser.add_argument_group('Location',
                                                   'Specify the location in the Registry to write credentials data.')
group_location.add_argument('-M', '--machine', action='store_true',
                            help='Write registry entries under HKEY_LOCAL_MACHINE instead of HKEY_CURRENT_USER. '
                            'Requires running with elevated privileges.')
group_location.add_argument('-B', '--base-key', action='store', default=DEFAULT_KEYPATH,
                            help='The base registry key that credential sections are written to.')
group_location.add_argument('-s', '--section', action='store', required=True,
                            help='The section to store credential values into (required parameter).')

group_values = cmdline_parser.add_argument_group('Values', 'Specify credential values to be written to the Registry.')
group_values.add_argument('-u', '--url', action='store', help='The URL used to access the Carbon Black Cloud.')
group_values.add_argument('-t', '--token', action='store',
                          help='The access token to be used to authenticate to the server.')
group_values.add_argument('-k', '--orgkey', action='store',
                          help='The organization key specifying which organization to work with.')
group_values.add_argument('--ssl-verify', action='store_true', help='Validate the SSL connection.')
group_values.add_argument('--no-ssl-verify', action='store_true', help='Do not validate the SSL connection.')
group_values.add_argument('--ssl-verify-hostname', action='store_true',
                          help='Verify the host name of the server being connected to.')
group_values.add_argument('--no-ssl-verify-hostname', action='store_true',
                          help='Do not verify the host name of the server being connected to.')
group_values.add_argument('--ssl-cert-file', action='store',
                          help='Certificate file used to validate the certificates of the SSL connection.')
group_values.add_argument('--force-tls12', action='store_true', help='Force the connection to use TLS 1.2.')
group_values.add_argument('--no-force-tls12', action='store_true', help='Do not force the connection to use TLS 1.2.')
group_values.add_argument('--proxy', action='store', help='Name of a proxy host to be used in making the connection.')
group_values.add_argument('--ignore-system-proxy', action='store_true',
                          help='Ignore system proxy settings when connecting to the server.')
group_values.add_argument('--no-ignore-system-proxy', action='store_true',
                          help='Do not ignore system proxy settings when connecting to the server.')

group_cmd = cmdline_parser.add_mutually_exclusive_group()
group_cmd.add_argument('-C', '--create', action='store_true',
                       help='Create any required Registry keys if they do not exist.')
group_cmd.add_argument('-l', '--list', action='store_true', help='List current credential values in this section.')
group_cmd.add_argument('-d', '--delete', action='store_true', help='Delete this configuration section.')


def open_base_key(opts, writable=True):
    """
    Opens the base key for all Registry storage of credentials.

    Args:
        opts (Namespace): Options passed to the utility.
        writable (bool): True if the key should be opened as writable, False if read-only.

    Returns:
        PyHKEY: The handle to the key.
    """
    access_rights = winreg.KEY_READ
    if writable:
        access_rights |= winreg.KEY_WRITE
    root_key = winreg.HKEY_LOCAL_MACHINE if opts.machine else winreg.HKEY_CURRENT_USER
    if (opts.create or opts.delete) and writable:
        return winreg.CreateKeyEx(root_key, opts.base_key, 0, access_rights)
    else:
        return winreg.OpenKeyEx(root_key, opts.base_key, 0, access_rights)


def open_section_key(opts, base_key, writable=True):
    """
    Opens the key corresponding to the credentials section.

    Args:
        opts (Namespace): Options passed to the utility.
        base_key (PyHKEY): The handle to the base key for all credential sections.
        writable (bool): True if the key should be opened as writable, False if read-only.

    Returns:
        PyHKEY: The handle to the key.
    """
    access_rights = winreg.KEY_READ
    if writable:
        access_rights |= winreg.KEY_WRITE
    if opts.create and writable:
        return winreg.CreateKeyEx(base_key, opts.section, 0, access_rights)
    else:
        return winreg.OpenKeyEx(base_key, opts.section, 0, access_rights)


def list_contents(opts):
    """
    Lists the contents of the specified section.

    Args:
        opts (Namespace): Options passed to the utility.
    """
    with open_base_key(opts, False) as base_key:
        with open_section_key(opts, base_key, False) as section_key:
            info = winreg.QueryInfoKey(section_key)
            for i in range(info[1]):
                value = winreg.EnumValue(section_key, i)
                if value[0].upper() in CredentialValue.__members__:
                    if value[2] == winreg.REG_SZ:
                        print(f"{value[0]}: {value[1]}")
                    elif value[2] == winreg.REG_DWORD:
                        print(f"{value[0]}: {value[1] != 0}")
                    else:
                        print(f"{value[0]}: ** error - unknown data type")


def delete_section(opts):
    """
    Deletes a credentials section.

    Args:
        opts (Namespace): Options passed to the utility.
    """
    with open_base_key(opts) as base_key:
        winreg.DeleteKey(base_key, opts.section)


def write_section(opts, data):
    """
    Writes the data for a credentials section.

    Args:
        opts (Namespace): Options passed to the utility.
        data (dict): Contains the data to be written, indexed by CredentialValue.
    """
    with open_base_key(opts) as base_key:
        with open_section_key(opts, base_key) as section_key:
            for k in list(CredentialValue):
                if k in data:
                    if k.requires_boolean_value():
                        winreg.SetValueEx(section_key, k.name.lower(), 0, winreg.REG_DWORD, 1 if data[k] else 0)
                    elif data[k]:
                        winreg.SetValueEx(section_key, k.name.lower(), 0, winreg.REG_SZ, data[k])
                    else:
                        winreg.DeleteValue(section_key, k.name.lower())


def gather_boolean(opts, data, index, true_attr, false_attr):
    """
    Gathers a Boolean data value into the data dict.

    Args:
        opts (Namespace): Options passed to the utility.
        data (dict): Data being collected.
        index (CredentialValue): Index of credential value to be set.
        true_attr (str): Attribute that must be set in opts to store a True value.
        false_attr (str): Attribute that must be set in opts to store a False value.
    """
    if vars(opts)[true_attr]:
        data[index] = True
    elif vars(opts)[false_attr]:
        data[index] = False


def gather_section_data(opts):
    """
    Gather the data from the command-line arguments into a dict that can be written to the Registry.

    Args:
        opts (Namespace): Options passed to the utility.

    Returns:
        dict: Collected data for the credentials to be written.
    """
    data = {}
    if opts.url:
        data[CredentialValue.URL] = opts.url
    if opts.token:
        data[CredentialValue.TOKEN] = opts.token
    if opts.orgkey:
        data[CredentialValue.ORG_KEY] = opts.orgkey
    gather_boolean(opts, data, CredentialValue.SSL_VERIFY, 'ssl_verify', 'no_ssl_verify')
    gather_boolean(opts, data, CredentialValue.SSL_VERIFY_HOSTNAME, 'ssl_verify_hostname', 'no_ssl_verify_hostname')
    if opts.ssl_cert_file:
        data[CredentialValue.SSL_CERT_FILE] = opts.ssl_cert_file
    gather_boolean(opts, data, CredentialValue.SSL_FORCE_TLS_1_2, 'force_tls12', 'no_force_tls12')
    if opts.proxy:
        data[CredentialValue.PROXY] = opts.proxy
    gather_boolean(opts, data, CredentialValue.IGNORE_SYSTEM_PROXY, 'ignore_system_proxy', 'no_ignore_system_proxy')
    return data


def main(args):
    """
    Process command-line input to the utility.

    Args:
        args (list): Command-line input to the utility.
    """
    opts = cmdline_parser.parse_args(args)
    if opts.list:
        list_contents(opts)
    elif opts.delete:
        delete_section(opts)
    else:
        write_section(opts, gather_section_data(opts))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
