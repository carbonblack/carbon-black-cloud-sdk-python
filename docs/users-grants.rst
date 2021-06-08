Users and Grants
================

Using the Carbon Black Cloud SDK, you can work with the users in your organization, as well as their access grants
and profiles.

Uniform Resource Names (URNs)
-----------------------------

The various API functions that work with users and grants often make use of *uniform resource names* (URNs) that
uniquely represent various pieces of the Carbon Black Cloud environment.  These pieces include:

* **Organizations,** represented as ``psc:org:ORGKEY``, where ``ORGKEY`` is the organization's alphanumeric key value.
* **Users,** represented as ``psc:user:ORGKEY:USERID``, where ``ORGKEY`` is the organization's alphanumeric key value
  and ``USERID`` is the user's numeric login ID.
* **Access roles,** represented as ``psc:role:OPT-ORGKEY:NAME``, where ``OPT-ORGKEY`` is (optionally) the alphanumeric
  key value of the organization containing that role, and ``NAME`` is the name of the role.

Most of these are dealt with for you by the Carbon Black Cloud SDK.

Getting a List of Users
-----------------------

We can do a query on the ``User`` object to get a list of users within the organization we're accessing.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> query = api.select(User)
    >>> user_list = list(query)
    >>> for user in user_list:
    ...     print(f"{user.first_name} {user.last_name} (#{user.login_id}) <{user.email}>")
    ...
    Lysa Arryn (#2345670) <larryn@example.com>
    Olenna Redwyne (#2345671) <oredwyne@example.com>
    Arianne Martell (#2345672) <amartell@example.com>
    Jorah Mormont (#2345673) <jmormont@example.com>

We can restrict the query by user IDs or E-mail addresses by using the ``user_ids()`` or ``email_addresses()``
methods on the query object returned by ``select()`` before enumerating its results.

Modifying a User
----------------

A ``User`` can be modified by changing one or more of its fields and then calling its ``save()`` method.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> user = api.select(User, 2345672)
    >>> print(f"{user.first_name} {user.last_name}")
    Arianne Martell
    >>> print(user.phone)
    800-555-0000
    >>> user.phone = '888-555-9753'
    >>> user.save()
    <cbc_sdk.platform.users.User: id 2345672> @ https://defense.conferdeploy.net (*)
    >>> print(user.phone)
    888-555-9753

**Note:** A user's *role* must be changed by modifying its *access grant,* detailed below.

Creating a New User
-------------------

Creating a user may be done with the help of a *builder object,* which is returned from the ``User.create()``
function.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> builder = User.create(api)
    >>> builder.set_first_name('Samwell').set_last_name('Tarly')
    <cbc_sdk.platform.users.User.UserBuilder object at 0x00000209B8123D00>
    >>> builder.set_email('starly@example.com').set_phone('800-555-8008')
    <cbc_sdk.platform.users.User.UserBuilder object at 0x00000209B8123D00>
    >>> builder.set_role('psc:role::BETA_SYSTEM_ADMIN')
    <cbc_sdk.platform.users.User.UserBuilder object at 0x00000209B8123D00>
    >>> builder.build()

Alternately, you may construct a *template object* (a Python ``dict``) that contains the user's information and
create the user directly.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> user_template = {'first_name': 'Selyse', 'last_name': 'Florent', 'email': 'sflorent@example.com',
    ...                  'phone': '877-555-9099', 'role_urn': 'psc:role::BETA_SYSTEM_ADMIN'}
    >>> User.create(api, user_template)

**Note:** A user that has just been created will *not* be visible in either the UI or in a ``User`` query as detailed
above, until the intended user has responded to their invitation E-mail message, activated the account, and set
a password.

User Access Grants
------------------

Every user object has an *access grant* object associated with it, defining the access roles they are permitted to use.
You can use the ``grant()`` method on a ``User`` to get the grant and inspect or modify it.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> user = api.select(User, 2345672)
    >>> print(f"{user.first_name} {user.last_name}")
    Arianne Martell
    >>> grant = user.grant()
    >>> print(grant.roles)
    ['psc:role::BETA_SUPER_ADMIN']
    >>> grant.roles = ['psc:role::BETA_SYSTEM_ADMIN']
    >>> grant.save()
    <cbc_sdk.platform.grants.Grant: id psc:user:1A2B3C4DE:2345672> @ https://defense.conferdeploy.net
    >>> print(grant.roles)
    ['psc:role::BETA_SYSTEM_ADMIN']

You can see what roles you can work with by using the ``get_permitted_role_urns()`` function:

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Grant
    >>> for index, role_urn in enumerate(Grant.get_permitted_role_urns(api)):
    ...     print(f"{index}. {role_urn}")
    ...
    0. psc:role::BETA_LEVEL_3_ANALYST
    1. psc:role::KUBERNETES_SECURITY_DATAPLANE_ONLY
    2. psc:role::ALL_AND_LR
    3. psc:role::BETA_LEVEL_1_ANALYST
    4. psc:role::BETA_SYSTEM_ADMIN
    5. psc:role::KUBERNETES_SECURITY_DATAPLANE
    6. psc:role::VIEW_ONLY
    7. psc:role::ALL
    8. psc:role::KUBERNETES_SECURITY_ADMIN_USER
    9. psc:role::BETA_SUPER_ADMIN
    10. psc:role::KUBERNETES_SECURITY_READ_ONLY_USER
    11. psc:role::CONTAINER_IMAGE_CLI_TOOL
    12. psc:role::KUBERNETES_SECURITY_DEVOPS
    13. psc:role::BETA_VIEW_ALL
    14. psc:role::KUBERNETES_SECURITY_DEVOPS_VIEW_ONLY
    15. psc:role::BETA_LEVEL_2_ANALYST
    16. psc:role::KUBERNETES_SECURITY_DEVELOPER

Some organizations employ *access profiles* on the access grants, which allow roles for a user to be specified for
the organization and/or any child organizations.  Access profiles may be accessed and manipulated through the
access grant object.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import User
    >>> user = api.select(User, 3456789)
    >>> grant = user.grant()
    >>> for profile in grant.profiles_:
    ...     print(f"{profile.allowed_orgs} - {profile.roles}")
    ...
    ['psc:org:1A2B3C4DE'] - ['psc:role::BETA_LEVEL_3_ANALYST']
    ['psc:org:2F3G4H5JK'] - ['psc:role::BETA_LEVEL_1_ANALYST']
