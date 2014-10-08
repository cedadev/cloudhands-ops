..  Titling
    ##++::==~~--''``

Deploying the bundle
::::::::::::::::::::

You can transfer the bundle using a variety of methods, `scp` being an obvious
choice. In a benign environment, it can be useful to launch a simple web
server like this::

    $ cd ~/src/cloudhands-ops
    $ ~/pyops-3.3/bin/python -m http.server
    Serving HTTP on 0.0.0.0 port 8000 ...

From the portal host, you can pull the bundle with `wget` (ip address will
vary)::

    $ wget http://130.246.189.180:8000/jasmin-bundle.tar


Installing the bundle
:::::::::::::::::::::

* :ref:`install-platform`
* :ref:`portal-account`
* Log in as non-privileged user

::

    $ python3.3 -m venv pyops-3.3
    $ mkdir deploy
    $ tar -xvf jasmin-bundle.tar -C deploy/

Install `setuptools` from the bundle::

    $ cd deploy
    $ tar -xzvf setuptools-5.7.tar.gz
    $ cd setuptools-5.7
    $ ~/pyops3.3/bin/python3 setup.py install

Install `pip` from the bundle::

    $ tar -xzvf /pip-1.4.1.tar.gz
    $ cd pip-1.4.1
    $ ~/pyops3.3/bin/python3 setup.py install

Install the necessary packages from the bundle::

    $ cd ~ 
    $ ~/jasmin-py3.3/bin/pip install --upgrade --use-wheel --no-index -f file:///home/jasminportal/deploy -r deploy/requirements.txt
    $ ~/jasmin-py3.3/bin/pip install --upgrade --use-wheel --no-index -f file:///home/jasminportal/deploy cloudhands-ops cloudhands-web cloudhands-burst cloudhands-jasmin
