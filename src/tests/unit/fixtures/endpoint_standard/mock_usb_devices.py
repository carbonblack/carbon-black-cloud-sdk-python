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

USBDEVICE_BLOCK_BULK_CREATE_RESP = {
    "results": [
        {
            "created_at": "2020-11-12T16:24:46.226Z",
            "id": 55,
            "policy_id": "6997287",
            "updated_at": "2020-11-12T16:24:46.226Z"
        }
    ]
}

