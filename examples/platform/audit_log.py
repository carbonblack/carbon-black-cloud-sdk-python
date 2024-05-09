#!/usr/bin/env python
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

"""Example script which collects audit logs

This script demonstrates how to use Audit Logs in the SDK and the three different APIs.
    * Search
    * Export
    * Queue

    This example has minimal command line parsing in order to reduce complexity and focus on the SDK functions.
    Review the Authentication section of the Read the Docs for information about Authentication in the SDK
    https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/authentication/

    This command line will use "DEMO PROFILE" from the credentials file and poll every 30 seconds for three minutes.
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
    print("You should have a look at and change to a new method.")
    print("Field names have changed from CamelCase to snake_case.")
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

    print("deprecated_get_audit_logs completed")


def get_audit_logs_from_queue(cb, args):
    """Polls for audit logs for the period set on input at the specified interval.

    Uses the queue endpoint.
    """
    print("Starting get_audit_logs_from_queue")
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

    print("get_audit_logs_from_queue completed")


def search_audit_logs(cb):
    """Shows requests for audit logs exercising search criteria. Uses the /_search endpoint."""
    print("Starting search_audit_logs")
    # add_time_criteria can stake a start and end time, or a range
    # add_time_criteria(start="2024-04-23T09:00:00Z", end="2024-04-23T10:40:00Z")
    audit_log_records = cb.select(AuditLog).add_time_criteria(range="-3d").add_boolean_criteria("verbose", True)\
        .add_criteria("description", ["logged in"])
    print("Found {} alert records".format(len(audit_log_records)))

    # Instead of the criteria function, a lucene style query can be used in a where clause for comparable behaviour
    # to the search on the Audit Log page of the Carbon Black Cloud console.
    audit_log_records = cb.select(AuditLog).add_time_criteria(range="-3d").where("description:login")
    print("Found {} alert records".format(len(audit_log_records)))

    for a in audit_log_records:
        print("{}".format(a))

    print("search_audit_logs completed")


def export_audit_logs(cb):
    """Does one request for audit logs exercising search criteria and then exports via the Job Service.

    Uses the /_export endpoint.
    """
    print("Starting export_audit_logs")
    audit_log_query = cb.select(AuditLog).add_time_criteria(range="-1d")
    audit_log_export_job = audit_log_query.export(format="csv")
    results = audit_log_export_job.await_completion().result()
    print(results)
    results = audit_log_export_job.get_output_as_string()
    print(results)

    print("Async Export in json format")
    audit_log_export_job = cb.select(AuditLog).add_time_criteria(range="-1d").export(format="json")
    results = audit_log_export_job.get_output_as_file("/my/home/directory/audit_results.json")
    print("export_audit_logs complete")


def main():
    """Main function for Audit Logs example script.

    This script demonstrates how to use Audit Logs in the SDK and the three different APIs.
        * Search
        * Export
        * Queue

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

    export_audit_logs(cb)
    search_audit_logs(cb)
    get_audit_logs_from_queue(cb, args)
    deprecated_get_audit_logs(cb, args)
    print("The End")


if __name__ == "__main__":
    sys.exit(main())
