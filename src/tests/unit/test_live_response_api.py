# *******************************************************
# Copyright (c) VMware, Inc. 2020-2022. All Rights Reserved.
# SPDX-License-Identifier: MIT
# *******************************************************
# *
# * DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
# * WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
# * EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
# * WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
# * NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.

"""Tests for the Live Response API."""

import mox as pymox
import pytest
import copy
import io
from queue import Queue
from cbc_sdk.errors import ApiError, ObjectNotFoundError, ServerError, TimeoutError
from cbc_sdk.live_response_api import (LiveResponseError, LiveResponseSessionManager, CbLRManagerBase,
                                       CompletionNotification, WorkItem, WorkerStatus, JobWorker, GetFileJob,
                                       LiveResponseJobScheduler)
from cbc_sdk.connection import Connection
from cbc_sdk.credentials import Credentials
from cbc_sdk.platform import Device
from cbc_sdk.winerror import HRESULT_FROM_WIN32, Win32Error
from cbc_sdk.rest_api import CBCloudAPI
from tests.unit.fixtures.CBCSDKMock import CBCSDKMock
from tests.unit.fixtures.live_response.mock_command import (DIRECTORY_LIST_START_RESP,
                                                            DIRECTORY_LIST_END_RESP,
                                                            DELETE_FILE_START_RESP,
                                                            DELETE_FILE_END_RESP,
                                                            DELETE_FILE_ERROR_RESP,
                                                            PUT_FILE_START_RESP,
                                                            PUT_FILE_END_RESP,
                                                            CREATE_DIRECTORY_START_RESP,
                                                            GET_FILE_COMMAND_RESP,
                                                            GET_FILE_END_RESP,
                                                            CREATE_DIRECTORY_END_RESP,
                                                            WALK_RETURN_1,
                                                            WALK_RETURN_2,
                                                            WALK_RETURN_3,
                                                            KILL_PROC_START_RESP,
                                                            KILL_PROC_END_RESP,
                                                            CREATE_PROC_START_RESP,
                                                            CREATE_PROC_END_RESP,
                                                            RUN_PROC_START_RESP,
                                                            RUN_PROC_END_RESP,
                                                            LIST_PROC_START_RESP,
                                                            LIST_PROC_END_RESP,
                                                            REG_ENUM_START_RESP,
                                                            REG_ENUM_END_RESP,
                                                            REG_GET_START_RESP,
                                                            REG_GET_END_RESP,
                                                            REG_SET_START_RESP,
                                                            REG_SET_END_RESP,
                                                            REG_CREATE_KEY_START_RESP,
                                                            REG_CREATE_KEY_END_RESP,
                                                            REG_DELETE_KEY_START_RESP,
                                                            REG_DELETE_KEY_END_RESP,
                                                            REG_DELETE_START_RESP,
                                                            REG_DELETE_END_RESP,
                                                            MEMDUMP_START_RESP,
                                                            MEMDUMP_END_RESP,
                                                            MEMDUMP_DEL_START_RESP,
                                                            MEMDUMP_DEL_END_RESP,
                                                            GET_FILE_CANCELLED_RESP)
from tests.unit.fixtures.live_response.mock_device import DEVICE_RESPONSE, UDEVICE_RESPONSE, POST_DEVICE_SEARCH_RESP
from tests.unit.fixtures.live_response.mock_session import (SESSION_INIT_RESP, SESSION_POLL_RESP,
                                                            SESSION_POLL_RESP_ERROR, USESSION_INIT_RESP,
                                                            USESSION_POLL_RESP)


@pytest.fixture(scope="function")
def cb():
    """Create CBCloudAPI singleton"""
    return CBCloudAPI(url="https://example.com",
                      org_key="test",
                      token="abcd/1234",
                      ssl_verify=False)


@pytest.fixture(scope="function")
def cbcsdk_mock(monkeypatch, cb):
    """Mocks CBC SDK for unit tests"""
    return CBCSDKMock(monkeypatch, cb)


class MockRawFile:
    """Class to mock a raw file response"""
    @property
    def raw(self):
        """Raw property"""
        return io.StringIO('This is a test')


def get_file_content(url, stream=True):
    """Replacement function for the Connection.get"""
    return MockRawFile()


@pytest.fixture(scope="function")
def connection_mock(monkeypatch, cb):
    """Mocks Connection for unit tests"""
    creds = Credentials({'url': 'https://example.com', 'token': 'ABCDEFGH'})
    conn = Connection(creds)
    monkeypatch.setattr(conn, "get", get_file_content)
    cb.session = conn
    return conn


FILE_NOT_FOUND_ERR = {'status': 'ERROR', 'result_type': 'WinHresult',
                      'result_code': HRESULT_FROM_WIN32(Win32Error.ERROR_FILE_NOT_FOUND)}


# ==================================== UNIT TESTS BELOW ====================================


