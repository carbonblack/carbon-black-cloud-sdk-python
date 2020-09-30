Installation
================================

If you already have Python installed, skip to `Use Pip`_.

Install Python
--------------

Carbon Black Cloud Python SDK is compatible with Python 3.6+.
UNIX systems usually have Python installed by default; it will
have to be installed on Windows systems separately.

If you believe you have Python installed already, run the following two commands
at a command prompt::

    $ python --version
    Python 3.7.5

    $ pip --version
    pip 20.2.3 from /usr/local/lib/python3.7/site-packages (python 3.7)

If “python --version” reports back a version of 3.6.x or higher, you’re all set.
If “pip” is not found, follow the instructions on this
`guide <https://pip.pypa.io/en/stable/installing/>`_.

If you're on Windows, and Python is not installed yet, download the `latest Python
installer <https://www.python.org/downloads/>`_ from python.org.

.. image:: _static/install-windows.png
   :alt: Windows installation options showing "Add python.exe to path"
   :align: center

Ensure that the "Add Python to PATH" option is checked.

Use Pip
-------

Once Python and Pip are installed, open a command prompt and type::

    $ pip install cbc-sdk

This will download and install the latest version of the SDK from the Python PyPI packaging server.

Virtual Environments (optional)
-------------------------------

If you are installing the SDK with the intent to contribute to it's development,
it is recommended that you use virtual environments to manage multiple installations.

A virtual environment is a Python environment such that the Python interpreter,
libraries and scripts installed into it are isolated from those installed in other
virtual environments, and (by default) any libraries installed in a “system” Python,
i.e., one which is installed as part of your operating system [1]_.

See the python.org `virtual environment guide <https://docs.python.org/3/library/venv.html>`_
for more information.

Get Source Code
---------------

Carbon Black Cloud Python SDK is actively developed on GitHub and the code is available from the
`Carbon Black GitHub repository <https://github.com/carbonblack/cbc-sdk-python>`_.
The version of the SDK on GitHub reflects the latest development version.

To clone the latest version of the SDK repository from GitHub::

    $ git clone https://github.com/carbonblack/cbc-sdk-python.git

Once you have a copy of the source, you can install it in "development" mode into
your Python site-packages::

    $ cd cbc-sdk-python
    $ python setup.py develop

This will link the version of cbc-sdk-python you cloned into your Python site-packages
directory. Any changes you make to the cloned version of the SDK will be reflected
in your local Python installation. This is a good choice if you are thinking of
changing or further developing cbc-sdk-python.


.. [1] https://docs.python.org/3/library/venv.html
