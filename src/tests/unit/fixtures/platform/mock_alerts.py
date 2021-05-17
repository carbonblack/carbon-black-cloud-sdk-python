"""Mock responses for alert queries."""

GET_ALERT_RESP = {
    "type": "CB_ANALYTICS",
    "id": "86123310980efd0b38111eba4bfa5e98aa30b19",
    "legacy_alert_id": "62802DCE",
    "org_key": "4JDT3MX9Q",
    "create_time": "2021-05-13T00:20:46.474Z",
    "last_update_time": "2021-05-13T00:27:22.846Z",
    "first_event_time": "2021-05-13T00:20:13.043Z",
    "last_event_time": "2021-05-13T00:20:13.044Z",
    "threat_id": "a26842be6b54ea2f58848b23a3461a16",
    "severity": 1,
    "category": "MONITORED",
    "device_id": 8612331,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_name": "win-2016-devrel",
    "device_username": "Administrator",
    "policy_id": 7113786,
    "policy_name": "Standard",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "None",
        "last_update_time": "2021-05-13T00:20:46.474Z",
        "comment": "None",
        "changed_by": "Carbon Black"
    },
    "notes_present": False,
    "tags": "None",
    "reason": "A port scan was detected from 10.169.255.100 on an external network (off-prem).",
    "reason_code": "R_SCAN_OFF",
    "process_name": "svchost.exe",
    "device_location": "OFFSITE",
    "created_by_event_id": "0980efd0b38111eba4bfa5e98aa30b19",
    "threat_indicators": [
        {
            "process_name": "svchost.exe",
            "sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "ttps": [
                "ACTIVE_SERVER",
                "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                "NETWORK_ACCESS",
                "PORTSCAN"
            ]
        }
    ],
    "threat_activity_dlp": "NOT_ATTEMPTED",
    "threat_activity_phish": "NOT_ATTEMPTED",
    "threat_activity_c2": "NOT_ATTEMPTED",
    "threat_cause_actor_sha256": "10.169.255.100",
    "threat_cause_actor_name": "svchost.exe -k RPCSS -p",
    "threat_cause_actor_process_pid": "868-132563418721238249-0",
    "threat_cause_process_guid": "4JDT3MX9Q-008369eb-00000364-00000000-1d6f5ba1b173ce9",
    "threat_cause_parent_guid": "None",
    "threat_cause_reputation": "ADAPTIVE_WHITE_LIST",
    "threat_cause_threat_category": "NEW_MALWARE",
    "threat_cause_vector": "UNKNOWN",
    "threat_cause_cause_event_id": "0980efd1b38111eba4bfa5e98aa30b19",
    "blocked_threat_category": "UNKNOWN",
    "not_blocked_threat_category": "NEW_MALWARE",
    "kill_chain_status": ["RECONNAISSANCE"],
    "sensor_action": "None",
    "run_state": "RAN",
    "policy_applied": "NOT_APPLIED"
}

GET_ALERT_RESP_INVALID_ALERT_ID = {
    "type": "CB_ANALYTICS",
    "id": "86123310980efd0b38111eba4bfa5e98aa30b19",
    "legacy_alert_id": None,
    "org_key": "4JDT3MX9Q",
    "create_time": "2021-05-13T00:20:46.474Z",
    "last_update_time": "2021-05-13T00:27:22.846Z",
    "first_event_time": "2021-05-13T00:20:13.043Z",
    "last_event_time": "2021-05-13T00:20:13.044Z",
    "threat_id": "a26842be6b54ea2f58848b23a3461a16",
    "severity": 1,
    "category": "MONITORED",
    "device_id": 8612331,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_name": "win-2016-devrel",
    "device_username": "Administrator",
    "policy_id": 7113786,
    "policy_name": "Standard",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "None",
        "last_update_time": "2021-05-13T00:20:46.474Z",
        "comment": "None",
        "changed_by": "Carbon Black"
    },
    "notes_present": False,
    "tags": "None",
    "reason": "A port scan was detected from 10.169.255.100 on an external network (off-prem).",
    "reason_code": "R_SCAN_OFF",
    "process_name": "svchost.exe",
    "device_location": "OFFSITE",
    "created_by_event_id": "0980efd0b38111eba4bfa5e98aa30b19",
    "threat_indicators": [
        {
            "process_name": "svchost.exe",
            "sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "ttps": [
                "ACTIVE_SERVER",
                "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                "NETWORK_ACCESS",
                "PORTSCAN"
            ]
        }
    ]
}
