"""Mock command responses for Live Response."""

DIRECTORY_LIST_START_RESP = {
    'id': 6,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'directory list',
    'object': 'C:\\\\TEMP\\\\',
    'completion_time': 0
}

DIRECTORY_LIST_END_RESP = {
    'id': 6,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'directory list',
    'object': 'C:\\\\TEMP\\\\',
    'completion_time': 2345678901,
    'files': [
        {
            'attributes': ['DIRECTORY'],
            'create_time': 1471897244,
            'filename': '.',
            'last_access_time': 1476390670,
            'last_write_time': 1476390670,
            'size': 0
        },
        {
            'attributes': ['DIRECTORY'],
            'create_time': 1471897244,
            'filename': '..',
            'last_access_time': 1476390670,
            'last_write_time': 1476390670,
            'size': 0
        },
        {
            'attributes': ['ARCHIVE'],
            'create_time': 1476390668,
            'filename': 'test.txt',
            'last_access_time': 1476390668,
            'last_write_time': 1476390668,
            'size': 1234
        }
    ]
}

DELETE_FILE_START_RESP = {
    'id': 3,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'delete file',
    'object': 'C:\\\\TEMP\\\\foo.txt',
    'completion_time': 0
}

DELETE_FILE_END_RESP = {
    'id': 3,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'delete file',
    'object': 'C:\\\\TEMP\\\\foo.txt',
    'completion_time': 2345678901
}

DELETE_FILE_ERROR_RESP = {
    'id': 3,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'error',
    'name': 'delete file',
    'object': 'C:\\\\TEMP\\\\foo.txt',
    'completion_time': 2345678901,
    'result_code': -2147024894,
    'result_type': 'WinHresult',
    'result_desc': 'File not found'
}

PUT_FILE_START_RESP = {
    'id': 6,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'put file',
    'object': 'foobar.txt',
    'completion_time': 0
}

PUT_FILE_END_RESP = {
    'id': 6,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'put file',
    'object': 'foobar.txt',
    'completion_time': 2345678901
}

CREATE_DIRECTORY_START_RESP = {
    'id': 7,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'create directory',
    'object': 'C:\\\\TEMP\\\\TRASH',
    'completion_time': 0
}

CREATE_DIRECTORY_END_RESP = {
    'id': 7,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'create directory',
    'object': 'C:\\\\TEMP\\\\TRASH',
    'completion_time': 2345678901
}

WALK_RETURN_1 = [
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '.',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '..',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': 'FOO',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': 'BAR',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['ARCHIVE'],
        'create_time': 1476390668,
        'filename': 'test.txt',
        'last_access_time': 1476390668,
        'last_write_time': 1476390668,
        'size': 1234
    }
]

WALK_RETURN_2 = [
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '.',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '..',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['ARCHIVE'],
        'create_time': 1476390668,
        'filename': 'hoopy.doc',
        'last_access_time': 1476390668,
        'last_write_time': 1476390668,
        'size': 1234
    },
    {
        'attributes': ['ARCHIVE'],
        'create_time': 1476390668,
        'filename': 'frood.doc',
        'last_access_time': 1476390668,
        'last_write_time': 1476390668,
        'size': 1234
    }
]

WALK_RETURN_3 = [
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '.',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['DIRECTORY'],
        'create_time': 1471897244,
        'filename': '..',
        'last_access_time': 1476390670,
        'last_write_time': 1476390670,
        'size': 0
    },
    {
        'attributes': ['ARCHIVE'],
        'create_time': 1476390668,
        'filename': 'evil.exe',
        'last_access_time': 1476390668,
        'last_write_time': 1476390668,
        'size': 1234
    }
]

KILL_PROC_START_RESP = {
    'id': 13,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'kill',
    'object': 601,
    'completion_time': 0
}

KILL_PROC_END_RESP = {
    'id': 13,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'kill',
    'object': 601,
    'completion_time': 2345678901
}

CREATE_PROC_START_RESP = {
    'id': 52,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'create process',
    'object': 'start_daemon',
    'completion_time': 0
}

CREATE_PROC_END_RESP = {
    'id': 52,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'create process',
    'object': 'start_daemon',
    'completion_time': 2345678901
}

RUN_PROC_START_RESP = {
    'id': 9,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'create process',
    'object': 'gimme',
    'completion_time': 0
}

RUN_PROC_END_RESP = {
    'id': 9,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'create process',
    'object': 'gimme',
    'completion_time': 2345678901
}

LIST_PROC_START_RESP = {
    'id': 10,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'process list',
    'object': None,
    'completion_time': 0
}

