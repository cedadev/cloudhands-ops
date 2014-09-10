#!/usr/bin/env python
# encoding: UTF-8

from setuptools import setup
import os.path

import cloudhands.ops

__doc__ = open(os.path.join(os.path.dirname(__file__), "README.rst"),
               "r").read()

setup(
    name="cloudhands-ops",
    version=cloudhands.ops.__version__,
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
    package_data={"cloudhands.ops": [
                    "doc/*.rst",
                    "doc/_templates/*.css",
                    "doc/html/*.html",
                    "doc/html/*.js",
                    "doc/html/_sources/*",
                    "doc/html/_static/*",
                    ]},
    install_requires=[
        "sphinxcontrib-seqdiag>=0.7.2",
        "execnet>=1.2.0",
        "PyYAML==3.11",
        "cloudhands-common>=0.29",
    ],
    entry_points={
        "console_scripts": [
            "cloudhands-orgadmin = cloudhands.ops.orgadmin:run",
        ],
    },
    zip_safe=False
)
