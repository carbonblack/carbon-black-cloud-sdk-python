Developing New Credential Providers
===================================
The credentials management framework for the CBC SDK is designed to allow different handlers to be implemented, which
may supply credentials to the ``CBCloudAPI`` in ways not implemented by existing credential handlers.

Writing the Credential Provider
-------------------------------
Find all classes required to implement a new credential provider in the ``cbc_sdk.credentials`` package. See below for
descriptions of the classes. It is recommended, but not required, that your new credential provider inherit from the
``CredentialProvider`` abstract class, and that you implement the methods from that abstract class as detailed.

The arguments to the standard ``__init__()`` method are not defined by the interface specification; those may be used
to initialize your credential provider in any desired fashion.

Using the Credential Provider
-----------------------------
Create an instance of your credential provider object and pass it as the keyword parameter
``credential_provider`` when creating your ``CBCloudAPI`` object.  Example:

    >>> provider = MyCredentialProvider()
    >>> cbc_api = CBCloudAPI(credential_provider=provider, profile='default')

Your credential provider's ``get_credentials()`` method will be called, passing in any profile specified in the
``profile`` keyword parameter used when creating ``CBCloudAPI``.

Credential Provider Reference
-----------------------------
These are the classes from the ``cbc_sdk.credentials`` package that are used in making a credential provider.

CredentialValue class
+++++++++++++++++++++
This class is of an enumerated type, and represents the various credential items loaded by the credential provider
and fed to the rest of the SDK code.  The possible values are:

* ``URL`` - The URL used to access the Carbon Black Cloud.  This value *must* be specified.
* ``TOKEN`` - The access token to be used to authenticate to the server. It is the same structure as the
  ``X-Auth-Token:`` defined for direct API access in `the developer documentation`_. This value *must* be specified.
* ``ORG_KEY`` - The organization key specifying which organization to work with.  This value *must* be specified.
* ``SSL_VERIFY`` - A Boolean value indicating whether or not to validate the SSL connection.
  The default is ``True``.
* ``SSL_VERIFY_HOSTNAME`` - A Boolean value indicating whether or not to verify the host name of the
  server being connected to. The default is ``True``.
* ``SSL_CERT_FILE`` - The name of an optional certificate file used to validate the certificates of the SSL connection.
  If not specified, the standard system certificate verification will be used.
* ``SSL_FORCE_TLS_1_2`` - A Boolean value. If this is ``True``, the connection will be forced to use TLS 1.2
  rather than any later version. The default is ``False``.
* ``PROXY`` - If specified, this is the name of a proxy host to be used in making the connection.
* ``IGNORE_SYSTEM_PROXY`` - A Boolean value. If this is ``True``, any system proxy settings will be ignored
  in making the connection to the server. The default is ``False``.

.. _`the developer documentation`: https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/#creating-an-api-key

Values of this type have one method:

**requires_boolean_value**

``def requires_boolean_value(self):``

Returns whether or not this particular credential item takes a Boolean value.

Returns: ``True`` if the credential item takes a Boolean value, ``False`` if the credential item takes a
string value.

Credentials class
+++++++++++++++++
The class that holds credentials retrieved from the credential provider, and is used by the rest of the SDK.  It is
effectively immutable after creation.

**__init__**

``def __init__(self, values=None):``

Initializes a new ``Credentials`` object.

Parameters:

* ``values`` (type ``dict``): A dictionary containing the values to initialize the ``Credentials`` object with.  The
  keys of this dictionary may be either ``CredentialValue`` objects or their lowercase string equivalents, e.g.
  ``CredentialValue.URL`` or ``"url"``.  The values in the dict are strings for those credential items with string
  values. For credential items with Boolean values, the values may be either ``bool`` values, numeric values (with 0
  being treated as ``False`` and non-zero values treated as ``True``), or string values.  In the case of string values,
  the value must be "0", "false", "off", or "no" to be treated as a ``False`` falue, or "1", "true", "on", or
  "yes" to be treated as a ``True`` value (all values case-insensitive).  If an unrecognized string is used for a
  Boolean value, ``CredentialError`` will be raised.  Unrecognized keys in the dict are ignored.  Any missing items will
  be replaced by the default for that item.

Raises:

* ``CredentialError`` - If there is an error parsing a Boolean value string.

**get_value**

``def get_value(self, key):``

Retrieves a specific credential value from this object.

Parameters:

* ``key`` (type ``CredentialValue``): Indicates which item to retrieve.

Returns: The value of that credential item (``str`` or ``bool`` type).

**__getattr__**

``def __getattr__(self, name):``

Retrieves a specific credential value from this object.  This is a bit of "syntactic sugar" allowing other code to
access credential values, for instance, as ``cred_object.url`` instead of
``cred_object.get_value(CredentialValue.URL)``.

Parameters:

* ``name`` (type ``str``): Indicates which item to retrieve.

Returns: The value of that credential item (``str`` or ``bool`` type).

Raises:

* ``AttributeError`` - If the credential item ``name`` was unrecognized.

CredentialProvider class
++++++++++++++++++++++++
All credential providers *should* extend this abstract class, but, in any event, *must* implement the protocol it
defines.

**get_credentials**

``def get_credentials(self, section=None):``

Return a Credentials object containing the configured credentials.

Parameters:

* ``section`` (type ``str``): Indicates the credential section to retrieve.  May be interpreted by the credential
  provider in amy manner it likes; may also be ignored.

Returns: A ``Credentials`` object containing the retrieved credentials.

Raises:

* ``CredentialError`` - If there is an error retrieving the credentials.
