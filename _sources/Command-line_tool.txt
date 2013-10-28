Command-line Tool
=================

.. toctree::
    :maxdepth: 4 

    Device    
    Component
    Global_Properties
    Architecture
    Profile
    Zone

In order to use the CLI, you must provide your Automation username, password, tenant, and auth endpoint. Use the corresponding configuration options (--os-username, --os-password, --os-tenant-id, and --os-auth-url) or set them in environment variables:

.. code-block:: bash
   
   export OS_USERNAME=user
   export OS_PASSWORD=pass
   export OS_TENANT_NAME=admin
   export OS_AUTH_URL=http://auth.example.com:8089/v1.1

Once you've configured your authentication parameters, you can run 'automation help' to see a complete listing of available commands.


.. code-block:: bash

   $ automation help
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
    node-task-state     Show details about a task from a node in a zone.
    node-tasks-list     List all tasks from a node in a zone.
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
     --version          show program's version number and exit
     --debug            Print debugging output
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
     --insecure         Explicitly allow automationclient to perform
                        "insecure" TLS (https) requests. The server's
                        certificate will not be verified against any
                        certificate authorities. This option should be used
                        with caution.
     --retries <retries>   Number of retries.

   See "automation help COMMAND" for help on a specific command.
   $ 


