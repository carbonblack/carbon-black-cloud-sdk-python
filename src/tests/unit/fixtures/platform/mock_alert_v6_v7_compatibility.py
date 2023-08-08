"""Mocks for tests that verify Alert API v6 to v7 compatibility"""

"""V6 _info for CB_ANALYTIC alert generated by SDK 1.4.3 (before Alert API v7 was in use)"""
ALERT_V6_INFO_CB_ANALYTICS_SDK_1_4_3 = {
    "type": "CB_ANALYTICS",
    "id": "6f1173f5-f921-8e11-2160-edf42b799333",
    "legacy_alert_id": "6f1173f5-f921-8e11-2160-edf42b799333",
    "org_key": "ABCD1234",
    "create_time": "2023-08-03T00:23:09.659Z",
    "last_update_time": "2023-08-03T00:45:18.995Z",
    "first_event_time": "2023-08-03T00:22:29.972Z",
    "last_event_time": "2023-08-03T00:43:34.042Z",
    "threat_id": "9e0afc389c1acc43b382b1ba590498d2",
    "severity": 4,
    "category": "THREAT",
    "device_id": 12345678,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_name": "DEMO-Device-Name",
    "device_username": "demo@demo.org.com",
    "policy_name": "demo policy",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "v6_solved",
        "last_update_time": "2023-08-03T00:23:09.659Z",
        "comment": "Testing v6 with v7 live",
        "changed_by": "ABCD1234"
    },
    "notes_present": False,
    "tags": "",
    "policy_id": 876543,
    "reason": "A known virus (HackTool: Powerpuff) was detected running.",
    "reason_code": "T_REP_VIRUS",
    "process_name": "c:\\users\\administrator\\appdata\\local\\temp\\powerdump.ps1",
    "device_location": "OFFSITE",
    "created_by_event_id": "e9c71da7319611ee935f4d220f1572e7",
    "threat_indicators": [
        {
            "process_name": "powershell.exe",
            "sha256": "34d008ea32b73e016768545c6c601bc8a0dbca115fd7bc798d0cb435c3071555",
            "ttps": [
                "FILELESS",
                "RUN_CMD_SHELL",
                "MITRE_T1059_001_POWERSHELL",
                "MITRE_T1059_003_WIN_CMD_SHELL",
                "RUN_MALWARE_APP",
                "POLICY_DENY",
                "MITRE_T1059_CMD_LINE_OR_SCRIPT_INTER"
            ]
        },
        {
            "process_name": "powerdump.ps1",
            "sha256": "bea5ebaf8bbd6fb378b7f03fccb12ea4e0305c6a7be0e219e6b30e2b397f4508",
            "ttps": [
                "MALWARE_APP"
            ]
        }
    ],
    "threat_activity_dlp": "NOT_ATTEMPTED",
    "threat_activity_phish": "NOT_ATTEMPTED",
    "threat_activity_c2": "NOT_ATTEMPTED",
    "threat_cause_actor_sha256": "0640c9ee54aaca64ff238659b281ce28ae5c3729ff0b2700fdac916589aea848",
    "threat_cause_actor_name": "powerdump.ps1",
    "threat_cause_actor_process_pid": "2512-133354970126669173-0",
    "threat_cause_process_guid": "ABCD1234-006a07ff-000009d0-00000000-1d9c5a3876ed575",
    "threat_cause_parent_guid": "ABCD1234-006a07ff-00000638-00000000-1d9c5a385ff6892",
    "threat_cause_reputation": "KNOWN_MALWARE",
    "threat_cause_threat_category": "KNOWN_MALWARE",
    "threat_cause_vector": "WEB",
    "threat_cause_cause_event_id": "e9c71da7319611ee935f4d220f1572e7",
    "blocked_threat_category": "NON_MALWARE",
    "not_blocked_threat_category": "UNKNOWN",
    "kill_chain_status": [
        "INSTALL_RUN"
    ],
    "sensor_action": "TERMINATE",
    "run_state": "RAN",
    "policy_applied": "APPLIED",
    "alert_classification": ""
}

