"""Mocks for audit log functionality."""

AUDITLOGS_RESP = {
    "notifications": [
        {
            "requestUrl": None,
            "eventTime": 1529332687006,
            "eventId": "37075c01730511e89504c9ba022c3fbf",
            "loginName": "bs@carbonblack.com",
            "orgName": "example.org",
            "flagged": False,
            "clientIp": "192.0.2.3",
            "verbose": False,
            "description": "Logged in successfully",
        },
        {
            "requestUrl": None,
            "eventTime": 1529332689528,
            "eventId": "38882fa2730511e89504c9ba022c3fbf",
            "loginName": "bs@carbonblack.com",
            "orgName": "example.org",
            "flagged": False,
            "clientIp": "192.0.2.3",
            "verbose": False,
            "description": "Logged in successfully",
        },
        {
            "requestUrl": None,
            "eventTime": 1529345346615,
            "eventId": "b0be64fd732211e89504c9ba022c3fbf",
            "loginName": "bs@carbonblack.com",
            "orgName": "example.org",
            "flagged": False,
            "clientIp": "192.0.2.1",
            "verbose": False,
            "description": "Updated connector jason-splunk-test with api key Y8JNJZFBDRUJ2ZSM",
        },
        {
            "requestUrl": None,
            "eventTime": 1529345352229,
            "eventId": "b41705e7732211e8bd7e5fdbf9c916a3",
            "loginName": "bs@carbonblack.com",
            "orgName": "example.org",
            "flagged": False,
            "clientIp": "192.0.2.2",
            "verbose": False,
            "description": "Updated connector Training with api key GRJSDHRR8YVRML3Q",
        },
        {
            "requestUrl": None,
            "eventTime": 1529345371514,
            "eventId": "bf95ae38732211e8bd7e5fdbf9c916a3",
            "loginName": "bs@carbonblack.com",
            "orgName": "example.org",
            "flagged": False,
            "clientIp": "192.0.2.2",
            "verbose": False,
            "description": "Logged in successfully",
        },
    ],
    "success": True,
    "message": "Success",
}

AUDIT_SEARCH_REQUEST = {
    "criteria": {
        "actor_ip": ["10.29.99.1"],
        "actor": ["ABCDEFGHIJ"],
        "request_url": ["https://inclusiveladyship.com"],
        "description": ["FOOBAR"],
        "flagged": True,
        "verbose": False,
        "create_time": {
            "start": "2024-03-01T00:00:00.000000Z",
            "end": "2024-03-31T22:00:00.000000Z"
        }
    },
    "exclusions": {
        "actor_ip": ["10.29.99.254"],
        "actor": ["JIHGFEDCBA"],
        "request_url": ["https://links.inclusiveladyship.com"],
        "description": ["BLORT"],
        "flagged": False,
        "verbose": True,
        "create_time": {
            "range": "-5d"
        }
    },
    "query": "description:FOO",
    "sort": [
        {
            "field": "actor_ip",
            "order": "ASC"
        }
    ]
}

AUDIT_SEARCH_RESPONSE = {
    "num_found": 5,
    "num_available": 5,
    "results": [
        {
            "org_key": "test",
            "actor_ip": "192.168.0.5",
            "actor": "DEFGHIJKLM",
            "request_url": None,
            "description": "Connector DEFGHIJKLM logged in successfully",
            "flagged": False,
            "verbose": False,
            "create_time": "2024-04-17T19:18:37.480Z"
        },
        {
            "org_key": "test",
            "actor_ip": "192.168.3.5",
            "actor": "BELTALOWDA",
            "request_url": None,
            "description": "Updated report, 'MCRN threat feed'",
            "flagged": False,
            "verbose": False,
            "create_time": "2024-04-17T19:13:01.528Z"
        },
        {
            "org_key": "test",
            "actor_ip": "192.168.3.8",
            "actor": "BELTALOWDA",
            "request_url": None,
            "description": "Updated report, 'Reported by DOP'",
            "flagged": False,
            "verbose": False,
            "create_time": "2024-04-17T19:13:01.042Z"
        },
        {
            "org_key": "test",
            "actor_ip": "192.168.3.11",
            "actor": "BELTALOWDA",
            "request_url": None,
            "description": "Updated report, 'Reported by Mao-Kwikowski'",
            "flagged": False,
            "verbose": False,
            "create_time": "2024-04-17T19:13:00.235Z"
        },
        {
            "org_key": "test",
            "actor_ip": "192.168.3.14",
            "actor": "BELTALOWDA",
            "request_url": None,
            "description": "Updated report, 'Malware SSL Certificate Fingerprint'",
            "flagged": False,
            "verbose": False,
            "create_time": "2024-04-17T19:12:59.693Z"
        }
    ]
}

AUDIT_EXPORT_REQUEST = {
    "query": "description:FOO",
    "format": "csv"
}

MOCK_AUDIT_EXPORT_JOB = {
    "id": 4805565,
    "type": "EXTERNAL",
    "job_parameters": {
        "job_parameters": None
    },
    "org_key": "test",
    "status": "COMPLETED",
    "create_time": "2023-02-02T23:16:25.625583Z",
    "last_update_time": "2023-02-02T23:16:29.079184Z"
}
