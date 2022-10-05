VM Workloads Search Guide and Examples
======================================

These APIs allow you to visualize the inventory of compute resources available under either vSphere
or AWS.

.. note::
  A *compute resource* is a virtual machine without a sensor installed.

The API operations center around the ``VSphereComputeResource`` object for vSphere compute resources,
or around the ``AWSComputeResource`` for AWS compute resources.

.. note::
  The object name ``ComputeResource`` is an alias for ``VSphereComputeResource``, provided for
  backwards compatibility with earlier versions of the SDK.

Search Compute Resources
------------------------
By querying on one of the compute resource object types, you can obtain a list of matching
compute resources.  The SDK supports filtering by a number of different criteria, which are different
for each compute resource type.

**For VSphereComputeResource:**

- ``appliance_uuid``
- ``cluster_name``
- ``datacenter_name``
- ``deployment_type``
- ``esx_host_name``
- ``esx_host_uuid``
- ``vcenter_name``
- ``vcenter_host_url``
- ``vcenter_uuid``
- ``name``
- ``host_name``
- ``ip_address``
- ``device_guid``
- ``registration_id``
- ``eligibility``
- ``eligibility_code``
- ``installation_status``
- ``installation_type``
- ``uuid``
- ``os_description``
- ``os_type``
- ``os_architecture``
- ``vmwaretools_version``

**For AWSComputeResource:**

- ``auto_scaling_group_name``
- ``availability_zone``
- ``cloud_provider_account_id``
- ``cloud_provider_resource_id``
- ``cloud_provider_tags``
- ``deployment_type``
- ``id``
- ``installation_status``
- ``name``
- ``platform``
- ``platform_details``
- ``region``
- ``subnet_id``
- ``virtual_private_cloud_id``

Any of these criteria may be specified to be included in search results by calling the method ``set_XXX``,
or excluded by calling the method ``exclude_XXX``, where ``XXX`` is the specific criteria name.

Example (vSphere workloads)::

  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.workload import VSphereComputeResource

  >>> cbc = CBCloudAPI()
  >>> query = cbc.select(VSphereComputeResource).set_os_type(['WINDOWS']).set_cluster_name(['example-cluster-name'])
  >>> results = list(query)
  >>> print(results)

Example Output::

  ComputeResource object, bound to https://defense-dev01.cbdtest.io.
  -------------------------------------------------------------------------------

          appliance_uuid: c74bca54-e903-49e8-9962-2bb895f428c1
            cluster_name: example-cluster-name
              created_at: 2021-02-25T04:54:41.362Z
         datacenter_name: cwp-bucket-1-datacenter
             eligibility: ELIGIBLE
        eligibility_code: None
           esx_host_name: 10.105.17.113
           esx_host_uuid: a2311b42-3e53-8f21-97d7-66680007185f
               host_name: appd2012
                      id: 19902164
     installation_status: NOT_INSTALLED
    installation_status_code:
              ip_address: 10.105.17.84
                    name: cwp-bucket-1-windows_2012
         os_architecture: 64
          os_description: Microsoft Windows Server 2012 (64-bit)
                 os_type: WINDOWS
                    uuid: 500e14e6-3ea6-23aa-11bd-8e68444c6ce4
        vcenter_host_url: 10.105.17.114
            vcenter_name: VMware vCenter Server 6.7.0 build-14368073
            vcenter_uuid: 9a8a0be5-ae1e-49ce-b2aa-34bc7dc445e3
     vmwaretools_version: 11328 ComputeResource object, bound to https://defense-dev01.cbdtest.io.
  -------------------------------------------------------------------------------

          appliance_uuid: c74bca54-e903-49e8-9962-2bb895f428c1
            cluster_name: example-cluster-name
              created_at: 2021-02-25T04:54:41.362Z
         datacenter_name: cwp-bucket-1-datacenter
             eligibility: ELIGIBLE
        eligibility_code: None
           esx_host_name: 10.105.17.113
           esx_host_uuid: a2311b42-3e53-8f21-97d7-66680007185f
               host_name: appd2k8r2
                      id: 19902168
     installation_status: NOT_INSTALLED
    installation_status_code:
              ip_address: 10.105.17.237
                    name: cwp-bucket-1-windows_2008
         os_architecture: 64
          os_description: Microsoft Windows Server 2008 R2 (64-bit)
                 os_type: WINDOWS
                    uuid: 500e51ff-ca0d-5a70-a799-2595c9e87000
        vcenter_host_url: 10.105.17.114
            vcenter_name: VMware vCenter Server 6.7.0 build-14368073
            vcenter_uuid: 9a8a0be5-ae1e-49ce-b2aa-34bc7dc445e3
     vmwaretools_version: 11328 ComputeResource object, bound to https://defense-dev01.cbdtest.io.

