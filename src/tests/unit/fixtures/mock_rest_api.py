# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Mock for the rest api."""

NOTIFICATIONS_RESP = {
    "notifications": [
        {
            "policyAction": {
                "sha256Hash": "2552332222112552332222112552332222112552332222112552332222112552",
                "action": "TERMINATE",
                "reputation": "KNOWN_MALWARE",
                "applicationName": "firefox.exe",
            },
            "type": "POLICY_ACTION",
            "eventTime": 1423163263482,
            "eventId": "EV1",
            "url": "http://carbonblack.com/ui#device/100/hash/25523322221125523322221125523322221125523"
            "32222112552332222112552/app/firefox.exe/keyword/terminate policy action",
            "deviceInfo": {
                "deviceType": "WINDOWS",
                "email": "tester@carbonblack.com",
                "deviceId": 100,
                "deviceName": "testers-pc",
                "deviceHostName": None,
                "deviceVersion": "7 SP1",
                "targetPriorityType": "HIGH",
                "targetPriorityCode": 0,
                "internalIpAddress": "55.33.22.11",
                "groupName": "Executives",
                "externalIpAddress": "255.233.222.211",
            },
            "eventDescription": "Policy action 1",
            "ruleName": "Alert Rule 1",
        },
        {
            "threatInfo": {
                "time": 1423163263501,
                "indicators": [
                    {
                        "sha256Hash": "aafafafafafafafafafafafafafafafafafafa7347878",
                        "indicatorName": "BUFFER_OVERFLOW",
                        "applicationName": "chrome.exe",
                    },
                    {
                        "sha256Hash": "ddfdhjhjdfjdfjdhjfdjfhjdfhjdhfjdhfjdhfjdh7347878",
                        "indicatorName": "INJECT_CODE",
                        "applicationName": "firefox.exe",
                    },
                ],
                "summary": "Threat Summary 23",
                "score": 8,
                "incidentId": "ABCDEF",
            },
            "type": "THREAT",
            "eventTime": 1423163263501,
            "eventId": "EV2",
            "url": "http://carbonblack.com/ui#device/100/incident/ABCDEF",
            "deviceInfo": {
                "deviceType": "WINDOWS",
                "email": "tester@carbonblack.com",
                "deviceId": 100,
                "deviceName": "testers-pc",
                "deviceHostName": None,
                "deviceVersion": "7 SP1",
                "targetPriorityType": "HIGH",
                "targetPriorityCode": 0,
                "internalIpAddress": "55.33.22.11",
                "groupName": "Executives",
                "externalIpAddress": "255.233.222.211",
            },
            "eventDescription": "time|Threat summary 23|score",
            "ruleName": "Alert Rule 2",
        },
    ],
    "message": "Success",
    "success": True,
}


ALERT_SEARCH_SUGGESTIONS_RESP = {
    "suggestions": [
        {"term": "threat_category", "weight": 525},
        {"term": "watchlist_name", "weight": 512},
        {"term": "ttp", "weight": 486},
        {"term": "run_state", "weight": 481},
        {"term": "device_name", "weight": 477},
        {"term": "alert_id", "weight": 472},
        {"term": "event_id", "weight": 472},
        {"term": "threat_vector", "weight": 468},
        {"term": "device_username", "weight": 461},
        {"term": "report_id", "weight": 458},
        {"term": "process_guid", "weight": 431},
        {"term": "process_name", "weight": 431},
        {"term": "sensor_action", "weight": 424},
        {"term": "alert_severity", "weight": 419},
        {"term": "device_id", "weight": 412},
        {"term": "device_os", "weight": 412},
        {"term": "device_policy", "weight": 401},
        {"term": "process_pid", "weight": 311},
        {"term": "process_hash", "weight": 306},
        {"term": "process_reputation", "weight": 287},
    ]
}


PROCESS_SEARCH_VALIDATIONS_RESP = {"valid": True, "value_search_query": True}


CUSTOM_SEVERITY_RESP = {"results": [{"report_id": "id", "severity": 10}]}


PROCESS_LIMITS_RESP = {"time_bounds": {"lower": 1564686473166, "upper": 1579023412990}}


FETCH_PROCESS_QUERY_RESP = {
    "query_ids": [
        "4JDT3MX9Q/3867b4e7-b329-4caa-8f80-76899b1360fa",
        "4JDT3MX9Q/3871eab1-bb9b-4cb7-9ac4-a840f4a84fab",
    ]
}


CONVERT_FEED_QUERY_RESP = {"query": "(process_guid:123) -enriched:true"}
