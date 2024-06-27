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

"""Mock responses for Policy"""

FULL_POLICY_1 = {
    "id": 65536,
    "name": "A Dummy Policy",
    "org_key": "test",
    "version": 2,
    "priority_level": "HIGH",
    "position": 3,
    "is_system": False,
    "description": "",
    "auto_deregister_inactive_vdi_interval_ms": 0,
    "auto_delete_known_bad_hashes_delay": 86400000,
    "av_settings": {
        "avira_protection_cloud": {
            "enabled": True,
            "max_exe_delay": 45,
            "max_file_size": 4,
            "risk_level": 4
        },
        "on_access_scan": {
            "enabled": True,
            "mode": "AGGRESSIVE"
        },
        "on_demand_scan": {
            "enabled": True,
            "profile": "NORMAL",
            "schedule": {
                "start_hour": 0,
                "range_hours": 0,
                "recovery_scan_if_missed": True
            },
            "scan_usb": "AUTOSCAN",
            "scan_cd_dvd": "AUTOSCAN"
        },
        "signature_update": {
            "enabled": True,
            "schedule": {
                "full_interval_hours": 0,
                "initial_random_delay_hours": 1,
                "interval_hours": 2
            }
        },
        "update_servers": {
            "servers_override": [],
            "servers_for_onsite_devices": [
                {
                    "server": "http://updates2.cdc.carbonblack.io/update2",
                    "preferred": False
                }
            ],
            "servers_for_offsite_devices": [
                "http://updates2.cdc.carbonblack.io/update2"
            ]
        }
    },
    "rules": [
        {
            "id": 1,
            "required": True,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "PUP"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 2,
            "required": True,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "data"
            },
            "operation": "MEMORY_SCRAPE"
        }
    ],
    "directory_action_rules": [
        {
            "file_upload": False,
            "protection": False,
            "path": ""
        }
    ],
    "sensor_settings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "ALLOW_UPLOADS",
            "value": "false"
        },
        {
            "name": "SHOW_UI",
            "value": "true"
        },
        {
            "name": "ENABLE_THREAT_SHARING",
            "value": "true"
        },
        {
            "name": "QUARANTINE_DEVICE",
            "value": "false"
        },
        {
            "name": "LOGGING_LEVEL",
            "value": "false"
        },
        {
            "name": "QUARANTINE_DEVICE_MESSAGE",
            "value": "Your device has been quarantined. Please contact your administrator."
        },
        {
            "name": "SET_SENSOR_MODE",
            "value": "0"
        },
        {
            "name": "SENSOR_RESET",
            "value": "0"
        },
        {
            "name": "BACKGROUND_SCAN",
            "value": "true"
        },
        {
            "name": "POLICY_ACTION_OVERRIDE",
            "value": "true"
        },
        {
            "name": "HELP_MESSAGE",
            "value": ""
        },
        {
            "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
            "value": "false"
        },
        {
            "name": "HASH_MD5",
            "value": "true"
        },
        {
            "name": "SCAN_LARGE_FILE_READ",
            "value": "false"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "DELAY_EXECUTE",
            "value": "false"
        },
        {
            "name": "SCAN_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "BYPASS_AFTER_LOGIN_MINS",
            "value": "0"
        },
        {
            "name": "BYPASS_AFTER_RESTART_MINS",
            "value": "0"
        },
        {
            "name": "SHOW_FULL_UI",
            "value": "true"
        },
        {
            "name": "SECURITY_CENTER_OPT",
            "value": "true"
        },
        {
            "name": "CB_LIVE_RESPONSE",
            "value": "true"
        },
        {
            "name": "UNINSTALL_CODE",
            "value": "false"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        },
        {
            "name": "ALLOW_EXPEDITED_SCAN",
            "value": "true"
        }
    ],
    "rule_configs": [
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "name": "Authentication Events",
            "description": "Authentication Events",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_auth_events": True
            }
        },
        {
            "id": "cc075469-8d1e-4056-84b6-0e6f437c4010",
            "name": "XDR",
            "description": "Turns on XDR network data collection at the sensor",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_network_data_collection": False
            }
        },
        {
            "id": "1f8a5e4b-34f2-4d31-9f8f-87c56facaec8",
            "name": "Advanced Scripting Prevention",
            "description": "Addresses malicious fileless and file-backed scripts that leverage native programs [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "description": "Addresses threat actors obtaining credentials and relies on detecting the malicious [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
            "name": "Carbon Black Threat Intel",
            "description": "Addresses common and pervasive TTPs used for malicious activity as well as [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "description": "Addresses behaviors that indicate a threat actor has gained elevated access via [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...].",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                    "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                    "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
                },
                "enable_host_based_firewall": False
            }
        },
        {
            "id": "1664f2e6-645f-4d6e-98ec-0c80485cbe0f",
            "name": "Event Reporting Exclusions",
            "description": "Allows customers to exclude specific processes from reporting events to CBC",
            "inherited_from": "psc:region",
            "category": "bypass",
            "parameters": {}
        },
        {
            "id": "1c03d653-eca4-4adc-81a1-04b17b6cbffc",
            "name": "Event Reporting and Sensor Operation Exclusions",
            "description": "Allows customers to exclude specific processes and process events from reporting to CBC",
            "inherited_from": "psc:region",
            "category": "bypass",
            "parameters": {},
            "exclusions": {
                "windows": [
                    {
                        "id": 8090,
                        "criteria": [
                            {
                                "id": 13426,
                                "type": "initiator_process",
                                "attributes": [
                                    {
                                        "id": 93774,
                                        "name": "process_name",
                                        "values": [
                                            "**\\explorer.exe"
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": 13427,
                                "type": "operation",
                                "attributes": [
                                    {
                                        "id": 93775,
                                        "name": "operation_type",
                                        "values": [
                                            "ALL"
                                        ]
                                    }
                                ]
                            }
                        ],
                        "comments": "",
                        "type": "ENDPOINT_STANDARD_PROCESS_BYPASS",
                        "apply_to_descendent_processes": True,
                        "created_by": "ABCD1234",
                        "created_at": "2024-01-27T13:29:44.839Z",
                        "modified_by": "ABCD1234",
                        "modified_at": "2024-01-27T13:29:44.839Z"
                    }
                ]
            }
        }
    ]
}

SUMMARY_POLICY_1 = {
    "id": 65536,
    "name": "A Dummy Policy",
    "priority_level": "HIGH",
    "position": 3,
    "is_system": False,
    "description": "",
    "num_devices": 0
}

SUMMARY_POLICY_2 = {
    "id": 10191,
    "is_system": False,
    "name": "Forescout Policy",
    "description": "Initial Forescout policy, no protection turned on",
    "priority_level": "MEDIUM",
    "position": 4,
    "num_devices": 0
}

SUMMARY_POLICY_3 = {
    "id": 74656,
    "is_system": True,
    "name": "Remediant AC Policy",
    "description": "Verifying AC capabilities ",
    "priority_level": "LOW",
    "position": 5,
    "num_devices": 0
}

OLD_POLICY_1 = {
    "name": "A Dummy Policy",
    "description": "",
    "version": 2,
    "sensorSettings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "ALLOW_UPLOADS",
            "value": "false"
        },
        {
            "name": "SHOW_UI",
            "value": "true"
        },
        {
            "name": "ENABLE_THREAT_SHARING",
            "value": "true"
        },
        {
            "name": "QUARANTINE_DEVICE",
            "value": "false"
        },
        {
            "name": "LOGGING_LEVEL",
            "value": "false"
        },
        {
            "name": "QUARANTINE_DEVICE_MESSAGE",
            "value": "Your device has been quarantined. Please contact your administrator."
        },
        {
            "name": "SET_SENSOR_MODE",
            "value": "0"
        },
        {
            "name": "SENSOR_RESET",
            "value": "0"
        },
        {
            "name": "BACKGROUND_SCAN",
            "value": "true"
        },
        {
            "name": "POLICY_ACTION_OVERRIDE",
            "value": "true"
        },
        {
            "name": "HELP_MESSAGE",
            "value": ""
        },
        {
            "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
            "value": "false"
        },
        {
            "name": "HASH_MD5",
            "value": "true"
        },
        {
            "name": "SCAN_LARGE_FILE_READ",
            "value": "false"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "DELAY_EXECUTE",
            "value": "false"
        },
        {
            "name": "SCAN_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "BYPASS_AFTER_LOGIN_MINS",
            "value": "0"
        },
        {
            "name": "BYPASS_AFTER_RESTART_MINS",
            "value": "0"
        },
        {
            "name": "SHOW_FULL_UI",
            "value": "true"
        },
        {
            "name": "SECURITY_CENTER_OPT",
            "value": "true"
        },
        {
            "name": "CB_LIVE_RESPONSE",
            "value": "true"
        },
        {
            "name": "UNINSTALL_CODE",
            "value": "false"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        },
        {
            "name": "ALLOW_EXPEDITED_SCAN",
            "value": "true"
        }
    ],
    "avSettings": {
        "updateServers": {
            "servers": [
                {
                    "flags": 0,
                    "regId": None,
                    "server": ["http://updates2.cdc.carbonblack.io/update2"]
                }
            ],
            "serversForOffSiteDevices": ["http://updates2.cdc.carbonblack.io/update2"]
        },
        "apc": {
            "maxFileSize": 4,
            "maxExeDelay": 45,
            "riskLevel": 4,
            "enabled": True
        },
        "onAccessScan": {
            "profile": "AGGRESSIVE"
        },
        "features": [
            {
                "enabled": True,
                "name": "ONACCESS_SCAN"
            },
            {
                "enabled": True,
                "name": "ONDEMAND_SCAN"
            },
            {
                "enabled": True,
                "name": "SIGNATURE_UPDATE"
            }
        ],
        "onDemandScan": {
            "profile": "NORMAL",
            "scanCdDvd": "AUTOSCAN",
            "scanUsb": "AUTOSCAN",
            "schedule": {
                "days": None,
                "rangeHours": 0,
                "startHour": 0,
                "recoveryScanIfMissed": True
            }
        },
        "signatureUpdate": {
            "schedule": {
                "intervalHours": 2,
                "fullIntervalHours": 0,
                "initialRandomDelayHours": 1
            }
        }
    },
    "directoryActionRules": [
        {
            "actions": {
                "FILE_UPLOAD": False,
                "PROTECTION": False
            },
            "path": ""
        }
    ],
    "rules": [
        {
            "id": 1,
            "required": True,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "PUP"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 2,
            "required": True,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "data"
            },
            "operation": "MEMORY_SCRAPE"
        }
    ]
}