"""V6 _info for WATCHLIST alert generated by SDK 1.4.3 (before Alert API v7 was in use)"""
ALERT_V6_INFO_WATCHLIST_SDK_1_4_3 = {
    "type": "WATCHLIST",
    "id": "f6af290d-6a7f-461c-a8af-cf0d24311105",
    "legacy_alert_id": "f6af290d-6a7f-461c-a8af-cf0d24311105",
    "org_key": "ABCD1234",
    "create_time": "2023-08-03T15:46:03.764Z",
    "last_update_time": "2023-08-03T15:46:03.764Z",
    "first_event_time": "2023-08-03T15:40:38.378Z",
    "last_event_time": "2023-08-03T15:40:38.378Z",
    "threat_id": "C21CA826573A8D974C1E93C8471AAB7F",
    "severity": 5,
    "category": "THREAT",
    "device_id": 12345678,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_name": "DEMO-Device-Name",
    "device_username": "demo@demo.org.com",
    "policy_name": "demo policy",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "",
        "last_update_time": "2023-08-03T15:46:03.764Z",
        "comment": "",
        "changed_by": "ALERT_CREATION"
    },
    "notes_present": False,
    "tags": "",
    "policy_id": 9876,
    "reason": "Process powershell.exe was detected by the report \"Execution - AMSI - New Fileless Scheduled Task "
              "Behavior Detected\" in watchlist \"AMSI Threat Intelligence\"",
    "count": 0,
    "report_name": "Execution - AMSI - New Fileless Scheduled Task Behavior Detected",
    "ioc_id": "d1080521-e617-4e45-94e0-7a145c62c90a",
    "ioc_field": "",
    "ioc_hit": "(fileless_scriptload_cmdline:Register-ScheduledTask OR fileless_scriptload_cmdline:New-ScheduledTask "
               "OR scriptload_content:Register-ScheduledTask OR scriptload_content:New-ScheduledTask) AND NOT "
               "(process_cmdline:windows\\\\ccm\\\\systemtemp OR crossproc_name:windows\\\\ccm\\\\ccmexec.exe OR "
               "(process_publisher:\"VMware, Inc.\" AND process_publisher_state:FILE_SIGNATURE_STATE_TRUSTED))",
    "watchlists": [
        {
            "id": "mnbvc098766HN60hatQMQ",
            "name": "AMSI Threat Intelligence"
        }
    ],
    "process_guid": "ABCD1234-006a07ff-00000980-00000000-1d9c620d64ec999",
    "process_name": "powershell.exe",
    "run_state": "RAN",
    "threat_indicators": [
        {
            "process_name": "powershell.exe",
            "sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
            "ttps": [
                "d1080521-e617-4e45-94e0-7a145c62c90a"
            ]
        }
    ],
    "threat_cause_actor_sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
    "threat_cause_actor_md5": "123456789099074eb17c5f4dddefe239",
    "threat_cause_actor_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
    "threat_cause_reputation": "TRUSTED_WHITE_LIST",
    "threat_cause_threat_category": "UNKNOWN",
    "threat_cause_vector": "UNKNOWN",
    "document_guid": "Bo8uIQMuTnW87ndtKhE0EQ",
    "alert_classification": {
        "classification": "False_POSITIVE",
        "user_feedback": "NO_PREDICTION",
        "global_prevalence": "MEDIUM",
        "org_prevalence": "LOW",
        "asset_risk": "UNKNOWN"
    }
}

