# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Mock responses for event queries."""

EVENT_SEARCH_VALIDATION_RESP = {
    "invalid_message": "string",
    "invalid_trigger_offset": 0,
    "valid": True
}

EVENT_SEARCH_RESP_INTERIM = {
    "results": [
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "v1PSfkXGQAilYw5MYwoWQA",
            "event_hash": "zo-g2PNTSo2ZH23N--07Zw",
            "event_timestamp": "2020-08-26T21:38:17.090Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0d50f3c3d50b878ceae21b9be3f6a638",
            "modload_name": "c:\\windows\\system32\\kernel.appcore.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "bf0b1a5d4cea656695ffb45d930f6add63519aeae9f8aed21e4e50708fe5e84c",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "bYd9BiyVRdSI47Can0LWwA",
            "event_hash": "hg_Y48btT7K7As30HyJYVw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "b83b06508cadbc204b3daeecc395a571",
            "modload_name": "c:\\windows\\system32\\cryptbase.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "10045637aba4ef52f93602f5f78e8a50f2c2d9b2e646d0d0cc91e684c2ad1030",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "7ykrNX5pRTK85QHKnBtDng",
            "event_hash": "DGCt_a2uRI-Jk-aTMMK-Lg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "876a3e1a4db8720df66d653bdbad3e5d",
            "modload_name": "c:\\windows\\system32\\bcryptprimitives.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "6ed5bdc432e5f351e01995d345d296ca67af24b84951268f239c631a544054a5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "b8a3EOR7QX6wV_3QNtsOYQ",
            "event_hash": "ug_dVz7eSl6P1495gtGong",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8513a1e7ae4b9dc82c4b4f432c648a58",
            "modload_name": "c:\\windows\\system32\\profsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c0c629bf79722a12b35bda6d5ef6fd2d96e013d80d8f17077e9137ed3988b452",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "Y8VvqnGqQhe2A5l75G2o1g",
            "event_hash": "fIxqNyHtTFqt2FcOnHzqag",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "64e2c7176d189e4a838d04f7c724cae7",
            "modload_name": "c:\\windows\\system32\\userenv.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "a9ec868ab16c79d00d74d95ef9936772b9d4b7a1e64240534b4646029a207708",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "0MVGeGGHTkmFzdn4PR3gww",
            "event_hash": "dOZfzhW2Qm2wkmll8__dqQ",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "9a1175ef7b9e297fdc0add33783ef8ff",
            "modload_name": "c:\\windows\\system32\\sysntfy.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "0fc1a3942e0f3f1b5fba09598247fcb073150d485b25c4784710904a392b6ccd",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "j27Qsf9ITe66i1ykn_Mrgw",
            "event_hash": "omVbiu7BRkSgr_mc4U5lww",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8ed638461effcf584af5a8c291a2f9df",
            "modload_name": "c:\\windows\\system32\\profapi.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c8414d68e423d345212e90524897b781b944034c385123ded4aca508faddd11e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "RFTB31HjSaab4Tbl8Q8x3A",
            "event_hash": "-tSTPIjBTMueUGaTEC6lJg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "05fbe1f7c13e87af7a414cdf288b1f62",
            "modload_name": "c:\\windows\\system32\\themeservice.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "24079e1a6b2e33a1a8e76a77f73473b93dd6b379e44c982ce50d6ceed9747838",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "JXa204bEQFCVMfTyixps2Q",
            "event_hash": "ZmE7Dbu5RXSKfcq5HHZ69g",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0bde0fcf597e9b65600121ef54ff8340",
            "modload_name": "c:\\windows\\system32\\gpsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "da5c96e84e05ad09251c82b4bfede274342409803730cebf24eead0dcd42da7e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "9JiEKx8JTF-yFVgUftXWAQ",
            "event_hash": "HyaPPGZlQeWWzb7_13Dvhw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "aa9973f611039a02c8d1f71a65f8c775",
            "modload_name": "c:\\windows\\system32\\srvcli.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "2cfce559bed5be35b1970df544e0606af6559e02ef8381ba09270ed5fb8e1bf5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        }
    ],
    "num_found": 250,
    "num_available": 250,
    "total_segments": 7,
    "processed_segments": 3
}

