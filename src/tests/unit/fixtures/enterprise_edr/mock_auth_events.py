"""Mock responses for Auth Events queries."""

POST_AUTH_EVENTS_SEARCH_JOB_RESP = {"job_id": "62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs"}

GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP = {
  "results": [
    {
      "auth_domain_name": "NT AUTHORITY",
      "auth_event_action": "LOGON_SUCCESS",
      "auth_remote_device": "-",
      "auth_remote_port": 0,
      "auth_username": "SYSTEM",
      "backend_timestamp": "2023-01-13T17:19:01.013Z",
      "childproc_count": 0,
      "crossproc_count": 48,
      "device_group_id": 0,
      "device_id": 17686136,
      "device_name": "test_name",
      "device_policy_id": 20622246,
      "device_timestamp": "2023-01-13T17:17:45.322Z",
      "event_id": "DA9E269E-421D-469D-A212-9062888A02F4",
      "filemod_count": 3,
      "ingress_time": 1673630293265,
      "modload_count": 1,
      "netconn_count": 35,
      "org_id": "ABCD1234",
      "parent_guid": "ABCD1234-010dde78-00000260-00000000-1d9275de5e5b262",
      "parent_pid": 608,
      "process_guid": "ABCD1234-010dde78-00000308-00000000-1d9275de6169dd7",
      "process_hash": [
        "15a556def233f112d127025ab51ac2d3",
        "362ab9743ff5d0f95831306a780fc3e418990f535013c80212dd85cb88ef7427"
      ],
      "process_name": "c:\\windows\\system32\\lsass.exe",
      "process_pid": [
        776
      ],
      "process_username": [
        "NT AUTHORITY\\SYSTEM"
      ],
      "regmod_count": 11,
      "scriptload_count": 0,
      "windows_event_id": 4624
    }
  ],
  "num_found": 1,
  "num_available": 1,
  "approximate_unaggregated": 1,
  "num_aggregated": 1,
  "contacted": 4,
  "completed": 4
}


GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_0 = {
  "results": [],
  "num_found": 0,
  "num_available": 0,
  "approximate_unaggregated": 0,
  "num_aggregated": 0,
  "contacted": 0,
  "completed": 0
}


GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_ZERO_COMP = {
  "results": [],
  "num_found": 0,
  "num_available": 0,
  "approximate_unaggregated": 0,
  "num_aggregated": 0,
  "contacted": 242,
  "completed": 0
}


GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_ZERO = {
  "results": [],
  "num_found": 0,
  "num_available": 0,
  "approximate_unaggregated": 0,
  "num_aggregated": 0,
  "contacted": 242,
  "completed": 242
}


GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_2 = {
  "results": [
    {
      "auth_domain_name": "NT AUTHORITY",
      "auth_event_action": "LOGOFF_SUCCESS",
      "auth_remote_port": 0,
      "auth_username": "SYSTEM",
      "backend_timestamp": "2023-03-08T08:18:52.654Z",
      "childproc_count": 0,
      "crossproc_count": 1859,
      "device_group_id": 0,
      "device_id": 18101914,
      "device_name": "richm\\win11",
      "device_policy_id": 20886205,
      "device_timestamp": "2023-03-08T08:15:03.090Z",
      "event_id": "9D137450-6428-446E-8C23-F0C526156A0C",
      "filemod_count": 33,
      "ingress_time": 1678263444460,
      "modload_count": 7,
      "netconn_count": 113,
      "org_id": "ABCD1234",
      "parent_guid": "ABCD1234-0114369a-000002ac-00000000-1d94538fb2b061e",
      "parent_pid": 684,
      "process_guid": "ABCD1234-0114369a-0000033c-00000000-1d94538fb4eea6c",
      "process_hash": [
        "c0ba0caebf823de8f2ebf49eea9cc5e5",
        "c72b9e35e307fefe59bacc3c65842e93b963f6c3732934061857cc773d6e2e5b"
      ],
      "process_name": "c:\\windows\\system32\\lsass.exe",
      "process_pid": [
        828
      ],
      "process_username": [
        "NT AUTHORITY\\SYSTEM"
      ],
      "regmod_count": 42,
      "scriptload_count": 0,
      "windows_event_id": 4634
    },
    {
      "auth_domain_name": "NT AUTHORITY",
      "auth_event_action": "PRIVILEGES_GRANTED",
      "auth_remote_port": 0,
      "auth_username": "SYSTEM",
      "backend_timestamp": "2023-03-08T08:18:52.654Z",
      "childproc_count": 0,
      "crossproc_count": 1859,
      "device_group_id": 0,
      "device_id": 18101914,
      "device_name": "richm\\win11",
      "device_policy_id": 20886205,
      "device_timestamp": "2023-03-08T08:15:03.082Z",
      "event_id": "D5A08829-041E-401E-9C14-F8FDFBC2EE63",
      "filemod_count": 33,
      "ingress_time": 1678263444460,
      "modload_count": 7,
      "netconn_count": 113,
      "org_id": "ABCD1234",
      "parent_guid": "ABCD1234-0114369a-000002ac-00000000-1d94538fb2b061e",
      "parent_pid": 684,
      "process_guid": "ABCD1234-0114369a-0000033c-00000000-1d94538fb4eea6c",
      "process_hash": [
        "c0ba0caebf823de8f2ebf49eea9cc5e5",
        "c72b9e35e307fefe59bacc3c65842e93b963f6c3732934061857cc773d6e2e5b"
      ],
      "process_name": "c:\\windows\\system32\\lsass.exe",
      "process_pid": [
        828
      ],
      "process_username": [
        "NT AUTHORITY\\SYSTEM"
      ],
      "regmod_count": 42,
      "scriptload_count": 0,
      "windows_event_id": 4672
    }
  ],
  "num_found": 198,
  "num_available": 198,
  "approximate_unaggregated": 198,
  "num_aggregated": 198,
  "contacted": 241,
  "completed": 241
}