FULL_POLICY_2 = {
    "name": "default - S1",
    "org_key": "test",
    "priority_level": "MEDIUM",
    "description": "Hoopy Frood",
    "position": 2,
    "av_settings": {
        "avira_protection_cloud": {
            "enabled": False,
            "max_exe_delay": 45,
            "max_file_size": 4,
            "risk_level": 4
        },
        "on_access_scan": {
            "enabled": True,
            "mode": "NORMAL"
        },
        "on_demand_scan": {
            "enabled": True,
            "profile": "NORMAL",
            "schedule": {
                "days": None,
                "start_hour": 0,
                "range_hours": 0,
                "recovery_scan_if_missed": True
            },
            "scan_usb": "AUTOSCAN",
            "scan_cd_dvd": "AUTOSCAN"
        },
        "signature_update": {
            "enabled": True,
            "schedule": {
                "full_interval_hours": 0,
                "initial_random_delay_hours": 4,
                "interval_hours": 2
            }
        },
        "update_servers": {
            "servers_override": [],
            "servers_for_onsite_devices": [
                {
                    "server": "http://updates2.cdc.carbonblack.io/update2",
                    "preferred": False
                }
            ],
            "servers_for_offsite_devices": [
                "http://updates2.cdc.carbonblack.io/update2"
            ]
        }
    },
    "rules": [
        {
            "id": 1328,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "KNOWN_MALWARE"
            },
            "operation": "RUN"
        },
        {
            "id": 1329,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "COMPANY_BLACK_LIST"
            },
            "operation": "RUN"
        },
        {
            "id": 1330,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1331,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1332,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "PUP"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1333,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1334,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1335,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1336,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1337,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "INVOKE_SCRIPT"
        },
        {
            "id": 1338,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1339,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**/python"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1340,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1341,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1342,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1343,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1344,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\excel.exe"
            },
            "operation": "INVOKE_CMD_INTERPRETER"
        },
        {
            "id": 1345,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "RUN"
        },
        {
            "id": 1346,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "RUN_INMEMORY_CODE"
        },
        {
            "id": 1348,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "POL_INVOKE_NOT_TRUSTED"
        },
        {
            "id": 1349,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "INVOKE_CMD_INTERPRETER"
        },
        {
            "id": 1350,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "SIGNED_BY"
            },
            "operation": "NETWORK"
        },
        {
            "id": 1351,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "SUSPECT_MALWARE"
            },
            "operation": "RUN"
        }
    ],
    "directory_action_rules": [
        {
            "file_upload": False,
            "protection": False,
            "path": ""
        }
    ],
    "sensor_settings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "ALLOW_UPLOADS",
            "value": "false"
        },
        {
            "name": "SHOW_UI",
            "value": "true"
        },
        {
            "name": "ENABLE_THREAT_SHARING",
            "value": "true"
        },
        {
            "name": "QUARANTINE_DEVICE",
            "value": "false"
        },
        {
            "name": "LOGGING_LEVEL",
            "value": "false"
        },
        {
            "name": "QUARANTINE_DEVICE_MESSAGE",
            "value": "Your device has been quarantined. Please contact your administrator."
        },
        {
            "name": "SET_SENSOR_MODE",
            "value": "0"
        },
        {
            "name": "SENSOR_RESET",
            "value": "0"
        },
        {
            "name": "BACKGROUND_SCAN",
            "value": "false"
        },
        {
            "name": "POLICY_ACTION_OVERRIDE",
            "value": "true"
        },
        {
            "name": "HELP_MESSAGE",
            "value": ""
        },
        {
            "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
            "value": "false"
        },
        {
            "name": "HASH_MD5",
            "value": "false"
        },
        {
            "name": "SCAN_LARGE_FILE_READ",
            "value": "false"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "false"
        },
        {
            "name": "DELAY_EXECUTE",
            "value": "false"
        },
        {
            "name": "SCAN_NETWORK_DRIVE",
            "value": "false"
        },
        {
            "name": "BYPASS_AFTER_LOGIN_MINS",
            "value": "0"
        },
        {
            "name": "BYPASS_AFTER_RESTART_MINS",
            "value": "0"
        },
        {
            "name": "SHOW_FULL_UI",
            "value": "false"
        },
        {
            "name": "SECURITY_CENTER_OPT",
            "value": "true"
        },
        {
            "name": "CB_LIVE_RESPONSE",
            "value": "true"
        },
        {
            "name": "UNINSTALL_CODE",
            "value": "false"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        },
        {
            "name": "ALLOW_EXPEDITED_SCAN",
            "value": "false"
        },
        {
            "name": "RATE_LIMIT",
            "value": "0"
        },
        {
            "name": "CONNECTION_LIMIT",
            "value": "0"
        },
        {
            "name": "QUEUE_SIZE",
            "value": "100"
        },
        {
            "name": "LEARNING_MODE",
            "value": "0"
        }
    ],
    "version": 2
}