EVENT_SEARCH_RESP = {
    "results": [
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "v1PSfkXGQAilYw5MYwoWQA",
            "event_hash": "zo-g2PNTSo2ZH23N--07Zw",
            "event_timestamp": "2020-08-26T21:38:17.090Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0d50f3c3d50b878ceae21b9be3f6a638",
            "modload_name": "c:\\windows\\system32\\kernel.appcore.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "bf0b1a5d4cea656695ffb45d930f6add63519aeae9f8aed21e4e50708fe5e84c",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "bYd9BiyVRdSI47Can0LWwA",
            "event_hash": "hg_Y48btT7K7As30HyJYVw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "b83b06508cadbc204b3daeecc395a571",
            "modload_name": "c:\\windows\\system32\\cryptbase.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "10045637aba4ef52f93602f5f78e8a50f2c2d9b2e646d0d0cc91e684c2ad1030",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "7ykrNX5pRTK85QHKnBtDng",
            "event_hash": "DGCt_a2uRI-Jk-aTMMK-Lg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "876a3e1a4db8720df66d653bdbad3e5d",
            "modload_name": "c:\\windows\\system32\\bcryptprimitives.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "6ed5bdc432e5f351e01995d345d296ca67af24b84951268f239c631a544054a5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "b8a3EOR7QX6wV_3QNtsOYQ",
            "event_hash": "ug_dVz7eSl6P1495gtGong",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8513a1e7ae4b9dc82c4b4f432c648a58",
            "modload_name": "c:\\windows\\system32\\profsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c0c629bf79722a12b35bda6d5ef6fd2d96e013d80d8f17077e9137ed3988b452",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "Y8VvqnGqQhe2A5l75G2o1g",
            "event_hash": "fIxqNyHtTFqt2FcOnHzqag",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "64e2c7176d189e4a838d04f7c724cae7",
            "modload_name": "c:\\windows\\system32\\userenv.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "a9ec868ab16c79d00d74d95ef9936772b9d4b7a1e64240534b4646029a207708",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "0MVGeGGHTkmFzdn4PR3gww",
            "event_hash": "dOZfzhW2Qm2wkmll8__dqQ",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "9a1175ef7b9e297fdc0add33783ef8ff",
            "modload_name": "c:\\windows\\system32\\sysntfy.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "0fc1a3942e0f3f1b5fba09598247fcb073150d485b25c4784710904a392b6ccd",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "j27Qsf9ITe66i1ykn_Mrgw",
            "event_hash": "omVbiu7BRkSgr_mc4U5lww",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8ed638461effcf584af5a8c291a2f9df",
            "modload_name": "c:\\windows\\system32\\profapi.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c8414d68e423d345212e90524897b781b944034c385123ded4aca508faddd11e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "RFTB31HjSaab4Tbl8Q8x3A",
            "event_hash": "-tSTPIjBTMueUGaTEC6lJg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "05fbe1f7c13e87af7a414cdf288b1f62",
            "modload_name": "c:\\windows\\system32\\themeservice.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "24079e1a6b2e33a1a8e76a77f73473b93dd6b379e44c982ce50d6ceed9747838",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "JXa204bEQFCVMfTyixps2Q",
            "event_hash": "ZmE7Dbu5RXSKfcq5HHZ69g",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0bde0fcf597e9b65600121ef54ff8340",
            "modload_name": "c:\\windows\\system32\\gpsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "da5c96e84e05ad09251c82b4bfede274342409803730cebf24eead0dcd42da7e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "9JiEKx8JTF-yFVgUftXWAQ",
            "event_hash": "HyaPPGZlQeWWzb7_13Dvhw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "aa9973f611039a02c8d1f71a65f8c775",
            "modload_name": "c:\\windows\\system32\\srvcli.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "2cfce559bed5be35b1970df544e0606af6559e02ef8381ba09270ed5fb8e1bf5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        }
    ],
    "num_found": 250,
    "num_available": 250,
    "total_segments": 7,
    "processed_segments": 7
}

