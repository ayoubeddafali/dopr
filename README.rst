Dopr 
========

A minimal CLI tool for Provisionning Digital Ocean Droplets

Pre-requisites
------

- Pipenv Installed 
- make install
- Set you Digital Ocean Token as an environment variable **DO_TOKEN**

Installation 
------

::

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
 



Running Tests
-------------

::

    $ make


Python Support 
---------------

- Tested With Python3, It may work with Python2 if you're lucky :grinning:




















