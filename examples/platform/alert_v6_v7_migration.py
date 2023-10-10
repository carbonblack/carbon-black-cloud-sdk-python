#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2023. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
This example shows changes required in Alerts code to move from Carbon Black Cloud Python SDK v1.4.3 to 1.5.0

SDK v1.4.3 and earlier used the Alerts v6 API.  SDK 1.5.0 uses Alerts v7 API which has significantly more metadata
on the Alert record, but also some breaking changes.

It complements the Alert Migration guide available in Read The Docs
https://carbon-black-cloud-python-sdk.readthedocs.io
-->  Guides --> Migration Guides --> Alert Migration

Significant effort was put towards backwards compatibility to minimise the breaking changes in SDK 1.5.0.
The code to support legacy
"""

import sys
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Alert, BaseAlert
from cbc_sdk.errors import FunctionalityDecommissioned

# To see the http requests being made, and the structure of the search requests enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)


def main():
    """For convenience, all running code will be under this main function."""
    # This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
    # Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    # https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/
    api = CBCloudAPI(profile="YOUR PROFILE HERE")

    # The base class has changed from BaseAlert, to simply Alert.
    # Backwards compatibility was built in so this is not a breaking change
    # The default time range that was searched changed from one month to two weeks.

    # If you did this in SDK 1.4.3 it would have got one month of alerts.
    # Because SDK 1.5.0 is implemented only with Alerts v7 API, it returns the new default of the last 2 weeks.
    alerts = api.select(BaseAlert)
    # The search request in the SDK is not made until the results are requested.
    len(alerts)
    # The equivalent search in SDK 1.5.0 is:
    alerts = api.select(Alert).set_time_range(range="-1M")
    len(alerts)
    # Observed Alerts are not returned by the Alerts API v7 and are not available in SDK 1.5.0 onwards.
    # If you are calling the v6 API directly or using SDK 1.4.3 or earlier, use criteria is category=THREAT
    # to get the same alerts as will be returned by the v7 API and SDK 1.5.0.
    try:
        api.select(BaseAlert).set_categories("THREAT")
    except FunctionalityDecommissioned:
        print("The FunctionalityDecommissioned exception is expected.")
        print("In SDK 1.5.0 and Alert v7 API, `category` is not a valid attribute.")
        print("In SDK 1.4.3 and earlier this will limit the alert returned to match those from Alerts v7 API and "
              "SDK 1.5.0 onwards.")

    # get() methods
    # where the field has been renamed, the get_xxx method has been updated to return the value from the field using
    # the new name
    alert_list = api.select(BaseAlert)
    alert = alert_list.first()
    print("Printing the value of remote_ip = {}".format(alert.get("remote_ip")))
    print("Printing the value of netconn_remote_ip, the new name for that data = {}".
          format(alert.get("netconn_remote_ip")))

    # Some fields have been deprecated and do not have an equivalent value in Alerts v7 or SDK 1.5.0.
    # These will raise a FunctionalityDecommissioned exception.
    try:
        alert.get("blocked_threat_category")
    except FunctionalityDecommissioned:
        print("The FunctionalityDecommissioned exception is expected.")
        print("blocked_threat_category is not a valid field")

    # port - there are now two fields, netconn_local_port and netconn_remote_port that replace the legacy `port`.
    # The legacy method set_port in the criteria is translated to a search criteria of netconn_local_port.
    alerts = api.select(BaseAlert).set_ports([1234])
    len(alerts)
    #
    # in SDK 1.5.0, criteria uses a generic add_criteria method instead of hand crafted set_xxx methods.
    # The value can be a single value or a list of values
    # Validation is performed by the API, providing consistency to all callers
    #
    alerts = api.select(Alert).add_criteria('netconn_local_port', 1234)
    len(alerts)
    # or
    alerts = api.select(Alert).add_criteria('netconn_remote_port', [1234])
    len(alerts)

    return 0


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