LIST_PROC_END_RESP = {
    'id': 10,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'process list',
    'object': None,
    'completion_time': 2345678901,
    'processes': [
        {
            'pid': 303,
            'create_time': 1476390670,
            'proc_guid': '6EDF43E9-11B3-469F-B80F-D7917D60CC62',
            'path': 'proc1',
            'command_line': 'proc1',
            'sid': 'S-1-4-888',
            'username': 'root',
            'parent': 1,
            'parent_guid': 'D0A5F3CA-E08D-41CA-8FDF-BBF95850752F'
        },
        {
            'pid': 805,
            'create_time': 1476390670,
            'proc_guid': '17FD30A5-B8BF-41F9-8B38-4137B7241D4B',
            'path': 'server',
            'command_line': 'server',
            'sid': 'S-1-4-888',
            'username': 'root',
            'parent': 1,
            'parent_guid': 'D0A5F3CA-E08D-41CA-8FDF-BBF95850752F'
        },
        {
            'pid': 1024,
            'create_time': 1476390670,
            'proc_guid': '5EC3FFCA-238C-496E-ADEA-DF4F9EC4F473',
            'path': 'borg',
            'command_line': 'borg',
            'sid': 'S-1-4-888',
            'username': 'root',
            'parent': 1,
            'parent_guid': 'D0A5F3CA-E08D-41CA-8FDF-BBF95850752F'
        }
    ]
}

REG_ENUM_START_RESP = {
    'id': 56,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg enum key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI',
    'completion_time': 0
}

REG_ENUM_END_RESP = {
    'id': 56,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg enum key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI',
    'completion_time': 2345678901,
    'sub_keys': ['Parameters', 'Enum'],
    'values': [
        {'value_data': 0,
         'value_name': 'Start',
         'value_type': 'REG_DWORD'},
        {'value_data': 1,
         'value_name': 'Type',
         'value_type': 'REG_DWORD'},
        {'value_data': 3,
         'value_name': 'ErrorControl',
         'value_type': 'REG_DWORD'},
        {'value_data': 'system32\\drivers\\ACPI.sys',
         'value_name': 'ImagePath',
         'value_type': 'REG_EXPAND_SZ'},
        {'value_data': 'Microsoft ACPI Driver',
         'value_name': 'DisplayName',
         'value_type': 'REG_SZ'},
        {'value_data': 'Boot Bus Extender',
         'value_name': 'Group',
         'value_type': 'REG_SZ'},
        {'value_data': 'acpi.inf_x86_neutral_ddd3c514822f1b21',
         'value_name': 'DriverPackageId',
         'value_type': 'REG_SZ'},
        {'value_data': 1,
         'value_name': 'Tag',
         'value_type': 'REG_DWORD'}
    ]
}

REG_GET_START_RESP = {
    'id': 61,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg query value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Start',
    'completion_time': 0
}

REG_GET_END_RESP = {
    'id': 61,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg query value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Start',
    'completion_time': 2345678901,
    'value': {'value_data': 0, 'value_name': 'Start', 'value_type': 'REG_DWORD'}
}

REG_SET_START_RESP = {
    'id': 62,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg set value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
    'completion_time': 0
}

REG_SET_END_RESP = {
    'id': 62,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg set value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
    'completion_time': 2345678901
}

REG_CREATE_KEY_START_RESP = {
    'id': 63,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg create key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
    'completion_time': 0
}

REG_CREATE_KEY_END_RESP = {
    'id': 63,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg create key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
    'completion_time': 2345678901
}

REG_DELETE_KEY_START_RESP = {
    'id': 64,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg delete key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
    'completion_time': 0
}

REG_DELETE_KEY_END_RESP = {
    'id': 64,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg delete key',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
    'completion_time': 2345678901
}

REG_DELETE_START_RESP = {
    'id': 65,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'reg delete value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
    'completion_time': 0
}

REG_DELETE_END_RESP = {
    'id': 65,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'reg delete value',
    'object': 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
    'completion_time': 2345678901
}

MEMDUMP_START_RESP = {
    'id': 101,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'memdump',
    'object': None,
    'completion_time': 0,
    'return_code': 0,
    'complete': False,
    'percentdone': 0,
    'dumping': True
}

MEMDUMP_END_RESP = {
    'id': 101,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'memdump',
    'object': None,
    'completion_time': 2345678901,
    'return_code': 0,
    'complete': True,
    'percentdone': 100,
    'dumping': False
}

MEMDUMP_DEL_START_RESP = {
    'id': 102,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'in progress',
    'name': 'delete file',
    'object': None,
    'completion_time': 0
}

MEMDUMP_DEL_END_RESP = {
    'id': 102,
    'session_id': '1:2468',
    'sensor_id': 2468,
    'command_timeout': 120,
    'status': 'complete',
    'name': 'delete file',
    'object': None,
    'completion_time': 2345678901
}
