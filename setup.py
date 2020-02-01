"""Python toolkit for Tinker Pop 3 Gremlin Server."""

import os
from setuptools import find_packages, setup


__author__ = 'Jeffrey Phillips Freeman'
__email__ = 'Jeffrey.Freeman@CleverThis.com'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2017, CleverThis, Inc. and contributors'
__credits__ = ['David M. Brown - Project founder']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='goblin',
    version='2.2.1',
    license=__license__,
    author=__author__,
    author_email=__email__,
    description='Goblin OGM for the Tinkerpop 3 Stack,',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='http://goblin-ogm.com',
    download_url='https://github.com/goblin-ogm/goblin/archive/v2.2.1.tar.gz',
    include_package_data=True,
    keywords=['Tinkerpop', 'Tinkerpop3', 'gremlin', 'gremlin-python', 'asyncio', 'graphdb', 'ogm', 'orm'],
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'aiogremlin>=3.3.3',
    ],
    test_suite='tests',
    setup_requires=[
        'pytest-runner>=2.6.2',
    ],
    tests_require=['check-manifest>=0.25',
                   'isort>=4.2.2',
                   'pydocstyle>=1.0.0',
                   'pytest-asyncio>=0.8.0',
                   'pytest-cache>=1.0',
                   'pytest-cov>=2.5.1',
                   'pytest-pep8>=1.0.6',
                   'pytest-timeout>=1.3.4',
                   'pytest>=3.2.1',
                   'uvloop>=0.8.1',
                   'mock'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
