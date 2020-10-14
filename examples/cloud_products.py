"""Example for Developer Meetup October 22 covering most cloud products."""

"""Import Relevant Packages"""

# Audit and Remediation
from cbc_sdk.audit_remediation import Run, RunHistory, Result, DeviceSummary

# Endpoint Standard
from cbc_sdk.endpoint_standard import Policy
from cbc_sdk.endpoint_standard import Event as EndpointStandardEvent
from cbc_sdk.endpoint_standard import Device as EndpointStandardDevice

# Enterprise EDR
from cbc_sdk.enterprise_edr import Feed, Event, Process, Tree, Watchlist, Report, IOC, IOC_V2

# Platform Alerts and Devices
from cbc_sdk.platform import BaseAlert, WatchlistAlert, CBAnalyticsAlert, VMwareAlert, Workflow, WorkflowStatus
from cbc_sdk.platform import Device as PlatformDevice

# CBC SDK Base
from cbc_sdk import CBCloudAPI

"""Setup"""

# API keys with relevant permissions
aar_api = CBCloudAPI(profile='audit_remediation')
es_api = CBCloudAPI(profile='endpoint_standard')
eedr_api = CBCloudAPI(profile='enterprise_edr')
platform_api = CBCloudAPI(profile='platform')
