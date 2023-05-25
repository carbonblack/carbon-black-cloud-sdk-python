"""Mock responses for PolicyRuleConfig and subclasses"""


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

HBFW_ADD_RULE_GROUP_EMPTY_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
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

HBFW_ADD_RULE_GROUP_EMPTY_PUT_RESPONSE = {
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

HBFW_REMOVE_RULE_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
                {
                    "description": "Whatever",
                    "name": "Crapco_firewall",
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
                            "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                            "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                            "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                },
                {
                    "description": "IRC is a sewer",
                    "name": "Isolate",
                    "rules": [
                        {
                            "action": "BLOCK_ALERT",
                            "application_path": "*",
                            "direction": "BOTH",
                            "enabled": True,
                            "local_ip_address": "10.29.99.1",
                            "local_port_ranges": "*",
                            "name": "BlockIRC",
                            "protocol": "TCP",
                            "remote_ip_address": "26.2.0.74",
                            "remote_port_ranges": "6667",
                            "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                            "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                            "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
                }
            ],
            "default_rule": {
                "action": "ALLOW",
                "default_rule_access_check_guid": "e6da6ec1-2e04-4fe7-a864-c4db940510c3",
                "default_rule_inbound_event_check_guid": "6d38dce5-d2b2-4572-b61c-3d0bbefddbdb",
                "default_rule_outbound_event_check_guid": "26257374-2e78-46ea-b252-1e9916a885d4"
            },
            "enable_host_based_firewall": False
        }
    }
]

HBFW_REMOVE_RULE_PUT_RESPONSE = {
    "successful": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...]",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
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
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                                "test_mode": True
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    },
                    {
                        "description": "IRC is a sewer",
                        "name": "Isolate",
                        "rules": [
                            {
                                "action": "BLOCK_ALERT",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "BlockIRC",
                                "protocol": "TCP",
                                "remote_ip_address": "26.2.0.74",
                                "remote_port_ranges": "6667",
                                "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                                "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                                "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
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
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    },
                    {
                        "description": "IRC is a sewer",
                        "name": "Isolate",
                        "rules": [
                            {
                                "action": "BLOCK_ALERT",
                                "application_path": "*",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "BlockIRC",
                                "protocol": "TCP",
                                "remote_ip_address": "26.2.0.74",
                                "remote_port_ranges": "6667",
                                "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                                "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                                "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "e6da6ec1-2e04-4fe7-a864-c4db940510c3",
                    "default_rule_inbound_event_check_guid": "6d38dce5-d2b2-4572-b61c-3d0bbefddbdb",
                    "default_rule_outbound_event_check_guid": "26257374-2e78-46ea-b252-1e9916a885d4"
                },
                "enable_host_based_firewall": False
            }
        }
    ],
    "failed": []
}

HBFW_REMOVE_RULE_GROUP_PUT_REQUEST = [
    {
        "id": "df181779-f623-415d-879e-91c40246535d",
        "parameters": {
            "rule_groups": [
                {
                    "description": "Whatever",
                    "name": "Crapco_firewall",
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
                            "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                            "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                            "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
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
                            "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                            "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                            "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                            "test_mode": False
                        }
                    ],
                    "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                }
            ],
            "default_rule": {
                "action": "ALLOW",
                "default_rule_access_check_guid": "e6da6ec1-2e04-4fe7-a864-c4db940510c3",
                "default_rule_inbound_event_check_guid": "6d38dce5-d2b2-4572-b61c-3d0bbefddbdb",
                "default_rule_outbound_event_check_guid": "26257374-2e78-46ea-b252-1e9916a885d4"
            },
            "enable_host_based_firewall": False
        }
    }
]

HBFW_REMOVE_RULE_GROUP_PUT_RESPONSE = {
    "successful": [
        {
            "id": "df181779-f623-415d-879e-91c40246535d",
            "name": "Host Based Firewall",
            "description": "These are the Host based Firewall Rules which will be executed by the sensor. [...]",
            "inherited_from": "",
            "category": "host_based_firewall",
            "parameters": {
                "rulesets": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
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
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
                                "test_mode": True
                            },
                            {
                                "action": "BLOCK",
                                "application_path": "C:\\DOOM\\DOOM.EXE",
                                "direction": "BOTH",
                                "enabled": True,
                                "local_ip_address": "10.29.99.1",
                                "local_port_ranges": "*",
                                "name": "DoomyDoomsofDoom",
                                "protocol": "TCP",
                                "remote_ip_address": "199.201.128.1",
                                "remote_port_ranges": "666",
                                "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                                "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                                "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    }
                ],
                "rule_groups": [
                    {
                        "description": "Whatever",
                        "name": "Crapco_firewall",
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
                                "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                                "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                                "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
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
                                "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                                "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                                "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                                "test_mode": False
                            }
                        ],
                        "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
                    }
                ],
                "default_rule": {
                    "action": "ALLOW",
                    "default_rule_access_check_guid": "e6da6ec1-2e04-4fe7-a864-c4db940510c3",
                    "default_rule_inbound_event_check_guid": "6d38dce5-d2b2-4572-b61c-3d0bbefddbdb",
                    "default_rule_outbound_event_check_guid": "26257374-2e78-46ea-b252-1e9916a885d4"
                },
                "enable_host_based_firewall": False
            }
        }
    ],
    "failed": []
}