EVENT_SEARCH_RESP_INCOMPLETE = {
    "results": [
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "v1PSfkXGQAilYw5MYwoWQA",
            "event_hash": "zo-g2PNTSo2ZH23N--07Zw",
            "event_timestamp": "2020-08-26T21:38:17.090Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0d50f3c3d50b878ceae21b9be3f6a638",
            "modload_name": "c:\\windows\\system32\\kernel.appcore.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "bf0b1a5d4cea656695ffb45d930f6add63519aeae9f8aed21e4e50708fe5e84c",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "bYd9BiyVRdSI47Can0LWwA",
            "event_hash": "hg_Y48btT7K7As30HyJYVw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "b83b06508cadbc204b3daeecc395a571",
            "modload_name": "c:\\windows\\system32\\cryptbase.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "10045637aba4ef52f93602f5f78e8a50f2c2d9b2e646d0d0cc91e684c2ad1030",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "7ykrNX5pRTK85QHKnBtDng",
            "event_hash": "DGCt_a2uRI-Jk-aTMMK-Lg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "876a3e1a4db8720df66d653bdbad3e5d",
            "modload_name": "c:\\windows\\system32\\bcryptprimitives.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "6ed5bdc432e5f351e01995d345d296ca67af24b84951268f239c631a544054a5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "b8a3EOR7QX6wV_3QNtsOYQ",
            "event_hash": "ug_dVz7eSl6P1495gtGong",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8513a1e7ae4b9dc82c4b4f432c648a58",
            "modload_name": "c:\\windows\\system32\\profsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c0c629bf79722a12b35bda6d5ef6fd2d96e013d80d8f17077e9137ed3988b452",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "Y8VvqnGqQhe2A5l75G2o1g",
            "event_hash": "fIxqNyHtTFqt2FcOnHzqag",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "64e2c7176d189e4a838d04f7c724cae7",
            "modload_name": "c:\\windows\\system32\\userenv.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "a9ec868ab16c79d00d74d95ef9936772b9d4b7a1e64240534b4646029a207708",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "0MVGeGGHTkmFzdn4PR3gww",
            "event_hash": "dOZfzhW2Qm2wkmll8__dqQ",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "9a1175ef7b9e297fdc0add33783ef8ff",
            "modload_name": "c:\\windows\\system32\\sysntfy.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "0fc1a3942e0f3f1b5fba09598247fcb073150d485b25c4784710904a392b6ccd",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "j27Qsf9ITe66i1ykn_Mrgw",
            "event_hash": "omVbiu7BRkSgr_mc4U5lww",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "8ed638461effcf584af5a8c291a2f9df",
            "modload_name": "c:\\windows\\system32\\profapi.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "c8414d68e423d345212e90524897b781b944034c385123ded4aca508faddd11e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "RFTB31HjSaab4Tbl8Q8x3A",
            "event_hash": "-tSTPIjBTMueUGaTEC6lJg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "05fbe1f7c13e87af7a414cdf288b1f62",
            "modload_name": "c:\\windows\\system32\\themeservice.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "24079e1a6b2e33a1a8e76a77f73473b93dd6b379e44c982ce50d6ceed9747838",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "JXa204bEQFCVMfTyixps2Q",
            "event_hash": "ZmE7Dbu5RXSKfcq5HHZ69g",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0bde0fcf597e9b65600121ef54ff8340",
            "modload_name": "c:\\windows\\system32\\gpsvc.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_CATALOG_SIGNED",
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "da5c96e84e05ad09251c82b4bfede274342409803730cebf24eead0dcd42da7e",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.330Z",
            "event_guid": "9JiEKx8JTF-yFVgUftXWAQ",
            "event_hash": "HyaPPGZlQeWWzb7_13Dvhw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "aa9973f611039a02c8d1f71a65f8c775",
            "modload_name": "c:\\windows\\system32\\srvcli.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "2cfce559bed5be35b1970df544e0606af6559e02ef8381ba09270ed5fb8e1bf5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        }
    ],
    "num_found": 250,
    "num_available": 250,
    "total_segments": 7,
    "processed_segments": 4
}

