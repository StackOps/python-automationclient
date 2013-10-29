Zones
=====

What is a Zone?
---------------

An Openstack deployment **zone is usually called a Server Zone as well**. A zone allows the division of deployments within logical groups enabling better instance distribution. A zone requires, at least, an API node, a Scheduler, a MySQL database and a RabbitMQ. A zone commonly contains, as well, Volume Storage nodes and Computing nodes.

A zone does not share any component with others. The only way a zone can communicate with another is through the Openstack API, although this requires the zones to be hierarchically configured to be able to see one another.

What can I do with a Zone?
--------------------------

A zone is a set of physical compute, storage and network resources that, thanks to OpenStack magic, are offered to users as virtual resources. For example: 10 physical servers with 12 cores and 64GB of RAM can become 120 cores and 640GB of RAM virtually available for the users of that particular zone.

These zones can be enabled to customers in different ways:

    - Private Cloud: Any given IT Department sets up a StackOps Enterprise Edition and allocates part of one (or many) zone(s) to its internal customers, traditionally other departments or 
      services.
    
    - Public Cloud: A Hosting Company or a Service Provider decides to offer to its customers resources on demand under the pay-per-use model, allocating a single zone for multiple clients.
    
    - Virtual Private Cloud: A Hosting Company or a Service Provider allocates a full zone to a single customer, where all the resources are served upon demand but not shared.

Zone information
----------------

Each zone implements an architecture. This architecture helps to configure the different **nodes** of the zone based on the **properties** taken from the **architecture profile**.

Zone and their properties
-------------------------

**Automation** admininistrators are able to edit the content of the profile architecture propagated when creating the zone.


Similarly to system global properties and profile global properties, a global zone property can be stored in a zone. To reference this global zone property in any component property use $zone.zone_property_name convention. For example:

If the next zone property is created:

.. code-block:: bash
 
   my_user=stackops_user

A component property can reference it by setting the value property as follows:

.. code-block:: bash

   nova.user=$zone.my_user

Furthermore, zone properties propagated from the architecture profile may want to reference to other entities properties like node properties. To do that the content of these properties must follow the convention $node.id_node.node_property_name, for example:

.. code-block:: bash

   compute.mysql_host=$node.1.management_network_ip

What is a Role?
---------------

To know what a role is, you first need to know what is a component. A `component <http://stackops.github.io/python-automationclient/Component.html#what-is-a-component>`_ is a configured entity of the zone that defines its behaviour. It have a set of services that actually are actions over the component (stop, power on, install, reconfigure... etc).

**Roles** are created when user creates the zone. They are a set of components. A role might or might not be associated to a node.

Once user associates a role to a node then all the components of it will be deployed to the node through Fabuloso. When we associate a role to a node we are actually deploying all of its components in the target physical machine.

What is a Node?
---------------

Each zone is composed of different servers, the so-called Nodes. Each node can host different Openstack processes plus some components and applications that Nova needs to run.

Node properties
^^^^^^^^^^^^^^^

Each Node can be identified by this list of properties (example):

.. code-block:: bash

   +----------------------------------+-------------------------------------------------------------+
   |Property                          |	                         Sample Value                       |
   +==================================+=============================================================+
   |certified                         | true                                                        |
   +----------------------------------+-------------------------------------------------------------+
   |connection_data  	              | {                                                           |
   |                                  |    username="stackops",                                     |
   |                                  |    key_name="nonsecure",                                    |
   |                                  |    host="10.15.111.39",                                     |
   |                                  |    port=22                                                  |
   |                                  | }                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |cores 	                      | 1                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |created                           | "2013-09-30 08:39:42"                                       |
   +----------------------------------+-------------------------------------------------------------+
   |disk_size 	                      | 17179869184                                                 |
   +----------------------------------+-------------------------------------------------------------+
   |id 	                              | 1                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |ip 	                              | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |lom_ip 	                      | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |lom_mac 	                      | "00:50:56:3f:d7:60"                                         |
   +----------------------------------+-------------------------------------------------------------+
   |mac 	                      | "00:50:56:3f:d7:60"                                         |
   +----------------------------------+-------------------------------------------------------------+
   |management_network_dns 	      | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |management_network_gateway 	      | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |management_network_ip 	      | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |management_network_netmask 	      | "10.15.111.39"                                              |
   +----------------------------------+-------------------------------------------------------------+
   |megaherzs 	                      | 0                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |memory 	                      | 1073741824                                                  |
   +----------------------------------+-------------------------------------------------------------+
   |name 	                      | "controller-trinode-zone1"                                  |
   +----------------------------------+-------------------------------------------------------------+
   |ports 	                      | 1                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |product 	                      | "VMware Virtual Platform ()"                                |
   +----------------------------------+-------------------------------------------------------------+
   |status 	                      | "HOST_DOWN"                                                 |
   +----------------------------------+-------------------------------------------------------------+
   |threads 	                      | 1                                                           |
   +----------------------------------+-------------------------------------------------------------+
   |updated 	                      | "2013-09-30 14:48:27"                                       |
   +----------------------------------+-------------------------------------------------------------+
   |vendor 	                      | "VMware, Inc."                                              |
   +----------------------------------+-------------------------------------------------------------+
   |zone_id 	                      | 2                                                           |
   +----------------------------------+-------------------------------------------------------------+


What is a Task?
---------------

We define a task as the execution of a specific service of a role's component. You can not perform any operation after the task is been launched, unless this in the PENDING state, in which case the task can be cancelled.

Each task can be identified by this list of properties (example):

.. code-block:: bash

   +-----------+--------------------------------------------------+
   |Property   | Sample Value                                     |
   +===========+==================================================+
   |finished_at| "2013-09-30 09:57:03"                            |
   +-----------+--------------------------------------------------+
   |id 	       | 1                                                |
   +-----------+--------------------------------------------------+
   |name       | folsom.mysql.install                             |
   +-----------+--------------------------------------------------+
   |node_id    | 2                                                |
   +-----------+--------------------------------------------------+
   |result     | "Exception(u'Output: 10...5.111.39 out: install" |
   +-----------+--------------------------------------------------+
   |started_at | "None"                                           |
   +-----------+--------------------------------------------------+
   |state      | "FAILURE"                                        |
   +-----------+--------------------------------------------------+
   |uuid       | "0b288197-7a80-4ed3-bde7-188b3f6b9a8d"           |
   +-----------+--------------------------------------------------+


What are Zone Properties?
-------------------------

Zone properties are extensions of a zone through the key/value form, these ones can be used later to define service properties in each role of its zone.
In order to reference the value of these properties, use this nomenclature:

.. code-block:: bash

    zone.{key}

Managing Zones
--------------

The operations allowed in the python-automatioclient are:

.. code-block:: bash

   zone-list           List all the zones.
   zone-show           Show details about a zone.
   zone-create         Add a new zone by architecture according to a JSON
                       profile.
   zone-json           Gets the JSON of the zone.
   zone-delete         Remove a specific zone.
   zone-property-create
                       Create a zone property.
   zone-property-update
                       Update a zone property.
   zone-property-delete
                       Delete a zone property.
   zone-tasks-list     List all the tasks by zone.
   role-list           List all the roles by zone.
   role-show           Show details about a role.
   role-deploy         Associate a role to a node.
   role-component-list
                       List all components by zone and role.
   role-component-show
                       Show details about a component by zone and role.
   role-component-update
                       Update a component by zone and role .
   role-component-json
                       Gets the JSON of the component by zone and role.
   service-list        List all the services by zone, role and component.
   service-show        Show details about a service by zone, role and
                       component.
   service-execute     Execute a service by zone, role and component.
   node-list           List all activate devices in a zone.
   node-show           Show details about a node in a zone.
   node-tasks-list     List all tasks from a node in a zone.
   node-task-state     Show details about a task from a node in a zone.
   node-task-cancel    Cancel a task from a node in a zone.


Zone Operations
^^^^^^^^^^^^^^^

List zones
~~~~~~~~~~
 
.. code-block:: bash

   $ zone-list
   +----+-----------------+
   | id |       name      |
   +----+-----------------+
   | 1  | fakezonestorage |
   +----+-----------------+

Show a specific zone
~~~~~~~~~~~~~~~~~~~~

To show details about a zone, this one must be referenced by its ID

.. code-block:: bash

   $ zone-show 1
   +------------+------------------------------------------------+
   |  Property  |                     Value                      |
   +------------+------------------------------------------------+
   |     id     |                       1                        |
   |    name    |                fakezonestorage                 |
   | properties |                       {                        |
   |            |     "fake_property_key": "fake_property_value" |
   |            |                       }                        |
   +------------+------------------------------------------------+

