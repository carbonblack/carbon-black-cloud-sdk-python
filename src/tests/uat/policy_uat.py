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

"""Manual Test script for policy."""

import sys


def main():
    """Entry function for testing policy functions.

    This testing uses the example script examples/platform/policy_service_crud_operations.py

    It should be run from the command line in the following sequence, with variables replaced as follows.

    * PROFILE_NAME - the profile in credentials.cbc that has permission to CREATE, READ, UPDATE and DELETE permissions
    for policy management.  This is Policies > Policies > “org.policies” group of permissions.
    * DEFAULT_POLICY_ID - the Id of the default policy provided with Carbon Black Cloud.  Obtain this from the
    Carbon Black Cloud console.

    Sequence on command line is:

    # 0. List the policies
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose list

    # 1. export the default policy
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose export \
        --id DEFAULT_POLICY_ID
    # visually inspect the exported file.  Record the name for the next step

    # 2. import the default policy.  This tests the Create Policy function.
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose import -N \
        unique_policy_name -d policy_description -p MEDIUM -f policy_file_from_previous_export_step
    # record the policy id.  This is NEW_POLICY_ID in future steps

    # 3. Create a rule
    # Create a file (RULE_FILE.json) with one rule in it.  This sample works, or any valid variation
        {
          "application": {
            "type": "REPUTATION",
            "value": "SUSPECT_MALWARE"
          },
          "required": false,
          "operation": "RUN",
          "action": "DENY"
        }
    # Import the rule
    $ python3 examples/platform/policy_service_crud_operations.py  --profile PROFILE_NAME --verbose add-rule --id \
        NEW_POLICY_ID -f RULE_FILE.json

    # Export the new policy - verify changes are included
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose export \
        --id NEW_POLICY_ID
    # Verify the rule is there and write down the rule id (RULE_ID).
    # Also check the CBC console (refresh the screen)

    # Delete the rule
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose del-rule \
        -i NEW_POLICY_ID -r RULE_ID
    #Check in CBC console that it's not there

    # Delete the policy – put everything back how it was
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose delete \
        --id NEW_POLICY_ID

    # Then check the builder function works correctly:
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose \
        build-minimal-policy -N unique_policy_name -d description -p MEDIUM
    # Verify the policy has been created and write down the rule id (BUILDER_POLICY_ID)

    # Delete the policy – put everything back how it was
    $ python3 examples/platform/policy_service_crud_operations.py --profile PROFILE_NAME --verbose delete \
        --id BUILDER_POLICY_ID
    """


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
