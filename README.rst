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
3. Install the python-automationclient throught the command ``PBR_VERSION=0.5.21 python setup.py install``
4. This is all!! Start to contribute....


Command-line API
----------------
Installing this package gets you a shell command, ``automation``, that you
can use to interact with any Stackops Automation compatible API..

You'll need to provide your Stackops Automation username, password and tenant_name.
You can do this with the ``--os-auto-username``, ``--os-auto-password`` and  ``--os-auto-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_AUTO_USERNAME=stackops
    export OS_AUTO_PASSWORD=secret
    export OS_AUTO_TENANT_NAME=service

You will also need to define the authentication url with ``--os-auto-auth-url``
and the version of the API with ``--auto-version``.  Or set them as an environment
variables as well::

    export OS_AUTO_AUTH_URL=http://example.com:5000/v2.0/
    export OS_AUTO_VERSION=1

As Stackops Automation used Keystone, you need to set the AUTOMATION_URL to the keystone
endpoint::

    export OS_AUTO_AUTH_URL=http://example.com:5000/v2.0/

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-auto-region-name`` (or
``export OS_AUTO_REGION_NAME``). It defaults to the first in the list returned.

You'll find complete documentation on the shell by running
``automation help``::

    usage: cinder [--debug] [--os-auto-username <auto-auth-user-name>]
                  [--os-auto-password <auto-auth-password>]
                  [--os-auto-tenant-name <auto-auth-tenant-name>] [--os-auto-auth-url <auto-auth-url>]
                  [--os-auto-region-name <region-name>] [--auto-service-type <auto-service-type>]
                  [--auto-service-name <auto-service-name>]
                  [--auto-service-name <auto-service-name>]
                  [--auto-endpoint-type <auto-endpoint-type>]
                  [--os-auto-version <auto-compute-ver>]
                  [--os-auto-cacert <ca-auto-certificate>] [--auto-retries <auto-retries>]
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
      --os-auto-username <auth-auto-user-name>
                            Defaults to env[OS_AUTO_USERNAME].
      --os-auto-password <auth-auto-password>
                            Defaults to env[OS_AUTO_PASSWORD].
      --os-auto-tenant-name <auth-auto-tenant-name>
                            Defaults to env[OS_AUTO_TENANT_NAME].
      --os-auto-auth-url <auto-auth-url>
                            Defaults to env[OS_AUTO_AUTH_URL].
      --os-auto-region-name <auto-region-name>
                            Defaults to env[OS_AUTO_REGION_NAME].
      --auto-service-type <auto-service-type>
                            Defaults to compute for most actions
      --auto-service-name <auto-service-name>
                            Defaults to env[AUTOMATION_SERVICE_NAME]
      --auto-service-name <auto-service-name>
                            Defaults to env[AUTOMATION_SERVICE_NAME]
      --auto-endpoint-type <auto-endpoint-type>
                            Defaults to env[AUTOMATION_ENDPOINT_TYPE] or publicURL.
      --os-auto-api-version <auto-api-ver>
                            Accepts 1,defaults to env[OS_AUTO_API_VERSION].
      --os-auto-cacert <ca-auto-certificate>
                            Specify a CA bundle file to use in verifying a TLS
                            (https) server certificate. Defaults to env[OS_AUTO_CACERT]
      --auto-retries <auto-retries>   Number of retries.

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start::

    # use v1.0 version)
    >>> from automationclient.v1 import client
    >>> at = client.Client(USERNAME, PASSWORD, TENANT_NAME)
    >>> at.components.list()
    [...]
