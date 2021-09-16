#!/usr/bin/env python
# *******************************************************
# Copyright (c) VMware, Inc. 2020-2021. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""
The following API calls are tested in this script.

For the validation CBC API requests are used.

To execute, a profile must be provided using the standard CBC Credentials.

Recommendations:
* Search Recommendations

The following API calls were not covered:
* Recommendation Workflow
"""

import sys
import requests
from cbc_sdk.helpers import build_cli_parser, get_cb_cloud_object
from cbc_sdk.endpoint_standard import Recommendation


def compare(context, object_field, raw_data, raw_field):
    """
    Compare an object field value against the raw field value it should have come from.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        object_field (Any): The value of the object field being compared.
        raw_data (dict): Raw data structure we're comparing a field from.
        raw_field (str): Name of the raw field we're doing the comparison on.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    if raw_field in raw_data:
        result = (object_field == raw_data[raw_field])
    else:
        result = (object_field is None)
    if not result:
        print(f"field value {raw_field} did not match in {context} - object value {object_field}, "
              f"raw value {raw_data.get(raw_field, None)}")
    return result


def check_not_present(context, raw_data, raw_field):
    """
    Verifies that a specified field is not present in a raw data structure.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        raw_data (dict): Raw data structure we're checking a field from.
        raw_field (str): Name of the raw field we're verifying is not present.

    Returns:
        True if the field was not present, False if it was.
    """
    if raw_field not in raw_data:
        return True
    print(f"field value {raw_field} should be absent from {context}, but is not")
    return False


def compare_impact(context, impact, raw_data):
    """
    Compare a RecommendationImpact object against the data that should represent it.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        impact (RecommendationImpact): The RecommendationImpact object to compare.
        raw_data (dict): The dictionary containing what should be the same data.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    result = compare(context, impact.event_count, raw_data, 'event_count')
    result = compare(context, impact.impact_score, raw_data, 'impact_score') and result
    result = compare(context, impact.impacted_devices, raw_data, 'impacted_devices') and result
    result = compare(context, impact.org_adoption, raw_data, 'org_adoption') and result
    result = compare(context, impact.update_time, raw_data, 'update_time') and result
    return result


def compare_application(context, application, raw_data):
    """
    Compare a RecommendationApplication object against the data that should represent it.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        application (RecommendationApplication): The Recommendation object to compare.
        raw_data (dict): The dictionary containing what should be the same data.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    result = compare(context, application.type, raw_data, 'type')
    result = compare(context, application.value, raw_data, 'value') and result
    return result


def compare_new_rule(context, new_rule, raw_data):
    """
    Compare a RecommendationNewRule object against the data that should represent it.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        new_rule (RecommendationNewRule): The RecommendationNewRule object to compare.
        raw_data (dict): The dictionary containing what should be the same data.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    result = compare(context, new_rule.action, raw_data, 'action')
    result = compare(context, new_rule.certificate_authority, raw_data, 'certificate_authority') and result
    result = compare(context, new_rule.filename, raw_data, 'filename') and result
    result = compare(context, new_rule.include_child_processes, raw_data, 'include_child_processes') and result
    result = compare(context, new_rule.operation, raw_data, 'operation') and result
    result = compare(context, new_rule.override_list, raw_data, 'override_list') and result
    result = compare(context, new_rule.override_type, raw_data, 'override_type') and result
    result = compare(context, new_rule.path, raw_data, 'path') and result
    result = compare(context, new_rule.sha256_hash, raw_data, 'sha256_hash') and result
    result = compare(context, new_rule.signed_by, raw_data, 'signed_by') and result
    if new_rule.application_:
        result = compare_application(f"{context}.application", new_rule.application_,
                                     raw_data['application']) and result
    else:
        result = check_not_present(context, raw_data, 'application') and result
    return result


def compare_workflow(context, workflow, raw_data):
    """
    Compare a RecommendationWorkflow object against the data that should represent it.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        workflow (RecommendationWorkflow): The RecommendationWorkflow object to compare.
        raw_data (dict): The dictionary containing what should be the same data.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    result = compare(context, workflow.changed_by, raw_data, 'changed_by')
    result = compare(context, workflow.create_time, raw_data, 'create_time') and result
    result = compare(context, workflow.ref_id, raw_data, 'ref_id') and result
    result = compare(context, workflow.status, raw_data, 'status') and result
    result = compare(context, workflow.update_time, raw_data, 'update_time') and result
    result = compare(context, workflow.comment, raw_data, 'comment') and result
    return result


