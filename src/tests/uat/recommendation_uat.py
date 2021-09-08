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


def compare_impact(impact, raw_data):
    """
    Compare a RecommendationImpact object against the data that should represent it.

    Args:
        impact (RecommendationImpact): The RecommendationImpact object to compare.
        raw_data (dict): The dictionary containing what should be the same data.
    """
    assert impact.event_count == raw_data['event_count']
    assert impact.impact_score == raw_data['impact_score']
    assert impact.impacted_devices == raw_data['impacted_devices']
    assert impact.org_adoption == raw_data['org_adoption']
    assert impact.update_time == raw_data['update_time']


def compare_application(application, raw_data):
    """
    Compare a RecommendationApplication object against the data that should represent it.

    Args:
        application (RecommendationApplication): The Recommendation object to compare.
        raw_data (dict): The dictionary containing what should be the same data.
    """
    assert application.type == raw_data['type']
    assert application.value == raw_data['value']


def compare_new_rule(new_rule, raw_data):
    """
    Compare a RecommendationNewRule object against the data that should represent it.

    Args:
        new_rule (RecommendationNewRule): The RecommendationNewRule object to compare.
        raw_data (dict): The dictionary containing what should be the same data.
    """
    assert new_rule.action == raw_data['action']
    assert new_rule.certificate_authority == raw_data['certificate_authority']
    assert new_rule.filename == raw_data['filename']
    assert new_rule.include_child_processes == raw_data['include_child_processes']
    assert new_rule.operation == raw_data['operation']
    assert new_rule.override_list == raw_data['override_list']
    assert new_rule.override_type == raw_data['override_type']
    assert new_rule.path == raw_data['path']
    assert new_rule.sha256_hash == raw_data['sha256_hash']
    assert new_rule.signed_by == raw_data['signed_by']
    if new_rule.application:
        compare_application(new_rule.application, raw_data['application'])
    else:
        assert 'application' not in raw_data


def compare_workflow(workflow, raw_data):
    """
    Compare a RecommendationWorkflow object against the data that should represent it.

    Args:
        workflow (RecommendationWorkflow): The RecommendationWorkflow object to compare.
        raw_data (dict): The dictionary containing what should be the same data.
    """
    assert workflow.changed_by == raw_data['changed_by']
    assert workflow.create_time == raw_data['create_time']
    assert workflow.ref_id == raw_data['ref_id']
    assert workflow.status == raw_data['status']
    assert workflow.update_time == raw_data['update_time']
    assert workflow.comment == raw_data['comment']


def compare_recommendation(recommendation, raw_data):
    """
    Compare a Recommendation object against the data that should represent it.

    Args:
        recommendation (Recommendation): The Recommendation object to compare.
        raw_data (dict): The dictionary containing what should be the same data.
    """
    assert recommendation.policy_id == raw_data['policy_id']
    assert recommendation.recommendation_id == raw_data['recommendation_id']
    assert recommendation.rule_type == raw_data['rule_type']
    if recommendation.impact:
        compare_impact(recommendation.impact, raw_data['impact'])
    else:
        assert 'impact' not in raw_data
    if recommendation.new_rule:
        compare_new_rule(recommendation.new_rule, raw_data['new_rule'])
    else:
        assert 'new_rule' not in raw_data
    if recommendation.workflow:
        compare_workflow(recommendation.workflow, raw_data['workflow'])
    else:
        assert 'workflow' not in raw_data


def compare_list_of_recommendations(recommendations, raw_data):
    """
    Compare a list of recommendations against the raw data that should represent them.

    Args:
        recommendations (list[Recommendation]): The list of Recommendation objects to compare.
        raw_data (list[dict]): The list of dictionaries containing what should be the same data.
    """
    assert len(recommendations) == len(raw_data)
    for recommendation, raw_segment in zip(recommendations, raw_data):
        compare_recommendation(recommendation, raw_segment)


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
    compare_list_of_recommendations(recommendations, raw_data['results'])
    print('Search Recommendations......OK')


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
