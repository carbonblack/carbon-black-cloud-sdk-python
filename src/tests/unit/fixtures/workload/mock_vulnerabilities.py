"""Mock responses for vulnerabilties queries."""

GET_VULNERABILITY_SUMMARY_ORG_LEVEL = {
    "monitored_assets": 13,
    "severity_summary": {
        "ALL": {
            "vuln_assets_count": 13,
            "vuln_count": 7616,
            "total_vuln_count": 9856,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 12,
                    "total_vuln_count": 9123,
                    "os_vuln_count": 4143,
                    "products_vuln_count": 2740
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 733,
                    "os_vuln_count": 717,
                    "products_vuln_count": 16
                }
            }
        },
        "MODERATE": {
            "vuln_assets_count": 13,
            "vuln_count": 391,
            "total_vuln_count": 505,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 12,
                    "total_vuln_count": 449,
                    "os_vuln_count": 164,
                    "products_vuln_count": 171
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 56,
                    "os_vuln_count": 56,
                    "products_vuln_count": 0
                }
            }
        },
        "LOW": {
            "vuln_assets_count": 13,
            "vuln_count": 7160,
            "total_vuln_count": 9270,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 12,
                    "total_vuln_count": 8605,
                    "os_vuln_count": 3946,
                    "products_vuln_count": 2549
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 665,
                    "os_vuln_count": 650,
                    "products_vuln_count": 15
                }
            }
        },
        "IMPORTANT": {
            "vuln_assets_count": 13,
            "vuln_count": 60,
            "total_vuln_count": 76,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 12,
                    "total_vuln_count": 66,
                    "os_vuln_count": 30,
                    "products_vuln_count": 20
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 10,
                    "os_vuln_count": 9,
                    "products_vuln_count": 1
                }
            }
        },
        "CRITICAL": {
            "vuln_assets_count": 2,
            "vuln_count": 5,
            "total_vuln_count": 5,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 3,
                    "os_vuln_count": 3,
                    "products_vuln_count": 0
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 2,
                    "os_vuln_count": 2,
                    "products_vuln_count": 0
                }
            }
        }
    }
}

GET_VULNERABILITY_SUMMARY_ORG_LEVEL_PER_SEVERITY = {
    "monitored_assets": 13,
    "severity_summary": {
        "CRITICAL": {
            "vuln_assets_count": 13,
            "vuln_count": 391,
            "total_vuln_count": 505,
            "asset_summary": {
                "LINUX": {
                    "monitored_assets": 12,
                    "vuln_assets_count": 12,
                    "total_vuln_count": 449,
                    "os_vuln_count": 164,
                    "products_vuln_count": 171
                },
                "WINDOWS": {
                    "monitored_assets": 1,
                    "vuln_assets_count": 1,
                    "total_vuln_count": 56,
                    "os_vuln_count": 56,
                    "products_vuln_count": 0
                }
            }
        }
    }
}

GET_ASSET_VIEW_VUL_RESP = {
    "num_found": 2,
    "results": [
        {
            "device_id": 7330223,
            "type": "WORKLOAD",
            "vm_id": "123",
            "name": "jdoe-windows_2012",
            "os_info": {
                "os_type": "WINDOWS",
                "os_name": "Microsoft Windows Server 2012 Standard",
                "os_version": "6.2.9200",
                "os_arch": "64-bit"
            },
            "vuln_count": 733,
            "severity": "CRITICAL",
            "highest_risk_score": 10.0,
            "last_sync_ts": "2020-10-30T16:00:52.897987Z",
            "sync_type": "SCHEDULED",
            "sync_status": "COMPLETED",
            "cve_ids": ["CVE-2014-4650"]
        },
        {
            "device_id": 7655988,
            "type": "WORKLOAD",
            "vm_id": "vm-34",
            "name": "cwp-windows_2012_r2",
            "os_info": {
                "os_type": "WINDOWS",
                "os_name": "Microsoft Windows Server 2012 R2 Standard",
                "os_version": "6.3.9600",
                "os_arch": "64-bit"
            },
            "vuln_count": 758,
            "severity": "LOW",
            "highest_risk_score": 10.0,
            "last_sync_ts": "2020-10-30T17:44:43.902389Z",
            "sync_type": "MANUAL",
            "sync_status": "COMPLETED",
            "cve_ids": ["CVE-2014-4650"]
        }
    ]
}

GET_AFFECTED_ASSETS_SPECIFIC_VULNERABILITY = {
    "num_found": 1,
    "results": [{
        "device_id": 98765,
        "vm_id": "123",
        "name": "jdoe-windows_2012"
    }]
}

