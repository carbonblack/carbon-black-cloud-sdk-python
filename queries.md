************************************************************************************************************************
Base
************************************************************************************************************************


""""""""""""""""""""
BaseQuery
""""""""""""""""""""

__init__()  =>  self._query = query

_clone() =>  return self.__class__(self._query)

all()  => self._perform_query()

_perform_query()  =>  return; yield (empty generator)

first()  => return self[:1][0]

one()  =>  return self[:2][0]; makes sure the slice up to 2 is one long

__len__()  =>  return 0 (will be overwritten, maybe should be NotImplementedError?)

__getitem__()  =>  return None (will be overwritten, maybe should be NotImplementedError?)



""""""""""""""""""""
SimpleQuery (BaseQuery)

compared to BaseQuery
""""""""""""""""""""


__init__()  =>  

    Not New Attr:

    - super()
    - self._query = {}

    New Attr:

    + self._doc_class = cls
    + self._urlobject = urlobject (else cls.urlobject)
    + self._cb
    + self._full_init = False
    + self._results = []
    + self._sort_by = None
    + self._returns_full_doc = (default) True

Not New Methods:

    - _clone()  =>  essentially same as BaseQuery._clone()

New Methods:

    + _match_query(i)  =>  compare i with self._query; return Bool

    + _sort(result_set)  =>  sort a result set

    + @property
    + results()  =>  return self._results (fully initialized)

    + __len__()  =>  return len(self.results)

    + __getitem__(item)  =>  return self.results[item] (slice or int)

    + where(new_query)  =>  return clone with additional key, value in self._query

    + and_(new_query)  =>  where(new_query)

    + _perform_query()  =>  yield item for item in self.results

    + sort(new_sort_key)  =>  clone the query with a new self._sort_by key


""""""""""""""""""""
PaginatedQuery (BaseQuery)

compared to BaseQuery
""""""""""""""""""""


__init__()  =>

    Not New Attr:

    - super(Query=None)


    New Attr:

    + self._doc_class = cls
    + self._cb
    + self._total_results = 0
    + self._count_valid = False
    + self._batch_size = 100

Not New Methods:

    - self._clone()  =>  essentially same as BaseQuery._clone(), with a batch_size Attr

New Methods:

    + __getitem__(item)  =>  _perform_query(item, numrows)
    + _perform_query(start=0, numrows=0)  =>  for item in _search(item), yield new class object
    + batch_size(new_batch_size)  =>  clone with new self._batch_size


""""""""""""""""""""
QueryBuilder (object)
""""""""""""""""""""


__init__()  =>

Makes a SolrQ query object, either raw string or Q

self._query = Q(**kwargs), or
self._query = None if not kwargs
self._raw_query = None
self._process_guid = None

_guard_query_params()  =>  enforces either a raw query or Q query

where()
and_()
or_()
not_()
_collapse()  =>  convert self._query or self._raw_query into a solr string



************************************************************************************************************************
Defense
************************************************************************************************************************


""""""""""""""""""""
Defense Query(PaginatedQuery)

compared to PaginatedQuery, BaseQuery
""""""""""""""""""""


__init__()  =>

    Not New Attr:

    - super(Query, self).__init__(doc_class, cb, query=None)
    - self._sort_by = None
    - self._group_by = None
    - self._batch_size = 100

    New Attr:

    + self._query = [query] or [] {converted to a list now}
    + self._sort_by = None
    + self._group_by = None

Not New Methods:

- self._clone()  =>  essentially same as BaseQuery._clone(), with a _batch_size, _sort_by, _group_by Attrs

New Methods:

+ where(query)  =>  _clone() then appends to self._query list
+ and_()  =>  pass thru to where()
+ prepare_query(args)  =>  adds key, value pairs in self._query to args dictionary input
+ _count()  =>  return int(GET_REQUEST_WITH_ARGS.get("totalResults"))
+ _search(start=0, rows=0)  =>  yield results from GET_REQUEST_WITH_ARGS _batch_size at a time, up to 100k

