**********
Sew django
**********

.. image:: https://travis-ci.org/jacoor/sew_django.png?branch=develop   :target: https://travis-ci.org/jacoor/sew_django

.. contents::

Prerequisites
=============
Python > 2.6, PIP, Homebrew (Mac OSX), Git (and a github account), VirtualEnv (mkvirtualenv helper script)

Dev requirements
================
**MySQL, Apache**


*Ubuntu/Mint*

::

    sudo apt-get install git python-dev python-pip libxml2-dev libxslt1-dev libmysqlclient-dev


*All dist*

::

    sudo easy_install pip
    sudo pip install flup


Getting Started
===============
Preparing virtualenv paths (optional if your profile doesn't have it).

::

    export WORKON_HOME=~/Envs
    source /usr/bin/virtualenvwrapper_lazy.sh or source /usr/local/bin/virtualenvwrapper_lazy.sh

Start by creating a virtual environment using the helper scripts provided. Do not include the systems site-packages.

::

    mkvirtualenv sew --no-site-packages
    workon sew

Clone the Github repository if you have not done so yet. You will need a git account to do this.

::

    git@github.com:jacoor/sew_django.git

Move into the newly created Project Data folder and install the Python requirements using PIP, which are located in the requirements.txt file. Ensure the platform requirements are installed (python-dev/python-devel).

::

    pip install -r requirements.txt

Create local settings or copy from config into your project root and custom it.

::

    cp config/local_settings.py styleguide/local_settings.py

Upon successful completion of the installation initialize the database. (NOTE: database must be running.)

::

    ./manage.py syncdb --migrate


Get Sass (OSX. for linux you need to do your own research :P )

::
    {<img src="https://travis-ci.org/jacoor/sew_django.png?branch=develop" alt="Build Status" />}[https://travis-ci.org/jacoor/sew_django]

    sudo gem install sass
    sudo gem install compass

Be sure to have 

::

    INTERNAL_IPS = (
        "127.0.0.1",
    ) 

in your local settings, otherwise live reload of css will not work. 


Create the static

::

    ./manage.py collectstatic -v0 --noinput && ./manage.py compress -f



Launching
=========
`python sass.py` - this makes sass watch for scss file change, thus enabling live css reload
`./manage.py runserver`


Git Flow
========
`git flow init -d`
If you run into problems:
`git checkout master && git pull && git checkout develop && git pull && git flow init -d`