GET_AUTH_EVENTS_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING = {
    "num_found": 808,
    "num_available": 1,
    "contacted": 6,
    "completed": 0,
    "results": [],
}


GET_AUTH_EVENTS_DETAIL_JOB_RESULTS_RESP = {
  "results": [
    {
      "auth_cleartext_credentials_logon": False,
      "auth_daemon_logon": False,
      "auth_domain_name": "NT AUTHORITY",
      "auth_elevated_token_logon": False,
      "auth_event_action": "LOGON_SUCCESS",
      "auth_failed_logon_count": 0,
      "auth_impersonation_level": "IMPERSONATION_INVALID",
      "auth_interactive_logon": False,
      "auth_key_length": 0,
      "auth_logon_id": "00000000-000003E7",
      "auth_logon_type": 5,
      "auth_package": "Negotiate",
      "auth_remote_device": "-",
      "auth_remote_logon": False,
      "auth_remote_port": 0,
      "auth_restricted_admin_logon": False,
      "auth_user_id": "S-1-5-18",
      "auth_username": "SYSTEM",
      "auth_virtual_account_logon": False,
      "backend_timestamp": "2023-02-23T14:31:09.058Z",
      "childproc_count": 0,
      "crossproc_count": 0,
      "device_external_ip": "66.170.98.188",
      "device_group_id": 0,
      "device_id": 17853466,
      "device_installed_by": "No user",
      "device_internal_ip": "10.52.4.52",
      "device_location": "UNKNOWN",
      "device_name": "cbawtd\\w10cbws2thtplt",
      "device_os": "WINDOWS",
      "device_os_version": "Windows 10 x64",
      "device_policy": "raj-test-monitor",
      "device_policy_id": 20622246,
      "device_sensor_version": "3.9.1.2451",
      "device_target_priority": "MEDIUM",
      "device_timestamp": "2023-02-23T14:29:03.588Z",
      "document_guid": "19F5ah7QR8mTUjdqRvXm0w",
      "event_id": "D06DC822-B25E-4162-A5A7-6166BFA9B8DF",
      "event_report_code": "SUB_RPT_NONE",
      "filemod_count": 0,
      "ingress_time": 1677162610331,
      "modload_count": 0,
      "netconn_count": 0,
      "org_id": "ABCD1234",
      "parent_cmdline": "wininit.exe",
      "parent_cmdline_length": 11,
      "parent_effective_reputation": "LOCAL_WHITE",
      "parent_effective_reputation_source": "IGNORE",
      "parent_guid": "ABCD1234-01106c1a-0000025c-00000000-1d942ef2b31029a",
      "parent_hash": [
        "9ef51c8ad595c5e2a123c06ad39fccd7",
        "268ca325c8f12e68b6728ff24d6536030aab6e05603d0179033b1e51d8476d86"
      ],
      "parent_name": "c:\\windows\\system32\\wininit.exe",
      "parent_pid": 604,
      "parent_reputation": "TRUSTED_WHITE_LIST",
      "process_cmdline": [
        "C:\\Windows\\system32\\lsass.exe"
      ],
      "process_cmdline_length": [
        29
      ],
      "process_effective_reputation": "LOCAL_WHITE",
      "process_effective_reputation_source": "IGNORE",
      "process_elevated": True,
      "process_guid": "ABCD1234-01106c1a-000002fc-00000000-1d942ef2b618b15",
      "process_hash": [
        "15a556def233f112d127025ab51ac2d3",
        "362ab9743ff5d0f95831306a780fc3e418990f535013c80212dd85cb88ef7427"
      ],
      "process_integrity_level": "SYSTEM",
      "process_name": "c:\\windows\\system32\\lsass.exe",
      "process_pid": [
        764
      ],
      "process_reputation": "TRUSTED_WHITE_LIST",
      "process_sha256": "362ab9743ff5d0f95831306a780fc3e418990f535013c80212dd85cb88ef7427",
      "process_start_time": "2023-02-17T16:44:57.657Z",
      "process_username": [
        "NT AUTHORITY\\SYSTEM"
      ],
      "regmod_count": 0,
      "scriptload_count": 0,
      "windows_event_id": 4624
    }
  ],
  "num_found": 1,
  "num_available": 1,
  "approximate_unaggregated": 1,
  "num_aggregated": 1,
  "contacted": 13,
  "completed": 13
}


