"""Mock responses for Grant and Profile"""

GET_GRANT_RESP = {
    "principal": "psc:user:12345678:ABCDEFGH",
    "expires": 0,
    "revoked": False,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER",
        "psc:role:test:APP_SERVICE_ROLE"
    ],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        }
    ],
    "org_ref": "psc:org:test",
    "principal_name": "J. Random Nerd",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

PUT_GRANT_RESP = {
    "principal": "psc:user:12345678:ABCDEFGH",
    "expires": 0,
    "revoked": False,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER",
        "psc:role:test:APP_SERVICE_ROLE",
        "psc:role:test:DUMMY_ROLE"
    ],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2",
                    "psc:org:test3"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        }
    ],
    "org_ref": "psc:org:test",
    "principal_name": "J. Random Nerd",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

POST_GRANT_RESP = {
    "principal": "psc:user:ABC12345:DEF67890",
    "expires": 0,
    "revoked": False,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER"
    ],
    "profiles": [
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Doug Jones",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

POST_PROFILE_IN_GRANT_RESP = {
    "profile_uuid": "REPLACEME",
    "orgs": {
        "allow": [
            "psc:org:test2"
        ],
    },
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER"
    ],
    "conditions": {
        "expiration": 0,
        "disabled": False
    },
    "can_manage": False
}

PUT_PROFILE_RESP = {
    "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
    "orgs": {
        "allow": [
            "psc:org:test2",
            "psc:org:test22"
        ],
    },
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER"
    ],
    "conditions": {
        "expiration": 0,
        "disabled": False
    },
    "can_manage": False
}

DELETE_PROFILE_RESP = {
    "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
    "orgs": {
        "allow": [
            "psc:org:test2"
        ],
    },
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER"
    ],
    "conditions": {
        "expiration": 0,
        "disabled": True
    },
    "can_manage": False
}

DELETE_GRANT_RESP = {
    "principal": "psc:user:12345678:ABCDEFGH",
    "expires": 0,
    "revoked": True,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER",
        "psc:role:test:APP_SERVICE_ROLE"
    ],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        }
    ],
    "org_ref": "psc:org:test",
    "principal_name": "J. Random Nerd",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

QUERY_GRANT_RESP = {
    "additionalProp1": [
        {
            "principal": "psc:user:12345678:ABCDEFGH",
            "expires": 0,
            "revoked": False,
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:APP_SERVICE_ROLE"
            ],
            "profiles": [
                {
                    "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
                    "orgs": {
                        "allow": [
                            "psc:org:test2"
                        ],
                    },
                    "roles": [
                        "psc:role::SECOPS_ROLE_MANAGER"
                    ],
                    "conditions": {
                        "expiration": 0,
                        "disabled": False
                    },
                    "can_manage": False
                }
            ],
            "org_ref": "psc:org:test",
            "principal_name": "J. Random Nerd",
            "created_by": "psc:user:FOO:BAR",
            "updated_by": "psc:user:FOO:BAR",
            "create_time": "2021-03-20T12:56:31.645Z",
            "update_time": "2021-03-20T12:56:31.645Z"
        },
        {
            "principal": "psc:user:87654321:HGFEDCBA",
            "expires": 0,
            "revoked": False,
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:APP_SERVICE_ROLE"
            ],
            "profiles": [
                {
                    "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
                    "orgs": {
                        "allow": [
                            "psc:org:test2"
                        ],
                    },
                    "roles": [
                        "psc:role::SECOPS_ROLE_MANAGER"
                    ],
                    "conditions": {
                        "expiration": 0,
                        "disabled": False
                    },
                    "can_manage": False
                }
            ],
            "org_ref": "psc:org:test",
            "principal_name": "Sally Shears",
            "created_by": "psc:user:FOO:BAR",
            "updated_by": "psc:user:FOO:BAR",
            "create_time": "2021-03-20T12:56:31.645Z",
            "update_time": "2021-03-20T12:56:31.645Z"
        }
    ]
}
