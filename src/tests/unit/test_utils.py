# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
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
import time
from datetime import datetime
from cbc_sdk.utils import convert_from_cb, convert_to_cb, BackoffHandler
from cbc_sdk.errors import TimeoutError
from cbc_sdk.connection import BaseAPI


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


def test_backoff_handler_operation():
    """Test the operation of the BackoffHandler."""
    cb = BaseAPI(integration_name='test1', url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')
    sut = BackoffHandler(cb, threshold=0.5)
    assert sut.timeout == 300000
    assert sut._initial == 0.1
    assert sut._multiplier == 2.0
    assert sut._threshold == 0.5
    with sut as b:
        assert b._pausetime == 0.0
        b.pause()
        assert b._pausetime == 0.1
        b.pause()
        assert b._pausetime == 0.2
        b.pause()
        assert b._pausetime == 0.4
        b.pause()
        assert b._pausetime == 0.5
        b.reset()
        assert b._pausetime == 0.1
        b.pause()
        assert b._pausetime == 0.2
        b.reset(True)
        assert b._pausetime == 0.0


def test_backoff_handler_timeouts():
    """Test the raising of TimeoutError by the BackoffHandler."""
    cb = BaseAPI(integration_name='test1', url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')
    sut = BackoffHandler(cb, timeout=10)
    with sut as b:
        time.sleep(0.1)
        with pytest.raises(TimeoutError):
            b.pause()
    sut.timeout = 250
    with sut as b:
        b.pause()   # no pause
        b.pause()   # pauses 0.1 sec
        with pytest.raises(TimeoutError):
            b.pause()
