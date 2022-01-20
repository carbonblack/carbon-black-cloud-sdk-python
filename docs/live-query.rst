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
#. Look at the results
#. Write the results to a file
#. Clean up since this is a tutorial
#. Get the run information for scheduled queries (templates)

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
    >>> print(f'Run id: {run.id} has {run.active_org_devices} active devices in the org of which {run.in_progress_count} are in progress and {run.not_started_count} have not started')
    Run id: vsc2be500dcuhc1q5bhvq7kdwoqh367i has 97 active devices in the org of which 0 are in progress and 97 have not started

Check status
------------

Give the run a few seconds to initialise, then refresh the information and print some statistics.

    >>> run.refresh()
    True
    >>> print(f'Run id: {run.id} has {run.active_org_devices} active devices in the org of which {run.in_progress_count} are in progress and {run.not_started_count} have not started')
    Run id: vsc2be500dcuhc1q5bhvq7kdwoqh367i has 97 active devices in the org of which 45 are in progress and 33 have not started

The run status returns all the information about the progress of query execution.  These are some of the interesting
fields that show the number of devices available to be queried and progress.

    * active_org_devices: 97
    * error_count: 3
    * in_progress_count: 45
    * last_result_time: 2021-12-23T21:21:26.437Z
    * match_count: 0
    * no_match_count: 45
    * not_started_count: 40
    * status: ACTIVE
    * total_results: 0

All details of the run can be pretty printed with
    >>> print(run)

Get the results
---------------
Partial results can be reviewed while the query is running.  This snippet gets the results and prints the device
information for each.

    >>> result_query = api.select(Result).run_id(run.id)
    >>> list_result = list(result_query)
    >>> for result in list_result:
    >>>     print(f'Device: {result.device_.id} has status {result.status}.  Device message: {result.device_message}')
    Device: 1234578 has status matched.  Device message:
    Device: 3456789 has status error.  Device message: Error: database or disk is full
    Device: 8765432 has status matched.  Device message:

There is also a helper option to get the results:
    >>> results_by_helper = run.query_results()

Other options
-------------
It is possible to export the results in several formats including csv, zipped csv and streaming
lines.  These options are documented in :meth:`cbc_sdk.audit_remediation.base.ResultQuery`

This snippet shows writing the results to a zipped csv file.

   >>> result_query.export_zipped_csv("/Users/myname/mydir/livequeryresults.zip")

For very large result sets there is an asynchronous API call.  The SDK makes use of Python Futures to wait for the
underlying call to complete.

For this call, in addition to live query permissions the API Key will require jobs.status(READ).

The sequence of calls are:

    >>> # first an extra import
    >>> from cbc_sdk.platform import Job
    >>> # then start the job
    >>> job = result_query.async_export()
    >>> # show the status is progress
    >>> print(job.status)
    IN_PROGRESS
    >>> # wait for it to finish and refresh the information in the SDK
    >>> job.await_completion()
    >>> job.refresh()
    >>> # show the job has completed
    >>> print(job.status)
    COMPLETED
    >>> # write the results to a csv file
    >>> job.get_output_as_file("/Users/myname/mydir/livequeryresults_async.csv")


Clean up
---------
Since this is a tutorial we'll clean up when we're done by first stopping the run and then deleting it.

Stopping the run will prevent the request going to any devices that have not yet checked in but will not stop the
query running on any that are in progress.  Checking in the console, the run and results will be visible with a
status of Stopped.

    >>> run.stop()
    True
    >>> print(run.status)
    CANCELLED

Since this is a tutorial, we can fully clean up.  This deletes the results so is probably not what you usually want.
It will not be visible in the console and attempting to refresh the object will return the error "cannot refresh a deleted query".

    >>> run.delete()
    True

A footnote on scheduled runs (templates)
----------------------------------------
A template is a query that is scheduled to run periodically. It is likely easier to configured these using the Carbon Black
Cloud console, but retrieving the result for import to another system may be useful.

An additional import:

    >>> from cbc_sdk.audit_remediation import Template, TemplateHistory

List all the templates (scheduled queries):

    >>> all_templates = api.select(TemplateHistory)
    >>> for t in list(all_templates):
    >>>     print(f'Name = {t.name}, id = {t.id}, next run time = {t.next_run_time}')

A where clause can be added to limit the templates returned.  Each time the scheduled query has executed is a run.

    >>> templates = list(api.select(TemplateHistory).where("CBC SDK Demo Template"))
    >>> for template in templates:
    >>>     print(f'template name = {template.name}, id = {template.id}, next run time = {t.next_run_time}')
    >>>     # and then get all the runs for each template
    >>>     runs = list(api.select(Template, template.id).query_runs())
    >>>     for run in runs:
    >>>         print(f'Run id = {run.id}, Run Status = {run.status}, Run create time = {run.create_time}, Results Returned = {run.total_results}, Template Id = {run.template_id}')
    name =  CBC SDK Demo Template   id =  p7qtvxms0oaju46whcrfmyppa9fiqpn9
    Run id = huoobhistdtxxpzhmg52yns7wmsuvjyx, Run Status = ACTIVE, Run create time = 2022-01-19T21:00:00.000Z, Results Returned = 2333, Template Id = p7qtvxms0oaju46whcrfmyppa9fiqpn9
    Run id = bdygnd8jvpjdqjmatdsuqzopaxebquqb, Run Status = TIMED_OUT, Run create time = 2022-01-18T21:00:00.000Z, Results Returned = 2988, Template Id = p7qtvxms0oaju46whcrfmyppa9fiqpn9




