Unified Binary Store
====================

The unified binary store (UBS) is a centralized service that is part of the Carbon Black Cloud. The UBS is responsible
for storing all binaries and corresponding metadata for those binaries. The UBS is a feature of Enterprise EDR.

Get Download URL
----------------

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> sha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = Binary(cb, sha256_hash)
    >>> download_url = binary.download_url()
    >>> print(download_url)
    ...
    https://cdc-file-storage-staging-us-east-1.s3.amazonaws.com/80/05/55/7c/16/14/c1/<...truncated...>

*Note: The download link for the binary will be active for 1 hour (default expiration period).*

Get Download URL Valid For Specific Period
------------------------------------------

We could set expiration period for the download link (in seconds).

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> sha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = Binary(cb, sha256_hash)
    >>> download_url = binary.download_url(expiration_seconds=30)
    >>> print(download_url)
    ...
    https://cdc-file-storage-staging-us-east-1.s3.amazonaws.com/80/05/55/7c/16/14/c1/<...truncated...>

*Note: The download link for the binary will be active for 30 seconds.*

Searching Binaries
------------------

Currently searching binaries is not possible, but we could use the following syntax to obtain a single binary.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> cb = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.enterprise_edr.ubs import Binary
    >>> sha256_hash = '8005557c1614c1e2c89f7db3702199de2b1e4605718fa32ff6ffdb2b41ed3759'
    >>> binary = cb.select(Binary, sha256_hash)
    >>> print(download_url)
    ...
    https://cdc-file-storage-staging-us-east-1.s3.amazonaws.com/80/05/55/7c/16/14/c1/<...truncated...>

*Note: If we try to use* :code:`binary = cb.select(Binary)` *, it will fail with exception that the model is a non queryable model.*

Find the full documentation at
`Unified Binary Store <https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/cbc_sdk.enterprise_edr/#module-cbc_sdk.enterprise_edr.ubs>`_.
