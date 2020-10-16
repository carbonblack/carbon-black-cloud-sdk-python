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

"""Credential helper"""

import argparse
import contextlib
import configparser

import os
import sys
from io import StringIO as StringIO

try:
    import winreg
    HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
    CreateKeyEx = winreg.CreateKeyEx
    SetValueEx = winreg.SetValueEx
except ModuleNotFoundError:
    HKEY_CURRENT_USER = object()

    def CreateKeyEx(base, path, reserved, access_rights):
        """Stub to maintain source compatibility"""
        return None

    def SetValueEx(key, name, reserved, type, value):
        """Stub to maintain source compatibility"""
        return None

# Define these constants locally so they don't depend on winreg. From the Windows Registry API docs.
REG_SZ = 1
REG_DWORD = 4
KEY_WRITE = 0x20006


DEFAULT_KEYPATH = 'Software\\VMware Carbon Black\\Cloud Credentials\\default'


@contextlib.contextmanager
def temp_umask(umask):
    """Temporary unmask"""
    oldmask = os.umask(umask)
    try:
        yield
    finally:
        os.umask(oldmask)


def configure_windows(opts):
    """Configure the Registry"""
    if not sys.platform.startswith("win32"):
        print("Cannot configure registry on a non-Windows system")
        return

    print("Welcome to the cbc_sdk for Windows.")

    url = input("URL to the Carbon Black Cloud API server (do not include '/integrationServices') [https://hostname]: ")

    ssl_verify = True

    connector_id = input("Connector ID: ")
    token = input("API key: ")

    org_key = input("Org Key: ")

    with CreateKeyEx(HKEY_CURRENT_USER, DEFAULT_KEYPATH, 0, KEY_WRITE) as regkey:
        SetValueEx(regkey, "url", 0, REG_SZ, url)
        SetValueEx(regkey, "token", 0, REG_SZ, "{0}/{1}".format(token, connector_id))
        SetValueEx(regkey, "org_key", 0, REG_SZ, org_key)
        SetValueEx(regkey, "ssl_verify", 0, REG_DWORD, 1 if ssl_verify else 0)

    print("Successfully wrote credentials to the registry.")


def configure(opts):
    """Configure file"""
    credential_path = os.path.join(os.path.expanduser("~"), ".carbonblack")
    credential_file = os.path.join(credential_path, "credentials.cbc")

    print("Welcome to the cbc_sdk.")
    if os.path.exists(credential_file):
        print("An existing credential file exists at {0}.".format(credential_file))
        resp = input("Do you want to continue and overwrite the existing configuration? [Y/N] ")
        if resp.strip().upper() != "Y":
            print("Exiting.")
            return 1

    if not os.path.exists(credential_path):
        os.makedirs(credential_path, 0o700)

    url = input("URL to the Carbon Black Cloud API server (do not include '/integrationServices') [https://hostname]: ")

    ssl_verify = True

    connector_id = input("Connector ID: ")
    token = input("API key: ")

    org_key = input("Org Key: ")

    config = configparser.ConfigParser()
    config.readfp(StringIO('[default]'))
    config.set("default", "url", url)
    config.set("default", "token", "{0}/{1}".format(token, connector_id))
    config.set("default", "org_key", org_key)
    config.set("default", "ssl_verify", ssl_verify)
    with temp_umask(0):
        with os.fdopen(os.open(credential_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), 'w') as fp:
            os.chmod(credential_file, 0o600)
            config.write(fp)
    print("Successfully wrote credentials to {0}.".format(credential_file))


command_map = {
    "configure": {
        "extra_args": {},
        "help": "Configure CBC SDK",
        "method": configure
    },
    "configure-windows": {
        "extra_args": {},
        "help": "Configure CBC SDK for the Windows Registry",
        "method": configure_windows
    }
}


def main(args):
    """Process command line input"""
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command_name", help="CBC SDK subcommand")

    for cmd_name, cmd_config in iter(command_map.items()):
        cmd_parser = commands.add_parser(cmd_name, help=cmd_config.get("help", None))
        for cmd_arg_name, cmd_arg_config in iter(cmd_config.get("extra_args", {}).items()):
            cmd_parser.add_argument(cmd_arg_name, **cmd_arg_config)

    opts = parser.parse_args(args)
    command = command_map.get(opts.command_name)
    if not command:
        parser.print_usage()
        return

    command_method = command.get("method", None)
    if command_method:
        return command_method(opts)
    else:
        parser.print_usage()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
