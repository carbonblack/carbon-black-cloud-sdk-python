"""Mock responses for enriched event queries."""

POST_ENRICHED_EVENTS_SEARCH_JOB_RESP = {
    'job_id': '08ffa932-b633-4107-ba56-8741e929e48b'
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP = {
    'contacted': 41,
    'completed': 41,
    'query': {
        'cb.event_docs': True,
        'cb.max_backend_timestamp': 1603973841000,
        'cb.min_backend_timestamp': 0,
        'cb.min_device_timestamp': 0,
        'cb.preview_results': 500,
        'cb.use_agg': True,
        'facet': False,
        'fq': '{!collapse field=event_id sort="device_timestamp desc"}',
        'q': '(process_pid:1000 OR process_pid:2000)',
        'rows': 500,
        'start': 0
    },
    'search_initiated_time': 1603973841206,
    'connector_id': 'P1PFUIAN32'
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_1 = {
    'num_found': 808,
    'num_available': 52,
    'contacted': 6,
    'completed': 6,
    'results': [
        {
            'backend_timestamp': '2020-10-23T08:25:24.797Z',
            'device_group_id': 0,
            'device_id': 215209,
            'device_name': 'scarpaci-win10-eap01',
            'device_policy_id': 2203,
            'device_timestamp': '2020-10-23T08:24:22.624Z',
            'enriched': True,
            'enriched_event_type': 'SYSTEM_API_CALL',
            'event_description': 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open itself for modification, by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
            'event_id': '27a278d5150911eb86f1011a55e73b72',
            'event_type': 'crossproc',
            'ingress_time': 1603441488750,
            'legacy': True,
            'org_id': 'WNEXFKQ7',
            'parent_guid': 'WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd',
            'parent_pid': 884,
            'process_guid': 'WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86',
            'process_hash': [
                '47a61bee31164ea1dd671d695424722e',
                '6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786'
            ],
            'process_name': 'c:\\windows\\system32\\wbem\\scrcons.exe',
            'process_pid': [1000],
            'process_username': ['NT AUTHORITY\\SYSTEM']
        },
    ]
}

GET_ENRICHED_EVENTS_SEARCH_JOB_RESULTS_RESP_2 = {
    'num_found': 808,
    'num_available': 52,
    'contacted': 6,
    'completed': 6,
    'results': [
        {
            'backend_timestamp': '2020-10-23T08:25:24.797Z',
            'device_group_id': 0,
            'device_id': 215209,
            'device_name': 'scarpaci-win10-eap01',
            'device_policy_id': 2203,
            'device_timestamp': '2020-10-23T08:24:22.624Z',
            'enriched': True,
            'enriched_event_type': 'SYSTEM_API_CALL',
            'event_description': 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open itself for modification, by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
            'event_id': '27a278d5150911eb86f1011a55e73b72',
            'event_type': 'crossproc',
            'ingress_time': 1603441488750,
            'legacy': True,
            'org_id': 'WNEXFKQ7',
            'parent_guid': 'WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd',
            'parent_pid': 884,
            'process_guid': 'WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86',
            'process_hash': [
                '47a61bee31164ea1dd671d695424722e',
                '6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786'
            ],
            'process_name': 'c:\\windows\\system32\\wbem\\scrcons.exe',
            'process_pid': [1000],
            'process_username': ['NT AUTHORITY\\SYSTEM']
        },
        {
            'backend_timestamp': '2020-10-23T08:25:24.797Z',
            'device_group_id': 0,
            'device_id': 215209,
            'device_name': 'scarpaci-win10-eap01',
            'device_policy_id': 2203,
            'device_timestamp': '2020-10-23T08:24:22.271Z',
            'enriched': True,
            'enriched_event_type': 'SYSTEM_API_CALL',
            'event_description': 'The application "<share><link hash="6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786">C:\\windows\\system32\\wbem\\scrcons.exe</link></share>" attempted to open the process "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18.2009.7-0\\MsMpEng.exe", by calling the function "OpenProcess". The operation was successful.',  # noqa: E501
            'event_id': '27a278d2150911eb86f1011a55e73b72',
            'event_type': 'crossproc',
            'ingress_time': 1603441488750,
            'legacy': True,
            'org_id': 'WNEXFKQ7',
            'parent_guid': 'WNEXFKQ7-000348a9-00000374-00000000-1d691b52d77fbcd',
            'parent_pid': 884,
            'process_guid': 'WNEXFKQ7-000348a9-000003e8-00000000-1d6a915e8ccce86',
            'process_hash': [
                '47a61bee31164ea1dd671d695424722e',
                '6c02d54afe705d7df7db7ee94d92afdefb2fb91f9d1805c970126a096df52786'
            ],
            'process_name': 'c:\\windows\\system32\\wbem\\scrcons.exe',
            'process_pid': [2000],
            'process_username': ['NT AUTHORITY\\SYSTEM']
        },
    ]
}

GET_ENRICHED_EVENTS_AGGREGATION_JOB_RESULTS_RESP_1 = {
    'results': [
        {
            'alert_id': ['null/99FI049P'],
            'backend_timestamp': '2020-06-25T21:05:10.787Z',
            'device_id': 195940,
            'device_name': 'desktop-8qonquj',
            'device_os': 'WINDOWS',
            'device_policy': 'default',
            'device_policy_id': 2198,
            'device_timestamp': '2020-06-25T20:36:06.608Z',
            'enriched': True,
            'enriched_event_type': 'CREATE_PROCESS',
            'event_description': 'test',
            'event_id': '8ff185c2b72311eaab6d9f3b90c54099',
            'event_type': 'childproc',
            'ingress_time': 1593117428851,
            'legacy': True,
            'num_devices': 1,
            'num_events': 2,
            'org_id': 'WNEXFKQ7',
            'parent_guid': 'WNEXFKQ7-0002fd64-00001ffc-00000000-1d64b3039bb7130',
            'parent_pid': 8188,
            'process_effective_reputation': 'LOCAL_WHITE',
            'process_guid': 'WNEXFKQ7-0002fd64-000007d0-00000000-1d64b30404d93d8',
            'process_hash': [
                '0dde659f0854d78f137119e13e1368ef',
                'de74b04a291133b8c6c5a30bff6b2cef8ad4141cd1813d063c8c62f2671652e8'
            ],
            'process_name': 'c:\\users\\dragon\\.rustup\\toolchains\\stable-x86_64-pc-windows-msvc\\bin\\rustc.exe',
            'process_pid': [2000],
            'process_sha256': 'de74b04a291133b8c6c5a30bff6b2cef8ad4141cd1813d063c8c62f2671652e8',
            'process_username': ['DESKTOP-8QONQUJ\\dragon']
        }
    ],
    'num_found': 1,
    'num_available': 1,
    'contacted': 29,
    'completed': 29
}
