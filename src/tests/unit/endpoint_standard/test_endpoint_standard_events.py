"""Testing Event object of cbc_sdk.endpoint_standard"""

import pytest
import logging
from cbc_sdk.endpoint_standard import Event
from cbc_sdk.errors import FunctionalityDecommissioned
from cbc_sdk.rest_api import CBCloudAPI

log = logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='log.txt')


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


# ==================================== UNIT TESTS BELOW ====================================

def test_event_query_decommissioned(cb):
    """Testing Event Querying has been decommissioned."""
    with pytest.raises(FunctionalityDecommissioned):
        Event(cb, 1234)
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(Event).where('hostNameExact:Win7x64')
    with pytest.raises(FunctionalityDecommissioned):
        cb.select(Event, 'a1e12604d67b11ea920d3d9192a785d1')