@pytest.mark.parametrize("details, message, decoded_win32", [
    (FILE_NOT_FOUND_ERR, "Win32 error code 0x-7FF8FFFE (ERROR_FILE_NOT_FOUND)", "ERROR_FILE_NOT_FOUND"),
    ({'status': 'ERROR', 'result_type': 'WinHresult', 'result_code': HRESULT_FROM_WIN32(10203)},
     "Win32 error code 0x-7FF8D825", None),
    ({'status': 'ERROR', 'result_type': 'int', 'result_code': HRESULT_FROM_WIN32(Win32Error.ERROR_FILE_NOT_FOUND)},
     "", ""),
    ({'status': 'warning', 'result_type': 'WinHResult',
      'result_code': HRESULT_FROM_WIN32(Win32Error.ERROR_FILE_NOT_FOUND)},
     "", ""),
    ({'status': 'ERROR', 'result_type': 'WinHresult',
      'result_code': 'ssss'},
     "Unknown Win32 error code", '')
])
def test_live_response_error(details, message, decoded_win32):
    """Test the creation of a LiveResponseError."""
    err = LiveResponseError(details)
    assert err.message == message
    assert str(err) == message
    assert err.decoded_win32_error == decoded_win32


def test_create_manager(cbcsdk_mock):
    """Test creating the Live Response session manager."""
    sut = LiveResponseSessionManager(cbcsdk_mock.api, 35)
    assert sut._timeout == 35
    assert not sut._keepalive_sessions
    assert sut._job_scheduler is None


def test_submit_job(cbcsdk_mock):
    """Test submit job to the Live Response session manager."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)
    sut = LiveResponseSessionManager(cbcsdk_mock.api, 35)
    assert sut._timeout == 35
    assert not sut._keepalive_sessions
    assert sut._job_scheduler is None
    sut.submit_job('some job', 2468)
    assert sut._job_scheduler is not None


def test_base_manager_submit_job(cbcsdk_mock):
    """Test submit job to the Live Response manager base."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)
    sut = CbLRManagerBase(cbcsdk_mock.api, timeout=35)
    assert sut._timeout == 35
    assert not sut._keepalive_sessions
    assert sut._job_scheduler is None
    sut.submit_job('some job', 2468)
    assert sut._job_scheduler is not None


def test_base_manager_submit_job_with_device_object(cbcsdk_mock):
    """Test submit job to the Live Response manager base."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request("POST", "/appservices/v6/orgs/test/devices/_search", POST_DEVICE_SEARCH_RESP)
    sut = CbLRManagerBase(cbcsdk_mock.api, timeout=35)
    assert sut._timeout == 35
    assert not sut._keepalive_sessions
    assert sut._job_scheduler is None
    device = Device(cbcsdk_mock.api, 2468)
    sut.submit_job('some job', device)
    assert sut._job_scheduler is not None


@pytest.mark.parametrize("thrown_exception", [
    (ObjectNotFoundError('/appservices/v6/orgs/test/liveresponse/sessions/1:2468/keepalive'),),
])
def test_base_manager_maintain_sessions(cbcsdk_mock, thrown_exception):
    """Test maintain sessions from Live Response manager base."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/keepalive',
                             thrown_exception)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    sut = LiveResponseSessionManager(cbcsdk_mock.api, 35, keepalive_sessions=True)
    assert sut._timeout == 35
    assert sut._keepalive_sessions
    assert sut._job_scheduler is None
    session = sut.request_session(2468)
    sut._sessions[2468] = session
    sut.__cleanup_thread_running = True
    sut._refcount = 1
    sut._maintain_sessions()


def test_base_manager_maintain_sessions_exc(cbcsdk_mock):
    """Test maintain sessions from Live Response manager base."""
    def thrown_exception(url, body, **kwargs):
        raise ServerError(500)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/keepalive',
                             thrown_exception)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    sut = LiveResponseSessionManager(cbcsdk_mock.api, 35, keepalive_sessions=True)
    assert sut._timeout == 35
    assert sut._keepalive_sessions
    assert sut._job_scheduler is None
    session = sut.request_session(2468)
    sut._sessions[2468] = session
    sut.__cleanup_thread_running = True
    sut._refcount = 1
    # queue = Queue()
    # queue.put('some job')
    sut._maintain_sessions()


def test_create_session(cbcsdk_mock):
    """Test creating a Live Response session."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        assert session.session_id == '1:2468'
        assert session.device_id == 2468
        assert session._cblr_manager is manager
        assert session._cb is cbcsdk_mock.api
        assert session.os_type == 1


def test_create_session_async(cbcsdk_mock):
    """Test creating a Live Response session."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    session_id, result = manager.request_session(2468, async_mode=True)
    session = result.result()
    assert session.session_id == '1:2468'
    assert session.device_id == 2468
    assert session._cblr_manager is manager
    assert session._cb is cbcsdk_mock.api
    assert session.os_type == 1
    session.close()


def test_create_session_with_poll_error(cbcsdk_mock):
    """Test creating a Live Response session with an error in the polling."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP_ERROR)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/devices/_search', POST_DEVICE_SEARCH_RESP)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with pytest.raises(TimeoutError) as excinfo:
        manager.request_session(2468)
    assert excinfo.value.uri == '/appservices/v6/orgs/test/liveresponse/sessions/1:2468'
    assert excinfo.value.error_code == 404


def test_create_session_with_init_poll_timeout(cbcsdk_mock):
    """Test creating a Live Response session with a timeout in the initial polling."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/devices/_search', POST_DEVICE_SEARCH_RESP)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    manager._init_poll_delay = 1.25
    manager._init_poll_timeout = 1
    with pytest.raises(TimeoutError) as excinfo:
        manager.request_session(2468)
    assert excinfo.value.uri == '/appservices/v6/orgs/test/liveresponse/sessions/1:2468'
    assert excinfo.value.error_code == 404


