..  Titling
    ##++::==~~--''``

User Story: Account creation
============================

As a scientist working for STFC I want to add colleagues to my 
JASMIN organisation so that they can begin working on their data.

Elaboration
~~~~~~~~~~~

* PI has Membership with admin role
* New user signs on with email address
* PI searches for new users and adds them to Organisation
* User account enriched with LDAP data

Tasks
~~~~~

* `Discoverable permissions`_
* Multiple authorization protocols
* Cross-domain identity mapping
* Hands-on JASMIN AP
* Hands-on example analytics code
* Explore deploy code
* Explore data access
* Explore process control and events
* Identify indicators

LDAP
~~~~

::

    ldapsearch -x -H ldap://homer.esc.rl.ac.uk -s sub -b "o=hpc,dc=rl,dc=ac,dc=uk" "(&(objectclass=organizationalunit))"

Find POSIX accounts which have no public keys::

    ldapsearch -x -H ldap://homer.esc.rl.ac.uk -s sub -b 'o=hpc,dc=rl,dc=ac,dc=uk' '(&(objectclass=posixAccount)(!(objectclass=ldapPublicKey)))'

Query the subschema for attribute types::

    ldapsearch -x -H ldap://homer.esc.rl.ac.uk -s base -b 'cn=subschema' attributeTypes

or::

    ldapsearch -x -H ldap://homer.esc.rl.ac.uk -s base -b 'cn=subschema' +

.. _search Exchange for emails with LDAP: https://gist.github.com/liveaverage/4503265
