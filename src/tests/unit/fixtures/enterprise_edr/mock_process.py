GET_PROCESS_RESP = {}

GET_PROCESS_SUMMARY_RESP = {
    "incomplete_results": False,
    "process": {
        "_s3_location": "A7Y2cg0hRsKblxNp_sqYRg:1742cae0777:f9d74:95f:default:3",
        "backend_timestamp": "2020-08-26T21:30:06.937Z",
        "device_external_ip": "144.121.3.50",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "10.210.34.172",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "sm-restrictive",
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
        "org_id": "WNEXFKQ7",
        "parent_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
        "parent_hash": [
            "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
        ],
        "parent_name": "/usr/lib/systemd/systemd",
        "parent_pid": 1,
        "partition_id": 0,
        "process_cmdline": [
            "/usr/lib/polkit-1/polkitd --no-debug"
        ],
        "process_guid": "WNEXFKQ7-0002b226-000015bd-00000000-1d6225bbba74c00",
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
            "device_internal_ip": "144.121.3.50",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "sm-restrictive",
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
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_guid": "WNEXFKQ7-0002b226-0000192c-00000000-1d6225bbba74c00",
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
            "device_external_ip": "144.121.3.50",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 176678,
            "device_internal_ip": "",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "sm-restrictive",
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
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/libexec/nm-dispatcher"
            ],
            "process_guid": "WNEXFKQ7-0002b226-00005e88-00000000-1d66feca9b7d350",
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
            "device_external_ip": "144.121.3.50",
            "device_group": "",
            "device_group_id": 0,
            "device_id": 176678,
            "device_internal_ip": "",
            "device_name": "devr-dev",
            "device_os": "LINUX",
            "device_policy": "sm-restrictive",
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
            "org_id": "WNEXFKQ7",
            "parent_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
            "parent_hash": [
                "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
            ],
            "parent_name": "/usr/lib/systemd/systemd",
            "parent_pid": 1,
            "partition_id": 0,
            "process_cmdline": [
                "/usr/libexec/nm-dispatcher"
            ],
            "process_guid": "WNEXFKQ7-0002b226-00000f79-00000000-1d66fef56e95f10",
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
        "device_external_ip": "144.121.3.50",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "10.210.34.172",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "sm-restrictive",
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
        "org_id": "WNEXFKQ7",
        "partition_id": 0,
        "process_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
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

GET_TREE_RESP = {
    "incomplete_results": False,
    "nodes": {
        "_s3_location": "A7Y2cg0hRsKblxNp_sqYRg:1742d01db15:a8a2:5fb:default:3",
        "backend_timestamp": "2020-08-26T23:02:10.357Z",
        "children": [
            {
                "_s3_location": "nNWpDm_5QXG5vVI5c9YG-Q:1720df24ea4:0:69a:longTerm:3",
                "backend_timestamp": "2020-05-13T12:11:23.172Z",
                "device_external_ip": "",
                "device_id": 176678,
                "device_internal_ip": "144.121.3.50",
                "device_name": "devr-dev",
                "device_os": "LINUX",
                "device_policy": "sm-restrictive",
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
                "org_id": "WNEXFKQ7",
                "parent_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
                "parent_hash": [
                    "81b37dcb0321108e564d528df827580153ab64005be3bcafd5162e9e7e707e85"
                ],
                "parent_name": "/usr/lib/systemd/systemd",
                "parent_pid": 1,
                "partition_id": 0,
                "process_guid": "WNEXFKQ7-0002b226-0000192c-00000000-1d6225bbba74c00",
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
        "device_external_ip": "144.121.3.50",
        "device_group_id": 0,
        "device_id": 176678,
        "device_internal_ip": "10.210.34.172",
        "device_name": "devr-dev",
        "device_os": "LINUX",
        "device_policy": "sm-restrictive",
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
        "org_id": "WNEXFKQ7",
        "partition_id": 0,
        "process_guid": "WNEXFKQ7-0002b226-00000001-00000000-1d6225bbba74c00",
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
