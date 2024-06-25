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

"""
Replicates export for Attack Stages

Requirements:
 - Create a CUSTOM API Key with org.alerts READ permission
    https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/#authenticating-your-request
 - Python 3 with pip
 - Carbon Black Cloud Python SDK
    https://pypi.org/project/carbon-black-cloud-sdk/

Optional Inputs:
  --severity SEVERITY, -s SEVERITY: (default=1) Minimum severity of alerts

  --range RANGE, -r RANGE: (default=3d) Time range from current time to X time ago.
                           Format: [quantity][unit] where unit is one of s for seconds,
                           m for minutes, h for hours, d for days, and w for weeks


Example:
    Once you install the Carbon Black Cloud Python SDK follow the Getting Started guide
        https://carbon-black-cloud-python-sdk.readthedocs.io/en/latest/getting-started/

    python3 alert_csv_export.py --profile custom \
                                --severity 3 \
                                --range 2w

    If you don't create a profile after installing the Carbon Black Cloud Python SDK then you'll need to specify
    each component below

    python3 alert_csv_export.py --cburl https://defense.conferdeploy.net \
                                --apitoken API_SECRET_KEY/API_ID \
                                --orgkey EXAMPLEKEY \
                                --severity 3 \
                                --range 2w
"""

import sys

from cbc_sdk.platform import CBAnalyticsAlert
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object

from datetime import datetime


def get_args():
    """Build argument parser and process cli args"""
    parser = build_cli_parser()
    parser.add_argument("--severity", "-s", type=int, default=1, help="Minimum severity of alerts")
    parser.add_argument("--range", "-r", type=str, default="3d", help="Time range from current time to X time ago. "
                                                                      "Format: [quantity][unit] where unit is one of"
                                                                      " s for seconds, m for minutes, h for hours,"
                                                                      " d for days, and w for weeks")
    return parser.parse_args()


def main():
    """Export an ordered csv file by kill_chain_status to current directory"""
    args = get_args()
    cb = get_cb_cloud_object(args)

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    sep = "|"

    attack_stages_query = cb.select(CBAnalyticsAlert)

    if args.severity:
        attack_stages_query = attack_stages_query.set_minimum_severity(args.severity)

    if args.range:
        attack_stages_query = attack_stages_query.set_time_range('last_update_time', range=f'-{args.range}')

    stages = [
        "RECONNAISSANCE",
        "WEAPONIZE",
        "DELIVER_EXPLOIT",
        "INSTALL_RUN",
        "COMMAND_AND_CONTROL",
        "EXECUTE_GOAL",
        "BREACH"
    ]

    processed_alerts = set()
    try:
        print(f'Writing Attack Stages to: attack_stages_{now}.csv')
        with open(f'attack_stages_{now}.csv', 'w') as export_file:
            export_file.write('Alert ID,Alert,ThreatScore,TargetPriority,Vector,Stage,First Seen,'
                              'DeviceHostName,Username,Policy,On/Off Premise,TTPs,ThreatCategory,'
                              'RunState,PolicyAppliedState,Dismissed,Reputation\n')
            for stage in stages:
                attack_stages_query = attack_stages_query.set_kill_chain_statuses([stage])

                alerts = list(attack_stages_query)
                if len(alerts) > 0:
                    for alert in alerts:
                        # Check if Alert was already exported as an Alert can have one or more kill_chain_statuses
                        if alert.id in processed_alerts:
                            continue
                        processed_alerts.add(alert.id)

                        export_file.write(f'{alert.id},')  # Alert ID
                        export_file.write(f'{alert.reason},')  # Alert
                        export_file.write(f'{alert.severity},')  # ThreatScore
                        export_file.write(f'{alert.target_value},')  # TargetPriority
                        export_file.write(f'{alert.threat_cause_vector},')  # Vector
                        export_file.write(f'{sep.join(alert.kill_chain_status)},')  # Stage
                        export_file.write(f'{alert.first_event_time},')  # First Seen
                        export_file.write(f'{alert.device_name},')  # DeviceHostName
                        export_file.write(f'{alert.device_username},')  # Username
                        export_file.write(f'{alert.policy_name},')  # Policy
                        export_file.write(f'{alert.device_location},')  # On/Off Premise
                        ttps = set()
                        if alert.threat_indicators:
                            for indicator in alert.threat_indicators:
                                if indicator["ttps"]:
                                    for ttp in indicator["ttps"]:
                                        ttps.add(ttp)
                        export_file.write(f'{sep.join(list(ttps))},')  # TTPs
                        export_file.write(f'{alert.threat_cause_threat_category},')  # ThreatCategory
                        export_file.write(f'{alert.run_state},')  # RunState
                        export_file.write(f'{alert.policy_applied},')  # PolicyAppliedState
                        export_file.write(f'{False if alert.workflow["state"] else True},')  # Dismissed
                        export_file.write(f'{alert.threat_cause_reputation},')  # Reputation
                        export_file.write('\n')
    except Exception as e:
        print(f'Verify your args are valid. Exception {e}')


if __name__ == "__main__":
    sys.exit(main())
