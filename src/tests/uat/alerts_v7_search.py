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

"""Working test script for Alert v7 updates targeted for SDK 1.5.0 release.

Status: working script to user test functionality incrementally during development.
May evolve to something automated and/or easily run manually.
"""

import sys
# from datetime import datetime, timedelta, timezone
from cbc_sdk import CBCloudAPI
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.platform import Alert, BaseAlert, CBAnalyticsAlert, ContainerRuntimeAlert, DeviceControlAlert, \
    WatchlistAlert

SEARCHABLE_FIELDS = {
    # BUG OPEN "alert_notes_present":False ,
    # BUG "remote_is_private" : True ,
    # BUG ON BACKEND - severity does not have effect in criteria "severity" : "3" ,
    # BUG "threat_notes_present" : False ,
    "watchlists_id": "adsfadsfasdf",
    "watchlists_name": "test watchlist",
    "workflow_changed_by_rule_id": "asdfadsfasdf",
    "workflow_changed_by_type": "API",
    "workflow_closure_reason": "RESOLVED",
    "workflow_status": "OPEN"}

SEARCHABLE_ARRAY_FIELDS = {
    "attack_tactic": "",
    "attack_technique": "",
    "blocked_effective_reputation": "TRUSTED_WHITE_LIST",
    "blocked_md5": "",
    "blocked_name": "",
    "blocked_sha256": "",
    "childproc_cmdline": "",
    "childproc_effective_reputation": ["IGNORE", "ADWARE"],
    "childproc_guid": "",
    "childproc_md5": "",
    "childproc_name": "",
    "childproc_sha256": "",
    "childproc_username": "",
    "connection_type": "INTERNAL_INBOUND",
    "determination_changed_by_type": "USER",
    "determination_value": "TRUE_POSITIVE",
    "device_external_ip": "1.2.3.4",
    "device_id": "12345678",
    "device_internal_ip": "1.2.3.4",
    "device_location": "ONSITE",
    "device_name": "",
    "device_os": "WINDOWS",
    "device_os_version": "",
    "device_policy": "default",
    "device_policy_id": "12345",
    "device_target_value": "LOW",
    "device_uem_id": "",
    "device_username": "",
    "egress_group_id": "",
    "egress_group_name": "",
    "external_device_friendly_name": "",
    "id": "",
    "ip_reputation": "78",
    "k8s_cluster": "",
    "k8s_kind": "",
    "k8s_namespace": "",
    "k8s_pod_name": "",
    "k8s_policy": "",
    "k8s_policy_id": "",
    "k8s_rule": "",
    "k8s_rule_id": "",
    "k8s_workload_name": "",
    "ml_classification_final_verdict": "NOT_ANOMALOUS",
    "ml_classification_global_prevalence": "UNKNOWN",
    "ml_classification_org_prevalence": "MEDIUM",
    "netconn_local_ip": "1.2.3.4",
    "netconn_local_ipv4": "1.2.3.4",
    "netconn_local_ipv6": "2001:0000:130F:0000:0000:09C0:876A:130B",
    "netconn_local_port": "123",
    "netconn_protocol": "TCP",
    "netconn_remote_domain": "a.b.c",
    "netconn_remote_ip": "1.2.3.4",
    "netconn_remote_ipv4": "1.2.3.4",
    "netconn_remote_ipv6": "2001:0000:130F:0000:0000:09C0:876A:130B",
    "netconn_remote_port": "432",
    "parent_cmdline": "",
    "parent_effective_reputation": "SUSPECT_MALWARE",
    "parent_guid": "",
    "parent_md5": "",
    "parent_name": "",
    "parent_pid": "123",
    "parent_reputation": "DLP_OBSOLETE",
    "parent_sha256": "",
    "parent_username": "",
    "policy_applied": "APPLIED",
    "primary_event_id": "",
    "process_cmdline": "",
    "process_effective_reputation": "GRAY_OBSOLETE",
    "process_guid": "",
    "process_issuer": "test_val",
    "process_publisher": "test_val",
    "process_md5": "",
    "process_name": "",
    "process_pid": "789",
    "process_reputation": "RESOLVING",
    "process_sha256": "",
    "process_username": "",
    "product_id": "",
    "product_name": "",
    "reason_code": "asdf4532",
    "remote_k8s_kind": "",
    "remote_k8s_namespace": "",
    "remote_k8s_pod_name": "",
    "remote_k8s_workload_name": "",
    "report_id": "",
    "report_link": "",
    "report_name": "",
    "rule_category_id": "",
    "rule_config_category": "",
    "rule_id": "abcd1234",
    "run_state": "DID_NOT_RUN",
    "sensor_action": "ALLOW",
    "serial_number": "",
    "tags": "testtag",
    "threat_id": "",
    "threat_name": "",
    "tms_rule_id": "",
    "ttps": "",
    "type": ["WATCHLIST", "CB_ANALYTICS", "CONTAINER_RUNTIME", "HOST_BASED_FIREWALL", "DEVICE_CONTROL",
             "INTRUSION_DETECTION_SYSTEM", "NETWORK_TRAFFIC_ANALYSIS"],
    "vendor_id": "",
    "vendor_name": "scandisk"}


def search_alert_single_field_criteria(cb, print_detail):
    """get a list of alerts, criteria is single value"""
    for c in SEARCHABLE_FIELDS:
        # alert_list = cb.select(Alert).add_criteria("alert_notes_present", True)
        alert_list = cb.select(Alert).add_criteria(c, SEARCHABLE_FIELDS[c])
        print(len(alert_list))


def search_alert_array_field_criteria(cb, print_detail=False):
    """get a list of alerts, criteria is single value"""
    for c in SEARCHABLE_ARRAY_FIELDS:
        # alert_list = cb.select(Alert).add_criteria("alert_notes_present", True)
        alert_list = cb.select(Alert).add_criteria(c, SEARCHABLE_ARRAY_FIELDS[c])
        print(len(alert_list))


def get_alert_by_id(cb, alert, print_detail):
    """Get a single alert by identifier"""
    alert_list = cb.select(BaseAlert).set_alert_ids([alert.id])
    found_alert = alert_list.first()
    found_alert.refresh()
    print("Search returned {} alerts for alert_id.".format(len(alert_list)))
    if print_detail:
        for a in alert_list:
            print(a)


def main():
    """Main function for Alerts - Demonstrate UAE features script."""

    parser = build_cli_parser("Test Alert Search")
    args = parser.parse_args()
    cb = get_cb_cloud_object(args)
    # search_alert_single_field_criteria(cb, False)
    search_alert_array_field_criteria(cb)
    # cb_container = CBCloudAPI(profile="CONTAINER_RUNTIME")

    return 0


if __name__ == "__main__":
    sys.exit(main())
