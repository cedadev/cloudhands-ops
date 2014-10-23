..  Titling
    ##++::==~~--''``

Web API
=======


Essential concepts
~~~~~~~~~~~~~~~~~~

What is REST?
    REST stands for `Representational State Transfer`. It is a set of
    principles to help you design Web APIs so that they are easy to use.

What is HATEOAS?
    HATEOAS stands for `Hypertext As The Engine Of Application State`.
    It is the name given to a particular class of REST APIs.

Design requirements
~~~~~~~~~~~~~~~~~~~

The following requirements are distilled from a reading of current best
practice. See References_ for more details.

*   Web API can return both JSON or HTML, as requested
*   Our JSON contains hypermedia links in the `_links` attribute of each
    object
*   We use the IANA `canonical`, `self`, and `create-form` link relations
    to describe hypermedia targets
*   Our HTML is semantic HTML5 written as well-formed XHTML
*   We render HTML5 forms, allowing client-side input validation with regular
    expressions
*   We use the same regular expressions to perform server-side validation of
    input

Page structure
~~~~~~~~~~~~~~

Each page has the following sections:

**Info**
    Metadata relevant to the page
**Nav**
    Navigable links away from the page
**Items**
    The items visible in the context of the page
**Options**
    The actions possible in the context of the page

Non-canonical items
~~~~~~~~~~~~~~~~~~~

It's often necessary to summarise the state or content of a resource from a
URL which does not represent that object.
In these cases, we always add a link to the `canonical` URI, as shown below:

*JSON*::

    {"items":
     {"1_6":
       {"uuid": "d57e4d1318dd4df88aff394e470e1637", "name": "object-000",
        "_links": [["object-000", "canonical", "/object/{}",
    "d57e4d1318dd4df88aff394e470e1637", "get", [], "View"]]},
      "2_6":
       {"uuid": "adff4b89289642c8a84014452849bf77", "name": "object-001",
        "_links": [["object-001", "canonical", "/object/{}",
    "adff4b89289642c8a84014452849bf77", "get", [], "View"]]},
    .
    .
    .
      "6_6":
      {"uuid": "d9a0dc2479c84e7c9eed33993e39f2f2", "name": "object-005",
       "_links": [["object-005", "canonical", "/object/{}",
    "d9a0dc2479c84e7c9eed33993e39f2f2", "get", [], "View"]]}}
    }

*HTML*::

    <ul>
    <li id="items-1_6">
    <dl id="227634281eed46edb00dd98c1f830445" class="objectview">
    <dt>name</dt>
    <dd>object-000</dd>
    </dl>
    <a rel="canonical" href="/object/227634281eed46edb00dd98c1f830445">View</a>
    </li>
    <li id="items-2_6">
    <dl id="16067afe80df4ac9afcb7ebfd85762ed" class="objectview">
    <dt>name</dt>
    <dd>object-001</dd>
    </dl>
    <a rel="canonical" href="/object/16067afe80df4ac9afcb7ebfd85762ed">View</a>
    </li>
    .
    .
    .
    <li id="items-6_6">
    <dl id="b76f3c8f85c64708a68921f3bd411490" class="objectview">
    <dt>name</dt>
    <dd>object-005</dd>
    </dl>
    <a rel="canonical" href="/object/b76f3c8f85c64708a68921f3bd411490">View</a>
    </li>
    </ul>

References
~~~~~~~~~~

http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
    The original (2000) definition of REST by Roy Fielding.

http://martinfowler.com/articles/richardsonMaturityModel.html
    Martin Fowler's explanation of the different levels of RESTfulness,
    `HATEOS` being the highest category.

http://www.infoq.com/presentations/web-api-html
    This conference video explains a modern HATEOAS API.

https://www.iana.org/assignments/link-relations/link-relations.xhtml
    IANA has started to formalise the terms used to describe the types of link
    relations used in Web APIs.

* https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement.dataset
* http://24ways.org/2011/displaying-icons-with-fonts-and-data-attributes