"""V6 _info for CONTAINER_RUNTIME alert generated by SDK 1.4.3 (before Alert API v7 was in use)"""
ALERT_V6_INFO_CONTAINER_RUNTIME_SDK_1_4_3 = {
    "type": "CONTAINER_RUNTIME",
    "id": "46b419c8-3d67-ead8-dbf1-9d8417610fac",
    "legacy_alert_id": "46b419c8-3d67-ead8-dbf1-9d8417610fac",
    "org_key": "ABCD1234",
    "create_time": "2023-08-03T10:48:54.536Z",
    "last_update_time": "2023-08-03T10:48:54.536Z",
    "first_event_time": "2023-08-03T10:45:28.860Z",
    "last_event_time": "2023-08-03T10:45:28.860Z",
    "threat_id": "a63ac7a14eadcb0577f48eae04c12955462727368be49b3d65dcaf0ddabf6246",
    "severity": 5,
    "category": "THREAT",
    "device_id": 0,
    "device_os": "",
    "device_os_version": "",
    "device_name": "",
    "device_username": "",
    "policy_name": "demo policy name",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "",
        "last_update_time": "2023-08-03T10:48:54.536Z",
        "comment": "",
        "changed_by": "ALERT_CREATION"
    },
    "notes_present": False,
    "tags": "",
    "policy_id": "453964c6-c730-4098-b634-c44a2734537a",
    "rule_id": "ec912f66-57c1-466b-b597-1d4a4ce1429c",
    "rule_name": "Allowed private destinations",
    "reason": "Detected a connection to a private network that isn't allowed for this scope",
    "run_state": "RAN",
    "cluster_name": "demo:cluster_name",
    "namespace": "demo_namespace",
    "workload_kind": "Deployment",
    "workload_id": "demo_workload_id",
    "workload_name": "demo_workload_name",
    "replica_id": "demo_workload_id-replica_54cd9c9477-gz6v8",
    "remote_namespace": "",
    "remote_workload_kind": "",
    "remote_workload_id": "",
    "remote_workload_name": "",
    "remote_replica_id": "",
    "connection_type": "EGRESS",
    "remote_is_private": True,
    "remote_ip": "1.2.3.4",
    "remote_domain": "",
    "protocol": "TCP",
    "port": 443,
    "egress_group_id": "",
    "egress_group_name": "",
    "ip_reputation": 0,
    "alert_classification": ""
}

"""V6 _info for HBFW alert generated by SDK 1.4.3 (before Alert API v7 was in use)"""
ALERT_V6_INFO_HBFW_SDK_1_4_3 = {
    "type": "HOST_BASED_FIREWALL",
    "id": "2be0652f-20bc-3311-9ded-8b873e28d830",
    "legacy_alert_id": "2be0652f-20bc-3311-9ded-8b873e28d830",
    "org_key": "ABCD1234",
    "create_time": "2023-03-10T11:30:53.388Z",
    "last_update_time": "2023-03-10T11:30:53.388Z",
    "first_event_time": "2023-03-10T11:28:36.200Z",
    "last_event_time": "2023-03-10T11:28:36.200Z",
    "threat_id": "86865bbbd875df0c949ce6f3c35bf39d90506577f74677e5dfd6506b135ad490",
    "severity": 4,
    "category": "THREAT",
    "device_id": 12345678,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 10 x64",
    "device_name": "hbfw-demo-device",
    "device_username": "deviceuser",
    "policy_name": "demo_policy",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "",
        "last_update_time": "2023-03-10T11:30:53.388Z",
        "comment": "",
        "changed_by": "ALERT_CREATION"
    },
    "notes_present": False,
    "tags": "",
    "policy_id": 19283746,
    "reason": "Outbound TCP connection blocked by firewall rule group 'Test Rule for Chrome access'.",
    "reason_code": "DD71F364-4A8C-4B14-89F6-7041CC6BEDEA:E0F3E7B8-BCB0-4231-8F0F-8DF0BCD54AA4",
    "rule_id": "E0F3E7B8-BCB0-4231-8F0F-8DF0BCD54AA4",
    "rule_category_id": "DD71F364-4A8C-4B14-89F6-7041CC6BEDEA",
    "threat_cause_actor_name": "c:\\program files\\google\\chrome\\application\\chrome.exe",
    "threat_cause_actor_process_pid": "ABCD1234-023411f8-0000241c-00000000-1d93aefb632cbb1",
    "threat_cause_actor_sha256": "2b42729ba9cd20511a28398279009e10533b0d911164a3f4af58a25ce2916530",
    "threat_cause_reputation": "NOT_LISTED",
    "threat_cause_threat_category": "NON_MALWARE",
    "threat_cause_cause_event_id": "ED57DA54-BF0F-11ED-BBE3-005056A5294B",
    "policy_applied": "APPLIED",
    "sensor_action": "DENY",
    "device_location": "UNKNOWN",
    "alert_classification": ""
}

