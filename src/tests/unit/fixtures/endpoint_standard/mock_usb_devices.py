"""Mock responses for USB device queries."""

USBDEVICE_APPROVAL_GET_RESP = {
    "id": "10373",
    "vendor_id": "0x0781",
    "vendor_name": "SanDisk",
    "product_id": "0x5581",
    "product_name": "Ultra",
    "serial_number": "4C531001331122115172",
    "created_at": "2020-11-05T23:51:56.396425Z",
    "updated_at": "2020-11-11T23:05:42.048625Z",
    "updated_by": "jrn@carbonblack.com",
    "notes": "A few notes",
    "approval_name": "Example Approval"
}

USBDEVICE_APPROVAL_PUT_RESP = {
    "id": "10373",
    "vendor_id": "0x0781",
    "vendor_name": "SanDisk",
    "product_id": "0x5581",
    "product_name": "Ultra",
    "serial_number": "4C531001331122115172",
    "created_at": "2020-11-05T23:51:56.396425Z",
    "updated_at": "2020-11-11T23:05:42.048625Z",
    "updated_by": "luser@carbonblack.com",
    "notes": "Altered state",
    "approval_name": "Altered Approval"
}

USBDEVICE_APPROVAL_QUERY_RESP = {
    "num_found": 1,
    "num_available": 1,
    "results": [
        {
            "id": "10373",
            "vendor_id": "0x0781",
            "vendor_name": "SanDisk",
            "product_id": "0x5581",
            "product_name": "Ultra",
            "serial_number": "4C531001331122115172",
            "created_at": "2020-11-05T23:51:56.396425Z",
            "updated_at": "2020-11-11T23:05:42.048625Z",
            "notes": "A few notes",
            "approval_name": "Example Approval"
        }
    ]
}

USBDEVICE_APPROVAL_BULK_CREATE_REQ = [
    {
        "vendor_id": "0x0781",
        "product_id": "0x5581",
        "serial_number": "4C531001331122115172",
        "notes": "A few notes",
        "approval_name": "Example Approval"
    },
    {
        "vendor_id": "0x0666",
        "product_id": "0x6969",
        "serial_number": "4Q2123456789",
        "notes": "Whatever",
        "approval_name": "Example Approval2"
    }
]

USBDEVICE_APPROVAL_BULK_CREATE_RESP = {
    "results": [
        {
            "id": "10373",
            "vendor_id": "0x0781",
            "vendor_name": "SanDisk",
            "product_id": "0x5581",
            "product_name": "Ultra",
            "serial_number": "4C531001331122115172",
            "created_at": "2020-11-05T23:51:56.396425Z",
            "updated_at": "2020-11-11T23:05:42.048625Z",
            "notes": "A few notes",
            "approval_name": "Example Approval"
        },
        {
            "id": "10444",
            "vendor_id": "0x0666",
            "vendor_name": "Sirius Cybernetics Corp.",
            "product_id": "0x6969",
            "product_name": "Happy Hard Drive",
            "serial_number": "4Q2123456789",
            "created_at": "2020-11-05T23:51:56.396425Z",
            "updated_at": "2020-11-11T23:05:42.048625Z",
            "notes": "Whatever",
            "approval_name": "Example Approval2"
        }
    ]
}

USBDEVICE_BLOCK_GET_RESP = {
    "created_at": "2020-11-12T16:24:46.226Z",
    "id": 55,
    "policy_id": "6997287",
    "updated_at": "2020-11-12T16:24:46.226Z"
}

USBDEVICE_BLOCK_GET_ALL_RESP = {
    "results": [
        {
            "created_at": "2020-11-12T16:24:46.226Z",
            "id": 55,
            "policy_id": "6997287",
            "updated_at": "2020-11-12T16:24:46.226Z"
        }
    ]
}

USBDEVICE_BLOCK_CREATE_RESP = {
    "results": [
        {
            "created_at": "2020-11-12T16:24:46.226Z",
            "id": 44,
            "policy_id": "9686969",
            "updated_at": "2020-11-12T16:24:46.226Z"
        }
    ]
}

USBDEVICE_BLOCK_BULK_CREATE_RESP = {
    "results": [
        {
            "created_at": "2020-11-12T16:24:46.226Z",
            "id": 55,
            "policy_id": "6997287",
            "updated_at": "2020-11-12T16:24:46.226Z"
        },
        {
            "created_at": "2020-11-12T16:24:46.226Z",
            "id": 65,
            "policy_id": "6998088",
            "updated_at": "2020-11-12T16:24:46.226Z"
        }
    ]
}

USBDEVICE_GET_RESP = {
    "id": "774",
    "first_seen": "2020-10-20T19:47:02Z",
    "last_seen": "2020-10-21T18:00:59Z",
    "vendor_name": "SanDisk",
    "vendor_id": "0x0781",
    "product_name": "Ultra",
    "product_id": "0x5581",
    "serial_number": "4C531001331122115172",
    "last_endpoint_name": "DESKTOP-IL2ON7C",
    "last_endpoint_id": 7590378,
    "last_policy_id": 6997287,
    "endpoint_count": 2,
    "device_friendly_name": "SanDisk Ultra USB Device",
    "device_name": "\\Device\\HarddiskVolume30",
    "created_at": "2020-10-20T19:59:06Z",
    "updated_at": "2020-10-21T18:00:59Z",
    "status": "APPROVED"
}

