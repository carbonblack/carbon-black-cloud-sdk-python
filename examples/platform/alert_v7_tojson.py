"""Example for alert v7 features. Very work in progress."""
import sys
import json
from cbc_sdk.helpers import (build_cli_parser)
# , get_cb_cloud_object)
from cbc_sdk.platform import BaseAlert


def alert_to_json_file_v6(cb, path, alert_id):
    """Run with SDK 1.4.3 or earlier to generate original v6 alert json from _info"""
    """THIS IS A MOCK"""
    alert = cb.select(BaseAlert, alert_id)
    filename = "{0}v6_alert-{1}-{2}.json".format(path, alert.type, alert_id)
    json.dump(alert._info, open(filename, "w"), indent=4)
    return filename


def alert_to_json_file_v6_by_v7(cb, path, alert_id):
    """Run with 1.5.0 (or wip for) to generate a v6 compatible output from the v7 request"""
    alert = cb.select(BaseAlert, alert_id)
    filename = "{0}v6_by_v7_alert-{1}-{2}.json".format(path, alert.type, alert_id)
    json.dump(alert.to_json("v6"), open(filename, "w"), indent=4)
    return filename


def alert_to_json_file_v7(cb, path, alert_id):
    """Run with 1.5.0 (or wip for) to generate a v7 output"""
    alert = cb.select(BaseAlert, alert_id)
    filename = "{0}v7_alert-{1}-{2}.json".format(path, alert.type, alert_id)
    json.dump(alert.to_json(), open(filename, "w"), indent=4)
    return filename


def alert_json_compare(path, v6_file, v6_by_v7_file, v7_file):
    """
    Compare the v6_file to v6_by_v7_file.

    v7_file is just provided for debugging to determine if the field is missing in the base v7 and therefore unable to
    be mapped as distinct from exists and was not mapped.
    """
    alert_v6 = json.load(open(path + v6_file))
    alert_v6_from_v7 = json.load(open(path + v6_by_v7_file))
    # v7 isn't used, only for troubleshooting
    # alert_v7 = json.load(open(path+v7_file))
    if alert_v6 == alert_v6_from_v7:
        print("Same")
    else:
        print("Not the same - checking one field at a time")
        for f in alert_v6:
            # for testing / debugging
            # if f == "threat_indicators":
            #    print("stop here")
            # fields from base alert that are not in v7. No mapping available
            if f == "group_details" or f == "category" or f == "threat_activity_c2":
                if f in alert_v6_from_v7:
                    print("ERROR: Field does not exist in v7 base alert and should be missing: {}".format(f))
                # else:
                    # do nothing
                    # print("Field does not exist in v7 and correctly missing: {}".format(f))

            # fields from cb analytics that are not in v7. No mapping available
            elif (f == "blocked_threat_category" or f == "kill_chain_status" or f == "not_blocked_threat_category"
                  or f == "threat_activity_c2" or f == "threat_activity_dlp" or f == "threat_activity_phish"
                  or f == "threat_cause_vector"):
                if f in alert_v6_from_v7:
                    print("ERROR: Field does not exist in v7 cb analytics alert and should be missing: {}".format(f))
                # else:
                    # do nothing
                    # print("Field does not exist in v7 and correctly missing: {}".format(f))

            # none for container runtime alerts
            # none for host based firewall alerts
            # fields from device control that are not in v7. No mapping available
            elif f == "threat_cause_vector":
                if f in alert_v6_from_v7:
                    print(
                        "ERROR: Field does not exist in v7 device control alert and should be missing: {}".format(f))
                # else:
                # do nothing
                # print("Field does not exist in v7 and correctly missing: {}".format(f))

            # fields from watchlist alert that are not in v7. No mapping available
            elif (f == "count" or f == "document_guid" or f == "threat_cause_vector"
                  or (f == "threat_indicators" and alert_v6["type"] == "WATCHLIST")):
                if f in alert_v6_from_v7:
                    print(
                        "ERROR: Field does not exist in v7 watchlist alert and should be missing: {}".format(f))
                # else:
                # do nothing
                # print("Field does not exist in v7 and correctly missing: {}".format(f))

            elif f in alert_v6_from_v7:
                if alert_v6_from_v7[f] != alert_v6[f]:
                    if isinstance(alert_v6[f], dict) or isinstance(alert_v6_from_v7[f], dict):
                        v6_inner = alert_v6[f]
                        v6_from_v7_inner = alert_v6_from_v7[f]
                        for i in v6_inner:
                            if (v6_inner[i] is not None
                                    and (i not in v6_from_v7_inner or v6_inner[i] != v6_from_v7_inner[i])):
                                print("inner value not matched for field {}".format(i))
                del alert_v6_from_v7[f]
            elif alert_v6[f] is None:
                pass
            else:
                print("{} was not found".format(f))


