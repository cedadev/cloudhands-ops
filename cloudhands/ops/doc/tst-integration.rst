..  Titling
    ##++::==~~--''``

Integration tests
=================

These instructions help check that the JASMIN portal can be correctly deployed
and integrated with other subsystems. The integration tests should be
performed in the Reference environment and are a gate to promotion into
Production.

.. note::

   You can perform these tests in the development environment, but all URLs
   will have their root at http://jasmin-cloud.jc.rl.ac.uk:8080, not as
   specified below.

JVO Onboarding
~~~~~~~~~~~~~~

This procedure begins with a fresh database. It tests that a new JVO can be
created along with its controlling admin user.

0. Prerequisites
----------------

    * Access to your on-site email account.
    * A running portal with a fresh database.

1. Verify guest access
----------------------

0. Prerequisites

    * Web portal is running.
    * Identity controller is running.

1. Visit https://jasmin-cloud.jc.rl.ac.uk

    * The home page is displayed.
    * The `Organisations` menu has no entries.

2. Add a JVO admin with the `orgadmin` script
---------------------------------------------

0. Prerequisites

    * You are logged in to the management node as a devops user.
    * You have installed the devops tools according the site-specific
      documentation.

1. Invoke the `orgadmin` script to create a fictional user and JVO, supplying your
   own email address for confirmation::

        ~/pyops-3.3/bin/cloudhands-orgadmin \
        --host=jasmin-cloud.jc.rl.ac.uk --identity=~/.ssh/id_rsa-jasminvm.pub \
        --db=/home/jasminuser/jasmin-web.sl3 \
        --account=bcumberbat \
        --email=<your_email_address> \
        --surname=Cumberbatch \
        --organisation=STFCloud \
        --activator=/root/bootstrap.sh \
        --providers=cloudhands.jasmin.vcloud.stfccloud-ref.cfg

   * The utility runs and emits a log trace similar to the following::

        2014-09-11 09:57:34,154 INFO    cloudhands.ops.orgadmin|Sending from jasmin-cloud.jc.rl.ac.uk.
        2014-09-11 09:57:35,759 INFO    cloudhands.ops.orgadmin|('user', 'bcumberbat', '52ebc31e02d74d1d9ec36fde6e4fe37d')
        2014-09-11 09:57:35,814 INFO    cloudhands.ops.orgadmin|('provider', 'cloudhands.jasmin.vcloud.stfccloud-ref.cfg', 'ac336c7059ef40eabd139f0aa133c474')
        2014-09-11 09:57:35,814 INFO    cloudhands.ops.orgadmin|('subscription', '1095d56df5c3430fa14dc139202a1cd7')
        2014-09-11 09:57:35,814 INFO    cloudhands.ops.orgadmin|('organisation', 'STFCloud', '8df90b357f0f46e89f1c558a6cd7e78f')
        2014-09-11 09:57:35,841 INFO    cloudhands.ops.orgadmin|('membership', 'admin', '8edcf1c4a28c45279b0498808e14e86d')
        2014-09-11 09:57:35,874 INFO    cloudhands.ops.orgadmin|('registration', '651ff2f1822948dcbd7e76212359ea82')

3. Activate the administrator account
-------------------------------------

1. Visit your email account and check the Inbox

    * The Inbox contains a new message entitled `JASMIN notification`.
    * The message contains a link to a resource under
      https://jasmin-cloud.jc.rl.ac.uk/membership.
       
      *NB: messages can take several minutes to be delivered*.

2. Click the confirmation link.

    * The linked page redirects you to a resource under
      https://jasmin-cloud.jc.rl.ac.uk/registration. The page is entitled
      `bcumberbat`.
    * The `Organisations` menu has the entry `STFCloud`.
    * A form is displayed with the title `Set your password`.
      It has a `Password` field and a `Change` button.

3. Enter a password for the user account.

    * Password: ``Cumb3rb@tch``

4. Click the button `Change`.

    * You are redirected to the login page.
    * A form is displayed with the title `User login`.
      It has two fields and a `Log in` button.
      The fields are `Username`, and `Password`.
    * The Username field has the value `bcumberbat` and is styled green.
    * The Password field is empty and styled red.

5. Enter the account password.

    * Password: ``Cumb3rb@tch``
    * The Password field is styled green.

6. Click `Log in`.

    * You are redirected to the home page.

User registration
~~~~~~~~~~~~~~~~~

This procedure tests various paths through the user registration process.

0. Prerequisites
----------------

* Set up a `free external email address`_.
  You should record login details and store them in a protected location
  (not in a code repository as this example does)::

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
    
    * The link takes you to https://jasmin-cloud.jc.rl.ac.uk/registration
    * A form is displayed with three fields and a `Register me` button.
      The fields are `Username`, `Password`, `Email`.

2. Enter registration details for a new user.

    * Username: ``denderby``
    * Password: ``D0m1n1c_Enderby``
    * Email: ``dominic.enderby@contractor.net``

3. Click the button `Register me`.

    * You are redirected to a confirmation page.
    * You can navigate by link to the home page.

2. Successful confirmation
--------------------------

0. Prerequisites
    * `1. Successful registration`_.


1. Visit email account and check Inbox

    * The Inbox contains a new message entitled `JASMIN notification`.
       
      *NB: messages can take several minutes to be delivered*.

    .. image:: _static/register_confirm_email-lab.png

2. Click the confirmation link.

    * The linked page redirects you to https://jasmin-cloud.jc.rl.ac.uk/login.

3. Successful login
-------------------

0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.

1. Visit https://jasmin-cloud.jc.rl.ac.uk/login.

    * A form is displayed with two fields and a `Log in` button.
      The fields are `Username`, `Password`.
    * The Username field is styled red and asks for a name 8 - 10 characters
      long.
    * The Password field is styled red and asks for a name 8 - 20 characters
      long.

        * at least one lowercase letter
        * at least one uppercase letter
        * at least one numeric digit
        * at least one special character
        * no whitespace.

2. Enter a valid username.

    * The Username field is styled green

3. Enter a valid password.

    * The Password field is styled green.

4. Click `Log in`.

    * You are redirected to the home page.

4. Unsuccessful login (password)
--------------------------------

0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.

1. Proceed with `3. Successful login`_, stopping before step 3.

2. Enter a false password which conforms to the password criteria.
   Example: ``N0t_MyPa55w0rd``.

    * The Password field is styled green.

3. Click `Log in`.
    * A yellow message appears: `Login failed. Please try again`.
    * The Username field is empty and styled red.
    * The Password field is empty and styled red.

5. LDAP entry created on first login
------------------------------------

.. important::

   The behaviour described in this section is undesirable on a public facing
   network as it constitutes `resource exhaustion`_ of unique `cn` names
   and (ultimately) `uidNumbers`.
 
0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.
    * `3. Successful login`_.

1. View LDAP record for `denderby`. Use the `ldapvi` program like this::

    ldapvi -d -h ldap-test.jc.rl.ac.uk -w password \
    --user "cn=dehaynes,ou=ceda,ou=People,o=hpc,dc=rl,dc=ac,dc=uk"

   Use the `G` key to navigate to the end of the file.

    * An LDAP record has been created as follows (numbers and password will
      vary)::

        cn=denderby,ou=jasmin2,ou=People,o=hpc,dc=rl,dc=ac,dc=uk
        objectClass: top
        objectClass: person
        objectClass: inetOrgPerson
        objectClass: organizationalPerson
        objectClass: posixAccount
        description: JASMIN2 vCloud registration
        sn: UNKNOWN
        cn: denderby
        uid: denderby
        uidNumber: 7010002
        gidNumber: 7010002
        homeDirectory: /home/denderby
        mail: dominic.enderby@contractor.net
        userPassword: {SSHA}Psxobi4ydMILrlSjufFzlyi/4d6Bo8ko


6. Successful key add to account
--------------------------------

