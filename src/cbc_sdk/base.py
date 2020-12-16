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

"""Models and Queries for the Base Carbon Black Cloud SDK"""

from __future__ import absolute_import

import copy
import base64
import os.path
from .utils import convert_from_cb, convert_to_cb
import yaml
import json
import time
from .errors import ApiError, ServerError, InvalidObjectError, MoreThanOneResultError
import logging
from datetime import datetime
from solrq import Q
import functools

log = logging.getLogger(__name__)

"""Base Models"""


class CreatableModelMixin(object):
    """Mixin for all objects which are creatable."""
    pass


class CbMetaModel(type):
    """Meta-model for NewBaseModel and its subclasses."""
    model_base_directory = os.path.dirname(__file__)
    model_classes = []

    def __new__(mcs, name, bases, clsdict):
        """
        Creates a new instance of a class, setting up the field descriptors based on the metafile.

        Args:
            name (str): The name of the class.
            bases (list): Base classes of the class to be created.
            clsdict (dict): Elements defined in the new class.
        """
        swagger_meta_file = clsdict.pop("swagger_meta_file", None)
        model_data = {}
        if swagger_meta_file:
            model_data = yaml.safe_load(
                open(os.path.join(mcs.model_base_directory, swagger_meta_file), 'rb').read())

        clsdict["__doc__"] = "Represents a %s object in the Carbon Black server.\n\n" % (name,)
        for field_name, field_info in iter(model_data.get("properties", {}).items()):
            docstring = field_info.get("description", None)
            if docstring:
                clsdict["__doc__"] += ":ivar %s: %s\n" % (field_name, docstring)

        foreign_keys = clsdict.pop("foreign_keys", {})

        cls = super(CbMetaModel, mcs).__new__(mcs, name, bases, clsdict)
        mcs.model_classes.append(cls)

        cls._valid_fields = []
        cls._required_fields = model_data.get("required", [])
        cls._default_value = {}

        for field_name, field_info in iter(model_data.get("properties", {}).items()):
            cls._valid_fields.append(field_name)

            default_value = field_info.get("default", None)
            if default_value:
                cls._default_value[field_name] = default_value

            field_format = field_info.get("type", "string")
            field_format = field_info.get("format", field_format)

            if field_format.startswith('int'):
                setattr(cls, field_name, FieldDescriptor(field_name, coerce_to=int))
            elif field_format == "iso-date-time":
                setattr(cls, field_name, IsoDateTimeFieldDescriptor(field_name))
            elif field_format == "epoch-ms-date-time":
                setattr(cls, field_name, EpochDateTimeFieldDescriptor(field_name, 1000.0))
            elif field_format == "boolean":
                setattr(cls, field_name, FieldDescriptor(field_name, coerce_to=bool))
            elif field_format == "array":
                setattr(cls, field_name, ArrayFieldDescriptor(field_name))
            elif field_format == "object":
                setattr(cls, field_name, ObjectFieldDescriptor(field_name))
            elif field_format == "double":
                setattr(cls, field_name, FieldDescriptor(field_name, coerce_to=float))
            elif field_format == "byte":
                setattr(cls, field_name, BinaryFieldDescriptor(field_name))
            else:
                setattr(cls, field_name, FieldDescriptor(field_name))

        for fk_name, fk_info in iter(foreign_keys.items()):
            setattr(cls, fk_name, ForeignKeyFieldDescriptor(fk_name, fk_info[0], fk_info[1]))

        return cls


class FieldDescriptor(object):
    """Object that describes a field within a model instance."""
    def __init__(self, field_name, coerce_to=None, default_value=None):
        """
        Initialize the FieldDescriptor object.

        Args:
            field_name (str): The name of the field.
            coerce_to (class): The type to which the value should be coerced, or None.
            default_value (Any): The default value of the field.
        """
        self.att_name = field_name
        self.default_value = default_value
        self.coerce_to = coerce_to

    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        if instance is not None:
            if self.att_name not in instance._info and not instance._full_init:
                instance.refresh()

            value = instance._info.get(self.att_name, self.default_value)
            coerce_type = self.coerce_to or type(value)
            if value is None:
                return None
            return coerce_type(value)

    def __set__(self, instance, value):
        """
        Sets the value of this field on an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            value (Any): New value for the field.
        """
        coerce_type = self.coerce_to or type(value)
        value = coerce_type(value)
        instance._set(self.att_name, value)


class ArrayFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields of 'array' type."""
    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        ret = super(ArrayFieldDescriptor, self).__get__(instance, instance_type)
        return ret or []


# TODO: this is a kludge to avoid writing "small" models?
class ObjectFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields of 'object' type."""
    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        ret = super(ObjectFieldDescriptor, self).__get__(instance, instance_type)
        return ret or {}


class IsoDateTimeFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields of 'iso-date-time' type."""
    def __init__(self, field_name):
        """
        Initialize the IsoDateTimeFieldDescriptor object.

        Args:
            field_name (str): The name of the field.
        """
        super(IsoDateTimeFieldDescriptor, self).__init__(field_name)

    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        d = super(IsoDateTimeFieldDescriptor, self).__get__(instance, instance_type)
        return convert_from_cb(d)

    def __set__(self, instance, value):
        """
        Sets the value of this field on an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            value (Any): New value for the field.
        """
        parsed_date = convert_to_cb(value)
        super(IsoDateTimeFieldDescriptor, self).__set__(instance, parsed_date)


class EpochDateTimeFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields of 'epoch-ms-date-time' type."""
    def __init__(self, field_name, multiplier=1.0):
        """
        Initialize the EpochDateTimeFieldDescriptor object.

        Args:
            field_name (str): The name of the field.
            multiplier(float): Unused.
        """
        super(EpochDateTimeFieldDescriptor, self).__init__(field_name)
        self.multiplier = float(multiplier)

    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        d = super(EpochDateTimeFieldDescriptor, self).__get__(instance, instance_type)
        if type(d) is float or type(d) is int:
            epoch_seconds = d / self.multiplier
            return datetime.utcfromtimestamp(epoch_seconds)
        else:
            return datetime.utcfromtimestamp(0)  # default to epoch time (1970-01-01) if we have a non-numeric type

    def __set__(self, instance, value):
        """
        Sets the value of this field on an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            value (Any): New value for the field.
        """
        if isinstance(value, datetime):
            new_value = (value - self.epoch).total_seconds() * self.multiplier
        else:
            new_value = value
        super(EpochDateTimeFieldDescriptor, self).__set__(instance, new_value)


class ForeignKeyFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields that are foreign keys."""
    def __init__(self, field_name, join_model, join_field=None):
        """
        Initialize the ForeignKeyFieldDescriptor object.

        Args:
            field_name (str): The name of the field.
            join_model (class): The class for which this field value is a foreign key.
            join_field (str): The name fo the field in the joined class for which this field value is a foreign key.
        """
        super(ForeignKeyFieldDescriptor, self).__init__(field_name)
        self.join_model = join_model
        if join_field is None:
            self.join_field = field_name + "_id"
        else:
            self.join_field = join_field

    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        foreign_id = getattr(instance, self.join_field)
        return instance._cb.select(self.join_model, foreign_id)

    def __set__(self, instance, value):
        """
        Sets the value of this field on an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            value (Any): New value for the field.
        """
        if type(value, NewBaseModel):
            setattr(self, self.join_field, getattr(value, "_model_unique_id"))
        else:
            setattr(self, self.join_field, value)


class BinaryFieldDescriptor(FieldDescriptor):
    """Field descriptor for fields of 'byte' type."""
    def __get__(self, instance, instance_type=None):
        """
        Retrieve the value of this field from an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            instance_type (class): Owning class type (not used).

        Returns:
            Any: Value of the field.
        """
        d = super(BinaryFieldDescriptor, self).__get__(instance, instance_type)
        return base64.b64decode(d)

    def __set__(self, instance, value):
        """
        Sets the value of this field on an object.

        Args:
            instance (NewBaseModel): Instance of the object to retrieve the field value from.
            value (Any): New value for the field.
        """
        super(BinaryFieldDescriptor, self).__set__(instance, base64.b64encode(value))


class NewBaseModel(object, metaclass=CbMetaModel):
    """Base class of all model objects within the Carbon Black Cloud SDK."""
    primary_key = "id"

    def __init__(self, cb, model_unique_id=None, initial_data=None, force_init=False, full_doc=False):
        """
        Initialize the NewBaseModel object.

        Args:
            cb (CBCloudAPI): A reference to the CBCloudAPI object.
            model_unique_id (Any): The unique ID for this particular instance of the model object.
            initial_data (dict): The data to use when initializing the model object.
            force_init (bool): True to force object initialization.
            full_doc (bool): True to mark the object as fully initialized.
        """
        self._cb = cb
        self._last_refresh_time = 0

        if initial_data is not None:
            self._info = initial_data
        else:
            self._info = {}

        if model_unique_id is not None:
            self._info[self.__class__.primary_key] = model_unique_id

        self._dirty_attributes = {}
        self._full_init = full_doc

        if force_init:
            self.refresh()

    @property
    def _model_unique_id(self):
        return self._info.get(self.__class__.primary_key, None)

    @classmethod
    def new_object(cls, cb, item, **kwargs):
        """
        Create a new object of a model class.

        Args:
            cb (CBCloudAPI): Reference to the CBCloudAPI object.
            item (dict): Item data to use to create the object.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            object: The new object instance.
        """
        return cb.select(cls, item[cls.primary_key], initial_data=item, **kwargs)

    def __getattr__(self, item):
        """
        Return an attribute of this object.

        Args:
            item (str): Name of the attribute to be returned.

        Returns:
            Any: The returned attribute value.

        Raises:
            AttributeError: If the object has no such attribute.
        """
        try:
            super(NewBaseModel, self).__getattribute__(item)
        except AttributeError:
            pass  # fall through to the rest of the logic...

        # try looking up via self._info, if we already have it.
        if item in self._info:
            return self._info[item]

        # if we're still here, let's load the object if we haven't done so already.
        if not self._full_init:
            self._refresh()

        # try one more time.
        if item in self._info:
            return self._info[item]
        else:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__,
                                                                              item))

    def __setattr__(self, attrname, val):
        """
        Set an attribute of this object.

        Args:
            attrname (str): Name of the attribute to be changed.
            val (Any): New value for the attribute.

        Raises:
            AttributeError: If the given attribute cannot be changed.
        """
        if attrname.startswith("_"):
            super(NewBaseModel, self).__setattr__(attrname, val)
        else:
            raise AttributeError("Field {0:s} is immutable".format(attrname))

    def get(self, attrname, default_val=None):
        """
        Return an attribute of this object.

        Args:
            attrname (str): Name of the attribute to be returned.
            default_val (Any): Default value to be used if the attribute is not set.

        Returns:
            Any: The returned attribute value, which may be defaulted.
        """
        return getattr(self, attrname, default_val)

    def _set(self, attrname, new_value):
        pass

    def refresh(self):
        """Reload this object from the server."""
        return self._refresh()

    def _refresh(self):
        if self._model_unique_id is not None and self.__class__.primary_key not in self._dirty_attributes.keys():
            # info = self._retrieve_cb_info()
            # print(f"self: {self}, self._retrieve_cb_info: {self._retrieve_cb_info()}")
            self._info = self._parse(self._retrieve_cb_info())
            self._full_init = True
            self._last_refresh_time = time.time()
            return True
        return False

    def _build_api_request_uri(self, http_method="GET"):
        baseuri = self.__class__.__dict__.get('urlobject', None)
        if self._model_unique_id is not None:
            return baseuri + "/%s" % self._model_unique_id
        else:
            return baseuri

    def _retrieve_cb_info(self):
        request_uri = self._build_api_request_uri()
        return self._cb.get_object(request_uri)

    def _parse(self, obj):
        return obj

    @property
    def original_document(self):
        """
        Returns the original meta-information about the object.

        Returns:
            object: The original meta-information about the object.
        """
        if not self._full_init:
            self.refresh()

        return self._info

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        if self._model_unique_id is not None:
            return "<%s.%s: id %s> @ %s" % (self.__class__.__module__, self.__class__.__name__, self._model_unique_id,
                                            self._cb.session.server)
        else:
            return "<%s.%s object at %s> @ %s" % (self.__class__.__module__, self.__class__.__name__, hex(id(self)),
                                                  self._cb.session.server)

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        lines = []
        lines.append("{0:s} object, bound to {1:s}.".format(self.__class__.__name__, self._cb.session.server))
        if self._last_refresh_time:
            lines.append(" Last refreshed at {0:s}".format(time.ctime(self._last_refresh_time)))
        if not self._full_init:
            lines.append(" Partially initialized. Use .refresh() to load all attributes")
        lines.append("-" * 79)
        lines.append("")

        # for dictionaries that can be sorted, sort them
        try:
            attributes = sorted(self._info)
        # dictionaries containing dictionaries cannot be sorted, so leave as is
        except:
            attributes = self._info

        for attr in attributes:
            # typical case, where the info dictionary value for this `attr` is a string
            if isinstance(attr, str):
                status = "   "
                if attr in self._dirty_attributes:
                    if self._dirty_attributes[attr] is None:
                        status = "(+)"
                    else:
                        status = "(*)"
                try:
                    val = str(self._info[attr])
                except UnicodeDecodeError:
                    val = repr(self._info[attr])
                if len(val) > 50:
                    val = val[:47] + u"..."
                lines.append(u"{0:s} {1:>20s}: {2:s}".format(status, attr, val))
            # edge case (seen in Facet searches) where the info dictionary value for this `attr` is a dictionary
            elif isinstance(attr, dict):
                # go through each attribute in the `attr` dictionary
                for att in attr:
                    status = "   "
                    if att in self._dirty_attributes:
                        if self._dirty_attributes[att] is None:
                            status = "(+)"
                        else:
                            status = "(*)"
                    try:
                        val = str(attr[att])
                    except UnicodeDecodeError:
                        val = repr(attr[att])
                    if len(val) > 50:
                        val = val[:47] + u"..."
                    lines.append(u"{0:s} {1:>20s}: {2:s}".format(status, att, val))

        return "\n".join(lines)

    def _join(self, join_cls, field_name):
        try:
            field_value = getattr(self, field_name)
        except AttributeError:
            return None

        if field_value is None:
            return None

        return self._cb.select(join_cls, field_value)


class UnrefreshableModel(NewBaseModel):
    """Represents a model that can't be refreshed, i.e. for which ``reset()`` is not a valid operation."""

    def refresh(self):
        """Reload this object from the server."""
        raise ApiError("refresh() called on an unrefreshable model")