GET_VULNERABILITY_RESP = {
    "num_found": 1,
    "results": [
        {
            "os_product_id": "90_5372",
            "category": "APP",
            "os_info": {
                "os_type": "CENTOS",
                "os_name": "CentOS Linux",
                "os_version": "7.1.1503",
                "os_arch": "x86_64"
            },
            "product_info": {
                "vendor": "CentOS",
                "product": "python-libs",
                "version": "2.7.5",
                "release": "16.el7",
                "arch": "x86_64"
            },
            "vuln_info": {
                "cve_id": "CVE-2014-4650",
                "cve_description": "The CGIHTTPServer module in Python 2.7.5 and 3.3.4 does not properly handle...",
                "risk_meter_score": 4.9,
                "severity": "MODERATE",
                "fixed_by": "0:2.7.5-34.el7",
                "solution": None,
                "created_at": "2020-02-20T17:15:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2014-4650",
                "cvss_access_complexity": "Low",
                "cvss_access_vector": "Local access",
                "cvss_authentication": "None required",
                "cvss_availability_impact": "Partial",
                "cvss_confidentiality_impact": "None",
                "cvss_integrity_impact": "None",
                "easily_exploitable": False,
                "malware_exploitable": False,
                "active_internet_breach": False,
                "cvss_exploit_subscore": 3.9,
                "cvss_impact_subscore": 2.9,
                "cvss_vector": "AV:L/AC:L/Au:N/C:N/I:N/A:P/E:U/RL:OF/RC:C",
                "cvss_v3_exploit_subscore": 3.9,
                "cvss_v3_impact_subscore": 2.9,
                "cvss_v3_vector": "CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
                "cvss_score": 3.9,
                "cvss_v3_score": 3.9
            },
            "device_count": 1,
            "affected_assets": [
                "jdoe-windows_2012"
            ]
        }
    ]
}

GET_VULNERABILITY_RESP_MULTIPLE_SAME_CVE = {
    "num_found": 1,
    "results": [
        {
            "os_product_id": "90_5372",
            "category": "APP",
            "os_info": {
                "os_type": "CENTOS",
                "os_name": "CentOS Linux",
                "os_version": "7.1.1503",
                "os_arch": "x86_64"
            },
            "product_info": {
                "vendor": "CentOS",
                "product": "python-libs",
                "version": "2.7.5",
                "release": "16.el7",
                "arch": "x86_64"
            },
            "vuln_info": {
                "cve_id": "CVE-2014-4650",
                "cve_description": "The CGIHTTPServer module in Python 2.7.5 and 3.3.4 does not properly handle...",
                "risk_meter_score": 4.9,
                "severity": "MODERATE",
                "fixed_by": "0:2.7.5-34.el7",
                "solution": None,
                "created_at": "2020-02-20T17:15:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2014-4650",
                "cvss_access_complexity": "Low",
                "cvss_access_vector": "Local access",
                "cvss_authentication": "None required",
                "cvss_availability_impact": "Partial",
                "cvss_confidentiality_impact": "None",
                "cvss_integrity_impact": "None",
                "easily_exploitable": False,
                "malware_exploitable": False,
                "active_internet_breach": False,
                "cvss_exploit_subscore": 3.9,
                "cvss_impact_subscore": 2.9,
                "cvss_vector": "AV:L/AC:L/Au:N/C:N/I:N/A:P/E:U/RL:OF/RC:C",
                "cvss_v3_exploit_subscore": 3.9,
                "cvss_v3_impact_subscore": 2.9,
                "cvss_v3_vector": "CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
                "cvss_score": 3.9,
                "cvss_v3_score": 3.9
            },
            "device_count": 1,
            "affected_assets": [
                "jdoe-windows_2012"
            ]
        },
        {
            "os_product_id": "89_1234",
            "category": "APP",
            "os_info": {
                "os_type": "CENTOS",
                "os_name": "CentOS Linux",
                "os_version": "7.2.1604",
                "os_arch": "x86_64"
            },
            "product_info": {
                "vendor": "CentOS",
                "product": "python-libs",
                "version": "3.0.1",
                "release": "12.el3",
                "arch": "x86_64"
            },
            "vuln_info": {
                "cve_id": "CVE-2014-4650",
                "cve_description": "The CGIHTTPServer module in Python 2.7.5 and 3.3.4 does not properly handle...",
                "risk_meter_score": 4.9,
                "severity": "MODERATE",
                "fixed_by": "0:2.7.5-34.el7",
                "solution": None,
                "created_at": "2020-02-20T17:15:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2014-4650",
                "cvss_access_complexity": "Low",
                "cvss_access_vector": "Local access",
                "cvss_authentication": "None required",
                "cvss_availability_impact": "Partial",
                "cvss_confidentiality_impact": "None",
                "cvss_integrity_impact": "None",
                "easily_exploitable": False,
                "malware_exploitable": False,
                "active_internet_breach": False,
                "cvss_exploit_subscore": 3.9,
                "cvss_impact_subscore": 2.9,
                "cvss_vector": "AV:L/AC:L/Au:N/C:N/I:N/A:P/E:U/RL:OF/RC:C",
                "cvss_v3_exploit_subscore": 3.9,
                "cvss_v3_impact_subscore": 2.9,
                "cvss_v3_vector": "CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
                "cvss_score": 3.9,
                "cvss_v3_score": 3.9
            },
            "device_count": 1,
            "affected_assets": [
                "jdoe-linux"
            ]
        }
    ]
}

