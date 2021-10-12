Recommendations
===============

Recommendations offer a quick shortcut for helping tune your policy configurations in an environment, by providing
suggested reputation overrides which you may add to improve your policy. They can speed up the process of tuning your
policy to an environment, rather than having to manually investigate endpoint activity and reconfigure the policy in
response to those investigations.

The Carbon Black Cloud SDK for Python offers assistance for dealing with Recommendations.

Getting the List of Recommendations
-----------------------------------

By querying the ``Recommendation`` object, you can see which recommendations have already been generated for you by
the Carbon Black Cloud.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import Recommendation
    >>> query = api.select(Recommendation).set_statuses(['NEW', 'ACCEPTED', 'REJECTED']).sort_by('impact_score', 'DESC')
    >>> recslist = list(query)
    >>> for rec in recslist:
    ...     print(rec)
    ...
    Recommendation object, bound to https://example.org.
    -------------------------------------------------------------------------------

                   impact: [RecommendationImpact object]:
                                event_count: 2
                               impact_score: 1.1710311
                           impacted_devices: 44
                               org_adoption: HIGH
                                update_time: 2021-05-18T16:37:07.000Z

                 new_rule: [RecommendationNewRule object]:
                                filename: zoom.exe
                           override_list: WHITE_LIST
                           override_type: SHA256
                             sha256_hash: 56f560d8254ebb453daeaf9abe5c3c6de2e18eafaa5a9e4...

                policy_id: 0
        recommendation_id: 5e6926d4-0c55-4757-a94d-e05883d5ee4c
                rule_type: reputation_override
                 workflow: [RecommendationWorkflow object]:
                            changed_by: estark@example.com
                               comment: test_recommendation_review_dismissed
                           create_time: 2021-05-18T16:37:07.000Z
                                ref_id: 6d90188a0d4f11ecb02e15835b040340
                                status: ACCEPTED
                           update_time: 2021-09-04T07:12:13.000Z

    Recommendation object, bound to https://example.org.
    -------------------------------------------------------------------------------

                   impact: [RecommendationImpact object]:
                                event_count: 9
                               impact_score: 0.2678737
                           impacted_devices: 5
                               org_adoption: HIGH
                                update_time: 2021-05-18T16:37:07.000Z

                 new_rule: [RecommendationNewRule object]:
                                filename: cxuiuexe.exe
                           override_list: WHITE_LIST
                           override_type: SHA256
                             sha256_hash: 90b196987fe62657bfce2627ab0a08a7096737363e13806...

                policy_id: 0
        recommendation_id: 100503cd-1897-425f-93b5-1ccba320438d
                rule_type: reputation_override
                 workflow: [RecommendationWorkflow object]:
                            changed_by: jbaratheon@example.com
                               comment:
                           create_time: 2021-05-18T16:37:07.000Z
                                status: NEW
                           update_time: 2021-09-14T07:12:13.000Z

    Recommendation object, bound to https://example.org.
    -------------------------------------------------------------------------------

                   impact: [RecommendationImpact object]:
                                event_count: 12
                               impact_score: 0.11177378
                           impacted_devices: 315
                               org_adoption: MEDIUM
                                update_time: 2021-05-18T16:37:07.000Z

                 new_rule: [RecommendationNewRule object]:
                                filename: mbcloudea.exe
                           override_list: WHITE_LIST
                           override_type: SHA256
                             sha256_hash: 0a2190c4ccfde82ef950836d014f31b2b188423bb67b51a...

                policy_id: 0
        recommendation_id: 3f89a837-034c-4b81-9f4c-f673a36ccb5c
                rule_type: reputation_override
                 workflow: [RecommendationWorkflow object]:
                            changed_by: tlannister@example.com
                               comment: test_recommendation_review_dismissed
                           create_time: 2021-05-18T16:37:07.000Z
                                ref_id: 16e842eb152b11eca8407fb13248831f
                                status: ACCEPTED
                           update_time: 2021-09-14T07:12:15.000Z

    Recommendation object, bound to https://example.org.
    -------------------------------------------------------------------------------

                   impact: [RecommendationImpact object]:
                                event_count: 20
                               impact_score: 0.05499694
                           impacted_devices: 44
                               org_adoption: MEDIUM
                                update_time: 2021-05-18T16:37:07.000Z

                 new_rule: [RecommendationNewRule object]:
                                filename: svctcom.exe
                           override_list: WHITE_LIST
                           override_type: SHA256
                             sha256_hash: d49a2beb44a603faf8aab2f5dfae3a292497c63f0b30d0e...

                policy_id: 0
        recommendation_id: 26ddb565-aff6-4b68-895c-fc286aa5f101
                rule_type: reputation_override
                 workflow: [RecommendationWorkflow object]:
                            changed_by: mtyrell@example.com
                               comment: test_recommendation_review_dismissed
                           create_time: 2021-05-18T16:37:07.000Z
                                status: REJECTED
                           update_time: 2021-09-11T07:12:14.000Z


**N.B.:** If you do not set status values on the recommendation query with ``set_statuses()``, the search defaults to
looking for ``NEW`` recommendations *only.*

Recommendations Workflow
------------------------

Individual recommendations in the ``NEW`` state may be accepted or rejected by calling their ``accept()`` or
``reject()`` methods, respectively.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import Recommendation
    >>> query = api.select(Recommendation).set_statuses(['NEW'])
    >>> recommendation = query[0]
    >>> recommendation.accept('Comment for acceptance')
    >>> print(recommendation.workflow_.status)
    ACCEPTED
    >>> recommendation = query[1]
    >>> recommendation.reject('Comment for rejection')
    >>> print(recommendation.workflow_.status)
    REJECTED

Individual recommendations in the ``ACCEPTED`` or ``REJECTED`` states may be reverted to the ``NEW`` state by calling
their ``reset()`` method.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import Recommendation
    >>> query = api.select(Recommendation).set_statuses(['REJECTED'])
    >>> recommendation = query.first()
    >>> recommendation.reset()
    >>> print(recommendation.workflow_.status)
    NEW

Recommendations and Reputation Overrides
----------------------------------------

A recommendation in the ``ACCEPTED`` state will have a reputation override created for it.  You can retrieve that
object with the ``reputation_override()`` method.

::

    >>> from cbc_sdk import CBCloudAPI
    >>> api = CBCloudAPI(profile='sample')
    >>> from cbc_sdk.endpoint_standard import Recommendation
    >>> query = api.select(Recommendation).set_statuses(['ACCEPTED'])
    >>> reputation_override = query.first().reputation_override()
    >>> print(reputation_override)
    ReputationOverride object, bound to https://example.org.
     Last refreshed at Wed Oct  6 08:51:49 2021
    -------------------------------------------------------------------------------

          create_time: 2021-09-15T07:12:12.594Z
           created_by: estark@example.com
          description: test_recommendation_review
             filename: pangphip.exe
                   id: 3fa9f84515f411ecb2525dd14785e643
        override_list: WHITE_LIST
        override_type: SHA256
          sha256_hash: 6a2cac7f36af5cebe0debbdb161d4f66b694b75192f1af4...
               source: RECOMMENDATION
           source_ref: 7b4e20d9-db28-408b-b7e9-af4008fa65cc

More information about reputation overrides may be found in :doc:`reputation-override`.
