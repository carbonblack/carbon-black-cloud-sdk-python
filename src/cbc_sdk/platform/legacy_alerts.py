#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Legacy Alerts and Workflows used Alert API v6 and SDK 1.4.3 or earlier"""

from cbc_sdk.errors import ApiError, FunctionalityDecommissioned
from cbc_sdk.platform.devices import DeviceSearchQuery
from cbc_sdk.base import CriteriaBuilderSupportMixin
import logging

log = logging.getLogger(__name__)

ALERT_VALID_REPUTATIONS = [
    "ADAPTIVE_WHITE_LIST",
    "COMMON_WHITE_LIST",
    "COMPANY_BLACK_LIST",
    "COMPANY_WHITE_LIST",
    "PUP",
    "TRUSTED_WHITE_LIST",
    "RESOLVING",
    "COMPROMISED_OBSOLETE",
    "DLP_OBSOLETE",
    "IGNORE",
    "ADWARE",
    "HEURISTIC",
    "SUSPECT_MALWARE",
    "KNOWN_MALWARE",
    "ADMIN_RESTRICT_OBSOLETE",
    "NOT_LISTED",
    "GRAY_OBSOLETE",
    "NOT_COMPANY_WHITE_OBSOLETE",
    "LOCAL_WHITE",
    "NOT_SUPPORTED"
]
ALERT_VALID_ALERT_TYPES = ["CB_ANALYTICS", "DEVICE_CONTROL", "WATCHLIST", "CONTAINER_RUNTIME"]
ALERT_VALID_WORKFLOW_VALS = ["OPEN", "DISMISSED"]
ALERT_VALID_FACET_FIELDS = ["ALERT_TYPE", "CATEGORY", "REPUTATION", "WORKFLOW", "TAG", "POLICY_ID",
                            "POLICY_NAME", "DEVICE_ID", "DEVICE_NAME", "APPLICATION_HASH",
                            "APPLICATION_NAME", "STATUS", "RUN_STATE", "POLICY_APPLIED_STATE",
                            "POLICY_APPLIED", "SENSOR_ACTION"]
CB_ANALYTICS_VALID_LOCATIONS = ["ONSITE", "OFFSITE", "UNKNOWN"]
CB_ANALYTICS_VALID_POLICY_APPLIED = ["APPLIED", "NOT_APPLIED"]
CB_ANALYTICS_VALID_RUN_STATES = ["DID_NOT_RUN", "RAN", "UNKNOWN"]
CB_ANALYTICS_VALID_SENSOR_ACTIONS = ["POLICY_NOT_APPLIED", "ALLOW", "ALLOW_AND_LOG", "TERMINATE", "DENY"]