GET_REQUEST_WITH_ARGS == self._cb.get_object(self._doc_class.urlobject, query_parameters=query_args)



************************************************************************************************************************
Platform Base
************************************************************************************************************************


""""""""""""""""""""
Platform QueryBuilder(object)

compared to Base QueryBuilder(object)
""""""""""""""""""""

No self._process_guid

self._collapse() may return None instead of "*:*"

Otherwise identical


""""""""""""""""""""
PSCQueryBase "Represents the base of all LiveQuery query classes."
""""""""""""""""""""

self._doc_class
self._cb
self._count_valid = False


""""""""""""""""""""
QueryBuilderSuportMixin "A mixin that supplies wrapper methods to access the _query_builder."
""""""""""""""""""""

Adds access to the _query_builder for objects that inherit this class


""""""""""""""""""""
IterableQueryMixin "A mix-in to provide iterability to a query."
""""""""""""""""""""

Adds the following methods:

- all()
- first()
- one()
- __len__()
- __getitem__()
- __iter_()


************************************************************************************************************************
Platform Devices
************************************************************************************************************************


""""""""""""""""""""
DeviceSearchQuery(PSCQueryBase, QueryBuilderSuportMixin, IterableQueryMixin)
""""""""""""""""""""

Many many different device-specific methods



************************************************************************************************************************
Platform Alerts
************************************************************************************************************************

So many additions, it makes sense to keep all of them in Alerts


""""""""""""""""""""
BaseAlertSearchQuery(PSCQueryBase, QueryBuilderSuportMixin, IterableQueryMixin)
""""""""""""""""""""


""""""""""""""""""""
WatchlistAlertSearchQuery(BaseAlertSearchQuery)
""""""""""""""""""""


""""""""""""""""""""
CBAnalyticsAlertSearchQuery(BaseAlertSearchQuery)
""""""""""""""""""""


""""""""""""""""""""
VMwareAlertSearchQuery(BaseAlertSearchQuery)
""""""""""""""""""""



************************************************************************************************************************
LiveQuery
************************************************************************************************************************


""""""""""""""""""""
RunQuery(PSCQueryBase) "Represents a query that either creates or retrieves the
    status of a LiveQuery run."

compared to Platform PSCQueryBase
""""""""""""""""""""

- super().__init__(doc_class, cb)

    New Attrs:

    + self._query_token = None
    + self._query_body = {"device_filter": {}}
    + self._device_filter = self._query_body["device_filter"]


New Methods:

+ device_ids(input_device_ids)  =>  self._device_filter["device_ids"] = input_device_ids
+ device_types(input_device_types)  =>  self._device_filter["device_types"] = input_device_types
+ policy_ids(input_policy_ids)  =>  self._device_filter["policy_ids"] = input_policy_ids
+ where(sql)  =>  self._query_body["sql"] = sql
+ name(name)  =>  self._query_body["name"] = name
+ notify_on_finish()  =>  self._query_body["notify_on_finish"] = True
+ submit()  =>  creates a new Run() instance with the response from POSTing


""""""""""""""""""""
RunHistoryQuery(PSCQueryBase, QueryBuilderSupportMixin, IterableQueryMixin) "Represents a query that retrieves historic LiveQuery runs."

compared to PSCQueryBase, QueryBuilderSupportMixin, IterableQueryMixin
""""""""""""""""""""

- super().__init(doc_class, cb)

    New Attrs:

    - self._query_builder = QueryBuilder {Platform}
    - self._sort = {}

New Methods:

+ sort_by(key, direction="ASC")  =>  self._sort.update({"field": key, "order": direction})
+ _build_request(start, rows)  =>  return "request" dict with ["query"], ["rows"], ["sort"], query from self._query_builder._collapse()
+ _count()  =>  return self._total_results or result["num_found"] from POSTing the query, set self._count_valid = True
+ _perform_query(start=0, rows=0)  =>  yield item for item in results, with no batch_size set



