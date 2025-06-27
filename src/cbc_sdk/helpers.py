#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Helper functions which are not strictly part of the SDK API, but which are used by many of the examples."""

from __future__ import print_function

import sys
import time
import argparse
import logging
from collections import defaultdict
import hashlib
import validators


from cbc_sdk import CBCloudAPI

log = logging.getLogger(__name__)


def eprint(*args, **kwargs):
    """
    Print to standard error output.

    Args:
        *args (list): Arguments to the print function.
        **kwargs (dict): Keyword arguments to the print function.
    """
    print(*args, file=sys.stderr, **kwargs)


def build_cli_parser(description="Cb Example Script"):
    """
    Build a basic CLI parser containing the arguments needed to create a CBCloudAPI. Additional arguments may be added.

    Args:
        description (str): Description of the script, for use in help messages.

    Returns:
        ArgumentParser: The new argument parser.
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--cburl", help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_argument("--proxy", help="Proxy URL.  e.g., http://127.0.0.1 ")
    parser.add_argument("--apitoken", help="API Token for VMware Carbon Black Cloud")
    parser.add_argument("--csp-api-token", help="CSP API Token for VMware Carbon Black Cloud")
    parser.add_argument("--csp-oauth-app-id", help="CSP OAuth App ID for VMware Carbon Black Cloud")
    parser.add_argument("--csp-oauth-app-secret", help="CSP OAuth App Secret for VMware Carbon Black Cloud")
    parser.add_argument("--csp-url-override", help="CSP URL to override default value %(default)s",
                        default="https://console.cloud.vmware.com")
    parser.add_argument("--orgkey", help="Organization key value for Carbon Black server")
    parser.add_argument("--no-ssl-verify", help="Do not verify server SSL certificate.", action="store_true",
                        default=False)
    parser.add_argument("--profile", help="profile to connect", default="default")
    parser.add_argument("--verbose", help="enable debug logging", default=False, action='store_true')

    return parser


def disable_insecure_warnings():
    """Disable warnings about insecure URLs."""
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()


def get_cb_cloud_object(args):
    """
    Based on parsed command line arguments, create and return a CBCloudAPI object.

    Args:
        args (Namespace): Arguments parsed from the command line.

    Returns:
        CBCloudAPI: The CBCloudAPI object.
    """
    if args.verbose:
        logging.basicConfig()
        logging.getLogger("cbc_sdk").setLevel(logging.DEBUG)
        logging.getLogger("__main__").setLevel(logging.DEBUG)

    if args.cburl and args.apitoken and args.orgkey:
        cb = CBCloudAPI(url=args.cburl,
                        proxy=args.proxy,
                        token=args.apitoken,
                        org_key=args.orgkey,
                        ssl_verify=(not args.no_ssl_verify))

    elif args.cburl and args.csp_api_token and args.orgkey:
        csp_url_override = args.csp_url_override if args.csp_url_override else "https://console.cloud.vmware.com"
        cb = CBCloudAPI(url=args.cburl,
                        proxy=args.proxy,
                        csp_api_token=args.csp_api_token,
                        csp_url_override=csp_url_override,
                        org_key=args.orgkey,
                        ssl_verify=(not args.no_ssl_verify))

    elif args.cburl and args.csp_oauth_app_id and args.csp_oauth_app_secret and args.orgkey:
        csp_url_override = args.csp_url_override if args.csp_url_override else "https://console.cloud.vmware.com"
        cb = CBCloudAPI(url=args.cburl,
                        proxy=args.proxy,
                        csp_oauth_app_id=args.csp_oauth_app_id,
                        csp_oauth_app_secret=args.csp_oauth_app_secret,
                        csp_url_override=csp_url_override,
                        org_key=args.orgkey,
                        ssl_verify=(not args.no_ssl_verify))
    else:
        cb = CBCloudAPI(profile=args.profile)

    return cb


def get_object_by_name_or_id(cb, cls, name_field="name", id=None, name=None):
    """
    Locate an object in the API by either ID or name.

    Args:
        cb (CBCloudAPI): Reference to the CBCloudAPI.
        cls (class): Class of object to be found.
        name_field (str): Name field to search on.
        id (int): ID of object to search for. May be None to do name searching.
        name (str): Object name to search on.
        force_init (bool): True to force a new object found by ID to be initialized.

    Returns:
        list: List of objects that match the search criteria.
    """
    clsname = cls.__name__
    attempted_to_find = ''
    try:
        if not (id or name) or (id and name):
            raise Exception("Either id or name should be provided.")
        if id:
            attempted_to_find = "ID of {0:d}".format(id)
            objs = [cb.select(cls, id)]
        else:
            attempted_to_find = "name {0:s}".format(name)
            objs = cb.select(cls).where("{0}:{1}".format(name_field, name))[::]
            if not len(objs):
                raise Exception("No {0}s match".format(clsname))
    except Exception as e:
        raise Exception("Could not find {0} with {1:s}: {2:s}".format(clsname, attempted_to_find, str(e)))
    else:
        return objs


def read_iocs(cb, file=sys.stdin):
    """
    Read indicators of compromise from standard input.

    Args:
        cb (CBCloudAPI): Reference to the CBCloudAPI.
        file: Not used.

    Returns:
        str: New report ID to be used.
        dict: The indicators of compromise that were read in.
    """
    iocs = defaultdict(list)
    report_id = hashlib.md5()
    report_id.update(str(time.time()).encode("utf-8"))

    for idx, line in enumerate(file):
        line = line.rstrip("\r\n")
        report_id.update(line.encode("utf-8"))
        if validators.md5(line):
            iocs["md5"].append(line)
        elif validators.sha256(line):
            eprint("line {}: sha256 provided but not yet supported by backend".format(idx + 1))
            iocs["sha256"].append(line)
        elif validators.ipv4(line):
            iocs["ipv4"].append(line)
        elif validators.ipv6(line):
            iocs["ipv6"].append(line)
        elif validators.domain(line):
            iocs["dns"].append(line)
        else:
            if cb.validate_process_query(line):
                query_ioc = {"search_query": line}
                iocs["query"].append(query_ioc)
            else:
                eprint("line {}: invalid query".format(idx + 1))

    return (report_id.hexdigest(), dict(iocs))
