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

"""Test code for the utility functions"""

# import pytest
from datetime import datetime
from cbc_sdk.utils import convert_from_cb, convert_to_cb


# ==================================== Unit TESTS BELOW ====================================


def test_convert_from_cb():
    """Test the conversion of dates from CB format strings."""
    t = convert_from_cb("2020-03-11T18:34:11")
    assert isinstance(t, datetime)
    assert t.year == 2020
    assert t.month == 3
    assert t.day == 11
    assert t.hour == 18
    assert t.minute == 34
    assert t.second == 11
    assert t.microsecond == 0
    t = convert_from_cb(None)
    assert isinstance(t, datetime)
    assert t.year == 1970
    assert t.month == 1
    assert t.day == 1
    assert t.hour == 0
    assert t.minute == 0
    assert t.second == 0
    assert t.microsecond == 0


def test_convert_to_cb():
    """Test the conversion of a date into CB format."""
    t = datetime(2020, 3, 11, 18, 34, 11, 123456)
    s = convert_to_cb(t)
    assert s == "2020-03-11 18:34:11.123456"
