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

GET_ASSET_VIEW_VUL_SUMMARY_RESP = {
    "num_found": 2,
    "results": [
        {
            "os_product_id": "18_2517",
            "category": "APP",
            "os_info": {
                "os_type": "WINDOWS",
                "os_name": "Microsoft Windows Server 2012 R2 Standard",
                "os_version": "6.3.9600",
                "os_arch": "64-bit"
            },
            "product_info": {
                "vendor": "Python Software Foundation",
                "product": "Python 3.6.4 (64-bit)",
                "version": "3.6.4150.0",
                "release": None,
                "arch": ""
            },
            "vuln_info": {
                "cve_id": "CVE-2007-4559",
                "cve_description": "Directory traversal vulnerability in the (1) extract and (2) extractall functions",
                "risk_meter_score": 2.9,
                "severity": "LOW",
                "fixed_by": None,
                "solution": None,
                "created_at": "2007-08-28T01:17:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2007-4559",
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
            "os_product_id": "328_2517",
            "category": "APP",
            "os_info": {
                "os_type": "WINDOWS",
                "os_name": "Microsoft Windows Server 2019 Datacenter",
                "os_version": "10.0.17763",
                "os_arch": "64-bit"
            },
            "product_info": {
                "vendor": "Python Software Foundation",
                "product": "Python 3.6.4 (64-bit)",
                "version": "3.6.4150.0",
                "release": None,
                "arch": ""
            },
            "vuln_info": {
                "cve_id": "CVE-2007-4559",
                "cve_description": "Directory traversal vulnerability in the (1) extract and (2) extractall functions",
                "risk_meter_score": 2.9,
                "severity": "LOW",
                "fixed_by": None,
                "solution": None,
                "created_at": "2007-08-28T01:17:00Z",
                "nvd_link": "https://nvd.nist.gov/vuln/detail/CVE-2007-4559",
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

GET_ASSET_VIEW_VUL_RESP = {
    "num_found": 2,
    "results": [
        {
            "device_id": 7330223,
            "type": "WORKLOAD",
            "vm_id": "vm-32",
            "name": "shwetap-windows_2012-2",
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
            "cve_ids": None
        },
        {
            "device_id": 7655988,
            "type": "WORKLOAD",
            "vm_id": "vm-34",
            "name": "cwp-bucket-1-windows_2012_r2",
            "os_info": {
                "os_type": "WINDOWS",
                "os_name": "Microsoft Windows Server 2012 R2 Standard",
                "os_version": "6.3.9600",
                "os_arch": "64-bit"
            },
            "vuln_count": 758,
            "severity": "CRITICAL",
            "highest_risk_score": 10.0,
            "last_sync_ts": "2020-10-30T17:44:43.902389Z",
            "sync_type": "MANUAL",
            "sync_status": "COMPLETED",
            "cve_ids": None
        }
    ]
}

GET_ASSET_VIEW_VUL_ALL_SETS_RESP = {
    "num_found": 1,
    "results": [
        {
            "device_id": 7330223,
            "type": "WORKLOAD",
            "vm_id": "vm-32",
            "name": "shwetap-windows_2012-2",
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
            "cve_ids": None
        }
    ]
}

GET_AFFECTED_ASSETS_SPECIFIC_VULNERABILITY = {
    "num_found": 1,
    "results": [{
        "device_id": 98765,
        "vm_id": "vm-1",
        "name": "VM-1"
    }]
}

GET_VULNERABILITY_RESP = {
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

GET_DEVICE_VULNERABILITY_RESP = {
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
