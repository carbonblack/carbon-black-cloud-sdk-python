"""Carbon Black Cloud Python SDK"""

from setuptools import setup
import sys

packages = ['cbc-sdk']

install_requires = [
    'requests',
    'attrdict',
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
    'pytest<=5.0'
    ]

# if sys.version_info < (2, 7):
#     install_requires.extend(['simplejson', 'total-ordering', 'ordereddict'])
if sys.version_info < (3, 0):
    install_requires.extend(['futures'])

setup(
    name='cbc-sdk',
    version='1.0.0',
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
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    scripts=[]
    )