class MutableBaseModel(NewBaseModel):
    """Base model for objects that can have properties changed and then saved back to the server."""
    _new_object_http_method = "POST"
    _change_object_http_method = "PUT"
    _new_object_needs_primary_key = False

    def __setattr__(self, attrname, val):
        """
        Set an attribute of this object.

        Args:
            attrname (str): Name of the attribute to be changed.
            val (Any): New value for the attribute.
        """
        # allow subclasses to define their own property setters
        propobj = getattr(self.__class__, attrname, None)
        if isinstance(propobj, property) and propobj.fset:
            return propobj.fset(self, val)

        if not attrname.startswith("_") and attrname not in self.__class__._valid_fields:
            if attrname in self._info:
                log.warning("Changing field not included in Swagger definition: {0:s}".format(attrname))
                self._set(attrname, val)
            else:
                print("Trying to set attribute {0:s}".format(attrname))
        else:
            object.__setattr__(self, attrname, val)

    def _set(self, attrname, new_value):
        # ensure that we are operating on the full object first
        if not self._full_init and self._model_unique_id is not None:
            self.refresh()

        # extract unique ID if we're updating a "joined" field
        if isinstance(new_value, NewBaseModel):
            new_value = new_value._model_unique_id

        # early exit if we attempt to set the field to its own value
        if new_value == self._info.get(attrname, None):
            return

        # update dirty_attributes if necessary
        if attrname in self._dirty_attributes:
            if new_value == self._dirty_attributes[attrname]:
                del self._dirty_attributes[attrname]
        else:
            self._dirty_attributes[attrname] = self._info.get(attrname, None)
        # finally, make the change
        self._info[attrname] = new_value

    def refresh(self):
        """Reload this object from the server."""
        if self._refresh():
            self._dirty_attributes = {}

    def is_dirty(self):
        """
        Returns whether or not any fields of this object have been changed.

        Returns:
            bool: True if any fields of this object have been changed, False if not.
        """
        return len(self._dirty_attributes) > 0

    def _update_object(self):
        if self.__class__.primary_key in self._dirty_attributes.keys() or self._model_unique_id is None:
            new_object_info = copy.deepcopy(self._info)
            try:
                if not self._new_object_needs_primary_key:
                    del (new_object_info[self.__class__.primary_key])
            except Exception:
                pass
            log.debug("Creating a new {0:s} object".format(self.__class__.__name__))
            http_method = self.__class__._new_object_http_method
            ret = self._cb.api_json_request(http_method, self.urlobject,
                                            data=new_object_info)
        else:
            log.debug("Updating {0:s} with unique ID {1:s}".format(self.__class__.__name__, str(self._model_unique_id)))
            http_method = self.__class__._change_object_http_method
            ret = self._cb.api_json_request(http_method, self._build_api_request_uri(http_method=http_method),
                                            data=self._info)

        return self._refresh_if_needed(ret)

    def _refresh_if_needed(self, request_ret):
        """
        Reload the object with the data returned by the server.

        Args:
            request_ret (Response): Return data from a request made to the server.

        Returns:
            Any: The unique ID of this object.
        """
        refresh_required = False

        if request_ret.status_code not in range(200, 300):
            try:
                message = json.loads(request_ret.text)[0]
            except Exception:
                message = request_ret.text

            raise ServerError(request_ret.status_code, message,
                              result="Did not update {} record.".format(self.__class__.__name__))
        else:
            try:
                message = request_ret.json()
                log.debug("Received response: %s" % message)
                if list(message.keys()) == ["result"]:
                    post_result = message.get("result", None)

                    if post_result and post_result != "success":
                        raise ServerError(request_ret.status_code, post_result,
                                          result="Did not update {0:s} record.".format(self.__class__.__name__))
                    else:
                        refresh_required = True
                else:
                    self._info = json.loads(request_ret.text)
                    if message.keys() == ["id"]:
                        # if all we got back was an ID, try refreshing to get the entire record.
                        log.debug("Only received an ID back from the server, forcing a refresh")
                        refresh_required = True
                    else:
                        self._full_init = True
            except Exception:
                refresh_required = True

        self._dirty_attributes = {}
        if refresh_required:
            self.refresh()
        return self._model_unique_id

    def save(self):
        """
        Save any changes made to this object's fields.

        Returns:
            MutableBaseModel: This object.
        """
        if not self.is_dirty():
            return

        self.validate()
        self._update_object()
        return self

    def reset(self):
        """Undo any changes made to this object's fields."""
        for k, v in iter(self._dirty_attributes.items()):
            if v is None:
                del self._info[k]
            else:
                self._info[k] = v

        self._dirty_attributes = {}

    # TODO: How do we delete this object from our LRU cache?
    def delete(self):
        """Delete this object."""
        return self._delete_object()

    def _delete_object(self):
        if self._model_unique_id:
            ret = self._cb.delete_object(self._build_api_request_uri())
        else:
            return

        if ret.status_code not in (200, 204):
            try:
                message = json.loads(ret.text)[0]
            except Exception:
                message = ret.text
            raise ServerError(ret.status_code, message, result="Did not delete {0:s}.".format(str(self)))

    def validate(self):
        """
        Validates this object.

        Returns:
            bool: True if the object is validated.

        Raises:
            InvalidObjectError: If the object has missing fields.
        """
        if not self._full_init:
            self.refresh()

        diff = list(set(self.__class__._required_fields) - set(self._info.keys()))
        if not diff:
            return True
        else:
            raise InvalidObjectError("Missing fields: [%s]" % (", ".join(diff)))

    def __repr__(self):
        """Returns a string representation of this object."""
        r = super(MutableBaseModel, self).__repr__()
        if self.is_dirty():
            r += " (*)"
        return r


