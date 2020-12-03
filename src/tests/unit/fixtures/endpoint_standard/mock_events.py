"""Mock responses for event queries."""

EVENT_GET_HOSTNAME_RESP = {
    "latestTime": 0,
    "success": True,
    "message": "Success",
    "elapsed": 26,
    "totalResults": 319,
    "results": [
        {
            "createTime": 1598465254999,
            "shortDescription": "The application \"<share><link hash=\"9dfd80610cbbc9188f6c6bc85c87016b0ae42254fc289c2b578e85282bdd9c23\">taskhost.exe</link></share>\" successfully attempted to enable executable memory.",  # noqa: E501
            "longDescription": "The application \"<share><link hash=\"9dfd80610cbbc9188f6c6bc85c87016b0ae42254fc289c2b578e85282bdd9c23\">C:\\windows\\system32\\taskhost.exe</link></share>\" attempted to enable executable memory, by calling the function \"NtProtectVirtualMemory\". The operation was successful.",  # noqa: E501
            "eventTime": 1598465240671,
            "eventId": "013c2b15e7c711ea9affe54c85cd133a",
            "threatIndicators": [
                "MODIFY_MEMORY_PROTECTION"
            ],
            "registryValue": None,
            "securityEventCode": None,
            "deviceDetails": {
                "deviceIpAddress": "144.121.3.50",
                "agentLocation": "OFFSITE",
                "deviceLocation": {
                    "city": None,
                    "region": None,
                    "areaCode": 0,
                    "countryName": "United States",
                    "countryCode": "US",
                    "dmaCode": 0,
                    "latitude": 37.751007,
                    "longitude": -97.822,
                    "metroCode": 0,
                    "postalCode": None
                },
                "deviceIpV4Address": "144.121.3.50",
                "deviceId": 98765,
                "deviceName": "Win7x64",
                "policyId": 11200,
                "email": "email@example.org",
                "deviceType": "WINDOWS",
                "deviceHostName": None,
                "deviceVersion": "Windows 7 x64 SP: 1",
                "targetPriorityType": "MEDIUM",
                "targetPriorityCode": 1,
                "loginUserName": None,
                "deviceOwnerName": None,
                "msmGroupId": 0,
                "msmGroupName": None,
                "policyName": "policy-restrictive"
            },
            "netFlow": {
                "destAddress": None,
                "peerFqdn": None,
                "peerLocation": None,
                "peerSiteReputation": None,
                "peerIpAddress": None,
                "sourceAddress": "10.210.34.165",
                "sourcePort": None,
                "destPort": None,
                "peerIpV4Address": None,
                "service": None
            },
            "processDetails": {
                "fullUserName": "fullUserName",
                "targetName": "taskhost.exe",
                "parentName": "services.exe",
                "userName": "LOCAL SERVICE",
                "privatePid": "4204-132429389232310730-0",
                "targetPrivatePid": None,
                "commandLine": "taskhost.exe $(Arg0)",
                "milisSinceProcessStart": 0,
                "processId": 4204,
                "parentPid": 540,
                "targetCommandLine": "taskhost.exe",
                "targetPid": None,
                "parentCommandLine": None,
                "interpreterName": None,
                "interpreterHash": None,
                "parentPrivatePid": "540-132368223470440203-0",
                "name": "taskhost.exe"
            },
            "eventType": "SYSTEM_API_CALL",
            "parentApp": {
                "effectiveReputationSource": "CLOUD",
                "effectiveReputation": "TRUSTED_WHITE_LIST",
                "applicationName": "services.exe",
                "sha256Hash": "0995f71c34f613207bc39ed4fcc1bbbee396a543fa1739656f7ddf70419309fc",
                "reputationProperty": "TRUSTED_WHITE_LIST",
                "virusSubCategory": None,
                "md5Hash": None,
                "applicationPath": None,
                "virusName": None,
                "virusCategory": None
            },
            "selectedApp": {
                "effectiveReputationSource": "WHITE_DATABASE",
                "effectiveReputation": "TRUSTED_WHITE_LIST",
                "applicationName": "taskhost.exe",
                "sha256Hash": "9dfd80610cbbc9188f6c6bc85c87016b0ae42254fc289c2b578e85282bdd9c23",
                "reputationProperty": "TRUSTED_WHITE_LIST",
                "virusSubCategory": None,
                "md5Hash": "639774c9acd063f028f6084abf5593ad",
                "applicationPath": "C:\\windows\\system32\\taskhost.exe",
                "virusName": None,
                "virusCategory": None
            },
            "targetApp": {
                "effectiveReputationSource": None,
                "effectiveReputation": None,
                "applicationName": "taskhost.exe",
                "sha256Hash": None,
                "reputationProperty": None,
                "virusSubCategory": None,
                "md5Hash": None,
                "applicationPath": None,
                "virusName": None,
                "virusCategory": None
            },
            "attackStage": None,
            "alertScore": 0,
            "alertCategory": None,
            "incidentId": None
        }]
}

