"""Mock data for NSX Remediation API."""

NSX_REQUEST_1 = {
    "device_ids": [142, 857],
    "action_type": "NSX_REMEDIATION",
    "options": {
        "toggle": "ON",
        "tag": "CB-NSX-Quarantine"
    }
}

NSX_RESPONSE_1 = {
    "job_ids": [
        "NSX_REMEDIATE_7ff05537-350a-420c-bfa8-3408ac70ce53"
    ]
}

JOB_STATUS_RUNNING = {
    "error_code": "",
    "reason": "Running",
    "status": "RUNNING"
}

NSX_REQUEST_2 = {
    "device_ids": [5150],
    "action_type": "NSX_REMEDIATION",
    "options": {
        "toggle": "OFF",
        "tag": "CB-NSX-Isolate"
    }
}

NSX_RESPONSE_2 = {
    "job_ids": [
        "NSX_REMEDIATE_540d3f7f-65f6-47c7-b581-692d2c892e22"
    ]
}

NSX_REQUEST_2A = {
    "device_ids": [98765],
    "action_type": "NSX_REMEDIATION",
    "options": {
        "toggle": "OFF",
        "tag": "CB-NSX-Quarantine"
    }
}

NSX_RESPONSE_2A = {
    "job_ids": [
        "NSX_REMEDIATE_2da0bc0e-ed1e-4a98-b8fa-ccc1e30c9576"
    ]
}

NSX_REQUEST_3 = {
    "device_ids": [12, 23, 34, 45, 56, 67, 78, 89, 90],
    "action_type": "NSX_REMEDIATION",
    "options": {
        "toggle": "ON",
        "tag": "CB-NSX-Custom"
    }
}

NSX_RESPONSE_3 = {
    "job_ids": [
        "NSX_REMEDIATE_8b45115f-2827-4b8e-a0ab-5919c00213ac",
        "NSX_REMEDIATE_18acf87a-9b92-4fd9-82a1-a3b75592e348",
        "NSX_REMEDIATE_7fd50527-3cdb-4996-b316-6ad45ec18af6"
    ]
}

NSX_LIFECYCLE_1 = {
    'NSX_REMEDIATE_9a904df0-38fb-4246-a537-1dbca6829b7c': ['SCHEDULED', 'RUNNING', 'SUCCESSFUL'],
    'NSX_REMEDIATE_87ce65c0-8325-4e99-a0e1-cd7343dbc38d': ['FAILED'],
    'NSX_REMEDIATE_e881b4f3-680b-4a43-bc7e-043330e65d50': ['RUNNING', 'RUNNING', 'RUNNING', 'RUNNING', 'SUCCESSFUL']
}

NSX_DEVICE_DATA_1 = {
    "deployment_type": "WORKLOAD",
    "id": 98765,
    "nsx_enabled": True,
    "nsx_distributed_firewall_policy": "CB-NSX-Quarantine"
}

NSX_DEVICE_DATA_1A = {
    "deployment_type": "WORKLOAD",
    "id": 99887,
    "nsx_enabled": True,
    "nsx_distributed_firewall_policy": "CB-NSX-Isolate"
}

NSX_DEVICE_DATA_2 = {
    "deployment_type": "ENDPOINT",
    "id": 13227,
    "nsx_enabled": True,
    "nsx_distributed_firewall_policy": "CB-NSX-Custom"
}

NSX_DEVICE_DATA_3 = {
    "deployment_type": "WORKLOAD",
    "id": 16676,
    "nsx_enabled": False,
    "nsx_distributed_firewall_policy": None
}

NSX_DEVICE_DATA_3A = {
    "deployment_type": "WORKLOAD",
    "id": 16676,
    "nsx_enabled": True,
    "nsx_distributed_firewall_policy": None
}
