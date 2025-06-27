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

"""Utility functions for use within the CBC SDK."""

from __future__ import absolute_import
import dateutil.parser
import time
from cbc_sdk.errors import TimeoutError


cb_datetime_format = "%Y-%m-%d %H:%M:%S.%f"


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


class BackoffHandler:
    """
    Logic for handling exponential backoff of multiple communications requests.

    The logic also handles timeouts of operations that go on too long.

    Example::

        backoff = BackoffHandler(timeout=600000)  # 10 minutes = 600 seconds
        with backoff as b:
            while operation_continues():
                b.pause()
                do_operation()
    """
    def __init__(self, cb, timeout=0, initial=0.1, multiplier=2.0, threshold=2.0):
        """
        Initialize the ``BackoffHandler``.

        Args:
            cb (BaseAPI): The API object for the operation.
            timeout (int): The timeout for the operation, in milliseconds.  If this is 0, the default timeout as
                           configured in the credentials will be used. The default is 0.
            initial (float): The initial value for the exponential backoff pause, in seconds.  The default is 0.1.
            multiplier (float): The value by which the exponential backoff pause will be multiplied each time
                                a pause happens.  The default is 2.0.
            threshold (float): The maximum value for the exponential backoff pause, in seconds. The default is 2.0.
        """
        self._cb = cb
        self._timeout = cb.credentials.default_timeout if timeout == 0 else timeout
        self._initial = initial
        self._multiplier = multiplier
        self._threshold = threshold

    class BackoffOperation:
        """
        Handler for a single operation requiring exponential backoff between communication attempts.

        This is returned by ``BackoffHandler`` as part of the ``with`` operation, and is stored in the variable
        referred to in its ``as`` clause.
        """
        def __init__(self, timeout, initial, multiplier, threshold):
            """
            Initialize the ``BackoffOperation``.

            Args:
                timeout (int): The timeout for the operation, in milliseconds.
                initial (float): The initial value for the exponential backoff pause, in seconds.
                multiplier (float): The value by which the exponential backoff pause will be multiplied each time
                                    a pause happens.
                threshold (float): The maximum value for the exponential backoff pause, in seconds.
            """
            self._initial = initial
            self._multiplier = multiplier
            self._threshold = threshold
            self._timeout_time = time.time() * 1000 + timeout
            self._pausetime = 0.0
            self._first = True

        def pause(self):
            """
            Pauses operation for a determined amount of time.

            The method also checks for a timeout and raises ``TimeoutError`` if it happens, and computes the amount
            of time to pause the next time this method is called.

            Raises:
                TimeoutError: If the timeout value is reached.
            """
            if time.time() * 1000 > self._timeout_time:
                raise TimeoutError(message="Operation timed out")
            if self._pausetime > 0.0:
                time.sleep(self._pausetime)
                if time.time() * 1000 > self._timeout_time:
                    raise TimeoutError(message="Operation timed out")
            if self._first:
                self._pausetime = self._initial
                self._first = False
            else:
                self._pausetime = min(self._pausetime * self._multiplier, self._threshold)

        def reset(self, full=False):
            """
            Resets the state of the operation so that the pause time is reset.

            Does not affect the timeout value. This should be used, for instance, after a successful operation to
            minimize the pause before the next operation is started.

            Args:
                full (bool): If this is ``True``, the next pause time will be reset to 0. If this is ``False``, the
                             next pause time will be reset to the initial pause time.
            """
            if full:
                self._pausetime = 0.0
                self._first = True
            else:
                self._pausetime = self._initial

    def __enter__(self):
        """
        Called at entry of the context specified by this object.

        Returns:
            BackoffHandler.BackoffOperation: A new ``BackoffOperation`` object to manage the current operation.
        """
        return BackoffHandler.BackoffOperation(self._timeout, self._initial, self._multiplier, self._threshold)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called at exit of the context specified by this object.

        This context does not suppress exceptions.

        Args:
            exc_type (Any): Exception type (not used).
            exc_val (Any): Exception value (not used).
            exc_tb (Any): Exception traceback (not used).

        Returns:
            bool: Always ``False``.
        """
        return False

    @property
    def timeout(self):
        """Returns the current timeout associated with this handler, in milliseconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        """
        Sets the the current timeout associated with this handler

        Args:
            val (int): New timeout value to set, in milliseconds.
        """
        self._timeout = self._cb.credentials.default_timeout if val == 0 else val
