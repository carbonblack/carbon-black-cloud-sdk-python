.. Carbon Black Cloud Python SDK documentation master file, created by
   sphinx-quickstart on Thu Apr 28 09:52:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CBC SDK: Carbon Black Cloud SDK for Python
==========================================

In Alpha Development
--------------------

Release v\ |release|.

The Carbon Black Cloud Python SDK provides an easy interface to connect with Carbon Black Cloud products,
including Endpoint Standard, Audit and Remediation, and Enterprise EDR. Use this SDK
to more easily query and manage your endpoints, manipulate data as Python objects, and
harness the full power of Carbon Black Cloud APIs.

Major Features
--------------
- Support For All Carbon Black Cloud Products
    Endpoint Standard, Audit and Remediation, and Enterprise EDR
- Reduced Complexity
    The SDK manages the differences among Carbon Black Cloud APIs
    behind a single, consistent Python interface. Spend less time
    learning specific API calls, and more time controlling your environment.
- More Efficient Performance
    A built-in caching layer makes repeated access to the same resource
    more efficient. Instead of making identical API requests repeatedly,
    the SDK caches the results of the request the first time, and references
    the cache when you make future requests for the resource. This reduces the
    time required to access the resource later.

API Credentials
---------------

To use the SDK and access data in Carbon Black Cloud, you must set up API keys with
the correct permissions. Different APIs have different permission requirements for use,
which is explained in the `Developer Network Authentication Guide
<https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/>`_.

The SDK manages your API credentials for you. There are multiple ways to supply the SDK
with your API credentials, which is explained in :ref:`authentication`.

User Guide
----------

Get started with Carbon Black Cloud Python SDK here. For detailed information on the objects and methods exposed by Carbon Black Cloud Python SDK, see the full API Documentation below.

.. toctree::
   :caption: User Guide
   :maxdepth: 2


   installation
   authentication
   Getting Started <getting-started>
   concepts
   logging
   changelog

SDK Documentation
-----------------

.. toctree::
   :caption: SDK Documentation
   :maxdepth: 2

   cbc_sdk.audit_remediation
   cbc_sdk.credential_providers
   developing-credential-providers
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