def test_create_session_with_keepalive_option(cbcsdk_mock):
    """Test creating a Live Response session using the keepalive option."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api, 100000, True)
    try:
        with manager.request_session(2468) as session1:
            assert session1.session_id == '1:2468'
            assert session1.device_id == 2468
            assert session1._cblr_manager is manager
            assert session1._cb is cbcsdk_mock.api
            assert session1.os_type == 1
        with manager.request_session(2468) as session2:
            assert session2 is session1
        assert len(manager._sessions) == 1
        manager._maintain_sessions()
        assert len(manager._sessions) == 0
    finally:
        manager.stop_keepalive_thread()


def test_create_session_with_keepalive_option_async(cbcsdk_mock):
    """Test creating a Live Response session using the keepalive option."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api, 100000, True)
    try:
        session_id, result = manager.request_session(2468, async_mode=True)
        session1 = result.result()
        assert session_id == '1:2468'
        assert session1.session_id == '1:2468'
        assert session1.device_id == 2468
        assert session1._cblr_manager is manager
        assert session1._cb is cbcsdk_mock.api
        assert session1.os_type == 1
        session1.close()
        session_id, result2 = manager.request_session(2468, async_mode=True)
        session2 = result2.result()
        assert session2 is session1
        session2.close()
        assert len(manager._sessions) == 1
        manager._maintain_sessions()
        assert len(manager._sessions) == 0
    finally:
        manager.stop_keepalive_thread()


@pytest.mark.parametrize("thrown_exception", [
    (ObjectNotFoundError('/appservices/v6/orgs/test/liveresponse/sessions/1:2468'),),
    (ServerError(404, 'test error'),)
])
def test_session_maintenance_sends_keepalive(cbcsdk_mock, thrown_exception):
    """Test to ensure the session maintenance sends the keepalive messages as needed."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/keepalive', {})
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/keepalive',
                             thrown_exception)
    manager = LiveResponseSessionManager(cbcsdk_mock.api, 100000, True)
    try:
        with manager.request_session(2468):
            manager._maintain_sessions()
            assert len(manager._sessions) == 1
            manager._maintain_sessions()
    finally:
        manager.stop_keepalive_thread()


def test_list_directory(cbcsdk_mock):
    """Test the response to the 'list directory' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             DIRECTORY_LIST_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/6',
                             DIRECTORY_LIST_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        files = session.list_directory('C:\\\\TEMP\\\\')
        assert files[0]['filename'] == '.'
        assert 'DIRECTORY' in files[0]['attributes']
        assert files[1]['filename'] == '..'
        assert 'DIRECTORY' in files[1]['attributes']
        assert files[2]['filename'] == 'test.txt'
        assert 'ARCHIVE' in files[2]['attributes']


def test_list_directory_async(cbcsdk_mock):
    """Test the response to the 'list directory' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             DIRECTORY_LIST_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/6',
                             DIRECTORY_LIST_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, result = session.list_directory('C:\\\\TEMP\\\\', async_mode=True)
        assert command_id == 6
        files = result.result()
        assert files[0]['filename'] == '.'
        assert 'DIRECTORY' in files[0]['attributes']
        assert files[1]['filename'] == '..'
        assert 'DIRECTORY' in files[1]['attributes']
        assert files[2]['filename'] == 'test.txt'
        assert 'ARCHIVE' in files[2]['attributes']


def test_delete_file(cbcsdk_mock):
    """Test the response to the 'delete file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             DELETE_FILE_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.delete_file('C:\\\\TEMP\\\\foo.txt')


def test_delete_file_async(cbcsdk_mock):
    """Test the response to the 'delete file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             DELETE_FILE_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, _ = session.delete_file('C:\\\\TEMP\\\\foo.txt', async_mode=True)
        assert command_id == 3


def test_delete_file_with_error(cbcsdk_mock):
    """Test the response to the 'delete file' command when it returns an error."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             DELETE_FILE_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_ERROR_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        with pytest.raises(LiveResponseError) as excinfo:
            session.delete_file('C:\\\\TEMP\\\\foo.txt')
        assert excinfo.value.decoded_win32_error == "ERROR_FILE_NOT_FOUND"


def test_get_file(cbcsdk_mock, connection_mock):
    """Test the response to the 'get file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.get_file('c:\\\\test.txt')


def test_get_file_cancelled(cbcsdk_mock, connection_mock):
    """Test the response to the 'get file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_CANCELLED_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        with pytest.raises(ApiError) as ex:
            session.get_file('c:\\\\test.txt')
        assert 'The command has been cancelled.' in str(ex.value)


def test_get_file_cancelled_async(cbcsdk_mock, connection_mock):
    """Test the response to the 'get file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_CANCELLED_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        with pytest.raises(ApiError) as ex:
            _, result = session.get_file('c:\\\\test.txt', async_mode=True)
            result.result()
        assert 'The command has been cancelled.' in str(ex.value)


def test_get_file_async(cbcsdk_mock, connection_mock):
    """Test the response to the 'get file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, _ = session.get_file('c:\\\\test.txt', async_mode=True)
        assert command_id == 7


def test_get_raw_file_async(cbcsdk_mock, connection_mock):
    """Test the response to the 'get file' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, _ = session.get_raw_file('c:\\\\test.txt', async_mode=True)
        assert command_id == 7


def test_command_status(cbcsdk_mock):
    """Test command status method"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        status = session.command_status(7)
        assert status == 'COMPLETE'


