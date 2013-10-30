Installation
============


From Apt
--------

*python-automationclient* can be installed through the *StackOps* apt repos. Just add the repos to your ``sources.list``:

.. code-block:: bash

    echo 'deb http://repos.stackops.net/ folsom main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-updates main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-security main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-backports main' >> /etc/apt/sources.list

And now you can run ``update`` and install *python-automationclient*:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install python-automationclient

From PyPI
---------

Automatic
^^^^^^^^^^

To install *python-automationclient* on Linux/Mac operating systems from the public Python Package index just run:

.. code-block:: bash

    $ pip install python-automationclient

Manually
^^^^^^^^

To manually install *python-automationclient* from the Python Package Index on Linux/Mac operating systems, download python-automationclient.tar.gz from https://pypi.python.org/pypi/python-automationclient. Then change to the directory you downloaded python-automationclient.tar.gz to and execute the following in a terminal

.. code-block:: bash 

   $ tar python-automationclient.tar.gz
   $ cd python-automationclient
   $ python setup.py install

From Github
-----------

We recommend to install *python-automationclient* into a *virtualenv*:

.. code-block:: bash

    $ virtualenv .venv
    $ source .venv/bin/activate
    (.venv)$

You can install the latest `python-automationclient` from the `github repo <https://github.com/StackOps/python-automationclient>`_ using pip:

.. code-block:: bash

    (.venv)$ pip install -e git+git://github.com/StackOps/python-automationclient.git#egg=python-automationclient

Or manually:

.. code-block:: bash

    (.venv)$ git clone git://github.com/StackOps/python-automatioclient.git
    (.venv)$ cd python-automationclient
    (.venv)$ python setup.py install