USBDEVICE_GET_ENDPOINTS_RESP = {
    "results": [
        {
            "id": "53",
            "first_seen": "2020-10-21T16:50:28Z",
            "last_seen": "2020-10-21T18:00:59Z",
            "endpoint_name": "DESKTOP-IL2ON7C",
            "endpoint_id": 7590378,
            "policy_name": "Standard",
            "policy_id": 6997287,
            "created_at": "2020-10-21T16:50:28Z",
            "updated_at": "2020-10-21T18:00:59Z"
        },
        {
            "id": "50",
            "first_seen": "2020-10-20T19:47:02Z",
            "last_seen": "2020-10-21T16:36:01Z",
            "endpoint_name": "DESKTOP-IL2ON7C",
            "endpoint_id": 7579317,
            "policy_name": "Standard",
            "policy_id": 6997287,
            "created_at": "2020-10-20T19:47:02Z",
            "updated_at": "2020-10-21T16:36:01Z"
        }
    ]
}

USBDEVICE_GET_RESP_BEFORE_APPROVE = {
    "id": "808",
    "first_seen": "2020-10-20T19:47:02Z",
    "last_seen": "2020-10-21T18:00:59Z",
    "vendor_name": "SanDisk",
    "vendor_id": "0x0781",
    "product_name": "Ultra",
    "product_id": "0x5581",
    "serial_number": "4C531001331122115172",
    "last_endpoint_name": "DESKTOP-IL2ON7C",
    "last_endpoint_id": 7590378,
    "last_policy_id": 6997287,
    "endpoint_count": 2,
    "device_friendly_name": "SanDisk Ultra USB Device",
    "device_name": "\\Device\\HarddiskVolume30",
    "created_at": "2020-10-20T19:59:06Z",
    "updated_at": "2020-10-21T18:00:59Z",
    "status": "UNAPPROVED"
}

USBDEVICE_APPROVE_RESP = {
    "results": [
        {
            "id": "12703",
            "vendor_id": "0x0781",
            "vendor_name": "SanDisk",
            "product_id": "0x5581",
            "product_name": "Ultra",
            "serial_number": "4C531001331122115172",
            "created_at": "2020-11-05T23:51:56.396425Z",
            "updated_at": "2020-11-11T23:05:42.048625Z",
            "notes": "Approval notes",
            "approval_name": "ApproveTest"
        },
    ]
}

USBDEVICE_GET_RESP_AFTER_APPROVE = {
    "id": "808",
    "first_seen": "2020-10-20T19:47:02Z",
    "last_seen": "2020-10-21T18:00:59Z",
    "vendor_name": "SanDisk",
    "vendor_id": "0x0781",
    "product_name": "Ultra",
    "product_id": "0x5581",
    "serial_number": "4C531001331122115172",
    "last_endpoint_name": "DESKTOP-IL2ON7C",
    "last_endpoint_id": 7590378,
    "last_policy_id": 6997287,
    "endpoint_count": 2,
    "device_friendly_name": "SanDisk Ultra USB Device",
    "device_name": "\\Device\\HarddiskVolume30",
    "created_at": "2020-10-20T19:59:06Z",
    "updated_at": "2020-10-21T18:00:59Z",
    "status": "APPROVED"
}

USBDEVICE_QUERY_RESP = {
    "num_found": 1,
    "num_available": 1,
    "results": [
        {
            "id": "774",
            "first_seen": "2020-10-20T19:47:02Z",
            "last_seen": "2020-10-21T18:00:59Z",
            "vendor_name": "SanDisk",
            "vendor_id": "0x0781",
            "product_name": "Ultra",
            "product_id": "0x5581",
            "serial_number": "4C531001331122115172",
            "last_endpoint_name": "DESKTOP-IL2ON7C",
            "last_endpoint_id": 7590378,
            "last_policy_id": 6997287,
            "endpoint_count": 2,
            "device_friendly_name": "SanDisk Ultra USB Device",
            "device_name": "\\Device\\HarddiskVolume30",
            "created_at": "2020-10-20T19:59:06Z",
            "updated_at": "2020-10-21T18:00:59Z",
            "status": "APPROVED"
        }
    ]
}

USBDEVICE_FACET_RESP = {
    "terms": [
        {
            "field": "product_name",
            "values": [
                {
                    "id": "Cruzer Dial",
                    "name": "Cruzer Dial",
                    "total": 1
                },
                {
                    "id": "Cruzer Glide",
                    "name": "Cruzer Glide",
                    "total": 1
                },
                {
                    "id": "U3 Cruzer Micro",
                    "name": "U3 Cruzer Micro",
                    "total": 1
                },
                {
                    "id": "Ultra",
                    "name": "Ultra",
                    "total": 1
                },
                {
                    "id": "Ultra USB 3.0",
                    "name": "Ultra USB 3.0",
                    "total": 1
                }
            ]
        }
    ]
}

USBDEVICE_GET_PRODUCTS_RESP = {
    "results": [
        {
            "vendor_id": "0x0781",
            "vendor_name": "SanDisk",
            "devices_count": 5,
            "products": [
                {
                    "product_id": "0x5406",
                    "product_name": "U3 Cruzer Micro",
                    "devices_count": 1
                },
                {
                    "product_id": "0x5575",
                    "product_name": "Cruzer Glide",
                    "devices_count": 1
                },
                {
                    "product_id": "0x5581",
                    "product_name": "Ultra",
                    "devices_count": 1
                },
                {
                    "product_id": "0x5595",
                    "product_name": "Ultra USB 3.0",
                    "devices_count": 1
                },
                {
                    "product_id": "0x5599",
                    "product_name": "Cruzer Dial",
                    "devices_count": 1
                }
            ]
        }
    ]
}
