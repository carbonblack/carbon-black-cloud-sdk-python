Unified Binary Store
====================

The unified binary store (UBS) is a centralized service that is part of the Carbon Black Cloud. The UBS is responsible
for storing all binaries and corresponding metadata for those binaries. The UBS comes packaged in with Enterprise EDR.

Get Download URL
----------------

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> ha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = Binary(cb, ha256_hash)
    >>> download_url = binary.download_url()

*Note: This is going to generate download link for the binary that will be active for 1 hour (default expiration period).*

Get Download URL Valid For Specific Period
------------------------------------------

We could set expiration period for the download link (in seconds).

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> ha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = Binary(cb, ha256_hash)
    >>> download_url = binary.download_url(expiration_seconds=30)

*Note: This is going to generate download link for the binary that will be active for 30 seconds.*

Querying Binaries
-----------------

Currently querying binaries is not possible, but we could use the following syntax to obtain a single binary.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> ha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = cb.select(Binary, ha256_hash)

*Note: If we try to use* :code:`binary = cb.select(Binary)` *, it will fail with exception that the model is non queryable model.* 

Find a full list of supported commands in the
`Unified Binary Store <https://developer.carbonblack.com/reference/carbon-black-cloud/cb-threathunter/latest/universal-binary-store-api/>`_.

