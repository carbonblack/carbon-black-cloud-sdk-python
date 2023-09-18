Device Control
==============

Using the Carbon Black Cloud SDK, you can retrieve information about USB devices used in your organization, and manage
the blocking of such devices from access by your endpoints.

.. note::

    ``USBDevice`` is distinct from either the Platform API ``Device`` or the Endpoint Standard ``Device``. Access
    to USB devices is through the Endpoint Standard package ``from cbc_sdk.endpoint_standard import USBDevice``.

Retrieving the List of Known USB Devices
----------------------------------------

Using a query of the ``USBDevice`` object, you can see which USB devices have been used on any endpoint in your
organization::

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

Note that individual USB devices may be ``APPROVED`` or ``UNAPPROVED``. USB devices which are ``UNAPPROVED`` cannot
be read on any endpoint with a policy that blocks unknown USB devices.

A USB device query can also be exported to either CSV or JSON format, for use by other software systems::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import USBDevice
    >>> query = api.select(USBDevice).where('1')
    >>> job = query.export('CSV')
    >>> csv_report = job.get_output_as_string()
    >>> # can also get the output as a file or as enumerated lines of text

Approving A Specific Device
---------------------------

We can create an approval for a USB device by using the device's ``approve()`` method.  First, we'll get a list of all
unapproved USB devices::

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

Now we'll select one of these devices and approve it::

    >>> usb = usb_list[1]
    >>> print(usb.status)
    UNAPPROVED
    >>> approval = usb.approve('Test1', 'API Testing')
    >>> print(approval.approval_name)
    Test1
    >>> print(approval.notes)
    API Testing
    >>> print(approval.serial_number)
    4C530000110722114075
    >>> print(approval.id)
    1ffd0a16-28ad-3fba-981d-d1c29c2903da
    >>> print(usb.status)
    APPROVED

The ``approve()`` method creates a ``USBDeviceApproval`` representing that particular device's approval, and
also reloads the ``USBDevice`` so its ``status`` reflects the fact that it's been approved.

Removing A Device's Approval
----------------------------

Device approvals may be removed via the API as well. Starting from the end of the previous example::

    >>> approval.delete()
    >>> usb.refresh()
    True
    >>> print(usb.status)
    UNAPPROVED

The ``delete()`` method is what causes the approval to be removed.  We then use ``refresh()`` on the actual
``USBDevice`` object to allow its ``status`` to be updated.

Retrieving the List of Approvals
--------------------------------

USB device approvals can also be enumerated directly::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import USBDeviceApproval
    >>> query = api.select(USBDeviceApproval)
    >>> for approval in query:
    ...     print(f"{approval.id} {approval.approval_name} {approval.serial_number}")
    ...

They can also be exported in a similar manner to USB devices::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import USBDeviceApproval
    >>> query = api.select(USBDeviceApproval)
    >>> job = query.export('CSV')
    >>> csv_report = job.get_output_as_string()
    >>> # can also get the output as a file or as enumerated lines of text

Device Control Alerts
---------------------

When an endpoint attempts to access a blocked USB device (the endpoint has USB device blocking configured and the USB
device is not approved), a ``DeviceControlAlert`` is generated.  These alerts may be queried using the standard
Platform API components.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import DeviceControlAlert
    >>> query = api.select(DeviceControlAlert).where('1')
    >>> alerts_list = list(query)
    >>> for alert in alerts_list:
    ...   print(f"{alert.vendor_name} {alert.product_name} {alert.serial_number}")
    ...
    USB Flash Disk FBI1305031200020
    USB Flash Disk FBI1305031200020
    USB Flash Disk FBI1305031200020
    USB Flash Disk FBI1305031200020
    PNY USB 2.0 FD 07189613DD84E242
    PNY USB 2.0 FD 07189613DD84E242
    PNY USB 2.0 FD 07189613DD84E242

There are a number of fields supported by ``DeviceControlAlert`` over and above the standard alert fields; see
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/#device-control-alert>`_
for details.
