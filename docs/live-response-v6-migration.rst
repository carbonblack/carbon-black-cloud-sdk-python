Migration Guide For Live Response From v3 To v6
=========================================================
This guide will help you migrate from Live Response v3 to v6.

Overview
--------
Most of the changes from v3 to v6 are on the routes. Thе updated API (v6) includes a more granular approach to roles-based access
control (RBAC).

This change was implemented in CBC SDK 1.3.0, Released June 8, 2021.  If you are on a more recent version of this SDK,
you are already using the new version.

Access Permissions
------------------
A key wth a Custom Access Level with appropriate permissions needs to be created for the Live Response. The following
table shows the corresponding permissions that needs to be enabled, based on the existing roles.

+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
|        Permission         |           What it controls (commands)                                         |  Which existing roles have access  |
+===========================+===============================================================================+====================================+
|     org.liveresponse      | | Permanently disabling the Live Response feature on an individual endpoint:  | | Level 3 Analyst                  |
|                           | | Disable Live Response on the Endpoints page                                 | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
|  org.liveresponse.files   | | Read, write and/or delete files on the endpoint:                            | | Level 2 Analyst                  |
|                           | | cd, delete, dir, drives, get, mkdir, put, pwd                               | | Level 3 Analyst                  |
|                           |                                                                               | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
| org.liveresponse.memdump  | | Dump kernel memory on the endpoint:                                         | | Level 3 Analyst                  |
|                           | | memdump                                                                     | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
| org.liveresponse.process  | | List, stop and execute  processes on the endpoint:                          | | Level 2 Analyst (cannot execute) |
|                           | | exec, execfg, kill, ps                                                      | | Level 3 Analyst                  |
|                           |                                                                               | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
| org.liveresponse.registry | | View, add, edit and delete registry entries:                                | | Level 2 Analyst                  |
|                           | | reg add, reg delete, reg query, reg set                                     | | Level 3 Analyst                  |
|                           |                                                                               | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+
| org.liveresponse.session  | | Initiate live response sessions, plus:                                      | | Level 2 Analyst                  |
|                           | | clear, help                                                                 | | Level 3 Analyst                  |
|                           |                                                                               | | Live Response Admin - Legacy     |
|                           |                                                                               | | Super Admin                      |
+---------------------------+-------------------------------------------------------------------------------+------------------------------------+


Changes in the routes and response codes
----------------------------------------

+-----------------------------------------------------------+---------------------------------------------------------+
| v3                                                        | v6                                                      |
+===========================================================+=========================================================+
| /integrationServices/v3/cblr/                             | /appservices/v6/orgs/{org_key}/liveresponse/            |
+-----------------------------------------------------------+---------------------------------------------------------+
| POST /sessions/{session_id} 200                           | POST /sessions 201                                      |
+-----------------------------------------------------------+---------------------------------------------------------+
| POST /session/{session_id)/file    200                    | POST /sessions/{session_id)/files 201                   |
+-----------------------------------------------------------+---------------------------------------------------------+
| POST /session/{session_id}/command                        | POST /sessions/{session_id}/commands                    |
+-----------------------------------------------------------+---------------------------------------------------------+
| PUT /session {"session_id": "1:37191", "status": "CLOSE"} | DELETE /sessions/{session_id} 204                       |
+-----------------------------------------------------------+---------------------------------------------------------+
| GET /session/{sessionId}/file/{fileId}/content   200      | GET /sessions/{session_id}/files/{file_id}/content 302  |
+-----------------------------------------------------------+---------------------------------------------------------+
| DELETE /session/{sessionId}/file/{fileId} 200             | DELETE /sessions/{session_id}/files/{file_id} 204       |
+-----------------------------------------------------------+---------------------------------------------------------+


Changes in some of the request/response fields
----------------------------------------------

+----------------------+------------------+------------------+
| Where is the change? | v3               | v6               |
+======================+==================+==================+
| All API endpoints    | sensor_id        | device_id        |
+----------------------+------------------+------------------+
| Process command      | username         | process_username |
+----------------------+------------------+------------------+
| Process command      | path             | process_path     |
+----------------------+------------------+------------------+
| Process command      | pid              | process_pid      |
+----------------------+------------------+------------------+
| Process command      | command_line     | process_cmdline  |
+----------------------+------------------+------------------+
| Process command      | parent           | parent_pid       |
+----------------------+------------------+------------------+
| Registry command     | valueType        | value_type       |
+----------------------+------------------+------------------+
| Registry command     | valueData        | value_data       |
+----------------------+------------------+------------------+
| Registry command     | valueName        | value_name       |
+----------------------+------------------+------------------+


Additional Information
----------------------

* `(CBC) Live Response API releasing v6: now with granular RBAC! <https://community.carbonblack.com/t5/Developer-Relations/CBC-Live-Response-API-releasing-v6-now-with-granular-RBAC/m-p/102358/thread-id/2595>`_
* `Live Response Documentation <https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/live-response-api/>`_
* `Live Response API Migration Guide <https://developer.carbonblack.com/reference/carbon-black-cloud/guides/api-migration/live-response-migration/>`_
