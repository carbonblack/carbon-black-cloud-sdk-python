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

"""Example script which collects audit logs

The Audit log API provides a read-once queue so no search parameters are requied.
The command line takes the command (get_audit_logs), the total time to run for in seconds and
the polling period, also in seconds.  This command will run for 180 seconds (3 minutes) polling for new audit
logs every 30 seconds.
> python examples/platform/audit_log.py --profile DEMO_PROFILE get_audit_logs -r 180 -p 30
"""

import sys
import time
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import AuditLog

# To see the http requests being made, and the structure of the search requests enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)


def deprecated_get_audit_logs(cb, args):
    """Deprecated: Polls for audit logs for the period set on input at the specified interval.

    Uses the deprecated queue endpoint.  Use AuditLog.get_queued_auditlogs(), shown in get_audit_logs_from_queue
    for equivalent functionality using an updated API signature.
    """
    print("The AuditLog.get_auditlogs() method is deprecated.")
    print("You should have a look at the new example script and change to a new method.")
    poll_interval = args.poll_interval
    run_period = args.run_period

    while run_period > 0:
        audit_log_records = AuditLog.get_auditlogs(cb)
        print("Runtime remaining: {0} seconds".format(run_period))
        if len(audit_log_records) == 0:
            print("No audit logs available")
        for audit_log in audit_log_records:
            print(f"Event {audit_log['eventId']}:")
            for (k, v) in audit_log.items():
                print(f"\t{k}: {v}")
        time.sleep(poll_interval)
        run_period = run_period - poll_interval

    print("Run time completed")


def get_audit_logs_from_queue(cb, args):
    """Polls for audit logs for the period set on input at the specified interval.

    Uses the queue endpoint.
    """
    poll_interval = args.poll_interval
    run_period = args.run_period

    while run_period > 0:
        audit_log_records = AuditLog.get_queued_auditlogs(cb)
        print("Runtime remaining: {0} seconds".format(run_period))
        if len(audit_log_records) == 0:
            print("No audit logs available")
        for audit_log in audit_log_records:
            print("New Event:")
            print("{}".format(audit_log))
        time.sleep(poll_interval)
        run_period = run_period - poll_interval

    print("Run time completed")


def search_audit_logs(cb, args):
    """Does one request for audit logs exercising search criteria. Uses the /_search endpoint."""
    # add_time_criteria can stake a start and end time, or a range
    # add_time_criteria(start="2024-04-23T09:00:00Z", end="2024-04-23T10:40:00Z")
    audit_log_records = cb.select(AuditLog).add_time_criteria(range="-3d").add_boolean_criteria("verbose", True)\
        .add_criteria("description", ["Connector (App)"])
    print("Found {} alert records".format(len(audit_log_records)))

    for a in audit_log_records:
        print("{}".format(a))

    print("End of search results.")


def main():
    """Main function for Audit Logs example script."""
    """This script demonstrates how to use Audit Logs in the SDK and the three different APIs.
        * Search
        * Export
        * Queue

        This example does not use command line parsing in order to reduce complexity and focus on the SDK functions.
        Review the Authentication section of the Read the Docs for information about Authentication in the SDK
        https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

        This is written for clarity of explanation, not perfect coding practices.
        """
    # CBCloudAPI is the connection to the cloud.  It holds the credentials for connectivity.
    # To execute this script, the profile must have an API key with the following permissions.
    # If you are restricted in the actions you're allowed to perform, expect a 403 response for missing permissions.
    # Permissions are set on Settings -> API Access -> Access Level and then assigned to an API Key
    # Audit Logs - org.audits - READ: View and Export Audits
    # Background tasks - Status - jobs.status - READ: To get the status and results of an asynchronous export

    # command line parameters are used for the PROFILE to get connection credentials and polling information.
    parser = build_cli_parser("Get Audit Logs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get = subparsers.add_parser("get", help="Gets audit logs using Queue, Search, Export and Deprecated queue")
    get.add_argument('-r', '--run_period', type=int, default=180, help="Time in seconds to continue polling for")
    # For production use, a longer poll interval of at least one minute should be used
    get.add_argument('-p', '--poll_interval', type=int, default=30, help="Time in seconds between calling the api")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    search_audit_logs(cb, args)
    get_audit_logs_from_queue(cb, args)
    deprecated_get_audit_logs(cb, args)


if __name__ == "__main__":
    sys.exit(main())
