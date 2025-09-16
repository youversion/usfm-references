#!/usr/bin/env python
"""Setup for distribution of USFM References package."""

import ast
import re
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("usfm_references/__init__.py", "rb") as fh_init:
    version = str(ast.literal_eval(_version_re.search(fh_init.read().decode("utf-8")).group(1)))

with open("README.md", "rb") as fh_desc:
    long_description = fh_desc.read().decode("utf-8")


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import shlex

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="usfm-references",
    version=version,
    url="https://github.com/bbelyeu/usfm-references",
    download_url="https://github.com/bbelyeu/usfm-references/archive/{}.zip".format(version),
    license="MIT",
    author="Brad Belyeu",
    author_email="bradleylamar@gmail.com",
    description="Tools to work with USFM references",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[],
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
