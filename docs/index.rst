.. Carbon Black Cloud Python SDK documentation master file, created by
   sphinx-quickstart on Thu Apr 28 09:52:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CBC SDK: Carbon Black Cloud SDK for Python
==========================================

Release v\ |release|.

The Carbon Black Cloud Python SDK provides an easy interface to connect with Carbon Black Cloud products,
including Endpoint Standard, Audit and Remediation, and Enterprise EDR. Use this SDK
to more easily query and manage your endpoints, manipulate data as Python objects, and
harness the full power of Carbon Black Cloud APIs.

Major Features
--------------
- Supports the following Carbon Black Cloud Products with extensions for new features and products planned
    * Endpoint Standard
    * Audit and Remediation
    * Enterprise EDR
    * Platform
    * Workload
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

Audience for the SDK
--------------------

In general, the Carbon Black Cloud Python SDK is directed at those that:

- Have a working knowledge of Python.
- Have a basic understanding of what the Carbon Black Cloud does, and its basic terminology such as events, alerts,
  and watchlists.

API Credentials
---------------

To use the SDK and access data in Carbon Black Cloud, you must set up API keys with
the correct permissions if you are using the X-Auth-Token authentication method, or create an access token
if you are using Bearer or Personal API Token. Different APIs have different permission requirements for use,
which is explained in the `Developer Network Authentication Guide
<https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/>`_.

The SDK manages your API credentials for you. There are multiple ways to supply the SDK
with your API credentials, which is explained in :ref:`authentication`.

Getting Started
---------------

Get started with Carbon Black Cloud Python SDK here. For detailed information on the objects and methods exposed by Carbon Black Cloud Python SDK, see the full SDK Documentation below.

.. toctree::
   :caption: User Guide
   :maxdepth: 2

   installation
   authentication
   Getting Started <getting-started>
   concepts
   resources
   porting-guide

Guides
------

.. toctree::
   :caption: Guides
   :maxdepth: 2

   alerts
   developing-credential-providers
   audit-log
   device-control
   differential-analysis
   live-query
   live-response
   policy
   recommendations
   reputation-override
   unified-binary-store
   users-grants
   vulnerabilities
   watchlists-feeds-reports
   workload

Full SDK Documentation
----------------------

See detailed information on the objects and methods exposed by the Carbon Black Cloud Python SDK here.

.. toctree::
   :caption: SDK Documentation
   :maxdepth: 4

   cbc_sdk.audit_remediation
   cbc_sdk.credential_providers
   cbc_sdk.endpoint_standard
   cbc_sdk.enterprise_edr
   cbc_sdk.platform
   cbc_sdk.workload
   cbc_sdk
   logging
   os_functional_testing
   changelog
   exceptions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