OLD_POLICY_2 = {
    "avSettings": {
        "apc": {
            "enabled": False,
            "maxExeDelay": 45,
            "maxFileSize": 4,
            "riskLevel": 4
        },
        "features": [
            {
                "enabled": True,
                "name": "SIGNATURE_UPDATE"
            },
            {
                "enabled": True,
                "name": "ONACCESS_SCAN"
            },
            {
                "enabled": True,
                "name": "ONDEMAND_SCAN"
            }
        ],
        "onAccessScan": {
            "profile": "NORMAL"
        },
        "onDemandScan": {
            "profile": "NORMAL",
            "schedule": {
                "days": None,
                "startHour": 0,
                "rangeHours": 0,
                "recoveryScanIfMissed": True
            },
            "scanUsb": "AUTOSCAN",
            "scanCdDvd": "AUTOSCAN"
        },
        "signatureUpdate": {
            "schedule": {
                "fullIntervalHours": 0,
                "initialRandomDelayHours": 4,
                "intervalHours": 2
            }
        },
        "updateServers": {
            "serversOverride": [],
            "servers": [
                {
                    "flags": 0,
                    "regId": None,
                    "server": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ],
                }
            ],
            "serversForOffSiteDevices": [
                "http://updates2.cdc.carbonblack.io/update2"
            ]
        }
    },
    "directoryActionRules": [
        {
            "actions": {
                "FILE_UPLOAD": False,
                "PROTECTION": False
            },
            "path": ""
        }
    ],
    "id": 91849,
    "rules": [
        {
            "id": 1328,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "KNOWN_MALWARE"
            },
            "operation": "RUN"
        },
        {
            "id": 1329,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "COMPANY_BLACK_LIST"
            },
            "operation": "RUN"
        },
        {
            "id": 1330,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1331,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1332,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "PUP"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1333,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1334,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1335,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1336,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "RANSOM"
        },
        {
            "id": 1337,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "INVOKE_SCRIPT"
        },
        {
            "id": 1338,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1339,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**/python"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1340,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1341,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 1342,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1343,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 1344,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\excel.exe"
            },
            "operation": "INVOKE_CMD_INTERPRETER"
        },
        {
            "id": 1345,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "RUN"
        },
        {
            "id": 1346,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "RUN_INMEMORY_CODE"
        },
        {
            "id": 1348,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "POL_INVOKE_NOT_TRUSTED"
        },
        {
            "id": 1349,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "/Users/*/Downloads/**"
            },
            "operation": "INVOKE_CMD_INTERPRETER"
        },
        {
            "id": 1350,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "SIGNED_BY"
            },
            "operation": "NETWORK"
        },
        {
            "id": 1351,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "SUSPECT_MALWARE"
            },
            "operation": "RUN"
        }
    ],
    "sensorSettings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "ALLOW_UPLOADS",
            "value": "false"
        },
        {
            "name": "SHOW_UI",
            "value": "true"
        },
        {
            "name": "ENABLE_THREAT_SHARING",
            "value": "true"
        },
        {
            "name": "QUARANTINE_DEVICE",
            "value": "false"
        },
        {
            "name": "LOGGING_LEVEL",
            "value": "false"
        },
        {
            "name": "QUARANTINE_DEVICE_MESSAGE",
            "value": "Your device has been quarantined. Please contact your administrator."
        },
        {
            "name": "SET_SENSOR_MODE",
            "value": "0"
        },
        {
            "name": "SENSOR_RESET",
            "value": "0"
        },
        {
            "name": "BACKGROUND_SCAN",
            "value": "false"
        },
        {
            "name": "POLICY_ACTION_OVERRIDE",
            "value": "true"
        },
        {
            "name": "HELP_MESSAGE",
            "value": ""
        },
        {
            "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
            "value": "false"
        },
        {
            "name": "HASH_MD5",
            "value": "false"
        },
        {
            "name": "SCAN_LARGE_FILE_READ",
            "value": "false"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "false"
        },
        {
            "name": "DELAY_EXECUTE",
            "value": "false"
        },
        {
            "name": "SCAN_NETWORK_DRIVE",
            "value": "false"
        },
        {
            "name": "BYPASS_AFTER_LOGIN_MINS",
            "value": "0"
        },
        {
            "name": "BYPASS_AFTER_RESTART_MINS",
            "value": "0"
        },
        {
            "name": "SHOW_FULL_UI",
            "value": "false"
        },
        {
            "name": "SECURITY_CENTER_OPT",
            "value": "true"
        },
        {
            "name": "CB_LIVE_RESPONSE",
            "value": "true"
        },
        {
            "name": "UNINSTALL_CODE",
            "value": "false"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        },
        {
            "name": "ALLOW_EXPEDITED_SCAN",
            "value": "false"
        },
        {
            "name": "RATE_LIMIT",
            "value": "0"
        },
        {
            "name": "CONNECTION_LIMIT",
            "value": "0"
        },
        {
            "name": "QUEUE_SIZE",
            "value": "100"
        },
        {
            "name": "LEARNING_MODE",
            "value": "0"
        }
    ]
}

