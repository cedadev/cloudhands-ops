..  Titling
    ##++::==~~--''``

Git Workflow
==============

Challenges
~~~~~~~~~~

*   The Cloudhands software is stored in multiple git repositories
*   To release the software is to aggregate this code from those repositories
    as a single namespace package
*   Some of those repositories implement the site-specific behaviour of a
    project partner
*   Project partners have different aspirations and intentions for the codebase
*   Core packages must support partner feature sets 

Best practice
~~~~~~~~~~~~~

There are several documented processes for working with git in a collaborative
environment. Each of them recommends strategies for branching, adding features,
and merging.

Of these, the Branch Per Feature (BPF) model represents a well-evolved good fit
for our purposes, based on the challenges stated above.

`BPF explained here`_.

Your responsibility as a developer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code you write for your own project is your own affair. Your responsibility
to others begins when you contribute it to a shared repository.

Git is hard to use in this environment without making mistakes. The attitudes
we recommend are:

* humble in the face of complexity
* respectful of the intentions of others
* meticulous in testing your product 

The very first thing you should do now is `read this description of the
workflow`_ so that you can start to familiarise yourself with the process.
It may take a while to assimilate.

Summary of workflow
~~~~~~~~~~~~~~~~~~~

*   The master branch contains the last known good release.
*   Create a single Trac ticket to represent your feature release.
*   Create a git feature branch in each repository where work is to be done.
    Name each branch after the ticket, eg: Trac_0123.
*   Developers regularly create an `integration` branch from master to check that
    upcoming features can be merged cleanly from their branches.
*   We capture integration issues in the Trac ticket for each feature.
    Discussion between partners here.
*   Optionally: record any merge conflict resolution using `git rerere` and
    commit to ``cloudhands-ops/git/rerere`` cache.
*   When a feature set is agreed for release, a `qa` branch is created from
    master and has features merged into it.
*   QA team tests the `qa` branch in Reference environment.
*   When `qa` branch is good it is merged into master and deployed to Production.

.. _BPF explained here: https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow
.. _read this description of the workflow: https://www.acquia.com/blog/pragmatic-guide-branch-feature-git-branching-strategy
