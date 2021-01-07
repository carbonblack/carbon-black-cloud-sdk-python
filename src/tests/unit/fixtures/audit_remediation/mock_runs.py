
"""Mock data for runs of audit and remediation code."""

GET_RUN_RESP = {
    "org_key": "ABCDEFGH",
    "name": "Find Programs Installed in Non-Standard Windows Locations",
    "id": "run_id",
    "sql": "SELECT path, DATETIME(atime,\"unixepoch\",\"localtime\") AS \"Last Accessed\", DATETIME(mtime,\"unixepoch\",\"localtime\") AS \"Last Modified\", DATETIME(ctime,\"unixepoch\",\"localtime\") AS \"Created\" FROM file WHERE path LIKE \"\\users\\%\\AppData\\%.exe\" OR path LIKE \"\\users\\%\\AppData\\Roaming\\%.exe\" OR path LIKE \"\\ProgramData\\%.exe\";",  # noqa: E501
    "created_by": "QZGH961F1B",
    "destinations": [
        "LQ"
    ],
    "create_time": "2020-06-16T19:09:00.227Z",
    "status_update_time": "2020-06-16T19:10:52.031Z",
    "timeout_time": "2020-06-23T19:09:00.227Z",
    "cancellation_time": None,
    "cancelled_by": None,
    "archive_time": None,
    "archived_by": None,
    "notify_on_finish": False,
    "active_org_devices": 3,
    "status": "COMPLETE",
    "device_filter": {
        "policy_id": None,
        "os": [
            "MAC",
            "WINDOWS",
            "LINUX"
        ],
        "device_id": None,
        "deployment_type": None,
        "policy_ids": None,
        "device_types": [
            "MAC",
            "WINDOWS",
            "LINUX"
        ],
        "device_ids": None
    },
    "recommended_query_id": None,
    "template_id": None,
    "schedule": None,
    "schema": None,
    "last_result_time": None,
    "total_results": 0,
    "not_started_count": 0,
    "match_count": 0,
    "no_match_count": 0,
    "success_count": 0,
    "in_progress_count": 0,
    "error_count": 0,
    "not_supported_count": 0,
    "cancelled_count": 0
}

GET_RUN_RESULTS_RESP = {
    "id": "run_id",
    "device": {
        "id": 1234567,
        "name": "WIN-A1B2C3D4",
        "policy_id": 1,
        "policy_name": "default",
        "os": "WINDOWS"
    },
    "status": "not_matched",
    "time_received": "2020-09-21T22:38:40.809Z",
    "device_message": "",
    # fields from livequery_framework.support.enums LiveQueryDeviceSummaryFacetFieldsV1
    "fields": {"status", "device.id"}

}

GET_RUN_RESULTS_RESP_1 = {
    "id": "run_id",
    "device": {
        "id": 1234567,
        "name": "WIN-A1B2C3D4",
        "policy_id": 1,
        "policy_name": "default",
        "os": "WINDOWS"
    },
    "status": "not_matched",
    "time_received": "2020-09-21T22:38:40.809Z",
    "device_message": "",
    # fields from livequery_framework.support.enums LiveQueryDeviceSummaryFacetFieldsV1
    "fields": {"status", "device.id"},
    "metrics": {
        "cpu": 24.3,
        "memory": 8.0
    }
}

