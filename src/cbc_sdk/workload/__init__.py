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

from __future__ import absolute_import

from cbc_sdk.workload.vm_workloads_search import VCenterComputeResource, AWSComputeResource
from cbc_sdk.workload.sensor_lifecycle import SensorKit
from cbc_sdk.workload.nsx_remediation import NSXRemediationJob
from cbc_sdk.workload.compliance_assessment import ComplianceBenchmark


# Maintain link for easier migration
from cbc_sdk.platform.vulnerability_assessment import Vulnerability
from cbc_sdk.workload.vm_workloads_search import VCenterComputeResource as ComputeResource
