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

from __future__ import print_function

import sys
import time
import argparse
import logging
from collections import defaultdict
import validators
import hashlib

from cbc_sdk import CBCloudAPI

log = logging.getLogger(__name__)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def build_cli_parser(description="Cb Example Script"):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--cburl", help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_argument("--apitoken", help="API Token for Carbon Black server")
    parser.add_argument("--orgkey", help="Organization key value for Carbon Black server")
    parser.add_argument("--no-ssl-verify", help="Do not verify server SSL certificate.", action="store_true",
                        default=False)
    parser.add_argument("--profile", help="profile to connect", default="default")
    parser.add_argument("--verbose", help="enable debug logging", default=False, action='store_true')

    return parser


def disable_insecure_warnings():
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()


def get_cb_cloud_object(args):
    if args.verbose:
        logging.basicConfig()
        logging.getLogger("cbapi").setLevel(logging.DEBUG)
        logging.getLogger("__main__").setLevel(logging.DEBUG)

    if args.cburl and args.apitoken:
        cb = CBCloudAPI(url=args.cburl, token=args.apitoken, ssl_verify=(not args.no_ssl_verify))
    else:
        cb = CBCloudAPI(profile=args.profile)

    return cb


def get_object_by_name_or_id(cb, cls, name_field="name", id=None, name=None, force_init=True):
    clsname = cls.__name__
    try:
        if id:
            attempted_to_find = "ID of {0:d}".format(id)
            objs = [cb.select(cls, id, force_init=force_init)]
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
    iocs = defaultdict(list)
    report_id = hashlib.md5()
    report_id.update(str(time.time()).encode("utf-8"))

    for idx, line in enumerate(sys.stdin):
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
            if cb.validate_query(line):
                query_ioc = {"search_query": line}
                iocs["query"].append(query_ioc)
            else:
                eprint("line {}: invalid query".format(idx + 1))

    return (report_id.hexdigest(), dict(iocs))
