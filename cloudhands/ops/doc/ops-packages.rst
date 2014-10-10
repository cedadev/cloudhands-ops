..  Titling
    ##++::==~~--''``

Building the packages
:::::::::::::::::::::

Log in to the :ref:`build-environment` as the non-privileged user `jasminportal`.

Change directory to the `cloudhands-ops` package::

    $ cd src/cloudhands-ops

Invoke the :ref:`check-script` script to run the unit tests::

    $ ./check.sh --novenv --nolint --nopep8

Invoke the :ref:`build-script` script to create the package bundle::

    $ ./build.sh --novenv --nopush --nosign

The bundle will be created as a `tar` archive named `jasmin-bundle.tar`.
