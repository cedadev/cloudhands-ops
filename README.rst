..  Titling
    ##++::==~~--''``

Cloudhands is a 'Platform as a Service' (PaaS) framework. It gives you the
software necessary to run a private computing cloud for your business or
organisation. A key objective is support for multiple back-end providers.


This release
::::::::::::

Cloudhands is a very young project. It is currently under heavy development,
with fixes and features added daily. 

You are welcome to give Cloudhands a try, but be aware that some parts
of the codebase lack the test coverage of a finished product. Improvements
to documentation are ongoing.


Requirements
::::::::::::

The reference platform is Centos 6.6 with Python 3.4. To install Python 3.4 on
a clean Centos 6.6 installation, the following can be used:

.. code:: bash

    $ yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.rpm
    $ yum install python34u python34u-devel python34u-pip


Creating a venv
:::::::::::::::

The safest way to ensure that Cloudhands is using the correct Python version and libraries
is to use a `Python virtual environment (venv) <https://docs.python.org/3/library/venv.html>`_.

To do this, run the following commands in the root directory of the ``cloudhands-ops`` project:

.. code:: bash

    # Directory where venv will live
    $ PYENV=~/jasmin-venv

    # Create a new venv
    $ python3.4 -m venv --clear $PYENV

    # Install Cloudhands dependencies
    $ $PYENV/bin/pip install -r requirements.txt
    
    
Installing Cloudhands in development mode
=========================================

This section assumes that all the Cloudhands projects are cloned as sub-directories in
the current working directory.

Installing Cloudhands in development mode, via setuptools, ensures that entry points are set up
properly, but instead of copying files to `site-packages` it creates `egg-link` files that act
like symbolic links. This ensures that changes we make to the source code are instantly picked
up by the venv.

.. code:: bash

    # Activate the venv
    $ source $PYENV/bin/activate
    
    # Install each cloudhands project in development mode
    $ for proj in `ls cloudhands-*`; do
        python setup.py develop
    done
    
    # Deactivate the venv
    $ deactivate


Building the documentation
::::::::::::::::::::::::::

.. code:: bash

    # Activate the venv
    $ source $PYENV/bin/activate

    # Navigate to the docs directory
    $ cd cloudhands-ops/cloudhands/ops/doc
    # Build the HTML docs
    $ make html
    # View the docs
    $ firefox _build/html/index.html

    # Deactivate the venv
    $ deactivate


Roadmap
:::::::

Cloudhands's mission is to provide a robust Pythonic framework to provision
and manage scientific analysis in the cloud.

It is developed in the UK and released to the public under a `BSD licence`_.

The API may change significantly as the project proceeds. At this early stage,
you should only use the latest release, which may not be compatible with
previous versions.


Can you help?
=============

* If you've spotted a bug in Cloudhands, please let us know so we can fix it.
* If you think Cloudhands lacks a feature, you can help drive development by
  describing your Use Case.


:author:    D Haynes
:contact:   david.e.haynes@stfc.ac.uk
:copyright: 2013 UK Science and Technology Facilities Council
:licence:   BSD

.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _BSD licence: http://opensource.org/licenses/BSD-3-Clause
