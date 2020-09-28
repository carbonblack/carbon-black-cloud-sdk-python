.. Carbon Black Cloud Python SDK documentation master file, created by
   sphinx-quickstart on Thu Apr 28 09:52:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CBC SDK: Carbon Black Cloud SDK for Python
==========================================

Release v\ |release|.

To regenerate docs (while in /cbc_sdk):
  >>> sphinx-apidoc -f -o docs src/cbc_sdk
Then while in /docs:
  >>> make html
View the documentation by opening docs/_build/html/index.html

Carbon Black Cloud Python SDK provides a straightforward interface to the VMware Carbon Black Cloud products: Endpoint Standard, Audit and Remediation, and Enterprise EDR.
This library provides a Pythonic layer to access the raw power of the REST APIs of all Carbon Black products, making it easier to query data from any platform or on-premise APIs, combine data from multiple API calls, manage all API credentials in one place, and manipulate data as Python objects. Take a look::


As of version 1.2, Carbon Black Cloud Python SDK also supports Carbon Black Cloud Endpoint Standard (formerly CB Defense):

   >>> from cbapi.psc.defense import *
   >>> #
   >>> # Create our CB Defense API object
   >>> #
   >>> p = CbDefenseAPI()
   >>> #
   >>> # Select any devices that have the hostname WIN-IA9NQ1GN8OI and an internal IP address of 192.168.215.150
   >>> #
   >>> devices = c.select(Device).where('hostNameExact:WIN-IA9NQ1GN8OI').and_("ipAddress:192.168.215.150").first()
   >>> #
   >>> # Change those devices' policy into the Windows_Restrictive_Workstation policy.
   >>> #
   >>> for dev in devices:
   >>>     dev.policyName = "Restrictive_Windows_Workstation"
   >>>     dev.save()


Major Features
--------------


API Credentials
---------------

Carbon Black Cloud Python SDK version 0.9.0 enforces the use of credential files.

In order to perform any queries via the API, you will need to get the API token for your CB user. See the documentation
on the Developer Network website on how to acquire the API token for
`Carbon Black EDR (CB Response) <http://developer.carbonblack.com/reference/enterprise-response/authentication/>`_,
`Carbon Black App Control (CB Protection) <http://developer.carbonblack.com/reference/enterprise-protection/authentication/>`_, or
`Carbon Black Cloud Endpoint Standard (CB Defense) <http://developer.carbonblack.com/reference/cb-defense/authentication/>`_.

Once you acquire your API token, place it in one of the default credentials file locations:

* ``/etc/carbonblack/``
* ``~/.carbonblack/``
* ``/current_working_directory/.carbonblack/``

For distinction between credentials of different Carbon Black products, use the following naming convention for your credentials files:

* ``credentials.psc`` for Carbon Black Cloud Endpoint Standard, Audit & Remediation, and Enterprise EDR (CB Defense, CB LiveOps, and CB ThreatHunter)
* ``credentials.response`` for Carbon Black EDR (CB Response)
* ``credentials.protection`` for Carbon Black App Control (CB Protection)

For example, if you use a Carbon Black Cloud product, you should have created a credentials file in one of these locations:

* ``/etc/carbonblack/credentials.psc``
* ``~/.carbonblack/credentials.psc``
* ``/current_working_directory/.carbonblack/credentials.psc``

Credentials found in a later path will overwrite earlier ones.

The credentials are stored in INI format. The name of each credential profile is enclosed in square brackets, followed
by key-value pairs providing the necessary credential information::

    [default]
    url=https://localhost
    token=abcdef0123456789abcdef
    ssl_verify=False

    [prod]
    url=https://cbserver.prod.corp.com
    token=aaaaaa
    ssl_verify=True

    [otheruser]
    url=https://localhost
    token=bbbbbb
    ssl_verify=False

The possible options for each credential profile are:

* **url**: The base URL of the Carbon Black server. This should include the protocol (https) and the hostname, and nothing else.
* **token**: The API token for the user ID. More than one credential profile can be specified for a given server, with
  different tokens for each.
* **ssl_verify**: True or False; controls whether the SSL/TLS certificate presented by the server is validated against
  the local trusted CA store.
* **org_key**: The organization key. This is required to access the Carbon Black Cloud, and can be found in the console. The format is ``123ABC45``.
* **proxy**: A proxy specification that will be used when connecting to the Carbon Black server. The format is:
  ``http://myusername:mypassword@proxy.company.com:8001/`` where the hostname of the proxy is ``proxy.company.com``, port
  8001, and using username/password ``myusername`` and ``mypassword`` respectively.
* **ignore_system_proxy**: If you have a system-wide proxy specified, setting this to True will force Carbon Black Cloud Python SDK to bypass
  the proxy and directly connect to the Carbon Black server.

Future versions of Carbon Black Cloud Python SDK will also provide the ability to "pin" the TLS certificate so as to provide certificate
verification on self-signed or internal CA signed certificates.

Environment Variable Support

The latest Carbon Black Cloud Python SDK for Python supports specifying API credentials in the following three environment variables:

`Carbon Black Cloud Python SDK_TOKEN` the envar for holding the CbR/CbP api token or the ConnectorId/APIKEY combination for Endpoint Standard (CB Defense)/Carbon Black Cloud.

The `Carbon Black Cloud Python SDK_URL` envar holds the FQDN of the target, a CbR , CBD, or CbD/Carbon Black Cloud server specified just as they are in the
configuration file format specified above.

The  optional `Carbon Black Cloud Python SDK_SSL_VERIFY` envar can be used to control SSL validation(True/False or 0/1), which will default to ON when
not explicitly set by the user.

Backwards & Forwards Compatibility
----------------------------------

User Guide
----------

Get started with Carbon Black Cloud Python SDK here. For detailed information on the objects and methods exposed by Carbon Black Cloud Python SDK, see the full API Documentation below.

.. toctree::
   :maxdepth: 2


   installation
   getting-started
   concepts
   logging
   changelog

API Documentation
-----------------

Once you have read the User Guide, you can view `examples on GitHub <https://github.com/carbonblack/cbapi-python/tree/master/examples>`_
or try writing code of your own. You can use the full API documentation below to see all the methods available in Carbon Black Cloud Python SDK
and unlock the full functionality of the SDK.

.. toctree::
   :maxdepth: 2

   cbc_sdk.audit_remediation
   cbc_sdk.credential_providers
   cbc_sdk.endpoint_standard
   cbc_sdk.enterprise_edr
   cbc_sdk.platform
   cbc_sdk
   exceptions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
