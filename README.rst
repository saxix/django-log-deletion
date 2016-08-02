===================
django-log-deletion
===================

.. image:: https://badge.fury.io/py/django-log-deletion.png
    :target: https://badge.fury.io/py/django-log-deletion

.. image:: https://travis-ci.org/saxix/django-log-deletion.png?branch=master
    :target: https://travis-ci.org/saxix/django-log-deletion

diango app to log model deletion.
It allow to expose records deletion via ws to allow systems syncronization.

Rationale
---------

Sometime you need to keep some tables that live in two different
systems "synchronized", so that the "slave" system always reflect rows in the "master"

Documentation
-------------

The full documentation is at https://django-log-deletion.readthedocs.org.

Quickstart
----------

Install django-log-deletion::

    pip install django-log-deletion

Then use it in a project::

    import log_deletion
