VM Workloads Search
==============

Visualize the inventory of vSphere workloads that do not have Carbon Black Cloud sensors installed.

Fetch Compute Resource by ID
----------------------------

Using a query of the ``ComputeResource`` object, you can get the compute resource by ID from your organization.

::

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


Search and Facet Compute Resources
----------------------------------
Using a query of the ``ComputeResource`` object, you can search and facet compute resources in your organization.
The Carbon Black Cloud Python SDK supports a set of criteria filters that can help you find the exact resource or resources you are looking for.

Available criteria filters are:
::

  appliance_uuid
  cluster_name
  eligibility
  installation_status
  ip_address
  name
  os_architecture
  os_type
  uuid


Start by making a simple query with our ComputeResource object.

::

  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.workload import ComputeResource

  >>> cbc = CBCloudAPI()
  >>> query = cbc.select(ComputeResource)

  >>> # Before we print to the console, lets see how many results found we have
  >>> print(len(query))
  >>> 218

Since this is too many entries to print to the console output, try to narrow down the search by adding criteria to the query.
To add a criteria to the query, add the desired method to the ComputeResource object.

The class methods are as follows:
::

  appliance_uuid -> set_appliance_uuid()
  cluster_name -> set_cluster_name()
  eligibility -> set_eligibility()
  installation_status -> set_installation_status()
  ip_address -> set_ip_address()
  name -> set_name()
  os_architecture -> set_os_architecture()
  os_type -> set_os_type()
  uuid -> set_uuid()

Each of these methods accepts an array of strings. You can find more detailed information about the class methods here(link to workload)

Example:
::

  set_appliance_uuid(['ABCD', 'DEFG'])

Next, make a query with a filter for OS type.

::

  >>> from cbc_sdk import CBCloudAPI
  >>> from cbc_sdk.workload import ComputeResource

  >>> cbc = CBCloudAPI()
  >>> filtered_query = cbc.select(ComputeResource).set_os_type(['WINDOWS'])

  >>> # Lets first find out how many results we found with the filtered query.
  >>> print(len(filtered_query))
  >>> 45

  >>> # Great, but not excellent, we can make our query even more specific.
  >>> # We can add any or all of the supported criteria.
  >>> filtered_query = cbc.select(ComputeResource).set_os_type(['WINDOWS']).set_cluster_name(['example-cluster-name'])

  >>> print(len(filtered_query))
  >>> 2

  >>> # And now we can comfortably print our results list object to the console output
  >>> print(*filtered_query)
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


Interactive example script featuring Workloads Search
-------------------------------------------------------------------------------
We have a number of example scripts you can use with the CBC SDK.

.. image:: _static/workloads_example_script.gif

This interactive script highlights the capabilities of the CBC SDK.

You can download it from: `here <https://github.com/carbonblack/carbon-black-cloud-sdk-python/blob/develop/examples/workload/workloads_search_example.py>`_