"""V6 _info for DEVICE_CONTROL alert generated by SDK 1.4.3 (before Alert API v7 was in use)"""
ALERT_V6_INFO_DEVICE_CONTROL_SDK_1_4_3 = {
    "type": "DEVICE_CONTROL",
    "id": "b6a7e48b-1d14-11ee-a9e0-888888888788",
    "legacy_alert_id": "b6a7e48b-1d14-11ee-a9e0-888888888788",
    "org_key": "ABCD1234",
    "create_time": "2023-07-10T14:27:42.772Z",
    "last_update_time": "2023-07-10T14:27:42.772Z",
    "first_event_time": "2023-07-07T22:22:46.955Z",
    "last_event_time": "2023-07-07T22:22:46.955Z",
    "threat_id": "4a5611e67f619874c1722259d160d45a8d420b79705af02f0dbc3d084e8c85e9",
    "severity": 3,
    "category": "THREAT",
    "device_id": 12121212,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 11 x64",
    "device_name": "demo-deviceP",
    "device_username": "sample@demoorg.com",
    "policy_name": "demo policy",
    "target_value": "MEDIUM",
    "workflow": {
        "state": "OPEN",
        "remediation": "",
        "last_update_time": "2023-07-10T14:27:42.772Z",
        "comment": "",
        "changed_by": "ALERT_CREATION"
    },
    "notes_present": False,
    "tags": "",
    "policy_id": 6525,
    "reason": "Access attempted on unapproved USB device Generic Mass Storage (SN: 56787654). "
              "A Deny Policy Action was applied.",
    "device_location": "UNKNOWN",
    "threat_cause_threat_category": "NON_MALWARE",
    "threat_cause_vector": "REMOVABLE_MEDIA",
    "sensor_action": "DENY",
    "run_state": "DID_NOT_RUN",
    "policy_applied": "APPLIED",
    "vendor_name": "Generic",
    "vendor_id": "0x058F",
    "product_name": "Mass Storage",
    "product_id": "0x6387",
    "external_device_friendly_name": "Generic Flash Disk USB Device",
    "serial_number": "56787654",
    "alert_classification": ""
}

""" V7 API Responses"""

"""V7 API response for CB_ANALYTIC alert, generated with direct API call and modified to be valid json"""
GET_ALERT_v7_CB_ANALYTICS_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url":
        "defense.conferdeploy.net/alerts?s[c][query_string]=id:6f1173f5-f921-8e11-2160-edf42b799333&orgKey=ABCD1234",
    "id": "6f1173f5-f921-8e11-2160-edf42b799333",
    "type": "CB_ANALYTICS",
    "backend_timestamp": "2023-08-03T00:23:09.659Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-08-03T00:45:18.995Z",
    "detection_timestamp": "2023-08-03T00:22:30.526Z",
    "first_event_timestamp": "2023-08-03T00:22:29.972Z",
    "last_event_timestamp": "2023-08-03T00:43:34.042Z",
    "severity": 4,
    "reason": "A known virus (HackTool: Powerpuff) was detected running.",
    "reason_code": "T_REP_VIRUS",
    "threat_id": "9e0afc389c1acc43b382b1ba590498d2",
    "primary_event_id": "e9c71da7319611ee935f4d220f1572e7",
    "policy_applied": "APPLIED",
    "run_state": "RAN",
    "sensor_action": "TERMINATE",
    "workflow": {
        "state": "OPEN",
        "change_timestamp": "2023-08-03T00:23:09.659Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ABCD1234",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-08-03T00:23:09.659Z",
        "value": "NONE",
        "changed_by_type": "",
        "changed_by": ""
    },
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": True,
    "device_id": 12345678,
    "device_name": "DEMO-Device-Name",
    "device_uem_id": "",
    "device_target_value": "MEDIUM",
    "device_policy": "demo policy",
    "device_policy_id": 876543,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_username": "demo@demo.org.com",
    "device_location": "OFFSITE",
    "device_external_ip": "1.2.3.4",
    "device_internal_ip": "4.3.2.1",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "ttps": [
        "MITRE_T1059_003_WIN_CMD_SHELL",
        "RUN_MALWARE_APP",
        "MALWARE_APP",
        "RUN_CMD_SHELL",
        "MITRE_T1059_CMD_LINE_OR_SCRIPT_INTER",
        "FILELESS",
        "MITRE_T1059_001_POWERSHELL",
        "POLICY_DENY"
    ],
    "attack_tactic": "TA0002",
    "process_guid": "ABCD1234-006a07ff-000009d0-00000000-1d9c5a3876ed575",
    "process_pid": 2512,
    "process_name": "c:\\users\\administrator\\appdata\\local\\temp\\powerdump.ps1",
    "process_sha256": "0640c9ee54aaca64ff238659b281ce28ae5c3729ff0b2700fdac916589aea848",
    "process_md5": "ec7d95dff90d2dcc91bb27f365c2c844",
    "process_effective_reputation": "KNOWN_MALWARE",
    "process_reputation": "KNOWN_MALWARE",
    "process_cmdline": "\"powershell.exe\" & {Write-Host \\\"\"STARTING TO SET BYPASS and DISABLE DEFENDER REALTIME "
                       "MON\\\"\" -fore green\nImport-Module \\\"\"$Env:Temp\\PowerDump.ps1\\\"\"\nInvoke-PowerDump}",
    "process_username": "DEMO_USER\\Administrator",
    "process_issuer": [],
    "process_publisher": [],
    "parent_guid": "ABCD1234-006a07ff-00000638-00000000-1d9c5a385ff6892",
    "parent_pid": 1592,
    "parent_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
    "parent_sha256": "6eed1fe48bd0fe3b968af00302d8d9377c9f19e5900f1a0b565a0560f402c1a4",
    "parent_md5": "",
    "parent_effective_reputation": "TRUSTED_WHITE_LIST",
    "parent_reputation": "TRUSTED_WHITE_LIST",
    "parent_cmdline": None,
    "parent_username": "DEMO_USER\\Administrator",
    "childproc_guid": "ABCD1234-006a07ff-00000000-00000000-19db1ded53e8000",
    "childproc_name": "",
    "childproc_sha256": "",
    "childproc_md5": "",
    "childproc_effective_reputation": "RESOLVING",
    "childproc_username": "DEMO_USER\\Administrator",
    "childproc_cmdline": ""
}

