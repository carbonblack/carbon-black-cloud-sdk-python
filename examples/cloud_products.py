"""Example for Developer Meetup October 22 covering most cloud products."""

"""Import Relevant Packages"""

# Audit and Remediation
from cbc_sdk.audit_remediation import Run, RunHistory, Result, DeviceSummary
from endpoint_standard.live_response_cli import CblrCli, connect_callback

# Endpoint Standard
from cbc_sdk.endpoint_standard import Policy
from cbc_sdk.endpoint_standard import Event as EndpointStandardEvent
from cbc_sdk.endpoint_standard import Device as EndpointStandardDevice

# Enterprise EDR
from cbc_sdk.enterprise_edr import Feed, Event, Process, Tree, Watchlist, Report, IOC, IOC_V2

# Platform Alerts and Devices
from cbc_sdk.platform import BaseAlert as PlatformAlert
from cbc_sdk.platform import Device as PlatformDevice

# CBC SDK Base
from cbc_sdk import CBCloudAPI

"""Setup"""

# API keys with relevant permissions
aar_api = CBCloudAPI(profile='audit_remediation')
es_api = CBCloudAPI(profile='endpoint_standard')
eedr_api = CBCloudAPI(profile='enterprise_edr')
platform_api = CBCloudAPI(profile='platform')


"""Platform Alerts and Devices"""

# Egregor Ransomware TTPs https://community.carbonblack.com/t5/Threat-Research-Docs/TAU-TIN-Egregor-Ransomware/ta-p/95786#
egregor_query = "DATA_TO_ENCRYPTION AND ACCESS_DATA_FILES AND PACKED_CALL AND ENUMERATE_PROCESSES AND MODIFY_MEMORY_PROTECTION"

# Find Alerts associated with the ransomware
# Equivalent to using the Alerts tab with Advanced search turned on in the UI
egregor_alerts = platform_api.select(PlatformAlert).where(egregor_query)

if egregor_alerts:
    print(f"Number of Alerts generated by Egregor Ransomware: {len(egregor_alerts)}")

harmless_query = "yahoo"
ioc_alerts = platform_api.select(PlatformAlert).where(harmless_query).set_create_time(range="-6h")

if ioc_alerts:
    potentially_compromised_devices = set()
    for alert in ioc_alerts:
        potentially_compromised_devices.add(alert.device_id)
        # alert.update_threat(remediation="Investigating", comment="Identified w/ CBCSDK. Proceeding to quarantine and Live Response.")

"""Endpoint Standard Live Response"""
# if potentially_compromised_devices:
#     for device_id in potentially_compromised_devices:
        # Quarantine the device and change its Policy
        # platform_dev = platform_api.select(PlatformDevice, device_id)
        # platform_dev.device_quarantine(True)
        # platform_dev.update_policy(6)

        # Start a Live Response Session (using an example helper)
        # command_line = CblrCli(aar_api, connect_callback)
        # command_line.do_connect(device_id)
        # command_line.cmdloop()

        # Can also directly execute a command
        # command_line.do_exec(r'cmd.exe /c "ping.exe 192.168.1.1"')



"""Enterprise EDR Processes"""








"""
Applications at Path:
**\rundll32.exe,
**\regsvr32.exe

Performs ransomware-like behavior
Invokes an untrusted process
Injects code or modifies memory of another process
Communicates over the network
Terminate Process
Terminate Process
Terminate Process
Deny Operation

Unknown application or process
Communicates over the network
Injects code or modifies memory of another process
Performs ransomware-like behavior
Deny Operation
Terminate Process
Terminate Process
"""