Example (AWS workloads)::

  TODO

Fetch Compute Resource by ID
----------------------------
Using a query of the ``VCenterComputeResource`` or ``AWSComputeResource`` objects, you can get the
compute resource by ID from your organization.

Example (vSphere workloads)::

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.workload import ComputeResource

    >>> # This is an example id that we want to query
    >>> id = 15054425

    >>> cbc = CBCloudAPI()
    >>> query = cbc.select(ComputeResource, id)

    >>> # A string object is returned here, so we can print the result directly.
    >>> print(query)

    ComputeResource object, bound to https://defense-dev01.cbdtest.io.
     Last refreshed at Mon Mar  1 12:02:14 2021
    -------------------------------------------------------------------------------

              appliance_uuid: c89f183b-f201-4bca-bacc-80184b5b8823
                cluster_name: example-cluster-name
                  created_at: 2020-11-18T07:41:16.834Z
             datacenter_name: None
                 eligibility: NOT_ELIGIBLE
            eligibility_code: ['Launcher not found']
               esx_host_name: 10.105.7.129
               esx_host_uuid: bb8d2842-0438-9a74-7964-1d0efad10f28
                   host_name: localhost.localdomain
                          id: 15054425
         installation_status: NOT_INSTALLED
        installation_status_code: None
                  ip_address: 10.105.7.201
                        name: CB-ServiceTest
             os_architecture: 64
              os_description: CentOS 7 (64-bit)
                     os_type: CENTOS
                        uuid: 5022227f-947a-84f8-5816-747f5e18e5ac
            vcenter_host_url: 10.105.5.63
                vcenter_name: VMware vCenter Server 7.0.0 build-15952599
                vcenter_uuid: 4a6b1382-f917-4e1a-8564-374cb7274bd7
         vmwaretools_version: 10336

Example (AWS workloads)::

    TODO

Facet Compute Resources
-----------------------

Any compute resource search may be turned into a *faceting* by calling the ``facet()`` method on the
query object returned by ``select()``, after setting search criteria.  A faceting breaks down each
specified field for all compute resources matching the criteria, showing which values that field can take
and how many times that field value shows up in the matching compute resources.  Only a subset of fields
can be faceted on, as listed here:

**For VSphereComputeResource:**

- ``eligibility``
- ``installation_status``
- ``vmwaretools_version``
- ``os_type``

**For AWSComputeResource:**

- ``auto_scaling_group_name``
- ``cloud_provider_tags``
- ``platform``
- ``platform_details``
- ``virtual_private_cloud_id``

Example (vSphere workloads)::

    TODO

Example (AWS workloads)::

    TODO

Download Compute Resource Listings
----------------------------------

The details of compute resources matching a search may be directly downloaded from the Carbon Black Cloud
by callin the ``download()`` method on the query object returned by ``select()``, after setting
search criteria.  The format for downloading may be specified as either JSON or CSV.

The ``download()`` method returns a ``Job`` object, which is processed asynchronously and from which
the results are available once the job has been completed.

Example (vSphere workloads)::

    TODO

Example (AWS workloads)::

    TODO

Summarize Compute Resources
---------------------------

.. note::
  This functionality is not available for vSphere compute resources.

By calling the ``summarize()`` method on the query object returned by ``select()``, after setting
search criteria, a summary of compute resources may be generated.  The fields which may be summarized
are as follows:

**For AWSComputeResource:**

- ``availability_zone``
- ``region``
- ``subnet_id``
- ``virtual_private_cloud_id``
- ``security_group_id``

Example (AWS workloads)::

    TODO

Interactive example script featuring Workloads Search
-----------------------------------------------------
We have a number of example scripts you can use with the CBC SDK.

.. image:: _static/workloads_example_script.gif

This interactive script highlights the capabilities of the CBC SDK. It uses user input to guide you
through the functionalities of the Workloads Search.

You can download it from: `here <https://github.com/carbonblack/carbon-black-cloud-sdk-python/blob/develop/examples/workload/workloads_search_example.py>`_
