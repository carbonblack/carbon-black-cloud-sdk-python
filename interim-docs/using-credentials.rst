Supplying Credentials to the CBC SDK
====================================
Use of the CBC SDK requires that credentials be supplied to the API for use in making requests to the
Carbon Black Cloud.  The most important of these credential items are:

* The URL used to access the Carbon Black Cloud.
* The access token which authenticates the user to the server, and also dictates what operations the user can perform.
* The organization key, which specifies which organization to work with.
* Optionally, a flag indicating whether the SSL connection should be verified (which defaults to ``True``).

These may be passed into the ``CBCloudAPI`` object in one of several ways.

Supplying the Credentials Directly
----------------------------------
The credentials may be passed into the ``CBCloudAPI`` object when it is created via the keyword parameters ``url``,
``token``, ``org_key``, and (optionally) ``ssl_verify``.

**Example:**

    >>> cbc_api = CBCloudAPI(url='https://example.com', token='ABCDEFGHIJKLM', org_key='A1B2C3D4')

Supplying the Credentials in a File
-----------------------------------
Credentials may be supplied in a file that resembles a Windows ``.INI`` file in structure, which allows for
multiple "profiles" or sets of credentials to be supplied in a single file.  This is an example of a credentials file:

::
    [default]
    url=http://example.com
    token=ABCDEFGH
    org_key=A1B2C3D4
    ssl_verify=false
    ssl_verify_hostname=no
    ssl_cert_file=foo.certs
    ssl_force_tls_1_2=1
    proxy=proxy.example
    ignore_system_proxy=on

    [partial]
    url=http://example.com
    ssl_verify=False

Individual profiles or sections are delimited in the file by placing their name within square brackets (\[\]).  Within
each section, individual credential values are supplied in a `keyword=value` format.  Valid keywords are
as follows:

* ``url``: The URL used to access the Carbon Black Cloud.
* ``token``: The access token to be used to authenticate to the server.
* ``org_key``: The organization key specifying which organization to work with.
* ``ssl_verify``: A Boolean value (see below) indicating whether or not to validate the SSL connection.
  The default is ``True``.
* ``ssl_verify_hostname``: A Boolean value (see below) indicating whether or not to verify the host name of the
  server being connected to. The default is ``True``.
* ``ssl_cert_file``: The name of an optional certificate file used to validate the certificates of the SSL connection.
  If not specified, the standard system certificate verification will be used.
* ``ssl_force_tls_1_2``: A Boolean value (see below). If this is ``True``, the connection will be forced to use TLS 1.2
  rather than any later version. The default is ``False``.
* ``proxy``: If specified, this is the name of a proxy host to be used in making the connection.
* ``ignore_system_proxy``: A Boolean value (see below). If this is ``True``, any system proxy settings will be ignored
  in making the connection to the server. The default is ``False``.

Unrecognized keywords are ignored.

**N.B.:** Boolean values are specified by using the strings ``true``, ``yes``, ``on``, or ``1`` to represent a
``True`` value, or the strings ``false``, ``no``, ``off``, or ``0`` to represent a ``False`` value (all of these
are case-insensitive). Any other string value specified will result in an error.

By default, the CBC SDK looks for credentials files in the following locations:

* The ``.carbonblack`` subdirectory of the current directory of the running process.
* The ``.carbonblack`` subdirectory of the user's home directory.
* The ``/etc/carbonblack`` subdirectory on Unix, or the ``C:\Windows\carbonblack`` subdirectory on Windows.

Within each of these directories, the SDK first looks for the ``credentials.cbc`` file, then the ``credentials.psc``
file (the older name for the credentials file under CBAPI).

You can override the file search logic and specify the full pathname of the credentials file in the keyword parameter
``credential_file`` when creating the ``CBCloudAPI`` object.

In all cases, you will have to specify the name of the profile to be retrieved from the credentials file in the
keyword parameter ``profile`` when creating the ``CBCloudAPI`` object.

**Example:**

    >>> cbc_api = CBCloudAPI(credential_file='~/.carbonblack/myfile.cbc', profile='default')

**Note on File Security:** It is recommended that the credentials file be secured properly on Unix. It should be owned
by the user running the process, as should the directory containing it, and neither one should specify any file
permissions for "group" or "other." In numeric terms, that means the file should have ``400`` or ``600`` permissions,
and its containing directory should have ``500`` or ``700`` permissions.  This is similar to securing configuration or
key files for ``ssh``. If these permissions are incorrect, a warning message will be logged; a future version of the
CBC SDK will disallow access to files altogether if they do not have the correct permissions.

Credential files *cannot* be properly secured in this manner under Windows; if they are used in that
environment, a warning message will be logged.

Supplying the Credentials Via the Environment
---------------------------------------------
