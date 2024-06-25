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

Exceptions
================================

If an error occurs, the API attempts to roll the error into an appropriate Exception class.

Exception Classes
-----------------

.. autoexception:: cbc_sdk.errors.ApiError
.. autoexception:: cbc_sdk.errors.CredentialError
.. autoexception:: cbc_sdk.errors.ServerError
.. autoexception:: cbc_sdk.errors.ObjectNotFoundError
.. autoexception:: cbc_sdk.errors.MoreThanOneResultError
.. autoexception:: cbc_sdk.errors.InvalidObjectError
.. autoexception:: cbc_sdk.errors.TimeoutError
