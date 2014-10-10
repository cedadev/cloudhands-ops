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
