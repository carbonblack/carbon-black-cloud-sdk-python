"""Mock responses for asset groups"""

CREATE_AG_REQUEST = {
    "description": "Group Test Description",
    "member_type": "DEVICE",
    "name": "Group Test",
    "policy_id": 7113785,
    "query": "os_version:Windows"
}

CREATE_AG_RESPONSE = {
    "id": "4b48a403-e371-4e3d-ae6c-8eb9080fe7ad",
    "name": "Group Test",
    "description": "Group Test Description",
    "org_key": "test",
    "status": "OK",
    "member_type": "DEVICE",
    "discovered": False,
    "create_time": "2022-11-09T06:27:30.734Z",
    "update_time": "2022-11-09T06:27:30.734Z",
    "query": "os_version:Windows",
    "member_count": 0,
    "policy_id": 7113785,
    "policy_name": "Monitored"
}

EXISTING_AG_DATA = {
    "id": "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
    "name": "Existing Group",
    "description": "Some Description",
    "org_key": "test",
    "status": "OK",
    "member_type": "DEVICE",
    "discovered": False,
    "create_time": "2022-11-09T06:27:30.734Z",
    "update_time": "2022-11-09T06:27:30.734Z",
    "query": None,
    "member_count": 0,
    "policy_id": 8675309,
    "policy_name": "Jenny"
}

EXISTING_AG_DATA_2 = {
    "id": "509f437f-6b9a-4b8e-996e-9183b35f9069",
    "name": "Another Group",
    "description": "Some new description",
    "org_key": "test",
    "status": "OK",
    "member_type": "DEVICE",
    "discovered": False,
    "create_time": "2022-11-09T06:27:30.734Z",
    "update_time": "2022-11-09T06:27:30.734Z",
    "query": None,
    "member_count": 0,
    "policy_id": 5555555,
    "policy_name": "MrsQueen"
}

UPDATE_AG_REQUEST = {
    "id": "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
    "name": "Renamed Group",
    "description": "Change This Too",
    "org_key": "test",
    "status": "OK",
    "member_type": "DEVICE",
    "discovered": False,
    "create_time": "2022-11-09T06:27:30.734Z",
    "update_time": "2022-11-09T06:27:30.734Z",
    "query": None,
    "member_count": 0,
    "policy_id": 9001,
    "policy_name": "Jenny"
}

QUERY_REQUEST = {
    "query": "test",
    "criteria": {
        "policy_id": [
            7113785
        ],
        "name": [
            "Group Test"
        ],
        "discovered": [
            False
        ],
        "group_id": [
            "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430"
        ]
    },
    "rows": 42,
    "sort": [
        {
            "field": "name",
            "order": "ASC"
        }
    ],
    "start": 0
}

QUERY_REQUEST_DEFAULT = {
    "rows": 100,
    "start": 0
}

QUERY_RESPONSE = {
    "num_found": 1,
    "results": [
        {
            "id": "9b8b8d84-4a44-4a94-81ec-1f8ef52d4430",
            "name": "Group Test",
            "description": "Group Test",
            "org_key": "test",
            "status": "OK",
            "member_type": "DEVICE",
            "discovered": False,
            "create_time": "2022-09-05T13:12:31.848Z",
            "update_time": "2022-09-05T13:12:31.848Z",
            "query": None,
            "member_count": 0,
            "policy_id": 7113785,
            "policy_name": "Monitored"
        }
    ]
}

LIST_MEMBERS_RESPONSE1 = {
    "num_found": 3,
    "member_ids": [
        "12345678",
        "66760099",
        "42691014"
    ],
    "members": [
        {
            "external_member_id": "12345678",
            "dynamic": True,
            "manual": False
        },
        {
            "external_member_id": "66760099",
            "dynamic": False,
            "manual": True
        },
        {
            "external_member_id": "42691014",
            "dynamic": True,
            "manual": False
        }
    ]
}

LIST_MEMBERS_OUTPUT1 = [
    {
        "external_member_id": 12345678,
        "dynamic": True,
        "manual": False
    },
    {
        "external_member_id": 66760099,
        "dynamic": False,
        "manual": True
    },
    {
        "external_member_id": 42691014,
        "dynamic": True,
        "manual": False
    }
]

LIST_MEMBERS_RESPONSE2 = {
    "num_found": 1,
    "member_ids": [
        "98765"
    ],
    "members": [
        {
            "external_member_id": "98765",
            "dynamic": False,
            "manual": True
        }
    ]
}
