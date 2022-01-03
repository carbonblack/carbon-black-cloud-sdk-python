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
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/vulnerability-assessment/>`_

Retrieving Vulnerabilities
--------------------

With the example below, you can retrieve the 5 most recent non-critical vulnerabilities for an organization.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerabilities = api.select(Vulnerability).set_severity("CRITICAL", "NOT_EQUALS")[:5]
    >>> print(vulnerabilities[0])

      affected_assets: [list:1 item]:
                     [0]: DESKTOP-KLVRRM4
           category: APP
             cve_id: CVE-1999-0794
       device_count: 1
            os_info: [dict] {
                            os_arch: 64-bit
                            os_name: Microsoft Windows 10 Pro
                            os_type: WINDOWS
                         os_version: 10.0.18363
                     }
      os_product_id: 37_282511
       product_info: [dict] {
                            arch:
                         product: Microsoft Office
                         release: None
                          vendor: Microsoft Corporation
                         version: 15.0.4693.1005
                     }
          vuln_info: [dict] {
                              active_internet_breach: False
                                          created_at: 1999-10-01T04:00:00Z
                                     cve_description: Microsoft Excel does not warn a user when a mac...
                                              cve_id: CVE-1999-0794
                              cvss_access_complexity: Low
                                  cvss_access_vector: Local access
                                 cvss_authentication: None required
                            cvss_availability_impact: Partial
                         cvss_confidentiality_impact: Partial
                               cvss_exploit_subscore: 3.9
                                cvss_impact_subscore: 6.4
                               cvss_integrity_impact: Partial
                                          cvss_score: 4.6
                            cvss_v3_exploit_subscore: None
                             cvss_v3_impact_subscore: None
                                       cvss_v3_score: None
                                      cvss_v3_vector: None
                                         cvss_vector: AV:L/AC:L/Au:N/C:P/I:P/A:P
                                  easily_exploitable: False
                                            fixed_by: None
                                 malware_exploitable: False
                                            nvd_link: https://nvd.nist.gov/vuln/detail/CVE-1999-0794
                                    risk_meter_score: 1.6
                                            severity: LOW
                                            solution: None
                     }

With the example below, you can retrieve the most recent vulnerability for a specific device type and operating system type.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerability = api.select(Vulnerability).set_device_type("ENDPOINT","EQUALS").set_os_type("WINDOWS","EQUALS").first()
    >>> print(vulnerability)

     affected_assets: [list:1 item]:
                     [0]: DESKTOP-KLVRRM4
           category: APP
             cve_id: CVE-1999-0794
       device_count: 1
            os_info: [dict] {
                            os_arch: 64-bit
                            os_name: Microsoft Windows 10 Pro
                            os_type: WINDOWS
                         os_version: 10.0.18363
                     }
      os_product_id: 37_282511
       product_info: [dict] {
                            arch:
                         product: Microsoft Office
                         release: None
                          vendor: Microsoft Corporation
                         version: 15.0.4693.1005
                     }
          vuln_info: [dict] {
                              active_internet_breach: False
                                          created_at: 1999-10-01T04:00:00Z
                                     cve_description: Microsoft Excel does not warn a user when a mac...
                                              cve_id: CVE-1999-0794
                              cvss_access_complexity: Low
                                  cvss_access_vector: Local access
                                 cvss_authentication: None required
                            cvss_availability_impact: Partial
                         cvss_confidentiality_impact: Partial
                               cvss_exploit_subscore: 3.9
                                cvss_impact_subscore: 6.4
                               cvss_integrity_impact: Partial
                                          cvss_score: 4.6
                            cvss_v3_exploit_subscore: None
                             cvss_v3_impact_subscore: None
                                       cvss_v3_score: None
                                      cvss_v3_vector: None
                                         cvss_vector: AV:L/AC:L/Au:N/C:P/I:P/A:P
                                  easily_exploitable: False
                                            fixed_by: None
                                 malware_exploitable: False
                                            nvd_link: https://nvd.nist.gov/vuln/detail/CVE-1999-0794
                                    risk_meter_score: 1.6
                                            severity: LOW
                                            solution: None
                     }


With the example below you can retrieve the 5 most recent vulnerabilities for a device type sorted by status.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerabilities = api.select(Vulnerability).set_device_type("WORKLOAD","EQUALS").sort_by("status")[:5]
    >>> for vulnerability in vulnerabilities:
    ...     print(vulnerability.cve_id, vulnerability.category, vulnerability.device_count, vulnerability.os_product_id)
    ...

    CVE-2008-5915 APP 1 4_820212
    CVE-2008-5915 APP 1 4_1027024
    CVE-2008-5915 APP 1 4_1107922
    CVE-2008-5915 APP 1 4_1336654
    CVE-2008-5915 APP 1 7_64452

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
    ...     print(vulnerability.cve_id, vulnerability.category, vulnerability.device_count, vulnerability.os_product_id)
    ...

    CVE-2010-3974 OS 2 14_0
    CVE-2010-3974 OS 1 61_0
    CVE-2011-0032 OS 2 14_0
    CVE-2011-0032 OS 1 61_0
    CVE-2011-0034 OS 2 14_0

.. tip::
    More information about the ``solrq`` can be found in the
    their `documentation <https://solrq.readthedocs.io/en/latest/index.html>`_.

Retrieving Vulnerability Details
------------------------

With the example below, you can retrieve vulnerability details for the most recent vulnerability.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerability = api.select(Vulnerability).first()
    >>> print(vulnerability.vuln_info)

    {
        'cve_id': 'CVE-1999-0794',
        'cve_description': 'Microsoft Excel does not warn a user when a macro is present in a Symbolic Link (SYLK) format file.',
        'risk_meter_score': 1.6,
        'severity': 'LOW',
        'fixed_by': None,
        'solution': None,
        'created_at': '1999-10-01T04:00:00Z',
        'nvd_link': 'https://nvd.nist.gov/vuln/detail/CVE-1999-0794',
        'cvss_access_complexity': 'Low',
        'cvss_access_vector': 'Local access',
        'cvss_authentication': 'None required',
        'cvss_availability_impact': 'Partial',
        'cvss_confidentiality_impact': 'Partial',
        'cvss_integrity_impact': 'Partial',
        'easily_exploitable': False,
        'malware_exploitable': False,
        'active_internet_breach': False,
        'cvss_exploit_subscore': 3.9,
        'cvss_impact_subscore': 6.4,
        'cvss_vector': 'AV:L/AC:L/Au:N/C:P/I:P/A:P',
        'cvss_v3_exploit_subscore': None,
        'cvss_v3_impact_subscore': None,
        'cvss_v3_vector': None,
        'cvss_score': 4.6,
        'cvss_v3_score': None
    }

Retrieving Affected Assets for a Vulnerability
--------------------------------------

With the example below, you can retrieve a list of affected assets for the last 5 critical vulnerabilities.

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.platform import Vulnerability
    >>> api = CBCloudAPI(profile='sample')
    >>> vulnerabilities = api.select(Vulnerability).set_severity("CRITICAL", "EQUALS")[:5]
    >>> for vulnerability in vulnerabilities:
    ...     print(vulnerability.affected_assets)
    ...

    ['DESKTOP-KLVRRM4']
    ['DESKTOP-KLVRRM4']
    ['DESKTOP-KLVRRM4']
    ['Windowhost-MAD', 'WINDOWHOST2-MAD']
    ['Windowhost-MAD', 'WINDOWHOST2-MAD']

