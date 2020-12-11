Porting Applications from CBAPI to Carbon Black Cloud SDK
=========================================================
Applications using the Carbon Black Cloud via the CBAPI can be ported to use the Carbon Black Cloud SDK.  CBAPI
applications using CB Protection or CB Response cannot be ported, as support for on-premise products is not present in
the CBC SDK.

Import Changes
--------------
A number of packages have new name equivalents in the CBC SDK.

* Package ``cbapi.example_helpers`` -> ``cbc_sdk.helpers``
* Package ``cbapi.psc`` -> ``cbc_sdk``
* Package ``cbapi.psc.alerts_query`` -> ``cbc_sdk.platform``
* Package ``cbapi.psc.devices_query`` -> ``cbc_sdk.platform``
* Package ``cbapi.psc.livequery`` -> ``cbc_sdk.audit_remediation``
* Package ``cbapi.psc.livequery.models`` -> ``cbc_sdk.audit_remediation``
* Package ``cbapi.psc.defense`` -> ``cbc_sdk.endpoint_standard``
* Package ``cbapi.psc.defense.models`` -> ``cbc_sdk.endpoint_standard``
* Package ``cbapi.psc.threathunter`` -> ``cbc_sdk.enterprise_edr``
* Package ``cbapi.psc.threathunter.models`` -> ``cbc_sdk.enterprise_edr``

Code Changes
------------
**Helper Functions:** Replace all calls to ``get_cb_defense_object()``, ``get_cb_livequery_object()``,
``get_cb_psc_object()``, and ``get_cb_threathunter_object()`` with ``get_cb_cloud_object()``.

**Audit/Remediation Queries:**

* Replace ``cb.query(sql_query)`` with ``cb.select(Run).where(sql=sql_query)``.
* Replace ``cb.query_history(query_string)`` with ``cb.select(RunHistory).where(query_string)``.
* On a query object, use the ``policy_id()`` method instead of ``policy_ids()``.  Only one policy ID can be specified.

**Base API Object**

The different API objects, ``CbDefenseAPI``, ``CbLiveQueryAPI``, ``CbPSCBaseAPI``, and ``CbThreatHunterAPI`` are
replaced with ``CBCloudAPI``.  Import this object from the ``cbc_sdk`` package, i.e. ``from cbc_sdk import CBCloudAPI``.

**Enterprise EDR Process and Event Search replaced with Platform Search**

CBAPI used the ``threathunter`` (Enterprise EDR) package for Process and Event searches. Platform search is replacing these APIs,
so the SDK now uses the ``platform`` package to handle Process and Event searches.

* ``threathunter.Process`` -> ``platform.Process``
* ``threathunter.Event`` -> ``platform.Event``

Additionally, Process Summaries and Trees now use the same API route, with the addition of a ``?format=tree``
query parameter to differentiate the two. Therefore, Process Trees have been integrated into the Process class.

* ``threathunter.Tree`` -> ``platform.Process.Tree``
