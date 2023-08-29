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
    >>> device_query = api.select(Device).where('avStatus:AV_ACTIVE')

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
    from cbc_sdk.endpoint_standard import Event
    >>> event_query = api.select(Event).where(hostName='Win10').and_(ipAddress='10.0.0.1')

    # further refine the query
    >>> event_query.and_(applicationName='googleupdate.exe').and_(eventType='REGISTRY_ACCESS')
    >>> event_query.and_(ownerNameExact='DevRel')

The ``where()`` method supplies the initial query parameters, while ``and_()`` and ``or_()`` add additional query
parameters. As with other languages, ``and_()`` gets grouped together before ``or_()``.

Parameters may either be supplied as text strings or as keyword assignments::

    >>> from cbc_sdk.platform import Device
    # the following two queries are equivalent
    >>> string_query = api.select(Device).where("avStatus:AV_ACTIVE")
    >>> keyword_query = api.select(Device).where(avStatus="AV_ACTIVE")

However, mixing the two types in a single query is not allowed::

    # this is not allowed
    >>> from cbc_sdk.platform import Device
    >>> bogus_query = api.select(Device).where(avStatus="AV_ACTIVE").and_("virtualMachine:true")
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
    >>> alert_query.set_criteria("device_os", ["MAC"]).set_criteria("device_os_version", ["10.14.6"])

.. note::

    The ``set_criteria()`` method is supported with Alerts v7, and will be supported in more classes over time.
    As it becomes supported in existing classes, the existing "specific" methods for setting criteria will be
    deprecated.

Executing a Query
-----------------

To execute a query after it's been refined, simply evaluate the query in an *iterable context.*  This may be done
either by passing it to a function that takes iterable values, or by iterating over it in a ``for`` loop.  This
example shows how a device query may be executed::

    # create and refine a device query
    >>> from cbc_sdk.platform import Device
    >>> device_query = api.select(Device).where('avStatus:AV_ACTIVE').set_os(["WINDOWS"])

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

Asynchronous Queries
********************

Some queries may also be executed asynchronously by using the ``execute_async()`` method, which is useful if you have
a query which wil take a long time to execute and you want your script to do other things while waiting for the query
to return.  Here's how we execute the device query from the last example asynchronously::

    # create and refine a device query
    >>> from cbc_sdk.platform import Device
    >>> device_query = api.select(Device).where('avStatus:AV_ACTIVE').set_os(["WINDOWS"])

    # now execute it
    future = device_query.execute_async()

    # await the results
    device_list = future.result()

The ``execute_async()`` method returns a standard ``concurrent.futures.Future`` object, and that ``Future``'s
``result()`` method will return a list with the results of the query.

