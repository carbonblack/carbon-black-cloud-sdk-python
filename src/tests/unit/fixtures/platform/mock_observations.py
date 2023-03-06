"""Mock responses for observations queries."""

POST_OBSERVATIONS_SEARCH_JOB_RESP = {"job_id": "08ffa932-b633-4107-ba56-8741e929e48b"}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP = {
    "approximate_unaggregated": 1,
    "completed": 4,
    "contacted": 4,
    "num_aggregated": 1,
    "num_available": 1,
    "num_found": 1,
    "results": [
        {
            "alert_category": ["OBSERVED"],
            "alert_id": None,
            "backend_timestamp": "2023-02-08T03:22:59.196Z",
            "device_group_id": 0,
            "device_id": 17482451,
            "device_name": "dev01-39x-1",
            "device_policy_id": 20792247,
            "device_timestamp": "2023-02-08T03:20:33.751Z",
            "enriched": True,
            "enriched_event_type": ["NETWORK"],
            "event_description": "The script",
            "event_id": "8fbccc2da75f11ed937ae3cb089984c6",
            "event_network_inbound": False,
            "event_network_local_ipv4": "10.203.105.21",
            "event_network_location": "Santa Clara,CA,United States",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "23.44.229.234",
            "event_network_remote_port": 80,
            "event_type": ["netconn"],
            "ingress_time": 1675826462036,
            "legacy": True,
            "observation_description": "The application firefox.exe invoked ",
            "observation_id": "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
            "observation_type": "CB_ANALYTICS",
            "org_id": "ABCD123456",
            "parent_guid": "ABCD123456-010ac2d3-00001c68-00000000-1d93b6c4d1f20ad",
            "parent_pid": 7272,
            "process_guid": "ABCD123456-010ac2d3-00001cf8-00000000-1d93b6c4d2b16a4",
            "process_hash": [
                "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dcda7b29"
            ],
            "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38\\updates",
            "process_pid": [2000],
            "process_username": ["DEV01-39X-1\\bit9qa"],
            "tms_rule_id": "8a4b43c5-5e0a-4f7d-aa46-bd729f1989a7",
        }
    ],
}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_0 = {
    "contacted": 0,
    "completed": 0,
    "results": [],
}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP = {
    "contacted": 10,
    "completed": 0,
    "results": [],
}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_ZERO = {
    "num_found": 0,
    "num_available": 0,
    "contacted": 10,
    "completed": 10,
    "results": [],
}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_2 = {
    "num_found": 808,
    "num_available": 52,
    "contacted": 6,
    "completed": 6,
    "results": [
        {
            "alert_category": ["OBSERVED"],
            "alert_id": None,
            "backend_timestamp": "2023-02-08T03:22:59.196Z",
            "device_group_id": 0,
            "device_id": 17482451,
            "device_name": "dev01-39x-1",
            "device_policy_id": 20792247,
            "device_timestamp": "2023-02-08T03:20:33.751Z",
            "enriched": True,
            "enriched_event_type": ["NETWORK"],
            "event_description": "The script",
            "event_id": "8fbccc2da75f11ed937ae3cb089984c6",
            "event_network_inbound": False,
            "event_network_local_ipv4": "10.203.105.21",
            "event_network_location": "Santa Clara,CA,United States",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "23.44.229.234",
            "event_network_remote_port": 80,
            "event_type": ["netconn"],
            "ingress_time": 1675826462036,
            "legacy": True,
            "observation_description": "The application firefox.exe invoked ",
            "observation_id": "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
            "observation_type": "CB_ANALYTICS",
            "org_id": "ABCD123456",
            "parent_guid": "ABCD123456-010ac2d3-00001c68-00000000-1d93b6c4d1f20ad",
            "parent_pid": 7272,
            "process_guid": "ABCD123456-010ac2d3-00001cf8-00000000-1d93b6c4d2b16a4",
            "process_hash": [
                "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dcda7b29"
            ],
            "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38\\updates",
            "process_pid": [2000],
            "process_username": ["DEV01-39X-1\\bit9qa"],
        },
        {
            "alert_category": ["OBSERVED"],
            "alert_id": None,
            "backend_timestamp": "2023-02-08T03:22:59.196Z",
            "device_group_id": 0,
            "device_id": 17482451,
            "device_name": "dev01-39x-1",
            "device_policy_id": 20792247,
            "device_timestamp": "2023-02-08T03:20:33.751Z",
            "enriched": True,
            "enriched_event_type": ["NETWORK"],
            "event_description": "The script",
            "event_id": "8fbccc2da75f11ed937ae3cb089984c6",
            "event_network_inbound": False,
            "event_network_local_ipv4": "10.203.105.21",
            "event_network_location": "Santa Clara,CA,United States",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "23.44.229.234",
            "event_network_remote_port": 80,
            "event_type": ["netconn"],
            "ingress_time": 1675826462036,
            "legacy": True,
            "observation_description": "The application firefox.exe invoked ",
            "observation_id": "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
            "observation_type": "CB_ANALYTICS",
            "org_id": "ABCD123456",
            "parent_guid": "ABCD123456-010ac2d3-00001c68-00000000-1d93b6c4d1f20ad",
            "parent_pid": 7272,
            "process_guid": "ABCD123456-010ac2d3-00001cf8-00000000-1d93b6c4d2b16a4",
            "process_hash": [
                "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dcda7b29"
            ],
            "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38\\updates",
            "process_pid": [2000],
            "process_username": ["DEV01-39X-1\\bit9qa"],
        },
    ],
}


GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING = {
    "num_found": 808,
    "num_available": 1,
    "contacted": 6,
    "completed": 0,
    "results": [],
}


GET_OBSERVATIONS_DETAIL_JOB_RESULTS_RESP = {
    "approximate_unaggregated": 2,
    "completed": 4,
    "contacted": 4,
    "num_aggregated": 1,
    "num_available": 1,
    "num_found": 1,
    "results": [
        {
            "alert_category": ["OBSERVED"],
            "alert_id": None,
            "backend_timestamp": "2023-02-08T03:22:21.570Z",
            "device_external_ip": "127.0.0.1",
            "device_group_id": 0,
            "device_id": 17482451,
            "device_installed_by": "bit9qa",
            "device_internal_ip": "127.0.0.1",
            "device_location": "ONSITE",
            "device_name": "dev01-39x-1",
            "device_os": "WINDOWS",
            "device_os_version": "Windows 10 x64",
            "device_policy": "lonergan policy",
            "device_policy_id": 12345,
            "device_target_priority": "MEDIUM",
            "device_timestamp": "2023-02-08T03:20:33.751Z",
            "document_guid": "KBrOYUNlTYe116ADgNvGw",
            "enriched": True,
            "enriched_event_type": "NETWORK",
            "event_description": "The script...",
            "event_id": "8fbccc2da75f11ed937ae3cb089984c6",
            "event_network_inbound": False,
            "event_network_local_ipv4": "127.0.0.1",
            "event_network_location": "Santa Clara,CA,United States",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "127.0.0.1",
            "event_network_remote_port": 80,
            "event_report_code": "SUB_RPT_NONE",
            "event_threat_score": [3],
            "event_type": "netconn",
            "ingress_time": 1675826462036,
            "legacy": True,
            "netconn_actions": ["ACTION_CONNECTION_ESTABLISHED"],
            "netconn_domain": "a1887..dscq..akamai..net",
            "netconn_inbound": False,
            "netconn_ipv4": 388818410,
            "netconn_local_ipv4": 11111,
            "netconn_local_port": 11,
            "netconn_location": "Santa Clara,CA,United States",
            "netconn_port": 80,
            "netconn_protocol": "PROTO_TCP",
            "observation_description": "The application firefox.exe invoked ",
            "observation_id": "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
            "observation_type": "CB_ANALYTICS",
            "org_id": "ABCD123456",
            "parent_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "parent_effective_reputation_source": "CLOUD",
            "parent_guid": "TEST-010ac2d3-00001c68-00000000-1d93b6c4d1f20ad",
            "parent_hash": [
                "69c8bd1c1dc6103df6bfa9882b5717c0dc4acb8c0c85d8f5c9900db860b6c29b"
            ],
            "parent_name": "c:\\program files\\mozilla firefox\\firefox.exe",
            "parent_pid": 7272,
            "parent_reputation": "NOT_LISTED",
            "process_cmdline": ["C:\\Program Files\\Mozilla "],
            "process_cmdline_length": [268],
            "process_effective_reputation": "NOT_LISTED",
            "process_effective_reputation_source": "AV",
            "process_guid": "ABCD123456-010ac2d3-00001cf8-00000000-1d93b6c4d2b16a4",
            "process_hash": [
                "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dc"
            ],
            "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38\\updates",
            "process_pid": [2000],
            "process_reputation": "NOT_LISTED",
            "process_sha256": "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dc",
            "process_start_time": "2023-02-08T03:20:32.131Z",
            "process_username": ["DEV01-39X-1\\bit9qa"],
            "ttp": [
                "INTERNATIONAL_SITE",
                "ACTIVE_CLIENT",
                "NETWORK_ACCESS",
                "UNKNOWN_APP",
            ],
        }
    ],
}