class LegacyAlertSearchQueryCriterionMixin(CriteriaBuilderSupportMixin):
    """Represents a legacy alert, based on Alert API v6 or SDK 1.4.3 or earlier."""

    def set_categories(self, categories):
        """
        The field `categories` was deprecated and not included in v7.  This method has been removed.

        In Alerts v7, only records with the type THREAT are returned.
        Records that in v6 had the category MONITORED (Observed) are now Observations
        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
            categories (list): List of categories to be restricted to.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_categories method does not exist in in SDK v1.5.0 "
                                          "because category is not a valid field on Alert v7 API.  The")

    def set_create_time(self, *args, **kwargs):
        """
        Restricts the alerts that this query is performed on to the specified creation time.

        The time may either be specified as a start and end point or as a range.
        In SDK 1.5.0 to align with Alerts v7 API, create_time is set as time_range outside of criteria.

        Deprecated:
            Use `add_time_criteria(field_name, start, end, range)` instead.

        Args:
            *args (list): Not used.
            **kwargs (dict): Used to specify start= for start time, end= for end time, and range= for range.

        Returns:
            AlertSearchQuery: This instance.
        """
        if kwargs.get("start", None) and kwargs.get("end", None):
            if kwargs.get("range", None):
                raise ApiError("cannot specify range= in addition to start= and end=")
            stime = kwargs["start"]
            if not isinstance(stime, str):
                stime = stime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            etime = kwargs["end"]
            if not isinstance(etime, str):
                etime = etime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            self.set_time_range(start=stime, end=etime)
        elif kwargs.get("range", None):
            if kwargs.get("start", None) or kwargs.get("end", None):
                raise ApiError("cannot specify start= or end= in addition to range=")
            self.set_time_range(range=kwargs["range"])
        else:
            raise ApiError("must specify either start= and end= or range=")
        return self

    def set_device_ids(self, device_ids):
        """
        Restricts the alerts that this query is performed on to the specified device IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            device_ids (list): List of integer device IDs.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(device_id, int) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device_id", device_ids)
        return self

    def set_device_names(self, device_names):
        """
        Restricts the alerts that this query is performed on to the specified device names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            device_names (list): List of string device names.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in device_names):
            raise ApiError("One or more invalid device names")
        self._update_criteria("device_name", device_names)
        return self

    def set_device_os(self, device_os):
        """
        Restricts the alerts that this query is performed on to the specified device operating systems.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            device_os (list): List of string operating systems.  Valid values are "WINDOWS", "ANDROID",
                              "MAC", "IOS", "LINUX", and "OTHER."

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all((osval in DeviceSearchQuery.VALID_OS) for osval in device_os):
            raise ApiError("One or more invalid operating systems")
        self._update_criteria("device_os", device_os)
        return self

    def set_device_os_versions(self, device_os_versions):
        """
        Restricts the alerts that this query is performed on to the specified device operating system versions.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            device_os_versions (list): List of string operating system versions.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in device_os_versions):
            raise ApiError("One or more invalid device OS versions")
        self._update_criteria("device_os_version", device_os_versions)
        return self

    def set_device_username(self, users):
        """
        Restricts the alerts that this query is performed on to the specified user names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            users (list): List of string user names.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(u, str) for u in users):
            raise ApiError("One or more invalid user names")
        self._update_criteria("device_username", users)
        return self

    def set_group_results(self, do_group):
        """
        The field `group_results` was deprecated and not included in v7.  This method has been removed.

        It previously specified whether to group the results of the query.
        Use the `Grouped Alerts Operations
        <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/alerts-api/>`_
        #grouped-alerts-operations) instead.
        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
            do_group (bool): True to group the results, False to not do so.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_group_results method does not exist in in SDK v1.5.0 "
                                          "because group_result is not a valid field on Alert v7 API.  The")

    def set_alert_ids(self, alert_ids):
        """
        Restricts the alerts that this query is performed on to the specified alert IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            alert_ids (list): List of string alert IDs.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(v, str) for v in alert_ids):
            raise ApiError("One or more invalid alert ID values")
        self._update_criteria("id", alert_ids)
        return self

    def set_legacy_alert_ids(self, alert_ids):
        """
        Restricts the alerts that this query is performed on to the specified legacy alert IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            alert_ids (list): List of string legacy alert IDs.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(v, str) for v in alert_ids):
            raise ApiError("One or more invalid alert ID values")
        self._update_criteria("id", alert_ids)
        return self

    def set_policy_ids(self, policy_ids):
        """
        Restricts the alerts that this query is performed on to the specified policy IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            policy_ids (list): List of integer policy IDs.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(policy_id, int) for policy_id in policy_ids):
            raise ApiError("One or more invalid policy IDs")
        self._update_criteria("device_policy_id", policy_ids)
        return self

    def set_policy_names(self, policy_names):
        """
        Restricts the alerts that this query is performed on to the specified policy names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            policy_names (list): List of string policy names.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in policy_names):
            raise ApiError("One or more invalid policy names")
        self._update_criteria("device_policy", policy_names)
        return self

    def set_process_names(self, process_names):
        """
        Restricts the alerts that this query is performed on to the specified process names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            process_names (list): List of string process names.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in process_names):
            raise ApiError("One or more invalid process names")
        self._update_criteria("process_name", process_names)
        return self

    def set_process_sha256(self, shas):
        """
        Restricts the alerts that this query is performed on to the specified process SHA-256 hash values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            shas (list): List of string process SHA-256 hash values.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in shas):
            raise ApiError("One or more invalid SHA256 values")
        self._update_criteria("process_sha256", shas)
        return self

    def set_reputations(self, reps):
        """
        Restricts the alerts that this query is performed on to the specified reputation values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            reps (list): List of string reputation values.  Valid values are "KNOWN_MALWARE", "SUSPECT_MALWARE",
                         "PUP", "NOT_LISTED", "ADAPTIVE_WHITE_LIST", "COMMON_WHITE_LIST", "TRUSTED_WHITE_LIST",
                         and "COMPANY_BLACK_LIST".

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all((r in ALERT_VALID_REPUTATIONS) for r in reps):
            log.warning("Reputation value not in enumeration. May be valid as enumeration values are extended in "
                        "Carbon Black Cloud ahead of SDK updates.")
        self._update_criteria("process_reputation", reps)
        return self

    def set_tags(self, tags):
        """
        Restricts the alerts that this query is performed on to the specified tag values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            tags (list): List of string tag values.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(tag, str) for tag in tags):
            raise ApiError("One or more invalid tags")
        self._update_criteria("tags", tags)
        return self

    def set_target_priorities(self, priorities):
        """
        Restricts the alerts that this query is performed on to the specified target priority values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            priorities (list): List of string target priority values.  Valid values are "LOW", "MEDIUM",
                               "HIGH", and "MISSION_CRITICAL".

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all((prio in DeviceSearchQuery.VALID_PRIORITIES) for prio in priorities):
            raise ApiError("One or more invalid priority values")
        self._update_criteria("device_target_value", priorities)
        return self

    def set_threat_ids(self, threats):
        """
        Restricts the alerts that this query is performed on to the specified threat ID values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            threats (list): List of string threat ID values.

        Returns:
            AlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in threats):
            raise ApiError("One or more invalid threat ID values")
        self._update_criteria("threat_id", threats)
        return self

    def set_types(self, alerttypes):
        """
        Restricts the alerts that this query is performed on to the specified alert type values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            alerttypes (list): List of string alert type values.  Valid values are "CB_ANALYTICS",
                               "WATCHLIST", "DEVICE_CONTROL", and "CONTAINER_RUNTIME".  In SDK 1.5.0,
                               to align with Alert API v7, more alert types are available but the `add_criteria`
                               method must be used.

        Returns:
            AlertSearchQuery: This instance.

        Note: - When filtering by fields that take a list parameter, an empty list will be treated as a wildcard and
        match everything.
        """
        if not all((t in ALERT_VALID_ALERT_TYPES) for t in alerttypes):
            raise ApiError("One or more invalid alert type values")
        self._update_criteria("type", alerttypes)
        return self

    def set_workflows(self, workflow_vals):
        """
        Restricts the alerts that this query is performed on to the specified workflow status values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            workflow_vals (list): List of string alert type values.  Valid values are "OPEN" and "DISMISSED".

        Returns:
            AlertSearchQuery: This instance.
        """
        new_vals = []
        for val in workflow_vals:
            if val not in ALERT_VALID_WORKFLOW_VALS:
                raise ApiError("One or more invalid workflow status values")
            elif val == "DISMISSED":
                new_vals.append("CLOSED")
            else:
                new_vals.append(val)

        self._update_criteria("workflow", new_vals)
        return self

    def set_cluster_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes cluster names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of Kubernetes cluster names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid cluster name values")
        self._update_criteria("k8s_cluster", names)
        return self

    def set_namespaces(self, namespaces):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes namespaces.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            namespaces (list): List of Kubernetes namespaces to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in namespaces):
            raise ApiError("One or more invalid namespace values")
        self._update_criteria("k8s_namespace", namespaces)
        return self

    def set_workload_kinds(self, kinds):
        """
        Restricts the alerts that this query is performed on to the specified workload types.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            kinds (list): List of workload types to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in kinds):
            raise ApiError("One or more invalid workload kind values")
        self._update_criteria("k8s_kind", kinds)
        return self

    def set_workload_ids(self, ids):
        """
        The field `workload_id` was deprecated and not included in v7.  This method has been removed.

        Use workload_name instead. See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
            ids (list): List of workload IDs to look for.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned(
            "Starting with SDK v1.5.0 workload_id is not a valid field on Alert.")

    def set_workload_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified workload names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of workload names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid workload name values")
        self._update_criteria("k8s_workload_name", names)
        return self

    def set_replica_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified pod names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of pod names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid replica ID values")
        self._update_criteria("k8s_pod_name", ids)
        return self

    def set_remote_ips(self, addrs):
        """
        Restricts the alerts that this query is performed on to the specified remote IP addresses.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            addrs (list): List of remote IP addresses to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in addrs):
            raise ApiError("One or more invalid remote IP values")
        self._update_criteria("netconn_remote_ip", addrs)
        return self

    def set_remote_domains(self, domains):
        """
        Restricts the alerts that this query is performed on to the specified remote domains.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            domains (list): List of remote domains to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in domains):
            raise ApiError("One or more invalid remote domain values")
        self._update_criteria("netconn_remote_domain", domains)
        return self

    def set_protocols(self, protocols):
        """
        Restricts the alerts that this query is performed on to the specified protocols.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            protocols (list): List of protocols to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in protocols):
            raise ApiError("One or more invalid protocol values")
        self._update_criteria("netconn_protocol", protocols)
        return self

    def set_ports(self, ports):
        """
        Restricts the alerts that this query is performed on to the specified netconn_local_ports.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Note that in SDK 1.5.0, to align with Alerts API v7, the search field was updated from
        `port` to `netconn_local_port`.  It is possible to search on either `netconn_local_port`
        or `netconn_remote_port` using the `add_criteria(fieldname, [field values]) method.

        Args:
            ports (list): List of netconn_local_ports to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, int) for n in ports):
            raise ApiError("One or more invalid port values")
        self._update_criteria("netconn_local_port", ports)
        return self

    def set_egress_group_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified egress group IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of egress group IDs to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid egress group ID values")
        self._update_criteria("egress_group_id", ids)
        return self

    def set_egress_group_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified egress group names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of egress group names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid egress group name values")
        self._update_criteria("egress_group_name", names)
        return self

    def set_ip_reputations(self, reputations):
        """
        Restricts the alerts that this query is performed on to the specified IP reputation values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            reputations (list): List of IP reputation values to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, int) for n in reputations):
            raise ApiError("One or more invalid IP reputation values")
        self._update_criteria("ip_reputation", reputations)
        return self

    def set_rule_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes policy rule IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        In SDK prior to 1.5.0 this was only supported for Container Runtime Alerts so will
        convert to k8s_rule_id in criteria.  In SDK 1.5.0 and later, aligned to Alert v7 API, use add_criteria()
        should be used for both k8s_rule_id and for other alert types, rule_id.

        Args:
            ids (list): List of Kubernetes policy rule IDs to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid rule ID values")
        self._update_criteria("k8s_rule_id", ids)
        return self

    def set_rule_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified Kubernetes policy rule names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of Kubernetes policy rule names to look for.

        Returns:
            ContainerRuntimeAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid rule name values")
        self._update_criteria("k8s_rule", names)
        return self

    def set_watchlist_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified watchlist ID values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of string watchlist ID values.

        Returns:
            WatchlistAlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in ids):
            raise ApiError("One or more invalid watchlist IDs")
        self._update_criteria("watchlist_id", ids)
        return self

    def set_watchlist_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified watchlist name values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of string watchlist name values.

        Returns:
            WatchlistAlertSearchQuery: This instance.
        """
        if not all(isinstance(name, str) for name in names):
            raise ApiError("One or more invalid watchlist names")
        self._update_criteria("watchlist_name", names)
        return self

    def set_blocked_threat_categories(self, categories):
        """
        The field `blocked_threat_category` was deprecated and not included in v7.  This method has been removed.

        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
        categories (list): List of threat categories to look for.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_blocked_threat_categories method does not exist in in SDK v1.5.0 "
                                          "because blocked_threat_category is not a valid field on Alert v7 API.  The")

    def set_device_locations(self, locations):
        """
        Restricts the alerts that this query is performed on to the specified device locations.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            locations (list): List of device locations to look for. Valid values are "ONSITE", "OFFSITE",
                              and "UNKNOWN".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((location in CB_ANALYTICS_VALID_LOCATIONS)
                   for location in locations):
            raise ApiError("One or more invalid device locations")
        self._update_criteria("device_location", locations)
        return self

    def set_kill_chain_statuses(self, statuses):
        """
        The field `kill_chain_status` was deprecated and not included in v7.  This method has been removed.

        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
        statuses (list): List of kill chain statuses to look for.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_kill_chain_statuses method does not exist in in SDK v1.5.0 because "
                                          "kill_chain_status is not a valid field on Alert v7 API.  The")

    def set_not_blocked_threat_categories(self, categories):
        """
        The field `not_blocked_threat_category` was deprecated and not included in v7.  This method has been removed.

        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
        categories (list): List of threat categories to look for.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_not_blocked_threat_categories method does not exist in in SDK v1.5.0 "
                                          "because not_blocked_threat_category is not a valid field on Alert v7 API."
                                          " The")

    def set_policy_applied(self, applied_statuses):
        """
        Restricts the alerts that this query is performed on to the specified policy status values.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            applied_statuses (list): List of status values to look for. Valid values are "APPLIED" and "NOT_APPLIED".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((s in CB_ANALYTICS_VALID_POLICY_APPLIED)
                   for s in applied_statuses):
            raise ApiError("One or more invalid policy-applied values")
        self._update_criteria("policy_applied", applied_statuses)
        return self

    def set_reason_code(self, reason):
        """
        Restricts the alerts that this query is performed on to the specified reason codes (enum values).

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            reason (list): List of string reason codes to look for.

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all(isinstance(t, str) for t in reason):
            raise ApiError("One or more invalid reason code values")
        self._update_criteria("reason_code", reason)
        return self

    def set_run_states(self, states):
        """
        Restricts the alerts that this query is performed on to the specified run states.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            states (list): List of run states to look for. Valid values are "DID_NOT_RUN", "RAN", and "UNKNOWN".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((s in CB_ANALYTICS_VALID_RUN_STATES)
                   for s in states):
            raise ApiError("One or more invalid run states")
        self._update_criteria("run_state", states)
        return self

    def set_sensor_actions(self, actions):
        """
        Restricts the alerts that this query is performed on to the specified sensor actions.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            actions (list): List of sensor actions to look for. Valid values are "POLICY_NOT_APPLIED", "ALLOW",
                            "ALLOW_AND_LOG", "TERMINATE", and "DENY".

        Returns:
            CBAnalyticsAlertSearchQuery: This instance.
        """
        if not all((action in CB_ANALYTICS_VALID_SENSOR_ACTIONS)
                   for action in actions):
            raise ApiError("One or more invalid sensor actions")
        self._update_criteria("sensor_action", actions)
        return self

    def set_threat_cause_vectors(self, vectors):
        """
        The field `threat_cause_vector` was deprecated and not included in v7.  This method has been removed.

        See `Developer Network Alerts v6 Migration
        <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/alerts-migration/>`_
        for more details.

        Args:
            vectors (list): List of threat cause vectors to look for.

        Raises:
            FunctionalityDecommissioned: If the requested attribute is no longer available.
        """
        raise FunctionalityDecommissioned("set_threat_cause_vectors method does not exist in in SDK v1.5.0 "
                                          "because threat_cause_vector is not a valid field on Alert v7 API.  The")

    def set_external_device_friendly_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified external device friendly names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of external device friendly names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid device name values")
        self._update_criteria("external_device_friendly_name", names)
        return self

    def set_external_device_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified external device IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of external device IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid device ID values")
        self._update_criteria("device_id", ids)
        return self

    def set_product_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified product IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of product IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid product ID values")
        self._update_criteria("product_id", ids)
        return self

    def set_product_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified product names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of product names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid product name values")
        self._update_criteria("product_name", names)
        return self

    def set_serial_numbers(self, serial_numbers):
        """
        Restricts the alerts that this query is performed on to the specified serial numbers.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            serial_numbers (list): List of serial numbers to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in serial_numbers):
            raise ApiError("One or more invalid serial number values")
        self._update_criteria("serial_number", serial_numbers)
        return self

    def set_vendor_ids(self, ids):
        """
        Restricts the alerts that this query is performed on to the specified vendor IDs.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            ids (list): List of vendor IDs to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in ids):
            raise ApiError("One or more invalid vendor ID values")
        self._update_criteria("vendor_id", ids)
        return self

    def set_vendor_names(self, names):
        """
        Restricts the alerts that this query is performed on to the specified vendor names.

        Deprecated:
            Use `add_criteria(field_name, [field_value])` instead.

        Args:
            names (list): List of vendor names to look for.

        Returns:
            DeviceControlAlertSearchQuery: This instance.
        """
        if not all(isinstance(n, str) for n in names):
            raise ApiError("One or more invalid vendor name values")
        self._update_criteria("vendor_name", names)
        return self
