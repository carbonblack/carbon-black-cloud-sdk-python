"""Carbon Black Cloud Python SDK"""

from setuptools import setup
import sys
import os

packages = ['cbc_sdk']

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

# if sys.version_info < (2, 7):
#     install_requires.extend(['simplejson', 'total-ordering', 'ordereddict'])
if sys.version_info < (3, 0):
    install_requires.extend(['futures'])


def read(fname):
    """Process files for configuration"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='cbc_sdk',
    version=read('VERSION'),
    url='https://github.com/carbonblack/cbc-sdk-python',
    license='MIT',
    author='Carbon Black',
    author_email='dev-support@carbonblack.com',
    description='Carbon Black Cloud Python SDK',
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