Create a zone
~~~~~~~~~~~~~

To create a zone you must specified the architecture ID, its name and generate through the operation `profile-json <http://stackops.github.io/python-automationclient/Profile.html#generate-a-json-output-from-a-specific-profile>`_ the JSON file to have as reference at the moment to create a zone

.. code-block:: bash

   $ help zone-create
   usage: automation zone-create <architecture-id> <name> <profile-file>

   Add a new zone by architecture according to a JSON profile.

   Positional arguments:
    <architecture-id>  ID of the architecture
    <name>             Name to the new zone to create
    <profile-file>     File with extension .json describing the new zone to
                       create. It is took from the operation profile-json as
                       reference.
   
   $ zone-create 1 zone-docu zone-docu.json 
   +------------+------------------------------------------------+
   |  Property  |                     Value                      |
   +------------+------------------------------------------------+
   |     id     |                       2                        |
   |    name    |                   zone-docu                    |
   | properties |                       {                        |
   |            |     "fake_property_key": "fake_property_value" |
   |            |                       }                        |
   +------------+------------------------------------------------+

Generate JSON file from a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ zone-json 2
   {
    "zone": { 
        "id": 2, 
        "properties": {
                 "fake_property_key": "fake_property_value"
        }, 
        "name": "zone-docu"
    }
   }

Delete a specific zone
~~~~~~~~~~~~~~~~~~~~~~

To delete a zone, this one must be referenced by its ID

.. code-block:: bash

   $ zone-delete 2

List taks from zone
~~~~~~~~~~~~~~~~~~~

To list all taks by zone, this one must be referenced by its ID

.. code-block:: bash

   $ zone-tasks-list 1
   +----+------+------+-------+--------+
   | id | name | uuid | state | result |
   +----+------+------+-------+--------+
   +----+------+------+-------+--------+

Properties Zone Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a zone property
~~~~~~~~~~~~~~~~~~~~~~

To create a zone property you must specific the ID zone

.. code-block:: bash
   
   $ help zone-property-create
   usage: automation zone-property-create <zone-id> <property-key>
                                          <property-value>

   Create a zone property.

   Positional arguments:
     <zone-id>         ID of the zone to create a property.
     <property-key>    The key property.
     <property-value>  The value property

   $ zone-property-create 1 key_docu_property value_docu_property
   +------------+-------------------------------------------------+
   |  Property  |                      Value                      |
   +------------+-------------------------------------------------+
   |     id     |                        1                        |
   |    name    |                 fakezonestorage                 |
   | properties |                        {                        |
   |            |     "fake_property_key": "fake_property_value", |
   |            |      "key_docu_property": "value_docu_property" |
   |            |                        }                        |
   +------------+-------------------------------------------------+

Modify specifc profile property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update a zone property you must specific the ID zone and the key of it.

.. code-block:: bash
 
   $ help zone-property-update
   usage: automation zone-property-update <zone-id> <property-key>
                                       <property-value>

   Update a zone property.

   Positional arguments:
     <zone-id>         ID of the zone to update a property.
     <property-key>    The key property.
     <property-value>  The value property

   $ zone-property-update 1 key_docu_property value_docu_property_update
   +------------+-------------------------------------------------------+
   |  Property  |                         Value                         |
   +------------+-------------------------------------------------------+
   |     id     |                           1                           |
   |    name    |                    fakezonestorage                    |
   | properties |                           {                           |
   |            |        "fake_property_key": "fake_property_value",    |
   |            |     "key_docu_property": "value_docu_property_update" |
   |            |                           }                           |
   +------------+-------------------------------------------------------+

Remove a specific profile property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To delete a zone property you must specific the ID zone and the key of it


.. code-block:: bash

  $ help zone-property-delete
  usage: automation zone-property-delete <zone-id> <property-key>

  Delete a zone property.

  Positional arguments:
     <zone-id>       ID of the zone to delete a property.
     <property-key>  The key property.

  $ zone-property-delete 1 key_docu_property
  +------------+------------------------------------------------+
  | Property   |                     Value                      |
  +------------+------------------------------------------------+
  |     id     |                       1                        |
  |    name    |                fakezonestorage                 |
  | properties |                       {                        |
  |            |     "fake_property_key": "fake_property_value" |
  |            |                       }                        |
  +------------+------------------------------------------------+

Roles Operations
^^^^^^^^^^^^^^^^

List roles
~~~~~~~~~~

