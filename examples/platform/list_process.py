from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Device

device_id = 9301703

cb = CBCloudAPI()
live_response = cb.select(Device, device_id).lr_session()

print(live_response.list_processes())
