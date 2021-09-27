import sys
from cbc_sdk.enterprise_edr import Feed, Report, Watchlist, WatchlistQuery
from cbc_sdk.helpers import eprint, build_cli_parser, get_cb_cloud_object
import json

from cbc_sdk import CBCloudAPI
api = CBCloudAPI(profile='default')

# >>> from cbc_sdk.enterprise_edr import Report, IOC_V2
# >>> builder = Report.create(api, "Unsigned Browsers", "Unsigned processes impersonating browsers", 5)
# >>> builder.add_tag("compliance").add_tag("unsigned_browsers")
# >>> builder.add_ioc(IOC_V2.create_query(api, "unsigned-chrome",
# ...                 "process_name:chrome.exe NOT process_publisher_state:FILE_SIGNATURE_STATE_SIGNED"))
# >>> report = builder.build()
# >>> report.save_watchlist()

watchlists = WatchlistQuery(Watchlist, api)

# watchlist = watchlists[2]
# print(">>> " + watchlist.name)

for watchlist in watchlists:
    for report_id in watchlist.report_ids:
        if report_id == "GUmF3BmITp2lLYA7YKKLeA":
            print(watchlist.name)
            print(watchlist.reports)

            # report = Report.get(api, report_id)
            # print(">>> Report named " + report.name)

            # report = watchlist.reports where report.id
            
            # report_list = [report for report in watchlist.reports where report.id == report_id]
