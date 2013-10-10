Python bindings to the Stackops Automation API
==============================================

This is a client for the Stackops Automation API. There's a Python API (the
``automationclient`` module), and a command-line script (``automation``). Each
implements 100% of the Stackops Automation API.

See the `Stackops Automation CLI guide`_ for information on how to use the ``automation``
command-line tool. You may also want to look at the
`Stackops Automation API documentation`_.

.. _Stackops Automation CLI guide: http://automationclient.stackops.org/
.. _Stackops Automation API documentation: http://docs.stackops.org/display/STACKOPSAUTOMATION/StackOps+Automation

The code is hosted on `Github`_.

.. _Github: https://github.com/StackOps/python-automationclient

This code a fork of `Openstack python-cinderclient`__ If you need API support
for the Openstack Cinder API solely or the Apache license, you should use that repository.

``python-automationclient`` is licensed under the Apache License.

__ https://github.com/openstack/cinder

.. contents:: Contents:
   :local:

Latest release version
----------------------

The latest release version of Stackops python-automationclient is ``v1.2.1``
that correspond with the current release of ``Stackops automation package``
who has the same number version as well.

Important Installation for development purpose (Temporal)
---------------------------------------------------------
Stackops python-automationclient is under development taking as groundwork the project
Openstack python-cinderclient, therefore to recreate the current project you need to clone this one
throught the command ``git clone https://github.com/StackOps/python-automationclient`` and then follow the
next steps:

1. Go to the directory ``python-automationclient``
2. Once on the directory run the command ``python tools/install_venv.py`` to create a virtual environment
   to work on it
