Porting Applications from CBAPI to Carbon Black Cloud SDK
=========================================================
Applications using the Carbon Black Cloud via the CBAPI can be ported to use the Carbon Black Cloud SDK.  CBAPI
applications using CB Protection or CB Response cannot be ported, as support for on-premise products is not present in
the CBC SDK.

Import Changes
--------------
A number of packages have new name equivalents in the CBC SDK.

* Package ``cbapi.example_helpers`` -> ``cbc_sdk.example_helpers``
* Package ``cbapi.psc`` -> ``cbc_sdk.platform``
* Package ``cbapi.psc.livequery`` -> ``cbc_sdk.audit_remediation``
* Package ``cbapi.psc.livequery.models`` -> ``cbc_sdk.audit_remediation.base``
* Package ``cbapi.psc.defense`` -> ``cbc_sdk.endpoint_standard``
* Package ``cbapi.psc.defense.models`` -> ``cbc_sdk.endpoint_standard.base``
* Package ``cbapi.psc.threathunter.models`` -> ``cbc_sdk.enterprise_edr.threat_intelligence``

Code Changes
------------
**Helper Functions:** Replace all calls to ``get_cb_defense_object()``, ``get_cb_livequery_object()``,
``get_cb_psc_object()``, and ``get_cb_threathunter_object()`` with ``get_cb_cloud_object()``.

**Audit/Remediation Queries:**

* Replace ``cb.query(sql_query)`` with ``cb.select(Run).where(sql=sql_query)``.
* Replace ``cb.query_history(query_string)`` with ``cb.select(RunHistory).where(query_string)``.
* On a query object, use the ``policy_id()`` method instead of ``policy_ids()``.  Only one policy ID can be specified.
