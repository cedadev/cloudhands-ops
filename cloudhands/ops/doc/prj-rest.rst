..  Titling
    ##++::==~~--''``


RESTful design
==============

API elaboration
~~~~~~~~~~~~~~~

* Design the landing page from the human perspective of workflow
* Each widget is a client of a resource
* Workflow use of resources drives navigation schema
* Each returned object has a 'self' link
* Forms are identified via their 'doc' URL and fragment

.. _Fielding dissertation: http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
.. _maturity model: http://martinfowler.com/articles/richardsonMaturityModel.html
.. _hypermedia APIs: http://oredev.org/2010/sessions/hypermedia-apis
.. _IANA link relations: https://www.iana.org/assignments/link-relations/link-relations.xhtml
.. _Requests library can send JSON encoded data: http://www.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
.. _Pyramid can accept JSON encoded data: http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/webob.html#dealing-with-a-json-encoded-request-body
