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

"""Mock data for Differential Analysis"""

QUERY_COMPARISON_COUNT_ONLY = {
    "org_key": "ABCD1234",
    "results": [
        {
            "newer_run_id": "qpopjb82whlmthlo0x1wrwcnoyxmrueu",
            "newer_run_create_time": "2022-05-11T10:49:36.190Z",
            "older_run_id": "kibloccplynombvigcgtu2et2zayhzal",
            "older_run_create_time": "2022-05-11T10:47:48.952Z",
            "diff_processed_time": 0.262,
            "newer_run_not_responded_devices": [],
            "older_run_not_responded_devices": [],
            "diff_results": [
                {
                    "device_id": 11412673,
                    "change_count": 1,
                    "added_count": 1,
                    "removed_count": 0,
                    "changes": "null",
                    "older_run_row_count": 17,
                    "newer_run_row_count": 18
                },
                {
                    "device_id": 12345678,
                    "change_count": 2,
                    "added_count": 2,
                    "removed_count": 0,
                    "changes": "null",
                    "older_run_row_count": 13,
                    "newer_run_row_count": 15
                }
            ]
        }
    ]
}

QUERY_COMPARISON_SET_DEVICE_ID = {
    "org_key": "ABCD1234",
    "results": [
        {
            "newer_run_id": "qpopjb82whlmthlo0x1wrwcnoyxmrueu",
            "newer_run_create_time": "2022-05-11T10:49:36.190Z",
            "older_run_id": "kibloccplynombvigcgtu2et2zayhzal",
            "older_run_create_time": "2022-05-11T10:47:48.952Z",
            "diff_processed_time": 0.262,
            "newer_run_not_responded_devices": [],
            "older_run_not_responded_devices": [],
            "diff_results": [
                {
                    "device_id": 11412673,
                    "change_count": 1,
                    "added_count": 1,
                    "removed_count": 0,
                    "changes": "null",
                    "older_run_row_count": 17,
                    "newer_run_row_count": 18
                }
            ]
        }
    ]
}

QUERY_COMPARISON_ACTUAL_CHANGES = {
    "org_key": "ABCD1234",
    "results": [
        {
            "newer_run_id": "qpopjb82whlmthlo0x1wrwcnoyxmrueu",
            "newer_run_create_time": "2022-05-11T10:49:36.190Z",
            "older_run_id": "kibloccplynombvigcgtu2et2zayhzal",
            "older_run_create_time": "2022-05-11T10:47:48.952Z",
            "diff_processed_time": 0.062,
            "newer_run_not_responded_devices": [],
            "older_run_not_responded_devices": [],
            "diff_results": [
                {
                    "device_id": 11412673,
                    "change_count": 1,
                    "added_count": 1,
                    "removed_count": 0,
                    "changes": [
                        {
                            "action": "added",
                            "fields": [
                                {
                                    "key": "name",
                                    "value": "Enhancer for YouTube™"
                                },
                                {
                                    "key": "path",
                                    "value": "C:\\Users\\Administrator\\"
                                },
                                {
                                    "key": "version",
                                    "value": "2.0.113"
                                }
                            ]
                        }
                    ],
                    "older_run_row_count": 17,
                    "newer_run_row_count": 18
                }
            ]
        }
    ]
}
