..
    # *******************************************************
    # Copyright (c) Broadcom, Inc. 2020-2024. All Rights Reserved. Carbon Black.
    # SPDX-License-Identifier: MIT
    # *******************************************************
    # *
    # * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
    # * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
    # * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
    # * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
    # * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

.. _live-response:

Live Response
==============

You can use Live Response with the Carbon Black Cloud Python SDK to:

* Upload, download, or remove files
* Create, retrieve and remove registry entries
* Dump contents of physical memory
* Execute, terminate and list processes

Before any commands are sent to the live response session, the proper permissions need to be configured for the Custom Key that is used.
The below table explains what permissions are needed for each of the SDK commands.

+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
|               Command                             | Required Permissions                                   |  Explanation                                         |
+===================================================+========================================================+======================================================+
| | Create LR session for device                    | **CREATE**, **READ** org.liveresponse.session          | CREATE is needed to start the LR session and         |
| | device.lr_session()                             |                                                        | READ is needed to check the status of the command    |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Close session                                   | **READ**, **DELETE** org.liveresponse.session          | DELETE is needed to terminate the LR session and     |
| | lr_session.close()                              |                                                        | READ is needed to check the status of the command    |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Get Raw File                                    | **READ** org.liveresponse.file                         |                                                      |
| | lr_session.get_raw_file(...)                    |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Get File                                        | **READ** org.liveresponse.file                         |                                                      |
| | lr_session.get_file(...)                        |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Upload File                                     | **CREATE**, **READ** org.liveresponse.file             | CREATE is needed to upload the file and READ is      |
| | lr_session.put_file(...)                        |                                                        | needed to check the status of the command            |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Delete file                                     | **READ**, **DELETE** org.liveresponse.file             | DELETE is needed to delete the file and READ is      |
| | lr_session.delete_file(...)                     |                                                        | needed to check the status of the command            |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | List Directory                                  | **READ** org.liveresponse.file                         |                                                      |
| | lr_session.list_directory(...)                  |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Create Directory                                | **CREATE**, **READ** org.liveresponse.file             | CREATE is needed to create the directory and         |
| | lr_session.create_directory(...)                |                                                        | READ is needed to check the status of the command    |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Walk Directory                                  | **READ** org.liveresponse.file                         |                                                      |
| | lr_session.walk(...)                            |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Kill Process                                    | **READ**, **DELETE** org.liveresponse.process          | DELETE is needed to kill the process and READ is     |
| | lr_session.kill_process(...)                    |                                                        | needed to check the status of the command            |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Create Process                                  | | **EXECUTE** org.liveresponse.process                 | If wait_for_completion = False, wait_for_output =    |
| | lr_session.create_process(...)                  | | OR                                                   | False only EXECUTE is needed.                        |
|                                                   | | **EXECUTE** org.liveresponse.process                 | Otherwise also file permissions are needed.          |
|                                                   | | **READ**, **DELETE** org.liveresponse.file           |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | List Processes                                  | **READ** org.liveresponse.process                      |                                                      |
| | lr_session.list_processes(...)                  |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | List Registry Keys and Values                   | **READ** org.liveresponse.registry                     |                                                      |
| | lr_session.list_registry_keys_and_values(...)   |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | List Registry Values                            | **READ** org.liveresponse.registry                     |                                                      |
| | lr_session.list_registry_values(...)            |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Get Registry Value                              | **READ** org.liveresponse.registry                     |                                                      |
| | lr_session.get_registry_value(...)              |                                                        |                                                      |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Set Registry                                    | **READ**, **UPDATE** org.liveresponse.registry         | UPDATE is needed to set/create the value for the     |
| | lr_session.set_registry_value(...)              |                                                        | registry and READ to check the status of the command |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Create Registry Key                             | **CREATE**, **READ** org.liveresponse.registry         | CREATE is needed to create the key and READ to       |
| | lr_session.create_registry_key(...)             |                                                        | check the status of the command.                     |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Delete Registry Key                             | **READ**, **DELETE** org.liveresponse.registry         | DELETE is needed to delete the key and READ to       |
| | lr_session.delete_registry_key(...)             |                                                        | check the status of the command.                     |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Delete Registry Value                           | **READ**, **DELETE** org.liveresponse.registry         | DELETE is needed to delete the value and READ to     |
| | lr_session.delete_registry_value(...)           |                                                        | check the status of the command.                     |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+
| | Memdump                                         | **READ** org.liveresponse.memdump                      | The command to dump the memory includes three        |
| | lr_session.memdump(...)                         | **READ**, **DELETE** org.liveresponse.file             | commands - dumping the memory in a file on the       |
|                                                   |                                                        | remote machine, downloading the file on the local    |
|                                                   |                                                        | machine and deleting the file.                       |
+---------------------------------------------------+--------------------------------------------------------+------------------------------------------------------+

To send commands to an endpoint, first establish a "session" with a device.

.. note::

    As of version 1.3.0, Live Response has been changed to support ``CUSTOM`` type API Keys which enables the platform
    Device model and Live Response session to be used with a single API key. Ensure your API key has the
    ``Device READ`` permission along with the desired Live Response permissions.

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
