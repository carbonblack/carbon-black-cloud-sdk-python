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

"""Credentials provider that reads the credentials from a file."""

import configparser
import logging
import os
import sys
from pathlib import Path
from cbc_sdk.credentials import Credentials, CredentialProvider
from cbc_sdk.errors import CredentialError

log = logging.getLogger(__name__)


class FileCredentialProvider(CredentialProvider):
    """The object which provides credentials based on a credential file."""
    def __init__(self, credential_file=None):
        """
        Initialize the FileCredentialProvider.

        Args:
            credential_file (object): A string or path-like object representing the credentials file, or a list
                of strings or path-like objects representing the search path for the credentials file.
        """
        self._search_path = []
        self._cached_credentials = None
        self._specific_file_warn = True
        self._general_warn = True
        if credential_file is None:
            filenames = ['credentials.psc', 'credentials.cbc']
            p = Path('.', '.carbonblack')
            local_path = [p / name for name in filenames]
            p = Path.home() / '.carbonblack'
            home_path = [p / name for name in filenames]
            if sys.platform.startswith('win32'):
                p = Path(os.environ.get('windir', 'C:\\Windows'), 'carbonblack')
            else:
                p = Path('/etc', 'carbonblack')
            sys_path = [p / name for name in filenames]
            self._search_path = sys_path + home_path + local_path
        else:
            if isinstance(credential_file, list):
                self._search_path = [Path(n) for n in credential_file]
            else:
                self._search_path = [Path(credential_file)]

    def _file_stat(self, path):
        """
        Return the status of the specified path. This is a "test point" for override during testing.

        Args:
            path (Path): The path to get the status of.

        Returns:
            os.stat_result: The resulting status.
        """
        return path.stat()

    def _security_check(self, path):
        """
        Perform a security check on the specified path object.

        Args:
            path (Path): The path to be security-checked.

        Returns:
            bool: True if the file is OK to use, False if not.
        """
        if not (path.exists() and path.is_file()):
            return False
        if sys.platform.startswith('win32'):
            if self._general_warn:
                log.warning("Security warning: Windows file access to CBC SDK credentials is inherently insecure")
                log.warning("A future version of CBC SDK will default to using a registry-based credentials provider.")
                self._general_warn = False
            return True
        else:
            failmsg = None
            uid = os.geteuid()
            stat_result = self._file_stat(path.parent)
            # Permission bit checks:
            # - None of the "group" or "other" permission bits (0077) should be set
            # - "User read" bit (0400) should always be set
            # - "User execute" bit (0100) should be set on the parent directory, clear on the file itself
            # - "User write" bit (0200) is don't care
            if stat_result.st_uid != uid:
                failmsg = f"Directory {str(path.parent)} not owned by current user"
            elif (stat_result.st_mode & 0o577) != 0o500:
                failmsg = f"Directory {str(path.parent)} has invalid permissions"
            else:
                stat_result = self._file_stat(path)
                if stat_result.st_uid != uid:
                    failmsg = f"File {str(path)} not owned by current user"
                elif (stat_result.st_mode & 0o577) != 0o400:
                    failmsg = f"File {str(path)} has invalid permissions"
            if failmsg:
                # for now, we just emit warning
                if self._specific_file_warn:
                    log.warning("Security warning: A future version of CBC SDK will disallow access to "
                                "the following files altogether unless their permissions are updated.")
                    self._specific_file_warn = False
                log.warning("Security warning: " + failmsg)
            return True

    def get_credentials(self, section=None):
        """
        Return a Credentials object containing the configured credentials.

        Args:
            section (str): The credential section to retrieve.

        Returns:
            Credentials: The credentials retrieved from that source.

        Raises:
            CredentialError: If there is any error retrieving the credentials.
        """
        if section is None:
            section = 'default'
        if self._cached_credentials is None:
            new_creds = {}
            cred_files = [p for p in self._search_path if self._security_check(p)]
            if not cred_files:
                raise CredentialError(f"Unable to locate credential file(s) from {self._search_path}")
            raw_cred_files = [str(p) for p in cred_files]  # needed to support 3.6.0 correctly & for error message
            try:
                parser = configparser.ConfigParser()
                parser.read(raw_cred_files)
                for sect in parser.sections():
                    new_creds[sect] = Credentials({name: value for (name, value) in parser.items(sect)})
            except configparser.Error as e:
                raise CredentialError(f"Unable to read credential file(s) {raw_cred_files}") from e
            self._cached_credentials = new_creds
        if section in self._cached_credentials:
            return self._cached_credentials[section]
        raise CredentialError(f"Section {section} not found in credential file(s)")
