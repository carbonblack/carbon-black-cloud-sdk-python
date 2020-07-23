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

from __future__ import absolute_import
import sys
import dateutil.parser


def convert_query_params(qd):
    o = []
    for k, v in iter(qd.items()):
        if type(v) == list:
            for item in v:
                o.append((k, item))
        else:
            o.append((k, v))

    return o


def convert_from_cb(s):
    # Use dateutil.parser to parse incoming dates; flexible on what we receive, strict on what we send.
    if s is None:
        return dateutil.parser.parse("1970-01-01T00:00:00Z")
    else:
        return dateutil.parser.parse(s)


def convert_to_cb(dt):
    return dt.strftime(cb_datetime_format)


def convert_to_kv_pairs(q):
    k, v = q.split(':', 1)
    return k, v
