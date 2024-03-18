Devices
=======

*Devices*, also known as *endpoints*, are at the heart of Carbon Black Cloud's functionality.  Each device has a
Carbon Black Cloud sensor installed on it, which communicates with Carbon Black analytics and the Carbon Black Cloud
console.

Using the Carbon Black Cloud SDK, you can search for devices with a wide range of criteria, filtering on many different
fields.  You can also perform actions on individual devices, such as setting quarantine status, setting bypass status,
or upgrading to a new sensor version.

Searching for Devices
---------------------

Using a query of the ``Device`` object, you can list the devices configured for your organization::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Device
    >>> query = api.select(Device).where("os:WINDOWS")
    >>> query.add_criteria('target_priority', ['LOW']).add_criteria('virtualization_provider', ['VirtualBox'])
    >>> for d in query:
    ...     print(f"{d.name} - {d.last_internal_ip_address}")
    DESKTOP-A19 - 10.0.2.44
    DESKTOP-Q210 - 10.10.25.169
    DESKTOP-Q211 - 10.10.25.170
    DESKTOP-Q211B - 10.10.25.180
    EVALUATION-1 - 10.0.2.51
    EVALUATION-2 - 10.0.2.52
    STAGING-1A - 192.168.1.99
    ZZIGNORE-1 - 10.0.3.74

The criteria supported in the ``where()`` and ``add_criteria()`` query methods are too numerous to enumerate here;
please see
`the Developer Network documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/devices-api/#search-devices>`_
for more details.

The results of a search query can also be exported::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Device
    >>> query = api.select(Device).where("os:WINDOWS")
    >>> query.add_criteria('target_priority', ['LOW']).add_criteria('virtualization_provider', ['VirtualBox'])
    >>> job = query.export()
    >>> csv_report = job.get_output_as_string()
    >>> # can also get the output as a file or as enumerated lines of text

Search Scrolling
++++++++++++++++

A Device Search request can return no more than 10,000 items at a time.  Some customers may have more endpoints than
that; to return *all* devices, you can use the ``scroll()`` method on the query to continue searching after all devices
that have been previously returned.  This snippet illustrates the technique::

    # assume "api" is your CBCloudAPI reference
    query = api.select(Device)
    # add search terms and/or criteria to the query (not shown here)
    for d in query:
        do_something_with_device(d)  # whatever you need for each device
    while query.num_remaining > 0:
        query.scroll()  # default is 10,000 devices at a time
        for d in query:
            do_something_with_device(d)

Device Actions
--------------

Most device actions in the Carbon Black Cloud can be performed on a single device through the ``Device`` object,
on multiple devices specified by ID, or on the results of a device query.

Bypass Enable/Disable
+++++++++++++++++++++

Setting a device to *bypass* disables all enforcement on the device; its sensor stops sending data to the Carbon Black
Cloud.

Setting bypass on a single device::

    >>> # assume "api" is your CBCloudAPI reference
    >>> d = api.select(Device, 12345)
    >>> d.bypass(True)

Setting bypass on multiple devices::

    >>> # assume "api" is your CBCloudAPI reference
    api.device_bypass([1001, 1002, 1003], True)

Setting bypass on the results of a device search::

    >>> # assume "api" is your CBCloudAPI reference
    query = api.select(Device)
    # add search terms and/or criteria to the query (not shown here)
    query.bypass(True)

Quarantine
++++++++++

A device that has been *quarantined* has its outbound traffic limited, and all inbound traffic to it stopped.  This
would be used on any device determined to be interacting badly.

Setting quarantine on a single device::

    >>> # assume "api" is your CBCloudAPI reference
    >>> d = api.select(Device, 12345)
    >>> d.quarantine(True)

Setting quarantine on multiple devices::

    >>> # assume "api" is your CBCloudAPI reference
    api.device_quarantine([1001, 1002, 1003], True)

Setting quarantine on the results of a device search::

    >>> # assume "api" is your CBCloudAPI reference
    query = api.select(Device)
    # add search terms and/or criteria to the query (not shown here)
    query.quarantine(True)

Background Scan
+++++++++++++++

Enabling *background scan* causes a one-time inventory scan on the device to identify any malware files already present
there.  The background scan is of the type specified in the device's policy, if that policy has background scans
enabled, or a standard background scan if it does not.

Disabling background scan causes any background scan currently running on the device to be temporarily suspended; it
will restart when background scan is enabled again, or when the endpoint restarts.

Enabling background scan on a single device::

    >>> # assume "api" is your CBCloudAPI reference
    >>> d = api.select(Device, 12345)
    >>> d.background_scan(True)

Enabling background scan on multiple devices::

    >>> # assume "api" is your CBCloudAPI reference
    api.device_background_scan([1001, 1002, 1003], True)

Enabling background scan on the results of a device search::

    >>> # assume "api" is your CBCloudAPI reference
    query = api.select(Device)
    # add search terms and/or criteria to the query (not shown here)
    query.background_scan(True)

