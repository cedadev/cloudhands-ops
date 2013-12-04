..  Titling
    ##++::==~~--''``

User Story: Account creation
============================

As a scientist working for STFC I want to add colleagues to my 
JASMIN organisation so that they can begin working on their data.

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