"""Base Queries"""


class BaseQuery(object):
    """The base query for finding objects via the API."""
    def __init__(self, query=None):
        """
        Initializes the BaseQuery object.

        Args:
            query (solrq.Q): The parent query of this one.
        """
        self._query = query

    def _clone(self):
        return self.__class__(self._query)

    def all(self):
        """
        Returns the objects that this query has located, all at once.

        Returns:
            list: The list of query objects.
        """
        return self._perform_query()

    def first(self):
        """
        Returns the first result of this query.

        Returns:
            object: The first result of this query, or None if it has no results.
        """
        res = self[:1]
        if not len(res):
            return None
        return res[0]

    def one(self):
        """
        Returns the single result of this query.

        Returns:
            object: The single result of this query.

        Raises:
            MoreThanOneResultError: If the query has any number of results other than 1.
        """
        res = self[:2]

        if len(res) == 0 or len(res) > 1:
            raise MoreThanOneResultError(message="{0:d} results found for query {1:s}"
                                         .format(len(self), str(self._query)))

        return res[0]

    def _perform_query(self):
        # This has the effect of generating an empty iterator.
        yield from ()

    def __len__(self):
        """
        Returns the number of items returned by this query.

        Returns:
            int: The number of items returned by this query.
        """
        return 0

    def __getitem__(self, item):
        """
        Return a specific item or items from the query.

        Args:
            item (object): Indicates the item(s) to retrieve, either as an int or a slice.

        Returns:
            object: Either an item or a list of items.
        """
        return None

    def __iter__(self):
        """
        Returns an iterator over the items returned by this query.

        Returns:
            Iterator: An iterator over the items returned by this query.
        """
        return self._perform_query()


class SimpleQuery(BaseQuery):
    """A simple query object."""
    _multiple_where_clauses_accepted = False

    def __init__(self, cls, cb, urlobject=None, returns_fulldoc=True):
        """
        Initialize the SimpleQuery object.

        Args:
            cls (class): Class of the object to be returned by the query.
            cb (CBCloudAPI): Reference to the CBCloudAPI object.
            urlobject (str): URL to be used in making the query.
            returns_fulldoc (bool): Whether the result of the Query yields objects that have been fully initialized.
        """
        super(SimpleQuery, self).__init__()

        self._doc_class = cls
        if not urlobject:
            self._urlobject = cls.urlobject
        else:
            self._urlobject = urlobject
        self._cb = cb
        self._full_init = False
        self._results = []
        self._query = {}
        self._sort_by = None
        self._returns_full_doc = returns_fulldoc

    def _clone(self):
        nq = self.__class__(self._doc_class, self._cb)
        nq._urlobject = self._urlobject
        nq._full_init = self._full_init
        nq._results = self._results[::]
        nq._query = copy.deepcopy(self._query)
        nq._sort_by = self._sort_by

        return nq

    def _match_query(self, i):
        for k, v in iter(self._query.items()):
            if isinstance(v, str):
                v = v.lower()
            target = getattr(i, k, None)
            if target is None:
                return False
            if str(target).lower() != v:
                return False
        return True

    def _sort(self, result_set):
        if self._sort_by is not None:
            return sorted(result_set, key=lambda x: getattr(x, self._sort_by, 0), reverse=True)
        else:
            return result_set

    @property
    def results(self):
        """
        Collect and return the results of this query.

        Returns:
            list: The results of this query.
        """
        if not self._full_init:
            self._results = []
            for item in self._cb.get_object(self._urlobject, default=[]):
                t = self._doc_class.new_object(self._cb, item, full_doc=self._returns_full_doc)
                if self._match_query(t):
                    self._results.append(t)
            self._results = self._sort(self._results)
            self._full_init = True

        return self._results

    def __len__(self):
        """
        Returns the number of items returned by this query.

        Returns:
            int: The number of items returned by this query.
        """
        return len(self.results)

    def __getitem__(self, item):
        """
        Return a specific item or items from the query.

        Args:
            item (object): Indicates the item(s) to retrieve, either as an int or a slice.

        Returns:
            object: Either an item or a list of items.
        """
        if isinstance(item, slice):
            return [self.results[ii] for ii in range(*item.indices(len(self)))]
        elif isinstance(item, int):
            return self.results[item]
        else:
            raise TypeError("Invalid argument type")

    def where(self, new_query):
        """
        Add a "where" clause to this query.

        Args:
            new_query (object): The "where" clause, as a string or solrq.Q object.

        Returns:
            SimpleQuery: A new query with the "where" clause specified.
        """
        if self._query and not self._multiple_where_clauses_accepted:
            raise ApiError("Cannot have multiple 'where' clauses")

        nq = self._clone()
        field, value = new_query.split(':', 1)
        nq._query[field] = value
        nq._full_init = False
        return nq

    def and_(self, new_query):
        """
        Add an additional "where" clause to this query.

        Args:
            new_query (object): The additional "where" clause, as a string or solrq.Q object.

        Returns:
            SimpleQuery: A new query with the extra "where" clause specified.
        """
        if not self._multiple_where_clauses_accepted:
            raise ApiError("Cannot have multiple 'where' clauses")
        return self.where(new_query)

    def _perform_query(self):
        for item in self.results:
            yield item

    def sort(self, new_sort):
        """
        Set the sorting for this query.

        Args:
            new_sort (object): The new sort criteria for this query.

        Returns:
            SimpleQuery: A new query with the sort parameter specified.
        """
        nq = self._clone()
        nq._sort_by = new_sort
        return nq


