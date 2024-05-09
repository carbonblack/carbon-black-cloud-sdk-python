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

"""Mocks for sensor lifecycle"""

GET_CONFIG_TEMPLATE_RESP = \
    """[customer]
    EncodedCompanyCode = ALSK12KHG83B110DKK
    CompanyCode = ABCD1234
    BackendServer = backendserver.org"""

GET_SENSOR_INFO_RESP = {
    "sensor_infos": [
        {
            "sensor_type": {
                'device_type': 'LINUX',
                'architecture': '64',
                'type': 'SUSE',
                'version': '1.2.3.4'
            },
            "sensor_url": "https://SensorURL1",
            "sensor_config_url": "https://SensorConfigURL1",
            "error_code": "NoErr1",
            "message": "Message1"
        },
        {
            "sensor_type": {
                'device_type': 'MAC',
                'architecture': '64',
                'type': 'MAC',
                'version': '5.6.7.8'
            },
            "sensor_url": "https://SensorURL2",
            "sensor_config_url": "https://SensorConfigURL2",
            "error_code": "NoErr2",
            "message": "Message2"
        }
    ]
}

REQUEST_SENSOR_INSTALL_RESP = {
    'type': "INFO",
    'code': "INSTALL_SENSOR_REQUEST_PROCESSED"
}