GET_OBSERVATIONS_SEARCH_JOB_RESULTS_RESP_ALERTS = {
    "approximate_unaggregated": 2,
    "completed": 4,
    "contacted": 4,
    "num_aggregated": 1,
    "num_available": 1,
    "num_found": 1,
    "results": [
        {
            "alert_category": ["OBSERVED"],
            "alert_id": ["be6ff259-88e3-6286-789f-74defa192fff"],
            "backend_timestamp": "2023-02-08T03:22:21.570Z",
            "device_external_ip": "127.0.0.1",
            "device_group_id": 0,
            "device_id": 17482451,
            "device_installed_by": "bit9qa",
            "device_internal_ip": "127.0.0.1",
            "device_location": "ONSITE",
            "device_name": "dev01-39x-1",
            "device_os": "WINDOWS",
            "device_os_version": "Windows 10 x64",
            "device_policy": "lonergan policy",
            "device_policy_id": 12345,
            "device_target_priority": "MEDIUM",
            "device_timestamp": "2023-02-08T03:20:33.751Z",
            "document_guid": "KBrOYUNlTYe116ADgNvGw",
            "enriched": True,
            "enriched_event_type": "NETWORK",
            "event_description": "The script...",
            "event_id": "8fbccc2da75f11ed937ae3cb089984c6",
            "event_network_inbound": False,
            "event_network_local_ipv4": "127.0.0.1",
            "event_network_location": "Santa Clara,CA,United States",
            "event_network_protocol": "TCP",
            "event_network_remote_ipv4": "127.0.0.1",
            "event_network_remote_port": 80,
            "event_report_code": "SUB_RPT_NONE",
            "event_threat_score": [3],
            "event_type": "netconn",
            "ingress_time": 1675826462036,
            "legacy": True,
            "netconn_actions": ["ACTION_CONNECTION_ESTABLISHED"],
            "netconn_domain": "a1887..dscq..akamai..net",
            "netconn_inbound": False,
            "netconn_ipv4": 388818410,
            "netconn_local_ipv4": 11111,
            "netconn_local_port": 11,
            "netconn_location": "Santa Clara,CA,United States",
            "netconn_port": 80,
            "netconn_protocol": "PROTO_TCP",
            "observation_description": "The application firefox.exe invoked ",
            "observation_id": "8fbccc2da75f11ed937ae3cb089984c6:be6ff259-88e3-6286-789f-74defa192d2e",
            "observation_type": "CB_ANALYTICS",
            "org_id": "ABCD123456",
            "parent_effective_reputation": "ADAPTIVE_WHITE_LIST",
            "parent_effective_reputation_source": "CLOUD",
            "parent_guid": "TEST-010ac2d3-00001c68-00000000-1d93b6c4d1f20ad",
            "parent_hash": [
                "69c8bd1c1dc6103df6bfa9882b5717c0dc4acb8c0c85d8f5c9900db860b6c29b"
            ],
            "parent_name": "c:\\program files\\mozilla firefox\\firefox.exe",
            "parent_pid": 7272,
            "parent_reputation": "NOT_LISTED",
            "process_cmdline": ["C:\\Program Files\\Mozilla "],
            "process_cmdline_length": [268],
            "process_effective_reputation": "NOT_LISTED",
            "process_effective_reputation_source": "AV",
            "process_guid": "ABCD123456-010ac2d3-00001cf8-00000000-1d93b6c4d2b16a4",
            "process_hash": [
                "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dc"
            ],
            "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38\\updates",
            "process_pid": [2000],
            "process_reputation": "NOT_LISTED",
            "process_sha256": "9df1ec5e25919660a1b0b85d3965d55797b9aac81e028008428106c4dc",
            "process_start_time": "2023-02-08T03:20:32.131Z",
            "process_username": ["DEV01-39X-1\\bit9qa"],
            "ttp": [
                "INTERNATIONAL_SITE",
                "ACTIVE_CLIENT",
                "NETWORK_ACCESS",
                "UNKNOWN_APP",
            ],
        }
    ],
}