class PaginatedQuery(BaseQuery):
    """A query that returns objects in a paginated fashion."""
    def __init__(self, cls, cb, query=None):
        """
        Initialize the PaginatedQuery object.

        Args:
            cls (class): The class of objects being returned by this query.
            cb (CBCloudAPI): Reference to the CBCloudAPI object.
            query (BaseQuery): The query that we are paginating.
        """
        super(PaginatedQuery, self).__init__(query)
        self._doc_class = cls
        self._cb = cb
        # TODO: this should be subject to a TTL
        self._total_results = 0
        self._count_valid = False
        self._batch_size = 100

    def _clone(self):
        nq = self.__class__(self._doc_class, self._cb, query=self._query)
        nq._batch_size = self._batch_size
        return nq

    def __len__(self):
        """
        Returns the number of items returned by this query.

        Returns:
            int: The number of items returned by this query.
        """
        if self._count_valid:
            return self._total_results
        return self._count()

    def __getitem__(self, item):
        """
        Return a specific item or items from the query.

        Args:
            item (object): Indicates the item(s) to retrieve, either as an int or a slice.

        Returns:
            object: Either an item or a list of items.
        """
        if isinstance(item, slice):
            if item.step and item.step != 1:
                raise ValueError("steps not supported")

            must_count_result_set = False
            if item.start is None or item.start == 0:
                start = 0
            else:
                start = item.start
                if item.start < 0:
                    must_count_result_set = True

            if item.stop is None or item.stop == 0:
                numrows = 0
            else:
                numrows = item.stop - start
                if item.stop < 0:
                    must_count_result_set = True
                elif numrows <= 0:
                    return []

            if must_count_result_set:
                log.debug('Must count result set')
                # general case
                item_range = range(*item.indices(len(self)))
                if not len(item_range):
                    return []

                start, numrows = item_range[0], len(item_range)

            try:
                return list(self._perform_query(start, numrows))
            except StopIteration:
                return []
        elif isinstance(item, int):
            if item < 0:
                item += len(self)
            if item < 0:
                return None

            try:
                return next(self._perform_query(item, 1))
            except StopIteration:
                return None
        else:
            raise TypeError("invalid type")

    def _perform_query(self, start=0, numrows=0):
        for item in self._search(start=start, rows=numrows):
            yield self._doc_class.new_object(self._cb, item)

    def batch_size(self, new_batch_size):
        """
        Set the batch size of the paginated query.

        Args:
            new_batch_size (int): The new batch size.

        Returns:
            PaginatedQuery: A new query with the updated batch size.
        """
        nq = self._clone()
        nq._batch_size = new_batch_size
        return nq


class QueryBuilder(object):
    """
    Provides a flexible interface for building prepared queries for the CB Cloud backend.

    This object can be instantiated directly, or can be managed implicitly
    through the CBCloudAPI.select API.

    Examples:
    >>> from cbc_sdk.base import QueryBuilder
    >>> # build a query with chaining
    >>> query = QueryBuilder().where(process_name="malicious.exe").and_(device_name="suspect")
    >>> # start with an initial query, and chain another condition to it
    >>> query = QueryBuilder(device_os="WINDOWS").or_(process_username="root")

    """

    def __init__(self, **kwargs):
        """
        Initialize the QueryBuilder object.

        Args:
            **kwargs (dict): If present, these are used to construct a Solrq Query.
        """
        if kwargs:
            self._query = Q(**kwargs)
        else:
            self._query = None
        self._raw_query = None
        self._process_guid = None

    def _guard_query_params(func):
        """Decorates the query construction methods of *QueryBuilder.*

        Prevents them from being called with parameters that would result in an internally
        inconsistent query.
        """

        @functools.wraps(func)
        def wrap_guard_query_change(self, q, **kwargs):
            if self._raw_query is not None and (kwargs or isinstance(q, Q)):
                raise ApiError("Cannot modify a raw query with structured parameters")
            if self._query is not None and isinstance(q, str):
                raise ApiError("Cannot modify a structured query with a raw parameter")
            return func(self, q, **kwargs)

        return wrap_guard_query_change

    @_guard_query_params
    def where(self, q, **kwargs):
        """
        Adds a conjunctive filter to a QueryBuilder.

        Args:
            q (object): Either a string or solrq.Q object representing the query to be added.
            **kwargs (dict): Arguments with which to construct a solrq.Q object.

        Returns:
            QueryBuilder: This object.

        Raises:
            ApiError: If the q parameter is of an invalid type.
        """
        if isinstance(q, str):
            if self._raw_query is None:
                self._raw_query = []
            self._raw_query.append(q)
        elif isinstance(q, Q) or kwargs:
            if self._query is not None:
                raise ApiError("Use .and_() or .or_() for an extant solrq.Q object")
            if kwargs:
                self._process_guid = self._process_guid or kwargs.get("process_guid")
                q = Q(**kwargs)
            self._query = q
        else:
            raise ApiError(".where() only accepts strings or solrq.Q objects")

        return self

    @_guard_query_params
    def and_(self, q, **kwargs):
        """
        Adds a conjunctive filter to a QueryBuilder.

        Args:
            q (object): Either a string or solrq.Q object representing the query to be added.
            **kwargs (dict): Arguments with which to construct a solrq.Q object.

        Returns:
            QueryBuilder: This object.

        Raises:
            ApiError: If the q parameter is of an invalid type.
        """
        if isinstance(q, str):
            self.where(q)
        elif isinstance(q, Q) or kwargs:
            if kwargs:
                self._process_guid = self._process_guid or kwargs.get("process_guid")
                q = Q(**kwargs)
            if self._query is None:
                self._query = q
            else:
                self._query = self._query & q
        else:
            raise ApiError(".and_() only accepts strings or solrq.Q objects")

        return self

    @_guard_query_params
    def or_(self, q, **kwargs):
        """
        Adds a disjunctive filter to a QueryBuilder.

        Args:
            q (object): Either a string or solrq.Q object representing the query to be added.
            **kwargs (dict): Arguments with which to construct a solrq.Q object.

        Returns:
            QueryBuilder: This object.

        Raises:
            ApiError: If the q parameter is of an invalid type.
        """
        if kwargs:
            self._process_guid = self._process_guid or kwargs.get("process_guid")
            q = Q(**kwargs)

        if isinstance(q, Q):
            if self._query is None:
                self._query = q
            else:
                self._query = self._query | q
        else:
            raise ApiError(".or_() only accepts solrq.Q objects")

        return self

    @_guard_query_params
    def not_(self, q, **kwargs):
        """
        Adds a negative filter to a QueryBuilder.

        Args:
            q (object): Either a string or solrq.Q object representing the query to be added.
            **kwargs (dict): Arguments with which to construct a solrq.Q object.

        Returns:
            QueryBuilder: This object.

        Raises:
            ApiError: If the q parameter is of an invalid type.
        """
        if kwargs:
            q = ~Q(**kwargs)

        if isinstance(q, Q):
            if self._query is None:
                self._query = q
            else:
                self._query = self._query & q
        else:
            raise ApiError(".not_() only accepts solrq.Q objects")

        return self

    def _collapse(self):
        """
        Collapse the query into a single string.

        The query can be represented by either an array of strings (_raw_query) which is concatenated and passed
        directly to Solr, or a solrq.Q object (_query) which is then converted into a string to pass to Solr.
        This function will perform the appropriate conversions to end up with the 'q' string sent into the
        POST request to the Cloud API query endpoint.

        Returns:
            str: The collapsed query.
        """
        if self._raw_query is not None:
            return " ".join(self._raw_query)
        elif self._query is not None:
            return str(self._query)
        else:
            return ""  # return everything