EVENT_GET_SPECIFIC_RESP = {
    "eventInfo": {
        "shortDescription": "The application \"<share><link hash=\"93b2ed4004ed5f7f3039dd7ecbd22c7e4e24b6373b4d9ef8d6e45a179b13a5e8\">svchost.exe</link></share>\" unsuccessfully invoked the application \"<share><link hash=\"933e1778b2760b3a9194c2799d7b76052895959c3caedefb4e9d764cbb6ad3b5\">notepad.exe</link></share>\".",  # noqa: E501
        "longDescription": "The application \"<share><link hash=\"93b2ed4004ed5f7f3039dd7ecbd22c7e4e24b6373b4d9ef8d6e45a179b13a5e8\">C:\\Windows\\System32\\svchost.exe -k LocalSystemNetworkRestricted</link></share>\" invoked the application \"<share><link hash=\"933e1778b2760b3a9194c2799d7b76052895959c3caedefb4e9d764cbb6ad3b5\">C:\\windows\\system32\\notepad.exe</link></share>\". The operation was <accent>blocked by Cb Endpoint Standard</accent>.",  # noqa: E501
        "eventTime": 1596563706477,
        "eventId": "a1e12604d67b11ea920d3d9192a785d1",
        "createTime": 1596563731121,
        "threatIndicators": [
            "POLICY_DENY"
        ],
        "registryValue": None,
        "securityEventCode": None,
        "deviceDetails": {
            "deviceIpAddress": "144.121.3.50",
            "agentLocation": "OFFSITE",
            "deviceLocation": None,
            "deviceIpV4Address": "144.121.3.50",
            "deviceType": "WINDOWS",
            "email": "email@example.org",
            "policyId": 11200,
            "deviceId": 98765,
            "deviceName": "Win7x64",
            "deviceHostName": None,
            "deviceVersion": "Windows 7 x64 SP: 1",
            "targetPriorityType": "MEDIUM",
            "targetPriorityCode": 1,
            "loginUserName": None,
            "deviceOwnerName": None,
            "msmGroupId": None,
            "msmGroupName": None,
            "policyName": "policy-restrictive"
        },
        "netFlow": {
            "destAddress": None,
            "peerFqdn": None,
            "peerLocation": None,
            "peerSiteReputation": None,
            "peerIpAddress": None,
            "sourceAddress": None,
            "sourcePort": None,
            "destPort": None,
            "peerIpV4Address": None,
            "service": None
        },
        "processDetails": {
            "userName": "SYSTEM",
            "parentName": "services.exe",
            "privatePid": "888-132368223540796326-0",
            "targetPrivatePid": "4294967295",
            "commandLine": "C:\\Windows\\System32\\svchost.exe -k LocalSystemNetworkRestricted",
            "milisSinceProcessStart": 0,
            "processId": 888,
            "parentPid": 540,
            "targetCommandLine": "notepad.exe",
            "targetPid": 4294967295,
            "parentCommandLine": None,
            "interpreterName": None,
            "interpreterHash": None,
            "parentPrivatePid": "540-132368223470440203-0",
            "fullUserName": "fullUserName",
            "targetName": "notepad.exe",
            "name": "svchost.exe"
        },
        "eventType": "CREATE_PROCESS",
        "parentApp": {
            "applicationName": "services.exe",
            "sha256Hash": "0995f71c34f613207bc39ed4fcc1bbbee396a543fa1739656f7ddf70419309fc",
            "reputationProperty": "TRUSTED_WHITE_LIST",
            "virusSubCategory": None,
            "md5Hash": None,
            "applicationPath": None,
            "virusName": None,
            "virusCategory": None,
            "effectiveReputationSource": "CLOUD",
            "effectiveReputation": "TRUSTED_WHITE_LIST"
        },
        "selectedApp": {
            "applicationName": "svchost.exe",
            "sha256Hash": "93b2ed4004ed5f7f3039dd7ecbd22c7e4e24b6373b4d9ef8d6e45a179b13a5e8",
            "reputationProperty": "TRUSTED_WHITE_LIST",
            "virusSubCategory": None,
            "md5Hash": "c78655bc80301d76ed4fef1c1ea40a7d",
            "applicationPath": "C:\\windows\\system32\\svchost.exe",
            "virusName": None,
            "virusCategory": None,
            "effectiveReputationSource": "WHITE_DATABASE",
            "effectiveReputation": "TRUSTED_WHITE_LIST"
        },
        "targetApp": {
            "applicationName": "notepad.exe",
            "sha256Hash": "933e1778b2760b3a9194c2799d7b76052895959c3caedefb4e9d764cbb6ad3b5",
            "reputationProperty": "TRUSTED_WHITE_LIST",
            "virusSubCategory": None,
            "md5Hash": None,
            "applicationPath": None,
            "virusName": None,
            "virusCategory": None,
            "effectiveReputationSource": "CLOUD",
            "effectiveReputation": "TRUSTED_WHITE_LIST"
        },
        "attackStage": "INSTALL_RUN",
        "alertScore": 3,
        "alertCategory": "WARNING",
        "incidentId": "NNMH0QAU"
    },
    "success": True,
    "message": "Success"
}
