"""Mock responses for enriched event queries."""

POST_ENRICHED_EVENTS_SEARCH_JOB_RESP = {
    "job_id": "08ffa932-b633-4107-ba56-8741e929e48b"
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP = {
    "contacted": 41,
    "completed": 41,
    "num_found": 808,
    "num_available": 1,
    "results": [{
        "backend_timestamp": "2020-10-23T08:25:24.797Z",
        "device_group_id": 0,
        "device_id": 215209,
        "device_name": "scarpaci-win10-eap01",
        "device_policy_id": 2203,
        "device_timestamp": "2020-10-23T08:24:22.624Z",
        "enriched": True,
        "enriched_event_type": "SYSTEM_API_CALL",
        "event_description": 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open itself for modification, by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
        "event_id": "27a278d5150911eb86f1011a55e73b72",
        "event_type": "crossproc",
        "ingress_time": 1603441488750,
        "legacy": True,
        "org_id": "WNEXFKQ7",
        "parent_guid": "WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd",
        "parent_pid": 884,
        "process_guid": "WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86",
        "process_hash": [
            "47a61bee31164ea1dd671d695424722e",
            "6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786",
        ],
        "process_name": "c:\\windows\\system32\\wbem\\scrcons.exe",
        "process_pid": [1000],
        "process_username": ["NT AUTHORITY\\SYSTEM"],
    }]
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_0 = {
    "contacted": 0,
    "completed": 0,
    "results": []
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP = {
    "contacted": 10,
    "completed": 0,
    "results": []
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_ZERO = {
    "num_found": 0,
    "num_available": 0,
    "contacted": 10,
    "completed": 10,
    "results": []
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2 = {
    "num_found": 808,
    "num_available": 52,
    "contacted": 6,
    "completed": 6,
    "results": [
        {
            "backend_timestamp": "2020-10-23T08:25:24.797Z",
            "device_group_id": 0,
            "device_id": 215209,
            "device_name": "scarpaci-win10-eap01",
            "device_policy_id": 2203,
            "device_timestamp": "2020-10-23T08:24:22.624Z",
            "enriched": True,
            "enriched_event_type": "SYSTEM_API_CALL",
            "event_description": 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open itself for modification, by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
            "event_id": "27a278d5150911eb86f1011a55e73b72",
            "event_type": "crossproc",
            "ingress_time": 1603441488750,
            "legacy": True,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd",
            "parent_pid": 884,
            "process_guid": "WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86",
            "process_hash": [
                "47a61bee31164ea1dd671d695424722e",
                "6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786",
            ],
            "process_name": "c:\\windows\\system32\\wbem\\scrcons.exe",
            "process_pid": [1000],
            "process_username": ["NT AUTHORITY\\SYSTEM"],
        },
        {
            "backend_timestamp": "2020-10-23T08:25:24.797Z",
            "device_group_id": 0,
            "device_id": 215209,
            "device_name": "scarpaci-win10-eap01",
            "device_policy_id": 2203,
            "device_timestamp": "2020-10-23T08:24:22.271Z",
            "enriched": True,
            "enriched_event_type": "SYSTEM_API_CALL",
            "event_description": 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open the process "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18.2009.7-0\\MsMpEng.exe", by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
            "event_id": "27a278d2150911eb86f1011a55e73b72",
            "event_type": "crossproc",
            "ingress_time": 1603441488750,
            "legacy": True,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd",
            "parent_pid": 884,
            "process_guid": "WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86",
            "process_hash": [
                "47a61bee31164ea1dd671d695424722e",
                "6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786",
            ],
            "process_name": "c:\\windows\\system32\\wbem\\scrcons.exe",
            "process_pid": [2000],
            "process_username": ["NT AUTHORITY\\SYSTEM"],
        },
    ],
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING = {
    "num_found": 808,
    "num_available": 1,
    "contacted": 6,
    "completed": 0,
    "results": [],
}

GET_ENRICHED_EVENTS_AGG_JOB_RESULTS_RESP_1 = {
    "results": [
        {
            "alert_id": ["null/99FI049P"],
            "backend_timestamp": "2020-06-25T21:05:10.787Z",
            "device_id": 195940,
            "device_name": "desktop-8qonquj",
            "device_os": "WINDOWS",
            "device_policy": "default",
            "device_policy_id": 2198,
            "device_timestamp": "2020-06-25T20:36:06.608Z",
            "enriched": True,
            "enriched_event_type": "CREATE_PROCESS",
            "event_description": "test",
            "event_id": "8ff185c2b72311eaab6d9f3b90c54099",
            "event_type": "childproc",
            "ingress_time": 1593117428851,
            "legacy": True,
            "num_devices": 1,
            "num_events": 2,
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-0002fd64-00001ffc-00000000-1d64b3039bb7130",
            "parent_pid": 8188,
            "process_effective_reputation": "LOCAL_WHITE",
            "process_guid": "WNEXFKQ7-0002fd64-000007d0-00000000-1d64b30404d93d8",
            "process_hash": [
                "0dde659f0854d78f137119e13e1368ef",
                "de74b04a291133b8c6c5a30bff6b2cef8ad4141cd1813d063c8c62f2671652e8",
            ],
            "process_name": "c:\\users\\dragon\\.rustup\\toolchains\\stable-x86_64-pc-windows-msvc\\bin\\rustc.exe",
            "process_pid": [2000],
            "process_sha256": "de74b04a291133b8c6c5a30bff6b2cef8ad4141cd1813d063c8c62f2671652e8",
            "process_username": ["DESKTOP-8QONQUJ\\dragon"],
        }
    ],
    "num_found": 1,
    "num_available": 1,
    "contacted": 32,
    "completed": 32,
}


GET_ENRICHED_EVENTS_DETAIL_JOB_RESULTS_RESP = {
    "results": [
        {
            "alert_id": ["null/99FI049P"],
            "backend_timestamp": "2020-10-09T14:17:24.704Z",
            "childproc_cmdline": '"c:\\Windows\\System32\\cmd.exe"',
            "childproc_cmdline_length": 4877,
            "childproc_effective_reputation": "TRUSTED_WHITE_LIST",
            "childproc_guid": "WNEXFKQ7-0002fd64-00001bec-00000000-1d64b304076f88d",
            "childproc_hash": [
                "ff79d3c4a0b7eb191783c323ab8363ebd1fd10be58d8bcc96b07067743ca81d5"
            ],
            "childproc_name": "c:\\windows\\system32\\cmd.exe",
            "childproc_pid": 7148,
            "childproc_reputation": "COMMON_WHITE_LIST",
            "device_id": 195940,
            "device_installed_by": "user@vmware.com",
            "device_internal_ip": "111.222.111.222",
            "device_location": "OFFSITE",
            "device_name": "desktop",
            "device_os": "WINDOWS",
            "device_os_version": "Windows 10 x64",
            "device_policy": "default",
            "device_policy_id": 2198,
            "device_target_priority": "MEDIUM",
            "device_timestamp": "2020-06-25T20:36:06.608Z",
            "document_guid": "udUDvAqqSIib030hecSTrw",
            "enriched": True,
            "enriched_event_type": "CREATE_PROCESS",
            "event_description": "test",
            "event_id": "8ff185c2b72311eaab6d9f3b90c54099",
            "event_type": "childproc",
            "ingress_time": 1602253036356,
            "legacy": True,
            "org_id": "test",
            "parent_effective_reputation": "LOCAL_WHITE",
            "parent_guid": "WNEXFKQ7-0002fd64-00001ffc-00000000-1d64b3039bb7130",
            "parent_hash": [
                "574fefcfd4f2f9de53a63cbc791698f93637e709b0631478ac2c40f43f9a08cb"
            ],
            "parent_name": "cargo.exe",
            "parent_pid": 8188,
            "parent_publisher_state": ["FILE_SIGNATURE_STATE_NOT_SIGNED"],
            "parent_reputation": "ADAPTIVE_WHITE_LIST",
            "process_cmdline": ['"rustc.exe"'],
            "process_cmdline_length": [796],
            "process_effective_reputation": "LOCAL_WHITE",
            "process_guid": "WNEXFKQ7-0002fd64-000007d0-00000000-1d64b30404d93d8",
            "process_hash": ["0dde659f0854d78f137119e13e1368ef"],
            "process_name": "rustc.exe",
            "process_pid": [2000],
            "process_publisher_state": ["FILE_SIGNATURE_STATE_NOT_SIGNED"],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_sha256": "de74b04a291133b8c6c5a30bff6b2cef8ad4141cd1813d063c8c62f2671652e8",
            "process_start_time": "2020-06-25T20:36:06.334Z",
            "process_username": ["DESKTOP-8QONQUJ\\dragon"],
            "ttp": ["ADAPTIVE_WHITE_APP"],
        }
    ],
    "num_found": 1,
    "num_available": 1,
    "contacted": 32,
    "completed": 32,
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_ALERTS = {
    "approximate_unaggregated": 2,
    "completed": 7,
    "contacted": 7,
    "num_aggregated": 2,
    "num_available": 2,
    "num_found": 2,
    "results": [
        {
            "alert_category": ["OBSERVED"],
            "alert_id": ["62802DCE"],
            "backend_timestamp": "2021-05-13T00:21:13.086Z",
            "device_external_ip": "66.170.99.2",
            "device_group_id": 0,
            "device_id": 8612331,
            "device_installed_by": "Administrator",
            "device_internal_ip": "10.169.255.100",
            "device_location": "OFFSITE",
            "device_name": "win-2016-devrel",
            "device_os": "WINDOWS",
            "device_os_version": "Windows Server 2019 x64",
            "device_policy": "standard",
            "device_policy_id": 7113786,
            "device_target_priority": "MEDIUM",
            "device_timestamp": "2021-05-13T00:20:13.044Z",
            "document_guid": "VNs_NgMIQ-u3_06Sa4Sclg",
            "enriched": True,
            "enriched_event_type": "NETWORK",
            "event_attack_stage": ["RECONNAISSANCE"],
            "event_description": 'The application "<share><link '
            'hash="7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6"'
            '-k RPCSS -p</link></share>" accepted a '
            "<accent>TCP/135</accent> connection from "
            "<share><accent>10.169.255.100</accent></share><accent>:38240</accent> "
            "to "
            "<share><accent>10.126.6.201</accent></share><accent>:135</accent>. "
            "The device was off the corporate network "
            "using the public address "
            "<accent>66.170.99.2</accent> "
            "(<accent>win-2016-devrel</accent>, located "
            "in San Jose CA, United States). The "
            "operation was successful.",
            "event_id": "0980efd1b38111eba4bfa5e98aa30b19",
            "event_network_inbound": True,
            "event_network_local_ipv4": "10.126.6.201",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "10.169.255.100",
            "event_network_remote_port": 38240,
            "event_report_code": "SUB_RPT_NONE",
            "event_threat_score": [1],
            "event_type": "netconn",
            "ingress_time": 1620865258371,
            "legacy": True,
            "netconn_inbound": True,
            "netconn_ipv4": 178913124,
            "netconn_local_ipv4": 176031433,
            "netconn_local_port": 135,
            "netconn_port": 135,
            "netconn_protocol": "PROTO_TCP",
            "org_id": "4JDT3MX9Q",
            "parent_effective_reputation": "LOCAL_WHITE",
            "parent_effective_reputation_source": "CERT",
            "parent_guid": "4JDT3MX9Q-008369eb-00000268-00000000-1d6f5ba1abcf6fc",
            "parent_hash": [
                "e8ea65fb51db75b1cb93890bee4364fc0b804f8f68e1817887e4a7f767ceb9ab"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 616,
            "parent_reputation": "NOT_LISTED",
            "process_cmdline": ["C:\\Windows\\system32\\svchost.exe -k RPCSS " "-p"],
            "process_cmdline_length": [43],
            "process_effective_reputation": "LOCAL_WHITE",
            "process_effective_reputation_source": "CERT",
            "process_guid": "4JDT3MX9Q-008369eb-00000364-00000000-1d6f5ba1b173ce9",
            "process_hash": [
                "8a0a29438052faed8a2532da50455756",
                "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            ],
            "process_name": "c:\\windows\\system32\\svchost.exe",
            "process_pid": [868],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "process_start_time": "2021-01-28T13:12:17.823Z",
            "process_username": ["NT AUTHORITY\\NETWORK SERVICE"],
            "ttp": [
                "PORTSCAN",
                "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                "NETWORK_ACCESS",
                "ACTIVE_SERVER",
            ],
        },
        {
            "alert_category": ["OBSERVED"],
            "alert_id": ["62802DCE"],
            "backend_timestamp": "2021-05-13T00:21:08.028Z",
            "device_external_ip": "66.170.99.2",
            "device_group_id": 0,
            "device_id": 8612331,
            "device_installed_by": "Administrator",
            "device_internal_ip": "10.169.255.100",
            "device_location": "OFFSITE",
            "device_name": "win-2016-devrel",
            "device_os": "WINDOWS",
            "device_os_version": "Windows Server 2019 x64",
            "device_policy": "standard",
            "device_policy_id": 7113786,
            "device_target_priority": "MEDIUM",
            "device_timestamp": "2021-05-13T00:20:13.043Z",
            "document_guid": "WwZPWPLITqSNpAmQKagBYw",
            "enriched": True,
            "enriched_event_type": "NETWORK",
            "event_attack_stage": ["RECONNAISSANCE"],
            "event_description": 'The application "<share><link '
            'hash="7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6"'
            '-k termsvcs -s TermService</link></share>" '
            "accepted a <accent>TCP/3389</accent> "
            "connection from "
            "<share><accent>10.169.255.100</accent></share><accent>:38604</accent> "
            "to "
            "<share><accent>10.126.6.201</accent></share><accent>:3389</accent>. "
            "The device was off the corporate network "
            "using the public address "
            "<accent>66.170.99.2</accent> "
            "(<accent>win-2016-devrel</accent>, located "
            "in San Jose CA, United States). The "
            "operation was successful.",
            "event_id": "0980efd0b38111eba4bfa5e98aa30b19",
            "event_network_inbound": True,
            "event_network_local_ipv4": "10.126.6.201",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "10.169.255.100",
            "event_network_remote_port": 38604,
            "event_report_code": "SUB_RPT_NONE",
            "event_threat_score": [1],
            "event_type": "netconn",
            "ingress_time": 1620865258370,
            "legacy": True,
            "netconn_inbound": True,
            "netconn_ipv4": 178913124,
            "netconn_local_ipv4": 176031433,
            "netconn_local_port": 3389,
            "netconn_port": 3389,
            "netconn_protocol": "PROTO_TCP",
            "org_id": "4JDT3MX9Q",
            "parent_effective_reputation": "LOCAL_WHITE",
            "parent_effective_reputation_source": "CERT",
            "parent_guid": "4JDT3MX9Q-008369eb-00000268-00000000-1d6f5ba1abcf6fc",
            "parent_hash": [
                "e8ea65fb51db75b1cb93890bee4364fc0b804f8f68e1817887e4a7f767ceb9ab"
            ],
            "parent_name": "c:\\windows\\system32\\services.exe",
            "parent_pid": 616,
            "parent_reputation": "NOT_LISTED",
            "process_cmdline": [
                "C:\\Windows\\System32\\svchost.exe -k " "termsvcs -s TermService"
            ],
            "process_cmdline_length": [58],
            "process_effective_reputation": "LOCAL_WHITE",
            "process_effective_reputation_source": "CERT",
            "process_guid": "4JDT3MX9Q-008369eb-0000016c-00000000-1d6f5ba1b4bd98d",
            "process_hash": [
                "8a0a29438052faed8a2532da50455756",
                "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            ],
            "process_name": "c:\\windows\\system32\\svchost.exe",
            "process_pid": [364],
            "process_reputation": "ADAPTIVE_WHITE_LIST",
            "process_sha256": "7fd065bac18c5278777ae44908101cdfed72d26fa741367f0ad4d02020787ab6",
            "process_start_time": "2021-01-28T13:12:18.168Z",
            "process_username": ["NT AUTHORITY\\NETWORK SERVICE"],
            "ttp": [
                "PORTSCAN",
                "MITRE_T1046_NETWORK_SERVICE_SCANNING",
                "NETWORK_ACCESS",
                "ACTIVE_SERVER",
            ],
        },
    ],
}
