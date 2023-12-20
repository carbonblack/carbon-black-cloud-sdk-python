"""Mock responses for device queries."""

GET_DEVICE_RESP = {
    "activation_code": None,
    "activation_code_expiry_time": "2019-12-12T16:23:14.291Z",
    "ad_group_id": 0,
    "appliance_name": None,
    "appliance_uuid": None,
    "asset_group": [
        {
            "id": "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
            "name": "Existing Group",
            "membership_type": "MANUAL"
        },
        {
            "id": "509f437f-6b9a-4b8e-996e-9183b35f9069",
            "name": "Another Group",
            "membership_type": "DYNAMIC"
        }
    ],
    "av_ave_version": "8.3.62.44",
    "av_engine": "4.13.0.207-ave.8.3.62.44:avpack.8.5.0.66:vdf.8.18.9.10 (20200826)",
    "av_last_scan_time": None,
    "av_master": False,
    "av_pack_version": "8.5.0.66",
    "av_product_version": "4.13.0.207",
    "av_status": [
        "AV_ACTIVE",
        "ONDEMAND_SCAN_DISABLED"
    ],
    "av_update_servers": None,
    "av_vdf_version": "8.18.9.10 (20200826)",
    "cluster_name": None,
    "current_sensor_policy_name": "policy-restrictive",
    "datacenter_name": None,
    "deployment_type": "ENDPOINT",
    "deregistered_time": None,
    "device_meta_data_item_list": [],
    "device_owner_id": 93474,
    "email": "email@example.org",
    "esx_host_name": None,
    "esx_host_uuid": None,
    "first_name": None,
    "id": 98765,
    "last_contact_time": "2020-08-26T21:05:42.518Z",
    "last_device_policy_changed_time": "2019-12-05T16:24:23.216Z",
    "last_device_policy_requested_time": "2020-06-23T00:43:28.164Z",
    "last_external_ip_address": "192.168.0.1",
    "last_internal_ip_address": "192.168.0.1",
    "last_location": "OFFSITE",
    "last_name": None,
    "last_policy_updated_time": None,
    "last_reported_time": "2020-08-26T18:29:37.148Z",
    "last_reset_time": None,
    "last_shutdown_time": None,
    "linux_kernel_version": None,
    "login_user_name": "email@example.org",
    "mac_address": "000000000000",
    "middle_name": None,
    "name": "Win7x64",
    "organization_id": 654,
    "organization_name": "org-name.example.com",
    "os": "WINDOWS",
    "os_version": "Windows 7 x64 SP: 1",
    "passive_mode": False,
    "policy_id": 11200,
    "policy_name": "policy-restrictive",
    "policy_override": True,
    "quarantined": False,
    "registered_time": "2019-12-05T16:23:14.320Z",
    "scan_last_action_time": None,
    "scan_last_complete_time": None,
    "scan_status": None,
    "sensor_kit_type": "WINDOWS",
    "sensor_out_of_date": True,
    "sensor_pending_update": False,
    "sensor_states": [
        "ACTIVE",
        "LIVE_RESPONSE_NOT_RUNNING",
        "LIVE_RESPONSE_NOT_KILLED",
        "LIVE_RESPONSE_ENABLED",
        "SECURITY_CENTER_OPTLN_DISABLED"
    ],
    "sensor_version": "3.6.0.1201",
    "status": "REGISTERED",
    "target_priority": "MEDIUM",
    "uninstall_code": "ABCDEF",
    "vcenter_name": None,
    "vcenter_uuid": "11eb-bcbc",
    "vdi_base_device": None,
    "virtual_machine": False,
    "virtualization_provider": "UNKNOWN",
    "vm_ip": None,
    "vm_name": None,
    "vm_uuid": None,
    "vuln_score": 0.0,
    "vuln_severity": None,
    "windows_platform": None
}

