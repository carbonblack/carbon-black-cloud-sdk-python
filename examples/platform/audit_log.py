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


def get_audit_logs(cb, args):
    """Polls for audit logs for the period set on input at the specified interval."""
    poll_interval = args.poll_interval
    run_period = args.run_period

    while run_period > 0:
        events_list = AuditLog.get_auditlogs(cb)
        print("Runtime remaining: {0} seconds".format(run_period))
        if len(events_list) == 0:
            print("No audit logs available")
        for event in events_list:
            print(f"Event {event['eventId']}:")
            for (k, v) in event.items():
                print(f"\t{k}: {v}")
        time.sleep(poll_interval)
        run_period = run_period - poll_interval

    print("Run time completed")


def main():
    """Main function for Audit Logs example script."""
    parser = build_cli_parser("Get Audit Logs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get = subparsers.add_parser("get_audit_logs", help="Get available audit logs")

    get.add_argument('-r', '--run_period', type=int, default=180, help="Time in seconds to continue polling for")
    # For production use, a longer poll interval of at least one minute should be used
    get.add_argument('-p', '--poll_interval', type=int, default=30, help="Time in seconds between calling the api")

    args = parser.parse_args()
    cb = get_cb_cloud_object(args)

    if args.command == "get_audit_logs":
        get_audit_logs(cb, args)


if __name__ == "__main__":
    sys.exit(main())
