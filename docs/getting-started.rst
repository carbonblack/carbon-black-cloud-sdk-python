.. _getting-started:

Getting Started with the Carbon Black Cloud Python SDK - "Hello CBC"
====================================================================
This document will help you get started with the Carbon Black Cloud Python SDK by installing it, configuring
authentication for it, and executing a simple example program that makes one API call.

Installation
------------
Make sure you are using Python 3.  Use the command ``pip install cbc_sdk`` to install the SDK and all its dependencies.
(In some environments, the correct command will be ``pip3 install cbc_sdk`` to use Python 3.)

You can also access the SDK in development mode by cloning the GitHub repository, and then executing
``python setup.py develop`` (in some environments, ``python3 setup.py develop``) from the top-level directory.
Setting your ``PYTHONPATH`` environment variable to the directory ``[sdk]/src``, where ``[sdk]`` is the top-level
directory of the SDK, will also work for these purposes.  (On Windows, use ``[sdk]\src``.)

Authentication
--------------
In order to make use of the API, you will need an *API token,* which you will get from the Carbon Black Cloud UI.
For the purposes of our example, we will need a custom key with the ability to list devices.

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

Following the ``url=`` keyword, add the top-level URL you use to access the Carbon Black Cloud, including the
``https://`` prefix and the domain name, but without any of the path information following it.

Following the ``token=`` keyword, add the ``API Secret Key`` from the ``API Credentials`` dialog, followed by a forward
slash (/) character, followed by the ``API ID`` from the ``API Credentials`` dialog.  (The secret key is always 24
characters in length, and the API ID is always 10 characters in length.)

Following the ``org_key=`` keyword, add the organization key from your organization, which may be seen under the
``Org Key:`` heading at the top of the ``API Keys`` display under ``Settings > API Access``.  It is always 8 characters
in length.

Save the completed ``credentials.cbc`` file.

Running the Example
-------------------
The example we will be running is ``list_devices.py``, located in the ``examples/platform`` subdirectory of the GitHub
repository.  If you cloned the repository, change directory to ``[sdk]/examples/platform``, where ``[sdk]`` is the
top-level directory of the SDK.  (On Windows, use ``[sdk]\examples\platform``.)  Alternately, you may view the current
version of that script in "raw" mode in GitHub, and use your browser's ``Save As`` function to save the script locally.
In that case, change directory to whichever directory you saved the script to.

Execute the script by using the command ``python list_devices.py -q '1'`` (in some environments,
``python3 list_devices.py -q '1'``).  If all is well, you will see a list of devices (endpoints) registered in your
organization, showing their numeric ID, host name, IP address, and last checkin time.

You can change what devices are shown by modifying the query value supplied to the ``-q`` parameter, and also by using
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
