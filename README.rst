Dopr
========

A minimal CLI tool for Provisionning Digital Ocean Droplets

Pre-requisites
------

- Pipenv Installed
- Set you Digital Ocean Token as an environment variable **DO_TOKEN**

Installation
------

::

    $ make install
    $ python setup.py bdist_wheel
    $ pip install -I dist/dopr-0.1.0-py2.py3-none-any.whl

Usage
------

List Droplets :

::

    $ dopr --list


Destroy All droplets

::

    $ dopr --clean


Create Droplets :

::

    $ dopr -c 1 centos s-1vcpu-1gb


Create Droplets and Install some packages :

::

    $ dopr -c 1 centos s-1vcpu-1gb -p python,vim

Create Droplets with an Ansible inventory 

::

    $ dopr -c 3 ubuntu s-1vcpu-1gb --with-inventory app,db,redis


Droplets Status :

::

    $ dopr --status


Running Tests
-------------

::

    $ make

Demo
-------------

### https://asciinema.org/a/XqeHVAkTuPRM5CHBqqHQLuJK7


Python Support
---------------

- Tested With Python3, It may work with Python2 if you're lucky :grinning:




















