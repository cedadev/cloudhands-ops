..  Titling
    ##++::==~~--''``

Running services
::::::::::::::::

All services should run as the `jasminportal` user. They should be started
sequentially (they write to the database on startup) to ensure correct
initialisation.

First start the indexer::

    $ ~/jasmin-py3.3/bin/cloud-index --interval=15 --index=jasmin-index.wsh --log=cloud-index.log

Then the web service::

    $ ~/jasmin-py3.3/bin/cloud-webserve --port=8080 --db=jasmin-web.sl3 --index=jasmin-index.wsh

Identity manager::

    $ ~/jasmin-py3.3/bin/cloud-identity --interval=20 --db=jasmin-web.sl3 --log=cloud-identity.log

Burst controller::

    $ ~/jasmin-py3.3/bin/cloud-burst --interval=6 --db=jasmin-web.sl3 --log=cloud-burst.log

Reference
=========

The `cloud-index` process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. argparse::
   :ref: cloudhands.web.indexer.parser
   :prog: cloud-index
   :nodefault:

The `cloud-webserve` process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: cloudhands.web.main

.. argparse::
   :ref: cloudhands.web.main.parser
   :prog: cloud-webserve
   :nodefault:

The `cloud-identity` process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. argparse::
   :ref: cloudhands.identity.main.parser
   :prog: cloud-identity
   :nodefault:

The `cloud-burst` process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. argparse::
   :ref: cloudhands.burst.main.parser
   :prog: cloud-burst
   :nodefault:
