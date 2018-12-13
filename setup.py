#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name='pytrellis-test',
      version='0.1.0',
      description='Python-based test of Trellis docker containers.',
      author='Aaron Coburn',
      author_email='acoburn@apache.org',
      maintainer='Aaron Coburn',
      maintainer_email='acoburn@apache.org',
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet :: WWW/HTTP"],
      url='https://github.com/trellis-ldp/trellis-docker-tests',
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      install_requires=[
          'requests'])
