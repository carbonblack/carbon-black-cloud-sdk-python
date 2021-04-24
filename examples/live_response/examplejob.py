#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Example script for get file"""


class GetFileJob(object):
    """Get file"""
    def __init__(self, file_name):
        """Initializer"""
        self._file_name = file_name

    def run(self, session):
        """Get the file"""
        return session.get_file(self._file_name)


def getjob():
    """Get job"""
    return GetFileJob("c:\\test.txt")
