..  Titling
    ##++::==~~--''``

User lifecycle
==============

One of the tasks of the portal is to hide from the user the complexity of
managing credentials required by:

* funding bodies who control access to on-site resources
* the authentication systems implemented by VM operating systems
* back-end providers (VMWare, Azure, Amazon, etc)

Organisation membership
~~~~~~~~~~~~~~~~~~~~~~~

Membership of an organisation is administered by a named individual (typically
the `principal investigator` of the project). That individual has the authority
to admit others to the organisation, giving them use of the resources allocated
to it.

In order to identify a prospective member, the administrator must at a
miniumu:

* know the surname of the individual
* know an email address where he can be reached

Account properties
~~~~~~~~~~~~~~~~~~

Session credentials
~~~~~~~~~~~~~~~~~~~


Elaboration
~~~~~~~~~~~

* PI requires Membership with admin role
* PI searches for new user from LDAP records
* PI selects user and generates an invitation
* (Out of band) PI sends to user a link to the invitation
* New user signs on with email address

LDAP
~~~~

This query finds the list of live users::

    ldapsearch -x -H ldap://homer.esc.rl.ac.uk -s sub -b 'ou=ceda,ou=People,o=hpc,dc=rl,dc=ac,dc=uk' '(&(objectclass=posixAccount)(objectclass=ldapPublicKey))'

It might also be possible to `search Exchange for emails with LDAP`_.

.. _search Exchange for emails with LDAP: https://gist.github.com/liveaverage/4503265