GET_DEVICE_RESP_NO_VCENTER = {
    "activation_code": None,
    "activation_code_expiry_time": "2019-12-12T16:23:14.291Z",
    "ad_group_id": 0,
    "appliance_name": None,
    "appliance_uuid": None,
    "asset_group": [
        {
            "id": "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
            "name": "Existing Group",
            "membership_type": "MANUAL"
        },
        {
            "id": "509f437f-6b9a-4b8e-996e-9183b35f9069",
            "name": "Another Group",
            "membership_type": "DYNAMIC"
        }
    ],
    "av_ave_version": "8.3.62.44",
    "av_engine": "4.13.0.207-ave.8.3.62.44:avpack.8.5.0.66:vdf.8.18.9.10 (20200826)",
    "av_last_scan_time": None,
    "av_master": False,
    "av_pack_version": "8.5.0.66",
    "av_product_version": "4.13.0.207",
    "av_status": [
        "AV_ACTIVE",
        "ONDEMAND_SCAN_DISABLED"
    ],
    "av_update_servers": None,
    "av_vdf_version": "8.18.9.10 (20200826)",
    "cluster_name": None,
    "current_sensor_policy_name": "policy-restrictive",
    "datacenter_name": None,
    "deployment_type": "ENDPOINT",
    "deregistered_time": None,
    "device_meta_data_item_list": [],
    "device_owner_id": 93474,
    "email": "email@example.org",
    "esx_host_name": None,
    "esx_host_uuid": None,
    "first_name": None,
    "id": 98765,
    "last_contact_time": "2020-08-26T21:05:42.518Z",
    "last_device_policy_changed_time": "2019-12-05T16:24:23.216Z",
    "last_device_policy_requested_time": "2020-06-23T00:43:28.164Z",
    "last_external_ip_address": "192.168.0.1",
    "last_internal_ip_address": "192.168.0.1",
    "last_location": "OFFSITE",
    "last_name": None,
    "last_policy_updated_time": None,
    "last_reported_time": "2020-08-26T18:29:37.148Z",
    "last_reset_time": None,
    "last_shutdown_time": None,
    "linux_kernel_version": None,
    "login_user_name": "email@example.org",
    "mac_address": "000000000000",
    "middle_name": None,
    "name": "Win7x64",
    "organization_id": 654,
    "organization_name": "org-name.example.com",
    "os": "WINDOWS",
    "os_version": "Windows 7 x64 SP: 1",
    "passive_mode": False,
    "policy_id": 11200,
    "policy_name": "policy-restrictive",
    "policy_override": True,
    "quarantined": False,
    "registered_time": "2019-12-05T16:23:14.320Z",
    "scan_last_action_time": None,
    "scan_last_complete_time": None,
    "scan_status": None,
    "sensor_kit_type": "WINDOWS",
    "sensor_out_of_date": True,
    "sensor_pending_update": False,
    "sensor_states": [
        "ACTIVE",
        "LIVE_RESPONSE_NOT_RUNNING",
        "LIVE_RESPONSE_NOT_KILLED",
        "LIVE_RESPONSE_ENABLED",
        "SECURITY_CENTER_OPTLN_DISABLED"
    ],
    "sensor_version": "3.6.0.1201",
    "status": "REGISTERED",
    "target_priority": "MEDIUM",
    "uninstall_code": "ABCDEF",
    "vcenter_name": None,
    "vcenter_uuid": None,
    "vdi_base_device": None,
    "virtual_machine": False,
    "virtualization_provider": "UNKNOWN",
    "vm_ip": None,
    "vm_name": None,
    "vm_uuid": None,
    "vuln_score": 0.0,
    "vuln_severity": None,
    "windows_platform": None
}

