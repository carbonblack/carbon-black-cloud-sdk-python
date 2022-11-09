"""Mock responses for asset groups"""


CREATE_AG_REQUEST = {
    "description": "Group Test Description",
    "member_type": "DEVICE",
    "name": "Group Test",
    "policy_id": 7113785
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
    "member_count": 0,
    "policy_id": 8675309,
    "policy_name": "Jenny"
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
    "member_count": 0,
    "policy_id": 9001,
    "policy_name": "Jenny"
}
