# Running the Example Scripts

To run the example scripts, first set up the CBC SDK with either the `pip install cbc_sdk` or `python setup.py develop`
commands as detailed in the top-level `README.md` file.  You may also set your `PYTHONPATH` environment variable to
point to the `{cbc_sdk}/src` directory, where `{cbc_sdk}` refers to the top-level directory where you have cloned
the CBC SDK repository.

You should also have an API key and have set up a `credentials` file as detailed in the "API Token" section of the
top-level `README.md` file.

Once you have done so, you should be able to run any example script with the command:

		python scriptname.py [arguments]

Executing any script with the `--help` argument should give you a detailed message about the arguments that can
be supplied to the script when it is executed.