RULE_ADD_1 = {
    "required": True,
    "action": "TERMINATE",
    "application": {
        "type": "SIGNED_BY",
        "value": "something"
    },
    "operation": "RANSOM"
}

RULE_ADD_2 = {
    "id": 409,
    "required": True,
    "action": "TERMINATE",
    "application": {
        "type": "SIGNED_BY",
        "value": "something"
    },
    "operation": "RANSOM"
}

RULE_MODIFY_1 = {
    "id": 2,
    "required": True,
    "action": "TERMINATE",
    "application": {
        "type": "NAME_PATH",
        "value": "data"
    },
    "operation": "MEMORY_SCRAPE"
}

NEW_POLICY_CONSTRUCT_1 = {
    "name": "New Policy Name",
    "org_key": "test",
    "priority_level": "HIGH",
    "version": 2,
    "is_system": False,
    "description": "Foobar",
    "auto_deregister_inactive_vdi_interval_ms": 1000,
    "auto_delete_known_bad_hashes_delay": 500,
    "av_settings": {
        "avira_protection_cloud": {
            "enabled": True,
            "max_exe_delay": 3600,
            "max_file_size": 1024,
            "risk_level": 5
        },
        "on_access_scan": {
            "enabled": True,
            "mode": "AGGRESSIVE"
        },
        "on_demand_scan": {
            "enabled": True,
            "profile": "AGGRESSIVE",
            "schedule": {
                "days": ["MONDAY", "WEDNESDAY", "FRIDAY"],
                "start_hour": 6,
                "range_hours": 4,
                "recovery_scan_if_missed": False
            },
            "scan_usb": "DISABLED",
            "scan_cd_dvd": "DISABLED"
        },
        "signature_update": {
            "enabled": True,
            "schedule": {
                "full_interval_hours": 12,
                "initial_random_delay_hours": 3,
                "interval_hours": 6
            }
        },
        "update_servers": {
            "servers_override": ["http://contoso.com/foo"],
            "servers_for_onsite_devices": [
                {
                    "server": "http://example.com/foo",
                    "preferred": False
                },
                {
                    "server": "http://example.org/foo",
                    "preferred": True
                }
            ],
            "servers_for_offsite_devices": [
                "http://amytapie.com/foo"
            ]
        }
    },
    "directory_action_rules": [
        {
            "file_upload": True,
            "protection": True,
            "path": "/usr"
        },
        {
            "file_upload": False,
            "protection": False,
            "path": "/tmp"
        }
    ],
    "rules": [
        {
            "required": True,
            "action": "TERMINATE",
            "application": {
                "type": "SIGNED_BY",
                "value": "something"
            },
            "operation": "RANSOM"
        },
        {
            "required": False,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "COMPANY_BLACK_LIST"
            },
            "operation": "RUN"
        }
    ],
    "sensor_settings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        }
    ],
    "managed_detection_response_permissions": {
        "policy_modification": False,
        "quarantine": True
    },
    "rule_configs": [
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "inherited_from": "",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "inherited_from": "",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        }
    ]
}

