Command-line Tool
=================

In order to use the CLI, you must provide your Automation username, password, tenant, and auth endpoint. Use the corresponding configuration options (--os-username, --os-password, --os-tenant-id, and --os-auth-url) or set them in environment variables:

export OS_USERNAME=user

export OS_PASSWORD=pass

export OS_TENANT_NAME=admin

export OS_AUTH_URL=http://auth.example.com:8089/v1.1

Once you've configured your authentication parameters, you can run 'automation help' to see a complete listing of available commands.

.. toctree::
    :maxdepth: 2

    Device    
    Component
    Architecture
    Profile
    Node
    Zone
    Global_Properties