.. code-block:: bash

  $ role-list 1
  +----+------------+
  | id |    name    |
  +----+------------+
  | 1  | controller |
  | 2  | compute    |
  +----+------------+

Show details about a specific role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show details about a role you must specific the ID zone and the ID role

.. code-block:: bash

   $ help role-show
   usage: automation role-show <zone-id> <role-id>

   Show details about a role.

   Positional arguments:
     <zone-id>  ID of the zone.
     <role-id>  ID of the role.

   $ role-show 1 1
   role-show 1 1
   +----------+------------+
   | Property |   Value    |
   +----------+------------+
   |    id    |     1      |
   |   name   | controller |
   +----------+------------+

Associate a node (pyshical server discovered and in the pool) to a role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This in **one of the most important operations** in the python-automationclient, due to perform a critical stage in the system allowing the installation, configuration and operation of the nodes in a zone, creating the differents tasks once has been defined an architecture to be deployed.

To deploy a node must be specified the ID zone, ID role and the ID node as mandatories, other parameters can be add to perfom a different behavior

.. code-block:: bash 
 
   $ help role-deploy
   usage: automation role-deploy [--hostname <hostname>] [--no-dhcp-reload]
                                 [--bypass]
                                 <zone-id> <role-id> <node-id>

   Associate a role to a node.

   Positional arguments:
     <zone-id>             ID of the zone.
     <role-id>             ID of the role.
     <node-id>             ID of the node.

   Optional arguments:
    --hostname <hostname>
                          We know the hostname of the node
    --no-dhcp-reload      Specifies dhcp request in target node should ask for
                          an IP
    --bypass              Specifies if role should apply should be
                          skipped.Default is False

  
   $ role-deploy 1 1 1
   +----+------+------+-------+--------+
   | id | name | uuid | state | result |
   +----+------+------+-------+--------+
   +----+------+------+-------+--------+

List all component by zone and role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list all the components by zone and role defined at the moment to create the zone taken as reference an architecture you must specified the ID zone and the ID role

.. code-block:: bash

   $ help role-component-list
   usage: automation role-component-list <zone-id> <role-id>

   List all components by zone and role.

   Positional arguments:
     <zone-id>  ID of the zone.
     <role-id>  ID of the role.

   $ role-component-list 1 1
   +----+----------+
   | id |   name   |
   +----+----------+
   | 1  |  mysql   |
   | 2  | rabbitmq |
   | 3  | storage  |
   +----+----------+

Show a specific component in a node by zone and role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show details about a component configuration in a node you must specific the ID zone, the ID role, the ID node and the Name of the component