"""V7 API response for WATCHLIST alert, generated with direct API call and modified to be valid json"""
GET_ALERT_v7_WATCHLIST_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=id:"
                 "f6af290d-6a7f-461c-a8af-cf0d24311105&orgKey=ABCD1234",
    "id": "f6af290d-6a7f-461c-a8af-cf0d24311105",
    "type": "WATCHLIST",
    "backend_timestamp": "2023-08-03T15:46:03.764Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-08-03T15:46:03.764Z",
    "detection_timestamp": "2023-08-03T15:45:34.295Z",
    "first_event_timestamp": "2023-08-03T15:40:38.378Z",
    "last_event_timestamp": "2023-08-03T15:40:38.378Z",
    "severity": 5,
    "reason": "Process powershell.exe was detected by the report \"Execution - AMSI - New Fileless Scheduled Task "
              "Behavior Detected\" in watchlist \"AMSI Threat Intelligence\"",
    "reason_code": "c21ca826-573a-3d97-8c1e-93c8471aab7f:8033b29d-81d2-3c47-82d2-f4a7f398b85d",
    "threat_id": "C21CA826573A8D974C1E93C8471AAB7F",
    "primary_event_id": "S3CpoLVQQGqdO2N1o0kXBw-0",
    "policy_applied": "NOT_APPLIED",
    "run_state": "RAN",
    "sensor_action": "ALLOW",
    "workflow": {
        "change_timestamp": "2023-08-03T15:46:03.764Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-08-03T15:46:03.764Z",
        "value": "NONE",
        "changed_by_type": "",
        "changed_by": ""
    },
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": False,
    "device_id": 12345678,
    "device_name": "DEMO-Device-Name",
    "device_uem_id": "",
    "device_target_value": "MEDIUM",
    "device_policy": "demo policy",
    "device_policy_id": 9876,
    "device_os": "WINDOWS",
    "device_os_version": "Windows Server 2019 x64",
    "device_username": "demo@demo.org.com",
    "device_location": "UNKNOWN",
    "device_external_ip": "34.234.170.45",
    "device_internal_ip": "10.0.14.120",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "report_id": "LrKOC7DtQbm4g8w0UFruQg-d1080521-e617-4e45-94e0-7a145c62c90a",
    "report_name": "Execution - AMSI - New Fileless Scheduled Task Behavior Detected",
    "report_description": "Newer Powershell versions introduced built-in cmdlets to manage scheduled tasks natively "
                          "without calling out to typical scheduled task processes like at.exe or schtasks.exe. "
                          "This detection looks for behaviors related to the fileless execution of scheduled tasks. "
                          "If you are responding to this alert, be sure to correlate the fileless scriptload events "
                          "with events typically found in your environment Generally, attackers will create scheduled "
                          "tasks with binaries that are located in user writable directories like AppData, Temp, or "
                          "public folders.",
    "report_tags": [
        "execution",
        "privesc",
        "persistence",
        "t1053",
        "windows",
        "amsi",
        "attack",
        "attackframework"
    ],
    "report_link": "https://attack.mitre.org/techniques/T1053/",
    "ioc_id": "d1080521-e617-4e45-94e0-7a145c62c90a",
    "ioc_hit": "(fileless_scriptload_cmdline:Register-ScheduledTask OR fileless_scriptload_cmdline:New-ScheduledTask "
               "OR scriptload_content:Register-ScheduledTask OR scriptload_content:New-ScheduledTask) "
               "AND NOT (process_cmdline:windows\\\\ccm\\\\systemtemp OR crossproc_name:windows\\\\ccm\\\\ccmexec.exe "
               "OR (process_publisher:\"VMware, Inc.\" AND process_publisher_state:FILE_SIGNATURE_STATE_TRUSTED))",
    "watchlists": [
        {
            "id": "mnbvc098766HN60hatQMQ",
            "name": "AMSI Threat Intelligence"
        }
    ],
    "process_guid": "ABCD1234-006a07ff-00000980-00000000-1d9c620d64ec999",
    "process_pid": 2432,
    "process_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
    "process_sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
    "process_md5": "123456789099074eb17c5f4dddefe239",
    "process_effective_reputation": "TRUSTED_WHITE_LIST",
    "process_reputation": "TRUSTED_WHITE_LIST",
    "process_cmdline": "\"c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe\" -c \"cd c:\\ ; "
                       "echo MYPID=$PID; Invoke-AtomicTest T1003.003-5 -GetPrereqs \"",
    "process_username": "DEMO_USER\\Administrator",
    "process_issuer": [
        "Microsoft Windows Production PCA 2011"
    ],
    "process_publisher": [
        "Microsoft Windows"
    ],
    "parent_guid": "ABCD1234-006a07ff-0000047c-00000000-1d9c620d62d5c1a",
    "parent_pid": 1148,
    "parent_name": "c:\\windows\\system32\\openssh\\sshd.exe",
    "parent_sha256": "731e8034cb953abcd0fc86400ad55113efa302f77d276213198a76065601576b",
    "parent_md5": "72789836eea643c23cd87732b8535e7e",
    "parent_effective_reputation": "TRUSTED_WHITE_LIST",
    "parent_reputation": "TRUSTED_WHITE_LIST",
    "parent_cmdline": "\"C:\\Windows\\System32\\OpenSSH\\sshd.exe\" \"-z\"",
    "parent_username": "DEMO_USER\\Administrator",
    "childproc_guid": "",
    "childproc_username": "",
    "childproc_cmdline": "",
    "ml_classification_final_verdict": "NOT_ANOMALOUS",
    "ml_classification_global_prevalence": "MEDIUM",
    "ml_classification_org_prevalence": "LOW"
}