EVENT_SEARCH_RESP_PART_ONE = {
    "results": [
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "v1PSfkXGQAilYw5MYwoWQA",
            "event_hash": "zo-g2PNTSo2ZH23N--07Zw",
            "event_timestamp": "2020-08-26T21:38:17.090Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "0d50f3c3d50b878ceae21b9be3f6a638",
            "modload_name": "c:\\windows\\system32\\kernel.appcore.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "bf0b1a5d4cea656695ffb45d930f6add63519aeae9f8aed21e4e50708fe5e84c",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        }
    ],
    "num_found": 250,
    "num_available": 3,
    "total_segments": 7,
    "processed_segments": 7
}

EVENT_SEARCH_RESP_PART_TWO = {
    "results": [
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "bYd9BiyVRdSI47Can0LWwA",
            "event_hash": "hg_Y48btT7K7As30HyJYVw",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "b83b06508cadbc204b3daeecc395a571",
            "modload_name": "c:\\windows\\system32\\cryptbase.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "10045637aba4ef52f93602f5f78e8a50f2c2d9b2e646d0d0cc91e684c2ad1030",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        },
        {
            "backend_timestamp": "2020-08-26T21:39:42.695Z",
            "created_timestamp": "2020-08-26T22:31:14.329Z",
            "event_guid": "7ykrNX5pRTK85QHKnBtDng",
            "event_hash": "DGCt_a2uRI-Jk-aTMMK-Lg",
            "event_timestamp": "2020-08-26T21:38:17.106Z",
            "event_type": "modload",
            "legacy": False,
            "modload_action": "ACTION_LOADED_MODULE_DISCOVERED",
            "modload_effective_reputation": "REP_WHITE",
            "modload_md5": "876a3e1a4db8720df66d653bdbad3e5d",
            "modload_name": "c:\\windows\\system32\\bcryptprimitives.dll",
            "modload_publisher": "Microsoft Windows",
            "modload_publisher_state": [
                "FILE_SIGNATURE_STATE_OS",
                "FILE_SIGNATURE_STATE_SIGNED",
                "FILE_SIGNATURE_STATE_TRUSTED",
                "FILE_SIGNATURE_STATE_VERIFIED"
            ],
            "modload_sha256": "6ed5bdc432e5f351e01995d345d296ca67af24b84951268f239c631a544054a5",
            "process_guid": "J7G6DTLN-006633e3-00000334-00000000-1d677bedfbb1c2e",
            "process_pid": 820
        }
    ],
    "num_found": 250,
    "num_available": 3,
    "total_segments": 7,
    "processed_segments": 7
}

EVENT_FACETS_RESP = {
    "ranges": [],
    "terms": [
        {
            "values": [
                {
                    "total": 6,
                    "id": "modload",
                    "name": "modload"
                },
                {
                    "total": 3,
                    "id": "crossproc",
                    "name": "crossproc"
                },
                {
                    "total": 2,
                    "id": "filemod",
                    "name": "filemod"
                },
                {
                    "total": 1,
                    "id": "childproc",
                    "name": "childproc"
                }
            ],
            "field": "event_type"
        }
    ],
    "num_found": 12,
    "total_segments": 3,
    "processed_segments": 3
}

EVENT_FACETS_RESP_INCOMPLETE = {
    "ranges": [],
    "terms": [
        {
            "values": [
                {
                    "total": 6,
                    "id": "modload",
                    "name": "modload"
                },
                {
                    "total": 3,
                    "id": "crossproc",
                    "name": "crossproc"
                },
                {
                    "total": 2,
                    "id": "filemod",
                    "name": "filemod"
                },
                {
                    "total": 1,
                    "id": "childproc",
                    "name": "childproc"
                }
            ],
            "field": "event_type"
        }
    ],
    "num_found": 12,
    "total_segments": 3,
    "processed_segments": 1
}
