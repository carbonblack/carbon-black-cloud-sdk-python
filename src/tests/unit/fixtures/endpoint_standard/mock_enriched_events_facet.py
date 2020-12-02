POST_ENRICHED_EVENTS_FACET_SEARCH_JOB_RESP = {
    'job_id': '08ffa932-b633-4107-ba56-8741e929e48b'
}

GET_ENRICHED_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_1 = {
    'ranges': [
                {
                    "start": "2020-08-04T08:01:32.077Z",
                    "end": "2020-08-05T08:01:32.077Z",
                    "bucket_size": "+1HOUR",
                    "field": "device_timestamp",
                    "values": [
                                {
                                    "total": 456,
                                    "name": "2020-08-04T08:01:32.077Z"
                                }
                              ]
                 }
              ], 
    'terms': [
                {
                    'values': [
                                {'total': 116, 
                                 'id': 'chrome.exe', 
                                 'name': 'chrome.exe'
                                }
                              ], 
                    'field': 'process_name'
                 }
              ],
     'num_found': 116, 
     'contacted': 34, 
     'completed': 34
}

GET_ENRICHED_EVENTS_FACET_SEARCH_JOB_RESULTS_RESP_2 = {
    'ranges': [], 
    'terms': [
                {
                    'values': [
                                {'total': 116, 
                                 'id': 'chrome.exe', 
                                 'name': 'chrome.exe'
                                }
                              ], 
                    'field': 'process_name'
                 }
              ],
     'num_found': 116, 
     'contacted': 34, 
     'completed': 34

}


