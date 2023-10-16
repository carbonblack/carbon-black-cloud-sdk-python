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
from cbc_sdk.platform import Alert, BaseAlert, CBAnalyticsAlert
from cbc_sdk.errors import FunctionalityDecommissioned

# To see the http requests being made, and the structure of the search requests enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)


def base_class_and_default_time_range(api):
    """The base class has changed from BaseAlert, to simply Alert and the default time range searched is now 2 weeks.

    Backwards compatibility was built in so the change of class is not a breaking change.

    The default time range that was searched changed from one month to two weeks in Carbon Black Cloud
    and has not been overridden in the SDK. This is unlikely to affect polling scenarios which are typically searching
    the last period measured in minutes or hours, not weeks.  For one off history searches, the time range is typically
    set explicitly.
    """
    # If you did this in SDK 1.4.3 it would have got one month of alerts.
    # Because SDK 1.5.0 is implemented only with Alerts v7 API, it returns the new default of the last 2 weeks.
    alerts = api.select(BaseAlert)
    # The search request in the SDK is not made until the results are requested.
    len(alerts)
    # The equivalent search in SDK 1.5.0 is:
    alerts = api.select(Alert).set_time_range(range="-1M")
    len(alerts)


def category_monitored_removed(api):
    """Observed Alerts are not returned by the Alerts API v7 and are not available in SDK 1.5.0 onwards.

    If you are calling the v6 API directly or using SDK 1.4.3 or earlier, use criteria ``category=THREAT``
    to get the same alerts as will be returned by the v7 API and SDK 1.5.0.
    """
    try:
        api.select(BaseAlert).set_categories("THREAT")
    except FunctionalityDecommissioned:
        print("The FunctionalityDecommissioned exception is expected.")
        print("In SDK 1.5.0 and Alert v7 API, `category` is not a valid attribute.")
        print("In SDK 1.4.3 and earlier this will limit the alert returned to match those from Alerts v7 API and "
              "SDK 1.5.0 onwards.")


def get_methods_backwards_compatibility(api):
    """get() methods have support for backward compatibiltiy where possible

    Where the field has been renamed, the get_xxx method has been updated to return the value from the field using
    the new name.

    If the field has no equivalent, a ``FunctionalityDecommissioned`` exception is raised.
    """
    alert_list = api.select(BaseAlert)
    alert = alert_list.first()
    # This shows the field known as policy_id in Alert API v6 / SDK 1.4.3 and as device_policy_id in SDK 1.5.0 onwards
    print("Printing the value of policy_id = {}".format(alert.get("policy_id")))
    print("Printing the value of device_policy_id, the new name for that data = {}".
          format(alert.get("device_policy_id")))
    # When accessed using the field name as a property, the same functionality has been built in
    print("Printing the value of alert.policy_id = {}".format(alert.policy_id))
    print("Printing the value of alert.device_policy_id, the new name for that data = {}".
          format(alert.device_policy_id))
    # Some fields have been deprecated and do not have an equivalent value in Alerts v7 or SDK 1.5.0.
    # These will raise a FunctionalityDecommissioned exception.
    # This example uses field ``blocked_threat_category``
    try:
        alert.get("blocked_threat_category")
    except FunctionalityDecommissioned:
        print("The FunctionalityDecommissioned exception is expected.")
        print("blocked_threat_category is not a valid field")


def set_methods_backwards_compatibility(api):
    """set_xxx() methods used to set search criteria have support for backward compatibiltiy where possible

    Where the field has been renamed, the set_xxx method has been updated to return the value from the field using
    the new name.

    If the field has no equivalent, a ``FunctionalityDecommissioned`` exception is raised.
    """
    alert_list = api.select(Alert).set_policy_ids([1234])
    len(alert_list)
    # This shows the field known as policy_id in Alert API v6 / SDK 1.4.3 and as device_policy_id in SDK 1.5.0 onwards
    alert_list = api.select(Alert).add_criteria("device_policy_id", [1234])
    len(alert_list)
    # The set method has been extended to also enable exclusions, i.e. exclude records that match from the result
    alert_list = api.select(Alert).add_criteria("device_policy_id", [1234], True)
    len(alert_list)

    # Some fields have been deprecated and do not have an equivalent value in Alerts v7 or SDK 1.5.0.
    # These will raise a FunctionalityDecommissioned exception.
    # This example uses field ``blocked_threat_category``
    try:
        api.select(Alert).set_blocked_threat_category("UNKNOWN")
    except FunctionalityDecommissioned:
        print("The FunctionalityDecommissioned exception is expected.")
        print("blocked_threat_category is not a valid field")


