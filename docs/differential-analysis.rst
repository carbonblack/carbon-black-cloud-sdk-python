Differential Analysis
=====================

Differential Analysis provides the ability to compare and understand the changes between two
`Live Query <https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/cbc_sdk.audit_remediation/#cbc_sdk.audit_remediation.base.Run>`_ runs.
The differential is calculated based on point-in-time snapshots. These features answer the question, “What changed on endpoints, and when?”.

Overview
--------
This guide follows the steps for comparing two “point-in-time snapshots” of endpoints using a few different options and downloading the results using the Differential object.
This example aims to understand what Firefox add-ons were added or removed between the two Live Query snapshot intervals.

**1. Prerequisites**

To perform a Differential Analysis, create the "point-in-time" snapshots of your endpoints with Live Query or use existing ones.
You can find a step-by-step Live Query API guide `here <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/#quick-start>`_ and
a version for the CBC Python SDK `here <https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/live-query/>`_.
The example Live Query runs look for added or removed Firefox add-ons.

**2. Query Comparison**

Start a Query Comparison with the ID's you received from step 1. If the supplied ``newer_run_id`` is from a recurring Live Query run,
the ``older_run_id`` is not required - the backend will automatically compare it to previous to the supplied one.
The backend will throw a specific error if you provide a query id from a single Live Query run.
You can read more about it `here <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/differential-analysis-api/#query-comparison>`_.

Query Comparison
----------------

Basic Query
###########

This example shows the basic result of the ``Differential`` object. The ``.newer_run_id()`` method is required - it accepts the
run id that you want to mark as the starting point-in-time snapshot. By default, only the number of changes between the two runs are returned.
To receive the actual differential data, use the ``.count_only()`` method, as featured in the Actual Changes example.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.audit_remediation import Differential
    >>>
    >>> cbc = CBCloudAPI(profile='sample')
    >>>
    >>> query = cbc.select(Differential).newer_run_id('jcdqsju4utpaayj5dh5r2llzffeolg0u').older_run_id('yhbg3wcea9y1l4asiltky5tupkgauzas')
    >>> # The content of query object always has a length of 1, and contains the Differential response.
    >>> print(*query)
    Differential object, bound to https://defense-dev01.cbdtest.io.
    diff_processed_time: 0.633
    diff_results: [list:1 item]:
    [0]: {'device_id': 12345, 'change_count': 1, 'add...
    newer_run_create_time: 2022-08-10T13:07:44.194Z
    newer_run_id: jcdqsju4utpaayj5dh5r2llzffeolg0u
    newer_run_not_responded_devices: [list:0 items]
    older_run_create_time: 2022-08-10T12:57:03.872Z
    older_run_id: yhbg3wcea9y1l4asiltky5tupkgauzas
    older_run_not_responded_devices: [list:0 items]


You can also access a dictionary representation of the response with the ``._info`` property.

    >>> print(resp[0]._info)
    {'diff_processed_time': 0.037,
     'diff_results': [{'added_count': 1,
                       'change_count': 1,
                       'changes': None,
                       'device_id': 12345,
                       'newer_run_row_count': 21,
                       'older_run_row_count': 20,
                       'removed_count': 0}],
     'newer_run_create_time': '2022-08-10T13:07:44.194Z',
     'newer_run_id': 'jcdqsju4utpaayj5dh5r2llzffeolg0u',
     'newer_run_not_responded_devices': [],
     'older_run_create_time': '2022-08-10T12:57:03.872Z',
     'older_run_id': 'yhbg3wcea9y1l4asiltky5tupkgauzas',
     'older_run_not_responded_devices': []}


Actual Changes
##############

Using the ``.count_only()`` method with a value of ``False`` will allow you to see the actual changes between the two snapshots.
To use this method, append it to the rest of the Differential object query. The actual changes will be in the ``changes`` property, under ``diff_results``.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.audit_remediation import Differential
    >>>
    >>> cbc = CBCloudAPI(profile='sample')
    >>>
    >>> query = cbc.select(Differential).newer_run_id('jcdqsju4utpaayj5dh5r2llzffeolg0u').older_run_id('yhbg3wcea9y1l4asiltky5tupkgauzas')
    >>> actual_changes = query.count_only(False)
    >>> print(actual_changes[0]._info)
        {'diff_processed_time': 0.039,
         'diff_results': [{'added_count': 1,
                           'change_count': 1,
                           'changes': [{'action': 'ADDED',
                                        'fields': [{'key': 'name',
                                                    'value': 'AdBlocker Ultimate'}]}],
                           'device_id': 12345,
                           'newer_run_row_count': 21,
                           'older_run_row_count': 20,
                           'removed_count': 0}],
         'newer_run_create_time': '2022-08-10T13:07:44.194Z',
         'newer_run_id': 'jcdqsju4utpaayj5dh5r2llzffeolg0u',
         'newer_run_not_responded_devices': [],
         'older_run_create_time': '2022-08-10T12:57:03.872Z',
         'older_run_id': 'yhbg3wcea9y1l4asiltky5tupkgauzas',
         'older_run_not_responded_devices': []}


In the example response you can see that ``AdBlocker Ultimate`` add-on was added between the two snapshot intervals.


Filter Devices
##############

Using the ``.set_device_ids()`` you can narrow down the query to a specific devices only. The method accepts an array of integers.
To use this method, append it to the rest of the Differential object query or combine it with any of the other methods.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.audit_remediation import Differential
    >>>
    >>> cbc = CBCloudAPI(profile='sample')
    >>>
    >>> query = cbc.select(Differential).newer_run_id('jcdqsju4utpaayj5dh5r2llzffeolg0u').older_run_id('yhbg3wcea9y1l4asiltky5tupkgauzas')
    >>> actual_changes = query.count_only(False).set_device_ids([12345])
    >>> print(actual_changes[0]._info)
        {'diff_processed_time': 0.039,
         'diff_results': [{'added_count': 1,
                           'change_count': 1,
                           'changes': [{'action': 'ADDED',
                                        'fields': [{'key': 'name',
                                                    'value': 'AdBlocker Ultimate'}]}],
                           'device_id': 12345,
                           'newer_run_row_count': 21,
                           'older_run_row_count': 20,
                           'removed_count': 0}],
         'newer_run_create_time': '2022-08-10T13:07:44.194Z',
         'newer_run_id': 'jcdqsju4utpaayj5dh5r2llzffeolg0u',
         'newer_run_not_responded_devices': [],
         'older_run_create_time': '2022-08-10T12:57:03.872Z',
         'older_run_id': 'yhbg3wcea9y1l4asiltky5tupkgauzas',
         'older_run_not_responded_devices': []}



Export Results
##############

Using the ``.async_export()`` you can create an asynchronous job that exports the results from the run.
To use this method, append it to the rest of the Differential object query or combine it with any of the other methods.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk.audit_remediation import Differential
    >>>
    >>> cbc = CBCloudAPI(profile='sample')
    >>>
    >>> query = cbc.select(Differential).newer_run_id('jcdqsju4utpaayj5dh5r2llzffeolg0u').older_run_id('yhbg3wcea9y1l4asiltky5tupkgauzas')
    >>> export = query.count_only(False).set_device_ids([12345]).async_export()
    >>> export.await_completion()
    >>> # write the results to a file
    >>> export.get_output_as_file("example_data.json")
