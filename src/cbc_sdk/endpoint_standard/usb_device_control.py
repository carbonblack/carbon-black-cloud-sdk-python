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

"""Model and Query Classes for USB Device Control"""

from cbc_sdk.base import (NewBaseModel, MutableBaseModel, BaseQuery, QueryBuilder, QueryBuilderSupportMixin,
                          CriteriaBuilderSupportMixin, IterableQueryMixin, AsyncQueryMixin)
from cbc_sdk.errors import ApiError, ServerError
from cbc_sdk.platform.jobs import Job
import logging
import time
import json

log = logging.getLogger(__name__)

"""USB Device Control models"""


class USBDeviceApproval(MutableBaseModel):
    """Represents a USB device approval."""
    urlobject = "/device_control/v3/orgs/{0}/approvals"
    urlobject_single = "/device_control/v3/orgs/{0}/approvals/{1}"
    primary_key = "id"
    swagger_meta_file = "endpoint_standard/models/usbDeviceApproval.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the USBDeviceApproval object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(USBDeviceApproval, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            USBDeviceApprovalQuery: The query object for this alert type.
        """
        return USBDeviceApprovalQuery(cls, cb)

    def _build_api_request_uri(self, http_method="GET"):
        """
        Build the unique URL used to make requests for this object.

        Required Permissions:
            external-device.manage (READ)

        Args:
            http_method (str): Not used; retained for compatibility.

        Returns:
            str: The URL used to make requests for this object.
        """
        return self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)

    def _refresh(self):
        """
        Rereads the object data from the server.

        Returns:
            bool: True if refresh was successful, False if not.
        """
        resp = self._cb.get_object(self._build_api_request_uri())
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def _update_object(self):
        """
        Updates the object data on the server.

        Required Permissions:
            external-device.manage (CREATE)

        Returns:
            str: The unique ID of this object.
        """
        if self._model_unique_id is None:
            approval_in = {key: self._info[key]
                           for key in ['serial_number', 'vendor_id', 'product_id', 'approval_name', 'notes']
                           if key in self._info}
            output = USBDeviceApproval.bulk_create(self._cb, [approval_in])
            new_approval = output[0]
            self._info = new_approval._info
            self._last_refresh_time = time.time()
            return new_approval.id
        else:
            ret = self._cb.put_object(self._build_api_request_uri(), self._info)
            return self._refresh_if_needed(ret)

    @classmethod
    def create_from_usb_device(cls, usb_device):
        """
        Creates a new, unsaved approval object from a USBDeviceObject, filling in its basic fields.

        Args:
            usb_device (USBDevice): The USB device to create the approval from.

        Returns:
            USBDeviceApproval: The new approval object.
        """
        return USBDeviceApproval(usb_device._cb, None, {key: usb_device._info[key]
                                                        for key in ['serial_number', 'vendor_id', 'product_id']
                                                        if key in usb_device._info})

    @classmethod
    def bulk_create(cls, cb, approvals):
        """
        Creates multiple approvals and returns the USBDeviceApproval objects.  Data is supplied as a list of dicts.

        Required Permissions:
            external-device.manage (CREATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            approvals (list): List of dicts containing approval data to be created, formatted as shown below.

        Example:
            >>> [
                    {
                        "approval_name": "string",
                        "notes": "string",
                        "product_id": "string",
                        "serial_number": "string",
                        "vendor_id": "string"
                    }
                ]

        Returns:
            list: A list of USBDeviceApproval objects representing the approvals that were created.
        """
        url = cls.urlobject.format(cb.credentials.org_key) + "/_bulk"
        resp = cb.post_object(url, body=approvals)
        result = resp.json()
        item_list = result.get("results", [])
        return [cls(cb, item["id"], item) for item in item_list]

    @classmethod
    def bulk_create_csv(cls, cb, approval_data):
        """
        Creates multiple approvals and returns the USBDeviceApproval objects.  Data is supplied as text in CSV format.

        Required Permissions:
            external-device.manage (CREATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            approval_data (str): CSV data for the approvals to be created.  Header line MUST be included
                                 as shown below.

        Example:
            vendor_id,product_id,serial_number,approval_name,notes

            string,string,string,string,string

        Returns:
            list: A list of USBDeviceApproval objects representing the approvals that were created.
        """
        url = cls.urlobject.format(cb.credentials.org_key) + "/_bulk"
        resp = cb.post_object(url, body=approval_data, headers={"Content-Type": "text/csv"})
        result = resp.json()
        item_list = result.get("results", [])
        return [cls(cb, item["id"], item) for item in item_list]


class USBDeviceBlock(NewBaseModel):
    """Represents a USB device block."""
    urlobject = "/device_control/v3/orgs/{0}/blocks"
    urlobject_single = "/device_control/v3/orgs/{0}/blocks/{1}"
    primary_key = "id"
    swagger_meta_file = "endpoint_standard/models/usbDeviceBlock.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the USBDeviceBlock object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(USBDeviceBlock, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            USBDeviceBlockQuery: The query object for this alert type.
        """
        return USBDeviceBlockQuery(cls, cb)

    def _build_api_request_uri(self, http_method="GET"):
        """
        Build the unique URL used to make requests for this object.

        Args:
            http_method (str): Not used; retained for compatibility.

        Returns:
            str: The URL used to make requests for this object.
        """
        return self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)

    def _refresh(self):
        """
        Rereads the object data from the server.

        Required Permissions:
            org.policies (READ)

        Returns:
            bool: True if refresh was successful, False if not.
        """
        resp = self._cb.get_object(self._build_api_request_uri())
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def delete(self):
        """
        Delete this object.

        Required Permissions:
            org.policies (DELETE), external-device.enforce (UPDATE)
        """
        if self._model_unique_id:
            ret = self._cb.delete_object(self._build_api_request_uri())
        else:
            return

        if ret.status_code not in (200, 204):
            try:
                result = json.loads(ret.text)[0]
            except Exception:
                result = ret.text
            raise ServerError(ret.status_code, f"Did not delete {str(self)}.", result=result,
                              uri=self._build_api_request_uri())

    @classmethod
    def create(cls, cb, policy_id):
        """
        Creates a USBDeviceBlock for a given policy ID.

        Required Permissions:
            org.policies (UPDATE), external-device.enforce (UPDATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            policy_id (str/int): Policy ID to create a USBDeviceBlock for.

        Returns:
            USBDeviceBlock: New USBDeviceBlock object representing the block.
        """
        output = USBDeviceBlock.bulk_create(cb, [str(policy_id)])
        return output[0]

    @classmethod
    def bulk_create(cls, cb, policy_ids):
        """
        Creates multiple blocks and returns the USBDeviceBlocks that were created.

        Required Permissions:
            org.policies (UPDATE), external-device.enforce (UPDATE)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            policy_ids (list): List of policy IDs to have blocks created for.

        Returns:
            list: A list of USBDeviceBlock objects representing the approvals that were created.
        """
        request = [{"policy_id": s} for s in policy_ids]
        url = cls.urlobject.format(cb.credentials.org_key) + "/_bulk"
        resp = cb.post_object(url, body=request)
        result = resp.json()
        item_list = result.get("results", [])
        return [cls(cb, item["id"], item) for item in item_list]


class USBDevice(NewBaseModel):
    """Represents a USB device."""
    urlobject = "/device_control/v3/orgs/{0}/devices"
    urlobject_single = "/device_control/v3/orgs/{0}/devices/{1}"
    primary_key = "id"
    swagger_meta_file = "endpoint_standard/models/usbDevice.yaml"

    def __init__(self, cb, model_unique_id, initial_data=None):
        """
        Initialize the USBDevice object.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            model_unique_id (str): ID of the alert represented.
            initial_data (dict): Initial data used to populate the alert.
        """
        super(USBDevice, self).__init__(cb, model_unique_id, initial_data)
        if model_unique_id is not None and initial_data is None:
            self._refresh()
        self._full_init = True

    def approve(self, approval_name, notes):
        """
        Creates and saves an approval for this USB device, allowing it to be treated as approved from now on.

        Required Permissions:
            external-device.manage (CREATE)

        Args:
            approval_name (str): The name for this new approval.
            notes (str): Notes to be added to this approval.

        Returns:
            USBDeviceApproval: The new approval.
        """
        new_approval = USBDeviceApproval.create_from_usb_device(self)
        new_approval.approval_name = approval_name
        new_approval.notes = notes
        new_approval.save()
        self._refresh()
        return new_approval

    @classmethod
    def _query_implementation(cls, cb, **kwargs):
        """
        Returns the appropriate query object for this object type.

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.
            **kwargs (dict): Not used, retained for compatibility.

        Returns:
            USBDeviceQuery: The query object for this alert type.
        """
        return USBDeviceQuery(cls, cb)

    def _refresh(self):
        """
        Rereads the object data from the server.

        Required Permissions:
            external-device.manage (READ)

        Returns:
            bool: True if refresh was successful, False if not.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id)
        resp = self._cb.get_object(url)
        self._info = resp
        self._last_refresh_time = time.time()
        return True

    def get_endpoints(self):
        """
        Returns the information about endpoints associated with this USB device.

        Required Permissions:
            external-device.manage (READ)

        Returns:
            list: List of information about USB endpoints, each item specified as a dict.
        """
        url = self.urlobject_single.format(self._cb.credentials.org_key, self._model_unique_id) + "/endpoints"
        resp = self._cb.get_object(url)
        return resp.get("results", [])

    @classmethod
    def get_vendors_and_products_seen(cls, cb):
        """
        Returns all vendors and products that have been seen for the organization.

        Required Permissions:
            external-device.manage (READ)

        Args:
            cb (BaseAPI): Reference to API object used to communicate with the server.

        Returns:
            list: A list of vendors and products seen for the organization, each vendor being represented by a dict.
        """
        url = "/device_control/v3/orgs/{0}/products".format(cb.credentials.org_key)
        resp = cb.get_object(url)
        return resp.get("results", [])


"""USB Device Control queries"""


class USBDeviceApprovalQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                             IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate USBDeviceApproval objects."""
    VALID_EXPORT_FORMATS = ('CSV', 'JSON')

    def __init__(self, doc_class, cb):
        """
        Initialize the USBDeviceApprovalQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._total_results = 0

    def set_device_ids(self, device_ids):
        """
        Restricts the device approvals that this query is performed on to the specified device IDs.

        Args:
            device_ids (list): List of string device IDs.

        Returns:
            USBDeviceApprovalQuery: This instance.
        """
        if not all(isinstance(device_id, str) for device_id in device_ids):
            raise ApiError("One or more invalid device IDs")
        self._update_criteria("device.id", device_ids)
        return self

    def set_product_names(self, product_names):
        """
        Restricts the device approvals that this query is performed on to the specified product names.

        Args:
            product_names (list): List of string product names.

        Returns:
            USBDeviceApprovalQuery: This instance.
        """
        if not all(isinstance(product_name, str) for product_name in product_names):
            raise ApiError("One or more invalid product names")
        self._update_criteria("product_name", product_names)
        return self

    def set_vendor_names(self, vendor_names):
        """
        Restricts the device approvals that this query is performed on to the specified vendor names.

        Args:
            vendor_names (list): List of string vendor names.

        Returns:
            USBDeviceApprovalQuery: This instance.
        """
        if not all(isinstance(vendor_name, str) for vendor_name in vendor_names):
            raise ApiError("One or more invalid vendor names")
        self._update_criteria("vendor_name", vendor_names)
        return self

    def _build_request(self, from_row, max_rows):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.

        Returns:
            dict: The complete request body.
        """
        request = {"rows": 100}
        query = self._query_builder._collapse()
        if self._criteria:
            request["criteria"] = self._criteria
        if query:
            request["query"] = query

        # Fetch 100 rows per page (instead of 10 by default) for better performance
        if from_row > 0:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        return request

    def _build_url(self, tail_end):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Required Permissions:
            external-device.manage (READ)

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_available"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Required Permissions:
            external-device.manage (READ)

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_available"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item["id"], item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            if current >= self._total_results:
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Required Permissions:
            external-device.manage (READ)

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        self._total_results = result["num_available"]
        self._count_valid = True
        results = result.get("results", [])
        return [self._doc_class(self._cb, item["id"], item) for item in results]

    def export(self, export_format):
        """
        Starts the process of exporting USB device approval data from the organization in a specified format.

        Required Permissions:
            external-device.manage (READ)

        Args:
            export_format (str): The format to export USB device approval data in. Must be either "CSV" or "JSON".

        Returns:
            Job: The asynchronous job that will provide the export output when the server has prepared it.
        """
        if not (export_format and export_format.upper() in USBDeviceApprovalQuery.VALID_EXPORT_FORMATS):
            raise ApiError(f"invalid export format `{export_format}`")
        request = self._build_request(0, -1)
        request['format'] = export_format
        url = self._build_url("/_export")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        if 'job_id' not in result:
            raise ApiError("no job ID returned from server")
        return Job(self._cb, result['job_id'])


class USBDeviceBlockQuery(BaseQuery, IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate USBDeviceBlock objects."""

    def __init__(self, doc_class, cb):
        """
        Initialize the USBDeviceBlockQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._total_results = 0

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Required Permissions:
            org.policies (READ)

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        result = self._cb.get_object(self._doc_class.urlobject.format(self._cb.credentials.org_key))
        results = result.get("results", [])

        self._total_results = len(results)
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Required Permissions:
            org.policies (READ)

        Args:
            from_row (int): The row to start the query at (ignored).
            max_rows (int): The maximum number of rows to be returned (ignored).

        Returns:
            Iterable: The iterated query.
        """
        result = self._cb.get_object(self._doc_class.urlobject.format(self._cb.credentials.org_key))
        results = result.get("results", [])

        self._total_results = len(results)
        self._count_valid = True

        for item in results:
            yield self._doc_class(self._cb, item["id"], item)

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Required Permissions:
            org.policies (READ)

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        result = self._cb.get_object(self._doc_class.urlobject.format(self._cb.credentials.org_key))
        results = result.get("results", [])
        self._total_results = len(results)
        self._count_valid = True
        return [self._doc_class(self._cb, item["id"], item) for item in results]


class USBDeviceQuery(BaseQuery, QueryBuilderSupportMixin, CriteriaBuilderSupportMixin,
                     IterableQueryMixin, AsyncQueryMixin):
    """Represents a query that is used to locate USBDevice objects."""
    VALID_STATUSES = ["APPROVED", "UNAPPROVED"]
    VALID_FACET_FIELDS = ["vendor_name", "product_name", "endpoint.endpoint_name", "status"]
    VALID_EXPORT_FORMATS = ('CSV', 'JSON')

    def __init__(self, doc_class, cb):
        """
        Initialize the USBDeviceQuery.

        Args:
            doc_class (class): The model class that will be returned by this query.
            cb (BaseAPI): Reference to API object used to communicate with the server.
        """
        self._doc_class = doc_class
        self._cb = cb
        self._count_valid = False
        super(BaseQuery, self).__init__()
        self._query_builder = QueryBuilder()
        self._criteria = {}
        self._sortcriteria = {}
        self._total_results = 0
        self.max_rows = -1

    def set_endpoint_names(self, endpoint_names):
        """
        Restricts the devices that this query is performed on to the specified endpoint names.

        Args:
            endpoint_names (list): List of string endpoint names.

        Returns:
            USBDeviceQuery: This instance.
        """
        if not all(isinstance(endpoint_name, str) for endpoint_name in endpoint_names):
            raise ApiError("One or more invalid endpoint names")
        self._update_criteria("endpoint.endpoint_name", endpoint_names)
        return self

    def set_product_names(self, product_names):
        """
        Restricts the devices that this query is performed on to the specified product names.

        Args:
            product_names (list): List of string product names.

        Returns:
            USBDeviceQuery: This instance.
        """
        if not all(isinstance(product_name, str) for product_name in product_names):
            raise ApiError("One or more invalid product names")
        self._update_criteria("product_name", product_names)
        return self

    def set_serial_numbers(self, serial_numbers):
        """
        Restricts the devices that this query is performed on to the specified serial numbers.

        Args:
            serial_numbers (list): List of string serial numbers.

        Returns:
            USBDeviceQuery: This instance.
        """
        if not all(isinstance(serial_number, str) for serial_number in serial_numbers):
            raise ApiError("One or more invalid serial numbers")
        self._update_criteria("serial_number", serial_numbers)
        return self

    def set_statuses(self, statuses):
        """
        Restricts the devices that this query is performed on to the specified status values.

        Args:
            statuses (list): List of string status values.  Valid values are APPROVED and UNAPPROVED.

        Returns:
            USBDeviceQuery: This instance.
        """
        if not all((s in USBDeviceQuery.VALID_STATUSES) for s in statuses):
            raise ApiError("One or more invalid status values")
        self._update_criteria("status", statuses)
        return self

    def set_vendor_names(self, vendor_names):
        """
        Restricts the devices that this query is performed on to the specified vendor names.

        Args:
            vendor_names (list): List of string vendor names.

        Returns:
            USBDeviceQuery: This instance.
        """
        if not all(isinstance(vendor_name, str) for vendor_name in vendor_names):
            raise ApiError("One or more invalid vendor names")
        self._update_criteria("vendor_name", vendor_names)
        return self

    def set_max_rows(self, max_rows):
        """
        Sets the max number of usb devices to fetch in a singular query

        Args:
            max_rows (integer): Max number of usb devices

        Returns:
            USBDeviceQuery: This instance.

        Raises:
            ApiError: If rows is negative or greater than 10000
        """
        if max_rows < 0 or max_rows > 10000:
            raise ApiError("Max rows must be between 0 and 10000")
        self.max_rows = max_rows
        return self

    def sort_by(self, key, direction="ASC"):
        """
        Sets the sorting behavior on a query's results.

        Example:
            >>> cb.select(USBDevice).sort_by("product_name")

        Args:
            key (str): The key in the schema to sort by.
            direction (str): The sort order, either "ASC" or "DESC".

        Returns:
            USBDeviceQuery: This instance.
        """
        if direction not in CriteriaBuilderSupportMixin.VALID_DIRECTIONS:
            raise ApiError("invalid sort direction specified")
        self._sortcriteria = {"field": key, "order": direction}
        return self

    def _build_request(self, from_row, max_rows, add_sort=True):
        """
        Creates the request body for an API call.

        Args:
            from_row (int): The row to start the query at.
            max_rows (int): The maximum number of rows to be returned.
            add_sort (bool): If True(default), the sort criteria will be added as part of the request.

        Returns:
            dict: The complete request body.
        """
        request = {"rows": 100}
        query = self._query_builder._collapse()
        if self._criteria:
            request["criteria"] = self._criteria
        if query:
            request["query"] = query
        # Fetch 100 rows per page (instead of 10 by default) for better performance
        if from_row > 0:
            request["start"] = from_row
        if max_rows >= 0:
            request["rows"] = max_rows
        elif self.max_rows >= 0:
            request["rows"] = self.max_rows

        if add_sort and self._sortcriteria != {}:
            request["sort"] = [self._sortcriteria]
        return request

    def _build_url(self, tail_end):
        """
        Creates the URL to be used for an API call.

        Args:
            tail_end (str): String to be appended to the end of the generated URL.

        Returns:
            str: The complete URL.
        """
        url = self._doc_class.urlobject.format(self._cb.credentials.org_key) + tail_end
        return url

    def _count(self):
        """
        Returns the number of results from the run of this query.

        Required Permissions:
            external-device.manage (READ)

        Returns:
            int: The number of results from the run of this query.
        """
        if self._count_valid:
            return self._total_results

        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()

        self._total_results = result["num_available"]
        self._count_valid = True

        return self._total_results

    def _perform_query(self, from_row=0, max_rows=-1):
        """
        Performs the query and returns the results of the query in an iterable fashion.

        Required Permissions:
            external-device.manage (READ)

        Args:
            from_row (int): The row to start the query at (default 0).
            max_rows (int): The maximum number of rows to be returned (default -1, meaning "all").

        Returns:
            Iterable: The iterated query.
        """
        url = self._build_url("/_search")
        current = from_row
        numrows = 0
        still_querying = True
        while still_querying:
            request = self._build_request(current, max_rows)
            resp = self._cb.post_object(url, body=request)
            result = resp.json()

            self._total_results = result["num_available"]
            self._count_valid = True

            results = result.get("results", [])
            for item in results:
                yield self._doc_class(self._cb, item["id"], item)
                current += 1
                numrows += 1

                if max_rows > 0 and numrows == max_rows:
                    still_querying = False
                    break

            if current >= self._total_results:
                break

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query.

        Required Permissions:
            external-device.manage (READ)

        Args:
            context (object): Not used, always None.

        Returns:
            list: Result of the async query, which is then returned by the future.
        """
        url = self._build_url("/_search")
        request = self._build_request(0, -1)
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        self._total_results = result["num_available"]
        self._count_valid = True
        results = result.get("results", [])
        return [self._doc_class(self._cb, item["id"], item) for item in results]

    def facets(self, fieldlist, max_rows=0):
        """
        Return information about the facets for all known USB devices, using the defined criteria.

        Required Permissions:
            external-device.manage (READ)

        Args:
            fieldlist (list): List of facet field names. Valid names are "vendor_name", "product_name",
                              "endpoint.endpoint_name", and "status".
            max_rows (int): The maximum number of rows to return. 0 means return all rows.

        Returns:
            list: A list of facet information specified as dicts.
        """
        if not all((field in USBDeviceQuery.VALID_FACET_FIELDS) for field in fieldlist):
            raise ApiError("One or more invalid term field names")
        request = self._build_request(0, -1, False)
        del request["rows"]
        request["terms"] = {"fields": fieldlist, "rows": max_rows}
        url = self._build_url("/_facet")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        return result.get("terms", [])

    def export(self, export_format):
        """
        Starts the process of exporting USB device data from the organization in a specified format.

        Required Permissions:
            external-device.manage (READ)

        Args:
            export_format (str): The format to export USB device data in. Must be either "CSV" or "JSON".

        Returns:
            Job: The asynchronous job that will provide the export output when the server has prepared it.
        """
        if not (export_format and export_format.upper() in USBDeviceQuery.VALID_EXPORT_FORMATS):
            raise ApiError(f"invalid export format `{export_format}`")
        request = self._build_request(0, -1)
        request['format'] = export_format
        url = self._build_url("/_export")
        resp = self._cb.post_object(url, body=request)
        result = resp.json()
        if 'job_id' not in result:
            raise ApiError("no job ID returned from server")
        return Job(self._cb, result['job_id'])
