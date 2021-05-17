"""
Replicates export for Attacks Detected and Attacks Stopped

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

    python3 attacks_detected_stopped_export.py --profile custom \
                                               --severity 3 \
                                               --range 2w

    If you don't create a profile after installing the Carbon Black Cloud Python SDK then you'll need to specify
    each component below

    python3 attacks_detected_stopped_export.py --cburl https://defense.conferdeploy.net \
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
    """Export two csv files based on policy APPLIED and NOT_APPLIED to current directory"""
    args = get_args()
    cb = get_cb_cloud_object(args)

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    sep = "|"

    alerts_stopped = cb.select(CBAnalyticsAlert).set_policy_applied(['APPLIED'])
    alerts_detected = cb.select(CBAnalyticsAlert).set_policy_applied(['NOT_APPLIED'])

    if args.severity:
        alerts_stopped = alerts_stopped.set_minimum_severity(args.severity)
        alerts_detected = alerts_detected.set_minimum_severity(args.severity)

    if args.range:
        alerts_stopped = alerts_stopped.set_time_range('last_update_time', range=f'-{args.range}')
        alerts_detected = alerts_detected.set_time_range('last_update_time', range=f'-{args.range}')

    try:
        if len(alerts_stopped) > 0:
            print(f'Writing Attacks Stopped to: attacks_stopped_{now}.csv')
            with open(f'attacks_stopped_{now}.csv', 'w') as stopped:
                stopped.write('Alert ID,Alert,ThreatScore,TargetPriority,Vector,Stage,First Seen,DeviceHostName,'
                              'Username,Policy,On/Off Premise,TTPs,ThreatCategory,RunState,PolicyAppliedState,'
                              'Dismissed,Reputation\n')
                for alert in alerts_stopped:
                    stopped.write(f'{alert.id},')  # Alert ID
                    stopped.write(f'{alert.reason},')  # Alert
                    stopped.write(f'{alert.severity},')  # ThreatScore
                    stopped.write(f'{alert.target_value},')  # TargetPriority
                    stopped.write(f'{alert.threat_cause_vector},')  # Vector
                    stopped.write(f'{sep.join(alert.kill_chain_status)},')  # Stage
                    stopped.write(f'{alert.first_event_time},')  # First Seen
                    stopped.write(f'{alert.device_name},')  # DeviceHostName
                    stopped.write(f'{alert.device_username},')  # Username
                    stopped.write(f'{alert.policy_name},')  # Policy
                    stopped.write(f'{alert.device_location},')  # On/Off Premise
                    ttps = set()
                    if alert.threat_indicators:
                        for indicator in alert.threat_indicators:
                            if indicator["ttps"]:
                                for ttp in indicator["ttps"]:
                                    ttps.add(ttp)
                    stopped.write(f'{sep.join(list(ttps))},')  # TTPs
                    stopped.write(f'{alert.threat_cause_threat_category},')  # ThreatCategory
                    stopped.write(f'{alert.run_state},')  # RunState
                    stopped.write(f'{alert.policy_applied},')  # PolicyAppliedState
                    stopped.write(f'{False if alert.workflow["state"] else True},')  # Dismissed
                    stopped.write(f'{alert.threat_cause_reputation},')  # Reputation
                    stopped.write('\n')

        if len(alerts_detected) > 0:
            print(f'Writing Attacks Stopped to: attacks_detected_{now}.csv')
            with open(f'attacks_detected_{now}.csv', 'w') as detected:
                detected.write('Alert ID,Alert,ThreatScore,TargetPriority,Vector,Stage,First Seen,DeviceHostName,'
                               'Username,Policy,On/Off Premise,TTPs,ThreatCategory,RunState,PolicyAppliedState,'
                               'Dismissed,Reputation\n')
                for alert in alerts_detected:
                    detected.write(f'{alert.id},')  # Alert ID
                    detected.write(f'{alert.reason},')  # Alert
                    detected.write(f'{alert.severity},')  # ThreatScore
                    detected.write(f'{alert.target_value},')  # TargetPriority
                    detected.write(f'{alert.threat_cause_vector},')  # Vector
                    detected.write(f'{sep.join(alert.kill_chain_status)},')  # Stage
                    detected.write(f'{alert.first_event_time},')  # First Seen
                    detected.write(f'{alert.device_name},')  # DeviceHostName
                    detected.write(f'{alert.device_username},')  # Username
                    detected.write(f'{alert.policy_name},')  # Policy
                    detected.write(f'{alert.device_location},')  # On/Off Premise
                    ttps = set()
                    if alert.threat_indicators:
                        for indicator in alert.threat_indicators:
                            if indicator["ttps"]:
                                for ttp in indicator["ttps"]:
                                    ttps.add(ttp)
                    detected.write(f'{sep.join(list(ttps))},')  # TTPs
                    detected.write(f'{alert.threat_cause_threat_category},')  # ThreatCategory
                    detected.write(f'{alert.run_state},')  # RunState
                    detected.write(f'{alert.policy_applied},')  # PolicyAppliedState
                    detected.write(f'{False if alert.workflow["state"] else True},')  # Dismissed
                    detected.write(f'{alert.threat_cause_reputation},')  # Reputation
                    detected.write('\n')
    except Exception as e:
        print(f'Verify your args are valid. Exception {e}')


if __name__ == "__main__":
    sys.exit(main())