"""Mocks for observations facet query testing."""


POST_OBSERVATIONS_FACET_SEARCH_JOB_RESP = {
    "job_id": "08ffa932-b633-4107-ba56-8741e929e48b"
}


GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_1 = {
    "ranges": [
        {
            "start": "2020-08-04T08:01:32.077Z",
            "end": "2020-08-05T08:01:32.077Z",
            "bucket_size": "+1HOUR",
            "field": "device_timestamp",
            "values": [{"total": 456, "name": "2020-08-04T08:01:32.077Z"}],
        }
    ],
    "terms": [
        {
            "values": [{"total": 116, "id": "chrome.exe", "name": "chrome.exe"}],
            "field": "process_name",
        }
    ],
    "num_found": 116,
    "contacted": 34,
    "completed": 34,
}


GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_2 = {
    "ranges": [],
    "terms": [
        {
            "values": [{"total": 116, "id": "chrome.exe", "name": "chrome.exe"}],
            "field": "process_name",
        }
    ],
    "num_found": 116,
    "contacted": 34,
    "completed": 34,
}


GET_OBSERVATIONS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING = {
    "ranges": [],
    "terms": [],
    "num_found": 0,
    "contacted": 34,
    "completed": 0,
}


GET_OBSERVATIONS_GROUPED_RESULTS_RESP = {
    "approximate_unaggregated": 442,
    "completed": 7,
    "contacted": 7,
    "group_results": [
        {
            "group_end_timestamp": "2023-02-14T06:20:35.696Z",
            "group_key": "device_name",
            "group_start_timestamp": "2023-02-05T09:34:57.499Z",
            "group_value": "dev01-39x-1",
            "results": [
                {
                    "alert_category": ["OBSERVED"],
                    "alert_id": ["fbb78467-f63c-ac52-622a-f41c6f07d815"],
                    "backend_timestamp": "2023-02-14T06:23:18.887Z",
                    "device_group_id": 0,
                    "device_id": 17482451,
                    "device_name": "dev01-39x-1",
                    "device_policy_id": 20792247,
                    "device_timestamp": "2023-02-14T06:20:35.696Z",
                    "enriched": True,
                    "enriched_event_type": ["NETWORK"],
                    "event_description": "The script ...",
                    "event_id": "c7bdd379ac2f11ed92c0b59a6de446c9",
                    "event_network_inbound": False,
                    "event_network_local_ipv4": "10.203.105.21",
                    "event_network_location": "Santa Clara,CA,United States",
                    "event_network_protocol": "TCP",
                    "event_network_remote_ipv4": "23.67.33.87",
                    "event_network_remote_port": 80,
                    "event_type": ["netconn"],
                    "ingress_time": 1676355686412,
                    "legacy": True,
                    "observation_description": "The application",
                    "observation_id": "c7bdd379ac2f11ed92c0b59a6de446c9:fbb78467-f63c-ac52-622a-f41c6f07d815",
                    "observation_type": "CB_ANALYTICS",
                    "org_id": "ABCD123456",
                    "parent_guid": "ABCD123456-010ac2d3-00001164-00000000-1d9403c70fffc03",
                    "parent_pid": 4452,
                    "process_guid": "ABCD123456-010ac2d3-0000066c-00000000-1d9403c710932fb",
                    "process_hash": [
                        "dcb5ffb192d9bce84d21f274a87cb5f839ed92094121cc254b5f3bae2f266d62"
                    ],
                    "process_name": "c:\\programdata\\mozilla-1de4eec8-1241-4177-a864-e594e8d1fb38",
                    "process_pid": [2000],
                    "process_username": ["DEV01-39X-1\\bit9qa"],
                }
            ],
            "total_events": 1,
        }
    ],
    "groups_num_available": 0,
    "num_aggregated": 0,
    "num_available": 1,
    "num_found": 1,
}


GET_NETWORK_THREAT_METADATA_RESP = {
    "detector_abstract": "QE Test signature",
    "detector_goal": "QE Test signature",
    "false_negatives": None,
    "false_positives": None,
    "threat_public_comment": "Threat class used for VMWARE NSX Testing",
}