def test_session_status(cbcsdk_mock):
    """Test command status method"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    session_id, _ = manager.request_session(2468, async_mode=True)
    status = manager.session_status(session_id)
    assert status == 'ACTIVE'


def test_cancel_complete_command(cbcsdk_mock):
    """Test the response to the 'cancel command' command for completed command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        with pytest.raises(ApiError) as excinfo:
            session.cancel_command(7)
        assert excinfo.value.__str__().startswith('Cannot cancel command in status COMPLETE')


def test_cancel_pending_command(cbcsdk_mock):
    """Test the response to the 'cancel command' command for completed command."""
    _was_called = False

    def delete_req(url, body):
        nonlocal _was_called
        _was_called = True
        return None

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7', delete_req)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        try:
            session.cancel_command(7)
            assert _was_called
        except ApiError:
            raise Exception('Failed')


def test_put_file(cbcsdk_mock, mox):
    """Test the response to the 'put file' command."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        assert body['name'] == 'put file'
        assert body['file_id'] == 10203
        assert body['path'] == 'foobar.txt'
        return PUT_FILE_START_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/6',
                             PUT_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    filep = io.StringIO('This is a test')
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, '_upload_file')
        session._upload_file(filep).AndReturn(10203)
        mox.ReplayAll()
        session.put_file(filep, 'foobar.txt')
        mox.VerifyAll()


def test_put_file_async(cbcsdk_mock, mox):
    """Test the response to the 'put file' command."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        assert body['name'] == 'put file'
        assert body['file_id'] == 10203
        assert body['path'] == 'foobar.txt'
        return PUT_FILE_START_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/6',
                             PUT_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    filep = io.StringIO('This is a test')
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, '_upload_file')
        session._upload_file(filep).AndReturn(10203)
        mox.ReplayAll()
        command_id, _ = session.put_file(filep, 'foobar.txt', async_mode=True)
        assert command_id == 6
        mox.VerifyAll()


def test_create_directory(cbcsdk_mock):
    """Test the response to the 'create directory' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             CREATE_DIRECTORY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             CREATE_DIRECTORY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.create_directory('C:\\\\TEMP\\\\TRASH')


def test_create_directory_async(cbcsdk_mock):
    """Test the response to the 'create directory' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             CREATE_DIRECTORY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             CREATE_DIRECTORY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, _ = session.create_directory('C:\\\\TEMP\\\\TRASH', async_mode=True)
        assert command_id == 7


def test_walk(cbcsdk_mock, mox):
    """Test the logic of the directory walking."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, 'list_directory')
        session.list_directory('C:\\TEMP\\*').AndReturn(WALK_RETURN_1)
        session.list_directory('C:\\TEMP\\FOO\\*').AndReturn(WALK_RETURN_2)
        session.list_directory('C:\\TEMP\\BAR\\*').AndReturn(WALK_RETURN_3)
        mox.ReplayAll()
        index = 1
        for entry in session.walk('C:\\TEMP\\'):
            if index == 1:
                assert entry[0] == 'C:\\TEMP\\'
                assert len(entry[1]) == 2
                assert 'FOO' in entry[1]
                assert 'BAR' in entry[1]
                assert len(entry[2]) == 1
                assert 'test.txt' in entry[2]
            elif index == 2:
                assert entry[0] == 'C:\\TEMP\\FOO\\'
                assert len(entry[1]) == 0
                assert len(entry[2]) == 2
                assert 'hoopy.doc' in entry[2]
                assert 'frood.doc' in entry[2]
            elif index == 3:
                assert entry[0] == 'C:\\TEMP\\BAR\\'
                assert len(entry[1]) == 0
                assert len(entry[2]) == 1
                assert 'evil.exe' in entry[2]
            else:
                pytest.fail("Index went out of range")
            index = index + 1
        mox.VerifyAll()


def test_walk_bottomup_with_error(cbcsdk_mock, mox):
    """Test the logic of the directory walking with an error in one of the directories."""
    called_error_response = 0

    def error_response(err):
        assert err.decoded_win32_error == "ERROR_FILE_NOT_FOUND"
        nonlocal called_error_response
        called_error_response = called_error_response + 1

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, 'list_directory')
        session.list_directory('C:\\TEMP\\*').AndReturn(WALK_RETURN_1)
        session.list_directory('C:\\TEMP\\FOO\\*').AndRaise(LiveResponseError(FILE_NOT_FOUND_ERR))
        session.list_directory('C:\\TEMP\\BAR\\*').AndReturn(WALK_RETURN_3)
        mox.ReplayAll()
        index = 1
        for entry in session.walk('C:\\TEMP\\', False, error_response):
            if index == 1:
                assert entry[0] == 'C:\\TEMP\\BAR\\'
                assert len(entry[1]) == 0
                assert len(entry[2]) == 1
                assert 'evil.exe' in entry[2]
            elif index == 2:
                assert entry[0] == 'C:\\TEMP\\'
                assert len(entry[1]) == 2
                assert 'FOO' in entry[1]
                assert 'BAR' in entry[1]
                assert len(entry[2]) == 1
                assert 'test.txt' in entry[2]
            else:
                pytest.fail("Index went out of range")
            index = index + 1
        mox.VerifyAll()
    assert called_error_response == 1


def test_kill_process(cbcsdk_mock):
    """Test the response to the 'kill' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             KILL_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/13',
                             KILL_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        assert session.kill_process(601)


