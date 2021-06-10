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

POST_PROFILE_IN_GRANT_RESP_2 = {
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
        "expiration": '20211031T12:34:56',
        "disabled": True
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
    "results": [
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

DETAILS_GRANT1 = {
    "principal": "psc:user:test:3911",
    "expires": 0,
    "revoked": True,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER",
        "psc:role:test:APP_SERVICE_ROLE"
    ],
    "profiles": [],
    "org_ref": "psc:org:test",
    "principal_name": "Ed Mercer",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

EXPECT_CHANGE_ROLE_GRANT1 = {
    "principal": "psc:user:test:3911",
    "expires": 0,
    "revoked": True,
    "roles": [
        "psc:role::SECOPS_ROLE_MANAGER",
        "psc:role:test:APP_SERVICE_ROLE",
        "psc:role:test:NEW_ROLE"
    ],
    "profiles": [],
    "org_ref": "psc:org:test",
    "principal_name": "Ed Mercer",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

DETAILS_GRANT2 = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
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
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
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
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

EXPECT_CHANGE_ROLE_GRANT2A = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
            "orgs": {
                "allow": [
                    "psc:org:test2",
                    "psc:org:test3"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        }
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

EXPECT_CHANGE_ROLE_GRANT2B = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
            "orgs": {
                "allow": [
                    "psc:org:test2",
                    "psc:org:test3"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
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
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

EXPECT_DISABLE_ALL_GRANT2 = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": True
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
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
                "disabled": True
            },
            "can_manage": False
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
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
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

DETAILS_GRANT3 = {
    "principal": "psc:user:test:4338",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": True
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
            "orgs": {
                "allow": [
                    "psc:org:test3"
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
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Daniel Jackson",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

PROFILE_TEMPLATES_A = [
    {
        "orgs": {
            "allow": [
                "psc:org:test2"
            ],
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER",
            "psc:role:test:ALPHA_ROLE"
        ]
    },
    {
        "orgs": {
            "allow": [
                "psc:org:test_infinity"
            ],
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ]
    },
]

EXPECT_ADD_PROFILES_3A = {
    "principal": "psc:user:test:4338",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
            "orgs": {
                "allow": [
                    "psc:org:test3"
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
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Daniel Jackson",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

PROFILE_TEMPLATES_B = [
    {
        "orgs": {
            "allow": [
                "psc:org:test2"
            ],
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER",
            "psc:role:test:ALPHA_ROLE"
        ]
    }
]

EXPECT_ADD_PROFILES_3B = {
    "principal": "psc:user:test:4338",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
            "orgs": {
                "allow": [
                    "psc:org:test3"
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
    ],
    "org_ref": "psc:org:test",
    "principal_name": "Daniel Jackson",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

PROFILE_TEMPLATES_C = [
    {
        "orgs": {
            "allow": [
                "psc:org:test_infinity"
            ],
        },
        "roles": [
            "psc:role::SECOPS_ROLE_MANAGER"
        ]
    }
]

EXPECT_DISABLE_2B = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": True
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
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
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
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
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

EXPECT_SET_EXPIRATION_2B = {
    "principal": "psc:user:test:3934",
    "expires": 0,
    "revoked": False,
    "roles": [],
    "profiles": [
        {
            "profile_uuid": "c57ba255-1736-4bfa-a59d-c54bb97a41d6",
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": '20111031T12:34:56',
                "disabled": False
            },
            "can_manage": False
        },
        {
            "profile_uuid": "68b1f6e4-6d49-4e13-9278-723d08957cd4",
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
        },
        {
            "profile_uuid": "d79bcdd7-443c-409a-a415-92ccd7a1395c",
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
    "principal_name": "Malcolm Reynolds",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}

PERMITTED_ROLES_RESP = {
    "results": {
        "org1": [
            {
                "urn": "psc:role::ALPHA",
                "scoped": "psc:org:ABCD1234",
                "name": "Support",
                "desc": "The Alpha role.",
                "disabled": False,
                "capabilities": ["internal"],
                "child_urn": "psc:role::ALPHA",
                "created_by": "psc:user:ABCD1234:DEFG1234",
                "updated_by": "psc:user:ABCD1234:DEFG1234",
                "create_time": {},
                "update_time": {}
            },
            {
                "urn": "psc:role::BRAVO",
                "scoped": "psc:org:ABCD1234",
                "name": "Support",
                "desc": "The Bravo role.",
                "disabled": False,
                "capabilities": ["internal"],
                "child_urn": "psc:role::BRAVO",
                "created_by": "psc:user:ABCD1234:DEFG1234",
                "updated_by": "psc:user:ABCD1234:DEFG1234",
                "create_time": {},
                "update_time": {}
            }
        ],
        "org1:CHILDREN": [
            {
                "urn": "psc:role::CHARLIE",
                "scoped": "psc:org:ABCD1234",
                "name": "Support",
                "desc": "The Charlie role.",
                "disabled": False,
                "capabilities": ["internal"],
                "child_urn": "psc:role::CHARLIE",
                "created_by": "psc:user:ABCD1234:DEFG1234",
                "updated_by": "psc:user:ABCD1234:DEFG1234",
                "create_time": {},
                "update_time": {}
            },
            {
                "urn": "psc:role::BRAVO",
                "scoped": "psc:org:ABCD1234",
                "name": "Support",
                "desc": "The Bravo role.",
                "disabled": False,
                "capabilities": ["internal"],
                "child_urn": "psc:role::BRAVO",
                "created_by": "psc:user:ABCD1234:DEFG1234",
                "updated_by": "psc:user:ABCD1234:DEFG1234",
                "create_time": {},
                "update_time": {}
            }
        ]
    }
}

EXPECT_NEW_GRANT_5A = {
    "principal": "psc:user:test:3978",
    'org_ref': 'psc:org:test',
    'roles': [],
    'principal_name': "Beckett Mariner",
    'profiles': PROFILE_TEMPLATES_A
}

POST_GRANT_RESP_5A = {
    "principal": "psc:user:test:3978",
    "expires": 0,
    "revoked": False,
    "roles": [
    ],
    "profiles": [
        {
            "orgs": {
                "allow": [
                    "psc:org:test2"
                ],
            },
            "roles": [
                "psc:role::SECOPS_ROLE_MANAGER",
                "psc:role:test:ALPHA_ROLE"
            ],
            "conditions": {
                "expiration": 0,
                "disabled": False
            },
            "can_manage": False
        },
        {
            "orgs": {
                "allow": [
                    "psc:org:test_infinity"
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
    "principal_name": "Beckett Mariner",
    "created_by": "psc:user:FOO:BAR",
    "updated_by": "psc:user:FOO:BAR",
    "create_time": "2021-03-20T12:56:31.645Z",
    "update_time": "2021-03-20T12:56:31.645Z"
}
