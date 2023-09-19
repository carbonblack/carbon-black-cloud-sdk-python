"""Mock responses for alert queries."""

GET_ALERT_RESP = {"org_key": "ABCD1234",
                  "alert_url": "https://defense.conferdeploy.net/alerts?s[c][query_string]= \
    id:52fa009d-e2d1-4118-8a8d-04f521ae66aa&orgKey=ABCD1234",
                  "id": "12ab345cd6-e2d1-4118-8a8d-04f521ae66aa", "type": "WATCHLIST",
                  "backend_timestamp": "2023-04-14T21:30:40.570Z", "user_update_timestamp": None,
                  "backend_update_timestamp": "2023-04-14T21:30:40.570Z",
                  "detection_timestamp": "2023-04-14T21:27:14.719Z",
                  "first_event_timestamp": "2023-04-14T21:21:42.193Z",
                  "last_event_timestamp": "2023-04-14T21:21:42.193Z",
                  "severity": 8,
                  "reason": "Process infdefaultinstall.exe was detected by the report\
                   \"Defense Evasion - \" in 6 watchlists",
                  "reason_code": "05696200-88e6-3691-a1e3-8d9a64dbc24e:7828aec8-8502-3a43-ae68-41b5050dab5b",
                  "threat_id": "0569620088E6669121E38D9A64DBC24E", "primary_event_id": "-7RlZFHcSGWKSrF55B_4Ig-0",
                  "policy_applied": "NOT_APPLIED", "run_state": "RAN", "sensor_action": "ALLOW",
                  "workflow": {"change_timestamp": "2023-04-14T21:30:40.570Z", "changed_by_type": "SYSTEM",
                               "changed_by": "ALERT_CREATION", "closure_reason": "NO_REASON", "status": "OPEN"},
                  "determination": None,
                  "tags": ["tag1", "tag2"], "alert_notes_present": False, "threat_notes_present": False,
                  "is_updated": False,
                  "device_id": 18118174, "device_name": "demo-machine", "device_uem_id": "",
                  "device_target_value": "LOW",
                  "device_policy": "123abcde-c21b-4d64-9e3e-53595ef9c7af", "device_policy_id": 1234567,
                  "device_os": "WINDOWS",
                  "device_os_version": "Windows 10 x64 SP: 1", "device_username": "demouser@demoorg.com",
                  "device_location": "UNKNOWN", "device_external_ip": "1.2.3.4", "mdr_alert": False,
                  "report_id": "oJFtoawGS92fVMXlELC1Ow-b4ee93fc-ec58-436a-a940-b4d33a613513",
                  "report_name": "Defense Evasion - Signed Binary Proxy Execution - InfDefaultInstall",
                  "report_description": "\n\nThreat:\nThis behavior may be abused by adversaries to execute malicious\
                   files that could bypass application whitelisting and signature validation on systems.\n\nFalse \
                   Positives:\nSome environments may legitimate use this, but should be rare.\n\nScore:\n85",
                  "report_tags": ["attack", "attackframework", "threathunting"],
                  "report_link": "https://attack.mitre.org/wiki/Technique/T1218",
                  "ioc_id": "b4ee93fc-ec58-436a-a940-b4d33a613513-0",
                  "ioc_hit": "((process_name:InfDefaultInstall.exe)) -enriched:true",
                  "watchlists": [{"id": "9x0timurQkqP7FBKX4XrUw", "name": "Carbon Black Advanced Threats"}],
                  "process_guid": "ABC12345-000309c2-00000478-00000000-1d6a1c1f2b02805", "process_pid": 10980,
                  "process_name": "infdefaultinstall.exe",
                  "process_sha256": "1a2345cd88666a458f804e5d0fe925a9f55cf016733458c58c1980addc44cd774",
                  "process_md5": "12c34567894a49f13193513b0138f72a9", "process_effective_reputation": "LOCAL_WHITE",
                  "process_reputation": "NOT_LISTED",
                  "process_cmdline": "InfDefaultInstall.exe C:\\Users\\username\\userdir\\Infdefaultinstall.inf",
                  "process_username": "DEMO\\DEMOUSER", "process_issuer": "Demo Code Signing CA - G2",
                  "process_publisher": "Demo Test Authority", "childproc_guid": "", "childproc_username": "",
                  "childproc_cmdline": "",
                  "ml_classification_final_verdict": "NOT_ANOMALOUS", "ml_classification_global_prevalence": "LOW",
                  "ml_classification_org_prevalence": "LOW"}