.. code-block:: bash

   $ help role-component-show
   usage: automation role-component-show <zone-id> <role-id> <node-id>
                                         <component>
   
   Show details about a component by zone and role.

   Positional arguments:
     <zone-id>    ID of the zone.
     <role-id>    ID of the role.
     <node-id>    ID of the node.
     <component>  Name of the component.

   $  role-component-show 1 1 1 mysql
   +------------+--------------------------------------------+
   |  Property  |                   Value                    |
   +------------+--------------------------------------------+
   |     id     |                     1                      |
   |    name    |                   mysql                    |
   | properties |                     {                      |
   |            |                  "install": {              |
   |            |         "automation_password": "stackops", |
   |            |          "automation_user": "automation",  |
   |            |           "cinder_password": "stackops",   |
   |            |              "cinder_user": "cinder",      |
   |            |           "glance_password": "stackops",   |
   |            |              "glance_user": "glance",      |
   |            |          "keystone_password": "stackops",  |
   |            |            "keystone_user": "keystone",    |
   |            |            "nova_password": "stackops",    |
   |            |                "nova_user": "nova",        |
   |            |          "quantum_password": "stackops",   |
   |            |             "quantum_user": "quantum",     |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |              "set_accounting": {           |
   |            |         "accounting_password": "stackops", |
   |            |           "accounting_user": "activity",   |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |              "set_automation": {           |
   |            |         "automation_password": "stackops", |
   |            |          "automation_user": "automation",  |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_cinder": {             |
   |            |           "cinder_password": "stackops",   |
   |            |              "cinder_user": "cinder",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_glance": {             |
   |            |           "glance_password": "stackops",   |
   |            |              "glance_user": "glance",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |               "set_keystone": {            |
   |            |          "keystone_password": "stackops",  |
   |            |            "keystone_user": "keystone",    |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                 "set_nova": {              |
   |            |            "nova_password": "stackops",    |
   |            |                "nova_user": "nova",        |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_portal": {             |
   |            |           "portal_password": "stackops",   |
   |            |              "portal_user": "portal",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_quantum": {            |
   |            |          "quantum_password": "stackops",   |
   |            |             "quantum_user": "quantum",     |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   | 
   |            |                "teardown": {},             |
   |            |                 "validate": {              |
   |            |                "database_type": "",        |
   |            |                "drop_schema": null,        |
   |            |                    "host": "",             |
   |            |             "install_database": null,      |
   |            |                  "password": "",           |
   |            |                    "port": "",             |
   |            |                   "schema": "",            |
   |            |                   "username": ""           |
   |            |                       }                    |
   |            |                     }                      |
   +------------+--------------------------------------------+

Generate JSON component file in a node by zone and role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To generate a JSON file of a component configuration in a node you must specific the ID zone, the ID role, the ID node and the Name component

.. code-block:: bash

   $  help role-component-json
   usage: automation role-component-json <zone-id> <role-id> <node-id>
                                         <component>

   Gets the JSON of the component by zone and role.

   Positional arguments:
     <zone-id>    ID of the zone.
     <role-id>    ID of the role.
     <node-id>    ID of the node.
     <component>  Name of the component.

   $ {
      "component": {
        "id": 1,
        "properties": {
            "set_quantum": {
                "root_pass": "stackops",
                "quantum_user": "quantum",
                "quantum_password": "stackops"
            },
            "set_keystone": {
                "root_pass": "stackops",
                "keystone_password": "stackops",
                "keystone_user": "keystone"
            },
            "teardown": {},
            "set_cinder": {
                "cinder_user": "cinder",
                "root_pass": "stackops",
                "cinder_password": "stackops"
            },
            "set_automation": {
                "automation_password": "stackops",
                "root_pass": "stackops",
                "automation_user": "automation"
            },
            "set_accounting": {
                "accounting_user": "activity",
                "root_pass": "stackops",
                "accounting_password": "stackops"
            },
            "set_nova": {
                "root_pass": "stackops",
                "nova_password": "stackops",
                "nova_user": "nova"
            },
            "install": {
                "root_pass": "stackops",
                "keystone_user": "keystone",
                "cinder_user": "cinder",
                "quantum_password": "stackops",
                "glance_password": "stackops",
                "automation_user": "automation",
                "quantum_user": "quantum",
                "automation_password": "stackops",
                "keystone_password": "stackops",
                "cinder_password": "stackops",
                "nova_user": "nova",
                "glance_user": "glance",
                "nova_password": "stackops"
            },
            "set_glance": {
                "root_pass": "stackops",
                "glance_password": "stackops",
                "glance_user": "glance"
            },
            "validate": {
                "username": "",
                "drop_schema": null,
                "install_database": null,
                "database_type": "",
                "host": "",
                "password": "",
                "port": "",
                "schema": ""
            },
            "set_portal": {
                "root_pass": "stackops",
                "portal_user": "portal",
                "portal_password": "stackops"
            }
        },
        "name": "mysql"
      }
     }

Modify a specific component in a node by zone and role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update a component configuration in a node you must specific the ID zone, the ID role, the ID node, the Name component and the JSON file with the component to update generated through the operation **component-role-json** as input

.. code-block:: bash

   $ help role-component-update
   usage: automation role-component-update <zone-id> <role-id> <node-id>
                                           <component> <component-file>

   Update a component by zone and role .

   Positional arguments:
     <zone-id>         ID of the zone.
     <role-id>         ID of the role.
     <node-id>         ID of the node.
     <component>       Name of the component.
     <component-file>  File with extension .json describing the component to
                       update. It is took from the operation role-component-json
                       as reference.

   $ role-component-update 1 1 1 mysql role_component_update.json
   +------------+--------------------------------------------+
   |  Property  |                   Value                    |
   +------------+--------------------------------------------+
   |     id     |                     1                      |
   |    name    |                   mysql                    |
   | properties |                     {                      |
   |            |                  "install": {              |
   |            |         "automation_password": "stackops", |
   |            |          "automation_user": "automation",  |
   |            |           "cinder_password": "stackops",   |
   |            |              "cinder_user": "cinder",      |
   |            |           "glance_password": "stackops",   |
   |            |              "glance_user": "glance",      |
   |            |          "keystone_password": "stackops",  |
   |            |            "keystone_user": "keystone",    |
   |            |            "nova_password": "stackops",    |
   |            |                "nova_user": "nova",        |
   |            |          "quantum_password": "stackops",   |
   |            |             "quantum_user": "quantum",     |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |              "set_accounting": {           |
   |            |         "accounting_password": "stackops", |
   |            |           "accounting_user": "activity",   |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |              "set_automation": {           |
   |            |         "automation_password": "stackops", |
   |            |          "automation_user": "automation",  |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_cinder": {             |
   |            |           "cinder_password": "stackops",   |
   |            |              "cinder_user": "cinder",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_glance": {             |
   |            |           "glance_password": "stackops",   |
   |            |              "glance_user": "glance",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |               "set_keystone": {            |
   |            |          "keystone_password": "stackops",  |
   |            |            "keystone_user": "keystone",    |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                 "set_nova": {              |
   |            |            "nova_password": "stackops",    |
   |            |                "nova_user": "nova",        |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_portal": {             |
   |            |           "portal_password": "stackops",   |
   |            |              "portal_user": "portal",      |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "set_quantum": {            |
   |            |          "quantum_password": "stackops",   |
   |            |             "quantum_user": "quantum",     |
   |            |              "root_pass": "stackops"       |
   |            |                       },                   |
   |            |                "teardown": {},             |
   |            |                 "validate": {              |
   |            |             "database_type": "mysql",      |
   |            |               "drop_schema": false,        |
   |            |                "host": "localhost",        |
   |            |             "install_database": false,     |
   |            |              "password": "stackops",       |
   |            |                  "port": "3306",           |
   |            |                 "schema": "mysql",         |
   |            |               "username": "stackops"       |
   |            |                       }                    |
   |            |                     }                      |
   +------------+--------------------------------------------+

Services (Tasks) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

List services that are be able to execute by zone, role and component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the services you must specific th ID zone, ID role and name component

.. code-block:: bash

   $ help service-list 
   usage: automation service-list <zone-id> <role-id> <component>

   List all the services by zone, role and component.

   Positional arguments:
     <zone-id>    ID of the zone.
     <role-id>    ID of the role.
     <component>  Name of the component.

   $ service-list 1 1 mysql
   +----------------+-------------------------------------------------------------------+
   |      Name      |                            description                            |
   +----------------+-------------------------------------------------------------------+
   |    install     | Prepares a database and a user password for each StackOps schemas |
   | set_accounting | Creates a new database for accounting and grants privileges on it |
   | set_automation | Creates a new database for automation and grants privileges on it |
   |   set_cinder   |   Creates a new database for cinder and grants privileges on it   |
   |   set_glance   |   Creates a new database for glance and grants privileges on it   |
   |  set_keystone  |  Creates a new database for keystone and grants privileges on it  |
   |    set_nova    |    Creates a new database for nova and grants privileges on it    |
   |   set_portal   |   Creates a new database for portal and grants privileges on it   |
   |  set_quantum   |   Creates a new database for quantum and grants privileges on it  |
   |    teardown    |                       Stop the mysql service                      |
   |    validate    |             Validates main database to operate with it            |
   +----------------+-------------------------------------------------------------------+


Show a specific service that are be able to execute by zone, role and component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show details about a specific service you must specific th ID zone, ID role, the name component and the name service

.. code-block:: bash 

   $  <zone-id> <role-id> <component> <service-name>

   Show details about a service by zone, role and component.

   Positional arguments:
     <zone-id>       ID of the zone.
     <role-id>       ID of the role.
     <component>     Name of the component.
     <service-name>  Name of the service.

   $  service-show 1 1 mysql install
   +-------------+--------------------------------------------------------------------------------------------------+
   |   Property  |                                              Value                                               |
   +-------------+--------------------------------------------------------------------------------------------------+
   |    _links   | {"self": {"href": "http://0.0.0.0:8089/v1.1/zones/1/roles/1/components/mysql/services/install"}} |
   | description |                Prepares a database and a user password for each StackOps schemas                 |
   |     name    |                                             install                                              |
   +-------------+--------------------------------------------------------------------------------------------------+

Execute a specific service in a node by zone, role and component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To execute a specific service you must specific the ID zone, ID role, the name component, the name service and finally the ID node where it'll be execute

.. code-block:: bash 

   $ help service-execute
   usage: automation service-execute <zone-id> <role-id> <component>
                                     <service-name> <node>

   Execute a service by zone, role and component.

   Positional arguments:
     <zone-id>       ID of the zone.
     <role-id>       ID of the role.
     <component>     Name of the component.
     <service-name>  Name of the service.
     <node>          Identifier of the node.

   $ service-execute 1 1 mysql install 1

Nodes Operations
^^^^^^^^^^^^^^^^

List all activate nodes in a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ node-list 1
   +----+-------------------+-------------------+-----------+
   | id |        name       |        mac        |   status  |
   +----+-------------------+-------------------+-----------+
   | 1  | 08:00:27:1e:b6:cd | 08:00:27:1e:b6:cd | ACTIVATED |
   +----+-------------------+-------------------+-----------+

Show details about a node in a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show details about a specific node you must specific the ID node and the ID zone where it has been activated

.. code-block:: bash

   $ node-show <zone-id> <node-id>

   Show details about a node in a zone.

   Positional arguments:
     <zone-id>  ID of the zone.
     <node-id>  ID of the node.

   $ node-show 1 1
   +----------------------------+----------------------------------------------------------------------------------------+
   |          Property          |                                         Value                                          |
   +----------------------------+----------------------------------------------------------------------------------------+
   |         certified          |                                         False                                          |
   |      connection_data       | {"username": "stackops", "key_name": "nonsecure", "host": "180.10.10.119", "port": 22} |
   |           cores            |                                           1                                            |
   |          created           |                                  2013-10-09 11:18:39                                   |
   |         disk_size          |                                       8589934592                                       |
   |             id             |                                           1                                            |
   |             ip             |                                     180.10.10.119                                      |
   |           lom_ip           |                                        0.0.0.0                                         |
   |          lom_mac           |                                      00:00:00:00                                       |
   |            mac             |                                   08:00:27:1e:b6:cd                                    |
   |   management_network_dns   |                                        8.8.8.8                                         |
   | management_network_gateway |                                      180.10.10.1                                       |
   |   management_network_ip    |                                     180.10.10.119                                      |
   | management_network_netmask |                                     255.255.255.0                                      |
   |         megaherzs          |                                           0                                            |
   |           memory           |                                       515497984                                        |
   |            name            |                                   08:00:27:1e:b6:cd                                    |
   |           ports            |                                           1                                            |
   |          product           |                                     VirtualBox ()                                      |
   |           status           |                                       ACTIVATED                                        |
   |          threads           |                                           1                                            |
   |          updated           |                                  2013-10-09 15:18:20                                   |
   |           vendor           |                                      innotek GmbH                                      |
   |          zone_id           |                                           1                                            |
   +----------------------------+----------------------------------------------------------------------------------------+


Show tasks on the node in a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list all tasks on an specific node you must specific the ID node and the ID zone where it has been activated

.. code-block:: bash
   
   $ help node-tasks-list
   usage: automation node-tasks-list <zone-id> <node-id>

   List all tasks from a node in a zone.

   Positional arguments:
     <zone-id>  ID of the zone.
     <node-id>  ID of the node.

.. code-block:: bash
   
   $ help node-tasks-list 1 1
   node-tasks-list 1 1
   +----+------+------+-------+
   | id | name | uuid | state |
   +----+------+------+-------+
   +----+------+------+-------+

Show a specific state task on the node in a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show a specific task on a node you must specific the ID node and the ID zone where it has been activated and the ID task executed on it

.. code-block:: bash
   
   $ help node-tasks-list
   usage: automation node-task-state <zone-id> <node-id> <task-id>

   Show details about a task from a node in a zone.

   Positional arguments:
     <zone-id>  ID of the zone.
     <node-id>  ID of the node.
     <task-id>  ID of the task.


.. code-block:: bash
   
   $ help node-task-show 1 1 1

Cancel a specific task on the node in a zone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To cancel a specific task on a node you must specific the ID node and the ID zone where it has been activated and the ID task executed on it

.. code-block:: bash

   $ help node-task-cancel
   usage: automation node-task-cancel <zone-id> <node-id> <task-id>

   Cancel a task from a node in a zone.

   Positional arguments:
     <zone-id>  ID of the zone.
     <node-id>  ID of the node.
     <task-id>  ID of the task.

.. code-block:: bash
   
   $ help node-task-cancel 1 1 1
