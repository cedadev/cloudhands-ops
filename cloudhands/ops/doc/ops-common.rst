..  Titling
    ##++::==~~--''``

Essential tasks
===============

.. _install-platform:

Install platform requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The reference platform is Red Hat Enterprise Linux 6.5 with Python 3.3 from RPMs.
To install Python 3.3 on a RHEL platform, execute the following commands::

    $ wget http://jur-linux.org/download/el-updates/6/x86_64/python3-3.3.2-2.el6.x86_64.rpm
    $ wget http://jur-linux.org/download/el-updates/6/x86_64/python3-libs-3.3.2-2.el6.x86_64.rpm

Then, as superuser::

    $ yum localinstall -y python3-3.3.2-2.el6.x86_64.rpm python3-libs-3.3.2-2.el6.x86_64.rpm

.. _portal-account:

Create a non-privileged account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an account for portal operation like this::

    $ adduser jasminportal

Add your public key to ``/home/jasminportal/.ssh/authorized_keys`` to enable
`ssh` access.

Interrogate a database
~~~~~~~~~~~~~~~~~~~~~~

Cloudhands is designed to be a distributed system, comprising agents which
behave according to the messages they get. The history of the state of the
system is stored in one place; the portal database.

The database is therefore an essential reference when investigating system
issues. Knowledge of some simple SQL queries will come in handy.

Here's one useful query which you can run from the command line. It generates a
kind of log of all state changes and resource allocation::

    $ sqlite3 jasmin-web.sl3 "select s.fsm, s.name, art.uuid, a.handle, r.typ
    from
      touches as t left outer join
      resources as r on r.touch_id = t.id join
      actors as a on t.actor_id = a.id join
      artifacts as art on t.artifact_id = art.id join
      states as s on t.state_id = s.id
    order by t.at;"