GET_ALERT_RESP_INVALID_ALERT_ID = {"type": "CB_ANALYTICS", "id": "86123310980efd0b38111eba4bfa5e98aa30b19",
                                   "legacy_alert_id": None, "org_key": "ABCD1234",
                                   "create_time": "2021-05-13T00:20:46.474Z",
                                   "last_update_time": "2021-05-13T00:27:22.846Z",
                                   "first_event_time": "2021-05-13T00:20:13.043Z",
                                   "last_event_time": "2021-05-13T00:20:13.044Z",
                                   "threat_id": "a26842be6b54ea2f58848b23a3461a16", "severity": 1,
                                   "category": "MONITORED", "device_id": 8612331, "device_os": "WINDOWS",
                                   "device_os_version": "Windows Server 2019 x64", "device_name": "demo-machine",
                                   "device_username": "Administrator",
                                   "policy_id": 7113786, "policy_name": "Standard", "target_value": "MEDIUM",
                                   "workflow": {"state": "OPEN", "remediation": "None",
                                                "last_update_time": "2021-05-13T00:20:46.474Z",
                                                "comment": "None", "changed_by": "Carbon Black", },
                                   "notes_present": False, "tags": "None",
                                   "reason": "A port scan was detected from 10.169.255.100 on an external network \
                                   (off-prem).",
                                   "reason_code": "R_SCAN_OFF", "process_name": "svchost.exe",
                                   "device_location": "OFFSITE",
                                   "created_by_event_id": "0980efd0b38111eba4bfa5e98aa30b19",
                                   "threat_indicators": [{"process_name": "svchost.exe",
                                                          "sha256": "7fd065bac18c5278777ae4490810\
                                                          1cdfed72d26fa741367f0ad4d02020787ab6",
                                                          "ttps": ["ACTIVE_SERVER",
                                                                   "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                                                                   "NETWORK_ACCESS", "PORTSCAN"], }],
                                   }

GET_ALERT_TYPE_WATCHLIST = {"org_key": "ABC12345",
                            "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]= \
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                            "id": "887e6bbc-6224-4f36-ad37-084038b7fcab", "type": "WATCHLIST",
                            "backend_timestamp": "2023-07-17T17:42:29.822Z",
                            "user_update_timestamp": "null", "backend_update_timestamp": "2023-07-17T17:42:29.822Z",
                            "detection_timestamp": "2023-07-17T17:41:57.829Z",
                            "first_event_timestamp": "2023-07-17T17:40:24.688Z",
                            "last_event_timestamp": "2023-07-17T17:40:24.688Z", "severity": 10,
                            "reason": "Process powershell.exe was detected by the report \
     \"Credential Access - Suspect Volume Shadow Copy  Behavior Detected\" in  \
     watchlist \"Carbon Black Advanced Threats\"",
                            "reason_code": "d05c5be2-02f0-3161-bbe2-ee4b26c72712:b598b578-314c-39e2-b4ac-4a1b04b44708",
                            "threat_id": "D05C5BE202F0F1617BE2EE4B26C72712",
                            "primary_event_id": "Gy8SwrTARRWq6lp_PpxMKg-0",
                            "policy_applied": "NOT_APPLIED", "run_state": "RAN", "sensor_action": "ALLOW",
                            "workflow": {"change_timestamp": "2023-07-17T17:42:29.822Z", "changed_by_type": "SYSTEM",
                                         "changed_by": "ALERT_CREATION", "closure_reason": "NO_REASON",
                                         "status": "OPEN"},
                            "determination": {"change_timestamp": "2023-07-17T17:42:29.822Z", "value": "NONE",
                                              "changed_by_type": "null",
                                              "changed_by": "null"}, "tags": "null", "alert_notes_present": "false",
                            "threat_notes_present": "false",
                            "is_updated": "false", "device_id": 6948863, "device_name": "Kognos-W19-CB-3",
                            "device_uem_id": "",
                            "device_target_value": "MISSION_CRITICAL", "device_policy": "SSQ_Policy",
                            "device_policy_id": 112221,
                            "device_os": "WINDOWS", "device_os_version": "Windows Server 2019 x64",
                            "device_username": "rahul.gopi@devo.com",
                            "device_location": "UNKNOWN", "device_external_ip": "34.234.170.45",
                            "device_internal_ip": "10.0.14.120",
                            "mdr_alert": "false", "mdr_alert_notes_present": "false",
                            "mdr_threat_notes_present": "false",
                            "report_id": "MLRtPcpQGKFh5OE4BT3tQ-49760e2e-c1e4-42e9-8157-4084ff002bcc",
                            "report_name": "Credential Access - Suspect Volume Shadow Copy Behavior Detected",
                            "report_description": "\n\nThreat:\nAdversaries may attempt to access or create a copy of \
                            the Active Directory domain database in order to steal credential information, as well as \
                            obtain other information about domain members such as devices, users, and access rights. \
                            If you are responding to this alert you should take immediate action.\n\nFalse Positives:\n\
                            Some IT backup software may trigger this detection.\n\nScore:\n100",
                            "report_tags": ["credentialaccess", "activedirectory", "volumeshadowcopy", "ntds", "t1003",
                                            "attackframework",
                                            "windows"], "report_link": "https://attack.mitre.org/techniques/T1003/003/",
                            "ioc_id": "49760e2e-c1e4-42e9-8157-4084ff002bcc-0",
                            "ioc_hit": "((process_cmdline:HarddiskVolumeShadowCopy* AND (process_cmdline:\
                            ntds\\\\ntds.dit OR process_cmdline:system32\\\\config\\\\sam OR process_cmdline:system32\
                            \\\\config\\\\system)) - (process_name:windows\\\\system32\\\\esentutl.exe OR \
                            process_publisher:\"Veritas\\ Technologies\\ LLC\" OR process_publisher:\"Symantec\\ \
                            Corporation\")) -enriched:true",
                            "watchlists": [{"id": "Z7L0yVdGQ62w2VmqcBUnA", "name": "Carbon Black Advanced Threats"}],
                            "process_guid": "ABC12345-000309c2-00000478-00000000-1d6a1c1f2b02805", "process_pid": 1632,
                            "process_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
                            "process_sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                            "process_md5": "7353f60b1739074eb17c5f4dddefe239",
                            "process_effective_reputation": "TRUSTED_WHITE_LIST",
                            "process_reputation": "TRUSTED_WHITE_LIST",
                            "process_cmdline": "\"powershell.exe\" & {1..10 | % { \n try { [System.IO.File]:: \
    Copy(\\\"\"\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy$_\\Windows\\System32\\config\\SAM\\\"\" , \
     \\\"\"$env:TEMP\\SAMvss$_\\\"\", \\\"\"true\\\"\") } catch {}\n ls \\\"\"$env:TEMP\\SAMvss$_\\\"\" -ErrorAction  \
     Ignore\n}}",
                            "process_username": "KOGNOS-W19-CB-3\\Administrator",
                            "process_issuer": ["Microsoft Windows Production PCA 2011"],
                            "process_publisher": ["Microsoft Windows"],
                            "parent_guid": "ABC12345-006a07ff-000009a0-00000000-1d9b8d5c2fcbfb7",
                            "parent_pid": 2464,
                            "parent_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
                            "parent_sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                            "parent_md5": "7353f60b1739074eb17c5f4dddefe239",
                            "parent_effective_reputation": "TRUSTED_WHITE_LIST",
                            "parent_reputation": "TRUSTED_WHITE_LIST",
                            "parent_cmdline": "\"c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe\" -c \"\
                            cd c:\\ ; echo MYPID=$PID; Get-Date ; Invoke-AtomicTest T1003.002-6 \"",
                            "parent_username": "KOGNOS-W19-CB-3\\Administrator", "childproc_guid": "",
                            "childproc_username": "",
                            "childproc_cmdline": "", "ml_classification_final_verdict": "NOT_ANOMALOUS",
                            "ml_classification_global_prevalence": "MEDIUM", "ml_classification_org_prevalence": "LOW"}

GET_ALERT_TYPE_WATCHLIST_INVALID = {"org_key": "ABC12345",
                                    "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                                    "id": "887e6bbc-6224-4f36-ad37-084038b7fcab", "type": "WATCHLIST",
                                    "backend_timestamp": "2023-07-17T17:42:29.822Z",
                                    "user_update_timestamp": "null",
                                    "backend_update_timestamp": "2023-07-17T17:42:29.822Z",
                                    "detection_timestamp": "2023-07-17T17:41:57.829Z",
                                    "first_event_timestamp": "2023-07-17T17:40:24.688Z",
                                    "last_event_timestamp": "2023-07-17T17:40:24.688Z", "severity": 10,
                                    "reason": "Process powershell.exe was detected by the report \"Credential Access \
                                    - Suspect Volume Shadow Copy Behavior Detected\" in watchlist \"Carbon Black \
                                    Advanced Threats\"",
                                    "reason_code": "d05c5be2-02f0-3161-bbe2-ee4b26c72712\
                                    :b598b578-314c-39e2-b4ac-4a1b04b44708",
                                    "threat_id": "D05C5BE202F0F1617BE2EE4B26C72712",
                                    "primary_event_id": "Gy8SwrTARRWq6lp_PpxMKg-0",
                                    "policy_applied": "NOT_APPLIED", "run_state": "RAN", "sensor_action": "ALLOW",
                                    "workflow": {"change_timestamp": "2023-07-17T17:42:29.822Z",
                                                 "changed_by_type": "SYSTEM",
                                                 "changed_by": "ALERT_CREATION", "closure_reason": "NO_REASON",
                                                 "status": "OPEN"},
                                    "determination": {"change_timestamp": "2023-07-17T17:42:29.822Z", "value": "NONE",
                                                      "changed_by_type": "null",
                                                      "changed_by": "null"}, "tags": "null",
                                    "alert_notes_present": "false", "threat_notes_present": "false",
                                    "is_updated": "false", "device_id": 6948863, "device_name": "Kognos-W19-CB-3",
                                    "device_uem_id": "",
                                    "device_target_value": "MISSION_CRITICAL", "device_policy": "SSQ_Policy",
                                    "device_policy_id": 112221,
                                    "device_os": "WINDOWS", "device_os_version": "Windows Server 2019 x64",
                                    "device_username": "rahul.gopi@devo.com",
                                    "device_location": "UNKNOWN", "device_external_ip": "34.234.170.45",
                                    "device_internal_ip": "10.0.14.120",
                                    "mdr_alert": "false", "mdr_alert_notes_present": "false",
                                    "mdr_threat_notes_present": "false",
                                    "report_id": "MLRtPcpQGKFh5OE4BT3tQ-49760e2e-c1e4-42e9-8157-4084ff002bcc",
                                    "report_name": "Credential Access - Suspect Volume Shadow Copy Behavior Detected",
                                    "report_description": "\n\nThreat:\nAdversaries may attempt to access or create a \
                                    copy of the Active Directory domain database in order to steal credential \
                                    information, as well as obtain other information about domain members such as \
                                    devices, users, and access rights. If you are responding to this alert you should \
                                    take immediate action. \n\nFalse Positives:\nSome IT backup software may trigger \
                                    this detection.\n\nScore:\n100",
                                    "report_tags": ["credentialaccess", "activedirectory", "volumeshadowcopy", "ntds",
                                                    "t1003", "attackframework",
                                                    "windows"],
                                    "report_link": "https://attack.mitre.org/techniques/T1003/003/",
                                    "ioc_id": "49760e2e-c1e4-42e9-8157-4084ff002bcc-0",
                                    "ioc_hit": "((process_cmdline:HarddiskVolumeShadowCopy* AND (process_cmdline:\
                                    ntds\\\\ntds.dit OR process_cmdline:system32\\\\config\\\\sam OR \
                                    process_cmdline:system32\\\\config\\\\system)) -(process_name:windows\
                                    \\\\system32\\\\esentutl.exe OR process_publisher:\"Veritas\\ Technologies\\ LLC\" \
                                    OR process_publisher:\"Symantec\\ Corporation\")) -enriched:true",
                                    "watchlists": [
                                        {"id": "Z7L0yVdGQ62w2VmqcBUnA", "name": "Carbon Black Advanced Threats"}],
                                    "process_guid": "",
                                    "process_pid": 1632,
                                    "process_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
                                    "process_sha256": "de96a6e69944335375dc1ac238336066\
                                    889d9ffc7d73628ef4fe1b1b160ab32c",
                                    "process_md5": "7353f60b1739074eb17c5f4dddefe239",
                                    "process_effective_reputation": "TRUSTED_WHITE_LIST",
                                    "process_reputation": "TRUSTED_WHITE_LIST",
                                    "process_cmdline": "\"powershell.exe\" & {1..10 | % { \n try { [System.IO.File]::\
                                    Copy(\\\"\"\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy$_\\Windows\\System32\
                                    \\config\\SAM\\\"\" , \\\"\"$env:TEMP\\SAMvss$_\\\"\", \\\"\"true\\\"\") } catch {}\
                                    \n ls \\\"\"$env:TEMP\\SAMvss$_\\\"\" -ErrorAction Ignore\n}}",
                                    "process_username": "KOGNOS-W19-CB-3\\Administrator",
                                    "process_issuer": ["Microsoft Windows Production PCA 2011"],
                                    "process_publisher": ["Microsoft Windows"],
                                    "parent_guid": "ABC12345-006a07ff-000009a0-00000000-1d9b8d5c2fcbfb7",
                                    "parent_pid": 2464,
                                    "parent_name": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
                                    "parent_sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                                    "parent_md5": "7353f60b1739074eb17c5f4dddefe239",
                                    "parent_effective_reputation": "TRUSTED_WHITE_LIST",
                                    "parent_reputation": "TRUSTED_WHITE_LIST",
                                    "parent_cmdline": "\"c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe\
                                    \" -c \"cd c:\\ ; echo MYPID=$PID; Get-Date ; Invoke-AtomicTest T1003.002-6 \"",
                                    "parent_username": "KOGNOS-W19-CB-3\\Administrator", "childproc_guid": "",
                                    "childproc_username": "",
                                    "childproc_cmdline": "", "ml_classification_final_verdict": "NOT_ANOMALOUS",
                                    "ml_classification_global_prevalence": "MEDIUM",
                                    "ml_classification_org_prevalence": "LOW"}

GET_ALERT_RESP_WITH_NOTES = {"org_key": "ABC12345",
                             "alert_url": "defense-test03.cbdtest.io/alerts?s[c][query_string]=\
    id:52dbd1b6-539b-a3f7-34bd-f6eb13a99b81&orgKey=ABC12345",
                             "id": "52dbd1b6-539b-a3f7-34bd-f6eb13a99b81", "type": "CONTAINER_RUNTIME",
                             "backend_timestamp": "2023-07-18T00:02:17.465Z", "user_update_timestamp": "null",
                             "backend_update_timestamp": "2023-07-18T00:02:17.465Z",
                             "detection_timestamp": "2023-07-18T00:00:38.456Z",
                             "first_event_timestamp": "2023-07-17T23:59:31.502Z",
                             "last_event_timestamp": "2023-07-17T23:59:31.502Z",
                             "severity": 5,
                             "reason": "Detected a connection to a public destination that isn't allowed for \
                             this scope",
                             "reason_code": "6e41702c-c64e-4950-9eec-1737228cf9f7:f8b1637a-dc0c-49bb-bc28-5b48f97e6d58",
                             "threat_id": "78de82d612a7d3d4a6caffa4ce7e7bb718e23d926dcd9a5047f6e9f129279d44",
                             "primary_event_id": "5XkI7XjGQ-6k20UtdzvDKQ-552", "policy_applied": "NOT_APPLIED",
                             "run_state": "RAN",
                             "sensor_action": "ALLOW",
                             "workflow": {"change_timestamp": "2023-07-18T00:02:17.465Z", "changed_by_type": "SYSTEM",
                                          "changed_by": "ALERT_CREATION", "closure_reason": "NO_REASON",
                                          "status": "OPEN"},
                             "determination": {"change_timestamp": "2023-07-18T00:02:17.465Z", "value": "NONE",
                                               "changed_by_type": "null",
                                               "changed_by": "null"}, "tags": "null", "alert_notes_present": "false",
                             "threat_notes_present": "false",
                             "is_updated": "false", "mdr_alert": "false", "mdr_alert_notes_present": "false",
                             "mdr_threat_notes_present": "false", "netconn_remote_port": 443,
                             "netconn_local_port": 56802,
                             "netconn_protocol": "TCP", "netconn_remote_domain": "westus3.monitoring.azure.com",
                             "netconn_remote_ip": "10.10.10.10", "netconn_local_ip": "10.224.0.74",
                             "netconn_remote_ipv4": "10.10.10.10",
                             "netconn_local_ipv4": "10.224.0.74", "k8s_cluster": "test:test-azure-cni",
                             "k8s_namespace": "kube-system",
                             "k8s_kind": "DaemonSet", "k8s_workload_name": "ama-logs", "k8s_pod_name": "ama-logs-svxpg",
                             "k8s_policy_id": "6e41702c-c64e-4950-9eec-1737228cf9f7",
                             "k8s_policy": "test-runtime-policy",
                             "k8s_rule_id": "f8b1637a-dc0c-49bb-bc28-5b48f97e6d58",
                             "k8s_rule": "Allowed public destinations",
                             "connection_type": "EGRESS", "egress_group_id": "", "egress_group_name": "",
                             "ip_reputation": 0,
                             "remote_is_private": "false"}

GET_ALERT_NOTES = {"num_found": 2, "num_available": 2, "results": [
    {"author": "Grogu", "id": "3gsgsfds", "note": "I am Grogu", "create_timestamp": "2023-04-18T03:25:44.397Z",
     "last_update_timestamp": "2023-04-18T03:25:44.397Z", "source": "CUSTOMER", "parent_id": None,
     "read_history": None, "thread": None},
    {"author": "demouser@demoorg.com", "create_timestamp": "2023-04-18T03:25:44.397Z",
     "last_update_timestamp": "2023-04-18T03:25:44.397Z", "id": "2", "source": "CUSTOMER", "note": "My first note",
     "parent_id": None, "read_history": None, "thread": None}]}

CREATE_ALERT_NOTE_RESP = {"author": "Grogu", "id": "3gsgsfds", "note": "I am Grogu",
                          "create_timestamp": "2023-04-18T03:25:44.397Z",
                          "last_update_timestamp": "2023-04-18T03:25:44.397Z",
                          "source": "CUSTOMER", "parent_id": None, "read_history": None, "thread": None}
