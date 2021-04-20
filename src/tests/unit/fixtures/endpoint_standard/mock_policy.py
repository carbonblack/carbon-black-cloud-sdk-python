"""Mock responses for policy queries."""

POLICY_GET_SPECIFIC_RESP = {
    "policyInfo": {
        "id": 7049,
        "priorityLevel": "LOW",
        "systemPolicy": False,
        "latestRevision": 1505155560455,
        "policy": {
            "sensorSettings": [{
                "name": "SHOW_UI",
                "value": "True"
            }, {
                "name": "BACKGROUND_SCAN",
                "value": "True"
            }],
            "id": -1
        },
        "version": 2,
        "description": "test policy for documentation"
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_RESP = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "latestRevision": 1598397737423,
        "id": 30241,
        "systemPolicy": False,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "value": "COMPANY_BLACK_LIST",
                        "type": "REPUTATION"
                    },
                    "action": "TERMINATE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_RESP_1 = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "latestRevision": 1598397737423,
        "id": 30242,
        "systemPolicy": False,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "value": "COMPANY_BLACK_LIST",
                        "type": "REPUTATION"
                    },
                    "action": "TERMINATE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_RESP_2 = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "latestRevision": 1598397737423,
        "id": 30243,
        "systemPolicy": False,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "value": "COMPANY_BLACK_LIST",
                        "type": "REPUTATION"
                    },
                    "action": "TERMINATE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_POST_RESP = {
    "policyId": 30241,
    "success": True,
    "message": "Success"
}

POLICY_UPDATE_RESP = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "latestRevision": 1598397737423,
        "id": 30242,
        "systemPolicy": False,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "value": "COMPANY_BLACK_LIST",
                        "type": "REPUTATION"
                    },
                    "action": "TERMINATE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "newFakeName",
        "description": "",
        "testId": 1
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_WITH_NEW_RULE_RESP = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "id": 30241,
        "systemPolicy": False,
        "latestRevision": 1598468096918,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
                        "initialRandomDelayHours": 1,
                        "fullIntervalHours": 0
                    }
                }
            },
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "type": "REPUTATION",
                        "value": "COMPANY_BLACK_LIST"
                    },
                    "action": "TERMINATE"
                },
                {
                    "id": 21,
                    "required": True,
                    "operation": "RUN",
                    "application": {
                        "type": "NAME_PATH",
                        "value": "my_path_test"
                    },
                    "action": "DENY"
                },
                {
                    "id": 22,
                    "required": True,
                    "operation": "RUN",
                    "application": {
                        "type": "NAME_PATH",
                        "value": "my_path_test_2"
                    },
                    "action": "DENY"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_WITH_MODIFIED_RULE_RESP = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "id": 30241,
        "systemPolicy": False,
        "latestRevision": 1598468096918,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
                        "initialRandomDelayHours": 1,
                        "fullIntervalHours": 0
                    }
                }
            },
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "type": "REPUTATION",
                        "value": "COMPANY_BLACK_LIST"
                    },
                    "action": "TERMINATE"
                },
                {
                    "id": 22,
                    "required": True,
                    "operation": "RUN",
                    "application": {
                        "type": "NAME_PATH",
                        "value": "new_test_path"
                    },
                    "action": "IGNORE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_GET_WITH_DELETED_RULE_RESP = {
    "policyInfo": {
        "priorityLevel": "LOW",
        "latestRevision": 1598397737423,
        "id": 30241,
        "systemPolicy": False,
        "version": 2,
        "policy": {
            "avSettings": {
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
                        "enabled": False,
                        "name": "ONDEMAND_SCAN"
                    }
                ],
                "updateServers": {
                    "servers": [
                        {
                            "flags": 0,
                            "regId": None,
                            "server": [
                                "http://updates2.cdc.carbonblack.io/update2"
                            ]
                        }
                    ],
                    "serversForOffSiteDevices": [
                        "http://updates2.cdc.carbonblack.io/update2"
                    ]
                },
                "apc": {
                    "maxFileSize": 4,
                    "maxExeDelay": 45,
                    "riskLevel": 4,
                    "enabled": False
                },
                "onAccessScan": {
                    "profile": "AGGRESSIVE"
                },
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
            "sensorSettings": [
                {
                    "name": "ALLOW_UNINSTALL",
                    "value": "True"
                },
                {
                    "name": "ALLOW_UPLOADS",
                    "value": "True"
                },
                {
                    "name": "SHOW_UI",
                    "value": "True"
                },
                {
                    "name": "ENABLE_THREAT_SHARING",
                    "value": "True"
                },
                {
                    "name": "QUARANTINE_DEVICE",
                    "value": "False"
                },
                {
                    "name": "LOGGING_LEVEL",
                    "value": "False"
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
                    "value": "True"
                },
                {
                    "name": "POLICY_ACTION_OVERRIDE",
                    "value": "True"
                },
                {
                    "name": "HELP_MESSAGE",
                    "value": ""
                },
                {
                    "name": "SCAN_NETWORK_DRIVE",
                    "value": "False"
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
                    "value": "False"
                },
                {
                    "name": "SCAN_EXECUTE_ON_NETWORK_DRIVE",
                    "value": "False"
                },
                {
                    "name": "DELAY_EXECUTE",
                    "value": "True"
                },
                {
                    "name": "PRESERVE_SYSTEM_MEMORY_SCAN",
                    "value": "False"
                },
                {
                    "name": "HASH_MD5",
                    "value": "False"
                },
                {
                    "name": "SCAN_LARGE_FILE_READ",
                    "value": "False"
                },
                {
                    "name": "SECURITY_CENTER_OPT",
                    "value": "True"
                },
                {
                    "name": "CB_LIVE_RESPONSE",
                    "value": "True"
                },
                {
                    "name": "UNINSTALL_CODE",
                    "value": "True"
                },
                {
                    "name": "UBS_OPT_IN",
                    "value": "True"
                },
                {
                    "name": "ALLOW_EXPEDITED_SCAN",
                    "value": "True"
                }
            ],
            "directoryActionRules": [],
            "rules": [
                {
                    "id": 1,
                    "required": True,
                    "operation": "RANSOM",
                    "application": {
                        "value": "COMPANY_BLACK_LIST",
                        "type": "REPUTATION"
                    },
                    "action": "TERMINATE"
                }
            ],
            "knownBadHashAutoDeleteDelayMs": None,
            "id": -1
        },
        "name": "Lyon_test",
        "description": ""
    },
    "success": True,
    "message": "Success"
}

POLICY_POST_RULE_RESP = {
    "ruleId": 21,
    "success": True,
    "message": "Success"
}

POLICY_MODIFY_RULE_RESP = {
    "success": True,
    "message": "Success"
}

POLICY_DELETE_RULE_RESP = {
    "success": True,
    "message": "Success"
}
