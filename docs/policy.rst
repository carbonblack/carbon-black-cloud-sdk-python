..
    # *******************************************************
    # Copyright (c) Broadcom, Inc. 2020-2026. All Rights Reserved. Carbon Black.
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

How does the Policy get updated via SDK?
----------------------------------------
The Carbon Black Cloud Python SDK uses property updates to trigger the dirty attribute - modifying _info a protected property directly is not intended.

However in the case of e.g. modifying sensor settings, sensor_settings is an object so you’d have to modify the entire object to trigger the dirty attribute given the SDK doesn't support depth detection given you are no longer modifying the class object but instead a raw dictionary. The SDK would have to sub class the sensor settings to pick up the changes which gets into a whole different parent child object dirty attribute tracking.

TL;DR: You are not touching the policy object when modifying sub properties of sensor settings as you are now in a python dictionary

You need to perform a replace all on the entire sensor_settings to trigger the policy dirty attribute

.. code-block:: python

    >>> policy = cb.select(Policy, 123)

    >>> new_sensor_settings = copy.deepcopy(policy.sensor_settings)
    >>> new_sensor_settings["some_property"] = "new_setting"

    >>> policy.sensor_settings = new_sensor_settings

Note: this challenge/workaround affects other modifiable CBC objects with nested properties, where the SDK hasn't implemented sub-resourcing.

Resources
---------
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