************************************************************************************************************************
ThreatHunter
************************************************************************************************************************


""""""""""""""""""""
Query(PaginatedQuery)

compared to PaginatedQuery
""""""""""""""""""""

- super().__init__(doc_class, cb)

    New Attrs:

    + self._query_builder = QueryBuilder {Base}
    + self._sort_by
    + self._group_by
    + self._batch_size = 100
    + self._default_args = {}

New Methods:

    + where(q=None, **kwargs)  =>  self._query_builder.where(q, **kwargs)
    + and_(q=None, **kwargs)  =>  self._query_builder.and_(q, **kwargs)
    + or_(q=None, **kwargs)  =>  self._query_builder.or_(q, **kwargs)
    + not_(q=None, **kwargs)  =>  self._query_builder.not_(q, **kwargs)
    + _get_query_parameters()  =>  builds args dict with ['query'] and ['fields'] keys
    + _count()  =>  returns 'num_available' from result of POSTing a request
    + _validate(args)  =>  uses v1 validation route (removes ['sort'] key)
    + _search(start=0, rows=0)  =>  yield item for item in result of POSTing a request, 100 at a time. Saves self._total_results (num_available), self._total_segments, self._processed_segments, self._count_valid = True



""""""""""""""""""""
AsyncProcessQuery(Query)

compared to ThreatHunter Query
""""""""""""""""""""

- super(AsyncProcessQuery, self).__init__(doc_class, cb)

    New Attrs:

    + self._query_token = None
    + self._timeout = 0
    + self._timed_out = False
    + self._sort = []

New Methods:

    + sort_by(key, direction="ASC")  =>  if key not in self._sort, add it: self._sort.append({'field': key, 'order': direction}). Then, self._default_args['sort'] = self._sort
    + timeout(msecs)  =>  self._timeout = msecs
    + _submit()  =>  POST to /processes/search_jobs, assign "job_id" to self._query_token, create self._submit_time = time.time() * 1000
    + _still_querying()  =>  GET to /processes/search_jobs/`job_id`, compare contacted to completed
    + _count()  =>  GET to processes/search_jobs/`job_id`/results, return 'num_available'
    + _search(start=0, rows=0)  =>  yield item for item in results of GET to /results, batches of 10 (!!)



""""""""""""""""""""
TreeQuery(BaseQuery)

compared to Base BaseQuery
""""""""""""""""""""

- super(TreeQuery, self).__init__()

    New Attrs:

    + self._doc_class
    + self._cb
    + self._args = {}

New Methods:

    + where(**kwargs)  =>  self._args = dict(self._args, **kwargs)
    + and_(**kwargs)  =>  self.where(**kwargs)
    + or_(**kwargs)  =>  raise ApiError(".or_() cannot be called on Tree queries")
    + _perform_query()  =>  return results of GET request to /processes/tree



""""""""""""""""""""
FeedQuery(SimpleQuery)

compared to Base SimpleQuery
""""""""""""""""""""

- super(FeedQuery, self).__init__(doc_class, cb)

    New Attrs:

    + self._args = {}

New Methods:

    + where(**kwargs)  =>  self._args = dict(self._args, **kwargs)
    + @property
    + results()  =>  return list of Feeds matching self._args



""""""""""""""""""""
ReportQuery(SimpleQuery)

compared to Base SimpleQuery
""""""""""""""""""""

- super(ReportQuery, self).__init__(doc_class, cb)

New Attrs:

    + self._args = {}

New Methods:

    + where(**kwargs)  =>  self._args = dict(self._args, **kwargs)
    + @property
    + results()  =>  return list of Reports from Feed self._args["feed_id"] matching self._args



""""""""""""""""""""
WatchlistQuery(SimpleQuery)

compared to Base SimpleQuery
""""""""""""""""""""

- super(WatchlistQuery, self).__init__(doc_class, cb)

New Methods:

    + @property
    + results()  =>  return list of all Watchlists