class QueryBuilderSupportMixin:
    """A mixin that supplies wrapper methods to access the _query_builder."""

    def where(self, q=None, **kwargs):
        """
        Add a filter to this query.

        Args:
            q (Any): Query string, :py:class:`QueryBuilder`, or `solrq.Q` object
            **kwargs (dict): Arguments to construct a `solrq.Q` with

        Returns:
            Query: This Query object.
        """
        if isinstance(q, QueryBuilder):
            self._query_builder = q
        else:
            self._query_builder.where(q, **kwargs)
        return self

    def and_(self, q=None, **kwargs):
        """
        Add a conjunctive filter to this query.

        Args:
            q (Any): Query string or `solrq.Q` object
            **kwargs (dict): Arguments to construct a `solrq.Q` with

        Returns:
            Query: This Query object.
        """
        if not q and not kwargs:
            raise ApiError(".and_() expects a string, a solrq.Q, or kwargs")

        self._query_builder.and_(q, **kwargs)
        return self

    def or_(self, q=None, **kwargs):
        """
        Add a disjunctive filter to this query.

        Args:
            q (solrq.Q): Query object.
            **kwargs (dict): Arguments to construct a `solrq.Q` with.

        Returns:
            Query: This Query object.
        """
        if not q and not kwargs:
            raise ApiError(".or_() expects a solrq.Q or kwargs")

        self._query_builder.or_(q, **kwargs)
        return self

    def not_(self, q=None, **kwargs):
        """
        Adds a negated filter to this query.

        Args:
            q (solrq.Q): Query object.
            **kwargs (dict): Arguments to construct a `solrq.Q` with.

        Returns:
            Query: This Query object.
        """
        if not q and not kwargs:
            raise ApiError(".not_() expects a solrq.Q, or kwargs")

        self._query_builder.not_(q, **kwargs)
        return self


class IterableQueryMixin:
    """A mix-in to provide iterability to a query."""

    def all(self):
        """
        Returns all the items of a query as a list.

        Returns:
            list: List of query items
        """
        return self._perform_query()

    def first(self):
        """
        Returns the first item that would be returned as the result of a query.

        Returns:
            obj: First query item
        """
        allres = list(self)
        res = allres[:1]
        if not len(res):
            return None
        return res[0]

    def one(self):
        """
        Returns the only item that would be returned by a query.

        Returns:
            obj: Sole query return item

        Raises:
            MoreThanOneResultError: If the query returns zero items, or more than one item
        """
        allres = list(self)
        res = allres[:2]
        if len(res) == 0:
            raise MoreThanOneResultError(
                message="0 results for query {0:s}".format(self._query)
            )
        if len(res) > 1:
            raise MoreThanOneResultError(
                message="{0:d} results found for query {1:s}".format(
                    len(self), self._query
                )
            )
        return res[0]

    def __len__(self):
        """
        Return the number of objects this query returns.

        Returns:
            int: The number of objects this query returns.
        """
        return self._count()

    def __getitem__(self, item):
        """
        Not implemented.

        Args:
            item (int): Unused.

        Returns:
            None
        """
        return None

    def __iter__(self):
        """
        Returns the iterator for this query.

        Returns:
            Iterator: The iterator for this query.
        """
        return self._perform_query()