0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.
    * `3. Successful login`_.

1. Visit the `Account` page.

    * The account shows a `UId`.
    * The account shows a `Name`.
    * The account shows a `Email`.
    * The account shows a `Password` (obscured).
    * The account has a form entitled `Paste your key`.

2. Paste a `ssh-rsa` key into the form and click `Add`.

    * The key is added to the account.

Appliance lifecycle
~~~~~~~~~~~~~~~~~~~

This procedure allows a test of the integration with the VMWare back end. It
is only available in the `Lab` environment.

1. Login (demo user)
--------------------

0. Prerequisites
    * Demo portal is running

1. Visit https://jasmin-cloud.jc.rl.ac.uk/login.

    * A form is displayed with two fields and a `Log in` button.
      The fields are `Username`, `Password`.

2. Enter the admin username for the demo: ``bcampbel``.

    * The Username field is styled green.

3. Enter the password for the demo: ``IWannaS33TheDemo!``.

    * The Password field is styled green.

4. Click `Log in`.

    * You are redirected to the home page.

2. Launch an item from the catalogue
------------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.

1. From the `Organisations` dropdown, select `EOSCloud`.

    * You are sent to the EOSCloud JVO page.

2. From the breadcrumb menu, select `Catalogue`.

    * The catalogue page is populated with five items.
    * Clicking each item shows a name in bold, a description, and an `OK`
      button.

3. Select a catalogue item and click `OK`.

    * You are sent to the `Configure appliance` page.
    * There is a form called `General information` with three fields and an
      `OK` button. The fields are `Name`, `Description`, and `Ipaddr`.

4. Create a new appliance by filling the fields as follows:

    * Name: ``test_01``
    * Description: ``test appliance``

5. Click the button `OK`.

    * You are redirected to the EOSCloud JVO page.

3. Monitor the appliance lifecycle
----------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.

1. Note the initial state

    * The appliance begins in the `pre_provision` state.

2. Observe state updates.

    * The appliance state updates itself to show `provisioning` (~5s).
    * The appliance state updates itself to show `operational` (~60s).
    * The appliance item has a `Stop` and a `Check` button.
    * The appliance has a non-routable IP address. Note this value.

4. Check the deployed appliance
-------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.
    * `3. Monitor the appliance lifecycle`_.

1. Check the VApp in the `vCloud Director` GUI.

    * The vApp called `test_01` exists.
    * The vApp state is `Stopped`.

2. Check the customization script as follows:

   #. Click the vApp named `test_01`.
   #. Select the `Virtual Machine` tab.
   #. Click on the name of the VM inside the vApp.
   #. Click the `Guest OS Customization` tab.
   #. Scroll down to the `Customization Script` section.

    * The script contains an RSA public key.

3. Check the Edge gateway in the `vCloud Director` GUI as follows:

   #. Click the `Administration` tab and select the item named
      `un-managed_tenancy_test_org-std-compute-PAYG`.
   #. Click the `Edge Gateways` tab and select `jasmin-priv-external-network`.
   #. Click the dropdown settings menu and select `Edge Gateway Services...`

    * The `NAT` tab shows a DNAT rule for the IP address you noted in
      `3. Monitor the appliance lifecycle`_ above. It allows port 22 only.
      Note the public IP it routes to.
    * The `Firewall` tab shows a rule for the routable IP you noted here.
      It allows port 22 only.

5. Set the appliance running
----------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.
    * `3. Monitor the appliance lifecycle`_.
    * `4. Check the deployed appliance`_.

1. Click the button `Start`.

    * The appliance state updates itself to show `pre_start`.
    * The appliance state updates itself to show `running` (~2s).
    * The buttons are displayed as follows; `Stop`, `Check`.

1. Refresh the view `vCloud Director` GUI. Check the VApp status.

    * The vApp state is `Running`.

.. _free external email address: http://www.mail.com/int/
.. _resource exhaustion: https://www.owasp.org/index.php/Resource_exhaustion 
