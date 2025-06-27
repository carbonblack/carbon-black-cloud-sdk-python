#!/usr/bin/env python3

# *******************************************************
# Copyright (c) Broadcom, Inc. 2020-2025. All Rights Reserved. Carbon Black.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Model and Query Classes for Jobs API"""

import io
import logging
import time
from cbc_sdk.base import NewBaseModel, BaseQuery, IterableQueryMixin, AsyncQueryMixin
from cbc_sdk.errors import ObjectNotFoundError, ServerError, ApiError
from cbc_sdk.utils import BackoffHandler


log = logging.getLogger(__name__)


class Job(NewBaseModel):
    """Represents a job currently executing in the background."""
    urlobject = "/jobs/v1/orgs/{0}/jobs"
    urlobject_single = "/jobs/v1/orgs/{0}/jobs/{1}"
    primary_key = "id"
    swagger_meta_file = "platform/models/job.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the Job object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (int): ID of the job.
            initial_data (dict): Initial data used to populate the job.
        """
        super(Job, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        else:
            self._full_init = True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for Jobs.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            JobQuery: The query object for this object type.
        """
        return JobQuery(cls, cb)

    def _refresh(self):
        """
        Reload this object from the server.

        Required Permissions:
            jobs.status (READ)
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._full_init = True
        self._last_refresh_time = time.time()
        return True

    def get_progress(self):
        """
        Get and return the current progress information for the job.

        Required Permissions:
            jobs.status (READ)

        Returns:
            int: Total number of items to be operated on by this job.
            int: Total number of items for which operation has been completed.
            str: Current status message for the job.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + "/progress"
        resp = self._cb.get_object(url)
        self._info['progress'] = resp
        return resp['num_total'], resp['num_completed'], resp.get('message', None)

    def _await_completion(self, timeout=0):
        """
        Waits for this job to complete by examining the progress data.

        Required Permissions:
            jobs.status (READ)

        Args:
            timeout (int): The timeout for this wait in milliseconds. If this is 0, the default value will be used.

        Returns:
            Job: This object.

        Raises:
            TimeoutError: If the wait times out.
        """
        backoff = BackoffHandler(self._cb, timeout=timeout)
        with backoff as b:
            errorcount = 0
            status = ""
            while status not in ("FAILED", "COMPLETED"):
                b.pause()
                try:
                    self._refresh()
                    if self.status != status:
                        status = self.status
                        b.reset()
                except (ServerError, ObjectNotFoundError):
                    errorcount += 1
                    if errorcount == 3:
                        raise
                    status = ""
            if status == "FAILED":
                raise ApiError(f"Job {self.id} reports failure")
        return self

    def await_completion(self, timeout=0):
        """
        Create a Python ``Future`` to check for job completion and return results when available.

        Returns a ``Future`` object which can be used to await results that are ready to fetch. This function call
        does not block.

        Required Permissions:
            jobs.status (READ)

        Args:
            timeout (int): The timeout for this wait in milliseconds. If this is 0, the default value will be used.

        Returns:
            Future: A ``Future`` which can be used to wait for this job's completion. When complete, the result of the
                    ``Future`` will be this object.
        """
        return self._cb._async_submit(lambda arg, kwarg: arg[0]._await_completion(timeout), self)

    def get_output_as_stream(self, output):
        """
        Export the results from the job, writing the results to the given stream.

        Required Permissions:
            jobs.status (READ)

        Args:
            output (RawIOBase): Stream to write the CSV data from the request to.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + '/download'
        self._cb.api_request_stream('GET', url, output)

    def get_output_as_string(self):
        """
        Export the results from the job, returning the results as a string.

        Required Permissions:
            jobs.status (READ)

        Returns:
            str: The results from the job.
        """
        with io.BytesIO() as buffer:
            self.get_output_as_stream(buffer)
            return str(buffer.getvalue(), 'utf-8')

    def get_output_as_file(self, filename):
        """
        Export the results from the job, writing the results to the given file.

        Required Permissions:
            jobs.status (READ)

        Args:
            filename (str): Name of the file to write the results to.
        """
        with io.open(filename, 'wb') as file:
            self.get_output_as_stream(file)

    def get_output_as_lines(self):
        """
        Export the results from the job, returning the data as iterated lines of text.

        This is only intended for output that can reasonably be represented as lines of text, such as plain text or
        CSV.  If a job outputs structured text like JSON or XML, this method should not be used.

        Required Permissions:
            jobs.status (READ)

        Returns:
            iterable: An iterable that can be used to get each line of text in turn as a string.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + '/download'
        yield from self._cb.api_request_iterate('GET', url)


class JobQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    """Query for retrieving current jobs."""
    def __init__(self, doc_class, cb):
        """
        Initialize the Query object.

        Args:
            doc_class (class): The class of the model this query returns.
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
        """
        super(JobQuery, self).__init__(None)
        self._doc_class = doc_class
        self._cb = cb
        self._total_results = -1
        self._count_valid = False

    def _execute(self):
        """
        Executes the query and returns the list of raw results.

        Required Permissions:
            jobs.status(READ)

        Returns:
            list[dict]: The raw results of the query, as a list of dicts.
        """
        rawdata = self._cb.get_object(Job.urlobject.format(self._cb.credentials.org_key))
        return rawdata.get('results', [])

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Required Permissions:
            jobs.status(READ)

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

        Required Permissions:
            jobs.status(READ)

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

        Required Permissions:
            jobs.status(READ)

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