GET_RUN_RESULTS_RESP_2 = {
    "org_key": "A1B2C3D4E5",
    "num_found": 6,
    "results": [
        {
            "id": "run_id",
            "device": {
                "id": 12345,
                "name": "deviceName0",
                "policy_id": 98765,
                "policy_name": "device0policy",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-22T09:53:48.313Z",
            "device_message": "",
            "fields": {}
        },
        {
            "id": "run_id",
            "device": {
                "id": 23456,
                "name": "deviceName1",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-21T22:39:55.397Z",
            "device_message": "",
            "fields": {}
        },
        {
            "id": "run_id",
            "device": {
                "id": 87654,
                "name": "deviceName2",
                "policy_id": 10346,
                "policy_name": "1 Engineering",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-21T22:39:28.118Z",
            "device_message": "",
            "fields": {}
        },
        {
            "id": "run_id",
            "device": {
                "id": 34567,
                "name": "WIN-A1B2C3D4",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-21T22:39:20.147Z",
            "device_message": "",
            "fields": {}
        },
        {
            "id": "run_id",
            "device": {
                "id": 111222333,
                "name": "WIN-A1B2C3D4F",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-21T22:39:06.895Z",
            "device_message": "",
            "fields": {}
        },
        {
            "id": "run_id",
            "device": {
                "id": 98989898,
                "name": "deviceName4",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-21T22:38:40.809Z",
            "device_message": "",
            "fields": {}
        }
    ]
}

GET_RUN_RESULTS_RESP_3 = {
    "org_key": "A1B2C3D4E5",
    "num_found": 3,
    "results": [
        {
            "id": "4bkd3tkgdba8iis2r8kf7itaxdtr6tnz",
            "device": {
                "id": 12345,
                "name": "Win10",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "matched",
            "time_received": "2020-09-14T13:01:30.989Z",
            "device_message": "",
            "fields": {
                "author": "",
                "directory": "/Users/win",
                "locale": "en",
                "name": "Chrome Media Router",
                "path": "/Users/bit9qa/Library/Application Support/Google/Chrome/Default/Extensions/pkedcjkdefgpdelpbcmbmeomcjbeemfm/7519.422.0.3_0/",  # noqa: E501
                "persistent": 0,
                "shell": "/bin/bash",
                "type": "",
                "update_url": "https://clients2.google.com/service/update2/crx",
                "username": "win",
                "version": "7519.422.0.3"
            }
        },
        {
            "id": "4bkd3tkgdba8iis2r8kf7itaxdtr6tnz",
            "device": {
                "id": 12345,
                "name": "Win10",
                "policy_id": 1,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "status": "matched",
            "time_received": "2020-09-14T13:01:30.989Z",
            "device_message": "",
            "fields": {
                "author": "",
                "directory": "/Users/win",
                "locale": "en",
                "name": "Chrome Media Router",
                "path": "/Users/bit9qa/Library/Application Support/Google/Chrome/Default/Extensions/pkedcjkdefgpdelpbcmbmeomcjbeemfm/7419.311.0.1_0/",  # noqa: E501
                "persistent": 0,
                "shell": "/bin/bash",
                "type": "",
                "update_url": "https://clients2.google.com/service/update2/crx",
                "username": "win",
                "version": "7419.311.0.1"
            }
        },
        {
            "id": "4bkd3tkgdba8iis2r8kf7itaxdtr6tnz",
            "device": {
                "id": 12345,
                "name": "Win7x64",
                "policy_id": 2,
                "policy_name": "policy2",
                "os": "WINDOWS"
            },
            "status": "matched",
            "time_received": "2020-09-14T13:01:30.989Z",
            "device_message": "",
            "fields": {
                "author": "",
                "directory": "/Users/win",
                "locale": "en",
                "name": "Chrome Media Router",
                "path": "/Users/bit9qa/Library/Application Support/Google/Chrome/Default/Extensions/pkedcjkdefgpdelpbcmbmeomcjbeemfm/7619.603.0.2_0/",  # noqa: E501
                "persistent": 0,
                "shell": "/bin/bash",
                "type": "",
                "update_url": "https://clients2.google.com/service/update2/crx",
                "username": "win",
                "version": "7619.603.0.2"
            }
        }
    ]
}

GET_DEVICE_SUMMARY_RESP_1 = {
    "org_key": "test",
    "num_found": 5,
    "results": [
        {
            "total_results": 0,
            "status": "in_progress",
            "device": {
                "id": 3430049,
                "name": "HW-HOST-A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": None,
            "metrics": {
                "average_system_memory_in_use": 70.0,
                "osquery_creation_time_unix_ms": 1.600804383268E12,
                "total_cpu_peak": 0.0
            },
            "start_time": "2020-09-22T19:53:05.883Z",
            "finish_time": None,
            "update_time": "2020-09-22T19:53:05.890Z"
        },
        {
            "total_results": 0,
            "status": "not_matched",
            "device": {
                "id": 3693561,
                "name": "LAB\\A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": "",
            "metrics": {
                "average_system_memory_in_use": 70.0,
                "osquery_creation_time_unix_ms": 1.600804383268E12,
                "total_cpu_peak": 0.0,
                "osquery_current_memory_in_use_mb": 0.0,
                "current_misc_io_operation_rate": 0.0,
                "current_misc_io_transfer_rate_kb": 0.0,
                "current_write_transfer_rate_kb": 0.0,
                "current_system_memory_in_use_mb": 2847.0,
                "total_cpu_current": 0.0,
                "total_write_operations": 5.0,
                "average_read_transfer_rate_kb": 0.0,
                "average_write_operation_rate": 0.0,
                "osquery_life_time_ms": 297.0,
                "current_system_memory_available": 30.0,
                "total_read_operations": 33.0,
                "average_misc_io_transfer_rate_kb": 0.0,
                "total_cpu_average": 0.0,
                "current_system_memory_in_use": 70.0,
                "peak_system_memory_available": 30.0,
                "kernel_cpu_average": 0.0,
                "total_write_transfer_count_mb": 0.0,
                "osquery_peak_memory_in_use_mb": 0.0,
                "average_misc_io_operation_rate": 0.0,
                "average_system_memory_in_use_mb": 2847.0,
                "average_read_operation_rate": 0.0,
                "peak_system_memory_in_use": 70.0,
                "current_read_operation_rate": 0.0,
                "osquery_total_kernel_mode_time_ms": 62.0,
                "kernel_cpu_peak": 0.0,
                "osquery_average_percent_of_memory_in_use": 0.0,
                "average_write_transfer_rate_kb": 0.0,
                "average_system_memory_available": 30.0,
                "osquery_average_memory_in_use_mb": 0.0,
                "total_read_transfer_count_mb": 0.0,
                "user_cpu_average": 0.0,
                "peak_system_memory_available_mb": 1200.0,
                "current_system_memory_available_mb": 1200.0,
                "peak_system_memory_in_use_mb": 2847.0,
                "current_read_transfer_rate_kb": 0.0,
                "kernel_cpu_current": 0.0,
                "total_misc_io_transfer_count_mb": 0.0,
                "osquery_current_percent_of_all_memory": 0.0,
                "osquery_peak_percent_of_memory_in_use": 0.01,
                "user_cpu_peak": 0.0,
                "average_system_memory_available_mb": 1200.0,
                "osquery_current_percent_of_memory_in_use": 0.0,
                "osquery_total_user_mode_time_ms": 15.0,
                "total_misc_io_operations": 319.0,
                "current_write_operation_rate": 0.0,
                "osquery_average_percent_of_all_memory": 0.01,
                "osquery_peak_percent_of_all_memory": 0.02,
                "process_monitoring_rate_ms": 500.0,
                "user_cpu_current": 0.0,
                "osquery_exit_time_unix_ms": 1.600804383565E12
            },
            "start_time": "2020-09-22T19:53:03.120Z",
            "finish_time": "2020-09-22T19:53:03.896Z",
            "update_time": "2020-09-22T19:53:04.427Z"
        },
        {
            "total_results": 0,
            "status": "in_progress",
            "device": {
                "id": 3533270,
                "name": "DESKTOP-A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": None,
            "metrics": {
                "average_system_memory_in_use": 70.0,
                "osquery_creation_time_unix_ms": 1.600804383268E12,
                "total_cpu_peak": 0.0
            },
            "start_time": "2020-09-22T19:53:03.792Z",
            "finish_time": None,
            "update_time": "2020-09-22T19:53:03.799Z"
        },
        {
            "total_results": 0,
            "status": "in_progress",
            "device": {
                "id": 3583182,
                "name": "DESKTOP-A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": None,
            "metrics": {
                "average_system_memory_in_use": 70.0,
                "osquery_creation_time_unix_ms": 1.600804383268E12,
                "total_cpu_peak": 0.0
            },
            "start_time": "2020-09-22T19:52:58.204Z",
            "finish_time": None,
            "update_time": "2020-09-22T19:52:58.212Z"
        },
        {
            "total_results": 0,
            "status": "in_progress",
            "device": {
                "id": 3449992,
                "name": "TEST\\A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": None,
            "metrics": {
                "average_system_memory_in_use": 70.0,
                "osquery_creation_time_unix_ms": 1.600804383268E12,
                "total_cpu_peak": 0.0
            },
            "start_time": "2020-09-22T19:52:58.114Z",
            "finish_time": None,
            "update_time": "2020-09-22T19:52:58.124Z"
        },
        {
            "total_results": 0,
            "status": "not_matched",
            "device": {
                "id": 3602314,
                "name": "desktop1-A1B2C3D4F",
                "policy_id": 6525,
                "policy_name": "default",
                "os": "WINDOWS"
            },
            "error_description": "",
            "metrics": {
                "average_system_memory_in_use": 57.0,
                "osquery_creation_time_unix_ms": 1.600804359063E12,
                "total_cpu_peak": 14.29,
                "osquery_current_memory_in_use_mb": 0.0,
                "current_misc_io_operation_rate": 162.0,
                "current_misc_io_transfer_rate_kb": 4.0,
                "current_system_memory_in_use_mb": 2342.0,
                "current_write_transfer_rate_kb": 0.0,
                "total_cpu_current": 14.29,
                "total_write_operations": 1.0,
                "average_read_transfer_rate_kb": 0.0,
                "average_write_operation_rate": 1.0,
                "current_system_memory_available": 43.0,
                "osquery_life_time_ms": 280.0,
                "total_read_operations": 4.0,
                "average_misc_io_transfer_rate_kb": 4.0,
                "total_cpu_average": 14.29,
                "current_system_memory_in_use": 57.0,
                "peak_system_memory_available": 43.0,
                "kernel_cpu_average": 14.29,
                "total_write_transfer_count_mb": 0.0,
                "osquery_peak_memory_in_use_mb": 14.0,
                "average_misc_io_operation_rate": 162.0,
                "average_system_memory_in_use_mb": 2345.0,
                "average_read_operation_rate": 0.0,
                "peak_system_memory_in_use": 57.0,
                "current_read_operation_rate": 0.0,
                "osquery_total_kernel_mode_time_ms": 46.0,
                "kernel_cpu_peak": 14.29,
                "osquery_average_percent_of_memory_in_use": 0.31,
                "average_write_transfer_rate_kb": 0.0,
                "average_system_memory_available": 43.0,
                "osquery_average_memory_in_use_mb": 7.0,
                "total_read_transfer_count_mb": 0.0,
                "user_cpu_average": 0.0,
                "peak_system_memory_available_mb": 1752.0,
                "peak_system_memory_in_use_mb": 2347.0,
                "current_system_memory_available_mb": 1752.0,
                "current_read_transfer_rate_kb": 0.0,
                "kernel_cpu_current": 14.29,
                "total_misc_io_transfer_count_mb": 0.0,
                "osquery_current_percent_of_all_memory": 0.0,
                "osquery_peak_percent_of_memory_in_use": 0.63,
                "user_cpu_peak": 0.0,
                "osquery_current_percent_of_memory_in_use": 0.0,
                "average_system_memory_available_mb": 1750.0,
                "osquery_total_user_mode_time_ms": 62.0,
                "total_misc_io_operations": 344.0,
                "current_write_operation_rate": 1.0,
                "osquery_peak_percent_of_all_memory": 0.84,
                "osquery_average_percent_of_all_memory": 0.42,
                "process_monitoring_rate_ms": 500.0,
                "user_cpu_current": 0.0,
                "osquery_exit_time_unix_ms": 1.600804359343E12
            },
            "start_time": "2020-09-22T19:52:38.676Z",
            "finish_time": "2020-09-22T19:53:40.056Z",
            "update_time": "2020-09-22T19:53:41.542Z"
        }
    ]
}

GET_RESULTS_FACETS_RESP = {
    "terms": [
        {
            "field": "device.policy_id",
            "values": [
                {
                    "id": "idOfFieldBeingEnumerated",
                    "name": "policyId1",
                    "total": 1
                }
            ]
        }
    ]
}

POST_RUN_HISTORY_RESP = {
    "org_key": "test",
    "num_found": 7,
    "results": [
        {
            "org_key": "test",
            "name": "Find Programs Installed in Non-Standard Windows Locations",
            "id": "9cpymo06omijuveboi3zomfigc8sosrd",
            "sql": "SELECT path, DATETIME(atime,\"unixepoch\",\"localtime\") AS \"Last Accessed\", DATETIME(mtime,\"unixepoch\",\"localtime\") AS \"Last Modified\", DATETIME(ctime,\"unixepoch\",\"localtime\") AS \"Created\" FROM file WHERE path LIKE \"\\users\\%\\AppData\\%.exe\" OR path LIKE \"\\users\\%\\AppData\\Roaming\\%.exe\" OR path LIKE \"\\ProgramData\\%.exe\";",  # noqa: E501
            "created_by": "A1B2C3",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-09-22T19:52:05.076Z",
            "status_update_time": "2020-09-22T19:52:05.076Z",
            "timeout_time": "2020-09-29T19:52:05.076Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 50,
            "status": "ACTIVE",
            "device_filter": {
                "policy_id": None,
                "os": [
                    "WINDOWS"
                ],
                "device_id": None,
                "deployment_type": None,
                "policy_ids": None,
                "device_types": [
                    "WINDOWS"
                ],
                "device_ids": None
            },
            "recommended_query_id": None,
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": "2020-09-23T03:19:47.211Z",
            "total_results": 3,
            "not_started_count": 9,
            "match_count": 2,
            "no_match_count": 35,
            "success_count": 37,
            "in_progress_count": 2,
            "error_count": 2,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": "Dell SafeBIOS Verification Status",
            "id": "2gm989gsbqx0hmplmbjoqntonbvmtdtx",
            "sql": "WITH b1 AS\n  (SELECT COUNT(*) AS cnt,\n          1 AS one\n   FROM registry\n   WHERE PATH LIKE 'HKEY_LOCAL_MACHINE\\SOFTWARE\\DELL\\BIOSVerification\\%'\n     AND name = 'Result.json'\n     AND DATA LIKE '%\"biosVerification\":\"True\"%' ),\n     b2 AS\n  (SELECT COUNT(*) AS cnt,\n          1 AS one\n   FROM registry\n   WHERE PATH LIKE 'HKEY_LOCAL_MACHINE\\SOFTWARE\\DELL\\BIOSVerification\\%'\n     AND name = 'Result.json'\n     AND DATA LIKE '%\"biosVerification\":\"False\"%' ),\n     b3 AS\n  (SELECT COUNT (*) AS cnt,\n                1 AS one\n   FROM FILE\n   WHERE PATH LIKE '\\Program Files\\Dell\\TrustedDevice\\Dell.TrustedDevice.Service.Console.exe' ),\n     b4 AS\n  (SELECT COUNT (*) AS cnt,\n                1 AS one\n   FROM FILE\n   WHERE PATH like '\\Program Files\\Dell\\BIOSVerification\\Dell.SecurityCenter.Agent.Console.exe' ),\n     b5 AS\n  (SELECT count(*),\n          VERSION,\n          1 AS one\n   FROM programs\n   WHERE name LIKE '%BIOS Verification%'\n     OR name LIKE '%trusted device%' ),\n     b6 AS\n  (SELECT hardware_vendor,\n          hardware_model,\n          1 AS one\n   FROM system_info),\n     b7 AS\n  (SELECT count(*),\n          DATETIME(mtime, 'unixepoch') AS mtime,\n          1 AS one\n   FROM FILE\n   WHERE PATH = 'C:\\ProgramData\\Dell\\BIOSVerification\\result.json' )\nSELECT CASE\n           WHEN b1.cnt = 1 THEN \"PASSED\"\n           WHEN b2.cnt = 1 THEN \"FAILED\"\n           WHEN (b1.cnt = 0\n                 AND b2.cnt = 0) THEN \"NOT AVAILABLE\"\n       END \"BIOS_verification_status\",\n       CASE\n           WHEN b3.cnt = 1 THEN \"True\"\n           WHEN b4.cnt = 1 THEN \"True\"\n           WHEN (b3.cnt = 0\n                 AND b4.cnt = 0) THEN \"False\"\n       END \"Dell_TD_installed\",\n       CASE\n           WHEN b5.version IS NOT None THEN b5.version\n           WHEN b5.version IS None THEN \"N/A\"\n       END \"Dell_TD_version\",\n       CASE\n           WHEN b6.hardware_vendor like 'Dell%' THEN b6.hardware_model\n           WHEN b6.hardware_vendor not like 'Dell%' THEN \"UNSUPPORTED\"\n       END \"HARDWARE_MODEL\",\n       CASE\n           WHEN b7.mtime IS NOT None THEN b7.mtime\n           WHEN b7.mtime IS None THEN \"NOT AVAILABLE\"\n       END \"LAST_RUNTIME\"\nFROM b1\nJOIN b2 USING(one)\nJOIN b3 USING(one)\nJOIN b4 USING(one)\nJOIN b5 USING(one)\nJOIN b6 USING(one)\nJOIN b7 USING(one)\nWHERE b6.hardware_vendor like 'Dell%';",  # noqa: E501
            "created_by": "test@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-07-17T18:49:55.661Z",
            "status_update_time": "2020-07-17T18:51:00.513Z",
            "timeout_time": "2020-07-24T18:49:55.661Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 1,
            "status": "COMPLETE",
            "device_filter": {
                "policy_id": None,
                "os": None,
                "device_id": [
                    12345
                ],
                "deployment_type": None,
                "policy_ids": None,
                "device_types": None,
                "device_ids": [
                    12345
                ]
            },
            "recommended_query_id": "ed67d15cdb5ec30f1f0d8eb7",
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": "Detect sdelete.exe Execution",
            "id": "t7lknmp40tio2w45oxsxoayqb6j6saon",
            "sql": "SELECT filename,\n       datetime(atime, \"unixepoch\", \"localtime\") AS atime,\n       datetime(ctime, \"unixepoch\", \"localtime\") AS ctime,\n       datetime(mtime, \"unixepoch\", \"localtime\") AS mtime\nFROM FILE\nWHERE PATH LIKE \"\\Windows\\prefetch\\sdelete.exe%\";",  # noqa: E501
            "created_by": "example@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-06-01T11:09:13.503Z",
            "status_update_time": "2020-06-02T07:51:14.560Z",
            "timeout_time": "2020-06-08T11:09:13.503Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 28,
            "status": "COMPLETE",
            "device_filter": {
                "policy_id": None,
                "os": [
                    "WINDOWS"
                ],
                "device_id": None,
                "deployment_type": None,
                "policy_ids": None,
                "device_types": [
                    "WINDOWS"
                ],
                "device_ids": None
            },
            "recommended_query_id": None,
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": "Detect sdelete.exe Execution",
            "id": "ll7kypanfakakc3rvw0phdfdlldol0sp",
            "sql": "SELECT filename,\n       datetime(atime, \"unixepoch\", \"localtime\") AS atime,\n       datetime(ctime, \"unixepoch\", \"localtime\") AS ctime,\n       datetime(mtime, \"unixepoch\", \"localtime\") AS mtime\nFROM FILE\nWHERE PATH LIKE \"\\Windows\\prefetch\\sdelete.exe%\";",  # noqa: E501
            "created_by": "example@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-05-31T13:13:02.669Z",
            "status_update_time": "2020-06-02T07:51:12.652Z",
            "timeout_time": "2020-06-07T13:13:02.669Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 28,
            "status": "COMPLETE",
            "device_filter": {
                "policy_id": None,
                "os": [
                    "WINDOWS"
                ],
                "device_id": None,
                "deployment_type": None,
                "policy_ids": None,
                "device_types": [
                    "WINDOWS"
                ],
                "device_ids": None
            },
            "recommended_query_id": "22af467428fb7be4573f840d",
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": "YairTest2",
            "id": "78c7ghmw6m5qn7kpflace0qbtgkac4xn",
            "sql": "SELECT filename, path FROM file LIMIT 1",
            "created_by": "example@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-05-17T14:03:04.513Z",
            "status_update_time": "2020-05-17T14:03:52.812Z",
            "timeout_time": "2020-05-24T14:03:04.513Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 1,
            "status": "COMPLETE",
            "device_filter": {
                "policy_id": None,
                "os": None,
                "device_id": [
                    3444087
                ],
                "deployment_type": None,
                "policy_ids": None,
                "device_types": None,
                "device_ids": [
                    3444087
                ]
            },
            "recommended_query_id": None,
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": "YairTest",
            "id": "wb1is6dma49ermnggn9iupvrf7yzz0rf",
            "sql": "SELECT filename, path FROM file LIMIT 1",
            "created_by": "example@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2020-05-17T14:02:31.375Z",
            "status_update_time": "2020-05-17T14:02:44.751Z",
            "timeout_time": "2020-05-24T14:02:31.375Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 1,
            "status": "COMPLETE",
            "device_filter": {
                "policy_id": None,
                "os": None,
                "device_id": [
                    3371328
                ],
                "deployment_type": None,
                "policy_ids": None,
                "device_types": None,
                "device_ids": [
                    3371328
                ]
            },
            "recommended_query_id": None,
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        },
        {
            "org_key": "test",
            "name": None,
            "id": "coulq8iz842cwif9rjhnb1fh1uxehini",
            "sql": "SELECT f.filename, f.path, u.username, h.sha256,\n   datetime(f.atime,\"unixepoch\",\"localtime\") AS atime,\n   datetime(f.ctime,\"unixepoch\",\"localtime\") AS ctime,\n   datetime(f.mtime,\"unixepoch\",\"localtime\") AS mtime\nFROM file as f\nJOIN users AS u USING(uid)\nJOIN hash AS h USING(path)\nWHERE ((filename like \"%passw%\") OR (filename like \"%pwd%\"));",  # noqa: E501
            "created_by": "example@email.com",
            "destinations": [
                "LQ"
            ],
            "create_time": "2019-11-12T06:26:07.905Z",
            "status_update_time": "2019-11-13T23:33:54.067Z",
            "timeout_time": "2019-11-19T06:26:07.905Z",
            "cancellation_time": None,
            "cancelled_by": None,
            "archive_time": None,
            "archived_by": None,
            "notify_on_finish": False,
            "active_org_devices": 20,
            "status": "COMPLETE",
            "device_filter": None,
            "recommended_query_id": None,
            "template_id": None,
            "schedule": None,
            "schema": None,
            "last_result_time": None,
            "total_results": 0,
            "not_started_count": 0,
            "match_count": 0,
            "no_match_count": 0,
            "success_count": 0,
            "in_progress_count": 0,
            "error_count": 0,
            "not_supported_count": 0,
            "cancelled_count": 0
        }
    ]
}

GET_RUN_RESULTS_RESP_OVER_10k = {
    "org_key": "A1B2C3D4E5",
    "num_found": 10001,
    "results": [
        {
            "id": "run_id",
            "device": {
                "id": 12345,
                "name": "deviceName0",
                "policy_id": 98765,
                "policy_name": "device0policy",
                "os": "WINDOWS"
            },
            "status": "not_matched",
            "time_received": "2020-09-22T09:53:48.313Z",
            "device_message": "",
            "fields": {}
        }
    ]
}