def test_kill_process_async(cbcsdk_mock):
    """Test the response to the 'kill' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             KILL_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/13',
                             KILL_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, result = session.kill_process(601, async_mode=True)
        assert command_id == 13
        assert result.result()


def test_kill_process_timeout(cbcsdk_mock):
    """Test the response to the 'kill' command when it times out."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             KILL_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/13',
                             KILL_PROC_START_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api, 2)
    with manager.request_session(2468) as session:
        assert not session.kill_process(601)


def test_create_process(cbcsdk_mock):
    """Test the response to the 'create process' command with wait for completion."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             CREATE_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/52',
                             CREATE_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        assert session.create_process('start_daemon', False) is None


def test_create_process_async(cbcsdk_mock):
    """Test the response to the 'create process' command with wait for completion."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             CREATE_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/52',
                             CREATE_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, result = session.create_process('start_daemon', False, async_mode=True)
        assert command_id == 52
        assert result.result() is None


def test_spawn_process(cbcsdk_mock):
    """Test the response to the 'create process' command without wait for completion."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             CREATE_PROC_START_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        assert session.create_process('start_daemon', False, None, None, 30, False) is None


@pytest.mark.parametrize("remotefile", [('junk.txt',), (None,)])
def test_run_process_with_output(cbcsdk_mock, mox, remotefile):
    """Test the response to the 'create process' command with output that we retrieve."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        if body['name'] == 'create process':
            return RUN_PROC_START_RESP
        elif body['name'] == 'delete file':
            resp = copy.deepcopy(DELETE_FILE_START_RESP)
            resp['path'] = body['path']
            return resp
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def validate_get_file(name):
        if name is None:
            return False
        if remotefile is not None:
            return name == remotefile
        return True

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/9',
                             RUN_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, 'get_file')
        session.get_file(pymox.Func(validate_get_file)).AndReturn('I Got It')
        mox.ReplayAll()
        rc = session.create_process('gimme', True, remotefile)
        assert rc == 'I Got It'
        mox.VerifyAll()


def test_run_process_with_output_no_remote_file(cbcsdk_mock, mox):
    """Test the response to the 'create process' command with output that we retrieve."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        if body['name'] == 'create process':
            return RUN_PROC_START_RESP
        elif body['name'] == 'delete file':
            resp = copy.deepcopy(DELETE_FILE_START_RESP)
            resp['path'] = body['path']
            return resp
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def validate_get_file(name):
        if name is None:
            return False
        return True

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/9',
                             RUN_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        mox.StubOutWithMock(session, 'get_file')
        session.get_file(pymox.Func(validate_get_file)).AndReturn('I Got It')
        mox.ReplayAll()
        rc = session.create_process('gimme', True, None, 'c:\\temp')
        assert rc == 'I Got It'
        mox.VerifyAll()


def test_list_processes(cbcsdk_mock):
    """Test the response to the 'list processes' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             LIST_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             LIST_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        plist = session.list_processes()
        assert len(plist) == 3
        assert plist[0]['process_path'] == 'proc1'
        assert plist[1]['process_path'] == 'server'
        assert plist[2]['process_path'] == 'borg'


def test_list_processes_async(cbcsdk_mock):
    """Test the response to the 'list processes' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             LIST_PROC_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/10',
                             LIST_PROC_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        command_id, result = session.list_processes(async_mode=True)
        plist = result.result()
        assert command_id == 10
        assert len(plist) == 3
        assert plist[0]['process_path'] == 'proc1'
        assert plist[1]['process_path'] == 'server'
        assert plist[2]['process_path'] == 'borg'


def test_registry_enum(cbcsdk_mock):
    """Test the response to the 'reg enum keys' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_ENUM_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/56',
                             REG_ENUM_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        rc1 = session.list_registry_keys_and_values('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI')
        assert len(rc1['sub_keys']) == 2
        assert 'Parameters' in rc1['sub_keys']
        assert 'Enum' in rc1['sub_keys']
        value_names = ['Start', 'Type', 'ErrorControl', 'ImagePath', 'DisplayName', 'Group', 'DriverPackageId', 'Tag']
        assert len(rc1['values']) == len(value_names)
        for keyitem in rc1['values']:
            assert keyitem['value_name'] in value_names
        rc2 = session.list_registry_values('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI')
        assert len(rc2) == len(value_names)
        for keyitem in rc2:
            assert keyitem['value_name'] in value_names


def test_registry_enum_async(cbcsdk_mock):
    """Test the response to the 'reg enum keys' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_ENUM_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/56',
                             REG_ENUM_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, result = session.list_registry_keys_and_values('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI',
                                                             async_mode=True)
        rc1 = result.result()
        assert c_id == 56
        assert len(rc1['sub_keys']) == 2
        assert 'Parameters' in rc1['sub_keys']
        assert 'Enum' in rc1['sub_keys']
        value_names = ['Start', 'Type', 'ErrorControl', 'ImagePath', 'DisplayName', 'Group', 'DriverPackageId', 'Tag']
        assert len(rc1['values']) == len(value_names)
        for keyitem in rc1['values']:
            assert keyitem['value_name'] in value_names
        command_id, result = session.list_registry_values('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI',
                                                          async_mode=True)
        assert command_id == 56
        rc2 = result.result()
        assert len(rc2) == len(value_names)
        for keyitem in rc2:
            assert keyitem['value_name'] in value_names


def test_registry_get(cbcsdk_mock):
    """Test the response to the 'reg get value' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_GET_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/61',
                             REG_GET_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        val = session.get_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Start')
        assert val['value_data'] == 0
        assert val['value_name'] == 'Start'
        assert val['value_type'] == 'REG_DWORD'


