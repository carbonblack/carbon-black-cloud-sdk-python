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
    DESKTOP-A19 - 10.0.2.15
    DESKTOP-Q210 - 10.10.25.210
    DESKTOP-Q211 - 10.10.25.211
    DESKTOP-Q211B - 10.10.25.210
    EVALUATION-1 - 10.0.2.15
    EVALUATION-2 - 10.0.2.15
    STAGING-1A - 192.168.1.100
    ZZIGNORE-1 - 10.0.3.15

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

Device Actions
--------------

Bypass Enable/Disable
+++++++++++++++++++++

Setting a device to *bypass* disables all enforcement on the device; its sensor stops sending data to the Carbon Black
Cloud.

Quarantine
++++++++++

A device that has been *quarantined* has its outbound traffic limited, and all inbound traffic to it stopped.  This
would be used on any device determined to be interacting badly.

Background Scan
+++++++++++++++

Enabling *background scan* causes a one-time inventory scan on the device to identify any malware files already present
there.  The background scan is of the type specified in the device's policy, if that policy has background scans
enabled, or a standard background scan if it does not.

Disabling background scan causes any background scan currently running on the device to be temporarily suspended; it
will restart when background scan is enabled again, or when the endpoint restarts.

