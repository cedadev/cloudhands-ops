..  Titling
    ##++::==~~--''``

Integration tests
=================

These instructions help check that the JASMIN portal is correctly deployed
and integrated with other subsystems. The integration tests should be
performed in the Reference environment and are a gate to promotion in to
Production.

User registration
~~~~~~~~~~~~~~~~~

This procedure tests various paths through the user registration process.

0. Prerequisites
----------------

* Set up a `free external email address`_.
  You should record login details and store them in a protected location,
  eg::

    Address: dominic.enderby@contractor.net
    Customer number: 211828816
    Gender: Male
    Date of birth: 01/04/1984
    Country: UK
    Password: D0m1n1c_Enderby
    Security question: What city where you born in?
    Security answer: Harwell

1. Successful registration
--------------------------

1. Visit the JASMIN home page and click on the `Register` link.
    
    * The link takes you to https://jasmin-cloud.jc.rl.ac.uk/register
    * A form is displayed

.. _free external email address: http://www.mail.com/int/
