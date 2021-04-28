Live Response
==============

With the Carbon Black Cloud SDK, we can use the Live Response functionality to upload, download, and remove files,
retrieve and remove registry entries, dump contents of physical memory, execute and terminate processes.
Before any commands can be sent to an endpoint, we must first establish a “session” with a device.

Establish A Session With A Device
---------------------------------
Using a query of the ``Device`` object, we can choose a device to connect to.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Device
    >>> device = api.select(Device).first()
    >>> lr_session = device.lr_session()

File Commands
-------------

Once a session is established we are going to create a directory and upload a file in that newly created directory.
List directory command is returning the content of the directory including the uploaded file.

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

Note that the creation of the directory will fail if the directory already exists.

Now we will get the contents of the file and then delete the file and the directory.

::

    >>> contents = lr_session.get_file('C:\\\\demo\\\\demo.txt')
    >>> lr_session.delete_file('C:\\\\demo\\\\demo.txt')
    >>> lr_session.delete_file('C:\\\\demo\\\\')

Note that we could delete a directory with the delete file command.

Process Commands
----------------
We can also execute commands to manage processes. Once we have established a session we could check the
running processes, create or kill a process.

::

    >>> processes = lr_session.list_processes()
    >>> for process in processes:
    ...   print(f"{process['process_pid']} {process['process_path']}")
    ...
    42 c:\windows\explorer.exe
    43 c:\windows\system32\svchost.exe

We can create a process and kill it.

::

    >>> lr_session.create_process(r'cmd.exe /c "ping.exe -t 127.0.0.1"',
                                  wait_for_completion=False, wait_for_output=False)
    >>> processes = lr_session.list_processes()
    >>> for process in processes:
    ...     if 'ping.exe' in process['process_path']:
    ...         lr_session.kill_process(process['process_pid'])

Note that we need to pass the pid of the process to kill it.

Additional Resources
--------------------

There are a number other commands supported. For full list and description see
`the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/live-response-api/>`_
for details.

Check the migration guide of Live Response from v3 to v6 :doc:`live-response-v6-migration`
