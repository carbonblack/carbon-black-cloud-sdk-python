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
multiple "profiles" or sets of credentials to be supplied in a single file.  The file format is compatible with that
used by the older CBAPI for Carbon Black Cloud, so older files can continue to be used.  This is an example of a
credentials file:

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

* ``url``: The URL used to access the Carbon Black Cloud.  This value *must* be specified.
* ``token``: The access token to be used to authenticate to the server.  It is the same structure as the
  ``X-Auth-Token:`` defined for direct API access in `the developer documentation`_.  This value *must* be specified.
* ``org_key``: The organization key specifying which organization to work with.  This value *must* be specified.
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

.. _`the developer documentation`: https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/#creating-an-api-key

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
The credentials may be supplied to CBC SDK via the environment variables ``CBC_URL``, ``CBC_TOKEN``, ``CBC_ORG_KEY``,
and ``CBC_SSL_VERIFY``. For backwards compatibility with CBAPI, the environment variables ``CBAPI_URL``,
``CBAPI_TOKEN``, ``CBAPI_ORG_KEY``, and ``CBAPI_SSL_VERIFY`` may also be used; if both are specified, the newer
``CBC_xxx`` environment variables override their corresponding ``CBAPI_xxx`` equivalents. To use the environment
variables, they must be set before the application is run (at least ``CBC_URL`` or ``CBAPI_URL``, and ``CBC_TOKEN`` or
``CBAPI_TOKEN``), and the ``credential_file`` keyword parameter to ``CBCloudAPI`` must be either ``None`` or left
unspecified. (The ``profile`` keyword parameter will be ignored.)

**N.B.:** Passing credentials via the environment can be insecure, and, if this method is used, a warning message to
that effect will be generated in the log.

Supplying the Credentials Via the Windows Registry
--------------------------------------------------
CBC SDK also provides the ability to use the Windows Registry to supply credentials, a method which is more secure on
Windows than other methods.

**N.B.:** Presently, to use the Windows Registry, you must supply its credential provider as an "external" credential
provider.  A future version of the CBC SDK will move to using this as a default provider when running on Windows.

By default, registry entries are stored under the key
``HKEY_CURRENT_USER\Software\VMware Carbon Black\Cloud Credentials``.  Under this key, there may be multiple subkeys,
each of which specifies a "profile" (as with credential files).  Within these subkeys, the following named values may
be specified:

* ``url`` (type ``REG_SZ``): The URL used to access the Carbon Black Cloud.
* ``token`` (type ``REG_SZ``): The access token to be used to authenticate to the server.
* ``org_key`` (type ``REG_SZ``): The organization key specifying which organization to work with.
* ``ssl_verify`` (type ``REG_DWORD``): A value which is nonzero to validate the SSL connection, or zero to bypass
  validation. The default is 1.
* ``ssl_verify_hostname`` (type ``REG_DWORD``): A value which is nonzero to verify the host name of the server being
  connected to, or zero to bypass this validation. The default is 1.
* ``ssl_cert_file`` (type ``REG_SZ``): The name of an optional certificate file used to validate the certificates
  of the SSL connection.  If not specified, the standard system certificate verification will be used.
* ``ssl_force_tls_1_2`` (type ``REG_DWORD``): A value which is nonzero to force the connection to use TLS 1.2
  rather than any later version. The default is 0.
* ``proxy`` (type ``REG_SZ``): If specified, this is the name of a proxy host to be used in making the connection.
* ``ignore_system_proxy`` (type ``REG_DWORD``): A value which is nonzero to force system proxy settings to be ignored
  in making the connection to the server. The default is 0.

Unrecognized named values are ignored.

To use the Registry credential provider, create an instance of it, then pass the reference to that instance in the
``credential_provider`` keyword parameter when creating ``CBCloudAPI``.  As with credential files, the name of the
profile to be retrieved from the Registry should be specified in the keyword parameter ``profile``.

**Example:**

    >>> provider = RegistryCredentialProvider()
    >>> cbc_api = CBCloudAPI(credential_provider=provider, profile='default')

**TK: Use information for the Registry setup tool**

**Advanced Usage:** The parameters ``keypath`` and ``userkey`` to ``RegistryCredentialProvider`` may be used to
control the exact location of the "base" registry key where the sections of credentials are located.  The ``keypath``
parameter allows specification of the path from ``HKEY_CURRENT_USER`` where the base registry key is located. If
``userkey``, which is ``True`` by default, is ``False``, the path will be interpreted as being rooted at
``HKEY_LOCAL_MACHINE`` rather than ``HKEY_CURRENT_USER``.

**Example:**

    >>> provider = RegistryCredentialProvider('Software\\Contoso\\My CBC Application')
    >>> cbc_api = CBCloudAPI(credential_provider=provider, profile='default')

Note the use of doubled backslashes to properly escape them under Python.

Using an External Credential Provider
-------------------------------------
Credentials may also be supplied by writing a class that conforms to the ``CredentialProvider`` interface protocol.
When creating ``CBCloudAPI``, pass a reference to an object of that class in the ``credential_provider`` keyword
parameter. Then pass the name of the profile you want to retrieve to the provider object using the keyword parameter
``profile``.

**Example:**

    >>> provider = MyCredentialProvider()
    >>> cbc_api = CBCloudAPI(credential_provider=provider, profile='default')

Details of writing a credential provider may be found in the "Developing Credential Providers" document.
**TK: better reference**
