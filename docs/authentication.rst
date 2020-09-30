.. _authentication:

Authentication
==============

The Carbon Black Cloud Python SDK uses API Keys to authenticate with
the Carbon Black Cloud. See the `Developer Network Authentication Guide`_ for
information about generating API Keys.

Components of API Credentials
-----------------------------

When supplying API credentials to the SDK `at runtime <#id2>`_, `with a file <#id3>`_,
or `with Windows Registry <#id4>`_, the credentials include these components:

***** **Required**

+-------------------------+------------------------------------------------------+---------+
|  Keyword                | Definition                                           | Default |
+=========================+======================================================+=========+
| ``url`` *****           | The URL used to access the Carbon Black Cloud.       |         |
+-------------------------+------------------------------------------------------+---------+
| ``token`` *****         | The access token to authenticate with.  Same         |         |
|                         | structure as ``X-Auth-Token`` defined in             |         |
|                         | the `Developer Network Authentication Guide`_.       |         |
|                         | Derived from an API Key's Secret Key and API ID.     |         |
+-------------------------+------------------------------------------------------+---------+
|``org_key`` *****        | The organization key specifying which organization to|         |
|                         | work with.                                           |         |
+-------------------------+------------------------------------------------------+---------+
| ``ssl_verify``          | A Boolean value (see below) indicating whether or not| ``True``|
|                         | to validate the SSL connection.                      |         |
+-------------------------+------------------------------------------------------+---------+
| ``ssl_verify_hostname`` | A Boolean value (see below) indicating whether or not| ``True``|
|                         | to verify the host name of the server being connected|         |
|                         | to.                                                  |         |
+-------------------------+------------------------------------------------------+---------+
|``ignore_system_proxy``  | A Boolean value (see below). If this is ``True``, any|``False``|
|                         | system proxy settings will be ignored in making the  |         |
|                         | connection to the server.                            |         |
+-------------------------+------------------------------------------------------+---------+
|``ssl_force_tls_1_2``    | A Boolean value (see below). If this is ``True``,    |``False``|
|                         | the connection will be forced to use TLS 1.2         |         |
|                         | rather than any later version.                       |         |
+-------------------------+------------------------------------------------------+---------+
|``ssl_cert_file``        | The name of an optional certificate file used to     |         |
|                         | validate the certificates of the SSL connection.     |         |
|                         | If not specified, the standard system certificate    |         |
|                         | verification will be used.                           |         |
+-------------------------+------------------------------------------------------+---------+
|``proxy``                | If specified, this is the name of a proxy host to be |         |
|                         | used in making the connection.                       |         |
+-------------------------+------------------------------------------------------+---------+
|``integration_name``     | The name of the integration to use these credentials.|         |
|                         | The string may optionally end with a slash character,|         |
|                         | followed by the integration's version number.  Passed|         |
|                         | as part of the ``User-Agent:`` HTTP header on all    |         |
|                         | requests made by the SDK.                            |         |
+-------------------------+------------------------------------------------------+---------+


When supplying API credentials to the SDK `with environmental variables <#id5>`_ (not recommended),
the credentials include these components:

+-------------------------+----------------------+---------+
| Keyword                 | Alternative          | Default |
+=========================+======================+=========+
| ``CBC_URL``             | ``CBAPI_URL``        |         |
+-------------------------+----------------------+---------+
| ``CBC_TOKEN``           | ``CBAPI_TOKEN``      |         |
+-------------------------+----------------------+---------+
| ``CBC_ORG_KEY``         | ``CBAPI_ORG_KEY``    |         |
+-------------------------+----------------------+---------+
| ``CBC_SSL_VERIFY``      | ``CBAPI_SSL_VERIFY`` | ``True``|
+-------------------------+----------------------+---------+

Alternative keywords are available to maintain backwards compatibility with CBAPI.

Boolean Values
^^^^^^^^^^^^^^

Boolean values are specified by using the strings ``true``, ``yes``, ``on``, or ``1`` to represent a
``True`` value, or the strings ``false``, ``no``, ``off``, or ``0`` to represent a ``False`` value. All of these
are case-insensitive. Any other string value specified will result in an error.

For example, to disable SSL connection validation, any of the following would work::

  ssl_verify=False
  ssl_verify=false
  ssl_verify=No
  ssl_verify=no
  ssl_verify=Off
  ssl_verify=off
  ssl_verify=0

Supply SDK With Credentials
---------------------------

Credentials may be passed into the :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>` object in several ways:

- `At Runtime`_
- `With a File`_
- `With Windows Registry`_
- `With Environmental Variables`_

.. _`Developer Network Authentication Guide`: https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/#creating-an-api-key

At Runtime
^^^^^^^^^^
The credentials may be passed into the :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>` object when it is created via the keyword parameters ``url``,
``token``, ``org_key``, and (optionally) ``ssl_verify`` and ``integration_name``.

**Example:**

    >>> api = CBCloudAPI(url='https://example.com', token='ABCDEFGHIJKLMNOPQRSTUVWX/12345678',
    ...                  org_key='A1B2C3D4', ssl_verify=False, integration_name='MyScript/1.0')

The ``integration_name`` may be specified even if using another credential provider. If specified as a
parameter, the ``integration_name`` overrides any integration name specified by means of the credential provider.

With a File
^^^^^^^^^^^
Credentials may be supplied in a file that resembles a Windows ``.INI`` file in structure, which allows for
multiple "profiles" or sets of credentials to be supplied in a single file.  The file format is backwards compatible with
CBAPI, so older files can continue to be used.  This is an example of a credentials file:

::

    [default]
    url=http://example.com
    token=ABCDEFGHIJKLMNOPQRSTUVWX/12345678
    org_key=A1B2C3D4
    ssl_verify=false
    ssl_verify_hostname=no
    ssl_cert_file=foo.certs
    ssl_force_tls_1_2=1
    proxy=proxy.example
    ignore_system_proxy=on
    integration_name=MyScript/0.9.0

    [production]
    url=http://example.com
    token=QRSTUVWXYZABCDEFGHIJKLMN/76543210
    org_key=A1B2C3D4
    ssl_verify=false
    ssl_verify_hostname=no
    ssl_cert_file=foo.certs
    ssl_force_tls_1_2=1
    proxy=proxy.example
    ignore_system_proxy=on
    integration_name=MyApplication/1.3.1

Individual profiles or sections are delimited in the file by placing their name within square brackets: ``[profile_name]``.  Within
each section, individual credential values are supplied in a ``keyword=value`` format.


Unrecognized keywords are ignored.



By default, the CBC SDK looks for credentials files in the following locations:

* The ``.carbonblack`` subdirectory of the current directory of the running process.
* The ``.carbonblack`` subdirectory of the user's home directory.
* The ``/etc/carbonblack`` subdirectory on Unix, or the ``C:\Windows\carbonblack`` subdirectory on Windows.

Within each of these directories, the SDK first looks for the ``credentials.cbc`` file, then the ``credentials.psc``
file (the older name for the credentials file under CBAPI).

You can override the file search logic and specify the full pathname of the credentials file in the keyword parameter
``credential_file`` when creating the :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>` object.

In all cases, you will have to specify the name of the profile to be retrieved from the credentials file in the
keyword parameter ``profile`` when creating the :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>` object.

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

With Windows Registry
^^^^^^^^^^^^^^^^^^^^^
CBC SDK also provides the ability to use the Windows Registry to supply credentials, a method which is more secure on
Windows than other methods.

**N.B.:** Presently, to use the Windows Registry, you must supply its credential provider as an "external" credential
provider.  A future version of the CBC SDK will move to using this as a default provider when running on Windows.

By default, registry entries are stored under the key
``HKEY_CURRENT_USER\Software\VMware Carbon Black\Cloud Credentials``.  Under this key, there may be multiple subkeys,
each of which specifies a "profile" (as with credential files).  Within these subkeys, the following named values may
be specified:

***** **Required**

+-------------------------+----------------+---------+
|  Keyword                | Value Type     | Default |
+=========================+================+=========+
| ``url`` *****           | ``REG_SZ``     |         |
+-------------------------+----------------+---------+
| ``token`` *****         | ``REG_SZ``     |         |
+-------------------------+----------------+---------+
|``org_key`` *****        | ``REG_SZ``     |         |
+-------------------------+----------------+---------+
| ``ssl_verify``          | ``REG_DWORD``  | 1       |
+-------------------------+----------------+---------+
| ``ssl_verify_hostname`` | ``REG_DWORD``  | 1       |
+-------------------------+----------------+---------+
|``ignore_system_proxy``  |``REG_DWORD``   | 0       |
+-------------------------+----------------+---------+
|``ssl_force_tls_1_2``    |``REG_DWORD``   | 0       |
+-------------------------+----------------+---------+
|``ssl_cert_file``        | ``REG_SZ``     |         |
+-------------------------+----------------+---------+
|``proxy``                | ``REG_SZ``     |         |
+-------------------------+----------------+---------+
|``integration_name``     | ``REG_SZ``     |         |
+-------------------------+----------------+---------+

Unrecognized named values are ignored.

To use the Registry credential provider, create an instance of it, then pass the reference to that instance in the
``credential_provider`` keyword parameter when creating :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>`.  As with credential files, the name of the
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

With Environmental Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The credentials may be supplied to CBC SDK via the environment variables ``CBC_URL``, ``CBC_TOKEN``, ``CBC_ORG_KEY``,
and ``CBC_SSL_VERIFY``. For backwards compatibility with CBAPI, the environment variables ``CBAPI_URL``,
``CBAPI_TOKEN``, ``CBAPI_ORG_KEY``, and ``CBAPI_SSL_VERIFY`` may also be used; if both are specified, the newer
``CBC_xxx`` environment variables override their corresponding ``CBAPI_xxx`` equivalents. To use the environment
variables, they must be set before the application is run (at least ``CBC_URL`` or ``CBAPI_URL``, and ``CBC_TOKEN`` or
``CBAPI_TOKEN``), and the ``credential_file`` keyword parameter to :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>` must be either ``None`` or left
unspecified. (The ``profile`` keyword parameter will be ignored.)

**N.B.:** Passing credentials via the environment can be insecure, and, if this method is used, a warning message to
that effect will be generated in the log.

Using an External Credential Provider
-------------------------------------
Credentials may also be supplied by writing a class that conforms to the ``CredentialProvider`` interface protocol.
When creating :py:mod:`CBCloudAPI <cbc_sdk.rest_api.CBCloudAPI>`, pass a reference to an object of that class in the ``credential_provider`` keyword
parameter. Then pass the name of the profile you want to retrieve to the provider object using the keyword parameter
``profile``.

**Example:**

    >>> provider = MyCredentialProvider()
    >>> cbc_api = CBCloudAPI(credential_provider=provider, profile='default')

Details of writing a credential provider may be found in the "Developing Credential Providers" document.
**TK: better reference**
