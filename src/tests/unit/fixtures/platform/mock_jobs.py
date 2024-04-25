"""Mock responses for Job"""

_JOB1 = {
    "id": 12345,
    "type": "livequery_export",
    "job_parameters": {
        "job_parameters": None
    },
    "connector_id": "ABCDEFGHIJ",
    "org_key": "test",
    "status": "COMPLETED",
    "progress": {
        "num_total": 18,
        "num_completed": 18
    },
    "create_time": "2022-01-04T19:18:58.213Z",
    "last_update_time": "2022-01-04T19:18:59.385Z"
}


_JOB2 = {
    "id": 23456,
    "type": "livequery_export",
    "job_parameters": {
        "job_parameters": None
    },
    "connector_id": "ABCDEFGHIJ",
    "org_key": "test",
    "status": "CREATED",
    "progress": {
        "num_total": 34,
        "num_completed": 16
    },
    "create_time": "2022-01-04T19:18:58.213Z",
    "last_update_time": "2022-01-04T19:18:59.385Z"
}


FIND_ALL_JOBS_RESP = {
    "num_found": 2,
    "results": [_JOB1, _JOB2]
}

JOB_DETAILS_1 = _JOB1

JOB_DETAILS_2 = _JOB2

PROGRESS_1 = {
    "num_total": 18,
    "num_completed": 18
}

PROGRESS_2 = {
    "num_total": 34,
    "num_completed": 16,
    "message": "Foo"
}

AWAIT_COMPLETION_DETAILS_PROGRESS_1 = ["CREATED", "CREATED", "CREATED", "COMPLETED"]

AWAIT_COMPLETION_DETAILS_PROGRESS_2 = ["CREATED", "CREATED", "CREATED", "FAILED"]