NEW_POLICY_RETURN_1 = {
    "id": 30250,
    "name": "New Policy Name",
    "org_key": "test",
    "priority_level": "HIGH",
    "position": 6,
    "version": 2,
    "is_system": False,
    "description": "Foobar",
    "auto_deregister_inactive_vdi_interval_ms": 1000,
    "auto_delete_known_bad_hashes_delay": 500,
    "av_settings": {
        "avira_protection_cloud": {
            "enabled": True,
            "max_exe_delay": 3600,
            "max_file_size": 1024,
            "risk_level": 5
        },
        "on_access_scan": {
            "enabled": True,
            "mode": "AGGRESSIVE"
        },
        "on_demand_scan": {
            "enabled": True,
            "profile": "AGGRESSIVE",
            "schedule": {
                "days": ["MONDAY", "WEDNESDAY", "FRIDAY"],
                "start_hour": 6,
                "range_hours": 4,
                "recovery_scan_if_missed": False
            },
            "scan_usb": "DISABLED",
            "scan_cd_dvd": "DISABLED"
        },
        "signature_update": {
            "enabled": True,
            "schedule": {
                "full_interval_hours": 12,
                "initial_random_delay_hours": 3,
                "interval_hours": 6
            }
        },
        "update_servers": {
            "servers_override": ["http://contoso.com/foo"],
            "servers_for_onsite_devices": [
                {
                    "server": "http://example.com/foo",
                    "preferred": False
                },
                {
                    "server": "http://example.org/foo",
                    "preferred": True
                }
            ],
            "servers_for_offsite_devices": [
                "http://amytapie.com/foo"
            ]
        }
    },
    "directory_action_rules": [
        {
            "file_upload": True,
            "protection": True,
            "path": "/usr"
        },
        {
            "file_upload": False,
            "protection": False,
            "path": "/tmp"
        }
    ],
    "rules": [
        {
            "id": 1,
            "required": True,
            "action": "TERMINATE",
            "application": {
                "type": "SIGNED_BY",
                "value": "something"
            },
            "operation": "RANSOM"
        },
        {
            "id": 2,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "REPUTATION",
                "value": "COMPANY_BLACK_LIST"
            },
            "operation": "RUN"
        }
    ],
    "sensor_settings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "true"
        }
    ],
    "managed_detection_response_permissions": {
        "policy_modification": False,
        "quarantine": True
    },
    "rule_configs": [
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "name": "Authentication Events",
            "description": "Authentication Events",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_auth_events": True
            }
        },
        {
            "id": "1f8a5e4b-34f2-4d31-9f8f-87c56facaec8",
            "name": "Advanced Scripting Prevention",
            "description": "Addresses malicious fileless and file-backed scripts that leverage native programs [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "description": "Addresses threat actors obtaining credentials and relies on detecting the malicious [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
            "name": "Carbon Black Threat Intel",
            "description": "Addresses common and pervasive TTPs used for malicious activity as well as [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "description": "Addresses behaviors that indicate a threat actor has gained elevated access via [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        }
    ]
}

BASIC_CONFIG_TEMPLATE_RETURN = {
    "type": "object",
    "properties": {
        "WindowsAssignmentMode": {
            "default": "BLOCK",
            "description": "Used to change assignment mode to PREVENT or BLOCK",
            "type": "string",
            "enum": [
                "REPORT",
                "BLOCK"
            ]
        }
    }
}

TEMPLATE_RETURN_BOGUS_TYPE = {
    "type": "object",
    "properties": {
        "WindowsAssignmentMode": {
            "default": "BLOCK",
            "description": "Used to change assignment mode to PREVENT or BLOCK",
            "type": "bogus"
        }
    }
}

