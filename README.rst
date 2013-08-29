Python bindings to the Stackops Automation API
===========================================

This is a client for the Stackops Automation API. There's a Python API (the
``automationclient`` module), and a command-line script (``automation``). Each
implements 100% of the Stackops Automation API.

See the `Stackops Automation CLI guide`_ for information on how to use the ``automation``
command-line tool. You may also want to look at the
`Stackops Automation API documentation`_.

.. _Stackops Automation CLI guide: http://docs.stackops.org/display/STACKOPSDOCS/RESTful+API
.. _Stackops Automation API documentation: http://docs.stackops.org/display/STACKOPSDOCS/RESTful+API

The code is hosted on `Github`_.

.. _Github: https://github.com/StackOps/python-automationclient

This code a fork of `Openstack python-cinderclient`__ If you need API support
for the Openstack Cinder API solely or the Apache license, you should use that repository.
python-automationclient is licensed under the Apache License like the rest of OpenStack.

__ https://github.com/openstack/cinder

.. contents:: Contents:
   :local:


Important Installation for development purpose (Temporal)
----------------------------------------------
Stackops python-automationclient is under development taking as groundwork the project
Openstack python-cinderclient, therefore to recreate the current project you need to clone this one
throught the command ``git clone https://github.com/StackOps/python-automationclient`` and then follow the
next steps:

1. Go to the directory ``python-automationclient``
2. Once on the directory run the command ``python tool/install_venv.py`` to create a virtual environment
   to work on it
3. Activate the virtual environment with the command source ``.venv/bin/activate``
4. Install the python-automationclient throught the command ``python setup.py install``
5. This is all!! Start to contribute....


Command-line API
----------------
Installing this package gets you a shell command, ``automation``, that you
can use to interact with any Stackops Automation compatible API..

You'll need to provide your Stackops Automation username, password and tenant_name.
You can do this with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=stackops
    export OS_PASSWORD=secret
    export OS_TENANT_NAME=service

You will also need to define the authentication url with ``--os-auth-url``
and the version of the API with ``--version``.  Or set them as an environment
variables as well::

    export OS_AUTH_URL=http://example.com:5000/v2.0/
    export OS_VERSION=1

As Stackops Automation used Keystone, you need to set the AUTOMATION_URL to the keystone
endpoint::

    export OS_AUTH_URL=http://example.com:5000/v2.0/

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-region-name`` (or
``export OS_REGION_NAME``). It defaults to the first in the list returned.

You'll find complete documentation on the shell by running
``automation help``::

    usage: cinder [--debug] [--os-username <auth-user-name>]
                  [--os-password <auth-password>]
                  [--os-tenant-name <auth-tenant-name>] [--os-auth-url <auth-url>]
                  [--os-region-name <region-name>] [--service-type <service-type>]
                  [--service-name <service-name>]
                  [--service-name <service-name>]
                  [--endpoint-type <endpoint-type>]
                  [--os-version <-compute-ver>]
                  [--os-cacert <ca-certificate>] [--retries <auto-retries>]
                  <subcommand> ...

    Command-line interface to the Stackops Automation API..

    Positional arguments:
      <subcommand>
        components-list     List all the componets that are available on automation
        componet-show       Show a specific component with details
        bash-completion     Prints all of the commands and options to stdout so
                            that the
        help                Display help about this program or one of its
                            subcommands.
        list-extensions     List all the os-api extensions that are available.

    Optional arguments:
      --debug               Print debugging output
      --os-username <auth-user-name>
                            Defaults to env[OS_USERNAME].
      --os-password <auth-password>
                            Defaults to env[OS_PASSWORD].
      --os-tenant-name <auth-tenant-name>
                            Defaults to env[OS_TENANT_NAME].
      --os-auth-url <auth-url>
                            Defaults to env[OS_AUTH_URL].
      --os-region-name <region-name>
                            Defaults to env[OS_REGION_NAME].
      ---service-type <service-type>
                            Defaults to compute for most actions
      --service-name <service-name>
                            Defaults to env[SERVICE_NAME]
      --service-name <service-name>
                            Defaults to env[SERVICE_NAME]
      --endpoint-type <endpoint-type>
                            Defaults to env[ENDPOINT_TYPE] or publicURL.
      --os-api-version <api-ver>
                            Accepts 1,defaults to env[OS_API_VERSION].
      --os-cacert <ca-certificate>
                            Specify a CA bundle file to use in verifying a TLS
                            (https) server certificate. Defaults to env[OS_CACERT]
      --retries <auto-retries>   Number of retries.

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start::

    # use v1.0 version)
    >>> from automationclient.v1 import client
    >>> at = client.Client(USERNAME, PASSWORD, TENANT_NAME)
    >>> at.components.list()
    [...]
