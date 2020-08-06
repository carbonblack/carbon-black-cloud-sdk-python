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

"""Tests for the Windows Registry credential provider."""

import pytest
import sys
from cbc_sdk.credential_providers import RegistryCredentialProvider
from cbc_sdk.credential_providers.registry_credential_provider \
    import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, REG_SZ, REG_DWORD
from cbc_sdk.errors import CredentialError


class StubKeyObject:
    """Stub key object used in testing."""
    def __enter__(self):
        """
        Enter the context created by this object.

        Returns:
            StubKeyObject: self is always returned.
        """
        self._entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context created by this object.

        Args:
            exc_type (type): Type of the exception that was thrown to exit, if applicable.
            exc_val (BaseException): Value of the exception that was thrown to exit, if applicable.
            exc_tb (Any): Traceback information, if applicable.

        Returns:
            bool: False is always returned.
        """
        self._exited = True
        return False

    def check(self):
        """Validate that the context was properly entered and exited."""
        assert getattr(self, '_entered', False), "Key context not actually entered"
        assert getattr(self, '_exited', False), "Key context entered without being exited"


def test_breaks_not_on_windows(monkeypatch):
    """Test that creating the RegistryCredentialProvider breaks if we're not on Windows."""
    monkeypatch.setattr(sys, "platform", "linux")
    with pytest.raises(CredentialError):
        RegistryCredentialProvider()


def test_select_base_key(monkeypatch):
    """Test that the base key is selected correctly depending on the flag."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    assert sut._base_key() is HKEY_CURRENT_USER
    sut = RegistryCredentialProvider(None, False)
    assert sut._base_key() is HKEY_LOCAL_MACHINE


@pytest.mark.parametrize('key, return_val, check_val', [
    ('Alpha', ('Correct', REG_SZ), 'Correct'),
    ('Bravo', None, None)
])
def test_read_str(monkeypatch, mox, key, return_val, check_val):
    """Test reading strings from the registry."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, key).AndReturn(return_val)
    mox.ReplayAll()
    assert check_val == sut._read_str(stub_key, key)
    mox.VerifyAll()


def test_read_str_exceptions(monkeypatch, mox):
    """Test reading strings from the registry in ways that throw exceptions."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, "Alpha").AndReturn((42, REG_DWORD))
    sut._read_value(stub_key, "Bravo").AndRaise(CredentialError("Unable to read"))
    mox.ReplayAll()
    with pytest.raises(CredentialError) as e1:
        sut._read_str(stub_key, "Alpha")
    assert "not of string type" in str(e1.value)
    with pytest.raises(CredentialError) as e2:
        sut._read_str(stub_key, "Bravo")
    assert "Unable to read" in str(e2.value)
    mox.VerifyAll()


@pytest.mark.parametrize('key, return_val, check_val', [
    ('Alpha', (0, REG_DWORD), False),
    ('Bravo', (5, REG_DWORD), True),
    ('Charlie', None, None)
])
def test_read_bool(monkeypatch, mox, key, return_val, check_val):
    """Test reading boolean values from the registry."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, key).AndReturn(return_val)
    mox.ReplayAll()
    assert sut._read_bool(stub_key, key) is check_val
    mox.VerifyAll()


def test_read_bool_exceptions(monkeypatch, mox):
    """Test reading boolean values from the registry, in ways that generate exceptions."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, "Alpha").AndReturn(("!Funky!Stuff!", REG_SZ))
    sut._read_value(stub_key, "Bravo").AndRaise(CredentialError("Unable to read"))
    mox.ReplayAll()
    with pytest.raises(CredentialError) as e1:
        sut._read_bool(stub_key, "Alpha")
    assert "not of integer type" in str(e1.value)
    with pytest.raises(CredentialError) as e2:
        sut._read_bool(stub_key, "Bravo")
    assert "Unable to read" in str(e2.value)
    mox.VerifyAll()


def test_read_credentials(monkeypatch, mox):
    """Test reading an entire Credentials object from the registry."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, "url").AndReturn(("http://example.com", REG_SZ))
    sut._read_value(stub_key, "token").AndReturn(("ABCDEFGH", REG_SZ))
    sut._read_value(stub_key, "org_key").AndReturn(("A1B2C3D4", REG_SZ))
    sut._read_value(stub_key, "ssl_verify").AndReturn((0, REG_DWORD))
    sut._read_value(stub_key, "ssl_verify_hostname").AndReturn((0, REG_DWORD))
    sut._read_value(stub_key, "ssl_cert_file").AndReturn(("foo.certs", REG_SZ))
    sut._read_value(stub_key, "ssl_force_tls_1_2").AndReturn((1, REG_DWORD))
    sut._read_value(stub_key, "proxy").AndReturn(("proxy.example", REG_SZ))
    sut._read_value(stub_key, "ignore_system_proxy").AndReturn((1, REG_DWORD))
    mox.ReplayAll()
    creds = sut._read_credentials(stub_key)
    mox.VerifyAll()
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert not creds.ssl_verify_hostname
    assert creds.ssl_cert_file == "foo.certs"
    assert creds.ssl_force_tls_1_2
    assert creds.proxy == "proxy.example"
    assert creds.ignore_system_proxy


