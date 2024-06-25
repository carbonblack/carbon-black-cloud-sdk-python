..
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

.. _getting-started:

Getting Started with the Carbon Black Cloud Python SDK - "Hello CBC"
====================================================================

This document will help you get started with the Carbon Black Cloud Python SDK by installing it, configuring
authentication for it, and executing a simple example program that makes one API call.

Installation
------------

Make sure you are using Python 3.  Use the command ``pip install carbon-black-cloud-sdk`` to install the SDK and all
its dependencies. (In some environments, the correct command will be ``pip3 install carbon-black-cloud-sdk`` to
use Python 3.)

You can also access the SDK in development mode by cloning the GitHub repository, and then executing
``python setup.py develop`` (in some environments, ``python3 setup.py develop``) from the top-level directory.
Setting your ``PYTHONPATH`` environment variable to the directory ``[sdk]/src``, where ``[sdk]`` is the top-level
directory of the SDK, will also work for these purposes.  (On Windows, use ``[sdk]\src``.)

See also the :doc:`installation` section of this documentation for more information.

Authentication
--------------

To make use of APIs, you will need an *API token,* in case you are using Carbon Black Cloud to manage your
identity and authentication, or if you are using VMware Cloud Services Platform, an *OAuth App with Bearer* or
a *Personal API Token*.  For our example, we will use a custom CBC-managed key with the ability to list devices.
To learn more about the different authentication methods, click
`here <https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/>`_.

Log into the Carbon Black Cloud UI and go to ``Settings > API Access``.  Start by selecting ``Access Levels`` at the
top of the screen and press ``Add Access Level``.  Fill in a name and description for your sample access level, keep
``Copy permissions from`` set to ``None``, and, under the permission category ``Device`` and permission name
``General information``, check the ``Read`` check box.  Press ``Save`` to save and create the new access level.

Now select ``API Keys`` at the top of the screen and press ``Add API Key``.  Enter a name for the key, and, optionally,
a description.  For ``Access Level type``, select ``Custom``, and for ``Custom Access Level``, select the access level
you created above.  Press ``Save`` to save and create the new API key.  An ``API Credentials`` dialog will be displayed
with the new API ID and secret key; this dialog may also be re-displayed at any time by finding the API key in the list,
clicking the drop-down arrow under the ``Actions`` column, and selecting ``API Credentials``.

We will use a credentials file to store the credential information by default.  Create a directory named
``.carbonblack`` under your user home directory. (On Windows, this directory is generally ``C:\Users\[username]``,
where ``[username]`` is your user name.)  Within this directory create a file ``credentials.cbc`` to store your
credentials.  Copy the following template to this new file::

    [default]
    url=
    token=
    org_key=
    ssl_verify=True
    integrationName=CustomSDKScript/1.0

Following the ``url=`` keyword, add the top-level URL you use to access the Carbon Black Cloud, including the
``https://`` prefix and the domain name, but without any of the path information following it.

Following the ``token=`` keyword, add the ``API Secret Key`` from the ``API Credentials`` dialog, followed by a forward
slash (/) character, followed by the ``API ID`` from the ``API Credentials`` dialog.  (The secret key is always 24
characters in length, and the API ID is always 10 characters in length.)

Following the ``org_key=`` keyword, add the organization key from your organization, which may be seen under the
``Org Key:`` heading at the top of the ``API Keys`` display under ``Settings > API Access``.  It is always 8 characters
in length.

Save the completed ``credentials.cbc`` file, which should look like this *(example text only)*::

    [default]
    url=https://example.net
    token=ABCDEFGHGIJKLMNOPQRSTUVWX/ABCDEFGHIJ
    org_key=A1B2C3D4
    ssl_verify=True

On UNIX systems, you must make sure that the ``credentials.cbc`` file is properly secured.  The simplest commands for
doing so are::

    $ chmod 600 ~/.carbonblack/credentials.cbc
    $ chmod 700 ~/.carbonblack

For further information, please see the :doc:`authentication` section of the documentation, as well as the
`Authentication Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/>`_ on the
Carbon Black Cloud Developer Network.

Setting the User-Agent
----------------------

The SDK supports custom ``User-Agent``s, which allow you to identify yourself when using the SDK to make API calls.
The credential parameter ``integration_name`` is used for this. If you use a file to authenticate the SDK, this is
how you could identify yourself::

    [default]
    url=http://example.com
    token=ABCDEFGHIJKLMNOPQRSTUVWX/12345678
    org_key=A1B2C3D4
    integration_name=MyScript/0.9.0

See the :doc:`authentication` documentation for more information about credentials.

Running the Example
-------------------

The example we will be running is ``list_devices.py``, located in the ``examples/platform`` subdirectory of the GitHub
repository.  If you cloned the repository, change directory to ``[sdk]/examples/platform``, where ``[sdk]`` is the
top-level directory of the SDK.  (On Windows, use ``[sdk]\examples\platform``.)  Alternately, you may view the current
version of that script in "raw" mode in GitHub, and use your browser's ``Save As`` function to save the script locally.
In that case, change directory to whichever directory you saved the script to.

Execute the script by using the command ``python list_devices.py`` (in some environments,
``python3 list_devices.py``).  If all is well, you will see a list of devices (endpoints) registered in your
organization, showing their numeric ID, host name, IP address, and last checkin time.

You can change what devices are shown by adding a query value with the ``-q`` parameter, and also by using
additional parameters to modify the search criteria.  Execute the command ``python list_devices.py --help`` (in some
environments, ``python3 list_devices.py --help``) for a list of all possible command line parameters.

Inside the Example Script
-------------------------

Once the command-line arguments are parsed, we create a Carbon Black Cloud API object with a call to the helper
function ``get_cb_cloud_object()``.  The standard ``select()`` method is used to create a query object that queries for
devices; the query string is passed to that object via the ``where()`` method, and other criteria are added using
specific setters.

The query is an iterable object, and calling upon its iterator methods invokes the query, which, in this case, is the
`Search Devices <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/devices-api/#search-devices>`_
API.  The example script turns those results into an in-memory list, then iterates on that list, printing only certain
properties of each retrieved Device object.

Calling the SDK Directly
------------------------

Now we'll repeat this example, but using the Python command line directly without a script.

Access your Python interpreter with the ``python`` command (or ``python3`` if required) and type::

    >>> from cbc_sdk.rest_api import CBCloudAPI
    >>> from cbc_sdk.platform import Device
    >>> cb = CBCloudAPI(profile='default')

This imports the necessary classes and creates an instance of the base ``CBCloudAPI`` object.  By default, the file
credentials provider is used. We set it to use the ``default`` profile in your ``credentials.cbc`` file, which you
set up earlier.

.. note::

    On Windows, a security warning message will be generated about file access to CBC SDK credentials being
    inherently insecure.

This creates a query object that searches for all devices::

    >>> query = cb.select(Device)

For convenience, we load the entirety of the query results into an in-memory list::

    >>> devices = list(query)

Using a simple ``for`` loop, we print out the ID, host name, internal IP address, and last contact time from each
returned device.  Note that the contents of the list are ``Device`` objects, not dictionaries, so we access individual
properties with the ``object.property_name`` syntax, rather than ``object['property_name']``::

    >>> for device in devices:
    ...     print(device.id, device.name, device.last_internal_ip_address, device.last_contact_time)
    ...

Searching is an important operation in the SDK, as that is how objects are generally retrieved for other operations.
The :doc:`Guide to Searching <searching>` contains more information about searching.

Next Steps
----------

 - :doc:`guides`: Information and Examples related to specific actions you want to take on your Carbon Black Cloud data
