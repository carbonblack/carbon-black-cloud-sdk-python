#!/usr/bin/env python3

# *******************************************************
# Copyright (c) VMware, Inc. 2020. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Jobs API"""

import logging
from cbc_sdk.base import NewBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin


log = logging.getLogger(__name__)


class Job(NewBaseModel):
    urlobject = "/jobs/v1/orgs/{0}/jobs"
    urlobject_single = "/jobs/v1/orgs/{0}/jobs/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/job.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        super(Job, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        else:
            self._full_init = True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        return JobQuery(cls, cb)

    def _refresh(self):
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._full_init = True
        self._last_refresh_time = time.time()
        return True

    def get_progress(self):
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + "/progress"
        resp = self._cb.get_object(url)
        self._info['progress'] = resp
        return resp['num_total'], resp['num_completed'], resp['message']


class JobQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    def __init__(self, doc_class, cb):
        super(JobQuery, self).__init__(None)
        self._doc_class = doc_class
        self._cb = cb

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Returns:
            list[dict]: The raw results of the query, as a list of dicts.
        """
        rawdata = self._cb.get_object(Job.urlobject.format(self._cb.credentials.org_key))
        return rawdata.get('results', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Returns:
            int: The number of results from the run of this query.
        """
        if not self._count_valid:
            return_data = self._execute()
            self._total_results = len(return_data)
            self._count_valid = True
        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Args:
            from_row (int): Unused in this implementation, always 0.
            max_rows (int): Unused in this implementation, always -1.

        Returns:
            Iterable: The iterated query.
        """
        return_data = self._execute()
        self._total_results = len(return_data)
        self._count_valid = True
        for item in return_data:
            yield Job(self._cb, item['id'], item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Args:
            context (object): Not used; always None.

        Returns:
            list[Job]: Result of the async query, as a list of Job objects.
        """
        return_data = self._execute()
        output = [Job(self._cb, item['id'], item) for item in return_data]
        self._total_results = len(output)
        self._count_valid = True
        return output
