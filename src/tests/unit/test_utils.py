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

"""Test code for the utility functions"""

import pytest
from datetime import datetime
from cbc_sdk.utils import convert_query_params, convert_from_cb, convert_to_cb, dynamic_load, dynamic_create


class TestClassForLoad:
    """Stub class to be used as a target for loading operations."""
    pass

# ==================================== Unit TESTS BELOW ====================================


def test_convert_query_params():
    """Test that query parameter dicts are properly converted."""
    lv = convert_query_params({'answer': 42, 'hup': [2, 3, 4], 'goody': 'twoshoes'})
    assert isinstance(lv, list)
    assert len(lv) == 5
    assert ('answer', 42) in lv
    assert ('hup', 2) in lv
    assert ('hup', 3) in lv
    assert ('hup', 4) in lv
    assert ('goody', 'twoshoes') in lv
    lv = convert_query_params({})
    assert isinstance(lv, list)
    assert len(lv) == 0


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


def test_dynamic_load():
    """Test to make sure we can dynamically load a class."""
    class1 = dynamic_load('tests.unit.test_utils.TestClassForLoad')
    assert class1 == TestClassForLoad
    with pytest.raises(ImportError):
        dynamic_load('bogus_package.bogus_class')


def test_dynamic_create():
    """Test to make sure we can dynamically load a class and create an instance of said class."""
    obj1 = dynamic_create('tests.unit.test_utils.TestClassForLoad')
    assert isinstance(obj1, TestClassForLoad)
    with pytest.raises(ImportError):
        dynamic_create('bogus_package.bogus_class')