def test_registry_get_async(cbcsdk_mock):
    """Test the response to the 'reg get value' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_GET_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/61',
                             REG_GET_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, result = session.get_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Start',
                                                  async_mode=True)
        val = result.result()
        assert c_id == 61
        assert val['value_data'] == 0
        assert val['value_name'] == 'Start'
        assert val['value_type'] == 'REG_DWORD'


@pytest.mark.parametrize("set_val,check_val,overwrite,set_type,check_type", [
    (42, 42, False, None, 'REG_DWORD'),
    (['a', 'b', 'c'], ['a', 'b', 'c'], True, None, 'REG_MULTI_SZ'),
    ([10, 20, 30], ['10', '20', '30'], False, None, 'REG_MULTI_SZ'),
    ('Quimby', 'Quimby', True, None, 'REG_SZ'),
    (80231, 80231, False, 'REG_QWORD', 'REG_QWORD')
])
def test_registry_set(cbcsdk_mock, set_val, check_val, overwrite, set_type, check_type):
    """Test the response to the 'reg set value' command."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        assert body['name'] == 'reg set value'
        assert body['path'] == 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue'
        assert body['overwrite'] == overwrite
        assert body['value_type'] == check_type
        assert body['value_data'] == check_val
        return REG_SET_START_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/62',
                             REG_SET_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.set_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue', set_val,
                                   overwrite, set_type)


@pytest.mark.parametrize("set_val,check_val,overwrite,set_type,check_type", [
    (42, 42, False, None, 'REG_DWORD'),
    (['a', 'b', 'c'], ['a', 'b', 'c'], True, None, 'REG_MULTI_SZ'),
    ([10, 20, 30], ['10', '20', '30'], False, None, 'REG_MULTI_SZ'),
    ('Quimby', 'Quimby', True, None, 'REG_SZ'),
    (80231, 80231, False, 'REG_QWORD', 'REG_QWORD')
])
def test_registry_set_async(cbcsdk_mock, set_val, check_val, overwrite, set_type, check_type):
    """Test the response to the 'reg set value' command."""
    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        assert body['name'] == 'reg set value'
        assert body['path'] == 'HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue'
        assert body['overwrite'] == overwrite
        assert body['value_type'] == check_type
        assert body['value_data'] == check_val
        return REG_SET_START_RESP

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/62',
                             REG_SET_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, _ = session.set_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
                                             set_val,
                                             overwrite,
                                             set_type,
                                             async_mode=True)
        assert c_id == 62


def test_registry_create_key(cbcsdk_mock):
    """Test the response to the 'reg create key' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_CREATE_KEY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/63',
                             REG_CREATE_KEY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.create_registry_key('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense')


def test_registry_create_key_async(cbcsdk_mock):
    """Test the response to the 'reg create key' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_CREATE_KEY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/63',
                             REG_CREATE_KEY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, _ = session.create_registry_key('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
                                              async_mode=True)
        assert c_id == 63


def test_registry_delete_key(cbcsdk_mock):
    """Test the response to the 'reg delete key' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_DELETE_KEY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/64',
                             REG_DELETE_KEY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.delete_registry_key('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense')


def test_registry_delete_key_async(cbcsdk_mock):
    """Test the response to the 'reg delete key' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_DELETE_KEY_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/64',
                             REG_DELETE_KEY_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, _ = session.delete_registry_key('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense',
                                              async_mode=True)
        assert c_id == 64


def test_registry_delete(cbcsdk_mock):
    """Test the response to the 'reg delete value' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_DELETE_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/65',
                             REG_DELETE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        session.delete_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue')


def test_registry_delete_async(cbcsdk_mock):
    """Test the response to the 'reg delete value' command."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             REG_DELETE_START_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/65',
                             REG_DELETE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, _ = session.delete_registry_value('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\testvalue',
                                                async_mode=True)
        assert c_id == 65


def test_registry_unsupported_command(cbcsdk_mock):
    """Test the response to a command that we know isn't supported on the target node."""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', USESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:7777', USESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/7777', UDEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(7777) as session:
        with pytest.raises(ApiError) as excinfo:
            session.create_registry_key('HKLM\\SYSTEM\\CurrentControlSet\\services\\ACPI\\Nonsense')
        assert excinfo.value.__str__().startswith("Command reg create key not supported")


def test_memdump(cbcsdk_mock):
    """Test the response to the 'memdump' command."""
    generated_file_name = None
    target_file_name = None

    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        nonlocal generated_file_name, target_file_name
        if body['name'] == 'memdump':
            generated_file_name = body['path']
            target_file_name = generated_file_name
            if body['compress']:
                target_file_name += '.zip'
            retval = copy.deepcopy(MEMDUMP_START_RESP)
            retval['path'] = generated_file_name
            return retval
        elif body['name'] == 'delete file':
            assert body['path'] == target_file_name
            retval = copy.deepcopy(MEMDUMP_DEL_START_RESP)
            retval['path'] = target_file_name
            return retval
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def respond_get_memdump_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_END_RESP)
        retval['path'] = generated_file_name
        return retval

    def respond_delete_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_DEL_END_RESP)
        retval['path'] = target_file_name
        return retval

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/101',
                             respond_get_memdump_file)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/102',
                             respond_delete_file)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        memdump = session.start_memdump()
        assert memdump.lr_session is session
        assert memdump.remote_filename == target_file_name
        memdump.wait()
        memdump.delete()


