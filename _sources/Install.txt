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


