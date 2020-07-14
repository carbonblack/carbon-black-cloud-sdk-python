#!/usr/bin/env python3

"""Credential helper"""

import argparse
import contextlib

import os
import sys
from io import StringIO as StringIO


from cbc_sdk.six.moves.configparser import RawConfigParser


@contextlib.contextmanager
def temp_umask(umask):
    """Temporary unmask"""
    oldmask = os.umask(umask)
    try:
        yield
    finally:
        os.umask(oldmask)


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

    config = RawConfigParser()
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
        "help": "Configure CbAPI",
        "method": configure
    }
}


def main(args):
    """Process command line input"""
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command_name", help="CbAPI subcommand")

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
