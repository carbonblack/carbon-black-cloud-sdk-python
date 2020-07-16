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
from importlib import import_module


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


def dynamic_load(full_class_name):
    """
    Loads a Python class object given its fully-qualified class name.

    Args:
        full_class_name (str): The class name of the object to be loaded.

    Returns:
        The class object.

    Raises:
        ImportError: If the class could not be loaded.

    """
    try:
        module_path, class_name = full_class_name.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(full_class_name) from e


def dynamic_create(full_class_name):
    """
    Creates a Python object given its fully-qualified class name.

    Args:
        full_class_name (str): The class name of the object to be created.

    Returns:
        A new instance of that object.

    """
    class_obj = dynamic_load(full_class_name)
    return class_obj()
