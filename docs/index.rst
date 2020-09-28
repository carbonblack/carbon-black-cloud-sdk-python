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


Major Features
--------------


API Credentials
---------------


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
