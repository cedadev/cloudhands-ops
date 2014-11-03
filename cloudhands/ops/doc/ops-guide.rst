.. _operations-guide:

Operations guide
::::::::::::::::

This guide gives you the ability to deploy and administer services with the
`cloudhands` software. The software consists of several separate packages:

+-------------------+-----------------------------------------------+-----------------------------+
| Package           | git clone `<url>`                             | Description                 |
+===================+===============================================+=============================+
| cloudhands-common | `git@github.com:cedadev/cloudhands-common.git`| Common types, utilities and |
|                   |                                               | database schema             |
+-------------------+-----------------------------------------------+-----------------------------+
| cloudhands-burst  | `git@github.com:cedadev/cloudhands-burst.git` | Agent-based interfacing to  |
|                   |                                               | provider APIs               |
+-------------------+-----------------------------------------------+-----------------------------+
| cloudhands-web    | `git@github.com:cedadev/cloudhands-web.git`   | Identity management and     |
|                   |                                               | web portal application      |
+-------------------+-----------------------------------------------+-----------------------------+
| cloudhands-jasmin | `git@proj.badc.rl.ac.uk:cloudhands-jasmin`    | Site-specific configuration |
|                   |                                               | for JASMIN infrastructure   |
|                   |                                               | (private)                   |
+-------------------+-----------------------------------------------+-----------------------------+
| cloudhands-ops    | `git@github.com:cedadev/cloudhands-ops.git`   | Contains this manual, some  |
|                   |                                               | operations scripts and all  |
|                   |                                               | third-party dependencies    |
+-------------------+-----------------------------------------------+-----------------------------+

You should check out the source repositories under a common directory `src` as shown::

    src
    |-- cloudhands-burst
    |   `-- cloudhands
    |       `-- burst
    |           |-- main.py
    |           `-- test
    |-- cloudhands-common
    |   `-- cloudhands
    |       `-- common
    |           `-- test
    |-- cloudhands-jasmin
    |   `-- cloudhands
    |       `-- jasmin
    |-- cloudhands-ops
    |   |-- build.sh
    |   |-- check.sh
    |   |-- cloudhands
    |   |   `-- ops
    |   |       `-- doc
    |   |-- design
    |   `-- vendor
    `-- cloudhands-web
        `-- cloudhands
            |-- identity
            |   |-- main.py
            |   `-- test
            `-- web
                |-- demo.py
                |-- indexer.py
                |-- main.py
                |-- static
                |   |-- css
                |   `-- img
                |-- templates
                `-- test


Essential concepts
==================

If you already have experience of systems administration, you may be used to
a different  terminology than is used in this guide. Here's what you need to
know:
 
Revisions and Versions
~~~~~~~~~~~~~~~~~~~~~~

* A revision is an integer or a commit id like `0dbf4c8ba484756563f0dfece9ed25552fab2095`.
  A revision is used to reference the state of code in a source repository.
* A version is an identifier with numerical fields and other modifiers, like `0.44c1`.
  This is a label we apply to a package of software we intend to deploy.
  The format for Python package versioning is defined in `PEP 440`_.

The Bundle
~~~~~~~~~~

We will describe later on how to create a bundle of the `cloudhands` software,
as a means of easy transportation and deployment. A bundle consists of the
following:

The Release
    A Python source distribution (tar.gz) for each of the namespace packages in
    the `cloudhands` project.
 
Vendor packages
    A copy of all Python dependency packages. These are to be found in the
    `vendor` directory of the `cloudhands-ops` source tree. 

All these items are packed together in a file archive, typically named
`jasmin-bundle.tar`.

Procedures
==========

.. toctree::
   :maxdepth: 1

   ops-common
   ops-platform
   ops-packages
   ops-deploy
   ops-services
   ops-onboard

References
==========

* `Structural and naming conventions for Python packages`_
* `Format specifications for package versioning`_

.. _PEP 440: http://legacy.python.org/dev/peps/pep-0440/ 
.. _Structural and naming conventions for Python packages: http://www.python.org/dev/peps/pep-0423/
.. _Format specifications for package versioning: http://www.python.org/dev/peps/pep-0386/