GET_DEVICE_VULNERABILITY_SUMMARY_RESP = {
    "os_info": {
        "os_type": "CENTOS",
        "os_name": "CentOS Linux",
        "os_version": "7.1.1503",
        "os_arch": "x86_64"
    },
    "monitored": True,
    "os_compatible": True,
    "sensor_compatible": True,
    "sync_type": "SCHEDULED",
    "sync_status": "COMPLETED",
    "last_sync_ts": "2020-10-30T16:17:16.078363Z",
    "severity_counts": {
        "critical": 0,
        "important": 7,
        "moderate": 45,
        "low": 804
    }
}

GET_VULNERABILITY_RESP_MULTIPLE = {
    "num_found": 2,
    "results": [
        {
            "os_product_id": "90_5363",
            "category": "APP",
            "os_info": {
                "os_type": "CENTOS",
                "os_name": "CentOS Linux",
                "os_version": "7.1.1503",
                "os_arch": "x86_64"
            },
            "product_info": {
                "vendor": "CentOS",
                "product": "python",
                "version": "2.7.5",
                "release": "16.el7",
                "arch": "x86_64"
            },
            "vuln_info": {
                "cve_id": "CVE-2014-4650",
                "cve_description": "The CGIHTTPServer module in Python 2.7.5 and 3.3.4 does not properly handle ...",
                "risk_meter_score": 4.9,
                "severity": "MODERATE",
                "fixed_by": "0:2.7.5-34.el7",
                "solution": None,
                "created_at": "2020-02-20T17:15:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2014-4650",
                "cvss_access_complexity": None,
                "cvss_access_vector": None,
                "cvss_authentication": None,
                "cvss_availability_impact": None,
                "cvss_confidentiality_impact": None,
                "cvss_integrity_impact": None,
                "easily_exploitable": None,
                "malware_exploitable": None,
                "active_internet_breach": None,
                "cvss_exploit_subscore": None,
                "cvss_impact_subscore": None,
                "cvss_vector": None,
                "cvss_v3_exploit_subscore": None,
                "cvss_v3_impact_subscore": None,
                "cvss_v3_vector": None,
                "cvss_score": None,
                "cvss_v3_score": None
            },
            "device_count": 1,
            "affected_assets": None
        },
        {
            "os_product_id": "90_5372",
            "category": "APP",
            "os_info": {
                "os_type": "CENTOS",
                "os_name": "CentOS Linux",
                "os_version": "7.1.1503",
                "os_arch": "x86_64"
            },
            "product_info": {
                "vendor": "CentOS",
                "product": "python-libs",
                "version": "2.7.5",
                "release": "16.el7",
                "arch": "x86_64"
            },
            "vuln_info": {
                "cve_id": "CVE-2014-4650",
                "cve_description": "The CGIHTTPServer module in Python 2.7.5 and 3.3.4 does not properly handle...",
                "risk_meter_score": 4.9,
                "severity": "MODERATE",
                "fixed_by": "0:2.7.5-34.el7",
                "solution": None,
                "created_at": "2020-02-20T17:15:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2014-4650",
                "cvss_access_complexity": None,
                "cvss_access_vector": None,
                "cvss_authentication": None,
                "cvss_availability_impact": None,
                "cvss_confidentiality_impact": None,
                "cvss_integrity_impact": None,
                "easily_exploitable": None,
                "malware_exploitable": None,
                "active_internet_breach": None,
                "cvss_exploit_subscore": None,
                "cvss_impact_subscore": None,
                "cvss_vector": None,
                "cvss_v3_exploit_subscore": None,
                "cvss_v3_impact_subscore": None,
                "cvss_v3_vector": None,
                "cvss_score": None,
                "cvss_v3_score": None
            },
            "device_count": 1,
            "affected_assets": None
        }
    ]
}