"""V7 API response for CONTAINER_RUNTIME alert, generated with direct API call and modified to be valid json"""
GET_ALERT_v7_CONTAINER_RUNTIME_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url": "defense-test03.cbdtest.io/alerts?s[c][query_string]="
                 "id:46b419c8-3d67-ead8-dbf1-9d8417610fac&orgKey=ABCD1234",
    "id": "46b419c8-3d67-ead8-dbf1-9d8417610fac",
    "type": "CONTAINER_RUNTIME",
    "backend_timestamp": "2023-08-03T10:48:54.536Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-08-03T10:48:54.536Z",
    "detection_timestamp": "2023-08-03T10:46:01.641Z",
    "first_event_timestamp": "2023-08-03T10:45:28.860Z",
    "last_event_timestamp": "2023-08-03T10:45:28.860Z",
    "severity": 5,
    "reason": "Detected a connection to a private network that isn't allowed for this scope",
    "reason_code": "453964c6-c730-4098-b634-c44a2734537a:ec912f66-57c1-466b-b597-1d4a4ce1429c",
    "threat_id": "a63ac7a14eadcb0577f48eae04c12955462727368be49b3d65dcaf0ddabf6246",
    "primary_event_id": "X0eNZIe7StKs07MWe5oevw-1083",
    "policy_applied": "NOT_APPLIED",
    "run_state": "RAN",
    "sensor_action": "ALLOW",
    "workflow": {
        "change_timestamp": "2023-08-03T10:48:54.536Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-08-03T10:48:54.536Z",
        "value": "NONE",
        "changed_by_type": "",
        "changed_by": ""
    },
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": False,
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "netconn_remote_port": 56246,
    "netconn_local_port": 443,
    "netconn_protocol": "TCP",
    "netconn_remote_domain": "",
    "netconn_remote_ip": "1.2.3.4",
    "netconn_local_ip": "4.3.2.1",
    "netconn_remote_ipv4": "1.2.3.4",
    "netconn_local_ipv4": "4.3.2.1",
    "k8s_cluster": "demo:cluster_name",
    "k8s_namespace": "demo_namespace",
    "k8s_kind": "Deployment",
    "k8s_workload_name": "demo_workload_name",
    "k8s_pod_name": "demo_workload_id-replica_54cd9c9477-gz6v8",
    "k8s_policy_id": "453964c6-c730-4098-b634-c44a2734537a",
    "k8s_policy": "demo policy name",
    "k8s_rule_id": "ec912f66-57c1-466b-b597-1d4a4ce1429c",
    "k8s_rule": "Allowed private destinations",
    "connection_type": "EGRESS",
    "egress_group_id": "",
    "egress_group_name": "",
    "ip_reputation": 0,
    "remote_is_private": True
}