def test_read_credentials_defaults(monkeypatch, mox):
    """Test reading a credentials object from the registry that is entirely defaulted."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider()
    mox.StubOutWithMock(sut, '_read_value')
    stub_key = StubKeyObject()
    sut._read_value(stub_key, "url").AndReturn(None)
    sut._read_value(stub_key, "token").AndReturn(None)
    sut._read_value(stub_key, "org_key").AndReturn(None)
    sut._read_value(stub_key, "ssl_verify").AndReturn(None)
    sut._read_value(stub_key, "ssl_verify_hostname").AndReturn(None)
    sut._read_value(stub_key, "ssl_cert_file").AndReturn(None)
    sut._read_value(stub_key, "ssl_force_tls_1_2").AndReturn(None)
    sut._read_value(stub_key, "proxy").AndReturn(None)
    sut._read_value(stub_key, "ignore_system_proxy").AndReturn(None)
    mox.ReplayAll()
    creds = sut._read_credentials(stub_key)
    mox.VerifyAll()
    assert creds.url is None
    assert creds.token is None
    assert creds.org_key is None
    assert creds.ssl_verify
    assert creds.ssl_verify_hostname
    assert creds.ssl_cert_file is None
    assert not creds.ssl_force_tls_1_2
    assert creds.proxy is None
    assert not creds.ignore_system_proxy


def test_get_credentials(monkeypatch, mox):
    """Test getting the credentials from the credential provider."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider('Software\\Test')
    mox.StubOutWithMock(sut, '_open_key')
    mox.StubOutWithMock(sut, '_read_value')
    key1 = StubKeyObject()
    key2 = StubKeyObject()
    sut._open_key(HKEY_CURRENT_USER, 'Software\\Test').AndReturn(key1)
    sut._open_key(key1, 'default').AndReturn(key2)
    sut._read_value(key2, "url").AndReturn(("http://example.com", REG_SZ))
    sut._read_value(key2, "token").AndReturn(("ABCDEFGH", REG_SZ))
    sut._read_value(key2, "org_key").AndReturn(("A1B2C3D4", REG_SZ))
    sut._read_value(key2, "ssl_verify").AndReturn((0, REG_DWORD))
    sut._read_value(key2, "ssl_verify_hostname").AndReturn((0, REG_DWORD))
    sut._read_value(key2, "ssl_cert_file").AndReturn(("foo.certs", REG_SZ))
    sut._read_value(key2, "ssl_force_tls_1_2").AndReturn((1, REG_DWORD))
    sut._read_value(key2, "proxy").AndReturn(("proxy.example", REG_SZ))
    sut._read_value(key2, "ignore_system_proxy").AndReturn((1, REG_DWORD))
    mox.ReplayAll()
    creds = sut.get_credentials('default')
    assert creds.url == "http://example.com"
    assert creds.token == "ABCDEFGH"
    assert creds.org_key == "A1B2C3D4"
    assert not creds.ssl_verify
    assert not creds.ssl_verify_hostname
    assert creds.ssl_cert_file == "foo.certs"
    assert creds.ssl_force_tls_1_2
    assert creds.proxy == "proxy.example"
    assert creds.ignore_system_proxy
    creds2 = sut.get_credentials('default')
    assert creds2 is creds
    mox.VerifyAll()
    key1.check()
    key2.check()


def test_get_credentials_fail_open_section_key(monkeypatch, mox):
    """Test getting the credentials from the credential provider, but the section key won't open."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider('Software\\Test')
    mox.StubOutWithMock(sut, '_open_key')
    mox.StubOutWithMock(sut, '_read_value')
    key1 = StubKeyObject()
    sut._open_key(HKEY_CURRENT_USER, 'Software\\Test').AndReturn(key1)
    sut._open_key(key1, 'notexist').AndRaise(CredentialError("Unable to open registry subkey"))
    mox.ReplayAll()
    with pytest.raises(CredentialError) as e:
        sut.get_credentials('notexist')
    assert "Unable to open registry subkey" in str(e.value)
    mox.VerifyAll()
    key1.check()


def test_get_credentials_fail_open_base_key(monkeypatch, mox):
    """Test getting the credentials from the credential provider, but the base key won't open."""
    monkeypatch.setattr(sys, "platform", "win32")
    sut = RegistryCredentialProvider('Software\\Test')
    mox.StubOutWithMock(sut, '_open_key')
    mox.StubOutWithMock(sut, '_read_value')
    sut._open_key(HKEY_CURRENT_USER, 'Software\\Test').AndRaise(CredentialError("Unable to open registry subkey"))
    mox.ReplayAll()
    with pytest.raises(CredentialError) as e:
        sut.get_credentials('default')
    assert "Unable to open registry subkey" in str(e.value)
    mox.VerifyAll()
