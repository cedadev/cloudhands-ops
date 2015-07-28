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

..code:: bash

    $ yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.rpm
    $ yum install python34u python34u-devel python34u-pip


Creating a venv
:::::::::::::::

The safest way to ensure that Cloudhands is using the correct Python version and libraries
is to use a `Python virtual environment (venv) <https://docs.python.org/3/library/venv.html>`_.

To do this, run the following commands in the root directory of the ``cloudhands-ops`` project:

.. code:: bash

    $ PYENV=~/jasmin-venv                         # Directory where venv will live
    $ python3.4 -m venv --clear $PYENV            # Create a new venv
    $ $PYENV/bin/pip install -r requirements.txt  # Install Cloudhands dependencies
    
    
Adding Cloudhands to the ``PYTHONPATH`` for the venv
====================================================

This method is used during development to allow changes to the Cloudhands source to be picked up.

We assume that all the Cloudhands projects are cloned as sub-directories under a common parent,
referred to as ``$PARENT``.

.. code:: bash

    $ CH_PARENT=$(readlink -e $PARENT)  # Make sure we have the full path to $PARENT
    $ cat << EOF > $PYENV/lib/python3.4/site-packages/cloudhands.pth  # Write a .pth file
    $CH_PARENT/cloudhands-burst
    $CH_PARENT/cloudhands-common
    $CH_PARENT/cloudhands-jasmin
    $CH_PARENT/cloudhands-ops
    $CH_PARENT/cloudhands-web
    EOF


Building the documentation
::::::::::::::::::::::::::

.. code:: bash

    $ cd cloudhands-ops/cloudhands/ops/doc  # Navigate to the docs directory
    $ source $PYENV/bin/activate            # Activate the venv
    $ make html                             # Build the HTML docs
    $ firefox _build/html/index.html        # View the docs


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
