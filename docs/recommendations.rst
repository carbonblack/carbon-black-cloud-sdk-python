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
    ...     print(f"{rec.recommendation_id} - {rec.workflow_.status} - {rec.impact_.impact_score}")
    ...
    5e6926d4-0c55-4757-a94d-e05883d5ee4c - ACCEPTED - 1.1710311
    c9221b98-f64c-45dc-acb4-93caacd9dcee - ACCEPTED - 0.71904415
    8afdcebc-12ca-4b63-8d8f-2d8055b652f2 - NEW - 0.6051892
    100503cd-1897-425f-93b5-1ccba320438d - ACCEPTED - 0.2678737
    b44586ea-4bba-4684-addb-d4934c10b3e2 - NEW - 0.1663951
    3f89a837-034c-4b81-9f4c-f673a36ccb5c - NEW - 0.11177378
    d9a9a122-8440-44d2-9fa4-84e77345155b - ACCEPTED - 0.08829709
    7fcb6092-7adb-4069-861b-fed439d5f22a - REJECTED - 0.063399866
    26ddb565-aff6-4b68-895c-fc286aa5f101 - ACCEPTED - 0.05499694
    908e691e-5dbf-4028-bb52-a41cedada2f9 - ACCEPTED - 0.016786003

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
    >>> print(reputation_override.id)
    add2969714b811ecbf7c61c0c0ef6d2a

More information about reputation overrides may be found in :doc:`reputation-override`.
