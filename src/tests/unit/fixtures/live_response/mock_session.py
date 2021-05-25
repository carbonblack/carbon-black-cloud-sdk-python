"""Mock session responses for the Live Response API."""

SESSION_INIT_RESP = {
    "id": "1:2468",
    "device_id": 2468,
    "check_in_timeout": 900,
    "session_timeout": 900,
    "status": "pending",
    "current_command_index": 0,
    "create_time": "2021-04-07T17:49:58.792Z",
    "device_check_in_time": "2021-04-07T17:49:58.793Z"
}

SESSION_POLL_RESP = {
    "hostname": None,
    "address": None,
    "os_version": None,
    "current_working_directory": "C:\\Windows\\system32",
    "supported_commands": [
        "put file",
        "get file",
        "memdump",
        "create directory",
        "delete file",
        "directory list",
        "reg enum key",
        "reg query value",
        "reg create key",
        "reg delete key",
        "reg delete value",
        "reg set value",
        "process list",
        "kill",
        "create process"
    ],
    "drives": [
        "A:\\",
        "C:\\",
        "D:\\"
    ],
    "id": "1:2468",
    "device_id": 2468,
    "check_in_timeout": 900,
    "session_timeout": 900,
    "sensor_check_in_time": 1502126744685,
    "status": "active",
    "current_command_index": 0,
    "create_time": 1502126655758
}

SESSION_POLL_RESP_ERROR = {
    "hostname": None,
    "address": None,
    "os_version": None,
    "current_working_directory": "C:\\Windows\\system32",
    "supported_commands": [
        "put file",
        "get file",
        "memdump",
        "create directory",
        "delete file",
        "directory list",
        "reg enum key",
        "reg query value",
        "reg create key",
        "reg delete key",
        "reg delete value",
        "reg set value",
        "process list",
        "kill",
        "create process"
    ],
    "drives": [
        "A:\\",
        "C:\\",
        "D:\\"
    ],
    "id": "1:2468",
    "device_id": 2468,
    "check_in_timeout": 900,
    "session_timeout": 900,
    "sensor_check_in_time": 1502126744685,
    "status": "error",
    "current_command_index": 0,
    "create_time": 1502126655758
}

USESSION_INIT_RESP = {
    "hostname": None,
    "address": None,
    "os_version": None,
    "current_working_directory": None,
    "supported_commands": None,
    "drives": None,
    "id": "1:7777",
    "device_id": 7777,
    "check_in_timeout": 900,
    "session_timeout": 900,
    "sensor_check_in_time": None,
    "status": "pending",
    "current_command_index": 0,
    "create_time": 1502126352449
}

USESSION_POLL_RESP = {
    "hostname": None,
    "address": None,
    "os_version": None,
    "current_working_directory": "/",
    "supported_commands": [
        "put file",
        "get file",
        "memdump",
        "create directory",
        "delete file",
        "directory list",
        "process list",
        "kill",
        "create process"
    ],
    "drives": ["/"],
    "id": "1:7777",
    "device_id": 7777,
    "check_in_timeout": 900,
    "session_timeout": 900,
    "sensor_check_in_time": 1502126744685,
    "status": "active",
    "current_command_index": 0,
    "create_time": 1502126655758
}
