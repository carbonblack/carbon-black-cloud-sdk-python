"""Carbon Black Cloud Python SDK"""

from setuptools import setup
import os

packages = [
    'cbc_sdk',
    'cbc_sdk.audit_remediation',
    'cbc_sdk.cache',
    'cbc_sdk.credential_providers',
    'cbc_sdk.endpoint_standard',
    'cbc_sdk.enterprise_edr',
    'cbc_sdk.platform',
    'cbc_sdk.workload'
]

install_requires = [
    'requests',
    'pyyaml',
    'python-dateutil',
    'schema',
    'solrq',
    'validators',
    'jsonschema',
    "keyring;platform_system=='Darwin'",
    'boto3',
    "backports-datetime-fromisoformat==2.0.1; python_version < '3.11'",
]

extras_require = {
    "test": [
        'pytest==7.2.1',
        'pymox==1.0.0',
        'coverage==6.5.0',
        'flake8==5.0.4',
        'flake8-colors==0.1.9',
        'flake8-docstrings==1.7.0',
        'pre-commit>=2.15.0',
        'requests-mock==1.10.0'
    ]
}


def read(fname):
    """Process files for configuration"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='carbon-black-cloud-sdk',
    version=read('VERSION'),
    url='https://github.com/carbonblack/carbon-black-cloud-sdk-python',
    license='MIT',
    author='Carbon Black',
    author_email='cb-developer-network@vmware.com',
    description='Carbon Black Cloud Python SDK',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=packages,
    include_package_data=True,
    package_dir={'': 'src'},
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    scripts=[]
)
