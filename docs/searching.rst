.. _searching-guide:

Searching
=========

Almost every interaction with the Carbon Black Cloud SDK will involve searching for some object on the server that your
code can then inspect or operate on.  Searching in the SDK involves three steps:

1. Create a *query object* with the ``select()`` method.
2. Refine the query by using the query object's methods to add a text *query* and/or *search criteria.*
3. Execute the query to see its results.

Creating a Query Object
-----------------------

A query object is created via the :func:`CBCloudAPI.select() <cbc_sdk.connection.BaseAPI.select>` operation, specifying
the type of data to be retrieved.

In this example, we create a query to search for all devices with antivirus active::

    # assume the CBCloudAPI object is in the variable "api"
    >>> from cbc_sdk.platform import Device
    >>> device_query = api.select(Device).where('status:ACTIVE')

    # The device query has been created but not yet executed
    >>> type(device_query)
    <class 'cbc_sdk.platform.devices.DeviceSearchQuery'>

The ``select()`` method may take either a class reference or a string class name::

    >>> query1 = api.select(Device)
    >>> query2 = api.select("Device")

    # prove that the query we get back in either case is the same
    >>> type(query1) == type(query2)
    True

Selecting an Object Directly
****************************

The ``select()`` method may also be used to retrieve an object directly if you know its ID value, by passing the ID as
a second parameter::

    >>> dev = api.select(Device, 1234567)  # assume this device exists
    >>> type(dev)
    <class 'cbc_sdk.platform.devices.Device'>

Refining a Query
----------------

Queries may support one of two different methods for refining a query:

* Through the use of *text query.*
* Through adding *criteria.*

Text Query Support
******************

Text queries may be added to a query object by using the query object's
:func:`where() <cbc_sdk.base.QueryBuilder.where>`, :func:`and_() <cbc_sdk.base.QueryBuilder.and_>`, and
:func:`or_() <cbc_sdk.base.QueryBuilder.or_>` methods.  The following example sets up a query looking for events
in which the program ``googleupdate.exe`` accesses the system registry on a device with a specific hostname, IP
address, and owner::

    # assume the CBCloudAPI object is in the variable "api"
    >>> from cbc_sdk.platform import Observation
    >>> obs_query = api.select(Observation).where(process_name='svchost.exe').and_(observation_type='CONTEXTUAL_ACTIVITY')

    # further refine the query
    >>> obs_query.and_(event_type='netconn')
    >>> obs_query.and_(netconn_protocol='PROTO_TCP').and_(netconn_port=80)

The ``where()`` method supplies the initial query parameters, while ``and_()`` and ``or_()`` add additional query
parameters. As with other languages, ``and_()`` gets grouped together before ``or_()``.

Parameters may either be supplied as text strings or as keyword assignments::

    >>> from cbc_sdk.platform import Device
    # the following two queries are equivalent
    >>> string_query = api.select(Device).where("status:ACTIVE")
    >>> keyword_query = api.select(Device).where(status="ACTIVE")

However, mixing the two types in a single query is not allowed::

    # this is not allowed
    >>> from cbc_sdk.platform import Device
    >>> bogus_query = api.select(Device).where(status="ACTIVE").and_("virtualMachine:true")
    cbc_sdk.errors.ApiError: Cannot modify a structured query with a raw parameter

Criteria Support
****************

Criteria are usually added to queries using methods specific to each query.  For example, this query looks for alerts
with severity 9 or 10 on a machine running macOS 10.14.6::

    >>> from cbc_sdk.platform import Alert
    >>> alert_query = api.select(Alert)

    # Refine the query with parameters
    >>> alert_query.where(alert_severity=9).or_(alert_severity=10)

    # Refine the query with criteria
    >>> alert_query.set_device_os(["MAC"]).set_device_os_versions(["10.14.6"])

This query produces the following JSON block to be passed to a ``POST`` request to the server:

.. code-block:: json

  {
    "query": "alert_severity:9 OR alert_severity:10",
    "criteria": {
      "device_os": ["MAC"],
      "device_os_version": ["10.14.6"]
    }
  }

In newer queries, the various specific methods for setting each individual criterion will be replaced with a single
method::

    # Refine the query with criteria (new style)
    >>> alert_query.add_criteria("device_os", ["MAC"]).add_criteria("device_os_version", ["10.14.6"])

.. note::

    The ``add_criteria()`` method is explicitly supported with Alerts v7, as well as other query classes that make use
    of ``CriteriaBuilderSupportMixin``. Over time, the existing "specific" methods for setting criteria will be
    deprecated.

Certain queries accept a *time range* criterion, set with the ``set_time_range()`` method.  This allows a range of
times to be specified which returned objects must fall within.  Parameters for ``set_time_range()`` are as follows:

- ``start``: Specifies the starting time of the range, in ISO 8601 format.
- ``end``: Specifies the ending time of the range, in ISO 8601 format.
- ``range``: Specifies the scope of the request in units of time.

A ``range`` parameter begins with a minus sign, marking an interval backwards from the current time. This is followed
by an integer number of units, followed by a letter specifying whether the interval is years ('y'), weeks ('w'),
days ('d'), hours ('h'), minutes ('m'), or seconds ('s').

.. note::

    For ``Process`` search, the ``range`` parameter is called ``window``.

When setting a time range, either ``start`` and ``end`` must *both* be specified, or ``range`` must be specified.
``range`` takes precedence if it is specified alongside ``start`` and/or ``end``.

Executing a Query
-----------------

To execute a query after it's been refined, simply evaluate the query in an *iterable context.*  This may be done
either by passing it to a function that takes iterable values, or by iterating over it in a ``for`` loop.  This
example shows how a device query may be executed::

    # create and refine a device query
    >>> from cbc_sdk.platform import Device
    >>> device_query = api.select(Device).where('status:ACTIVE').set_os(["WINDOWS"])

    # easiest way to execute it is to turn it into a list
    >>> matching_devices = list(device_query)

    # or you can iterate over it using a for loop
    >>> for matching_device in device_query:
    ...     print(f"Matching device ID: {matching_device.id})
    ...
    Matching device ID: 1234
    Matching device ID: 5678

    # using it in a list comprehension also works
    >>> matching_device_ids = [device.id for device in device_query]
    >>> print(matching_device_ids)
    [1234, 5678]

    # you can also use the standard Python len() function to return the number of results
    >>> print(len(device_query))
    2

The ``first()`` or ``one()`` methods on a query always return the first object matched by that query. The difference
between those is that, if there is more than one result for that query, the ``one()`` method will raise an error.

Asynchronous Queries
********************

Some queries may also be executed asynchronously by using the ``execute_async()`` method, which is useful if you have
a query which wil take a long time to execute and you want your script to do other things while waiting for the query
to return.  Here's how we execute the device query from the last example asynchronously::

    # create and refine a device query
    >>> from cbc_sdk.platform import Device
    >>> device_query = api.select(Device).where('status:ACTIVE').set_os(["WINDOWS"])

    # now execute it
    future = device_query.execute_async()

    # await the results
    device_list = future.result()

The ``execute_async()`` method returns a standard ``concurrent.futures.Future`` object, and that ``Future``'s
``result()`` method will return a list with the results of the query.

Faceting
--------

Facet search queries return statistical information indicating the relative weighting of the requested values as per
the specified criteria.  Only certain query types support faceting.

Simple Faceting
***************

Simple faceting is built into certain queries, allowing you to generate a summary on certain fields of all objects that
match the query. To perform this, create and refine a query object as you would normally, then call the ``facets()``
method on the query, passing it the names of the fields you want to facet on.

Here is an example for USB devices::

    >>> from cbc_sdk.endpoint_standard import USBDevice
    >>> usb_devices = api.select(USBDevice).set_statuses(['APPROVED'])
    >>> facet_data = usb_devices.facets(['vendor_name', 'product_name'])

This facet query might produce data that looks like this:

.. code-block:: json

    [
        {
            "field": "vendor_name",
            "values": [
                {
                    "id": "Generic",
                    "name": "Generic",
                    "total": 2
                },
                {
                    "id": "Kingston",
                    "name": "Kingston",
                    "total": 2
                }
            ]
        },
        {
            "field": "product_name",
            "values": [
                {
                    "id": "DataTraveler 3.0",
                    "name": "DataTraveler 3.0",
                    "total": 2
                },
                {
                    "id": "Mass Storage",
                    "name": "Mass Storage",
                    "total": 2
                }
            ]
        }
    ]

Facet Queries
*************

More complex facet queries are performed by creating a query *on* a facet type, then refining it as usual, then getting
the results from the query::

    >>> from cbc_sdk.platform import ObservationFacet
    >>> query = api.select(ObservationFacet).where(process_pid=1000)

Facet queries have two types of special criteria that may be set. One is the ``range`` type which is used to specify
discrete values (integers or timestamps - specified both as seconds since epoch and also as ISO 8601 strings).
The results are then grouped by occurrence within the specified range::

    >>> from cbc_sdk.platform import ObservationFacet
    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> query = api.select(ObservationFacet).where(process_pid=1000).add_range(range)

The range settings are as follows:

* ``field`` - the field to return the range for, should be a discrete one (integer or ISO 8601 timestamp)
* ``start`` - the value to begin grouping at
* ``end`` - the value to end grouping at
* ``bucket_size``- how large of a bucket to group results in. If grouping an ISO 8601 property, use a string
  like ``'-3DAYS'``.

Multiple ranges can be configured per query by passing a list of range dictionaries.

The other special criterion that may be set is the ``term`` type, which allows for one or more fields to use as a
criteria on which to return weighted results. Terms may be added using the ``add_facet_field()`` method, specifying
the name of the field to be summarized::

    >>> from cbc_sdk.platform import ObservationFacet
    >>> query = api.select(ObservationFacet).where(process_pid=1000).add_facet_field("process_name")

Once the facet query has been fully refined, it is executed by examining its ``results`` property::

    >>> from cbc_sdk.platform import EventFacet
    >>> event_facet_query = api.select(EventFacet).add_facet_field("event_type")
    >>> event_facet_query.where(process_guid="WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> event_facet_query.add_range(range)
    >>> synchronous_results = event_facet_query.results
    >>> print(synchronous_results)
    EventFacet object, bound to https://defense-eap01.conferdeploy.net.
    -------------------------------------------------------------------------------
               num_found: 16
      processed_segments: 1
                  ranges: [{'start': '2020-10-16T00:00:00Z', 'end': '2020...
                   terms: [{'values': [{'total': 14, 'id': 'modload', 'na...
          total_segments: 1

Facet queries may also be executed asynchronously, as with other asynchronous queries, by calling their
``execute_async()`` method and then calling the ``result()`` method on the returned ``Future`` object::

    >>> from cbc_sdk.platform import EventFacet
    >>> event_facet_query = api.select(EventFacet).add_facet_field("event_type")
    >>> event_facet_query.where(process_guid="WNEXFKQ7-00050603-0000066c-00000000-1d6c9acb43e29bb")
    >>> range = {
    ...                 "bucket_size": "+1DAY",
    ...                 "start": "2020-10-16T00:00:00Z",
    ...                 "end": "2020-11-16T00:00:00Z",
    ...                 "field": "device_timestamp"
    ...         }
    >>> event_facet_query.add_range(range)
    >>> asynchronous_future = event_facet_query.execute_async()
    >>> asynchronous_result = asynchronous_future.result()
    >>> print(asynchronous_result)
    EventFacet object, bound to https://defense-eap01.conferdeploy.net.
    -------------------------------------------------------------------------------
               num_found: 16
      processed_segments: 1
                  ranges: [{'start': '2020-10-16T00:00:00Z', 'end': '2020...
                   terms: [{'values': [{'total': 14, 'id': 'modload', 'na...
          total_segments: 1

The result for facet queries is a single object with two properties, ``terms`` and ``ranges``, that contain the facet
search result weighted as per the criteria provided::

    >>> print(synchronous_result.terms)
    [{'values': [{'total': 14, 'id': 'modload', 'name': 'modload'}, {'total': 2, 'id': 'crossproc', 'name': 'crossproc'}], 'field': 'event_type'}]
    >>> print(synchronous_result.ranges)
    [{'start': '2020-10-16T00:00:00Z', 'end': '2020-11-16T00:00:00Z', 'bucket_size': '+1DAY', 'field': 'device_timestamp', 'values': None}]

Query Timeouts
--------------

Some search queries make use of a timeout value, specified in milliseconds, which may be specified wither through
a ``timeout`` parameter to a method, or via a ``timeout()`` setter method on a query class.  These timeouts follow a
specific set of rules.

The *absolute maximum* timeout value is 300,000 milliseconds (5 minutes).  No search may have a timeout longer
than this.

An application may specify a *shorter* maximum timeout value for all searches by including it in the credentials,
under the key name ``default_timeout``.  This default timeout value may not be greater than the absolute maximum
timeout.  If this value is specified, no search may have a timeout longer than this value.

This means that, for any given search, the timeout will be the *smallest* of these values:

* The value specified via a parameter to the search, if one was specified.
* The value configured in the credentials, if one is so configured.
* The absolute maximum timeout value, as defined above.

Search Suggestions
------------------

Some classes offer the ability to provide "suggestions" as to search terms that may be employed, via a static method on
the class.  Here is an example for ``Observation``::

    >>> from cbc_sdk.platform import Observation
    >>> suggestions = Observation.search_suggestions(api, query="device_id", count=2)
    >>> for suggestion in suggestions:
    ...     print(suggestion["term"], suggestion["required_skus_all"], suggestion["required_skus_some"])
    device_id [] ['threathunter', 'defense']
    netconn_remote_device_id ['xdr'] []

And here is an example for ``BaseAlert``::

    >>> from cbc_sdk.platform import BaseAlert
    >>> suggestions = BaseAlert.search_suggestions(api, query="device_id")
    >>> for suggestion in suggestions:
    ...     print(suggestion["term"], suggestion["required_skus_some"])
    device_id ['defense', 'threathunter', 'deviceControl']
    device_os ['defense', 'threathunter', 'deviceControl']
    [...additional entries elided...]
    workload_name ['kubernetesSecurityRuntimeProtection']
