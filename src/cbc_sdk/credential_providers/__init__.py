from __future__ import absolute_import

from .file_credential_provider import FileCredentialProvider
from .environ_credential_provider import EnvironCredentialProvider
from .registry_credential_provider import RegistryCredentialProvider
from .aws_sm_credential_provider import AWSCredentialProvider

import platform

# Only import if macOS
if platform.system() == 'Darwin':
    from .keychain_credential_provider import KeychainCredentialProvider
