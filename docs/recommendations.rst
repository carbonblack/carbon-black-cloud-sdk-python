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
    ...     print(f"{rec.recommendation_id}/{rec.new_rule_.filename}/{rec.new_rule_.override_list} - "
    ...           f"{rec.workflow_.status} - {rec.impact_.impact_score}")
    ...
    5e6926d4-0c55-4757-a94d-e05883d5ee4c/zoom.exe/WHITE_LIST - ACCEPTED - 1.1710311
    100503cd-1897-425f-93b5-1ccba320438d/cxuiuexe.exe/WHITE_LIST - NEW - 0.2678737
    3f89a837-034c-4b81-9f4c-f673a36ccb5c/mbcloudea.exe/WHITE_LIST - ACCEPTED - 0.11177378
    26ddb565-aff6-4b68-895c-fc286aa5f101/svctcom.exe/WHITE_LIST - REJECTED - 0.05499694

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
     Last refreshed at Wed Sep 22 14:15:55 2021
    -------------------------------------------------------------------------------

                 create_time: 2021-09-11T07:12:12.064Z
                  created_by: estark@example.com
                 description: test_recommendation_review
                          id: 95b1f2b112cf11eca7813f4ceaa27a41
        include_child_processes: False
               override_list: WHITE_LIST
               override_type: IT_TOOL
                        path: c:\windows\ccm\*
                      source: RECOMMENDATION
                  source_ref: c9221b98-f64c-45dc-acb4-93caacd9dcee

More information about reputation overrides may be found in :doc:`reputation-override`.
