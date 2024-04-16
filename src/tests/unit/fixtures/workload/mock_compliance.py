"""Mock data for ComplianceBenchmark"""

SEARCH_COMPLIANCE_BENCHMARKS = {
    "num_found": 1,
    "results": [
        {
            "id": "eee5e491-9c31-4a38-84d8-50c9163ef559",
            "name": "CIS Compliance - Microsoft Windows Server",
            "version": "1.0.0.4",
            "os_family": "WINDOWS_SERVER",
            "bundle_name": "CIS Compliance - Microsoft Windows Server",
            "enabled": True,
            "type": "Default",
            "supported_os_info": [
                {
                    "os_metadata_id": "1",
                    "os_type": "WINDOWS",
                    "os_name": "Windows Server 2012 x64",
                    "cis_version": "2.3.0"
                },
                {
                    "os_metadata_id": "2",
                    "os_type": "WINDOWS",
                    "os_name": "Windows Server 2012 R2 x64",
                    "cis_version": "2.5.0"
                },
                {
                    "os_metadata_id": "3",
                    "os_type": "WINDOWS",
                    "os_name": "Windows Server 2016 x64",
                    "cis_version": "1.4.0"
                },
                {
                    "os_metadata_id": "4",
                    "os_type": "WINDOWS",
                    "os_name": "Windows Server 2019 x64",
                    "cis_version": "1.3.0"
                },
                {
                    "os_metadata_id": "71",
                    "os_type": "WINDOWS",
                    "os_name": "Windows Server 2022 x64",
                    "cis_version": "1.0.0"
                }
            ],
            "created_by": "CB_ADMIN",
            "updated_by": "user@vmware.com",
            "create_time": "2023-03-20T13:04:38.557369Z",
            "update_time": "2023-07-10T13:56:35.238166Z",
            "release_time": "2023-07-10T13:55:59.274881Z"
        }
    ]
}

COMPLIANCE_SCHEDULE = {
    "scan_schedule": "FREQ=WEEKLY;BYDAY=TU;BYHOUR=11;BYMINUTE=30;BYSECOND=0",
    "scan_timezone": "UTC"
}


GET_SECTIONS = [
    {
        "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
        "section_name": "Remote Assistance",
        "parent_id": "8C180BA0-EE6F-FB08-18F5-8F5FFC9A3FFF"
    },
    {
        "section_id": "0D69B5D9-B931-5ADB-EB04-F3775256B445",
        "section_name": "App runtime",
        "parent_id": "F072A0E3-24F6-B29C-6F2E-254F42CA6DF6"
    },
    {
        "section_id": "0FD8844A-C679-3F8F-748D-CDEAFF892CD4",
        "section_name": "System Services",
        "parent_id": None
    }
]

SEARCH_RULES = {
    "num_found": 4,
    "results": [
        {
            "id": "39D861A0-3631-442B-BF94-CC442C73C03E",
            "rule_name": "(L1) Ensure 'Configure Offer Remote Assistance' is set to 'Disabled'",
            "enabled": True,
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance"
        },
        {
            "id": "C5632571-24C4-430D-9CCE-542F30B6933A",
            "rule_name": "(L1) Ensure 'Configure Solicited Remote Assistance' is set to 'Disabled'",
            "enabled": True,
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance"
        },
        {
            "id": "6A530464-631B-43E4-AB8C-5B06A747B7D7",
            "rule_name": "(L1) Ensure 'Allow Microsoft accounts to be optional' is set to 'Enabled'",
            "enabled": True,
            "section_id": "0D69B5D9-B931-5ADB-EB04-F3775256B445",
            "section_name": "App runtime"
        },
        {
            "id": "1F65A756-338E-49A8-AA78-3EC07734B96D",
            "rule_name": "(L1) Ensure 'Print Spooler (Spooler)' is set to 'Disabled' (DC only)",
            "enabled": True,
            "section_id": "0FD8844A-C679-3F8F-748D-CDEAFF892CD4",
            "section_name": "System Services"
        }
    ]
}

