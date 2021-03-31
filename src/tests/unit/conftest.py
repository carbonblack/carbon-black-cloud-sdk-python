# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Contains test configuration and generic fixtures."""

import pytest
import mox as pymox


@pytest.fixture(scope='function')
def mox():
    """
    Creates an instance of the mocking system as a fixture for a test.

    Returns:
        Mox: The mocking framework object.
    """
    mock_system = pymox.Mox()
    yield mock_system
    mock_system.UnsetStubs()
