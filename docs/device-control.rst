Device Control
==============

Using the Carbon Black Cloud SDK, you can retrieve information about USB devices used in your organization, and manage
the blocking of such devices from access by your endpoints.

Retrieving the List of Known USB Devices
----------------------------------------

Using a query of the `USBDevice` object, you can see which USB devices have been used on any endpoint in your
organization.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import USBDevice
    >>> query = api.select(USBDevice).where('1')
    >>> for usb in query:
    ...   print(f"{usb.vendor_name} {usb.product_name} {usb.serial_number} {usb.status}")
    ...
    SanDisk Ultra 4C531001331122115172 UNAPPROVED
    SanDisk Cruzer Dial 4C530000110722114075 UNAPPROVED
    PNY USB 2.0 FD 07189613DD84E242 UNAPPROVED
    USB Flash Disk FBI1305031200020 APPROVED

Note that individual USB devices may be `APPROVED` or `UNAPPROVED`. USB devices which are `UNAPPROVED` cannot be read
on any endpoint with a policy that blocks unknown USB devices.

Approving A Specific Device
---------------------------

We can create one or more approvals for a specific USB device by using the `USBDeviceApproval` object and its
`bulk_create` method.  First, we'll get a list of all unapproved USB devices.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import USBDevice
    >>> query = api.select(USBDevice).where('1').set_statuses(['UNAPPROVED'])
    >>> usb_list = list(query)
    >>> for usb in usb_list:
    ...   print(f"{usb.vendor_name} {usb.product_name} {usb.serial_number}")
    ...
    SanDisk Ultra 4C531001331122115172
    SanDisk Cruzer Dial 4C530000110722114075
    PNY USB 2.0 FD 07189613DD84E242

Now we'll select one of these devices and create an approval for it.

::

    >>> usb = usb_list[1]
    >>> from cbc_sdk.endpoint_standard import USBDeviceApproval
    >>> my_approval = {'serial_number': usb.serial_number, 'vendor_id': usb.vendor_id, 'product_id': usb.product_id,
    ...                'approval_name': 'Test1', 'notes': 'API testing'}
    >>> output = USBDeviceApproval.bulk_create(api, [my_approval])
    >>> print(output[0].approval_name)
    Test1
    >>> print(output[0].notes)
    API testing
    >>> print(output[0].id)
    7c034be7-7386-3ef3-877d-e712bda803d6

The `bulk_create` method returns a list of `USBDeviceApproval` objects representing the approvals created.
