CORE_PREVENTION_RETURNS = {
    "results": [
        {
            "id": "1f8a5e4b-34f2-4d31-9f8f-87c56facaec8",
            "name": "Advanced Scripting Prevention",
            "description": "Addresses malicious fileless and file-backed scripts that leverage native programs [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        },
        {
            "id": "ac67fa14-f6be-4df9-93f2-6de0dbd96061",
            "name": "Credential Theft",
            "description": "Addresses threat actors obtaining credentials and relies on detecting the malicious [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
            "name": "Carbon Black Threat Intel",
            "description": "Addresses common and pervasive TTPs used for malicious activity as well as [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "REPORT"
            }
        },
        {
            "id": "88b19232-7ebb-48ef-a198-2a75a282de5d",
            "name": "Privilege Escalation",
            "description": "Addresses behaviors that indicate a threat actor has gained elevated access via [...]",
            "inherited_from": "psc:region",
            "category": "core_prevention",
            "parameters": {
                "WindowsAssignmentMode": "BLOCK"
            }
        }
    ]
}

CORE_PREVENTION_UPDATE_1 = [
    {
        "id": "c4ed61b3-d5aa-41a9-814f-0f277451532b",
        "parameters": {
            "WindowsAssignmentMode": "BLOCK"
        }
    }
]

HBFW_GET_RESULT = {
    "results": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...].",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                    "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                    "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
                },
                "enable_host_based_firewall": False
            }
        }
    ]
}

HBFW_MODIFY_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
                {
                    "description": "Starship go BOOM",
                    "name": "Argon_firewall",
                    "rules": [
                        {
                            "action": "ALLOW",
                            "application_path": "*",
                            "direction": "BOTH",
                            "enabled": True,
                            "local_ip_address": "1.2.3.4",
                            "local_port_ranges": "1234",
                            "name": "my_first_rule",
                            "protocol": "TCP",
                            "remote_ip_address": "199.201.128.1",
                            "remote_port_ranges": "5678",
                            "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                            "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                            "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                }
            ],
            "default_rule": {
                "action": "BLOCK",
                "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
            },
            "enable_host_based_firewall": True
        }
    }
]

HBFW_MODIFY_PUT_RESPONSE = {
    "successful": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...].",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Starship go BOOM",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "default_rule": {
                    "action": "BLOCK",
                    "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                    "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                    "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
                },
                "enable_host_based_firewall": True
            }
        }
    ],
    "failed": []
}

HBFW_ADD_RULE_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
                {
                    "description": "Whatever",
                    "name": "Argon_firewall",
                    "rules": [
                        {
                            "action": "ALLOW",
                            "application_path": "*",
                            "direction": "IN",
                            "enabled": True,
                            "local_ip_address": "1.2.3.4",
                            "local_port_ranges": "1234",
                            "name": "my_first_rule",
                            "protocol": "TCP",
                            "remote_ip_address": "5.6.7.8",
                            "remote_port_ranges": "5678",
                            "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                            "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                            "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                            "test_mode": False
                        },
                        {
                            "action": "BLOCK",
                            "application_path": "C:\\DOOM\\DOOM.EXE",
                            "direction": "BOTH",
                            "enabled": True,
                            "local_ip_address": "10.29.99.1",
                            "local_port_ranges": "*",
                            "name": "DoomyDoomsOfDoom",
                            "protocol": "TCP",
                            "remote_ip_address": "199.201.128.1",
                            "remote_port_ranges": "666",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                }
            ],
            "default_rule": {
                "action": "ALLOW",
                "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
            },
            "enable_host_based_firewall": False
        }
    }
]

HBFW_ADD_RULE_PUT_RESPONSE = {
    "successful": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...].",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            },
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsOfDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            },
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsOfDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                    "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                    "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
                },
                "enable_host_based_firewall": False
            }
        }
    ],
    "failed": []
}

HBFW_ADD_RULE_GROUP_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
                {
                    "description": "Whatever",
                    "name": "Argon_firewall",
                    "rules": [
                        {
                            "action": "ALLOW",
                            "application_path": "*",
                            "direction": "IN",
                            "enabled": True,
                            "local_ip_address": "1.2.3.4",
                            "local_port_ranges": "1234",
                            "name": "my_first_rule",
                            "protocol": "TCP",
                            "remote_ip_address": "5.6.7.8",
                            "remote_port_ranges": "5678",
                            "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                            "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                            "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                },
                {
                    "description": "No playing DOOM!",
                    "name": "DOOM_firewall",
                    "rules": [
                        {
                            "action": "BLOCK",
                            "application_path": "C:\\DOOM\\DOOM.EXE",
                            "direction": "BOTH",
                            "enabled": True,
                            "local_ip_address": "10.29.99.1",
                            "local_port_ranges": "*",
                            "name": "DoomyDoomsOfDoom",
                            "protocol": "TCP",
                            "remote_ip_address": "199.201.128.1",
                            "remote_port_ranges": "666",
                            "test_mode": False
                        }
                    ]
                }
            ],
            "default_rule": {
                "action": "ALLOW",
                "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
            },
            "enable_host_based_firewall": False
        }
    }
]

HBFW_ADD_RULE_GROUP_PUT_RESPONSE = {
    "successful": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...].",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            },
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    },
                    {
                        "description": "No playing DOOM!",
                        "name": "DOOM_firewall",
                        "rules": [
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsOfDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Argon_firewall",
                        "rules": [
                            {
                                "action": "ALLOW",
                                "application_path": "*",
                                "direction": "IN",
                                "enabled": True,
                                "local_ip_address": "1.2.3.4",
                                "local_port_ranges": "1234",
                                "name": "my_first_rule",
                                "protocol": "TCP",
                                "remote_ip_address": "5.6.7.8",
                                "remote_port_ranges": "5678",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            },
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    },
                    {
                        "description": "No playing DOOM!",
                        "name": "DOOM_firewall",
                        "rules": [
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsOfDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "6d36954a-a944-4944-ae94-df6f94b877b8",
                                "rule_inbound_event_check_guid": "8a39c00b-f907-4085-929f-f2e98e8b7b87",
                                "rule_outbound_event_check_guid": "7e7a9761-4187-4065-8ae1-b5161fae75a2",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "0c0ce332-6f81-43d9-ad9b-875e82eb53f9"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "08dc129b-ab72-4ed7-8282-8db7f62bc7e8",
                    "default_rule_inbound_event_check_guid": "40dd836c-e676-4e3b-b98b-c870c4b6faa7",
                    "default_rule_outbound_event_check_guid": "94283d79-c2d1-472c-b303-77a0fb387bcc"
                },
                "enable_host_based_firewall": False
            }
        }
    ],
    "failed": []
}
