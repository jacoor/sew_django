**********
Django form widgets
**********

.. contents::

Prerequisites
=============
Django

Usage
=====

::

    {% for f in form %}
        {% include "inc/forms/form_as_ul.html" with f=f %}
    {% endfor %}