"""V7 API response for HBFW alert, generated with direct API call and modified to be valid json"""
GET_ALERT_v7_HBFW_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url": "defense-test03.cbdtest.io/alerts?s[c][query_string]="
                 "id:2be0652f-20bc-3311-9ded-8b873e28d830&orgKey=ABCD1234",
    "id": "2be0652f-20bc-3311-9ded-8b873e28d830",
    "type": "HOST_BASED_FIREWALL",
    "backend_timestamp": "2023-03-10T11:30:53.388Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-03-10T11:30:53.388Z",
    "detection_timestamp": "2023-03-10T11:28:36.200Z",
    "first_event_timestamp": "2023-03-10T11:28:36.200Z",
    "last_event_timestamp": "2023-03-10T11:28:36.200Z",
    "severity": 4,
    "reason": "Outbound TCP connection blocked by firewall rule group 'Test Rule for Chrome access'.",
    "reason_code": "DD71F364-4A8C-4B14-89F6-7041CC6BEDEA:E0F3E7B8-BCB0-4231-8F0F-8DF0BCD54AA4",
    "threat_id": "86865bbbd875df0c949ce6f3c35bf39d90506577f74677e5dfd6506b135ad490",
    "primary_event_id": "ED57DA54-BF0F-11ED-BBE3-005056A5294B",
    "policy_applied": "APPLIED",
    "run_state": "DID_NOT_RUN",
    "sensor_action": "DENY",
    "workflow": {
        "change_timestamp": "2023-03-10T11:30:53.388Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-03-10T11:30:53.388Z",
        "value": "NONE",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION"
    },
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": False,
    "rule_category_id": "DD71F364-4A8C-4B14-89F6-7041CC6BEDEA",
    "rule_id": "E0F3E7B8-BCB0-4231-8F0F-8DF0BCD54AA4",
    "device_id": 12345678,
    "device_name": "hbfw-demo-device",
    "device_uem_id": "",
    "device_target_value": "MEDIUM",
    "device_policy": "demo_policy",
    "device_policy_id": 19283746,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 10 x64",
    "device_username": "deviceuser",
    "device_location": "UNKNOWN",
    "device_external_ip": "1.2.3.4",
    "device_internal_ip": "5.6.7.8",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "process_guid": "ABCD1234-023411f8-0000241c-00000000-1d93aefb632cbb1",
    "process_pid": 9244,
    "process_name": "c:\\program files\\google\\chrome\\application\\chrome.exe",
    "process_sha256": "2b42729ba9cd20511a28398279009e10533b0d911164a3f4af58a25ce2916530",
    "process_md5": "ffa2b8e17f645bcc20f0e0201fef83ed",
    "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
    "process_reputation": "NOT_LISTED",
    "process_cmdline": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --type=utility "
                       "--utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=none "
                       "--mojo-platform-channel-handle=2236 --field-trial-handle=1836,i,"
                       "17669044556379481032,7348693199459682555,131072 /prefetch:8",
    "process_username": "hbfw-demo-device\\deviceuser",
    "process_issuer": [
        "DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1"
    ],
    "process_publisher": [
        "Google LLC"
    ],
    "parent_guid": "ABCD1234-023411f8-00001f94-00000000-1d93aefb47214d9",
    "parent_pid": 8084,
    "parent_name": "c:\\program files\\google\\chrome\\application\\chrome.exe",
    "parent_sha256": "2b42729ba9cd20511a28398279009e10533b0d911164a3f4af58a25ce2916530",
    "parent_md5": "ffa2b8e17f645bcc20f0e0201fef83ed",
    "parent_effective_reputation": "ADAPTIVE_WHITE_LIST",
    "parent_reputation": "NOT_LISTED",
    "parent_cmdline": "\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" ",
    "parent_username": "hbfw-demo-device\\deviceuser",
    "childproc_guid": "",
    "childproc_username": "",
    "childproc_cmdline": "",
    "netconn_remote_port": 443,
    "netconn_local_port": 54405,
    "netconn_protocol": "",
    "netconn_remote_domain": "demo.domain.com",
    "netconn_remote_ip": "2.3.4.5",
    "netconn_local_ip": "5.6.7.8",
    "netconn_remote_ipv4": "2.3.4.5",
    "netconn_local_ipv4": "5.6.7.8"
}

