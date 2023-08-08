The CBCloudAPI Object
*********************

The ``CBCloudAPI`` object is the key object used in working with the Carbon Black Cloud.  It represents the connection
to the Carbon Black Cloud server, to the specific organization to which you have access.  It is used to search for
objects representing specific data items on the server, such as devices, alerts, policies, and so forth. It also has
a number of utility functions and properties providing access to additional functionality on the server, such as
:ref:`live-response`.

A program using the Carbon Black Cloud SDK will start by creating a ``CBCloudAPI`` object, passing it the parameters
necessary to authenticate to the server. The authentication parameters may be specified as direct arguments when the
object is created, or may be provided by a credential provider (see :ref:`cbc_sdk.credential_providers`). This object
is then called upon for SDK operations, or passed as a parameter to other SDK functions.

As the ``CBCloudAPI`` object relies upon REST calls to the server, it does not hold network connections open, and
hence need not be explicitly closed.

CBCloudAPI Creation Examples
============================

Authenticate to the Carbon Black Cloud server with directly-supplied parameters:

::

    from cbc_sdk import CBCloudAPI
    api = CBCloudAPI(url='https://defense.conferdeploy.net', token='ABCDEFGHIJKLMNOPQRSTUVWX/YZ12345678',
                     org_key='ABCD1234')

    # as an example, get the list of all policies
    from cbc_sdk.platform import Policy
    query = api.select(Policy)
    policy_list = list(query)

Authenticate to the Carbon Black Cloud server using a profile with the default credential provider:

::

    from cbc_sdk import CBCloudAPI
    api = CBCloudAPI(profile='my_profile')

    # as an example, get the list of all policies
    from cbc_sdk.platform import Policy
    query = api.select(Policy)
    policy_list = list(query)

Authenticate to the Carbon Black Cloud server using a profile supplied by a different credential provider:

::

    from cbc_sdk import CBCloudAPI
    from cbc_sdk.credentials import KeychainCredentialProvider
    creds = KeychainCredentialProvider('keychain-to-use', 'my-username')
    api = CBCloudAPI(profile='my_profile', credential_provider=creds)

    # as an example, get the list of all policies
    from cbc_sdk.platform import Policy
    query = api.select(Policy)
    policy_list = list(query)

Class Documentation
===================

.. autoclass:: cbc_sdk.rest_api.CBCloudAPI
   :members:
   :inherited-members:
   :show-inheritance:
