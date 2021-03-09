Reputation Override
===================

Using the Carbon Black Cloud SDK, you can manage your ReputationOverrides to create a
list of approved or banned applications using a SHA-256 hash, a certificate signer,
or a path to a known IT tool application

Creating a Reputation Override
------------------------------

Using the ReputationOverride model, you can create new overrides directly provided you
have the necessary required properties. For a SHA256 you need the hash and optionally the filename,
IT_TOOL needs a file path with or without wildcards and optionally an indicator for including the child processes,
CERT needs the signer of the application and optionally the certificate authority.
See `the developer documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-defense/latest/reputation-override-api/#configure-reputation-override>`_
for more details.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import ReputationOverride
    >>> ReputationOverride.create(cb, {
    ...   "description": "An override for a sha256 hash",
    ...   "override_list": "BLACK_LIST",
    ...   "override_type": "SHA256",
    ...   "sha256_hash": "af62e6b3d475879c4234fe7bd8ba67ff6544ce6510131a069aaac75aa92aee7a",
    ...   "filename": "foo.exe"
    ... })
    <cbc_sdk.platform.reputation.ReputationOverride: id 83008db065a611eb9a953907c2e1ed66> @ https://defense.conferdeploy.net
    >>> ReputationOverride.create(cb, {
    ...   "description": "An override for an IT Tool",
    ...   "override_list": "WHITE_LIST",
    ...   "override_type": "IT_TOOL",
    ...   "path": "C://tools//*.exe",
    ...   "include_child_processes": True
    ... })
    <cbc_sdk.platform.reputation.ReputationOverride: id 9e5c7a2f5ef140a989550c2351de1a32> @ https://defense.conferdeploy.net
    >>> ReputationOverride.create(cb, {
    ...   "description": "An override for a CERT",
    ...   "override_list": "WHITE_LIST",
    ...   "override_type": "CERT",
    ...   "signed_by": "VMware Inc.",
    ...   "certificate_authority": "VMware"
    ... })
    <cbc_sdk.platform.reputation.ReputationOverride: id 1768b71d356744498eec5ecd6526ca10> @ https://defense.conferdeploy.net


If you have an ``EnrichedEvent`` or ``Process`` object then you can use either
``ban_process_sha256`` or ``approve_process_sha256`` to add the applications sha256
hash to either the ``WHITE_LIST`` or ``BLACK_LIST``.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import Process
    >>> proc = cb.select(Process, "ABCD1234-00348f83-0000015c-00000000-1d667eb58a2ec94")
    >>> proc.approve_process_sha256("Example approved sha256 from Process")
    <cbc_sdk.platform.reputation.ReputationOverride: id 829e252b65aa11ebb1c7a965f279498c> @ https://defense.conferdeploy.net




Retrieving existing Reputation Overrides
----------------------------------------

Using a query of the ``ReputationOverride`` object, you can see the reputation overrides that
have been created within your organization. If you want to filter the results try including
``set_override_list`` or ``set_override_type`` in your query or include a more restrictive
where claus which can include wildcards such as ``*tools*``.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import ReputationOverride
    >>> overrides = cb.select(ReputationOverride).where("1")
    >>> for override in overrides:
    ...   print(override)
    ...
    -------------------------------------------------------------------------------

             create_time: 2021-02-02T22:32:20.176Z
              created_by: ABCDE12345
             description: An override for an IT Tool
                      id: 83008db065a611eb9a953907c2e1ed66
    include_child_processes: True
           override_list: WHITE_LIST
           override_type: IT_TOOL
                    path: C://tools//*.exe


If you already have an id for a ReputationOverride then you can make a query including
the id as seen below.

::

    >>> override = cb.select(ReputationOverride, 83008db065a611eb9a953907c2e1ed66)
    >>> print(override)
    -------------------------------------------------------------------------------

             create_time: 2021-02-02T22:32:20.176Z
              created_by: ABCDE12345
             description: An override for an IT Tool
                      id: 83008db065a611eb9a953907c2e1ed66
    include_child_processes: True
           override_list: WHITE_LIST
           override_type: IT_TOOL
                    path: C://tools//*.exe


Deleting a Reputation Override
------------------------------

If you no longer need a ``ReputationOverride`` then you can delete the override using ``delete()``
or ``bulk_delete([])`` if you have a few that need deleted at once.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.platform import ReputationOverride
    >>> override = cb.select(ReputationOverride, 83008db065a611eb9a953907c2e1ed66)
    >>> override.delete()
    >>> ReputationOverride.bulk_delete([
    ...   "9e5c7a2f5ef140a989550c2351de1a32",
    ...   "1768b71d356744498eec5ecd6526ca10"
    ... ])
