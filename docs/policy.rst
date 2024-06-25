..
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

Policy
=========================================================

A policy determines preventative behavior and establishes sensor settings. Each endpoint sensor or sensor group
is assigned a policy.

Policies are a collection of prevention rules and behavioral settings that define how your sensor interacts and
prevents or allows behavior on your endpoint. Within Policies, you can create custom blocking rules, allow
applications, and modify the way your sensor communicates with the Carbon Black Cloud.

Example scripts are available in the GitHub repository in examples/platform that demonstrate

* Basic Create, Read, Update, Delete and Export/Import operations for Prevention, Local Scan and Sensor rules

  * policy_service_crud_operations.py

* Core Prevention policy rule operations

  * policy_core_prevention.py

* Host-Based Firewall policy rule operations

  * policy_host_based_firewall.py

* Data Collection policy rule operations

  * Demonstrates how to enable and disable Auth Event collection.

  * policy_data_collection.py
