""" Setup script for the dxlstreamingclient package """

# pylint: disable=no-member, no-name-in-module, import-error, wrong-import-order
# pylint: disable=missing-docstring, no-self-use

from __future__ import absolute_import
import glob
import os
from setuptools import Command, setup
import setuptools.command.sdist
import distutils.command.sdist
import distutils.log
import subprocess
import sys


# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

VERSION_INFO = {}
CWD = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(CWD, "dxlstreamingclient", "_version.py")) as f:
    exec(f.read(), VERSION_INFO) # pylint: disable=exec-used

class LintCommand(Command):
    """
    Custom setuptools command for running lint
    """
    description = 'run lint against project source files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce("Running pylint for library source files, tools, and tests",
                      level=distutils.log.INFO)
        subprocess.check_call(
            ["pylint", "dxlstreamingclient", "tests"] +
            glob.glob("*.py"))
        self.announce("Running pylint for samples", level=distutils.log.INFO)
        subprocess.check_call(["pylint"] + glob.glob("sample/*.py") +
                              glob.glob("sample/**/*.py") +
                              ["--rcfile", ".pylintrc.samples"])

class CiCommand(Command):
    """
    Custom setuptools command for running steps that are performed during
    Continuous Integration testing.
    """
    description = 'run CI steps (lint, test, etc.)'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command("lint")
        self.announce("Running tests", level=distutils.log.INFO)
        subprocess.check_call([sys.executable, "-m", "pytest", "tests"])

TEST_REQUIREMENTS = [
    # nose is unmaintained and does not work on Python >= 3.10; pynose is a
    # maintained drop-in fork providing the same ``nose`` package.
    'nose; python_version < "3.10"',
    'pynose; python_version >= "3.10"',
    "pytest",
    "mock",
    'astroid<2.3.0; python_version < "3.10"',
    'pylint<=2.3.1; python_version < "3.10"',
    'pylint; python_version >= "3.10"'
]

setup(
    # Package name:
    name="dxlstreamingclient",

    # Version number:
    version=VERSION_INFO["__version__"],

    # Package requirements
    install_requires=[
        "furl",
        "requests",
        "retrying"
    ],

    tests_require=TEST_REQUIREMENTS,

    extras_require={
        "test": TEST_REQUIREMENTS
    },

    # Python version requirements
    python_requires=">=3.8",

    # Package author details:
    author="McAfee LLC",

    # License
    license="Apache License 2.0",

    # Keywords
    keywords=['opendxl', 'dxl', 'mcafee', 'client', 'streaming'],

    # Packages
    packages=[
        "dxlstreamingclient",
        "dxlstreamingclient._config",
        "dxlstreamingclient._config.sample"],

    package_data={
        "dxlstreamingclient._config.sample" : ['*']},

    # Details
    url="http://www.mcafee.com",

    description="OpenDXL Streaming client library",

    long_description=open('README').read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14"
    ],

    cmdclass={
        'ci': CiCommand,
        'lint': LintCommand
    }
)