HBFW_COPY_RULES_PUT_REQUEST = {
    "target_policy_ids": [601, 65536, 344],
    "parameters": {
        "rule_groups": [
            {
                "description": "Whatever",
                "name": "Crapco_firewall",
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
                        "rule_access_check_guid": "935477b8-997a-4476-8160-9179840d9892",
                        "rule_inbound_event_check_guid": "203d0685-04a6-49d8-bd9b-20ddda2c6c73",
                        "rule_outbound_event_check_guid": "16b8a622-a6d0-4873-8197-2974295c0f47",
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
                        "rule_access_check_guid": "28acfcac-7891-423d-9e99-d887aa4662fc",
                        "rule_inbound_event_check_guid": "01e26bc9-7729-4c0d-a550-f63a865b8c9f",
                        "rule_outbound_event_check_guid": "b9b625eb-1599-4f7d-b852-0f12db6c5a19",
                        "test_mode": False
                    }
                ],
                "ruleset_id": "fa3f7254-6d50-4ebf-aca6-d617bcd644b9"
            },
            {
                "description": "IRC is a sewer",
                "name": "Isolate",
                "rules": [
                    {
                        "action": "BLOCK_ALERT",
                        "application_path": "*",
                        "direction": "BOTH",
                        "enabled": True,
                        "local_ip_address": "10.29.99.1",
                        "local_port_ranges": "*",
                        "name": "BlockIRC",
                        "protocol": "TCP",
                        "remote_ip_address": "26.2.0.74",
                        "remote_port_ranges": "6667",
                        "rule_access_check_guid": "b1454c18-f08c-419a-9b57-186c25aa6c9d",
                        "rule_inbound_event_check_guid": "b80e9216-5f9f-4e9a-9bcb-79a5af78d976",
                        "rule_outbound_event_check_guid": "765cdf79-4ff9-419c-9775-abb18e6f6518",
                        "test_mode": False
                    }
                ],
                "ruleset_id": "cc7b30e8-b0e5-4253-96e9-93d345fbe642"
            }
        ]
    }
}

HBFW_COPY_RULES_PUT_RESPONSE = {
    "failed_policy_ids": [344],
    "num_applied": 3,
    "message": "This is a message",
    "success": True
}

HBFW_EXPORT_RULE_CONFIGS_RESPONSE = [
    {
        "policy_name": "Crapco",
        "rule_group_name": "Crapco_firewall",
        "rule_group_description": "Whatever",
        "rule_group_rank": "1",
        "rule_group_enabled": "true",
        "rule_rank": "1",
        "rule_enabled": True,
        "action": "ALLOW",
        "application_path": "*",
        "direction": "IN",
        "local_ip": "1.2.3.4",
        "local_port": "1234",
        "remote_ip": "5.6.7.8",
        "remote_port": "5678",
        "protocol": "TCP"
    },
    {
        "policy_name": "Crapco",
        "rule_group_name": "Crapco_firewall",
        "rule_group_description": "Whatever",
        "rule_group_rank": "1",
        "rule_group_enabled": "true",
        "rule_rank": "2",
        "rule_enabled": True,
        "action": "BLOCK",
        "application_path": "C:\\DOOM\\DOOM.EXE",
        "direction": "BOTH",
        "local_ip": "10.29.99.1",
        "local_port": "*",
        "remote_ip": "199.201.128.1",
        "remote_port": "666",
        "protocol": "TCP"
    },
    {
        "policy_name": "Crapco",
        "rule_group_name": "Isolate",
        "rule_group_description": "IRC is a sewer",
        "rule_group_rank": "2",
        "rule_group_enabled": "true",
        "rule_rank": "1",
        "rule_enabled": True,
        "action": "BLOCK_ALERT",
        "application_path": "*",
        "direction": "BOTH",
        "local_ip": "10.29.99.1",
        "local_port": "*",
        "remote_ip": "26.2.0.74",
        "remote_port": "6667",
        "protocol": "TCP"
    },
    {
        "policy_name": "Crapco",
        "rule_group_rank": "3",
        "rule_group_enabled": "true",
        "rule_rank": "1",
        "rule_enabled": True,
        "action": "ALLOW",
        "application_path": "*",
        "direction": "BOTH",
        "local_ip": "*",
        "local_port": "*",
        "remote_ip": "*",
        "remote_port": "*",
        "protocol": "ANY"
    }
]

HBFW_EXPORT_RULE_CONFIGS_RESPONSE_CSV = """Policy Name,Rule Group Name,Rule Group Description,Rule Group Rank,...
Crapco,Crapco_firewall,Whatever,1,true,1,true,ALLOW,*,IN,1.2.3.4,1234,5.6.7.8,5678,TCP
Crapco,Crapco_firewall,Whatever,1,true,2,true,BLOCK,C:\\DOOM\\DOOM.EXE,BOTH,10.29.99.1,*,199.201.128.1,666,TCP
Crapco,Isolate,IRC is a sewer,2,true,1,true,BLOCK_ALERT,*,BOTH,10.29.99.1,*,26.2.0.74,6667,TCP
Crapco,,,3,true,1,true,ALLOW,*,BOTH,*,*,*,*,ANY
"""