REFRESH_DEVICE_RESP = {
    "created_at": "2021-02-09T07:29:09.179588Z",
    "device_id": 98765,
    "lq_query_id": "qwety",
    "lq_query_status": "ACTIVE",
    "org_key": "orgkey",
    "schedule_type": "LINUX_OS_PRODUCT",
    "updated_at": "2021-02-09T07:29:09.179589Z"
}

MOCK_WORKLOAD = {
    'activation_code': None,
    'activation_code_expiry_time': '2020-09-22T09:11:03.686Z',
    'ad_group_id': 0,
    'appliance_name': None,
    'appliance_uuid': '4cbd614e-87ae-43d7-92ee-0fc5d500c984',
    'av_ave_version': '8.3.62.188',
    'av_engine': '4.13.0.207-ave.8.3.62.188:avpack.8.5.2.2:vdf.8.18.30.88',
    'av_last_scan_time': None,
    'av_master': False,
    'av_pack_version': '8.5.2.2',
    'av_product_version': '4.13.0.207',
    'av_status': ['AV_ACTIVE', 'ONDEMAND_SCAN_DISABLED'],
    'av_update_servers': None,
    'av_vdf_version': '8.18.30.88',
    'cluster_name': 'jdoe-cluster',
    'current_sensor_policy_name': 'Standard',
    'datacenter_name': 'jdoe-datacenter',
    'deployment_type': 'WORKLOAD',
    'deregistered_time': None,
    'device_meta_data_item_list': [
        {
            'key_name': 'OS_MAJOR_VERSION',
            'key_value': 'Windows',
            'position': 0
        }, {
            'key_name': 'SUBNET',
            'key_value': '66.170.99',
            'position': 0
        }
    ],
    'device_owner_id': 6738868,
    'email': 'Administrator',
    'esx_host_name': '10.123.45.89',
    'esx_host_uuid': 'c8ba1342-1329-0c62-f465-abd0be8468c9',
    'first_name': None,
    'id': 98765,
    'last_contact_time': '2021-04-30T22:21:23.302Z',
    'last_device_policy_changed_time': None,
    'last_device_policy_requested_time': '2021-04-30T05:08:19.487Z',
    'last_external_ip_address': '66.77.99.88',
    'last_internal_ip_address': '10.123.92.123',
    'last_location': 'OFFSITE',
    'last_name': None,
    'last_policy_updated_time': '2021-02-17T12:26:52.655Z',
    'last_reported_time': '2021-04-30T21:41:08.406Z',
    'last_reset_time': None,
    'last_shutdown_time': None,
    'linux_kernel_version': None,
    'login_user_name': 'Window Manager\\DWM-1',
    'mac_address': '000000000000',
    'middle_name': None,
    'name': 'jdoe-windows_2012',
    'organization_id': 1923756,
    'organization_name': 'regression.com',
    'os': 'WINDOWS',
    'os_version': 'Server 2012 x64',
    'passive_mode': False,
    'policy_id': 7113786,
    'policy_name': 'Standard',
    'policy_override': False,
    'quarantined': False,
    'registered_time': '2021-04-28T18:46:04.929Z',
    'scan_last_action_time': None,
    'scan_last_complete_time': None,
    'scan_status': None,
    'sensor_kit_type': 'WINDOWS',
    'sensor_out_of_date': True,
    'sensor_pending_update': False,
    'sensor_states': ['ACTIVE', 'LIVE_RESPONSE_NOT_RUNNING', 'LIVE_RESPONSE_NOT_KILLED', 'LIVE_RESPONSE_ENABLED'],
    'sensor_version': '3.6.0.1628',
    'status': 'REGISTERED',
    'target_priority': 'MEDIUM',
    'uninstall_code': '4YI26YK7',
    'vcenter_host_url': '10.173.94.177',
    'vcenter_name': 'VMware vCenter Server 6.7.0 build-14368073',
    'vcenter_uuid': '450dfe53-d2b6-4718-97b0-5917ee79955a',
    'vdi_base_device': None,
    'virtual_machine': True,
    'virtualization_provider': 'VMW_ESX',
    'vm_ip': '10.173.92.123',
    'vm_name': 'sowmiyas-windows_2012',
    'vm_uuid': '501ee1d6-89bc-73d4-3bdb-49329ab09e6d',
    'vulnerability_score': 10.0,
    'vulnerability_severity': 'CRITICAL',
    'windows_platform': None
}

MOCK_WORKLOAD_RESP = {
    "results": [MOCK_WORKLOAD],
    "num_found": 1
}