def ports_split_local_remote(api):
    """Port - the single field ``port`` has been replaced by two fields, netconn_local_port and netconn_remote_port.

    The legacy method set_port in the criteria is translated to a search criteria of netconn_local_port.
    """
    # This statement will search against ``netconn_local_port``.
    alerts = api.select(BaseAlert).set_ports([1234])
    len(alerts)
    #
    # In SDK 1.5.0, criteria uses a generic add_criteria method instead of hand-crafted set_xxx methods.
    # The value can be a single value or a list of values
    # Validation is performed by the API, providing consistency to all callers
    #
    alerts = api.select(Alert).add_criteria('netconn_local_port', 1234)
    len(alerts)
    # or
    alerts = api.select(Alert).add_criteria('netconn_remote_port', [1234])
    len(alerts)


def facet_terms(api):
    """In Alerts v7 and SDK 1.5.0, more fields are available to use as facets and the term matches the field name.

    In Alerts v6 API (and therefore SDK 1.4.3) the terms available for use in a facet were very limited and the
    names did not always match the field name it operated on.
    """
    # This is an example of a field in v6 that is unchanged in v7.  This code snippet will continue to succeed.
    facet_list = api.select(BaseAlert).facets(['POLICY_APPLIED'])
    print(facet_list)
    # This is an example of a field in v6 that was renamed in v7.  This code snippet will raise a
    # ``FunctionalityDecommissioned exception.
    # Use the migration guide to determine which field should be used instead, and also consider if there are new fields
    # that can improve the utility of your integration.
    # Fields that can be used as Facets
    facet_list = api.select(BaseAlert).facets(['ALERT_TYPE'])
    print(facet_list)


def show_to_json(api):
    """The method to_json() has been added as a supported way to get a json representation of the class.

    If you were using the ``_info`` field, this should be replaced with the ``to_json()``
    method.  It defaults to the latest API version (currently v7) and takes a version as an optional parameter.
    """
    alerts = api.select(Alert)
    alert = alerts.first()
    print("This is the default, v7, representation: \n\n{}\n\n".format(alert.to_json()))
    print("This is when the version is specified to v6: \n\n{}\n\n".format(alert.to_json("v6")))


def observation_replaces_enriched_event(api):
    """Enriched Events were removed and replaced by Observations.

    The helper function for Enriched Events has been removed and a FunctionalityDecommissioned exception is raised
    if it is called.

    A new helper function to get Observations has been added.  This can be used on all alert types, whereas
    get_enriched_events was limited to CB_ANALYTICS alerts.
    """
    alerts = api.select(CBAnalyticsAlert)
    alert = alerts.first()
    # do use get_observations()
    alert.get_observations()
    try:
        # do not use get_enriched_events
        alert.get_enriched_events()
    except Exception as e:
        print("Expected exception.  get_enriched_events has been removed")
        print(e)


def main():
    """For convenience, each change has been put in a function.

    Hopefully this makes it easier to understand the bounds of each change and focus on the item you're interested in.

    This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
    Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

    Information about the migration from Alerts v6 API to Alerts v7 API which shows the mapping from v6 field names
    to v7 field names, and new fields that were introduced is on the Developer Network.
    https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/

    Alert v7 API specification:
    https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/

    Search Fields - Alerts, including which alert types each field is available on and whether they can be
    used in criteria or facet terms.
    https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alert-search-fields/
    """
    # api = CBCloudAPI(profile="YOUR PROFILE HERE")
    api = CBCloudAPI(profile="TECH_AL")

    base_class_and_default_time_range(api)
    set_methods_backwards_compatibility(api)
    get_methods_backwards_compatibility(api)
    show_to_json(api)
    observation_replaces_enriched_event(api)
    category_monitored_removed(api)
    # facet_terms(api)
    ports_split_local_remote(api)


if __name__ == "__main__":
    # Trap keyboard interrupts while running the script.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt\n")
        sys.exit(0)
