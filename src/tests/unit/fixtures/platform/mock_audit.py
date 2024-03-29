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
