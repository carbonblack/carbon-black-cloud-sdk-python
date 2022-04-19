#!/usr/bin/env python3

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

"""
Helper script for adding an entry into macos's keychain.

Use the script by simply invoking it without any system arguments to
import your configuration from a file or manually by inputs.

Invoke it with system arguments to create an entry without having to type the credentials manually.

Examples:
    Using system arguments:
    $ ./set-macos-keychain.py -e CBC_SDK -a default -t <TOKEN> -k <ORG_KEY> -u <URL>

    By using credentials file:
    $ ./set-macos-keychain.py -i

    By manually inputting the values:
    $ ./set-macos-keychain.py
"""

import argparse
import json
import configparser
import sys
from pathlib import Path
import keyring

from cbc_sdk.credential_providers import FileCredentialProvider

DEFAULT_CREDENTIALS_PATH = Path.home() / ".carbonblack/credentials.cbc"


def import_from_file(file):
    """Set credentials from a local file.

    Args:
        file (str | Path): The cbc credential file.
    """
    parser = configparser.ConfigParser()
    parser.read(file)
    for section in parser.sections():
        # reusing the parsing of the credentials because it is redundant to implement it twice
        credentials = FileCredentialProvider(credential_file=file).get_credentials(section=section).to_dict()
        keyring.set_password(f"CBC SDK API [{section}]", section, json.dumps(credentials))


def set_from_input():
    """Set credentials from user's input"""
    keychain_entry_name = input("Keychain Entry Name: ")
    keychain_account_name = input("Keychain Account Name: ")
    url = input("URL to the Carbon Black Cloud API server (do not include '/integrationServices') [https://hostname]: ")
    ssl_verify = True
    connector_id = input("API ID: ")
    token = input("API Secret Key: ")
    org_key = input("Org Key: ")
    json_obj = {
        "url": url,
        "ssl_verify": ssl_verify,
        "token": f"{token}/{connector_id}",
        "org_key": org_key,
    }
    keyring.set_password(keychain_entry_name, keychain_account_name, json.dumps(json_obj))
    print("Successfully set the entry into the Keychain!")


def set_from_kwargs(args):
    """Set credentials from given keyword args.

    Args:
        args (Namespace): The parsed args from the ArgumentParser.
    """
    _args = vars(args)
    keychain_entry = _args.pop("keychain_entry", "CBC SDK API")
    keychain_account = _args.pop("keychain_account", "default")

    keyring.set_password(keychain_entry, keychain_account, json.dumps(_args))
    print("Successfully set the entry into the Keychain!")


def main(argv=None):
    """Entry to the script

    Args:
        argv (Iterable): The kwargs coming from the system.
    """
    cmdline_parser = argparse.ArgumentParser()
    cmdline_parser.add_argument(
        "-e", "--keychain-entry", action="store", help="the entry name in keychain."
    )
    cmdline_parser.add_argument(
        "-a", "--keychain-account", action="store", help="the account name in keychain."
    )
    cmdline_parser.add_argument(
        "-u", "--url", action="store", help="the url used to access the carbon black cloud."
    )
    cmdline_parser.add_argument(
        "-t",
        "--token",
        action="store",
        help="the access token to be used to authenticate to the server.",
    )
    cmdline_parser.add_argument(
        "-k",
        "--orgkey",
        action="store",
        help="the organization key specifying which organization to work with.",
    )
    cmdline_parser.add_argument(
        "--ssl-verify", action="store_true", help="validate the ssl connection."
    )
    cmdline_parser.add_argument(
        "--no-ssl-verify", action="store_true", help="do not validate the ssl connection."
    )
    cmdline_parser.add_argument(
        "--ssl-verify-hostname",
        action="store_true",
        help="verify the host name of the server being connected to.",
    )
    cmdline_parser.add_argument(
        "--no-ssl-verify-hostname",
        action="store_true",
        help="do not verify the host name of the server being connected to.",
    )
    cmdline_parser.add_argument(
        "--ssl-cert-file",
        action="store",
        help="certificate file used to validate the certificates of the ssl connection.",
    )
    cmdline_parser.add_argument(
        "--force-tls12", action="store_true", help="force the connection to use tls 1.2."
    )
    cmdline_parser.add_argument(
        "--no-force-tls12",
        action="store_true",
        help="do not force the connection to use tls 1.2.",
    )
    cmdline_parser.add_argument(
        "--proxy",
        action="store",
        help="name of a proxy host to be used in making the connection.",
    )
    cmdline_parser.add_argument(
        "--ignore-system-proxy",
        action="store_true",
        help="ignore system proxy settings when connecting to the server.",
    )
    cmdline_parser.add_argument(
        "--no-ignore-system-proxy",
        action="store_true",
        help="do not ignore system proxy settings when connecting to the server.",
    )
    cmdline_parser.add_argument(
        "-i",
        "--import-credentials",
        action="store_true",
        help="use a credential file to import your credentials."
    )
    args = cmdline_parser.parse_args(argv)

    # Check if an existing credentials are available, if not prompt a path to credentials.
    if args.import_credentials:
        if DEFAULT_CREDENTIALS_PATH.is_file():
            print(f"An existing credential file exists at {DEFAULT_CREDENTIALS_PATH}.")
            resp = input("Do you want to import the existing configuration? [Y/N] ")
            if resp.strip().upper() != "N":
                import_from_file(DEFAULT_CREDENTIALS_PATH)
                return 0
            else:
                path = input("Specify the path to your credentials file: ")
                path_to_credentials = Path(path)
                if path_to_credentials.is_file():
                    import_from_file(path_to_credentials)
                    return 0
                else:
                    print("The specified path does not contain a file.")
                    return 1

    # If there are system arguments, set the credentials from them.
    if len(sys.argv) > 1:
        set_from_kwargs(args)
        return 0

    # If you want to setup manually by input.
    set_from_input()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
