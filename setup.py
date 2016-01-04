#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
from setuptools import setup

install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
        name='pyswedbank',
        packages=['pyswedbank'],
        version='1.1',
        install_requires=reqs,
        description='A python wrapper for swedbank api.',
        author='Magnus Knutas',
        author_email='magnusknutas@gmail.com',
        url='https://github.com/spaam/swedbank-cli',
        keywords=['banking', 'api', 'wrapper'],  # arbitrary keywords
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],
        license='MIT',
        scripts=['pyswedbank/swedbank-cli']
)
