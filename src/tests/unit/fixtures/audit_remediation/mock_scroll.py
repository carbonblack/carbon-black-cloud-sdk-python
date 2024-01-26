"""Mocks for Live Query Result Scroll"""

SINGLE_RESULT = {
    "id": "oc5c5q9yc1mv107wuaxj6xqpmaoezwrh",
    "device": {
        "id": 21665421,
        "name": "psc-auto-centos75",
        "policy_id": 17567367,
        "policy_name": "0",
        "os": "LINUX"
    },
    "status": "matched",
    "time_received": "2023-12-11T19:02:40.579Z",
    "device_message": "",
    "fields": {
        "cmdline": "/usr/sbin/NetworkManager --no-daemon",
        "cwd": "/",
        "name": "NetworkManager",
        "on_disk": 1,
        "path": "/usr/sbin/NetworkManager"
    }
}


def GET_SCROLL_RESULTS(rows, num_found, num_remaining):
    """Generate results response based on num_remaining"""
    return {
        "org_key": "test",
        "num_found": num_found,
        "num_remaining": num_remaining,
        "search_after": "MTcwMjMyMTM2MDU3OSwyMT" if num_remaining > 0 else "",
        "results": [SINGLE_RESULT for _ in range(rows)]
    }
