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

"""Tests for the FileCredentialProvider"""

import pytest
import os
import sys
from pathlib import Path
from cbc_sdk.credential_providers.file import FileCredentialProvider
from cbc_sdk.errors import CredentialError


def path_of(filename):
    """Determine a full pathname of a test file."""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_file_data', filename)

# === UNIT TESTS BELOW === #


@pytest.mark.parametrize("platform, sysprefix", [
    ("linux", f"{os.sep}etc{os.sep}carbonblack"),
    ("win32", f"C:{os.sep}Windows{os.sep}carbonblack")
])
def test_search_path_default(platform, sysprefix, monkeypatch):
    """Validate the building of the default search path based on the platform."""
    monkeypatch.setattr(sys, "platform", platform)
    monkeypatch.setenv("windir", f"C:{os.sep}Windows")
    sut = FileCredentialProvider()
    search_path = sut._search_path
    assert len(search_path) == 6
    basepath = Path(sysprefix)
    assert str(search_path[0]) == str(basepath / "credentials.psc")
    assert str(search_path[1]) == str(basepath / "credentials.cbc")
    basepath = Path.home() / '.carbonblack'
    assert str(search_path[2]) == str(basepath / "credentials.psc")
    assert str(search_path[3]) == str(basepath / "credentials.cbc")
    basepath = Path('.', '.carbonblack')
    assert str(search_path[4]) == str(basepath / "credentials.psc")
    assert str(search_path[5]) == str(basepath / "credentials.cbc")


def test_search_path_onearg():
    """Validate the building of the search path with a single item."""
    sut = FileCredentialProvider(path_of("config_valid.cbc"))
    search_path = sut._search_path
    assert len(search_path) == 1
    assert str(search_path[0]) == path_of("config_valid.cbc")


def test_search_path_listarg():
    """Validate the building of the search path with multiple items in a list."""
    sut = FileCredentialProvider([path_of("config_partial1.cbc"), path_of("config_partial2.cbc")])
    search_path = sut._search_path
    assert len(search_path) == 2
    assert str(search_path[0]) == path_of("config_partial1.cbc")
    assert str(search_path[1]) == path_of("config_partial2.cbc")


def test_security_check_simple_cases():
    """Test the easy simple cases of the _security_check() function."""
    sut = FileCredentialProvider()
    testpath = Path(path_of("config_notexist.cbc"))
    assert not sut._security_check(testpath)  # fails because it doesn't exist
    assert not sut._security_check(testpath.parent)  # fails because it's a directory


def test_security_check_windows(monkeypatch):
    """Test expected behavior for a Windows "security check" on a file."""
    monkeypatch.setattr(sys, "platform", "win32")
    testpath = Path(path_of("config_valid.cbc"))
    sut = FileCredentialProvider()
    assert sut._security_check(testpath)
    assert not sut._general_warn


class MockStatResult:
    """Used to create a mock return for _file_stat."""
    def __init__(self):
        """Initialize the MockStatResult"""
        self.st_mode = 0
        self.st_uid = 0


@pytest.mark.parametrize("fileuid, filemode, parentuid, parentmode, warned, prefix, suffix", [
    (1234, 0o600, 1234, 0o700, True, None, None),
    (1234, 0o644, 1234, 0o700, False, "File ", " has invalid permissions"),
    (1234, 0o200, 1234, 0o700, False, "File ", " has invalid permissions"),
    (1230, 0o600, 1234, 0o700, False, "File ", " not owned by current user"),
    (1234, 0o644, 1234, 0o750, False, "Directory ", " has invalid permissions"),
    (1234, 0o644, 1234, 0o300, False, "Directory ", " has invalid permissions"),
    (1234, 0o644, 1230, 0o750, False, "Directory ", " not owned by current user"),
])
def test_security_check_unix(fileuid, filemode, parentuid, parentmode, warned, prefix, suffix, monkeypatch):
    """Test expected behavior for Unix-style security checks on a file."""
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(os, "geteuid", lambda: 1234, False)
    testpath = Path(path_of("config_valid.cbc"))

    def mock_stat(path):
        rc = MockStatResult()
        if path == testpath:
            rc.st_mode = filemode
            rc.st_uid = fileuid
        elif path == testpath.parent:
            rc.st_mode = parentmode
            rc.st_uid = parentuid
        return rc

    sut = FileCredentialProvider()
    monkeypatch.setattr(sut, "_file_stat", mock_stat)
    assert sut._security_check(testpath)
    assert sut._specific_file_warn == warned
    if prefix:
        assert sut._last_failmsg.startswith(prefix)
    else:
        assert sut._last_failmsg is None
    if suffix:
        assert sut._last_failmsg.endswith(suffix)
    else:
        assert sut._last_failmsg is None


def test_read_single_file():
    """Test the basic reading of multiple credential sets from a single file."""
    sut = FileCredentialProvider(path_of("config_valid.cbc"))
    creds = sut.get_credentials("default")
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert not creds.ssl_verify_hostname
    assert creds.ssl_cert_file == "foo.certs"
    assert creds.ssl_force_tls_1_2
    assert creds.proxy == "proxy.example"
    assert creds.ignore_system_proxy
    creds = sut.get_credentials("partial")
    assert creds.url == "http://example.com"
    assert creds.token is None
    assert creds.org_key is None
    assert not creds.ssl_verify
    assert creds.ssl_verify_hostname
    assert creds.ssl_cert_file is None
    assert not creds.ssl_force_tls_1_2
    assert creds.proxy is None
    assert not creds.ignore_system_proxy
    with pytest.raises(CredentialError):
        sut.get_credentials("notexist")


def test_read_multiple_files():
    """Test reading a credential set from multiple files."""
    sut = FileCredentialProvider([path_of("config_partial1.cbc"), path_of("config_partial2.cbc")])
    creds = sut.get_credentials("default")
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert not creds.ssl_verify_hostname
    assert creds.ssl_cert_file == "foo.certs"
    assert creds.ssl_force_tls_1_2
    assert creds.proxy == "proxy.example"
    assert creds.ignore_system_proxy


def test_file_witn_parsing_error():
    """Test reading a file that has a parsing error."""
    sut = FileCredentialProvider(path_of("config_parseerror.cbc"))
    with pytest.raises(CredentialError):
        sut.get_credentials("default")
