"""Mock data for Live Query templates"""

EXAMPLE_TEMPLATE = {
    'id': 'xzllqfvlie2bzghqqfkxk9xizqniwcvr',
    'name': 'CBC SDK',
    'created_by': 'ABCDE12345',
    'create_time': '2020-12-10T23:42:28.359Z',
    'update_time': '2020-12-10T23:42:28.359Z',
    'notify_on_finish': False,
    'device_filter': {
        'policy_id': None,
        'os': ['WINDOWS'],
        'device_id': None,
        'deployment_type': None,
        'policy_ids': None,
        'device_types': ['WINDOWS'],
        'device_ids': None
    },
    'sql': 'SELECT name, VERSION, install_date FROM programs;',
    'last_run_create_time': None,
    'next_run_time': '2020-12-11T18:30:00.000Z',
    'schedule': {
        'status': 'ACTIVE',
        'recurrence': 'DAILY',
        'timezone': 'America/New_York',
        'rrule': 'FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0',
        'previous_run_time': None,
        'next_run_time': '2020-12-11T18:30:00.000Z',
        'cancellation_time': None,
        'cancelled_by': None
    },
    'recommended_query_id': None,
    'schema': None,
    'destinations': ['LQ']
}

EXAMPLE_TEMPLATE_REFRESH = {
    'id': 'xzllqfvlie2bzghqqfkxk9xizqniwcvr',
    'name': 'CBC SDK',
    'created_by': 'ABCDE12345',
    'create_time': '2020-12-10T23:42:28.359Z',
    'update_time': '2020-12-10T23:42:28.359Z',
    'notify_on_finish': False,
    'device_filter': {
        'policy_id': None,
        'os': ['WINDOWS'],
        'device_id': None,
        'deployment_type': None,
        'policy_ids': None,
        'device_types': ['WINDOWS'],
        'device_ids': None
    },
    'sql': 'SELECT name, VERSION, install_date FROM programs;',
    'last_run_create_time': '2020-12-11T18:30:00.000Z',
    'next_run_time': '2020-12-12T18:30:00.000Z',
    'schedule': {
        'status': 'ACTIVE',
        'recurrence': 'DAILY',
        'timezone': 'America/New_York',
        'rrule': 'FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0',
        'previous_run_time': '2020-12-11T18:30:00.000Z',
        'next_run_time': '2020-12-12T18:30:00.000Z',
        'cancellation_time': None,
        'cancelled_by': None
    },
    'recommended_query_id': None,
    'schema': None,
    'destinations': ['LQ']
}

EXAMPLE_TEMPLATE_STOPPED = {
    'id': 'xzllqfvlie2bzghqqfkxk9xizqniwcvr',
    'name': 'CBC SDK',
    'created_by': 'ABCDE12345',
    'create_time': '2020-12-10T23:42:28.359Z',
    'update_time': '2020-12-10T23:58:48.283Z',
    'notify_on_finish': False,
    'device_filter': {
        'policy_id': None,
        'os': ['WINDOWS'],
        'device_id': None,
        'deployment_type': None,
        'policy_ids': None,
        'device_types': ['WINDOWS'],
        'device_ids': None
    },
    'sql': 'SELECT name, VERSION, install_date FROM programs;',
    'last_run_create_time': None,
    'next_run_time': None,
    'schedule': {
        'status': 'CANCELLED',
        'recurrence': 'DAILY',
        'timezone': 'America/New_York',
        'rrule': 'FREQ=DAILY;BYHOUR=13;BYMINUTE=30;BYSECOND=0',
        'previous_run_time': None,
        'next_run_time': None,
        'cancellation_time': '2020-12-10T23:58:48.283Z',
        'cancelled_by': 'ABCDE12345'
    },
    'recommended_query_id': None,
    'schema': None,
    'destinations': ['LQ']
}
