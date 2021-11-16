Managing Vulnerabilities
======

The Vulnerability Assessment API allows users to view asset (Endpoint or Workload) vulnerabilities,
increase security visibility, and undertake prioritized proactive security patching on critical systems.
The API provides a summary of vulnerability information filtered at the organization level,
by device, or by vulnerability CVE ID. With a list of vulnerabilities prioritized by severity,
exploitability, and current activity, users can apply proactive and impactful vulnerability patches.
The Carbon Black Cloud Python SDK provides all of the functionalities you might need to use vulnerabilities efficiently.
You can use all of the operations shown in the API such as retrieving, filtering, exporting, and performing actions.
The full list of operations and attributes can be found in the :py:mod:`Vulnerability() <cbc_sdk.platform.vulnerability_assessment.Vulnerability>` class.

For more information see
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/vulnerability-assessment/#get-specific-vcenter-device-vulnerability-summary>`_

Retrieve Vulnerabilities
--------------------

With the example below, you can retrieve the last 5 vulnerabilities with critical severity for an organization.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerabilities = api.select(Vulnerability).set_severity("CRITICAL", "EQUALS")[:5]
    >>> print(vulnerabilities[0].cve_id, vulnerabilities[0].category, vulnerabilities[0].device_count, vulnerabilities[0].os_product_id,
        vulnerabilities[0].os_info, vulnerabilities[0].affected_assets, vulnerabilities[0].product_info, vulnerabilities[0].vuln_info)


Filtering
^^^^^^^^^

You can use the ``where`` method to filter the vulnerabilities. The ``where`` supports strings and solr like queries, alternatively you can use the ``solrq`` query objects
for more complex searches. The example below will search with a solr query search string for the last 5 vulnerabilities in the OS category.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerabilities = api.select(Vulnerability).where("OS")[:5]
    >>> for vulnerability in vulnerabilities:
    ...     print(vulnerabilities.cve_id, vulnerabilities.category, vulnerabilities.device_count, vulnerabilities.os_product_id)


.. tip::
    More information about the ``solrq`` can be found in the
    their `documentation <https://solrq.readthedocs.io/en/latest/index.html>`_.

Retrieve a Device List with a Vulnerability Summary
--------------------------------------------------------------

With the example below, you can retrieve a device list with a Vulnerability Summary for a vCenter Server.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

Retrieve Vulnerability List
----------------

With the example below, you can retrieve a vulnerability list filtered and sorted for a specific operating system and application.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

With the example below you can retrieve a vulnerability list for a vCenter server in csv format.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

With the example below you can retrieve an Operating System or Application Vulnerability List for a specific device.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

Retrieve Vulnerability Details
------------------------

With the example below, you can retrieve vulnerability details for a specific CVE ID.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

Perform Actions on a Device
---------------------

With the example below, you can perform an action on a specific vCenter device.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

Retrieve Affected Assets for a Vulnerability
--------------------------------------

With the example below, you can retrieve a list of assets affected by a specific vulnerability CVE ID.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> tbd