POST_DEVICE_SEARCH_RESP = {
    "results": [
        {
            "activation_code": None,
            "activation_code_expiry_time": "2019-12-12T16:23:14.291Z",
            "ad_group_id": 0,
            "appliance_name": None,
            "appliance_uuid": None,
            "asset_group": [
                {
                    "id": "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
                    "name": "Existing Group",
                    "membership_type": "MANUAL"
                },
                {
                    "id": "509f437f-6b9a-4b8e-996e-9183b35f9069",
                    "name": "Another Group",
                    "membership_type": "DYNAMIC"
                }
            ],
            "av_ave_version": "8.3.62.44",
            "av_engine": "4.13.0.207-ave.8.3.62.44:avpack.8.5.0.66:vdf.8.18.9.10 (20200826)",
            "av_last_scan_time": None,
            "av_master": False,
            "av_pack_version": "8.5.0.66",
            "av_product_version": "4.13.0.207",
            "av_status": [
                "AV_ACTIVE",
                "ONDEMAND_SCAN_DISABLED"
            ],
            "av_update_servers": None,
            "av_vdf_version": "8.18.9.10 (20200826)",
            "cluster_name": None,
            "current_sensor_policy_name": "policy-restrictive",
            "datacenter_name": None,
            "deployment_type": "ENDPOINT",
            "deregistered_time": None,
            "device_meta_data_item_list": [
                {
                    "key_name": "OS_MAJOR_VERSION",
                    "key_value": "Windows",
                    "position": 0
                },
                {
                    "key_name": "SUBNET",
                    "key_value": "192.10.33",
                    "position": 0
                }
            ],
            "device_owner_id": 93474,
            "email": "email@example.org",
            "esx_host_name": None,
            "esx_host_uuid": None,
            "first_name": None,
            "id": 98765,
            "last_contact_time": "2020-08-26T21:25:19.513Z",
            "last_device_policy_changed_time": "2019-12-05T16:24:23.216Z",
            "last_device_policy_requested_time": "2020-06-23T00:43:28.164Z",
            "last_external_ip_address": "192.168.0.1",
            "last_internal_ip_address": "192.168.0.1",
            "last_location": "OFFSITE",
            "last_name": None,
            "last_policy_updated_time": "2020-01-06T22:55:56.218Z",
            "last_reported_time": "2020-08-26T18:29:37.148Z",
            "last_reset_time": None,
            "last_shutdown_time": None,
            "linux_kernel_version": None,
            "login_user_name": "email@example.org",
            "mac_address": "000000000000",
            "middle_name": None,
            "name": "Win7x64",
            "organization_id": 654,
            "organization_name": "org-name.example.com",
            "os": "WINDOWS",
            "os_version": "Windows 7 x64 SP: 1",
            "passive_mode": False,
            "policy_id": 11200,
            "policy_name": "policy-restrictive",
            "policy_override": True,
            "quarantined": False,
            "registered_time": "2019-12-05T16:23:14.320Z",
            "scan_last_action_time": None,
            "scan_last_complete_time": None,
            "scan_status": None,
            "sensor_kit_type": "WINDOWS",
            "sensor_out_of_date": True,
            "sensor_pending_update": False,
            "sensor_states": [
                "ACTIVE",
                "LIVE_RESPONSE_NOT_RUNNING",
                "LIVE_RESPONSE_NOT_KILLED",
                "LIVE_RESPONSE_ENABLED",
                "SECURITY_CENTER_OPTLN_DISABLED"
            ],
            "sensor_version": "3.6.0.1201",
            "status": "REGISTERED",
            "target_priority": "MEDIUM",
            "uninstall_code": "ABCDEF",
            "vcenter_name": None,
            "vcenter_uuid": None,
            "vdi_base_device": None,
            "virtual_machine": False,
            "virtualization_provider": "UNKNOWN",
            "vm_ip": None,
            "vm_name": None,
            "vm_uuid": None,
            "vuln_score": 0.0,
            "vuln_severity": None,
            "windows_platform": None
        }
    ],
    "num_found": 1
}