3. Activate the virtual environment with the command ``source .venv/bin/activate``
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

    usage: automation [--version] [--debug] [--os-username <auth-user-name>]
                  [--os-password <auth-password>]
                  [--os-tenant-name <auth-tenant-name>]
                  [--os-tenant-id <auth-tenant-id>] [--os-auth-url <auth-url>]
                  [--os-region-name <region-name>]
                  [--service-type <service-type>]
                  [--service-name <service-name>]
                  [--endpoint-type <endpoint-type>]
                  [--os-automation-api-version <automation-api-ver>]
                  [--os-cacert <ca-certificate>] [--insecure]
                  [--retries <retries>]
                  <subcommand> ...

    Command-line interface to the Stackops Automation API.

    Positional arguments:
      <subcommand>
        architecture-create
                            Add a new architecture.
        architecture-delete
                            Remove a specific architecture.
        architecture-list   List all the architectures that are available on
                            automation.
        architecture-show   Show details about an architecture.
        architecture-template
                            Get template from a specific architecture.
        component-list      List all the components that are available on
                            automation.
        component-services  List all the services by a component.
        component-show      Show details about a component.
        datastore-add       Validate and add to the pool a NFS endpoint or GLUSTER
                            endpoint.
        datastore-attach    Attach a specific datastore to a zone.
        datastore-content   List top content (first level) of a specific
                            datastore.
        datastore-delete    Delete specific datastore.
        datastore-detach    Detach a specific datastore from a zone.
        datastore-discovery
                            Discovery endpoints from NFS.
        datastore-list      List a pool of datastores.
        datastore-show      Show details about a datastore.
        datastore-space     Show the space of a specific datastore.
        datastore-update    Update parameters of a specific datastore.
        datastore-validate  Validate a discovered NFS endpoint or just a GLUSTER
                            endpoint.
        device-activate     Activate a specific device in the pool.
        device-delete       Remove a specific device from pool.
        device-list         List all the devices in the pool.
        device-power-off    Power off a specific device in the pool.
        device-power-on     Power on a specific device in the pool.
        device-reboot       Reboot a specific device in the pool.
        device-replace      Replaces a node in a zone by a specific device in the
                            pool.
        device-show         Show details about a device.
        device-shutdown     Shutdown a specific device in the pool.
        device-soft-reboot  Soft reboot a specific device in the pool.
        device-update       Update a device.
        endpoints           Discover endpoints that get returned from the
                            authenticate services.
        global-property-create
                            Add a new property.
        global-property-delete
                            Delete a property.
        global-property-list
                            List all the properties that are available on
                            automation.
        global-property-update
                            Updates a property.
        node-deactivate     Deactivates a zone node. Moves an activated node from
                            the zone
        node-list           List all activate devices in a zone.
        node-show           Show details about a node in a zone.
        node-task-cancel    Cancel a task from a node in a zone.
        node-task-delete    Remove a task from a node in a zone from automation
                        DB.
        node-task-state     Show details about a task from a node in a zone.
        node-tasks-list     List all tasks from a node in a zone.
        node-task-delete    Remove a task from a node in a zone from automation
                            DB.
        profile-create      Add a new profile by architecture.
        profile-delete      Remove a specific profile by architecture.
        profile-json        Gets the JSON of the profile.
        profile-list        List all the profiles by architecture.
        profile-property-create
                            Create a profile property by architecture.
        profile-property-delete
                            Delete a profile property by architecture.
        profile-property-update
                            Update a profile property by architecture.
        profile-show        Show details about a profile by architecture.
        profile-update      Update a profile by architecture.
        role-component-json
                            Gets the JSON of the component by zone and role.
        role-component-list
                            List all components by zone and role.
        role-component-show
                            Show details about a component by zone and role.
        role-component-update
                            Update a component by zone and role .
        role-deploy         Associate a role to a node.
        role-list           List all the roles by zone.
        role-show           Show details about a role.
        service-execute     Execute a service by zone, role and component.
        service-list        List all the services by zone, role and component.
        service-show        Show details about a service by zone, role and
                            component.
        zone-create         Add a new zone by architecture according to a JSON
                            profile.
        zone-delete         Remove a specific zone.
        zone-json           Gets the JSON of the zone.
        zone-list           List all the zones.
        zone-property-create
                            Create a zone property.
        zone-property-delete
                            Delete a zone property.
        zone-property-update
                            Update a zone property.
        zone-show           Show details about a zone.
        zone-tasks-list     List all the tasks by zone.
        bash-completion     Print arguments for bash_completion.
        help                Display help about this program or one of its
                            subcommands.
        list-extensions     List all the os-api extensions that are available.

    Optional arguments:
      --version             show program's version number and exit
      --debug               Print debugging output
      --os-username <auth-user-name>
                            Defaults to env[OS_USERNAME].
      --os-password <auth-password>
                            Defaults to env[OS_PASSWORD].
      --os-tenant-name <auth-tenant-name>
                            Defaults to env[OS_TENANT_NAME].
      --os-tenant-id <auth-tenant-id>
                            Defaults to env[OS_TENANT_ID].
      --os-auth-url <auth-url>
                            Defaults to env[OS_AUTH_URL].
      --os-region-name <region-name>
                            Defaults to env[OS_REGION_NAME].
      --service-type <service-type>
                            Defaults to automation for most actions
      --service-name <service-name>
                            Defaults to env[AUTOMATION_SERVICE_NAME]
      --endpoint-type <endpoint-type>
                            Defaults to env[AUTOMATION_ENDPOINT_TYPE] or
                            publicURL.
      --os-automation-api-version <automation-api-ver>
                            Accepts 1.1 or 2,defaults to
                            env[OS_AUTOMATION_API_VERSION].
      --os-cacert <ca-certificate>
                            Specify a CA bundle file to use in verifying a TLS
                            (https) server certificate. Defaults to env[OS_CACERT]
      --insecure            Explicitly allow automationclient to perform
                            "insecure" TLS (https) requests. The server's
                            certificate will not be verified against any
                            certificate authorities. This option should be used
                            with caution.
      --retries <retries>   Number of retries.

    See "automation help COMMAND" for help on a specific command.

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start::

    # use v1.1 version)
    >>> from automationclient.v1_1 import client
    >>> at = client.Client(USERNAME, PASSWORD, TENANT_NAME)
    >>> at.components.list()
    [...]
