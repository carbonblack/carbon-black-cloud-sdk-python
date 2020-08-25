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

"""Utility functions for use within the CBC SDK."""

from __future__ import absolute_import
import dateutil.parser


cb_datetime_format = "%Y-%m-%d %H:%M:%S.%f"


def convert_query_params(qd):
    """
    Expand a dictionary of query parameters by turning "list" values into multiple pairings of key with value.

    Args:
        qd (dict): A mapping of parameter names to values.

    Returns:
        list: A list of query parameters, each one a tuple containing name and value, after the expansion is applied.
    """
    o = []
    for k, v in iter(qd.items()):
        if type(v) == list:
            for item in v:
                o.append((k, item))
        else:
            o.append((k, v))

    return o


def convert_from_cb(s):
    """
    Parse a date and time value into a datetime object.

    Args:
        s (str): The date and time string to parse. If this is None, we use the UNIX epoch timestamp.

    Returns:
        datetime: The parsed date and time.
    """
    if s is None:
        return dateutil.parser.parse("1970-01-01T00:00:00Z")
    else:
        return dateutil.parser.parse(s)


def convert_to_cb(dt):
    """
    Convert a date and time to a string in the Carbon Black format.

    Args:
        dt (datetime): The date and time to be converted.

    Returns:
        str: The date and time as a string.
    """
    return dt.strftime(cb_datetime_format)
