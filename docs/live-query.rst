Live Query
==========

With Live Query, you can ask questions of endpoints and quickly identify areas for improving security and IT hygiene.

You can use recommended queries created by Carbon Black security experts or craft your own SQL queries. Live Query is
powered by https://osquery.io, an open source project that uses an SQLite interface. This guide will get you started
using Live Query via the Python SDK.

More information about the Audit and Remediation product which uses Live Query is available in the
`Carbon Black Cloud user guide
<https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-129D4F84-1BF0-49F3-BF95-83002FD63217.html/>`_

More information about Live Query APIs is available on the `Developer Network <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/>`_.

Overview
--------
This guide shows how to find specific files on a system. This is the same scenario as the Quick Start Guide for the
APIs on the `Developer Network <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-liveops/latest/livequery-api/>`_

The steps we'll go through are:

#. Set up the python imports and Carbon Black Cloud credentials
#. Start the Query Run
#. Get the Query Run by ID to check the status
#. Get the results of the query

Setting up
----------

The code snippets assume that the python environment has been set up with the necessary imports and credentials.

    >>> from cbc_sdk import CBCloudAPI
    >>> from cbc_sdk import audit_remediation
    >>> from cbc_sdk.audit_remediation import Run, RunHistory, Result, ResultQuery
    >>> api = CBCloudAPI(profile='sample')

For more information on credential handling in the SDK, see :doc:`authentication`

Start a Query Run
-----------------
Set up the query for the file you are looking for.  Then create a query object, execute it, and get the id of the run.

    >>> query_string = "SELECT filename, path FROM file WHERE path = 'C:\\Windows\\Temp\\dbutil_2_3.sys\\' OR path LIKE 'C:\\Users\\%\\AppData\\Local\\Temp\\dbutil_2_3.sys';"
    >>> query_object = api.select(Run).where(sql=query_string)
    >>> run = query_object.submit()
    >>> print(run.id)
    vsc2be500dcuhc1q5bhvq7kdwoqh367i

Get the Query Run to check status
---------------------------------

    >>> run_status = api.select(Run, run.id)
    >>> print(run_status)

The run status returns all the information about the progress of query execution.  These are some of the interesting
fields that show the number of devices available to be queried and progress.

active_org_devices: 93
in_progress_count: 6
last_result_time: 2021-12-23T21:21:26.437Z
match_count: 0
no_match_count: 45
not_started_count: 40
status: ACTIVE
    total_results: 0

Get the results
---------------
Partial results can be reviewed while the query is running.  This snippet gets the results and prints the device
information for each.

    >>> result_query = api.select(Result).run_id(run.id)
    >>> list_result = list(result_query)
    >>> for result in list_result:
    >>> ...    print(f'Device: {result.device_.id} has status {result.status}.  Device message: {result.device_message}')
    >>> ...
    Device: 1234578 has status matched.  Device message:
    Device: 3456789 has status error.  Device message: Error: database or disk is full
    Device: 8765432 has status matched.  Device message:

Other options
-------------
For large result sets it is possible to export the results in several formats including csv, zipped csv and streaming
lines.  These options are documented in :meth:`cbc_sdk.audit_remediation.base.ResultQuery`

This snippet shows writing the results to a zipped csv file.

   >>> api.select(Result).run_id(run.id).export_zipped_csv("/Users/myname/mydir/livequeryresults.zip")

Clean up
---------
Since this is a tutorial we'll clean up when we're done by first stopping the query and then deleting it.

    >>> run.stop()
    True
    >>> run.delete()
    True


