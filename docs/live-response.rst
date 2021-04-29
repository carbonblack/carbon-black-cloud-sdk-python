Live Response
==============

You can use Live Response with the Carbon Black Cloud Python SDK to:

* Upload, download, or remove files
* Create, retrieve and remove registry entries
* Dump contents of physical memory
* Execute, terminate and list processes

To send commands to an endpoint, first establish a "session" with a device.

Establish A Session With A Device
---------------------------------
Connect to a device by querying the ``Device`` object.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Device
    >>> device = api.select(Device).first()
    >>> lr_session = device.lr_session()

File Commands
-------------

Once a session is established, create a directory and upload a file to that directory.
The ``list directory`` command returns the content of the directory, including the uploaded file.

::

    >>> lr_session.create_directory('C:\\\\demo\\\\')
    >>> lr_session.put_file(open("demo.txt", "r"), 'C:\\\\demo\\\\demo.txt')
    >>> directories = lr_session.list_directory('C:\\\\demo\\\\')
    >>> for directory in directories:
    ...   print(f"{directory['attributes'][0]} {directory['filename']}")
    ...
    DIRECTORY .
    DIRECTORY ..
    ARCHIVE demo.txt

*Note that the creation of the directory will fail if the directory already exists.*

Next, get the contents of the file and then delete the file and the directory.

::

    >>> contents = lr_session.get_file('C:\\\\demo\\\\demo.txt')
    >>> lr_session.delete_file('C:\\\\demo\\\\demo.txt')
    >>> lr_session.delete_file('C:\\\\demo\\\\')

*Note: you can also delete a directory with the delete file command.*

Process Commands
----------------
You can also execute commands to manage processes. Once you have established a session, you can check running processes.

::

    >>> processes = lr_session.list_processes()
    >>> for process in processes:
    ...   print(f"{process['process_pid']} {process['process_path']}")
    ...
    42 c:\windows\explorer.exe
    43 c:\windows\system32\svchost.exe

You can also create or kill a process.

::

    >>> lr_session.create_process(r'cmd.exe /c "ping.exe -t 127.0.0.1"',
                                  wait_for_completion=False, wait_for_output=False)
    >>> processes = lr_session.list_processes()
    >>> for process in processes:
    ...     if 'ping.exe' in process['process_path']:
    ...         lr_session.kill_process(process['process_pid'])

*Note: you must pass the PID of the process to kill it.*

Additional Resources
--------------------

Find a full list of supported commands in the
`Live Response API documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/live-response-api/>`_.

For tips on migrating from Live Response v3 to v6, check the :doc:`migration guide<live-response-v6-migration>`.
