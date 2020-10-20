Running the CBC Python SDK Functional Tests on different platforms
==================================================================
This document will provide information about how to run the functional tests
for the CBC Python SDK in Linux and Windows platforms.

These instructions assume you already have the CBC SDK sources present
locally.  If not, they can be checked out from GitHub using the URL
https://github.com/carbonblack/carbon-black-cloud-sdk-python; doing so will require you to
either have Git installed or download the source tree packed as a zip archive from GitHub 
and then unarchive it


Running the tests on Microsoft Windows
======================================

Install Python
--------------
From http://python.org, download the installer for the most recent Python 3.8 version
(as of this writing, version 3.8.6 is the latest). 

Fix the Execution PATH
----------------------
Go to the Environment Variables dialog (System Control Panel or Properties page
for My Computer/This PC, then select **Advanced system settings** and then the
**Environment Variables** button). Ensure that the first two components of
the user PATH environment variable are *%USERPROFILE%\AppData\Local\Programs\Python\Python38*
and *%USERPROFILE%\AppData\Local\Programs\Python\Python38\Scripts*. 

To test this, open a command window and use the command:
``python --version``
It should run Python and show that you are running Python 3.8.

### Install CBC Python SDK Requirements
From the top-level CBC SDK source directory, execute the following commands:

``pip install -r requirements.txt``

This will ensure that all required python modules are installed.

Execute the Functional Tests
----------------------------
From the top-level CBC SDK source directory, execute the following command:

``pytest``

The tests should return that they all completed successfully.


Running the tests on Linux
==========================
Carbon Black Cloud Python SDK provides a number of Dockerfiles inside the docker folder
of the source root. Those contain the necessary instructions to build docker images
containing a number of distributions with CBC Python SDK preinstalled in /app directory
(relative to image root)

Build the docker image
----------------------
Currently the following Dockerfiles are available:

- docker/amazon/Dockerfile - Amazon Linux (latest) image
- docker/ubuntu/Dockerfile - Ubuntu 18.04 image
- docker/rhel/Dockerfile - RHEL8 UBI image
- docker/suse/Dockerfile - OpenSUSE Leap (latest) image

Building the images should be done from the CBC SDK root directory by explicitly providing
the path to the Dockerfile to be built, e.g for the RHEL one, the build command would be:

``docker build -t cbc-sdk-python=rhel -f docker/rhel/Dockerfile .``

By default, the docker Unix socket is owned by root user / docker group. In case you are running
the build as a non-root user that isn't member of docker group, sudo should be used:

``sudo docker build -t cbc-sdk-python-rhel -f docker/rhel/Dockerfile .``

Run the container and execute the test
--------------------------------------
When the docker image builds, it should be started, e.g:

``docker run -it cbc-sdk-python-rhel``

This will run the container and spawn an interactive shell running in it. CBC Python SDK is installed
in the /app directory, so pytest needs to be executed from there:

``cd /app && pytest``
