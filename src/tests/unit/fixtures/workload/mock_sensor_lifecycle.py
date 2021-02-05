"""Mocks for sensor lifecycle"""

MOCK_SENSOR_INFO = {
    "sensor_type": {
        "device_type": "WINDOWS",
        "architecture": "64",
        "type": "WINDOWS",
        "version": "3.6.0.1719"
    },
    "sensor_url": "https://sensor-url",
    "sensor_config_url": "https://sensor-config-url",
    "error_code": '808',
    "message": 'NoMessage'
}

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
