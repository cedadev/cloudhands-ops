#!/usr/bin/env python
# encoding: UTF-8

import ast
from setuptools import setup
import os.path

try:
    import cloudhands.ops.__version__ as version
except ImportError:
    # Pip evals this file prior to running setup.
    # This causes ImportError in a fresh virtualenv.
    version = str(ast.literal_eval(
                open(os.path.join(os.path.dirname(__file__),
                "cloudhands", "ops", "__init__.py"),
                'r').read().split("=")[-1].strip()))

__doc__ = open(os.path.join(os.path.dirname(__file__), "README.rst"),
               "r").read()

setup(
    name="cloudhands-ops",
    version=version,
    description="Operations for cloudhands PaaS",
    author="D Haynes",
    author_email="david.e.haynes@stfc.ac.uk",
    url="https://github.com/cedadev/cloudhands-ops.git",
    long_description=__doc__,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License"
    ],
    namespace_packages=["cloudhands"],
    packages=[
        "cloudhands.ops",
        "cloudhands.ops.test"
    ],
    package_data={
        "cloudhands.ops": [
            "doc/*.rst",
            "doc/_templates/*.css",
            "doc/html/*.html",
            "doc/html/*.js",
            "doc/html/_sources/*",
            "doc/html/_static/*",
        ],
        "cloudhands.ops.test": [
            "*.rson",
        ],
    },
    install_requires=[
        "sphinxcontrib-seqdiag>=0.7.2",
        "execnet>=1.2.0",
        "PyYAML==3.11",
        "cloudhands-common>=0.31",
    ],
    entry_points={
        "console_scripts": [
            "cloudhands-catalogadmin = cloudhands.ops.catalogadmin:run",
            "cloudhands-orgadmin = cloudhands.ops.orgadmin:run",
        ],
    },
    zip_safe=False
)
