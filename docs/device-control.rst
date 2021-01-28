Device Control
==============

Using the Carbon Black Cloud SDK, you can retrieve information about USB devices used in your organization, and manage
the blocking of such devices from access by your endpoints.

Retrieving the List of Known USB Devices
----------------------------------------

Using a query of the ``USBDevice`` object, you can see which USB devices have been used on any endpoint in your
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

Note that individual USB devices may be ``APPROVED`` or ``UNAPPROVED``. USB devices which are ``UNAPPROVED`` cannot
be read on any endpoint with a policy that blocks unknown USB devices.

Approving A Specific Device
---------------------------

We can create an approval for a USB device by using the device's ``approve()`` method.  First, we'll get a list of all
unapproved USB devices.

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

Now we'll select one of these devices and approve it.

::

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

Device approvals may be removed via the API as well. Starting from the end of the previous example:

    >>> approval.delete()
    >>> usb.refresh()
    True
    >>> print(usb.status)
    UNAPPROVED

The ``delete()`` method is what causes the approval to be removed.  We then use ``refresh()`` on the actual
``USBDevice`` object to allow its ``status`` to be updated.