def test_memdump_async(cbcsdk_mock):
    """Test the response to the 'memdump' command."""
    generated_file_name = None
    target_file_name = None

    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        nonlocal generated_file_name, target_file_name
        if body['name'] == 'memdump':
            generated_file_name = body['path']
            target_file_name = generated_file_name
            print(target_file_name)
            if body['compress']:
                target_file_name += '.zip'
            retval = copy.deepcopy(MEMDUMP_START_RESP)
            retval['path'] = generated_file_name
            return retval
        elif body['name'] == 'delete file':
            assert body['path'] == target_file_name
            retval = copy.deepcopy(MEMDUMP_DEL_START_RESP)
            retval['path'] = target_file_name
            return retval
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def respond_get_memdump_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_END_RESP)
        retval['path'] = generated_file_name
        return retval

    def respond_delete_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_DEL_END_RESP)
        retval['path'] = target_file_name
        return retval

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/101',
                             respond_get_memdump_file)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/102',
                             respond_delete_file)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        c_id, _ = session.memdump('test.txt', async_mode=True)
        assert c_id == 101


def test_memdump_errors(cbcsdk_mock):
    """Test the response to the 'memdump' command."""
    generated_file_name = None
    target_file_name = None

    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        nonlocal generated_file_name, target_file_name
        if body['name'] == 'memdump':
            generated_file_name = body['path']
            target_file_name = generated_file_name
            if body['compress']:
                target_file_name += '.zip'
            retval = copy.deepcopy(MEMDUMP_START_RESP)
            retval['path'] = generated_file_name
            return retval
        elif body['name'] == 'delete file':
            assert body['path'] == target_file_name
            retval = copy.deepcopy(MEMDUMP_DEL_START_RESP)
            retval['path'] = target_file_name
            return retval
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def respond_get_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_END_RESP)
        retval['path'] = generated_file_name
        return retval

    def respond_delete_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_DEL_END_RESP)
        retval['path'] = target_file_name
        return retval

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/101',
                             respond_get_file)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/102',
                             respond_delete_file)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        memdump = session.start_memdump()
        assert memdump.lr_session is session
        assert memdump.remote_filename == target_file_name
        memdump._done = True
        memdump._error = Exception('some error')
        with pytest.raises(Exception):
            memdump.get('test.txt')
        memdump.wait()
        memdump.delete()


def test_memdump_not_done(cbcsdk_mock):
    """Test the response to the 'memdump' command."""
    generated_file_name = None
    target_file_name = None

    def respond_to_post(url, body, **kwargs):
        assert body['session_id'] == '1:2468'
        nonlocal generated_file_name, target_file_name
        if body['name'] == 'memdump':
            generated_file_name = body['path']
            target_file_name = generated_file_name
            if body['compress']:
                target_file_name += '.zip'
            retval = copy.deepcopy(MEMDUMP_START_RESP)
            retval['path'] = generated_file_name
            return retval
        elif body['name'] == 'delete file':
            assert body['path'] == target_file_name
            retval = copy.deepcopy(MEMDUMP_DEL_START_RESP)
            retval['path'] = target_file_name
            return retval
        else:
            pytest.fail(f"Invalid command name seen: {body['name']}")

    def respond_get_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_END_RESP)
        retval['path'] = generated_file_name
        return retval

    def respond_delete_file(url, query_parameters, default):
        retval = copy.deepcopy(MEMDUMP_DEL_END_RESP)
        retval['path'] = target_file_name
        return retval

    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands', respond_to_post)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/101',
                             respond_get_file)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/102',
                             respond_delete_file)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        memdump = session.start_memdump()
        assert memdump.lr_session is session
        assert memdump.remote_filename == target_file_name
        memdump._done = False
        memdump._error = Exception('some error')
        with pytest.raises(Exception):
            memdump.get('test.txt')
        memdump.wait()
        memdump.delete()


def test_lr_post_command(cbcsdk_mock):
    """Test creating a Live Response session."""
    called = False

    def start_command(url, param_table, **kwargs):
        nonlocal called
        if called is False:
            called = True
            raise ObjectNotFoundError('/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                                      message='{"error_code": "NOT_FOUND"}')
        return DELETE_FILE_START_RESP
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             start_command)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        data = {"name": "delete file", "path": 'filename'}
        session._lr_post_command(data)


def test_lr_post_command_error(cbcsdk_mock):
    """Test creating a Live Response session."""
    def start_command(url, param_table, **kwargs):
        raise ObjectNotFoundError('/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                                  message='other')
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             start_command)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        data = {"name": "delete file", "pth": 'filename'}
        with pytest.raises(ApiError):
            session._lr_post_command(data)


