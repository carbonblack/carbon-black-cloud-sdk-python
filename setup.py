"""VMware Carbon Black Cloud Python SDK"""

from setuptools import setup
import sys
import os

packages = [
    'cbc_sdk',
    'cbc_sdk.audit_remediation',
    'cbc_sdk.cache',
    'cbc_sdk.credential_providers',
    'cbc_sdk.endpoint_standard',
    'cbc_sdk.enterprise_edr',
    'cbc_sdk.platform'
]

install_requires = [
    'requests',
    'cachetools',
    'pyyaml',
    'pika',
    'prompt_toolkit',
    'pygments',
    'python-dateutil',
    'protobuf',
    'solrq',
    'validators'
]

tests_requires = [
    'pytest',
    'pymox'
]

if sys.version_info < (3, 0):
    install_requires.extend(['futures'])


def read(fname):
    """Process files for configuration"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='carbon-black-cloud-sdk',
    version=read('VERSION'),
    url='https://github.com/carbonblack/carbon-black-cloud-sdk-python',
    license='MIT',
    author='VMware Carbon Black',
    author_email='cb-developer-network@vmware.com',
    description='VMware Carbon Black Cloud Python SDK',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=packages,
    include_package_data=True,
    package_dir={'': 'src'},
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_requires=tests_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    scripts=[]
)