GET_RULE = {
    "id": "39D861A0-3631-442B-BF94-CC442C73C03E",
    "rule_name": "(L1) Ensure 'Configure Offer Remote Assistance' is set to 'Disabled'",
    "enabled": True,
    "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
    "section_name": "Remote Assistance",
    "supported_os_info": [
        {
            "os_metadata_id": "1",
            "os_type": "WINDOWS",
            "os_name": "Windows Server 2012 x64",
            "cis_version": "2.3.0"
        },
        {
            "os_metadata_id": "2",
            "os_type": "WINDOWS",
            "os_name": "Windows Server 2012 R2 x64",
            "cis_version": "2.5.0"
        },
        {
            "os_metadata_id": "3",
            "os_type": "WINDOWS",
            "os_name": "Windows Server 2016 x64",
            "cis_version": "1.4.0"
        },
        {
            "os_metadata_id": "4",
            "os_type": "WINDOWS",
            "os_name": "Windows Server 2019 x64",
            "cis_version": "1.3.0"
        },
        {
            "os_metadata_id": "71",
            "os_type": "WINDOWS",
            "os_name": "Windows Server 2022 x64",
            "cis_version": "1.0.0"
        }
    ],
    "description": "This policy setting allows you to turn on or turn off Offer (Unsolicited) Remote Assistance on this"
    " computer.\n\nHelp desk and support personnel will not be able to proactively offer assistance, although they can"
    " still respond to user assistance requests.\n\nThe recommended state for this setting is: `Disabled`.",
    "rationale": "A user might be tricked and accept an unsolicited Remote Assistance offer from a malicious user.",
    "impact": "None - this is the default behavior.",
    "remediation": {
        "procedure": "To establish the recommended configuration via GP, set the following UI path to `Disabled`",
        "steps": "\n\n```\nComputer Configuration\\Policies\\Administrative Templates\\System\\Remote"
        " Assistance\\Configure Offer Remote Assistance\n```\n\n**Note"
    },
    "profile": [
        "Level 1 Domain Controller",
        "Level 1 Member Server"
    ]
}

RULE_COMPLIANCES = {
    "num_found": 2,
    "results": [
        {
            "rule_id": "39D861A0-3631-442B-BF94-CC442C73C03E",
            "rule_name": "(L1) Ensure 'Configure Offer Remote Assistance' is set to 'Disabled'",
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance",
            "compliant_assets": 1,
            "non_compliant_assets": 0,
            "profile": [
                "Level 1 Domain Controller",
                "Level 1 Member Server"
            ]
        },
        {
            "rule_id": "C5632571-24C4-430D-9CCE-542F30B6933A",
            "rule_name": "(L1) Ensure 'Configure Solicited Remote Assistance' is set to 'Disabled'",
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance",
            "compliant_assets": 1,
            "non_compliant_assets": 0,
            "profile": [
                "Level 1 Domain Controller",
                "Level 1 Member Server"
            ]
        }
    ]
}

DEVICE_SPECIFIC_RULE_COMPLIANCE = {
    "num_found": 2,
    "results": [
        {
            "id": "39D861A0-3631-442B-BF94-CC442C73C03E",
            "rule_name": "(L1) Ensure 'Configure Offer Remote Assistance' is set to 'Disabled'",
            "enabled": True,
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance",
            "compliance_result": True,
            "message": "Registry_Terminal_Services_fAllowUnsolicited=0"
        },
        {
            "id": "C5632571-24C4-430D-9CCE-542F30B6933A",
            "rule_name": "(L1) Ensure 'Configure Solicited Remote Assistance' is set to 'Disabled'",
            "enabled": True,
            "section_id": "0ABA0288-8A68-83AF-3BAE-A7F45167564B",
            "section_name": "Remote Assistance",
            "compliance_result": True,
            "message": "Registry_Terminal_Services_fAllowToGetHelp=0"
        }
    ]
}

RULE_COMPLIANCE_DEVICE_SEARCH = {
    "num_found": 1,
    "results": [
        {
            "device_id": 1,
            "device_name": "Example\\Win2022",
            "os_version": "Windows Server 2022 x64",
            "compliance_result": True
        }
    ]
}
