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
    def __init__(self, file_name, file_dir):
        """Initializer"""
        self._file_name = file_name
        self._file_dir = file_dir

    def run(self, session):
        """List directory and get file"""
        directories = session.list_directory(self._file_dir)
        for directory in directories:
            print(f"{directory['attributes'][0]} {directory['filename']}")
        return session.get_file(self._file_name)


def getjob():
    """Get job"""
    return GetFileJob("c:\\test.txt", "c:\\")
