GET_PROCESS_RESP = {}

GET_PROCESS_VALIDATION_RESP = {
    "valid": True,
    "value_search_query": False
}

GET_PROCESS_VALIDATION_RESP_INVALID = {
    "invalid_message": "Invalid Query Parameter",
    "valid": False,
    "value_search_query": False,
    "invalid_trigger_offset": 0
}

POST_PROCESS_SEARCH_JOB_RESP = {
    "job_id": "2c292717-80ed-4f0d-845f-779e09470920"
}

GET_PROCESS_SEARCH_JOB_RESULTS_RESP = {
    "results": [
        {
            "backend_timestamp": "2020-09-11T19:35:02.972Z",
            "childproc_count": 0,
            "crossproc_count": 787,
            "device_external_ip": "192.168.0.1",
            "device_group_id": 0,
            "device_id": 1234567,
            "device_internal_ip": "192.168.0.2",
            "device_name": "Windows10Device",
            "device_os": "WINDOWS",
            "device_policy_id": 12345,
            "device_timestamp": "2020-09-11T19:32:12.821Z",
            "enriched": True,
            "enriched_event_type": [
                "INJECT_CODE",
                "SYSTEM_API_CALL"
            ],
            "event_type": [
                "crossproc"
            ],
            "filemod_count": 0,
            "ingress_time": 1599852859660,
            "legacy": True,
            "modload_count": 1,
            "netconn_count": 0,
            "org_id": "test",
            "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00procsearchparent",
            "parent_hash": [
                "9090e0e44e14709fb09b23b98572e0e61c810189e2de8f7156021bc81c3b1bb6",
                "bccc12eb2ef644e662a63a023fb83f9b"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 644,
            "process_cmdline": [
                "\"C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe\""
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "test-0034d5f2-00000ba0-00000000-1d68709850fe522getprocjobres",
            "process_hash": [
                "63d423ea882264dbb157a965c200306212fc5e1c6ddb8cbbb0f1d3b51ecd82e6",
                "c7084336325dc8eadfb1e8ff876921c4"
            ],
            "process_name": "c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe",
            "process_pid": [
                2976
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_username": [
                "Username"
            ],
            "regmod_count": 1,
            "scriptload_count": 0,
            "ttp": [
                "ENUMERATE_PROCESSES",
                "INJECT_CODE",
                "MITRE_T1003_CREDENTIAL_DUMP",
                "MITRE_T1005_DATA_FROM_LOCAL_SYS",
                "MITRE_T1055_PROCESS_INJECT",
                "MITRE_T1057_PROCESS_DISCOVERY",
                "RAM_SCRAPING",
                "READ_SECURITY_DATA"
            ]
        }
    ],
    "num_found": 616,
    "num_available": 1,
    "contacted": 45,
    "completed": 45
}

GET_PROCESS_SEARCH_PARENT_JOB_RESULTS_RESP = {
    "results": [
        {
            "backend_timestamp": "2020-09-11T19:35:02.972Z",
            "childproc_count": 0,
            "crossproc_count": 787,
            "device_external_ip": "192.168.0.1",
            "device_group_id": 0,
            "device_id": 1234567,
            "device_internal_ip": "192.168.0.2",
            "device_name": "Windows10Device",
            "device_os": "WINDOWS",
            "device_policy_id": 12345,
            "device_timestamp": "2020-09-11T19:32:12.821Z",
            "enriched": True,
            "enriched_event_type": [
                "INJECT_CODE",
                "SYSTEM_API_CALL"
            ],
            "event_type": [
                "crossproc"
            ],
            "filemod_count": 0,
            "ingress_time": 1599852859660,
            "legacy": True,
            "modload_count": 1,
            "netconn_count": 0,
            "org_id": "test",
            "parent_guid": "parentofparent",
            "parent_hash": [
                "9090e0e44e14709fb09b23b98572e0e61c810189e2de8f7156021bc81c3b1bb6",
                "bccc12eb2ef644e662a63a023fb83f9b"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 644,
            "process_cmdline": [
                "\"C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe\""
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "test-0002b226-00000001-00000000-1d6225bbba74c01",
            "process_hash": [
                "63d423ea882264dbb157a965c200306212fc5e1c6ddb8cbbb0f1d3b51ecd82e6",
                "c7084336325dc8eadfb1e8ff876921c4"
            ],
            "process_name": "c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe",
            "process_pid": [
                2976
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_username": [
                "Username"
            ],
            "regmod_count": 1,
            "scriptload_count": 0,
            "ttp": [
                "ENUMERATE_PROCESSES",
                "INJECT_CODE",
                "MITRE_T1003_CREDENTIAL_DUMP",
                "MITRE_T1005_DATA_FROM_LOCAL_SYS",
                "MITRE_T1055_PROCESS_INJECT",
                "MITRE_T1057_PROCESS_DISCOVERY",
                "RAM_SCRAPING",
                "READ_SECURITY_DATA"
            ]
        }
    ],
    "num_found": 6168,
    "num_available": 1,
    "contacted": 45,
    "completed": 45
}

GET_PROCESS_SEARCH_JOB_RESULTS_RESP_1 = {
    "results": [
        {
            "backend_timestamp": "2020-09-11T19:35:02.972Z",
            "childproc_count": 0,
            "crossproc_count": 787,
            "device_external_ip": "192.168.0.1",
            "device_group_id": 0,
            "device_id": 1234567,
            "device_internal_ip": "192.168.0.2",
            "device_name": "Windows10Device",
            "device_os": "WINDOWS",
            "device_policy_id": 12345,
            "device_timestamp": "2020-09-11T19:32:12.821Z",
            "enriched": True,
            "enriched_event_type": [
                "INJECT_CODE",
                "SYSTEM_API_CALL"
            ],
            "event_type": [
                "crossproc"
            ],
            "filemod_count": 0,
            "ingress_time": 1599852859660,
            "legacy": True,
            "modload_count": 1,
            "netconn_count": 0,
            "org_id": "test",
            "parent_guid": "test-0034d5f2-00000284-00000000-1d687097e9cf7b5",
            "parent_hash": [
                "9090e0e44e14709fb09b23b98572e0e61c810189e2de8f7156021bc81c3b1bb6",
                "bccc12eb2ef644e662a63a023fb83f9b"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 644,
            "process_cmdline": [
                "\"C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe\""
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "process_hash": [
                "63d423ea882264dbb157a965c200306212fc5e1c6ddb8cbbb0f1d3b51ecd82e6",
                "c7084336325dc8eadfb1e8ff876921c4"
            ],
            "process_name": "c:\\program files\\vmware\\vmware tools\\vmtoolsd.exe",
            "process_pid": [
                3909
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_username": [
                "Username"
            ],
            "regmod_count": 1,
            "scriptload_count": 0,
            "ttp": [
                "ENUMERATE_PROCESSES",
                "INJECT_CODE",
                "MITRE_T1003_CREDENTIAL_DUMP",
                "MITRE_T1005_DATA_FROM_LOCAL_SYS",
                "MITRE_T1055_PROCESS_INJECT",
                "MITRE_T1057_PROCESS_DISCOVERY",
                "RAM_SCRAPING",
                "READ_SECURITY_DATA"
            ]
        }
    ],
    "num_found": 6168,
    "num_available": 1,
    "contacted": 45,
    "completed": 45
}

GET_PROCESS_SEARCH_JOB_RESP = {
    "contacted": 45,
    "completed": 45,
    "query": {
        "cb.max_backend_timestamp": 1599853172000,
        "cb.min_backend_timestamp": 0,
        "cb.min_device_timestamp": 0,
        "cb.preview_results": 500,
        "cb.use_agg": True,
        "facet": False,
        "fl": "*,parent_hash,parent_name,process_cmdline,backend_timestamp,device_external_ip,device_group,device_internal_ip,device_os,process_effective_reputation,process_reputation,ttp",
        "fq": "{!collapse field=process_collapse_id sort='max(0,legacy) asc,device_timestamp desc'}",
        "q": "(process_guid:test-0034d5f2-00000ba0-00000000-1d68709850fe521)",
        "rows": 500,
        "start": 0
    },
    "search_initiated_time": 1599853172533,
    "connector_id": "ABCDEFGH"
}

GET_PROCESS_SUMMARY_RESP = {
    "incomplete_results": False,
    "process": {
        "_s3_location": "A7Y2cg0hRsKblxNp_sqYRg:1742cae0777:f9d74:95f:default:3",
        "backend_timestamp": "2020-08-26T21:30:06.937Z",
        "device_external_ip": "192.168.0.1",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "192.168.0.1",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "policy-restrictive",
        "device_policy_id": 11200,
        "device_timestamp": "2020-08-26T20:29:20.731Z",
        "enriched": True,
        "enriched_event_type": "CREATE_PROCESS",
        "event_description": "The application \"<share><link hash=\"5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d\">/usr/lib/polkit-1/polkitd</link></share>\" invoked the application \"<share><link hash=\"949317971158c3ba88e19147d2e5c54466c9f665ce3809e38702de6f896cd0fa\">/usr/bin/pkla-check-authorization</link></share>\". ",
        "event_id": "f1d97afee7da11ea9affe54c85cd133a",
        "event_type": "childproc",
        "has_children": False,
        "index_class": "default",
        "ingress_time": 1598477387331,
        "legacy": True,
        "org_id": "test",
        "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c0parent",
        "parent_hash": [
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "parent_name": "/usr/lib/systemd/systemd",
        "parent_pid": 1,
        "partition_id": 0,
        "process_cmdline": [
            "/usr/lib/polkit-1/polkitd --no-debug"
        ],
        "process_guid": "test-0002b226-000015bd-00000000-1d6225bbba74c09",
        "process_hash": [
            "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d"
        ],
        "process_name": "/usr/lib/polkit-1/polkitd",
        "process_pid": [
            5565
        ],
        "process_reputation": "NOT_LISTED",
        "process_start_time": "2020-05-04T21:34:03.968Z",
        "process_username": [
            "polkitd"
        ],
        "ttp": [
            "RUN_SYSTEM_APP",
            "UNKNOWN_APP"
        ]
    },
    "siblings": [
        {
            "_s3_location": "nNWpDm_5QXG5vVI5c9YG-Q:1720df24ea4:0:69a:longTerm:3",
            "backend_timestamp": "2020-05-13T12:11:23.172Z",
            "device_external_ip": "",
            "device_id": 176678,
            "device_internal_ip": "192.168.0.1",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "policy-restrictive",
            "device_policy_id": 11200,
            "device_timestamp": "2020-05-13T12:10:02.073Z",
            "enriched": True,
            "enriched_event_type": "CREATE_PROCESS",
            "event_description": "The application \"<share><link hash=\"b9e3723553385b6e3d487bfae3878f9f8e57593ae4ec0a1ff4087f94b8e8368a\">/usr/sbin/crond</link></share>\" invoked the application \"<share><link hash=\"5975d972eea6b1c53ef9a69452797439ed5bf63fae72e1780761ea1c2cb6976a\">/usr/bin/bash</link></share>\". ",
            "event_id": "addca5e2951211eab71c3d5168eb0eaf",
            "event_type": "childproc",
            "has_children": False,
            "index_class": "longTerm",
            "ingress_time": 1589371825851,
            "legacy": True,
            "org_id": "test",
            "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00siblingparent",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_guid": "test-0002b226-0000192c-00000000-1d6225bbba74c00siblingproc",
            "process_hash": [
                "b9e3723553385b6e3d487bfae3878f9f8e57593ae4ec0a1ff4087f94b8e8368a"
            ],
            "process_name": "/usr/sbin/crond",
            "process_pid": [
                6444
            ],
            "process_reputation": "NOT_LISTED",
            "process_start_time": "2020-05-04T21:34:03.968Z",
            "ttp": [
                "MITRE_T1059_CMD_LINE_INTER",
                "RUN_CMD_SHELL",
                "RUN_UNKNOWN_APP",
                "UNKNOWN_APP"
            ]
        },
        {
            "_s3_location": "TlzX4o6VS1-Qalf_49Agrg:173ddf352b6:c691d:702:default:3",
            "backend_timestamp": "2020-08-11T14:36:17.809Z",
            "device_external_ip": "192.168.0.1",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 176678,
            "device_internal_ip": "",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "policy-restrictive",
            "device_policy_id": 11200,
            "device_timestamp": "2020-08-11T14:35:30.497Z",
            "enriched": True,
            "enriched_event_type": "CREATE_PROCESS",
            "event_description": "The application \"<share><link hash=\"2206d95e0a435aadad6c84b5bce370d076137efecf6adbbf6feddbe0515fb17e\">/usr/libexec/nm-dispatcher</link></share>\" invoked the application \"<share><link hash=\"9edd4a6490d43440da046535e8378894490fa0827a2b7101004fb776a0bd7092\">/etc/NetworkManager/dispatcher.d/20-chrony</link></share>\". ",
            "event_id": "ec9be172dbdf11eab3c8c1649f240e08",
            "event_type": "childproc",
            "has_children": True,
            "index_class": "default",
            "ingress_time": 1597156546529,
            "legacy": True,
            "org_id": "test",
            "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00sibling2parent",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/libexec/nm-dispatcher"
            ],
            "process_guid": "test-0002b226-00005e88-00000000-1d66feca9b7d350",
            "process_hash": [
                "2206d95e0a435aadad6c84b5bce370d076137efecf6adbbf6feddbe0515fb17e"
            ],
            "process_name": "/usr/libexec/nm-dispatcher",
            "process_pid": [
                24200
            ],
            "process_reputation": "NOT_LISTED",
            "process_start_time": "2020-08-11T14:35:30.437Z",
            "process_username": [
                "root"
            ],
            "ttp": [
                "RUN_UNKNOWN_APP",
                "UNKNOWN_APP"
            ]
        },
        {
            "_s3_location": "TlzX4o6VS1-Qalf_49Agrg:173de04abb8:1260aa:6fa:default:3",
            "backend_timestamp": "2020-08-11T14:55:14.776Z",
            "device_external_ip": "192.168.0.1",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 176678,
            "device_internal_ip": "",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "policy-restrictive",
            "device_policy_id": 11200,
            "device_timestamp": "2020-08-11T14:54:40.064Z",
            "enriched": True,
            "enriched_event_type": "CREATE_PROCESS",
            "event_description": "The application \"<share><link hash=\"2206d95e0a435aadad6c84b5bce370d076137efecf6adbbf6feddbe0515fb17e\">/usr/libexec/nm-dispatcher</link></share>\" invoked the application \"<share><link hash=\"9edd4a6490d43440da046535e8378894490fa0827a2b7101004fb776a0bd7092\">/etc/NetworkManager/dispatcher.d/20-chrony</link></share>\". ",
            "event_id": "9579a33cdbe211eab3c8c1649f240e08",
            "event_type": "childproc",
            "has_children": True,
            "index_class": "default",
            "ingress_time": 1597157696823,
            "legacy": True,
            "org_id": "test",
            "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00sibling3parent",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/libexec/nm-dispatcher"
            ],
            "process_guid": "test-0002b226-00000f79-00000000-1d66fef56e95f10",
            "process_hash": [
                "2206d95e0a435aadad6c84b5bce370d076137efecf6adbbf6feddbe0515fb17e"
            ],
            "process_name": "/usr/libexec/nm-dispatcher",
            "process_pid": [
                3961
            ],
            "process_reputation": "NOT_LISTED",
            "process_start_time": "2020-08-11T14:54:40.001Z",
            "process_username": [
                "root"
            ],
            "ttp": [
                "RUN_UNKNOWN_APP",
                "UNKNOWN_APP"
            ]
        }
    ],
    "parent": {
        "_s3_location": "A7Y2cg0hRsKblxNp_sqYRg:1742ca784d0:63a96:600:default:3",
        "backend_timestamp": "2020-08-26T21:23:30.081Z",
        "device_external_ip": "192.168.0.1",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "192.168.0.1",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "policy-restrictive",
        "device_policy_id": 11200,
        "device_timestamp": "2020-08-26T20:20:01.712Z",
        "enriched": True,
        "enriched_event_type": "CREATE_PROCESS",
        "event_description": "The application \"<share><link hash=\"81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85\">/usr/lib/systemd/systemd</link></share>\" invoked the application \"<share><link hash=\"485750de49ee527061ef804def367bc21e8fed6eae6b8ea5261331e65a46e8bb\">/usr/lib/systemd/systemd-cgroups-agent</link></share>\". ",
        "event_id": "9cd2c752e7d911ea9affe54c85cd133a",
        "event_type": "childproc",
        "has_children": True,
        "index_class": "default",
        "ingress_time": 1598476990368,
        "legacy": True,
        "org_id": "test",
        "partition_id": 0,
        "process_guid": "test-0002b226-00000001-00000000-1d6225bbba74c01",
        "process_hash": [
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [
            1
        ],
        "process_reputation": "NOT_LISTED",
        "process_start_time": "2020-05-04T21:34:03.968Z",
        "ttp": [
            "RUN_UNKNOWN_APP",
            "UNKNOWN_APP"
        ]
    },
    "children": None
}

GET_PROCESS_SUMMARY_RESP_1 = {
    "incomplete_results": False,
    "process": {
        "_s3_location": "1zQ8BfT2QUeXYSUjbQjZkQ:1747e718a0f:cd903:1059:default:3",
        "backend_timestamp": "2020-09-11T18:33:27.336Z",
        "childproc_count": 0,
        "crossproc_count": 0,
        "device_external_ip": "52.56.32.175",
        "device_group_id": 0,
        "device_id": 3410694,
        "device_internal_ip": "10.240.0.114",
        "device_name": "win10-carbonblack",
        "device_os": "WINDOWS",
        "device_policy": "default",
        "device_policy_id": 6525,
        "device_timestamp": "2020-09-11T18:31:13.327Z",
        "filemod_count": 0,
        "has_children": True,
        "index_class": "default",
        "ingress_time": 1599849196001,
        "modload_count": 0,
        "netconn_count": 0,
        "org_id": "7DESJ9GN",
        "parent_guid": "7DESJ9GN-00340b06-000002a8-00000000-1d686b9e470289e",
        "parent_hash": [
            "5f48638e3397204c2c63d7b76d025d62302d0e45fc5055c0a692b0bbc7e6b337",
            "858e3da84c5389952e1ad3701e410f61"
        ],
        "parent_name": "c:\\windows\\system32\\smss.exe",
        "parent_pid": 680,
        "partition_id": 0,
        "process_cmdline": [
            "wininit.exe"
        ],
        "process_effective_reputation": "TRUSTED_WHITE_LIST",
        "process_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
        "process_hash": [
            "e83650f70459a027aa596e1a73c961a1",
            "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e"
        ],
        "process_name": "c:\\windows\\system32\\wininit.exe",
        "process_pid": [
            788
        ],
        "process_reputation": "TRUSTED_WHITE_LIST",
        "process_start_time": "2020-09-09T15:00:02.039Z",
        "process_username": [
            "NT AUTHORITY\\SYSTEM"
        ],
        "regmod_count": 0,
        "scriptload_count": 0
    },
    "siblings": [
        {
            "_s3_location": "1zQ8BfT2QUeXYSUjbQjZkQ:1747e718a0f:29a37:1129:default:3",
            "backend_timestamp": "2020-09-11T18:33:27.336Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "52.56.32.175",
            "device_group_id": 0,
            "device_id": 3410694,
            "device_internal_ip": "10.240.0.114",
            "device_name": "win10-carbonblack",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T18:31:13.326Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599849196001,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "7DESJ9GN-00340b06-000002a8-00000000-1d686b9e470289e",
            "parent_hash": [
                "5f48638e3397204c2c63d7b76d025d62302d0e45fc5055c0a692b0bbc7e6b337",
                "858e3da84c5389952e1ad3701e410f61"
            ],
            "parent_name": "c:\\windows\\system32\\smss.exe",
            "parent_pid": 680,
            "partition_id": 0,
            "process_cmdline": [
                "%SystemRoot%\\system32\\csrss.exe ObjectDirectory=\\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "7DESJ9GN-00340b06-000002b0-00000000-1d686b9e4bdf819",
            "process_hash": [
                "23019322ffecb179746210be52d6de60",
                "f2c7d894abe8ac0b4c2a597caa6b3efe7ad2bdb4226845798d954c5ab9c9bf15"
            ],
            "process_name": "c:\\windows\\system32\\csrss.exe",
            "process_pid": [
                688
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-09-09T15:00:01.873Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        }
    ],
    "parent": {},
    "children": [
        {
            "_s3_location": "1zQ8BfT2QUeXYSUjbQjZkQ:1747e718a0f:1e258:125d:default:3",
            "backend_timestamp": "2020-09-11T18:33:27.336Z",
            "childproc_count": 0,
            "crossproc_count": 19,
            "device_external_ip": "52.56.32.175",
            "device_group_id": 0,
            "device_id": 3410694,
            "device_internal_ip": "10.240.0.114",
            "device_name": "win10-carbonblack",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T18:31:13.332Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599849196001,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
            "parent_hash": [
                "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                "e83650f70459a027aa596e1a73c961a1"
            ],
            "parent_name": "c:\\windows\\system32\\wininit.exe",
            "parent_pid": 788,
            "partition_id": 0,
            "process_cmdline": [
                "\"fontdrvhost.exe\""
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "7DESJ9GN-00340b06-00000288-00000000-1d686b9e55303cd",
            "process_hash": [
                "87295b931a8811415c3e8e9db19eed93",
                "725ffd2bc38975251262e85335e2c68b67a6c645d1948e5c39d43fb976327625"
            ],
            "process_name": "c:\\windows\\system32\\fontdrvhost.exe",
            "process_pid": [
                648
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-09-09T15:00:02.850Z",
            "process_username": [
                "Font Driver Host\\UMFD-0"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "FPzxTk8ORr2rGTrMkESxEg:1747ec36d68:17e08f:e23:default:3",
            "backend_timestamp": "2020-09-11T20:03:23.737Z",
            "childproc_count": 240,
            "crossproc_count": 174,
            "device_external_ip": "52.56.32.175",
            "device_group_id": 0,
            "device_id": 3410694,
            "device_internal_ip": "10.240.0.114",
            "device_name": "win10-carbonblack",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T20:00:03.353Z",
            "filemod_count": 0,
            "has_children": True,
            "index_class": "default",
            "ingress_time": 1599854555174,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
            "parent_hash": [
                "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                "e83650f70459a027aa596e1a73c961a1"
            ],
            "parent_name": "c:\\windows\\system32\\wininit.exe",
            "parent_pid": 788,
            "partition_id": 0,
            "process_cmdline": [
                "C:\\WINDOWS\\system32\\services.exe"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "7DESJ9GN-00340b06-0000038c-00000000-1d686b9e4ea6b5d",
            "process_hash": [
                "bccc12eb2ef644e662a63a023fb83f9b",
                "9090e0e44e14709fb09b23b98572e0e61c810189e2de8f7156021bc81c3b1bb6"
            ],
            "process_name": "c:\\windows\\system32\\services.exe",
            "process_pid": [
                908
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-09-09T15:00:02.164Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 50,
            "scriptload_count": 0
        },
        {
            "_s3_location": "ltDe2vIiR-6lbYmDSw-C-g:1747ed60f87:f9583:13cd:default:3",
            "backend_timestamp": "2020-09-11T20:23:23.545Z",
            "childproc_count": 0,
            "crossproc_count": 21932,
            "device_external_ip": "52.56.32.175",
            "device_group_id": 0,
            "device_id": 3410694,
            "device_internal_ip": "10.240.0.114",
            "device_name": "win10-carbonblack",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T20:22:15.443Z",
            "filemod_count": 12,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599855773364,
            "modload_count": 19,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
            "parent_hash": [
                "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                "e83650f70459a027aa596e1a73c961a1"
            ],
            "parent_name": "c:\\windows\\system32\\wininit.exe",
            "parent_pid": 788,
            "partition_id": 0,
            "process_cmdline": [
                "C:\\WINDOWS\\system32\\lsass.exe"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "7DESJ9GN-00340b06-000003a0-00000000-1d686b9e4f52684",
            "process_hash": [
                "5373e4594a071fe6031ad481cd23e910",
                "fea3f1f82ac2109b5abd187d7a8c1688d99dc356f9f40dc904ac0b524f28b428"
            ],
            "process_name": "c:\\windows\\system32\\lsass.exe",
            "process_pid": [
                928
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-09-09T15:00:02.235Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 53,
            "scriptload_count": 0
        }
    ]
}

GET_PROCESS_SUMMARY_RESP_2 = {
    "incomplete_results": False,
    "process": {
        "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747ee5271b:8083:a6c:default:3",
        "backend_timestamp": "2020-09-11T20:39:41.081Z",
        "childproc_count": 22357,
        "crossproc_count": 0,
        "device_external_ip": "173.73.46.160",
        "device_group_id": 0,
        "device_id": 3478460,
        "device_name": "va-centos7.vykin.corp",
        "device_os": "LINUX",
        "device_policy": "default",
        "device_policy_id": 6525,
        "device_timestamp": "2020-09-11T20:39:16.694Z",
        "filemod_count": 0,
        "has_children": False,
        "hits": True,
        "index_class": "default",
        "ingress_time": 1599856756730,
        "modload_count": 0,
        "netconn_count": 0,
        "org_id": "7DESJ9GN",
        "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
        "parent_hash": [
            "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
            "87725cbc9055be67cda79414fd8dccd6"
        ],
        "parent_name": "/usr/lib/systemd/systemd",
        "parent_pid": 1,
        "partition_id": 0,
        "process_cmdline": [
            "/bin/bash /usr/sbin/ksmtuned"
        ],
        "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
        "process_guid": "7DESJ9GN-003513bc-0000035c-00000000-1d640200c9a6204",
        "process_hash": [
            "708c8760385810080c4d17fa84d325ca"
        ],
        "process_name": "/usr/bin/bash",
        "process_pid": [
            860
        ],
        "process_reputation": "ADAPTIVE_WHITE_LIST",
        "process_start_time": "2020-06-11T18:42:24.858Z",
        "process_username": [
            "root"
        ],
        "regmod_count": 0,
        "scriptload_count": 0
    },
    "siblings": [
        {
            "_s3_location": "_Xk5yNrjRRiqmIfAAcr26A:173ea44c5a6:137f23:86b:default:3",
            "backend_timestamp": "2020-08-14T00:00:42.406Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_internal_ip": "",
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-14T00:00:01.788Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597363224591,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-000019c6-00000000-1d671cddb5b78ad",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                6598
            ],
            "process_start_time": "2020-08-14T00:00:01.644Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "_in4MdzcS3uUqLXSuFy0ww:173ef6bfb69:145d:7ea:default:3",
            "backend_timestamp": "2020-08-15T00:01:38.153Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_internal_ip": "",
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-15T00:00:02.188Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597449659529,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00006014-00000000-1d6729705d29cfd",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                24596
            ],
            "process_start_time": "2020-08-15T00:00:01.732Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "nK4ZAllTTGWA2el4767vNw:173f492e88c:17dab:ad1:default:3",
            "backend_timestamp": "2020-08-16T00:02:15.308Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-16T00:00:01.873Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597536094510,
            "modload_count": 0,
            "netconn_count": 8,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-000028fe-00000000-1d673603042be6c",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                10494
            ],
            "process_start_time": "2020-08-16T00:00:01.774Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "nK4ZAllTTGWA2el4767vNw:173f558b0a5:125978:6cd:default:3",
            "backend_timestamp": "2020-08-16T03:38:17.125Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-16T03:37:02.074Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597549059689,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/httpd -k graceful"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000338b-00000000-1d6737e80ebb1c1",
            "process_name": "/usr/sbin/httpd",
            "process_pid": [
                13195
            ],
            "process_start_time": "2020-08-16T03:37:02.001Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "0zHUwGLnSmGzkZYs_8xnoA:173f9b80ecd:177e2:78d:default:3",
            "backend_timestamp": "2020-08-17T00:00:56.012Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-17T00:00:01.925Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597622409598,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00006f46-00000000-1d674295aa453fd",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                28486
            ],
            "process_start_time": "2020-08-17T00:00:01.720Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "0zHUwGLnSmGzkZYs_8xnoA:173fedec55c:174fe:74b:default:3",
            "backend_timestamp": "2020-08-18T00:01:19.195Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-18T00:00:01.887Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597708844529,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000380f-00000000-1d674f285205671",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                14351
            ],
            "process_start_time": "2020-08-18T00:00:01.840Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "0zHUwGLnSmGzkZYs_8xnoA:1740405bf2f:a6f31:739:default:3",
            "backend_timestamp": "2020-08-19T00:01:59.598Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-19T00:00:01.695Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597795279798,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00007e3e-00000000-1d675bbaf703c4f",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                32318
            ],
            "process_start_time": "2020-08-19T00:00:01.671Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "VdeeCC10RSq6eQFQJJ45wg:174092c56ac:15a050:83e:default:3",
            "backend_timestamp": "2020-08-20T00:02:14.828Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-20T00:00:01.748Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597881715927,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000472d-00000000-1d67684d9d9f281",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                18221
            ],
            "process_start_time": "2020-08-20T00:00:01.670Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "nk9Vb3ztTeeqApAPwMBxpg:1740e5152f9:1076d2:96d:default:3",
            "backend_timestamp": "2020-08-21T00:00:44.793Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-21T00:00:01.624Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1597968029700,
            "modload_count": 0,
            "netconn_count": 7,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00000fe7-00000000-1d6774e04306a2a",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                4071
            ],
            "process_start_time": "2020-08-21T00:00:01.544Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "5EqvaRjTRsC3dW0kdOwebg:17413784b57:2fa2c:9d2:default:3",
            "backend_timestamp": "2020-08-22T00:01:24.822Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-22T00:00:01.563Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598054464768,
            "modload_count": 0,
            "netconn_count": 7,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00005604-00000000-1d678172e9625eb",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                22020
            ],
            "process_start_time": "2020-08-22T00:00:01.518Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "9OjDUqvMTIeayMW5MuPjyg:174189f3872:15bfa5:839:default:3",
            "backend_timestamp": "2020-08-23T00:02:01.969Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-23T00:00:01.662Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598140899882,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00001f0f-00000000-1d678e058fb0106",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                7951
            ],
            "process_start_time": "2020-08-23T00:00:01.486Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "9OjDUqvMTIeayMW5MuPjyg:174196afd8e:5756:6e1:default:3",
            "backend_timestamp": "2020-08-23T03:44:36.237Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-23T03:42:01.847Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598154225276,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/httpd -k graceful"
            ],
            "process_guid": "7DESJ9GN-003513bc-000029f9-00000000-1d678ff5c776813",
            "process_name": "/usr/sbin/httpd",
            "process_pid": [
                10745
            ],
            "process_start_time": "2020-08-23T03:42:01.733Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "MoUnZzf0RFindL_WdF_fhQ:1741dc4a3d0:a92:872:default:3",
            "backend_timestamp": "2020-08-24T00:01:00.367Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-24T00:00:01.588Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598227215373,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-000065b9-00000000-1d679a9836d5d9b",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                26041
            ],
            "process_start_time": "2020-08-24T00:00:01.542Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "RwluBVy2ThywZp2mP3b44A:17422eb711d:451f:74a:default:3",
            "backend_timestamp": "2020-08-25T00:01:29.373Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-25T00:00:01.608Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598313651764,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00002e88-00000000-1d67a72addbff81",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                11912
            ],
            "process_start_time": "2020-08-25T00:00:01.574Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "zRU9q_gMRQKBLTA4ztiaPg:17428126093:189fb1:808:default:3",
            "backend_timestamp": "2020-08-26T00:02:07.122Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-26T00:00:01.663Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598400086120,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-000074f2-00000000-1d67b3bd84b9a7b",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                29938
            ],
            "process_start_time": "2020-08-26T00:00:01.612Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "zRU9q_gMRQKBLTA4ztiaPg:1742d393b2f:3a8a:756:default:3",
            "backend_timestamp": "2020-08-27T00:02:39.534Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-27T00:00:01.722Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598486521086,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00003dc1-00000000-1d67c0502b9cdf2",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                15809
            ],
            "process_start_time": "2020-08-27T00:00:01.642Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "zRU9q_gMRQKBLTA4ztiaPg:174325e3df3:137b3:951:default:3",
            "backend_timestamp": "2020-08-28T00:01:11.154Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-28T00:00:01.819Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598572835844,
            "modload_count": 0,
            "netconn_count": 6,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000060d-00000000-1d67cce2d290b6f",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                1549
            ],
            "process_start_time": "2020-08-28T00:00:01.678Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "NApwKulRTnCEAVbUNi4ynA:174378504e1:8db3c:8bf:default:3",
            "backend_timestamp": "2020-08-29T00:01:38.528Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-29T00:00:01.748Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598659270938,
            "modload_count": 0,
            "netconn_count": 6,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00004d29-00000000-1d67d9757905492",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                19753
            ],
            "process_start_time": "2020-08-29T00:00:01.661Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "0IWxrKukQB6PQ1KHHk84DA:1743cabd09b:82f57:81a:default:3",
            "backend_timestamp": "2020-08-30T00:02:07.131Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-30T00:00:01.633Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598745706003,
            "modload_count": 0,
            "netconn_count": 5,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00001632-00000000-1d67e6081f27e41",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                5682
            ],
            "process_start_time": "2020-08-30T00:00:01.612Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "0IWxrKukQB6PQ1KHHk84DA:1743d5baf80:276aa:6d9:default:3",
            "backend_timestamp": "2020-08-30T03:14:12.991Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-30T03:13:01.942Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598757230648,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/httpd -k graceful"
            ],
            "process_guid": "7DESJ9GN-003513bc-00001fcd-00000000-1d67e7b78518b3e",
            "process_name": "/usr/sbin/httpd",
            "process_pid": [
                8141
            ],
            "process_start_time": "2020-08-30T03:13:01.869Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "R7QTKS2XRIav8AM20latpA:17441d11dd4:1019f:aad:default:3",
            "backend_timestamp": "2020-08-31T00:00:57.811Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-08-31T00:00:01.612Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598832021141,
            "modload_count": 0,
            "netconn_count": 9,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00005cdf-00000000-1d67f29ac4d6e4b",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                23775
            ],
            "process_start_time": "2020-08-31T00:00:01.515Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "g-kvhW7JTOCQ3Rr3AHlhcg:17446f82921:13fd7:7bd:default:3",
            "backend_timestamp": "2020-09-01T00:01:42.688Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "test",
            "device_policy_id": 32064,
            "device_timestamp": "2020-09-01T00:00:01.279Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1598918456032,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-000025d1-00000000-1d67ff2d681b15b",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                9681
            ],
            "process_start_time": "2020-09-01T00:00:01.164Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "g-kvhW7JTOCQ3Rr3AHlhcg:1744c1e950a:481f4:bff:default:3",
            "backend_timestamp": "2020-09-02T00:01:46.762Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-02T00:00:01.512Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599004890752,
            "modload_count": 0,
            "netconn_count": 12,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00006c65-00000000-1d680bc0111e47e",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                27749
            ],
            "process_start_time": "2020-09-02T00:00:01.416Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "g-kvhW7JTOCQ3Rr3AHlhcg:17451476e04:90012:60b:default:3",
            "backend_timestamp": "2020-09-03T00:04:29.828Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-03T00:00:01.945Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599091205796,
            "modload_count": 0,
            "netconn_count": 6,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000352c-00000000-1d681852b7729c2",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                13612
            ],
            "process_start_time": "2020-09-03T00:00:01.387Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:174566a8534:63df6:94e:default:3",
            "backend_timestamp": "2020-09-04T00:00:55.604Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-04T00:00:01.497Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599177640730,
            "modload_count": 0,
            "netconn_count": 7,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00007bc0-00000000-1d6824e55e5fa6e",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                31680
            ],
            "process_start_time": "2020-09-04T00:00:01.420Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:17456ea698c:94a04:6fc:default:3",
            "backend_timestamp": "2020-09-04T02:20:37.131Z",
            "childproc_count": 1,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-04T02:15:19.594Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599185804020,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/gdm"
            ],
            "process_effective_reputation": "NOT_LISTED",
            "process_guid": "7DESJ9GN-003513bc-000004d5-00000000-1d640200c9a6223",
            "process_hash": [
                "1ad760c90a4ac42ca439c161e1fee92d",
                "6386c1749f38f3767d6421224560763f4f05be4c5084da0062e1a97cad7b181a"
            ],
            "process_name": "/usr/sbin/gdm",
            "process_pid": [
                1237
            ],
            "process_reputation": "NOT_LISTED",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:17456ea698c:94303:701:default:3",
            "backend_timestamp": "2020-09-04T02:20:37.131Z",
            "childproc_count": 1,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-04T02:15:19.594Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599185804020,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/libvirtd"
            ],
            "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "process_guid": "7DESJ9GN-003513bc-000004c7-00000000-1d640200c9a6216",
            "process_hash": [
                "821207448d809fcf556cccddb6e6732d",
                "d92f4495e1c19d745f3094cd7eda22fb66e0041b3cae70bff68d5d3ac2efec94"
            ],
            "process_name": "/usr/sbin/libvirtd",
            "process_pid": [
                1223,
                1770
            ],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:17456ea698c:95100:71c:default:3",
            "backend_timestamp": "2020-09-04T02:20:37.131Z",
            "childproc_count": 29,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-04T02:15:19.594Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599185804020,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/bin/sh /usr/libexec/postfix/postfix-script start"
            ],
            "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "process_guid": "7DESJ9GN-003513bc-000004e1-00000000-1d640200c9a6229",
            "process_hash": [
                "708c8760385810080c4d17fa84d325ca",
                "a5f3d6f51fe87d0a01b4d4a1907952bdaf31b5f0887f5b2253a83f9f0180c2ce"
            ],
            "process_name": "/usr/bin/bash",
            "process_pid": [
                1249,
                1871
            ],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:17456ea698c:92def:6fb:default:3",
            "backend_timestamp": "2020-09-04T02:20:37.131Z",
            "childproc_count": 1,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-04T02:15:19.594Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599185804020,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/sbin/auditd"
            ],
            "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "process_guid": "7DESJ9GN-003513bc-000002ee-00000000-1d640200c9a61e8",
            "process_hash": [
                "fd1d4ab71650a77ae6df973bad437cf6",
                "fb728051d437f42c7846bb0b72fb6452c8968d8c62313f69a503b7732732dab2"
            ],
            "process_name": "/usr/sbin/auditd",
            "process_pid": [
                750
            ],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "f37_1xorTheYfgDXyKjK5Q:1745b9abcad:3a1e9:60e:default:3",
            "backend_timestamp": "2020-09-05T00:11:41.612Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-05T00:00:01.587Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599264075663,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000447d-00000000-1d68317804e76df",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                17533
            ],
            "process_start_time": "2020-09-05T00:00:01.412Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "eXEydrSES8O_AnnKDUbmTg:17460bd7a74:6b64b:608:default:3",
            "backend_timestamp": "2020-09-06T00:07:44.499Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-06T00:00:01.953Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599350510903,
            "modload_count": 0,
            "netconn_count": 3,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00000d92-00000000-1d683e0aad585c1",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                3474
            ],
            "process_start_time": "2020-09-06T00:00:01.604Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0,
            "watchlist_hit": [
                "mrTB06fAQbeNfvl47cQiGg:MLRtPcpQGKFh5OE4BT3tQ-1ba9bd74-cdd2-4764-865b-70c9ad51ec4c:9"
            ]
        },
        {
            "_s3_location": "eXEydrSES8O_AnnKDUbmTg:1746187eef0:1226d:6e0:default:3",
            "backend_timestamp": "2020-09-06T03:48:52.592Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-06T03:46:01.965Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599364076440,
            "modload_count": 0,
            "netconn_count": 4,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/httpd -k graceful"
            ],
            "process_guid": "7DESJ9GN-003513bc-00001897-00000000-1d684003d666dd2",
            "process_name": "/usr/sbin/httpd",
            "process_pid": [
                6295
            ],
            "process_start_time": "2020-09-06T03:46:01.899Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "eXEydrSES8O_AnnKDUbmTg:1746187eef0:10379:672:default:3",
            "backend_timestamp": "2020-09-06T03:48:52.592Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-06T03:46:02.009Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599364076440,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_guid": "7DESJ9GN-003513bc-000004c6-00000000-1d640200c9a6210",
            "process_name": "/usr/sbin/httpd",
            "process_pid": [
                1222
            ],
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "eXEydrSES8O_AnnKDUbmTg:17465ddc071:7069:b61:default:3",
            "backend_timestamp": "2020-09-07T00:01:05.649Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-07T00:00:01.883Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599436825914,
            "modload_count": 0,
            "netconn_count": 11,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00005404-00000000-1d684a9d56373dc",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                21508
            ],
            "process_start_time": "2020-09-07T00:00:01.841Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "FWvAZpaeTCGnSIVk-vKRKw:1746b048a63:f4ca:9be:default:3",
            "backend_timestamp": "2020-09-08T00:01:33.794Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-08T00:00:02.085Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599523261123,
            "modload_count": 0,
            "netconn_count": 8,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00001cd3-00000000-1d68572ffe60cbf",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                7379
            ],
            "process_start_time": "2020-09-08T00:00:02.004Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "FWvAZpaeTCGnSIVk-vKRKw:174702b3134:62ecb:90e:default:3",
            "backend_timestamp": "2020-09-09T00:01:52.947Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-09T00:00:00.389Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599609696323,
            "modload_count": 0,
            "netconn_count": 6,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00006311-00000000-1d6863c2947d074",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                25361
            ],
            "process_start_time": "2020-09-09T00:00:00.274Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "H3x-OibrQF609SeRWUooMw:17475505824:127a8f:a52:default:3",
            "backend_timestamp": "2020-09-10T00:00:33.827Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-10T00:00:00.976Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599696011346,
            "modload_count": 0,
            "netconn_count": 8,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-00002c12-00000000-1d6870554072d2d",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                11282
            ],
            "process_start_time": "2020-09-10T00:00:00.835Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "H3x-OibrQF609SeRWUooMw:1747a775afe:37b90:991:default:3",
            "backend_timestamp": "2020-09-11T00:01:16.541Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T00:00:00.901Z",
            "filemod_count": 0,
            "has_children": False,
            "index_class": "default",
            "ingress_time": 1599782446477,
            "modload_count": 0,
            "netconn_count": 7,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/unbound-anchor -a /var/lib/unbound/root.key -c /etc/unbound/icannbundle.pem"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000724f-00000000-1d687ce7e6ea6f4",
            "process_name": "/usr/sbin/unbound-anchor",
            "process_pid": [
                29263
            ],
            "process_start_time": "2020-09-11T00:00:00.820Z",
            "process_username": [
                "unbound"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747e616ae0:1c076:5ff:default:3",
            "backend_timestamp": "2020-09-11T18:15:47.680Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T18:13:14.117Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599848113224,
            "modload_count": 0,
            "netconn_count": 21,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/ntpd -u ntp:ntp -g"
            ],
            "process_guid": "7DESJ9GN-003513bc-0000031d-00000000-1d640200c9a61f4",
            "process_name": "/usr/sbin/ntpd",
            "process_pid": [
                797
            ],
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "ntp"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747ec641f0:c861:83a:default:3",
            "backend_timestamp": "2020-09-11T20:05:56.334Z",
            "childproc_count": 55,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T20:03:43.702Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599854715897,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/bin/rhsmcertd"
            ],
            "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "process_guid": "7DESJ9GN-003513bc-000004ca-00000000-1d640200c9a6220",
            "process_hash": [
                "46f45e96525fd1e7a4215566952b98f5",
                "53acf3e7f2c44dbabb63c1f0296fa0fbffc7056da6a41420bf7a3556f208821f"
            ],
            "process_name": "/usr/bin/rhsmcertd",
            "process_pid": [
                1226
            ],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747ede2c55:1089:846:default:3",
            "backend_timestamp": "2020-09-11T20:32:03.654Z",
            "childproc_count": 1312,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T20:30:01.199Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599856276616,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/sbin/crond -n"
            ],
            "process_effective_reputation": "NOT_LISTED",
            "process_guid": "7DESJ9GN-003513bc-000004d0-00000000-1d640200c9a6221",
            "process_hash": [
                "cfc5bcb6e5e4e336ae8c07937d7aa3fd",
                "bd0b2aa853dfd355147bfd6e71194d25d84fa1c67fa161b4ac0a35a7ac98b092"
            ],
            "process_name": "/usr/sbin/crond",
            "process_pid": [
                1232,
                12525
            ],
            "process_reputation": "NOT_LISTED",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "root"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        {
            "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747ede2c55:0:954:default:3",
            "backend_timestamp": "2020-09-11T20:32:03.654Z",
            "childproc_count": 5228,
            "crossproc_count": 0,
            "device_external_ip": "173.73.46.160",
            "device_group_id": 0,
            "device_id": 3478460,
            "device_name": "va-centos7.vykin.corp",
            "device_os": "LINUX",
            "device_policy": "default",
            "device_policy_id": 6525,
            "device_timestamp": "2020-09-11T20:30:01.240Z",
            "filemod_count": 0,
            "has_children": False,
            "hits": True,
            "index_class": "default",
            "ingress_time": 1599856276616,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "7DESJ9GN",
            "parent_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
            "parent_hash": [
                "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595",
                "87725cbc9055be67cda79414fd8dccd6"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/lib/polkit-1/polkitd --no-debug"
            ],
            "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "process_guid": "7DESJ9GN-003513bc-00000310-00000000-1d640200c9a61ed",
            "process_hash": [
                "07b80c3203bdecc78694b7647dd7bd69",
                "69dc94daf0d812e3a45af10955b235d24c0df7d5dd626af8f965e4b3b86359f7"
            ],
            "process_name": "/usr/lib/polkit-1/polkitd",
            "process_pid": [
                784
            ],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_start_time": "2020-06-11T18:42:24.858Z",
            "process_username": [
                "polkitd"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        }
    ],
    "parent": {
        "_s3_location": "-CHEXEN9SJm-exKd1dKzqQ:1747ede2c55:954:735:default:3",
        "backend_timestamp": "2020-09-11T20:32:03.654Z",
        "childproc_count": 0,
        "crossproc_count": 0,
        "device_external_ip": "173.73.46.160",
        "device_group_id": 0,
        "device_id": 3478460,
        "device_name": "va-centos7.vykin.corp",
        "device_os": "LINUX",
        "device_policy": "default",
        "device_policy_id": 6525,
        "device_timestamp": "2020-09-11T20:30:01.226Z",
        "filemod_count": 0,
        "has_children": True,
        "hits": True,
        "index_class": "default",
        "ingress_time": 1599856276616,
        "modload_count": 0,
        "netconn_count": 0,
        "org_id": "7DESJ9GN",
        "partition_id": 0,
        "process_effective_reputation": "ADAPTIVE_WHITE_LIST",
        "process_guid": "test-003513bc-00000001-00000000-1d640200c9a61d7",
        "process_hash": [
            "87725cbc9055be67cda79414fd8dccd6",
            "205ee15c06c93dea209cbfcabeee3bc8db85221e387df252556f7ac18db4b595"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [
            1
        ],
        "process_reputation": "ADAPTIVE_WHITE_LIST",
        "process_start_time": "2020-06-11T18:42:24.858Z",
        "regmod_count": 0,
        "scriptload_count": 0
    },
    "children": [
            {
                "_s3_location": "1zQ8BfT2QUeXYSUjbQjZkQ:1747e718a0f:1e258:125d:default:3",
                "backend_timestamp": "2020-09-11T18:33:27.336Z",
                "childproc_count": 0,
                "crossproc_count": 19,
                "device_external_ip": "52.56.32.175",
                "device_group_id": 0,
                "device_id": 3410694,
                "device_internal_ip": "10.240.0.114",
                "device_name": "win10-carbonblack",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 6525,
                "device_timestamp": "2020-09-11T18:31:13.332Z",
                "filemod_count": 0,
                "has_children": False,
                "index_class": "default",
                "ingress_time": 1599849196001,
                "modload_count": 0,
                "netconn_count": 0,
                "org_id": "7DESJ9GN",
                "parent_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
                "parent_hash": [
                    "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                    "e83650f70459a027aa596e1a73c961a1"
                ],
                "parent_name": "c:\\windows\\system32\\wininit.exe",
                "parent_pid": 788,
                "partition_id": 0,
                "process_cmdline": [
                    "\"fontdrvhost.exe\""
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "7DESJ9GN-00340b06-00000288-00000000-1d686b9e55303cd",
                "process_hash": [
                    "87295b931a8811415c3e8e9db19eed93",
                    "725ffd2bc38975251262e85335e2c68b67a6c645d1948e5c39d43fb976327625"
                ],
                "process_name": "c:\\windows\\system32\\fontdrvhost.exe",
                "process_pid": [
                    648
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-09-09T15:00:02.850Z",
                "process_username": [
                    "Font Driver Host\\UMFD-0"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            },
            {
                "_s3_location": "FPzxTk8ORr2rGTrMkESxEg:1747ec36d68:17e08f:e23:default:3",
                "backend_timestamp": "2020-09-11T20:03:23.737Z",
                "childproc_count": 240,
                "crossproc_count": 174,
                "device_external_ip": "52.56.32.175",
                "device_group_id": 0,
                "device_id": 3410694,
                "device_internal_ip": "10.240.0.114",
                "device_name": "win10-carbonblack",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 6525,
                "device_timestamp": "2020-09-11T20:00:03.353Z",
                "filemod_count": 0,
                "has_children": True,
                "index_class": "default",
                "ingress_time": 1599854555174,
                "modload_count": 0,
                "netconn_count": 0,
                "org_id": "7DESJ9GN",
                "parent_guid": "7DESJ9GN-00340b06-00000314-00000000-1d686b9e4d74f52",
                "parent_hash": [
                    "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                    "e83650f70459a027aa596e1a73c961a1"
                ],
                "parent_name": "c:\\windows\\system32\\wininit.exe",
                "parent_pid": 788,
                "partition_id": 0,
                "process_cmdline": [
                    "C:\\WINDOWS\\system32\\services.exe"
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "7DESJ9GN-00340b06-0000038c-00000000-1d686b9e4ea6b5d",
                "process_hash": [
                    "bccc12eb2ef644e662a63a023fb83f9b",
                    "9090e0e44e14709fb09b23b98572e0e61c810189e2de8f7156021bc81c3b1bb6"
                ],
                "process_name": "c:\\windows\\system32\\services.exe",
                "process_pid": [
                    908
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-09-09T15:00:02.164Z",
                "process_username": [
                    "NT AUTHORITY\\SYSTEM"
                ],
                "regmod_count": 50,
                "scriptload_count": 0
            },
    ]
}

GET_TREE_RESP = {
    "incomplete_results": False,
    "nodes": {
        "_s3_location": "A7Y2cg0hRsKblxNp_sqYRg:1742d01db15:a8a2:5fb:default:3",
        "backend_timestamp": "2020-08-26T23:02:192.357Z",
        "children": [
            {
                "_s3_location": "nNWpDm_5QXG5vVI5c9YG-Q:1720df24ea4:0:69a:longTerm:3",
                "backend_timestamp": "2020-05-13T12:11:23.172Z",
                "device_external_ip": "",
                "device_id": 176678,
                "device_internal_ip": "192.168.0.1",
                "device_name": "devr-dev",
                "device_os": "LINUX",
                "device_policy": "policy-restrictive",
                "device_policy_id": 11200,
                "device_timestamp": "2020-05-13T12:10:02.073Z",
                "enriched": True,
                "enriched_event_type": "CREATE_PROCESS",
                "event_description": "The application \"<share><link hash=\"b9e3723553385b6e3d487bfae3878f9f8e57593ae4ec0a1ff4087f94b8e8368a\">/usr/sbin/crond</link></share>\" invoked the application \"<share><link hash=\"5975d972eea6b1c53ef9a69452797439ed5bf63fae72e1780761ea1c2cb6976a\">/usr/bin/bash</link></share>\". ",
                "event_id": "addca5e2951211eab71c3d5168eb0eaf",
                "event_type": "childproc",
                "has_children": False,
                "index_class": "longTerm",
                "ingress_time": 1589371825851,
                "legacy": True,
                "org_id": "test",
                "parent_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00childtreeparent",
                "parent_hash": [
                    "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
                ],
                "parent_name": "/usr/lib/systemd/systemd",
                "parent_pid": 1,
                "partition_id": 0,
                "process_guid": "test-0002b226-0000192c-00000000-1d6225bbba74c00childtreeproc",
                "process_hash": [
                    "b9e3723553385b6e3d487bfae3878f9f8e57593ae4ec0a1ff4087f94b8e8368a"
                ],
                "process_name": "/usr/sbin/crond",
                "process_pid": [
                    6444
                ],
                "process_reputation": "NOT_LISTED",
                "process_start_time": "2020-05-04T21:34:03.968Z",
                "ttp": [
                    "MITRE_T1059_CMD_LINE_INTER",
                    "RUN_CMD_SHELL",
                    "RUN_UNKNOWN_APP",
                    "UNKNOWN_APP"
                ]
            }
        ],
        "device_external_ip": "192.168.0.1",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "192.168.0.1",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "policy-restrictive",
        "device_policy_id": 11200,
        "device_timestamp": "2020-08-26T23:01:01.754Z",
        "enriched": True,
        "enriched_event_type": "CREATE_PROCESS",
        "event_description": "The application \"<share><link hash=\"81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85\">/usr/lib/systemd/systemd</link></share>\" invoked the application \"<share><link hash=\"485750de49ee527061ef804def367bc21e8fed6eae6b8ea5261331e65a46e8bb\">/usr/lib/systemd/systemd-cgroups-agent</link></share>\". ",
        "event_id": "10a46d36e7f011ea9759353269fbac39",
        "event_type": "childproc",
        "has_children": True,
        "index_class": "default",
        "ingress_time": 1598482893553,
        "legacy": True,
        "org_id": "test",
        "partition_id": 0,
        "process_guid": "test-0002b226-00000001-00000000-1d6225bbba74c00treeproc",
        "process_hash": [
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [
            1
        ],
        "process_reputation": "NOT_LISTED",
        "process_start_time": "2020-05-04T21:34:03.968Z",
        "ttp": [
            "RUN_UNKNOWN_APP",
            "UNKNOWN_APP"
        ]
    }
}

GET_SUMMARY_NOT_FOUND = {
    "message": "Resource does not exist",
    "translation_key": "threathunter_resource_does_not_exist",
    "translation_format_values": None
}