"""V7 API response for DEVICE_CONTROL alert, generated with direct API call and modified to be valid json"""
GET_ALERT_v7_DEVICE_CONTROL_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]="
                 "id:b6a7e48b-1d14-11ee-a9e0-888888888788&orgKey=ABCD1234",
    "id": "b6a7e48b-1d14-11ee-a9e0-888888888788",
    "type": "DEVICE_CONTROL",
    "backend_timestamp": "2023-07-10T14:27:42.772Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-07-10T14:27:42.772Z",
    "detection_timestamp": "2023-07-07T22:22:46.955Z",
    "first_event_timestamp": "2023-07-07T22:22:46.955Z",
    "last_event_timestamp": "2023-07-07T22:22:46.955Z",
    "severity": 3,
    "reason": "Access attempted on unapproved USB device Generic Mass Storage (SN: 56787654). "
              "A Deny Policy Action was applied.",
    "reason_code": "6D578342-9DE5-4353-9C25-1D3D857BFC5B:DCAEB1FA-513C-4026-9AB6-37A935873FBC",
    "threat_id": "4a5611e67f619874c1722259d160d45a8d420b79705af02f0dbc3d084e8c85e9",
    "primary_event_id": "B6A7E48D-1D14-11EE-A9E0-888888888788",
    "policy_applied": "APPLIED",
    "run_state": "DID_NOT_RUN",
    "sensor_action": "DENY",
    "workflow": {
        "change_timestamp": "2023-07-10T14:27:42.772Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-07-10T14:27:42.772Z",
        "value": "NONE",
        "changed_by_type": "",
        "changed_by": ""
    },
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": False,
    "device_id": 12121212,
    "device_name": "demo-deviceP",
    "device_uem_id": "",
    "device_target_value": "MEDIUM",
    "device_policy": "demo policy",
    "device_policy_id": 6525,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 11 x64",
    "device_username": "sample@demoorg.com",
    "device_location": "UNKNOWN",
    "device_external_ip": "9.8.7.6",
    "device_internal_ip": "6.5.4.3",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "vendor_name": "Generic",
    "vendor_id": "0x058F",
    "product_name": "Mass Storage",
    "product_id": "0x6387",
    "external_device_friendly_name": "Generic Flash Disk USB Device",
    "serial_number": "56787654"
}