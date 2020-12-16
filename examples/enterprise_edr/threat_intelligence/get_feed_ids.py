"""Lists Enterprise EDR Feed IDs available for results dispatch."""

from cbc_sdk import CBCloudAPI
from cbc_sdk.enterprise_edr import Feed
import logging

log = logging.getLogger(__name__)


def get_feed_ids():
    """Read and log all the feed IDs from the default server."""
    cb = CBCloudAPI()
    feeds = cb.select(Feed)
    if not feeds:
        log.info("No feeds are available for the org key {}".format(cb.credentials.org_key))
    else:
        for feed in feeds:
            log.info("Feed name: {:<20} \t Feed ID: {:>20}".format(feed.name, feed.id))


if __name__ == '__main__':
    get_feed_ids()