class AsyncQueryMixin:
    """A mix-in which provides support for asynchronous queries."""

    def _init_async_query(self):
        """
        Initialize an async query and return a context for running in the background. Optional.

        Returns:
            object: Context for running in the background.
        """
        return None

    def _run_async_query(self, context):
        """
        Executed in the background to run an asynchronous query. Must be implemented in any inheriting classes.

        Args:
            context (object): The context returned by _init_async_query. May be None.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        raise NotImplementedError("must implement _run_async_query for AsyncQueryMixin support")

    def execute_async(self):
        """
        Executes the current query in an asynchronous fashion.

        Returns:
            Future: A future representing the query and its results.
        """
        context = self._init_async_query()
        return self._cb._async_submit(lambda arg, kwarg: arg[0]._run_async_query(arg[1]), self, context)


class FacetQuery(BaseQuery, AsyncQueryMixin, QueryBuilderSupportMixin):
    """Query class for asynchronous Facet API calls.

    These API calls return one result, and are not paginated or iterable.
    """
    def __init__(self, cls, cb, query=None):
        """Initialize the FacetQuery object."""
        super(FacetQuery, self).__init__(query)
        self._doc_class = cls
        self._cb = cb
        self._full_init = False
        self._query_builder = QueryBuilder()

        # unqiue identifier, typically a job id
        self._query_token = None
        # whether self._total_results is a valid value
        self._count_valid = False
        # seconds to wait for num_contacted == num_completed until timing out
        self._timeout = 0
        # whether the query timed-out
        self._timed_out = False
        # query body parameters
        self._time_range = {}
        self._limit = None
        self._criteria = {}
        self._exclusions = {}
        self._facet_fields = []
        self._facet_rows = None
        self._ranges = []
        self._default_args = {}

    def add_criteria(self, key, newlist):
        """Add to the criteria on this query with a custom criteria key.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (str or list[str]): Value or list of values to be set for the criteria item.

        Returns:
            The ResultQuery with specified custom criteria.

        Example:
            query = api.select(Event).add_criteria("event_type", ["filemod", "scriptload"])
            query = api.select(Event).add_criteria("event_type", "filemod")
        """
        if not isinstance(newlist, list):
            if not isinstance(newlist, str):
                raise ApiError("Criteria value(s) must be a string or list of strings. "
                               f"{newlist} is a {type(newlist)}.")
            self._add_criteria(key, [newlist])
        else:
            self._add_criteria(key, newlist)
        return self

    def _add_criteria(self, key, newlist):
        """
        Updates a list of criteria being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the criteria item to be set.
            newlist (list): List of values to be set for the criteria item.
        """
        oldlist = self._criteria.get(key, [])
        self._criteria[key] = oldlist + newlist

    def add_exclusions(self, key, newlist):
        """Add to the excluions on this query with a custom exclusion key.

        Args:
            key (str): The key for the exclusion item to be set.
            newlist (str or list[str]): Value or list of values to be set for the exclusion item.

        Returns:
            The ResultQuery with specified custom exclusion.

        Example:
            query = api.select(Event).add_exclusions("netconn_domain", ["www.google.com"])
            query = api.select(Event).add_exclusions("netconn_domain", "www.google.com")
        """
        if not isinstance(newlist, list):
            if not isinstance(newlist, str):
                raise ApiError("Exclusion value(s) must be a string or list of strings. "
                               f"{newlist} is a {type(newlist)}.")
            self._add_exclusions(key, [newlist])
        else:
            self._add_exclusions(key, newlist)
        return self

    def _add_exclusions(self, key, newlist):
        """
        Updates a list of exclusion being collected for a query, by setting or appending items.

        Args:
            key (str): The key for the exclusion item to be set.
            newlist (list): List of values to be set for the exclusion item.
        """
        oldlist = self._exclusions.get(key, [])
        self._exclusions[key] = oldlist + newlist

    def timeout(self, msecs):
        """Sets the timeout on an AsyncQuery. By default, there is no timeout.

        Arguments:
            msecs (int): Timeout duration, in milliseconds.

        Returns:
            Query (AsyncQuery): The Query object with new milliseconds
                parameter.

        Example:

        >>> cb.select(ProcessFacet).where(process_name="foo.exe").timeout(5000)
        """
        self._timeout = msecs
        return self

    def limit(self, limit):
        """Sets the maximum number of facets per category (i.e. any Process Search Fields in self._fields).

        The default limit for Process Facet searches in the Carbon Black Cloud backend is 100.

        Arguments:
            limit (int): Maximum number of facets per category.

        Returns:
            Query (AsyncQuery): The Query object with new limit parameter.

        Example:
        >>> cb.select(ProcessFacet).where(process_name="foo.exe").limit(50)
        """
        self._limit = limit
        return self

    def set_rows(self, rows):
        """Sets the number of facet results to return with the query.

        Args:
            rows (int): Number of rows to return.

        Returns:
            Query (AsyncQuery): The Query object with the new rows parameter.

        Example:
        >>> cb.select(ProcessFacet).set_rows(50)
        """
        self._facet_rows = rows
        return self

    def add_facet_field(self, field):
        """Sets the facet fields to be received by this query.

        Arguments:
            field (str or [str]): Field(s) to be received.

        Returns:
            Query (AsyncQuery): The Query object that will receive the specified field(s).

        Example:
        >>> cb.select(ProcessFacet).add_facet_field(["process_name", "process_username"])
        """
        if isinstance(field, str):
            self._facet_fields.append(field)
        else:
            for name in field:
                self._facet_fields.append(name)
        return self

    def _check_range(self, range):
        """Checks if range has all required keys, and that they have non-empty values."""
        start = range.get("start")
        end = range.get("end")
        field = range.get("field")
        bucket_size = range.get("bucket_size")

        if start is None or (start != 0 and not start):
            raise ApiError("No 'start' parameter in range, or its value is None.")
        if end is None or not end:
            raise ApiError("No 'end' parameter in range, or its value is None.")
        if bucket_size is None or not bucket_size:
            raise ApiError("No 'bucket_size' parameter in range, or its value is None.")
        if field is None or not field:
            raise ApiError("No 'field' parameter in range, or its value is None.")

        if type(start) not in [int, str]:
            raise ApiError("`start` parameter should be either int or ISO8601 timestamp string")
        if type(end) not in [int, str]:
            raise ApiError("`end` parameter should be either int or ISO8601 timestamp string")
        if type(field) not in [str]:
            raise ApiError("`field` parameter should be a string")
        if type(bucket_size) not in [int, str]:
            raise ApiError("`bucket_size` should be either int or ISO8601 timestamp string")

    def add_range(self, range):
        """Sets the facet ranges to be received by this query.

        Arguments:
            range (dict or [dict]): Range(s) to be received.

        Returns:
            Query (AsyncQuery): The Query object that will receive the specified range(s).

        Note: The range parameter must be in this dictionary format:
            {
                "bucket_size": "<object>",
                "start": "<object>",
                "end": "<object>",
                "field": "<string>"
            },
            where "bucket_size", "start", and "end" can be numbers or ISO 8601 timestamps.

        Examples:
        >>> cb.select(ProcessFacet).add_range({"bucket_size": 5, "start": 0, "end": 10, "field": "netconn_count"})
        >>> cb.select(ProcessFacet).add_range({"bucket_size": "+1DAY", "start": "2020-11-01T00:00:00Z",
                                               "end": "2020-11-12T00:00:00Z", "field": "backend_timestamp"})
        """
        if isinstance(range, dict):
            self._check_range(range)
            self._ranges.append(range)
        else:
            for r in range:
                self._check_range(r)
                self._ranges.append(r)
        return self

    def set_time_range(self, start=None, end=None, window=None):
        """
        Sets the 'time_range' query body parameter, determining a time window based on 'device_timestamp'.

        Args:
            start (str in ISO 8601 timestamp): When to start the result search.
            end (str in ISO 8601 timestamp): When to end the result search.
            window (str): Time window to execute the result search, ending on the current time.
                Should be in the form "-2w", where y=year, w=week, d=day, h=hour, m=minute, s=second.

        Note:
            - `window` will take precendent over `start` and `end` if provided.

        Examples:
            query = api.select(Event).set_time_range(start="2020-10-20T20:34:07Z")
            second_query = api.select(Event).set_time_range(start="2020-10-20T20:34:07Z", end="2020-10-30T20:34:07Z")
            third_query = api.select(Event).set_time_range(window='-3d')
        """
        if start:
            if not isinstance(start, str):
                raise ApiError(f"Start time must be a string in ISO 8601 format. {start} is a {type(start)}.")
            self._time_range["start"] = start
        if end:
            if not isinstance(end, str):
                raise ApiError(f"End time must be a string in ISO 8601 format. {end} is a {type(end)}.")
            self._time_range["end"] = end
        if window:
            if not isinstance(window, str):
                raise ApiError(f"Window must be a string. {window} is a {type(window)}.")
            self._time_range["window"] = window
        return self

    def _get_query_parameters(self):
        args = self._default_args.copy()
        if not (self._facet_fields or self._ranges):
            raise ApiError("Process Facet Queries require at least one field or range to be requested. "
                           "Use add_facet_field(['my_facet_field']) to add fields to the request, "
                           "or use add_range({}) to add ranges to the request.")
        terms = {}
        if self._facet_fields:
            terms["fields"] = self._facet_fields
        if self._facet_rows:
            terms["rows"] = self._facet_rows
        args["terms"] = terms
        if self._ranges:
            args["ranges"] = self._ranges
        if self._criteria:
            args["criteria"] = self._criteria
        if self._exclusions:
            args["exclusions"] = self._exclusions
        if self._time_range:
            args["time_range"] = self._time_range
        query = self._query_builder._collapse()
        if query:
            args['query'] = query
        return args

    def _submit(self):
        if self._query_token:
            raise ApiError(f"Query already submitted: token {self._query_token}")

        args = self._get_query_parameters()
        self._validate(args)

        submit_url = self._doc_class.submit_url.format(self._cb.credentials.org_key)
        query_start = self._cb.post_object(submit_url, body=args)

        self._query_token = query_start.json().get("job_id")

        self._timed_out = False
        self._submit_time = time.time() * 1000

    def _still_querying(self):
        if not self._query_token:
            self._submit()

        result_url = self._doc_class.result_url.format(self._cb.credentials.org_key, self._query_token)
        result = self._cb.get_object(result_url)

        searchers_contacted = result.get("contacted", 0)
        searchers_completed = result.get("completed", 0)
        log.debug("contacted = {}, completed = {}".format(searchers_contacted, searchers_completed))
        if searchers_contacted == 0:
            return True
        if searchers_completed < searchers_contacted:
            if self._timeout != 0 and (time.time() * 1000) - self._submit_time > self._timeout:
                self._timed_out = True
                return False
            return True

        return False

    def _count(self):
        if self._count_valid:
            return self._total_results

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="user-specified timeout exceeded while waiting for results")

        result_url = self._doc_class.result_url.format(self._cb.credentials.org_key, self._query_token)
        result = self._cb.get_object(result_url)

        self._total_results = result.get('num_found', 0)
        self._count_valid = True

        return self._total_results

    def _validate(self, args):
        if not hasattr(self._doc_class, "validation_url"):
            return

        url = self._doc_class.validation_url.format(self._cb.credentials.org_key)

        if args.get('query', False):
            args['q'] = args['query']

        # v2 search sort key does not work with v1 validation
        args.pop('sort', None)

        validated = self._cb.get_object(url, query_parameters=args)

        if not validated.get("valid"):
            raise ApiError("Invalid query: {}: {}".format(args, validated["invalid_message"]))

    def _search(self, start=0, rows=0):
        """Execute the query, with one expected result."""
        if not self._query_token:
            self._submit()

        while self._still_querying():
            time.sleep(.5)

        if self._timed_out:
            raise TimeoutError(message="User-specified timeout exceeded while waiting for results")

        log.debug(f"Pulling results, timed_out={self._timed_out}")

        result_url = self._doc_class.result_url.format(self._cb.credentials.org_key, self._query_token)
        if self._limit:
            query_parameters = {"limit": self._limit}
        else:
            query_parameters = {}

        result = self._cb.get_object(result_url, query_parameters=query_parameters)
        yield self._doc_class(self._cb, model_unique_id=self._query_token, initial_data=result)

    def _perform_query(self):
        for item in self.results:
            yield item

    @property
    def results(self):
        """Save query results to self._results with self._search() method."""
        if not self._full_init:
            for item in self._search():
                self._results = item
            self._full_init = True

        return self._results

    def _init_async_query(self):
        """Initialize an async query and return a context for running in the background.

        Returns:
            object: Context for running in the background (the query token).
        """
        self._submit()
        return self._query_token

    def _run_async_query(self, context):
        """Executed in the background to run an asynchronous query.

        Args:
            context (object): The context (query token) returned by _init_async_query.

        Returns:
            Any: Result of the async query, which is then returned by the future.
        """
        if context != self._query_token:
            raise ApiError("Async query not properly started")
        return list(self._search())
