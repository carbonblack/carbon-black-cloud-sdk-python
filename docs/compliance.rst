Compliance Benchmarks
======

CIS benchmarks are configuration guidelines published by the Center for Internet Security.
The CIS Benchmark enable configuration and retrieval of Benchmark Sets and Rules in Carbon Black Cloud, and
retrieval of the results from scans performed using these Rules.

For more information on CIS Benchmarks, see the `Center for Internet Security <https://www.cisecurity.org/cis-benchmarks>`_.
CIS benchmarks contain over 100 configuration guidelines created by a global community of cybersecurity experts to safeguard
various systems against attacks targeting configuration vulnerabilities.

You can use all the operations shown in the API, such as retrieving, filtering, reaccessing and enabling/disabling the benchmark rules.
You can locate the full list of operations and attributes in the  :py:mod:`ComplianceBenchmark() <cbc_sdk.workload.compliance_assessment.ComplianceBenchmark>` class.

Resources
---------
* `API Documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/workload-protection/latest/cis-benchmark-api>`_ on Developer Network
* `User Guide <https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-47645D2C-A093-47C8-B4CA-D6F685392733.html>`_

Retrieve Compliance Benchmarks
---------------

By using the following the example, you can retrieve the list of supported benchmarks

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.workload import ComplianceBenchmark
    >>> api = CBCloudAPI(profile='sample')
    >>> benchmark_query = api.select(ComplianceBenchmark)
    >>> for benchmark in benchmark_query:
    >>>     print(benchmark)
    ComplianceBenchmark object, bound to https://defense-test03.cbdtest.io.
    -------------------------------------------------------------------------------

            bundle_name: CIS Compliance - Microsoft Windows Server
            create_time: 2023-03-20T13:44:10.923039Z
            created_by: emuthu+csr@carbonblack.com
                enabled: True
                    id: b7d1b266-d899-4e28-bae6-7619019447ba
                    name: CIS Windows Server Retail application Prod
                os_family: WINDOWS_SERVER
            release_time: 2023-07-10T13:55:59.274881Z
        supported_os_info: [list:5 items]:
                        [0]: {'os_metadata_id': '1', 'os_type': 'WINDOWS', '...
                        [1]: {'os_metadata_id': '2', 'os_type': 'WINDOWS', '...
                        [2]: {'os_metadata_id': '3', 'os_type': 'WINDOWS', '...
                        [...]
                    type: Custom
            update_time: 2024-04-15T21:24:43.283032Z
            updated_by:
                version: 1.0.0.4


Modify Compliance Benchmarks Schedule
---------------

By using the following the example, you can get and set the benchmark assessment schedule

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.workload import ComplianceBenchmark
    >>> api = CBCloudAPI(profile='sample')
    >>> schedule = ComplianceBenchmark.get_compliance_schedule(api)
    >>> print(schedule)
    >>> ComplianceBenchmark.set_compliance_schedule(api, "RRULE:FREQ=DAILY;BYHOUR=17;BYMINUTE=30;BYSECOND=0", "UTC")
    {
        "scan_schedule": "FREQ=WEEKLY;BYDAY=TU;BYHOUR=11;BYMINUTE=30;BYSECOND=0",
        "scan_timezone": "UTC"
    }


Reassess Compliance Benchmarks
---------------

By using the following the example, you can reasses a benchmark

.. code-block:: python

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.workload import ComplianceBenchmark
    >>> api = CBCloudAPI(profile='sample')
    >>> benchmark = api.select(ComplianceBenchmark).first()
    >>> # Execute for all devices matching benchmark
    >>> benchmark.execute_action("REASSESS")
    >>> # Execute for a specific set of devices
    >>> benchmark.execute_action("REASSESS", [ 1, 2, 3 ])