"""Mocks for auth events facet query testing."""


POST_AUTH_EVENTS_FACET_SEARCH_JOB_RESP = {
    "job_id": "62be5c2c-d080-4ce6-b4f3-7c519cc2b41c-sqs"
}


GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_1 = {
    "ranges": [
        {
            "start": "2020-08-04T08:01:32.077Z",
            "end": "2020-08-05T08:01:32.077Z",
            "bucket_size": "+1HOUR",
            "field": "device_timestamp",
            "values": [{"total": 456, "name": "2020-08-04T08:01:32.077Z"}],
        }
    ],
    "terms": [
        {
            "values": [{"total": 116, "id": "chrome.exe", "name": "chrome.exe"}],
            "field": "process_name",
        }
    ],
    "num_found": 116,
    "contacted": 34,
    "completed": 34,
}


GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2 = {
    "ranges": [],
    "terms": [
        {
            "values": [{"total": 116, "id": "chrome.exe", "name": "chrome.exe"}],
            "field": "process_name",
        }
    ],
    "num_found": 116,
    "contacted": 34,
    "completed": 34,
}


GET_AUTH_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_STILL_QUERYING = {
    "ranges": [],
    "terms": [],
    "num_found": 0,
    "contacted": 34,
    "completed": 0,
}


GET_AUTH_EVENTS_GROUPED_RESULTS_RESP = {
  "group_results": [
    {
      "group_key": "auth_username",
      "group_value": "SYSTEM",
      "group_start_timestamp": "2023-02-23T14:29:03.588Z",
      "group_end_timestamp": "2023-03-07T11:11:21.593Z",
      "results": [
        {
          "auth_domain_name": "NT AUTHORITY",
          "auth_event_action": "LOGOFF_SUCCESS",
          "auth_remote_port": 0,
          "auth_username": "SYSTEM",
          "backend_timestamp": "2023-03-07T11:20:02.046Z",
          "childproc_count": 0,
          "crossproc_count": 1724,
          "device_group_id": 0,
          "device_id": 18101914,
          "device_name": "richm\\win11",
          "device_policy_id": 20886205,
          "device_timestamp": "2023-03-07T11:11:21.593Z",
          "event_id": "E8F7A1F9-72FC-4C5D-B8D2-113647B30D87",
          "filemod_count": 31,
          "ingress_time": 1678187557319,
          "modload_count": 7,
          "netconn_count": 112,
          "org_id": "ABCD1234",
          "parent_guid": "ABCD1234-0114369a-000002ac-00000000-1d94538fb2b061e",
          "parent_pid": 684,
          "process_guid": "ABCD1234-0114369a-0000033c-00000000-1d94538fb4eea6c",
          "process_hash": [
            "c0ba0caebf823de8f2ebf49eea9cc5e5",
            "c72b9e35e307fefe59bacc3c65842e93b963f6c3732934061857cc773d6e2e5b"
          ],
          "process_name": "c:\\windows\\system32\\lsass.exe",
          "process_pid": [
            828
          ],
          "process_username": [
            "NT AUTHORITY\\SYSTEM"
          ],
          "regmod_count": 39,
          "scriptload_count": 0,
          "windows_event_id": 4634
        },
              ],
      "total_events": 174
    }
  ],
  "num_found": 174,
  "num_available": 174,
  "groups_num_available": 1,
  "approximate_unaggregated": 174,
  "num_aggregated": 174,
  "contacted": 169,
  "completed": 169
}

AUTH_EVENTS_SEARCH_SUGGESTIONS_RESP = {
  "suggestions": [
    {
      "term": "auth_cleartext_credentials_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_daemon_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_domain_name",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_elevated_token_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_event_action",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_failed_logon_count",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_failure_status",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_failure_sub_status",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_interactive_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_logon_id",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_logon_type",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_privileges",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_device",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_ipv4",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_ipv6",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_location",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_remote_port",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_restricted_admin_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_user_id",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_user_principal_name",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_username",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    },
    {
      "term": "auth_virtual_account_logon",
      "weight": 300,
      "required_skus_all": [
        "auth"
      ],
      "required_skus_some": []
    }
  ]
}


AUTH_EVENTS_SEARCH_VALIDATIONS_RESP = {
  "valid": True,
  "value_search_query": True
}