def test_lr_post_command_error_timeout(cbcsdk_mock):
    """Test creating a Live Response session lr_post_command errors."""
    def start_command(url, param_table, **kwargs):
        raise ObjectNotFoundError('/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                                  message='{"error_code": "NOT_FOUND"}')
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             start_command)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/3',
                             DELETE_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        data = {"name": "delete file", "path": 'filename'}
        with pytest.raises(TimeoutError):
            session._lr_post_command(data)


def test_completion_notification_work_status(cbcsdk_mock):
    """Test CompletionNotification, WorkerStatus"""
    obj = CompletionNotification(2468)
    assert obj.device_id == 2468
    obj = WorkerStatus(2468)
    assert obj.device_id == 2468
    assert obj.status == "READY"
    assert obj.exception is None


def test_job_worker(cbcsdk_mock):
    """Test JobWorker Success Flow"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    results = Queue()
    job_worker = JobWorker(cbcsdk_mock.api, 2468, results)
    assert job_worker.device_id == 2468
    work_item = WorkItem(lambda lr_session: True, 2468)
    job_worker.job_queue.put(work_item)
    job_worker.job_queue.put(None)
    job_worker.run()
    assert job_worker.result_queue.get().status == "READY"
    assert isinstance(job_worker.result_queue.get(), CompletionNotification)
    assert job_worker.result_queue.get().status == "EXITING"
    assert job_worker.job_queue.empty()
    assert work_item.future.result() is True


def test_job_worker_no_item(cbcsdk_mock):
    """Test JobWorker"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    results = Queue()
    job_worker = JobWorker(cbcsdk_mock.api, 2468, results)
    assert job_worker.device_id == 2468
    job_worker.job_queue.put(None)
    job_worker.run()
    assert job_worker.result_queue.get().status == "READY"
    assert job_worker.result_queue.get().status == "EXITING"
    assert job_worker.job_queue.empty()


def test_job_worker_device_not_found(cbcsdk_mock):
    """Test JobWorker unable to make session with device"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET',
                             '/appservices/v6/orgs/test/liveresponse/sessions/1:2468',
                             ObjectNotFoundError("/appservices/v6/orgs/test/liveresponse/sessions/1:2468",
                                                 "Could not establish session with device 2468"))
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    results = Queue()
    job_worker = JobWorker(cbcsdk_mock.api, 2468, results)
    assert job_worker.device_id == 2468
    work_item = WorkItem(lambda lr_session: True, 2468)
    job_worker.job_queue.put(work_item)
    job_worker.run()
    assert job_worker.result_queue.get().status == "ERROR"
    assert job_worker.job_queue.empty()
    assert isinstance(work_item.future.exception(), Exception)


def test_get_file_job(cbcsdk_mock, connection_mock):
    """Test GetFileJob"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands',
                             GET_FILE_COMMAND_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468/commands/7',
                             GET_FILE_END_RESP)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    manager = LiveResponseSessionManager(cbcsdk_mock.api)
    with manager.request_session(2468) as session:
        file_job = GetFileJob('c:\\\\test.txt')
        file_job.run(session)


def test_job_scheduler_statuses(cbcsdk_mock):
    """Test LiveResponseJobScheduler"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    job_scheduler = LiveResponseJobScheduler(cbcsdk_mock.api)
    cn_obj = CompletionNotification(2468)
    assert cn_obj.device_id == 2468
    ws_obj_ready = WorkerStatus(2468)
    assert ws_obj_ready.device_id == 2468
    ws_obj = WorkerStatus(2469)
    assert ws_obj.device_id == 2469
    ws_obj_wrong_status = WorkerStatus(2468, status="alabala")
    ws_obj_error = WorkerStatus(2468, status="ERROR")
    job_scheduler.schedule_queue.put(ws_obj_error)
    job_scheduler.schedule_queue.put(ws_obj_ready)
    job_scheduler.schedule_queue.put(ws_obj_wrong_status)
    job_scheduler.schedule_queue.put(cn_obj)
    job_scheduler.schedule_queue.put('test')
    job_scheduler._job_workers[2469] = JobWorker(cbcsdk_mock.api, 2469, Queue())
    job_scheduler._unscheduled_jobs[2469] = [ws_obj]
    job_scheduler._unscheduled_jobs[2468] = [ws_obj_error]
    job_scheduler._idle_workers.add(2469)
    job_scheduler.run()


def test_job_scheduler_exiting(cbcsdk_mock, mox):
    """Test LiveResponseJobScheduler"""
    cbcsdk_mock.mock_request('POST', '/appservices/v6/orgs/test/liveresponse/sessions', SESSION_INIT_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', SESSION_POLL_RESP)
    cbcsdk_mock.mock_request('GET', '/appservices/v6/orgs/test/devices/2468', DEVICE_RESPONSE)
    cbcsdk_mock.mock_request('DELETE', '/appservices/v6/orgs/test/liveresponse/sessions/1:2468', None)
    job_scheduler = LiveResponseJobScheduler(cbcsdk_mock.api)
    ws_obj_exiting = WorkerStatus(2468, status="EXITING")
    job_scheduler.schedule_queue.put(ws_obj_exiting)
    job_scheduler._idle_workers.add(2469)
    job_worker = JobWorker(cbcsdk_mock.api, 2468, Queue())
    job_scheduler._job_workers[2468] = job_worker
    job_scheduler.schedule_queue.put('test')
    mox.StubOutWithMock(job_worker, 'join')
    job_worker.join().AndReturn(True)
    mox.ReplayAll()
    job_scheduler.run()
    mox.VerifyAll()
