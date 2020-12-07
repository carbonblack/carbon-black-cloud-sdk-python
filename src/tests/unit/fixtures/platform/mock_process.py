"""Mock responses for process queries."""

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

POST_TREE_SEARCH_JOB_RESP = {
    "job_id": "ee158f11-4dfb-4ae2-8f1a-7707b712226d"
}

GET_TREE_SEARCH_JOB_RESP = {
    "contacted": 34,
    "completed": 34
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
                "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d",
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
                "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
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

GET_PROCESS_SEARCH_JOB_RESULTS_RESP_2 = {
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
                788
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
                "5920199e4fbfa47c1717b863814722148a353e54f8c10912cf1f991a1c86309d",
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
        "fl": "*,parent_hash,parent_name,process_cmdline,backend_timestamp,device_external_ip,device_group,device_internal_ip,device_os,process_effective_reputation,process_reputation,ttp",  # noqa: E501
        "fq": "{!collapse field=process_collapse_id sort='max(0,legacy) asc,device_timestamp desc'}",
        "q": "(process_guid:test-0034d5f2-00000ba0-00000000-1d68709850fe521)",
        "rows": 500,
        "start": 0
    },
    "search_initiated_time": 1599853172533,
    "connector_id": "ABCDEFGH"
}

GET_PROCESS_SUMMARY_RESP = {
  "completed": 30,
  "contacted": 30,
  "exception": "string",
  "summary": {
    "children": [],
    "parent": {
        "_process_filename": "systemd",
        "backend_timestamp": "2020-08-28T19:12:07.989Z",
        "childproc_count": 0,
        "crossproc_count": 0,
        "device_external_ip": "34.56.78.90",
        "device_group_id": 0,
        "device_id": 176678,
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "sm-restrictive",
        "device_policy_id": 11200,
        "device_timestamp": "2020-08-28T19:10:02.123Z",
        "filemod_count": 0,
        "has_children": True,
        "hits": False,
        "ingress_time": 1598641901273,
        "modload_count": 0,
        "netconn_count": 0,
        "org_id": "ABCD1234",
        "process_effective_reputation": "NOT_LISTED",
        "process_guid": "ABCD1234-0002b226-00000001-00000000-1d6225bbba75e43",
        "process_hash": [
            "e4b9902024ac32b3ca37f6b4c9b841e8",
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "process_name": "/usr/lib/systemd/systemd",
        "process_pid": [
            1
        ],
        "process_reputation": "NOT_LISTED",
        "process_start_time": "2020-05-04T21:34:03.968Z",
        "regmod_count": 0,
        "scriptload_count": 0
    },
    "process": {
      "_process_filename": "bash",
      "backend_timestamp": "2020-08-28T19:16:11.959Z",
      "childproc_count": 333580,
      "crossproc_count": 0,
      "device_external_ip": "34.56.78.90",
      "device_group_id": 0,
      "device_id": 176678,
      "device_name": "devr-dev",
      "device_os": "LINUX",
      "device_policy": "sm-restrictive",
      "device_policy_id": 11200,
      "device_timestamp": "2020-08-28T19:14:41.231Z",
      "filemod_count": 0,
      "ingress_time": 1598642141411,
      "modload_count": 0,
      "netconn_count": 0,
      "org_id": "ABCD1234",
      "parent_guid": "ABCD1234-0002b226-00000001-00000000-1d6225bbba75e43",
      "parent_hash": [
          "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85",
          "e4b9902024ac32b3ca37f6b4c9b841e8"
      ],
      "parent_name": "/usr/lib/systemd/systemd",
      "parent_pid": 1,
      "process_cmdline": [
          "/bin/bash /usr/sbin/ksmtuned"
      ],
      "process_effective_reputation": "NOT_LISTED",
      "process_guid": "ABCD1234-0002b226-00001615-00000000-1d6225bbba75e5e",
      "process_hash": [
          "285044ad8f8b9322d0cc5e929e2cc18c",
          "5975d972eea6b1c53ef9a69452797439ed5bf63fae72e1780761ea1c2cb6976a"
      ],
      "process_name": "/usr/bin/bash",
      "process_pid": [
          5653,
          16139
      ],
      "process_reputation": "NOT_LISTED",
      "process_start_time": "2020-05-04T21:34:03.968Z",
      "process_username": [
          "root"
      ],
      "regmod_count": 0,
      "scriptload_count": 0
    },
    "siblings": [
      {
        "_process_filename": "nm-dispatcher",
        "backend_timestamp": "2020-08-19T20:55:33.446Z",
        "childproc_count": 1,
        "crossproc_count": 0,
        "device_external_ip": "34.56.78.90",
        "device_group_id": 0,
        "device_id": 176678,
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "sm-restrictive",
        "device_policy_id": 11200,
        "device_timestamp": "2020-08-19T20:54:44.980Z",
        "filemod_count": 0,
        "has_children": True,
        "hits": False,
        "ingress_time": 1597870506825,
        "modload_count": 0,
        "netconn_count": 0,
        "org_id": "ABCD1234",
        "parent_guid": "ABCD1234-0002b226-00000001-00000000-1d6225bbba75e43",
        "parent_hash": [
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85",
            "e4b9902024ac32b3ca37f6b4c9b841e8"
        ],
        "parent_name": "/usr/lib/systemd/systemd",
        "parent_pid": 1,
        "process_cmdline": [
            "/usr/libexec/nm-dispatcher"
        ],
        "process_effective_reputation": "NOT_LISTED",
        "process_guid": "ABCD1234-0002b226-00005742-00000000-1d6766af7bedb39",
        "process_hash": [
            "04b2450579a663c964f3960cd0cf93a8",
            "2206d95e0a435aadad6c84b5bce370d076137efecf6adbbf6feddbe0515fb17e"
        ],
        "process_name": "/usr/libexec/nm-dispatcher",
        "process_pid": [
            22338
        ],
        "process_reputation": "NOT_LISTED",
        "process_start_time": "2020-08-19T20:54:44.909Z",
        "process_username": [
            "root"
        ],
        "regmod_count": 0,
        "scriptload_count": 0
      }
    ]
  }
}

GET_PROCESS_SUMMARY_RESP_1 = {
    "exception": "",
    "summary": {
        "process": {
            "_process_filename": "csrss.exe",
            "backend_timestamp": "2020-12-03T20:34:38.889Z",
            "childproc_count": 0,
            "crossproc_count": 0,
            "device_external_ip": "24.243.76.124",
            "device_group_id": 0,
            "device_id": 329219,
            "device_internal_ip": "172.16.115.191",
            "device_name": "desktop-8qonquj",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 2198,
            "device_timestamp": "2020-12-03T20:32:21.866Z",
            "filemod_count": 0,
            "has_children": False,
            "ingress_time": 1607027652665,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-00050603-000001f4-00000000-1d6c86e28008165",
            "parent_hash": [
                "5f48638e3397204c2c63d7b76d025d62302d0e45fc5055c0a692b0bbc7e6b337",
                "858e3da84c5389952e1ad3701e410f61"
            ],
            "parent_name": "c:\\windows\\system32\\smss.exe",
            "parent_pid": 500,
            "process_cmdline": [
                "%SystemRoot%\\system32\\csrss.exe ObjectDirectory=\\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "WNEXFKQ7-00050603-00000204-00000000-1d6c86e2801cd1b",
            "process_hash": [
                "23019322ffecb179746210be52d6de60",
                "f2c7d894abe8ac0b4c2a597caa6b3efe7ad2bdb4226845798d954c5ab9c9bf15"
            ],
            "process_name": "c:\\windows\\system32\\csrss.exe",
            "process_pid": [
                516
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-12-02T05:44:09.717Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        },
        "siblings": [
            {
                "_process_filename": "winlogon.exe",
                "backend_timestamp": "2020-12-03T20:34:38.889Z",
                "childproc_count": 0,
                "crossproc_count": 0,
                "device_external_ip": "24.243.76.124",
                "device_group_id": 0,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-03T20:32:08.646Z",
                "filemod_count": 0,
                "has_children": True,
                "hits": False,
                "ingress_time": 1607027652665,
                "modload_count": 0,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-000001f4-00000000-1d6c86e28008165",
                "parent_hash": [
                    "5f48638e3397204c2c63d7b76d025d62302d0e45fc5055c0a692b0bbc7e6b337",
                    "858e3da84c5389952e1ad3701e410f61"
                ],
                "parent_name": "c:\\windows\\system32\\smss.exe",
                "parent_pid": 500,
                "process_cmdline": [
                    "winlogon.exe"
                ],
                "process_effective_reputation": "LOCAL_WHITE",
                "process_guid": "WNEXFKQ7-00050603-0000025c-00000000-1d6c86e280d8ba9",
                "process_hash": [
                    "fd9aad3ea144d4c893eb0ccbff394a83",
                    "d6df7bbd93e84f5e9aec4f2d36fb04b8168e62010eae617f386c10c73b9136e6"
                ],
                "process_name": "c:\\windows\\system32\\winlogon.exe",
                "process_pid": [
                    604
                ],
                "process_reputation": "ADAPTIVE_WHITE_LIST",
                "process_start_time": "2020-12-02T05:44:09.794Z",
                "process_username": [
                    "NT AUTHORITY\\SYSTEM"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            }
        ],
        "parent": {},
        "children": []
    },
    "contacted": 34,
    "completed": 34
}

GET_PROCESS_SUMMARY_RESP_2 = {
    "exception": "NODE_LIMIT_HIT",
    "summary": {
        "process": {
            "_process_filename": "svchost.exe",
            "backend_timestamp": "2020-12-03T20:34:38.889Z",
            "childproc_count": 3,
            "crossproc_count": 40,
            "device_external_ip": "24.243.76.124",
            "device_group_id": 0,
            "device_id": 329219,
            "device_internal_ip": "172.16.115.191",
            "device_name": "desktop-8qonquj",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 2198,
            "device_timestamp": "2020-12-03T20:32:20.912Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": False,
            "ingress_time": 1607027652665,
            "modload_count": 101,
            "netconn_count": 0,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-00050603-00000270-00000000-1d6c86e280fbff8",
            "parent_hash": [
                "1b6ffe1f5480675fc618b42247ef49a1c60ca99d2d53271b3472557e3bea2e8a",
                "2bd115a27b60b74bbeb31013519ac199"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 624,
            "process_cmdline": [
                "C:\\Windows\\System32\\svchost.exe -k LocalServiceNetworkRestricted -p -s wscsvc"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "WNEXFKQ7-00050603-00000b6c-00000000-1d6c86e29731218",
            "process_hash": [
                "9520a99e77d6196d0d09833146424113",
                "dd191a5b23df92e12a8852291f9fb5ed594b76a28a5a464418442584afd1e048"
            ],
            "process_name": "c:\\windows\\system32\\svchost.exe",
            "process_pid": [
                2924
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-12-02T05:44:12.137Z",
            "process_username": [
                "NT AUTHORITY\\LOCAL SERVICE"
            ],
            "regmod_count": 5,
            "scriptload_count": 0
        },
        "siblings": [
            {
                "_process_filename": "spoolsv.exe",
                "backend_timestamp": "2020-12-03T20:34:38.889Z",
                "childproc_count": 2,
                "crossproc_count": 35,
                "device_external_ip": "24.243.76.124",
                "device_group_id": 0,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-03T20:32:18.693Z",
                "filemod_count": 405,
                "has_children": True,
                "hits": False,
                "ingress_time": 1607027652665,
                "modload_count": 382,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-00000270-00000000-1d6c86e280fbff8",
                "parent_hash": [
                    "1b6ffe1f5480675fc618b42247ef49a1c60ca99d2d53271b3472557e3bea2e8a",
                    "2bd115a27b60b74bbeb31013519ac199"
                ],
                "parent_name": "c:\\windows\\system32\\services.exe",
                "parent_pid": 624,
                "process_cmdline": [
                    "C:\\Windows\\System32\\spoolsv.exe"
                ],
                "process_effective_reputation": "LOCAL_WHITE",
                "process_guid": "WNEXFKQ7-00050603-00000944-00000000-1d6c86e29169d10",
                "process_hash": [
                    "94170797d822cd195f8f92da9def082f",
                    "f45ca80e151494a7394dcd1958ee94c0b83fe3f7b9e281fa1e626e71ff6c2604"
                ],
                "process_name": "c:\\windows\\system32\\spoolsv.exe",
                "process_pid": [
                    2372
                ],
                "process_reputation": "COMMON_WHITE_LIST",
                "process_start_time": "2020-12-02T05:44:11.531Z",
                "process_username": [
                    "NT AUTHORITY\\SYSTEM"
                ],
                "regmod_count": 445,
                "scriptload_count": 0
            },
            {
                "_process_filename": "wmiapsrv.exe",
                "backend_timestamp": "2020-12-02T06:00:54.384Z",
                "childproc_count": 0,
                "crossproc_count": 3,
                "device_external_ip": "24.243.76.124",
                "device_group": "schumaker-test",
                "device_group_id": 1706,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-02T05:46:50.369Z",
                "filemod_count": 0,
                "has_children": False,
                "ingress_time": 1606888837162,
                "modload_count": 21,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-00000270-00000000-1d6c86e280fbff8",
                "parent_hash": [
                    "1b6ffe1f5480675fc618b42247ef49a1c60ca99d2d53271b3472557e3bea2e8a",
                    "2bd115a27b60b74bbeb31013519ac199"
                ],
                "parent_name": "c:\\windows\\system32\\services.exe",
                "parent_pid": 624,
                "process_cmdline": [
                    "C:\\Windows\\system32\\wbem\\WmiApSrv.exe"
                ],
                "process_effective_reputation": "LOCAL_WHITE",
                "process_guid": "WNEXFKQ7-00050603-000020f8-00000000-1d6c86e87b1e2be",
                "process_hash": [
                    "55e21dfb7ec2394903e5ca62fdca21e6",
                    "55c2021f06d28696843672ff90e242c33c4cf6d30cdf0b2d9dcf07d8282cfc19"
                ],
                "process_name": "c:\\windows\\system32\\wbem\\wmiapsrv.exe",
                "process_pid": [
                    8440
                ],
                "process_reputation": "ADAPTIVE_WHITE_LIST",
                "process_start_time": "2020-12-02T05:46:50.254Z",
                "process_terminated": True,
                "process_username": [
                    "NT AUTHORITY\\SYSTEM"
                ],
                "regmod_count": 1,
                "scriptload_count": 0
            }
        ],
        "parent": {
            "_process_filename": "services.exe",
            "backend_timestamp": "2020-12-03T20:34:38.889Z",
            "childproc_count": 243,
            "crossproc_count": 39,
            "device_external_ip": "24.243.76.124",
            "device_group_id": 0,
            "device_id": 329219,
            "device_internal_ip": "172.16.115.191",
            "device_name": "desktop-8qonquj",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 2198,
            "device_timestamp": "2020-12-03T20:32:13.397Z",
            "filemod_count": 0,
            "has_children": True,
            "hits": False,
            "ingress_time": 1607027652665,
            "modload_count": 53,
            "netconn_count": 0,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-00050603-000001fc-00000000-1d6c86e2801246d",
            "parent_hash": [
                "d5e122606054fa0b03db3ee8cf9ea7701e523875e2bdb87581ad7232ffc9308e",
                "e83650f70459a027aa596e1a73c961a1"
            ],
            "parent_name": "c:\\windows\\system32\\wininit.exe",
            "parent_pid": 508,
            "process_cmdline": [
                "C:\\Windows\\system32\\services.exe"
            ],
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "WNEXFKQ7-00050603-00000270-00000000-1d6c86e280fbff8",
            "process_hash": [
                "2bd115a27b60b74bbeb31013519ac199",
                "1b6ffe1f5480675fc618b42247ef49a1c60ca99d2d53271b3472557e3bea2e8a"
            ],
            "process_name": "c:\\windows\\system32\\services.exe",
            "process_pid": [
                624
            ],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_start_time": "2020-12-02T05:44:09.808Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 254,
            "scriptload_count": 0
        },
        "children": [
            {
                "_process_filename": "mpcmdrun.exe",
                "backend_timestamp": "2020-12-03T20:33:19.002Z",
                "childproc_count": 1,
                "crossproc_count": 5,
                "device_external_ip": "24.243.76.124",
                "device_group_id": 0,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-03T20:31:13.097Z",
                "filemod_count": 1,
                "has_children": True,
                "hits": False,
                "ingress_time": 1607027590489,
                "modload_count": 18,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-00000b6c-00000000-1d6c86e29731218",
                "parent_hash": [
                    "9520a99e77d6196d0d09833146424113",
                    "dd191a5b23df92e12a8852291f9fb5ed594b76a28a5a464418442584afd1e048"
                ],
                "parent_name": "c:\\windows\\system32\\svchost.exe",
                "parent_pid": 2924,
                "process_cmdline": [
                    "\"C:\\Program Files\\Windows Defender\\mpcmdrun.exe\" -wddisable"
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "WNEXFKQ7-00050603-0000157c-00000000-1d6c9b339b4a0cd",
                "process_hash": [
                    "cc4f6cbde75f08afdcefb95087149a5d",
                    "885557be148de55f6a127ea26ac457b9415e3e3baf30266d82b9d19b89e78ee4"
                ],
                "process_name": "c:\\program files\\windows defender\\mpcmdrun.exe",
                "process_pid": [
                    5500
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-12-03T20:31:05.847Z",
                "process_terminated": True,
                "process_username": [
                    "NT AUTHORITY\\LOCAL SERVICE"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            },
            {
                "_process_filename": "mpcmdrun.exe",
                "backend_timestamp": "2020-12-02T05:59:53.548Z",
                "childproc_count": 1,
                "crossproc_count": 4,
                "device_external_ip": "24.243.76.124",
                "device_group": "schumaker-test",
                "device_group_id": 1706,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-02T05:45:15.950Z",
                "filemod_count": 1,
                "has_children": True,
                "hits": False,
                "ingress_time": 1606888776302,
                "modload_count": 16,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-00000b6c-00000000-1d6c86e29731218",
                "parent_hash": [
                    "9520a99e77d6196d0d09833146424113",
                    "dd191a5b23df92e12a8852291f9fb5ed594b76a28a5a464418442584afd1e048"
                ],
                "parent_name": "c:\\windows\\system32\\svchost.exe",
                "parent_pid": 2924,
                "process_cmdline": [
                    "\"C:\\Program Files\\Windows Defender\\mpcmdrun.exe\" -wdenable"
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "WNEXFKQ7-00050603-00001d78-00000000-1d6c86e4f3c4a8f",
                "process_hash": [
                    "cc4f6cbde75f08afdcefb95087149a5d",
                    "885557be148de55f6a127ea26ac457b9415e3e3baf30266d82b9d19b89e78ee4"
                ],
                "process_name": "c:\\program files\\windows defender\\mpcmdrun.exe",
                "process_pid": [
                    7544
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-12-02T05:45:15.531Z",
                "process_terminated": True,
                "process_username": [
                    "NT AUTHORITY\\LOCAL SERVICE"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            },
            {
                "_process_filename": "mpcmdrun.exe",
                "backend_timestamp": "2020-12-02T05:58:52.326Z",
                "childproc_count": 1,
                "crossproc_count": 6,
                "device_external_ip": "24.243.76.124",
                "device_group": "schumaker-test",
                "device_group_id": 1706,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-02T05:44:48.561Z",
                "filemod_count": 1,
                "has_children": True,
                "hits": False,
                "ingress_time": 1606888714925,
                "modload_count": 18,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-00000b6c-00000000-1d6c86e29731218",
                "parent_hash": [
                    "9520a99e77d6196d0d09833146424113",
                    "dd191a5b23df92e12a8852291f9fb5ed594b76a28a5a464418442584afd1e048"
                ],
                "parent_name": "c:\\windows\\system32\\svchost.exe",
                "parent_pid": 2924,
                "process_cmdline": [
                    "\"C:\\Program Files\\Windows Defender\\mpcmdrun.exe\" -wddisable"
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "WNEXFKQ7-00050603-00001370-00000000-1d6c86e34d57249",
                "process_hash": [
                    "cc4f6cbde75f08afdcefb95087149a5d",
                    "885557be148de55f6a127ea26ac457b9415e3e3baf30266d82b9d19b89e78ee4"
                ],
                "process_name": "c:\\program files\\windows defender\\mpcmdrun.exe",
                "process_pid": [
                    4976
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-12-02T05:44:31.236Z",
                "process_terminated": True,
                "process_username": [
                    "NT AUTHORITY\\LOCAL SERVICE"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            }
        ]
    },
    "contacted": 34,
    "completed": 34
}

GET_TREE_RESP = {
    "exception": "",
    "summary": {
        "process": None,
        "siblings": None,
        "parent": None,
        "children": None
    },
    "tree": {
        "_process_filename": "ngen.exe",
        "backend_timestamp": "2020-12-03T19:47:23.199Z",
        "childproc_count": 1,
        "children": [
            {
                "_process_filename": "mscorsvw.exe",
                "backend_timestamp": "2020-12-03T19:47:23.199Z",
                "childproc_count": 0,
                "children": [],
                "crossproc_count": 3,
                "device_external_ip": "24.243.76.124",
                "device_group_id": 0,
                "device_id": 329219,
                "device_internal_ip": "172.16.115.191",
                "device_name": "desktop-8qonquj",
                "device_os": "WINDOWS",
                "device_policy": "default",
                "device_policy_id": 2198,
                "device_timestamp": "2020-12-03T19:44:25.004Z",
                "filemod_count": 0,
                "has_children": False,
                "ingress_time": 1607024805760,
                "modload_count": 14,
                "netconn_count": 0,
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-00050603-000008a0-00000000-1d6c9acb438f08d",
                "parent_hash": [
                    "0eb067650f90e1af3b660c229a58d5e4c505a928847349e06dadb5e88df713f4",
                    "660254c8228b83705c80374d47f570f1"
                ],
                "parent_name": "c:\\windows\\microsoft.net\\framework64\\v4.0.30319\\ngen.exe",
                "parent_pid": 2208,
                "process_cmdline": [
                    "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\mscorsvw.exe -StartupEvent 1b4 -InterruptEvent 0 -NGENProcess 168 -Pipe 174 -Comment \"NGen Worker Process\""
                ],
                "process_effective_reputation": "TRUSTED_WHITE_LIST",
                "process_guid": "WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb",
                "process_hash": [
                    "a0b98e5e57de8f666a04ac3eec86d25b",
                    "60def9905f16bd5d10684afea17ab3a9accdd8ba4a6e06240e84e3acb5f94e3d"
                ],
                "process_name": "c:\\windows\\microsoft.net\\framework64\\v4.0.30319\\mscorsvw.exe",
                "process_pid": [
                    1644
                ],
                "process_reputation": "TRUSTED_WHITE_LIST",
                "process_start_time": "2020-12-03T19:44:24.953Z",
                "process_terminated": True,
                "process_username": [
                    "NT AUTHORITY\\SYSTEM"
                ],
                "regmod_count": 0,
                "scriptload_count": 0
            }
        ],
        "crossproc_count": 4,
        "device_external_ip": "24.243.76.124",
        "device_group_id": 0,
        "device_id": 329219,
        "device_internal_ip": "172.16.115.191",
        "device_name": "desktop-8qonquj",
        "device_os": "WINDOWS",
        "device_policy": "default",
        "device_policy_id": 2198,
        "device_timestamp": "2020-12-03T19:44:25.020Z",
        "filemod_count": 5,
        "has_children": True,
        "hits": False,
        "ingress_time": 1607024805760,
        "modload_count": 11,
        "netconn_count": 0,
        "org_id": "WNEXFKQ7",
        "parent_guid": "WNEXFKQ7-00050603-000023fc-00000000-1d6c9acae2c7003",
        "parent_hash": [
            "6e4b6d2af6d99dcc1de0e097ea51d43a",
            "c4db063d8de31c0a64d172950f857509ee97baa488d8678d48eb6e75b17527b0"
        ],
        "parent_name": "c:\\windows\\microsoft.net\\framework64\\v4.0.30319\\ngentask.exe",
        "parent_pid": 9212,
        "process_cmdline": [
            "\"C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\ngen.exe\" install \"System.Core, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089\" /NoDependencies /noroot /version:v4.0.30319 /LegacyServiceBehavior"
        ],
        "process_effective_reputation": "TRUSTED_WHITE_LIST",
        "process_guid": "WNEXFKQ7-00050603-000008a0-00000000-1d6c9acb438f08d",
        "process_hash": [
            "660254c8228b83705c80374d47f570f1",
            "0eb067650f90e1af3b660c229a58d5e4c505a928847349e06dadb5e88df713f4"
        ],
        "process_name": "c:\\windows\\microsoft.net\\framework64\\v4.0.30319\\ngen.exe",
        "process_pid": [
            2208
        ],
        "process_reputation": "TRUSTED_WHITE_LIST",
        "process_start_time": "2020-12-03T19:44:24.919Z",
        "process_terminated": True,
        "process_username": [
            "NT AUTHORITY\\SYSTEM"
        ],
        "regmod_count": 0,
        "scriptload_count": 0
    },
    "contacted": 34,
    "completed": 34
}

GET_SUMMARY_NOT_FOUND = {
    "message": "Resource does not exist",
    "translation_key": "threathunter_resource_does_not_exist",
    "translation_format_values": None
}

GET_FACET_SEARCH_RESULTS_RESP = {
    "ranges": [
        {
            "start": "2020-10-20T00:00:00Z",
            "end": "2020-11-12T00:00:00Z",
            "bucket_size": "+1DAY",
            "field": "backend_timestamp",
            "values": [
                {
                    "total": 1555,
                    "name": "2020-10-20T00:00:00Z"
                },
                {
                    "total": 1970,
                    "name": "2020-10-21T00:00:00Z"
                },
                {
                    "total": 7727,
                    "name": "2020-10-22T00:00:00Z"
                },
                {
                    "total": 2453,
                    "name": "2020-10-23T00:00:00Z"
                },
                {
                    "total": 37,
                    "name": "2020-11-11T00:00:00Z"
                }
            ]
        }
    ],
    "terms": [
        {
            "values": [
                {
                    "total": 797,
                    "id": "2020-10-22T20:56:31.215Z",
                    "name": "2020-10-22T20:56:31.215Z"
                },
                {
                    "total": 708,
                    "id": "2020-10-19T22:35:43.547Z",
                    "name": "2020-10-19T22:35:43.547Z"
                },
                {
                    "total": 518,
                    "id": "2020-10-09T14:17:55.189Z",
                    "name": "2020-10-09T14:17:55.189Z"
                },
                {
                    "total": 83,
                    "id": "2020-11-12T01:40:04.682Z",
                    "name": "2020-11-12T01:40:04.682Z"
                },
                {
                    "total": 26,
                    "id": "2020-07-30T14:15:50.415Z",
                    "name": "2020-07-30T14:15:50.415Z"
                },
                {
                    "total": 9,
                    "id": "2020-10-20T18:09:58.469Z",
                    "name": "2020-10-20T18:09:58.469Z"
                },
                {
                    "total": 9,
                    "id": "2020-10-23T05:48:32.744Z",
                    "name": "2020-10-23T05:48:32.744Z"
                },
                {
                    "total": 8,
                    "id": "2020-08-24T18:46:30.369Z",
                    "name": "2020-08-24T18:46:30.369Z"
                },
                {
                    "total": 7,
                    "id": "2020-09-23T15:03:29.263Z",
                    "name": "2020-09-23T15:03:29.263Z"
                }
            ],
            "field": "backend_timestamp"
        },
        {
            "values": [
                {
                    "total": 38,
                    "id": "2020-10-19T21:25:06.668Z",
                    "name": "2020-10-19T21:25:06.668Z"
                },
                {
                    "total": 13,
                    "id": "2020-10-22T20:48:22.188Z",
                    "name": "2020-10-22T20:48:22.188Z"
                },
                {
                    "total": 5,
                    "id": "2020-07-30T14:12:47.986Z",
                    "name": "2020-07-30T14:12:47.986Z"
                },
                {
                    "total": 4,
                    "id": "2020-11-12T01:38:10.788Z",
                    "name": "2020-11-12T01:38:10.788Z"
                },
                {
                    "total": 2,
                    "id": "2020-07-30T14:10:41.125Z",
                    "name": "2020-07-30T14:10:41.125Z"
                },
                {
                    "total": 2,
                    "id": "2020-09-23T15:05:23.758Z",
                    "name": "2020-09-23T15:05:23.758Z"
                },
                {
                    "total": 2,
                    "id": "2020-10-20T15:53:30.260Z",
                    "name": "2020-10-20T15:53:30.260Z"
                },
                {
                    "total": 1,
                    "id": "2020-10-23T05:36:34.300Z",
                    "name": "2020-10-23T05:36:34.300Z"
                },
                {
                    "total": 1,
                    "id": "2020-08-24T17:32:31.211Z",
                    "name": "2020-08-24T17:32:31.211Z"
                }
            ],
            "field": "device_timestamp"
        }
    ],
    "num_found": 23753,
    "contacted": 36,
    "completed": 36
}

EXPECTED_PROCESS_FACETS = {
    "backend_timestamp": [
        {
            "total": 797,
            "id": "2020-10-22T20:56:31.215Z",
            "name": "2020-10-22T20:56:31.215Z"
        },
        {
            "total": 708,
            "id": "2020-10-19T22:35:43.547Z",
            "name": "2020-10-19T22:35:43.547Z"
        },
        {
            "total": 518,
            "id": "2020-10-09T14:17:55.189Z",
            "name": "2020-10-09T14:17:55.189Z"
        },
        {
            "total": 83,
            "id": "2020-11-12T01:40:04.682Z",
            "name": "2020-11-12T01:40:04.682Z"
        },
        {
            "total": 26,
            "id": "2020-07-30T14:15:50.415Z",
            "name": "2020-07-30T14:15:50.415Z"
        },
        {
            "total": 9,
            "id": "2020-10-20T18:09:58.469Z",
            "name": "2020-10-20T18:09:58.469Z"
        },
        {
            "total": 9,
            "id": "2020-10-23T05:48:32.744Z",
            "name": "2020-10-23T05:48:32.744Z"
        },
        {
            "total": 8,
            "id": "2020-08-24T18:46:30.369Z",
            "name": "2020-08-24T18:46:30.369Z"
        },
        {
            "total": 7,
            "id": "2020-09-23T15:03:29.263Z",
            "name": "2020-09-23T15:03:29.263Z"
        }
    ],
    "device_timestamp": [
        {
            "total": 38,
            "id": "2020-10-19T21:25:06.668Z",
            "name": "2020-10-19T21:25:06.668Z"
        },
        {
            "total": 13,
            "id": "2020-10-22T20:48:22.188Z",
            "name": "2020-10-22T20:48:22.188Z"
        },
        {
            "total": 5,
            "id": "2020-07-30T14:12:47.986Z",
            "name": "2020-07-30T14:12:47.986Z"
        },
        {
            "total": 4,
            "id": "2020-11-12T01:38:10.788Z",
            "name": "2020-11-12T01:38:10.788Z"
        },
        {
            "total": 2,
            "id": "2020-07-30T14:10:41.125Z",
            "name": "2020-07-30T14:10:41.125Z"
        },
        {
            "total": 2,
            "id": "2020-09-23T15:05:23.758Z",
            "name": "2020-09-23T15:05:23.758Z"
        },
        {
            "total": 2,
            "id": "2020-10-20T15:53:30.260Z",
            "name": "2020-10-20T15:53:30.260Z"
        },
        {
            "total": 1,
            "id": "2020-10-23T05:36:34.300Z",
            "name": "2020-10-23T05:36:34.300Z"
        },
        {
            "total": 1,
            "id": "2020-08-24T17:32:31.211Z",
            "name": "2020-08-24T17:32:31.211Z"
        }
    ]
}

EXPECTED_PROCESS_RANGES_FACETS = {
    "backend_timestamp": [
        {
            "total": 1555,
            "name": "2020-10-20T00:00:00Z"
        },
        {
            "total": 1970,
            "name": "2020-10-21T00:00:00Z"
        },
        {
            "total": 7727,
            "name": "2020-10-22T00:00:00Z"
        },
        {
            "total": 2453,
            "name": "2020-10-23T00:00:00Z"
        },
        {
            "total": 37,
            "name": "2020-11-11T00:00:00Z"
        }
    ]
}

GET_FACET_SEARCH_RESULTS_RESP_1 = {
    "ranges": [
        {
            "start": "2020-10-20T00:00:00Z",
            "end": "2020-11-12T00:00:00Z",
            "bucket_size": "+1DAY",
            "field": "backend_timestamp",
            "values": [
                {
                    "total": 1555,
                    "name": "2020-10-20T00:00:00Z"
                }
            ]
        }
    ],
    "terms": [
        {
            "values": [
                {
                    "total": 797,
                    "id": "2020-10-22T20:56:31.215Z",
                    "name": "2020-10-22T20:56:31.215Z"
                }
            ],
            "field": "backend_timestamp"
        }
    ],
    "num_found": 0,
    "contacted": 0,
    "completed": 0
}

GET_FACET_SEARCH_RESULTS_RESP_NOT_COMPLETE = {
    "ranges": [
        {
            "start": "2020-10-20T00:00:00Z",
            "end": "2020-11-12T00:00:00Z",
            "bucket_size": "+1DAY",
            "field": "backend_timestamp",
            "values": [
                {
                    "total": 1555,
                    "name": "2020-10-20T00:00:00Z"
                }
            ]
        }
    ],
    "terms": [
        {
            "values": [
                {
                    "total": 797,
                    "id": "2020-10-22T20:56:31.215Z",
                    "name": "2020-10-22T20:56:31.215Z"
                }
            ],
            "field": "backend_timestamp"
        }
    ],
    "num_found": 0,
    "contacted": 10,
    "completed": 2
}
