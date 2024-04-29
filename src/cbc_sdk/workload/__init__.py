from __future__ import absolute_import

from cbc_sdk.workload.vm_workloads_search import VCenterComputeResource, AWSComputeResource
from cbc_sdk.workload.sensor_lifecycle import SensorKit
from cbc_sdk.workload.nsx_remediation import NSXRemediationJob
from cbc_sdk.workload.compliance_assessment import ComplianceBenchmark


# Maintain link for easier migration
from cbc_sdk.platform.vulnerability_assessment import Vulnerability
from cbc_sdk.workload.vm_workloads_search import VCenterComputeResource as ComputeResource