def compare_recommendation(context, recommendation, raw_data):
    """
    Compare a Recommendation object against the data that should represent it.

    Args:
        context (str): The context of the comparison, used for printing error messages.
        recommendation (Recommendation): The Recommendation object to compare.
        raw_data (dict): The dictionary containing what should be the same data.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    result = compare(context, recommendation.policy_id, raw_data, 'policy_id')
    result = compare(context, recommendation.recommendation_id, raw_data, 'recommendation_id') and result
    result = compare(context, recommendation.rule_type, raw_data, 'rule_type') and result
    if recommendation.impact_:
        result = compare_impact(f"{context}.impact", recommendation.impact_, raw_data['impact']) and result
    else:
        result = check_not_present(context, raw_data, 'impact') and result
    if recommendation.new_rule_:
        result = compare_new_rule(f"{context}.new_rule", recommendation.new_rule_, raw_data['new_rule']) and result
    else:
        result = check_not_present(context, raw_data, 'new_rule') and result
    if recommendation.workflow_:
        result = compare_workflow(f"{context}.workflow", recommendation.workflow_, raw_data['workflow']) and result
    else:
        result = check_not_present(context, raw_data, 'workflow') and result
    return result


def compare_list_of_recommendations(recommendations, raw_data, verbose):
    """
    Compare a list of recommendations against the raw data that should represent them.

    Args:
        recommendations (list[Recommendation]): The list of Recommendation objects to compare.
        raw_data (list[dict]): The list of dictionaries containing what should be the same data.
        verbose (bool): True to print slightly more information.

    Returns:
        bool: True if comparison was successful, False if not.
    """
    if len(recommendations) != len(raw_data):
        print(f"resulting lists are of different lengths - object list {len(recommendations)}, "
              f"raw list {len(raw_data)}")
        return False
    if verbose:
        print(f"Comparing {len(recommendations)} items")
    index = 0
    success = 0
    for recommendation, raw_segment in zip(recommendations, raw_data):
        if verbose:
            print(f"Comparing item at index #{index}")
        if compare_recommendation(f"recommendations[{index}]", recommendation, raw_segment):
            success += 1
        index += 1
    if (success != index) or verbose:
        print(f"comparison of return lists: {success}/{index} compared OK")
    return success == index


def search_recommendations_raw(config_data):
    """
    Post a raw request to do a recommendations search.

    Args:
        config_data (dict): Contains configuration data for the request.

    Returns:
        dict: JSON output from the "search recommendations" API.
    """
    url = "{0}recommendation-service/v1/orgs/{1}/recommendation/_search".format(config_data['hostname'],
                                                                                config_data['org_key'])
    request_body = {'criteria': {}, 'sort': [{'field': 'impact_score', 'order': 'DESC'}]}
    request_headers = {'X-Auth-Token': config_data['apikey']}
    response = requests.post(url, json=request_body, headers=request_headers)
    return response.json()


def search_recommendations_api(api):
    """
    Use the API to do a recommendations search.

    Args:
        api (CBCloudAPI): The object connecting to the Carbon Black Cloud API.

    Returns:
        list[Recommendation]: A list of Recommendation objects.
    """
    query = api.select(Recommendation).sort_by('impact_score', 'DESC')
    return list(query)


def validate_status_via_raw(recommendation, config_data):
    """
    Runs validation checks against the recommendation status and associated reputation override.

    Args:
        recommendation (Recommendation): The recommendation object to be tested.
        config_data (dict): Contains configuration data for the request.

    Returns:
        bool: True if verification was successful, False if not.
    """
    url = "{0}recommendation-service/v1/orgs/{1}/recommendation/_search".format(config_data['hostname'],
                                                                                config_data['org_key'])
    request_body = {'criteria': {'status': ['NEW', 'REJECTED', 'ACCEPTED']}, 'rows': 50}
    request_headers = {'X-Auth-Token': config_data['apikey']}
    response = requests.post(url, json=request_body, headers=request_headers)
    if response.status_code != 200:
        print(f"attempt to get recommendation data failed with code {response.status_code}")
        return False

    result_array = response.json()['results']
    good_results = [block for block in result_array if block['recommendation_id'] == recommendation.recommendation_id]
    if len(good_results) != 1:
        print(f"Unable to re-locate recommendation with ID {recommendation.recommendation_id}")
        return False

    new_status = good_results[0]['workflow']['status']
    if new_status != recommendation.workflow_.status:
        print(f"Recommendation status incorrect - is {new_status}, should be {recommendation.workflow_.status}")
        return False

    if new_status == 'ACCEPTED':
        new_ref_id = good_results[0]['workflow'].get('ref_id', None)
        if not new_ref_id:
            print(f"Reputation Override reference ID is not present when it should be")
            return False

        rep_override = recommendation.reputation_override()
        if not rep_override:
            print(f"Reputation Override object is not present when it should be")
            return False

        url = "{0}appservices/v6/orgs/{1}/reputations/overrides/{2}".format(config_data['hostname'],
                                                                            config_data['org_key'], new_ref_id)
        response = requests.get(url, headers=request_headers)
        if response.status_code != 200:
            print(f"attempt to get reputation override data failed with code {response.status_code}")
            return False

        raw_rep_override = response.json()
        if raw_rep_override['id'] != rep_override.id:
            print(f"Reputation override ID incorrect - is {raw_rep_override['id']}, should be {rep_override.id}")
            return False

        if raw_rep_override['sha256_hash'] != rep_override.sha256_hash:
            print(f"Reputation override hash incorrect - is {raw_rep_override['sha256_hash']}, "
                  f"should be {rep_override.sha256_hash}")
            return False
    else:
        if good_results[0]['workflow'].get('ref_id', None):
            print(f"Reputation Override reference ID is present when it shouldn't be")
            return False

        if recommendation.reputation_override():
            print(f"Reputation Override object is present when it shouldn't be")
            return False

    return True


def main():
    """Script entry point"""
    parser = build_cli_parser()
    args = parser.parse_args()
    print_detail = args.verbose

    if print_detail:
        print(f"profile being used is {args.__dict__}")

    cb = get_cb_cloud_object(args)
    config_data = {'hostname': cb.credentials.url, 'org_key': cb.credentials.org_key, 'apikey': cb.credentials.token}

    recommendations = search_recommendations_api(cb)
    raw_data = search_recommendations_raw(config_data)
    result_search = compare_list_of_recommendations(recommendations, raw_data['results'], print_detail)
    print(f'Search Recommendations......{"OK" if result_search else "FAIL"}')

    result_workflow = True
    rec_candidates = [rec for rec in recommendations
                      if rec.rule_type == 'reputation_override' and rec.workflow_.status == 'NEW']
    if len(rec_candidates) > 0:
        recommendation = rec_candidates[0]  # arbitrary choice
        result_workflow = validate_status_via_raw(recommendation, config_data) and result_workflow
        if print_detail:
            print("--- Accepting recommendation")
        recommendation.accept()
        result_workflow = validate_status_via_raw(recommendation, config_data) and result_workflow
        if print_detail:
            print("--- Resetting recommendation")
        recommendation.reset()
        result_workflow = validate_status_via_raw(recommendation, config_data) and result_workflow
        if print_detail:
            print("--- Rejecting recommendation")
        recommendation.reject()
        result_workflow = validate_status_via_raw(recommendation, config_data) and result_workflow
        if print_detail:
            print("--- Resetting recommendation (again)")
        recommendation.reset()
        result_workflow = validate_status_via_raw(recommendation, config_data) and result_workflow
        print(f'Search Workflow.............{"OK" if result_workflow else "FAIL"}')
    else:
        print('Search Workflow.............Unable to run test (no candidate recommendations)')

    return 0 if result_search and result_workflow else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