POLICY_CONFIG_PRESENTATION = {
    "configs": [
        {
            "id": "cc075469-8d1e-4056-84b6-0e6f437c4010",
            "name": "XDR",
            "description": "Turns on XDR network data collection at the sensor",
            "presentation": {
                "category": "data_collection"
            },
            "parameters": []
        },
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "name": "Authentication Events",
            "description": "Turns on Windows authentication events at the sensor",
            "presentation": {
                "category": "data_collection"
            },
            "parameters": []
        },
        {
            "id": "1c03d653-eca4-4adc-81a1-04b17b6cbffc",
            "name": "Event Reporting and Sensor Operation Exclusions",
            "description": "Allows customers to exclude specific processes and process events from reporting to CBC",
            "presentation": {
                "name": "process_exclusion.name",
                "category": "bypass",
                "description": [
                    "process_exclusion.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "exclusions": {
                            "criteria": [
                                "initiator_process",
                                "operations"
                            ],
                            "additional_attributes": [
                                "type",
                                "inheritence"
                            ]
                        }
                    }
                ]
            },
            "parameters": []
        },
        {
            "id": "0aa2b31a-f938-4cf9-acee-7cf7b810eb79",
            "name": "Background Scan",
            "description": "This rapid config handles DRE rules and sensor settings associated with Background Scan",
            "presentation": {
                "category": "sensor_settings"
            },
            "parameters": []
        },
        {
            "id": "1664f2e6-645f-4d6e-98ec-0c80485cbe0f",
            "name": "Event Reporting Exclusions",
            "description": "Allows customers to exclude specific processes from reporting events to CBC",
            "presentation": {
                "name": "event_reporting_exclusion.name",
                "category": "bypass",
                "description": [
                    "event_reporting_exclusion.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "exclusions": {
                            "criteria": [
                                "initiator_process",
                                "operations"
                            ],
                            "additional_attributes": [
                                "type",
                                "inheritence"
                            ]
                        }
                    }
                ]
            },
            "parameters": []
        },
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor."
            " The Definition will be part of Main Policies.",
            "presentation": {
                "category": "hbfw"
            },
            "parameters": []
        },
        {
            "id": "1f8a5e4b-34f2-4d31-9f8f-87c56facaec8",
            "name": "Advanced Scripting Prevention",
            "description": "Addresses malicious fileless and file-backed scripts that leverage native programs"
            " and common scripting languages.",
            "presentation": {
                "name": "amsi.name",
                "category": "core-prevention",
                "description": [
                    "amsi.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "amsi.windows.heading",
                        "subHeader": [
                            "amsi.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "description": "Addresses threat actors obtaining credentials and relies on detecting the malicious use of"
            " TTPs/behaviors that indicate such activity.",
            "presentation": {
                "name": "cred_theft.name",
                "category": "core-prevention",
                "description": [
                    "cred_theft.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "cred_theft.windows.heading",
                        "subHeader": [
                            "cred_theft.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "491dd777-5a76-4f58-88bf-d29926d12778",
            "name": "Prevalent Module Exclusions",
            "description": "Collects events created when a process loads a common library. Enabling this will increase"
            " the number of events reported for expected process behavior.",
            "presentation": {
                "category": "data_collection"
            },
            "parameters": []
        },
        {
            "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
            "name": "Carbon Black Threat Intel",
            "description": "Addresses common and pervasive TTPs used for malicious activity as well as living off the"
            " land TTPs/behaviors detected by Carbon Black’s Threat Analysis Unit.",
            "presentation": {
                "name": "cbti.name",
                "category": "core-prevention",
                "description": [
                    "cbti.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "cbti.windows.heading",
                        "subHeader": [
                            "cbti.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "description": "Addresses behaviors that indicate a threat actor has gained elevated access via a bug or"
            " misconfiguration within an operating system, and leverages the detection of TTPs/behaviors to prevent"
            " such activity.",
            "presentation": {
                "name": "privesc.name",
                "category": "core-prevention",
                "description": [
                    "privesc.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "privesc.windows.heading",
                        "subHeader": [
                            "privesc.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "97a03cc2-5796-4864-b16d-790d06bea20d",
            "name": "Defense Evasion",
            "description": "Addresses common TTPs/behaviors that threat actors use to avoid detection such as"
            " uninstalling or disabling security software, obfuscating or encrypting data/scripts and abusing"
            " trusted processes to hide and disguise their malicious activity.",
            "presentation": {
                "name": "defense_evasion.name",
                "category": "core-prevention",
                "description": [
                    "defense_evasion.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "defense_evasion.windows.heading",
                        "subHeader": [
                            "defense_evasion.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "id": "8a16234c-9848-473a-a803-f0f0ffaf5f29",
            "name": "Persistence",
            "description": "Addresses common TTPs/behaviors that threat actors use to retain access to systems across"
            " restarts, changed credentials, and other interruptions that could cut off their access.",
            "presentation": {
                "name": "persistence.name",
                "category": "core-prevention",
                "description": [
                    "persistence.description"
                ],
                "platforms": [
                    {
                        "platform": "WINDOWS",
                        "header": "persistence.windows.heading",
                        "subHeader": [
                            "persistence.windows.sub_heading"
                        ],
                        "actions": [
                            {
                                "component": "assignment-mode-selector",
                                "parameter": "WindowsAssignmentMode"
                            }
                        ]
                    }
                ]
            },
            "parameters": [
                {
                    "default": "BLOCK",
                    "name": "WindowsAssignmentMode",
                    "description": "Used to change assignment mode to PREVENT or BLOCK",
                    "recommended": "BLOCK",
                    "validations": [
                        {
                            "type": "enum",
                            "values": [
                                "REPORT",
                                "BLOCK"
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

REPLACE_RULECONFIG = {
    "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
    "name": "Privilege Escalation",
    "description": "Addresses behaviors that indicate a threat actor has gained elevated access via [...]",
    "inherited_from": "psc:region",
    "category": "core_prevention",
    "parameters": {
        "WindowsAssignmentMode": "REPORT"
    }
}

BUILD_RULECONFIG_1 = {
    "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
    "name": "Privilege Escalation",
    "inherited_from": "",
    "category": "core_prevention",
    "parameters": {
        "WindowsAssignmentMode": "BLOCK"
    }
}

FULL_POLICY_5 = {
    "id": 1492,
    "name": "Crapco",
    "org_key": "test",
    "priority_level": "MEDIUM",
    "position": 5,
    "is_system": False,
    "description": "If you buy this, you'll buy ANYTHING!",
    "auto_deregister_inactive_vdi_interval_ms": 0,
    "auto_deregister_inactive_vm_workloads_interval_ms": 0,
    "update_time": 1682625002305,
    "av_settings": {
        "avira_protection_cloud": {
            "enabled": True,
            "max_exe_delay": 45,
            "max_file_size": 4,
            "risk_level": 4
        },
        "on_access_scan": {
            "enabled": True,
            "mode": "NORMAL"
        },
        "on_demand_scan": {
            "enabled": True,
            "profile": "NORMAL",
            "schedule": {
                "start_hour": 0,
                "range_hours": 0,
                "recovery_scan_if_missed": True
            },
            "scan_usb": "AUTOSCAN",
            "scan_cd_dvd": "AUTOSCAN"
        },
        "signature_update": {
            "enabled": True,
            "schedule": {
                "full_interval_hours": 0,
                "initial_random_delay_hours": 4,
                "interval_hours": 4
            }
        },
        "update_servers": {
            "servers_override": [],
            "servers_for_onsite_devices": [
                {
                    "server": "http://updates2.cdc.carbonblack.io/update2",
                    "preferred": False
                }
            ],
            "servers_for_offsite_devices": [
                "http://updates2.cdc.carbonblack.io/update2"
            ]
        }
    },
    "rules": [
        {
            "id": 15,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "KNOWN_MALWARE"
            },
            "operation": "RUN"
        },
        {
            "id": 16,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "COMPANY_BLACK_LIST"
            },
            "operation": "RUN"
        },
        {
            "id": 17,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "SUSPECT_MALWARE"
            },
            "operation": "RUN"
        },
        {
            "id": 18,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "PUP"
            },
            "operation": "RUN"
        },
        {
            "id": 19,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 20,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "RESOLVING"
            },
            "operation": "RANSOM"
        },
        {
            "id": 21,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 22,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "REPUTATION",
                "value": "ADAPTIVE_WHITE_LIST"
            },
            "operation": "RANSOM"
        },
        {
            "id": 23,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\powershell*.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 24,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**/python"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 25,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 26,
            "required": False,
            "action": "TERMINATE",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "MEMORY_SCRAPE"
        },
        {
            "id": 27,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\wscript.exe"
            },
            "operation": "CODE_INJECTION"
        },
        {
            "id": 28,
            "required": False,
            "action": "DENY",
            "application": {
                "type": "NAME_PATH",
                "value": "**\\cscript.exe"
            },
            "operation": "CODE_INJECTION"
        }
    ],
    "directory_action_rules": [],
    "sensor_settings": [
        {
            "name": "ALLOW_UNINSTALL",
            "value": "true"
        },
        {
            "name": "SHOW_UI",
            "value": "true"
        },
        {
            "name": "ENABLE_THREAT_SHARING",
            "value": "true"
        },
        {
            "name": "QUARANTINE_DEVICE",
            "value": "false"
        },
        {
            "name": "LOGGING_LEVEL",
            "value": "false"
        },
        {
            "name": "QUARANTINE_DEVICE_MESSAGE",
            "value": "Device has been quarantined by your computer administrator."
        },
        {
            "name": "SET_SENSOR_MODE",
            "value": "0"
        },
        {
            "name": "SENSOR_RESET",
            "value": "0"
        },
        {
            "name": "BACKGROUND_SCAN",
            "value": "true"
        },
        {
            "name": "POLICY_ACTION_OVERRIDE",
            "value": "true"
        },
        {
            "name": "HELP_MESSAGE",
            "value": ""
        },
        {
            "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
            "value": "false"
        },
        {
            "name": "HASH_MD5",
            "value": "false"
        },
        {
            "name": "SCAN_LARGE_FILE_READ",
            "value": "false"
        },
        {
            "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
            "value": "true"
        },
        {
            "name": "DELAY_EXECUTE",
            "value": "true"
        },
        {
            "name": "SCAN_NETWORK_DRIVE",
            "value": "false"
        },
        {
            "name": "BYPASS_AFTER_LOGIN_MINS",
            "value": "0"
        },
        {
            "name": "BYPASS_AFTER_RESTART_MINS",
            "value": "0"
        },
        {
            "name": "SHOW_FULL_UI",
            "value": "false"
        },
        {
            "name": "SECURITY_CENTER_OPT",
            "value": "true"
        },
        {
            "name": "CB_LIVE_RESPONSE",
            "value": "false"
        },
        {
            "name": "ALLOW_INLINE_BLOCKING",
            "value": "true"
        },
        {
            "name": "UNINSTALL_CODE",
            "value": "false"
        },
        {
            "name": "DEFENSE_OPT_OUT",
            "value": "false"
        },
        {
            "name": "UBS_OPT_IN",
            "value": "false"
        }
    ],
    "rule_configs": [
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "name": "Authentication Events",
            "description": "Authentication Events",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_auth_events": True
            }
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "description": "Addresses threat actors obtaining credentials and relies on detecting the malicious [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
            "name": "Carbon Black Threat Intel",
            "description": "Addresses common and pervasive TTPs used for malicious activity as well as [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...]",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                                "test_mode": True
                            },
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsofDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                                "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                                "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    },
                    {
                        "description": "IRC is a sewer",
                        "name": "Isolate",
                        "rules": [
                            {
                                "action": "BLOCK_ALERT",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "BlockIRC",
                                "protocol": "TCP",
                                "remote_ip_address": "26.2.0.74",
                                "remote_port_ranges": "6667",
                                "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                                "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                                "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                                "test_mode": False
                            },
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsOfDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                                "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                                "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    },
                    {
                        "description": "IRC is a sewer",
                        "name": "Isolate",
                        "rules": [
                            {
                                "action": "BLOCK_ALERT",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "BlockIRC",
                                "protocol": "TCP",
                                "remote_ip_address": "26.2.0.74",
                                "remote_port_ranges": "6667",
                                "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                                "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                                "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "e6da6ec1-2e04-4fe7-a864-c4db940510c3",
                    "default_rule_inbound_event_check_guid": "6d38dce5-d2b2-4572-b61c-3d0bbefddbdb",
                    "default_rule_outbound_event_check_guid": "26257374-2e78-46ea-b252-1e9916a885d4"
                },
                "enable_host_based_firewall": False
            }
        },
        {
            "id": "1f8a5e4b-34f2-4d31-9f8f-87c56facaec8",
            "name": "Advanced Scripting Prevention",
            "description": "Addresses malicious fileless and file-backed scripts that leverage native programs [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "description": "Addresses behaviors that indicate a threat actor has gained elevated access via [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "97a03cc2-5796-4864-b16d-790d06bea20d",
            "name": "Defense Evasion",
            "description": "Addresses common TTPs/behaviors that threat actors use to avoid detection such as [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "8a16234c-9848-473a-a803-f0f0ffaf5f29",
            "name": "Persistence",
            "description": "Addresses common TTPs/behaviors that threat actors use to retain access to systems [...].",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        }
    ],
    "sensor_configs": []
}

SET_XDR_COLLECTION_REQUEST = {
    "id": "cc075469-8d1e-4056-84b6-0e6f437c4010",
    "parameters": {
        "enable_network_data_collection": True
    }
}

SET_XDR_COLLECTION_RESPONSE = {
    "successful": [
        {
            "id": "cc075469-8d1e-4056-84b6-0e6f437c4010",
            "name": "XDR",
            "description": "Turns on XDR network data collection at the sensor",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_network_data_collection": True
            }
        }
    ],
    "failed": []
}

SET_AUTH_EVENT_COLLECTION_REQUEST = {
    "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
    "parameters": {
        "enable_auth_events": False
    }
}

SET_AUTH_EVENT_COLLECTION_RESPONSE = {
    "successful": [
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "name": "Authentication Events",
            "description": "Authentication Events",
            "inherited_from": "",
            "category": "data_collection",
            "parameters": {
                "enable_auth_events": False
            }
        }
    ],
    "failed": []
}

SET_AUTH_EVENT_COLLECTION_RESPONSE_ERROR = {
    "successful": [],
    "failed": [
        {
            "id": "91c919da-fb90-4e63-9eac-506255b0a0d0",
            "error_code": "TESTING_ERROR",
            "message": "Test error"
        }
    ]
}

PREVIEW_POLICY_CHANGES_REQUEST1 = {
    "policies": [
        {
            "id": 10240,
            "position": 1
        }
    ]
}

PREVIEW_POLICY_CHANGES_RESPONSE1 = {
    "preview": [
        {
            "current_policy": {
                "id": 70722,
                "position": 2
            },
            "new_policy": {
                "id": 10240,
                "position": 1
            },
            "asset_count": 5,
            "asset_query": "(-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:1790b51e683c8a20c2b2bbe3e41eacdc53e3632087bb5a3f2868588e99157b06 AND policy_override:false) OR (-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:aa8bd7e69c4ee45918bb126a17d90a1c8368b46f9bb5bf430cb0250c317cd1dc AND policy_override:false)"  # noqa: E501
        },
        {
            "current_policy": {
                "id": 142857,
                "position": 1
            },
            "new_policy": {
                "id": 10240,
                "position": 1
            },
            "asset_count": 2,
            "asset_query": "(ag_agg_key_manual:1790b51e683c8a20c2b2bbe3e41eacdc53e3632087bb5a3f2868588e99157b06 AND ag_agg_key_dynamic:51f32868cdd197b491093617b259ea2f4a93550b7c130636df8d48e94d37c4c8 AND policy_override:false)"  # noqa: E501
        }
    ]
}

PREVIEW_POLICY_CHANGES_REQUEST2 = {
    "policies": [
        {
            "id": 65536,
            "position": 1
        }
    ]
}

PREVIEW_POLICY_CHANGES_RESPONSE2 = {
    "preview": [
        {
            "current_policy": {
                "id": 1492,
                "position": 2
            },
            "new_policy": {
                "id": 65536,
                "position": 1
            },
            "asset_count": 5,
            "asset_query": "(-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:1790b51e683c8a20c2b2bbe3e41eacdc53e3632087bb5a3f2868588e99157b06 AND policy_override:false) OR (-_exists_:ag_agg_key_dynamic AND ag_agg_key_manual:aa8bd7e69c4ee45918bb126a17d90a1c8368b46f9bb5bf430cb0250c317cd1dc AND policy_override:false)"  # noqa: E501
        },
        {
            "current_policy": {
                "id": 74656,
                "position": 1
            },
            "new_policy": {
                "id": 65536,
                "position": 1
            },
            "asset_count": 2,
            "asset_query": "(ag_agg_key_manual:1790b51e683c8a20c2b2bbe3e41eacdc53e3632087bb5a3f2868588e99157b06 AND ag_agg_key_dynamic:51f32868cdd197b491093617b259ea2f4a93550b7c130636df8d48e94d37c4c8 AND policy_override:false)"  # noqa: E501
        }
    ]
}

ADD_POLICY_OVERRIDE_REQUEST = {
    "action": "ADD_POLICY_OVERRIDE",
    "asset_ids": [123, 456, 789],
    "policy_id": 65536
}

ADD_POLICY_OVERRIDE_RESPONSE = {
    "preview": [
        {
            "current_policy": {
                "id": 11200,
                "position": 2
            },
            "new_policy": {
                "id": 65536,
                "position": 1
            },
            "asset_count": 3,
            "asset_query": "(device_id: 123 OR 456 OR 789)",
            "assets_search_definition": {
                "query": "(device_id: 123 OR 456 OR 789)"
            }
        }
    ]
}