def main():
    """Main function for Policy - Host-Based Firewall script."""
    parser = build_cli_parser("View or set host based firewall rules on a policy")
    parser.add_argument("--alert_id", help="id of alert to get")
    # args = parser.parse_args()

    path = "/Users/kebringer/kylie_code/carbon-black-cloud-sdk-python/test_out/"
    # cb = get_cb_cloud_object(args)

    # alert id's for each type
    # cb_analytics_alert_id = "6f1173f5-f921-8e11-2160-edf42b799333" # TECH_AL
    # container_runtime_alert_id = "46b419c8-3d67-ead8-dbf1-9d8417610fac"
    # org_key = VZMTPVJZR2, profile CONTAINER_RUNTIME
    # watchlist_alert_id = "f6af290d-6a7f-461c-a8af-cf0d24311105"
    # hbfw_alert_id = "2be0652f-20bc-3311-9ded-8b873e28d830" #org_key LXETKY4QQV, profile HBFW_TEST
    # device_control_alert_id = "b6a7e48b-1d14-11ee-a9e0-888888888788"

    # Command lines to generate the files
    # python3 examples/platform/alert_v7_tojson.py --profile TECH_AL --alert_id 6f1173f5-f921-8e11-2160-edf42b799333
    # python3 examples/platform/alert_v7_tojson.py --profile
    # CONTAINER_RUNTIME --alert_id 46b419c8-3d67-ead8-dbf1-9d8417610fac
    # python3 examples/platform/alert_v7_tojson.py --profile TECH_AL --alert_id f6af290d-6a7f-461c-a8af-cf0d24311105
    # python3 examples/platform/alert_v7_tojson.py --profile HBFW_TEST --alert_id 2be0652f-20bc-3311-9ded-8b873e28d830
    # python3 examples/platform/alert_v7_tojson.py --profile TECH_AL --alert_id b6a7e48b-1d14-11ee-a9e0-888888888788

    # Execute each of the following calls with an alert_id to generate the files for comparison
    # alert_to_json_file_v6(cb, path, args.alert_id)
    # alert_to_json_file_v6_by_v7(cb, path, args.alert_id)
    # alert_to_json_file_v7(cb, path, args.alert_id)

    # CB Analytics
    print("CB Analytics Alert Comparison")
    alert_json_compare(path, "v6_alert-CB_ANALYTICS-6f1173f5-f921-8e11-2160-edf42b799333.json",
                       "v6_by_v7_alert-CB_ANALYTICS-6f1173f5-f921-8e11-2160-edf42b799333.json",
                       "v7_alert-CB_ANALYTICS-6f1173f5-f921-8e11-2160-edf42b799333.json")
    # Watchlist
    print("")
    print("Watchlist Alert Comparison")
    alert_json_compare(path, "v6_alert-WATCHLIST-f6af290d-6a7f-461c-a8af-cf0d24311105.json",
                       "v6_by_v7_alert-WATCHLIST-f6af290d-6a7f-461c-a8af-cf0d24311105.json",
                       "v7_alert-WATCHLIST-f6af290d-6a7f-461c-a8af-cf0d24311105.json")
    # CONTAINER_RUNTIME
    print("")
    print("Container Runtime Alert Comparison")
    print("Containers not run")
    # alert_json_compare(path, "v6_alert-CONTAINER_RUNTIME-46b419c8-3d67-ead8-dbf1-9d8417610fac.json",
    #                    "v6_by_v7_alert-CONTAINER_RUNTIME-46b419c8-3d67-ead8-dbf1-9d8417610fac.json",
    #                    "v7_alert-CONTAINER_RUNTIME-46b419c8-3d67-ead8-dbf1-9d8417610fac.json")
    # DEVICE_CONTROL
    print("")
    print("Device Control Alert Comparison")
    alert_json_compare(path, "v6_alert-DEVICE_CONTROL-b6a7e48b-1d14-11ee-a9e0-888888888788.json",
                       "v6_by_v7_alert-DEVICE_CONTROL-b6a7e48b-1d14-11ee-a9e0-888888888788.json",
                       "v7_alert-DEVICE_CONTROL-b6a7e48b-1d14-11ee-a9e0-888888888788.json")
    # HBFW
    print("")
    print("Host Based Firewall Alert Comparison")
    alert_json_compare(path, "v6_alert-HOST_BASED_FIREWALL-2be0652f-20bc-3311-9ded-8b873e28d830.json",
                       "v6_by_v7_alert-HOST_BASED_FIREWALL-2be0652f-20bc-3311-9ded-8b873e28d830.json",
                       "v7_alert-HOST_BASED_FIREWALL-2be0652f-20bc-3311-9ded-8b873e28d830.json")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
