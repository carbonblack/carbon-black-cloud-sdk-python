"""Mock responses for Policy"""


FULL_POLICY_1 = {
    "id": 65536,
    "name": "A Dummy Policy",
    "org_key": "test",
    "priority_level": "HIGH",
    "position": -1,
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
    "rapid_configs": []
}

SUMMARY_POLICY_1 = {
    "id": 65536,
    "name": "A Dummy Policy",
    "priority_level": "HIGH",
    "position": -1,
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
    "position": -1,
    "num_devices": 0
}

SUMMARY_POLICY_3 = {
    "id": 74656,
    "is_system": True,
    "name": "Remediant AC Policy",
    "description": "Verifying AC capabilities ",
    "priority_level": "LOW",
    "position": -1,
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
    "rapid_configs": []
}

NEW_POLICY_RETURN_1 = {
    "id": 30250,
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
    "rapid_configs": []
}
