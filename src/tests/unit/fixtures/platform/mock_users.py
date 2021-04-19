"""Mock responses for User"""

_USER1 = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 3911,
    "org_id": 1,
    "login_name": "emercer@orville.planetary-union.net",
    "email": "emercer@orville.planetary-union.net",
    "last_name": "Mercer",
    "phone": "303-555-1234",
    "first_name": "Ed",
    "admin_login_version": 6,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 98153,
    "contact_version": 0
}

_USER2 = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 3934,
    "org_id": 1,
    "login_name": "mreynolds@browncoats.org",
    "email": "mreynolds@browncoats.org",
    "last_name": "Malcolm",
    "phone": "720-555-2345",
    "first_name": "Reynolds",
    "admin_login_version": 8,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 100754,
    "contact_version": 0
}

_USER3 = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 4338,
    "org_id": 1,
    "login_name": "djackson@stargate-command.af.mil",
    "email": "djackson@stargate-command.af.mil",
    "last_name": "Jackson",
    "phone": "213-555-3456",
    "first_name": "Daniel",
    "admin_login_version": 3,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 114475,
    "contact_version": 0
}

_USER4 = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 6942,
    "org_id": 1,
    "login_name": "jsheridan@babylon5.com",
    "email": "jsheridan@babylon5.com",
    "last_name": "Sheridan",
    "phone": "714-555-4567",
    "first_name": "John",
    "admin_login_version": 317,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 4,
    "contact_version": 0
}

_USER5 = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 3978,
    "org_id": 1,
    "login_name": "bmariner@cerritos.starfleet.mil",
    "email": "bmariner@cerritos.starfleet.mil",
    "last_name": "Mariner",
    "phone": "619-555-5678",
    "first_name": "Beckett",
    "admin_login_version": 10,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 101924,
    "contact_version": 0
}

_USER_NEW = {
    "org_key": "test",
    "auth_method": "PASSWORD",
    "login_id": 6969,
    "org_id": 1,
    "login_name": "rios@la-sirena.net",
    "email": "rios@la-sirena.net",
    "last_name": "Rios",
    "phone": "",
    "first_name": "Cristobal",
    "admin_login_version": 1,
    "org_admin_version": 0,
    "role": "DEPRECATED",
    "contact_id": 142857,
    "contact_version": 0
}

GET_USERS_RESP = {
    'success': True,
    'message': 'Success',
    'users': [_USER1, _USER2, _USER3, _USER4, _USER5]
}

GET_USERS_AFTER_CREATE_RESP = {
    'success': True,
    'message': 'Success',
    'users': [_USER1, _USER2, _USER3, _USER4, _USER5, _USER_NEW]
}

EXPECT_USER_ADD = {
    "org_id": 0,
    "email_id": "rios@la-sirena.net",
    "role": "DEPRECATED",
    "role_urn": "psc:role:test:APP_SERVICE_ROLE",
    "first_name": "Cristobal",
    "last_name": "Rios",
    "auth_method": "PASSWORD",
    "profiles": [
        {
            'orgs': {
                'allow': ['psc:org:test2']
            },
            'roles': ['psc:role:test2:DUMMY']
        },
        {
            'orgs': {
                'allow': ['psc:org:test3']
            },
            'roles': ['psc:role:test3:DUMMY']
        }
    ]
}

EXPECT_USER_ADD_SMALL = {
    "org_id": 0,
    "email_id": "rios@la-sirena.net",
    "role": "DEPRECATED",
    "role_urn": "psc:role:test:APP_SERVICE_ROLE",
    "first_name": "Cristobal",
    "last_name": "Rios",
    "auth_method": "PASSWORD",
    "profiles": [
        {
            'orgs': {
                'allow': ['psc:org:test2']
            },
            'roles': ['psc:role:test2:DUMMY']
        }
    ]
}

EXPECT_USER_ADD_V1 = {
    "org_id": 0,
    "email_id": "rios@la-sirena.net",
    "role": "DEPRECATED",
    "role_urn": "psc:role:test:APP_SERVICE_ROLE",
    "first_name": "Cristobal",
    "last_name": "Rios",
    "auth_method": "PASSWORD",
}

EXPECT_USER_ADD_V2 = {
    "org_id": 0,
    "email_id": "rios@la-sirena.net",
    "role": "DEPRECATED",
    "first_name": "Cristobal",
    "last_name": "Rios",
    "auth_method": "PASSWORD",
    "profiles": [
        {
            'orgs': {
                'allow': ['psc:org:test2']
            },
            'roles': ['psc:role:test2:DUMMY']
        }
    ]
}

USER_ADD_SUCCESS_RESP = {
    'password': 'abcd_efgh',
    'login_id': '6969',
    'registration_type': 'SUCCESS'
}

USER_ADD_FAILURE_RESP = {
    'password': '',
    'login_id': '',
    'registration_type': 'ERROR'
}