FACET_RESPONSE = {
    "results": [
        {
            "field": "policy_id",
            "values": [
                {
                    "total": 788,
                    "id": "6525",
                    "name": "6525"
                },
                {
                    "total": 25,
                    "id": "7691",
                    "name": "7691"
                },
                {
                    "total": 9,
                    "id": "68727",
                    "name": "68727"
                },
                {
                    "total": 7,
                    "id": "65066",
                    "name": "65066"
                },
                {
                    "total": 4,
                    "id": "69390",
                    "name": "69390"
                },
                {
                    "total": 1,
                    "id": "35704",
                    "name": "35704"
                },
                {
                    "total": 1,
                    "id": "6527",
                    "name": "6527"
                },
                {
                    "total": 1,
                    "id": "71498",
                    "name": "71498"
                },
                {
                    "total": 1,
                    "id": "78483",
                    "name": "78483"
                },
                {
                    "total": 1,
                    "id": "86029",
                    "name": "86029"
                }
            ]
        }
    ]
}

FACET_INIT_1 = {
    "field": "policy_id",
    "values": [
        {
            "total": 9,
            "id": "68727",
            "name": "68727"
        }
    ]
}

FACET_INIT_2 = {
    "field": "status",
    "values": [
        {
            "total": 115,
            "id": "ACTIVE",
            "name": "ACTIVE"
        }
    ]
}

FACET_INIT_3 = {
    "field": "os",
    "values": [
        {
            "total": 81,
            "id": "linux",
            "name": "linux"
        }
    ]
}

FACET_INIT_4 = {
    "field": "ad_group_id",
    "values": [
        {
            "total": 2,
            "id": "955",
            "name": "955"
        }
    ]
}

FACET_INIT_5 = {
    "field": "cloud_provider_account_id",
    "values": [
        {
            "total": 2,
            "id": "303",
            "name": "303"
        }
    ]
}

FACET_INIT_6 = {
    "field": "auto_scaling_group_name",
    "values": [
        {
            "total": 2,
            "id": "ARGON",
            "name": "ARGON"
        }
    ]
}

FACET_INIT_7 = {
    "field": "virtual_private_cloud_id",
    "values": [
        {
            "total": 2,
            "id": "65534",
            "name": "65534"
        }
    ]
}

ASSET_GROUPS_RESPONSE_1 = {
    "98765": [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ],
    "3031": [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
        "91366048-04dd-4034-baf0-b768128fe433",
        "4f0a24f8-002b-4fe7-aaa6-6844bae2639e"
    ],
    "1777": [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
        "297b9b31-3737-4831-9dd1-cf47770df3e5"
    ]
}

ASSET_GROUPS_OUTPUT_1 = {
    98765: [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ],
    3031: [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
        "91366048-04dd-4034-baf0-b768128fe433",
        "4f0a24f8-002b-4fe7-aaa6-6844bae2639e"
    ],
    1777: [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
        "297b9b31-3737-4831-9dd1-cf47770df3e5"
    ]
}

ASSET_GROUPS_RESPONSE_2 = {
    "98765": [
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ],
    "3031": [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
    ],
    "1777": [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
    ]
}

ASSET_GROUPS_OUTPUT_2 = {
    98765: [
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ],
    3031: [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
    ],
    1777: [
        "509f437f-6b9a-4b8e-996e-9183b35f9069",
    ]
}

ASSET_GROUPS_RESPONSE_3 = {
    "98765": [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
    ],
    "3031": [
        "91366048-04dd-4034-baf0-b768128fe433",
        "4f0a24f8-002b-4fe7-aaa6-6844bae2639e"
    ],
    "1777": [
        "297b9b31-3737-4831-9dd1-cf47770df3e5"
    ]
}

ASSET_GROUPS_OUTPUT_3 = {
    98765: [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
    ],
    3031: [
        "91366048-04dd-4034-baf0-b768128fe433",
        "4f0a24f8-002b-4fe7-aaa6-6844bae2639e"
    ],
    1777: [
        "297b9b31-3737-4831-9dd1-cf47770df3e5"
    ]
}

ASSET_GROUPS_RESPONSE_SINGLE = {
    "98765": [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ]
}

ASSET_GROUPS_OUTPUT_SINGLE = {
    98765: [
        "db416fa2-d5f2-4fb5-8a5e-cd89f6ecda16",
        "509f437f-6b9a-4b8e-996e-9183b35f9069"
    ]
}
