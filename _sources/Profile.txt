Profiles
========

What is a Profile?
------------------

A profile is just a way to save **predefined templates of an architecture without creating a full zone**. User may want to use several common properties for all his zones, and some specific properties for each zone. A way to save the common properties without the need of fill the whole template each time, is by the use of profiles. The profile endpoint will never check the input properties (the zone endpoint will), so you can save any properties you like to use later on. Only the name attribute is mandatory.

A profile is the set of architecture's properties. A profile can be empty (returned by the architecture-template operation) half-filled, or full-filled. Is a dictionary-like structure with all the properties ofthe **components** the architecture can have, this properties are recovered from **catalog components** managed by **FABuloso**.

Profiles and their properties
-----------------------------

A **global profile property** can be stored in a profile entity. To reference this global profile property in any component property use $property.profile_property_name convention. For example:

If the next profile property is created:

my_user=stackops_user

A **component property** can reference it by setting the value property as follows:

nova.user=$profile.my_user

A profile can be empty (returned by the get_template) half-filled, or full-filled. Is a dictionary-like structure with all the properties of the components the architecture can have.

.. note:: A profile must be used as an input at the moment to create a zone

Managing Profiles
-----------------

.. code-block:: bash

    profile-list        List all the profiles by architecture.
    profile-show        Show details about a profile by architecture.
    profile-create      Add a new profile by architecture.
    profile-update      Update a profile by architecture.
    profile-delete      Remove a specific profile by architecture.
    profile-json        Gets the JSON of the profile.
    profile-property-create
                        Create a profile property by architecture.
    profile-property-delete
                        Delete a profile property by architecture.
    profile-property-update
                        Update a profile property by architecture.


List profiles
^^^^^^^^^^^^^

At the moment to list profiles must be specified the ID architecture that has been taken

.. code-block:: bash

   $ help profile-list
   usage: automation profile-list <architecture-id>

   List all the profiles by architecture.

   Positional arguments:
    <architecture-id>  ID of the architecture.

   $ profile-list 1
   +----+-------------+
   | id |     name    |
   +----+-------------+
   | 1  | profile-doc |
   +----+-------------+


Show a specific profile
^^^^^^^^^^^^^^^^^^^^^^^

To show details about a profile, this one must be reference by its ID and must be specified the ID architecture that has been taken as reference

.. code-block:: bash

   $ profile-show 1 1
   +------------+------------------------------------------------+
   |  Property  |                     Value                      |
   +------------+------------------------------------------------+
   | components |                       {                        | 
   |            |                "name": "rabbitmq",             |
   |            |                  "properties": {               |
   |            |                      "install": {              |
   |            |                     "cluster": false,          |
   |            |                    "password": "guest"         |
   |            |                           },                   |
   |            |                      "start": {},              |
   |            |                      "stop": {},               |
   |            |                     "validate": {              |
   |            |                        "host": "",             |
   |            |                     "rpassword": null,         |
   |            |                       "rport": null,           |
   |            |                       "ruser": null,           |
   |            |                    "service_type": "",         |
   |            |                    "virtual_host": null        |
   |            |                           }                    |
   |            |                         }                      |
   |            |                       }                        |
   |     id     |                       1                        |
   |    name    |                  profile-doc                   |
   | properties |                       {                        |
   |            |     "fake_property_key": "fake_property_value" |
   |            |                       }                        |
   +------------+------------------------------------------------+


Create a profile
^^^^^^^^^^^^^^^^

To create a profile you must to specific the ID architecture to take as reference, the name of the profile and a JSON file that can be generate with the operation architecture-template.

.. code-block:: bash

   $ help profile-create
   usage: automation profile-create <architecture-id> <name> <profile-file>

   Add a new profile by architecture.

   Positional arguments:
     <architecture-id>  ID of the architecture to create a new profile on it
     <name>             Name for the new profile
     <profile-file>     File with extension .json describing the new profile to
                        create.

   $ create 1 profile-CLI profile-cli.json 
   +------------+----------------------------------+
   |  Property  |              Value               |
   +------------+----------------------------------+
   | components |                {                 |
   |            |         "name": "rabbitmq",      |
   |            |           "properties": {        |
   |            |               "install": {       |
   |            |              "cluster": false,   |
   |            |             "password": "guest"  |
   |            |                    },            |
   |            |               "start": {},       |
   |            |               "stop": {},        |
   |            |              "validate": {       |
   |            |                 "host": "",      |
   |            |              "rpassword": null,  |
   |            |                "rport": null,    |
   |            |                "ruser": null,    |
   |            |             "service_type": "",  |
   |            |             "virtual_host": null |
   |            |                    }             |
   |            |                  }               |
   |            |                }                 |
   |     id     |                2                 |
   |    name    |           profile-CLI            |
   | properties |                {}                |
   +------------+----------------------------------+

Modify a specific profile
^^^^^^^^^^^^^^^^^^^^^^^^^

To update a profile you must to specific the ID architecture, the ID of the profile and a JSON file that can be generate with the operation profile-json and modify it.

.. code-block:: bash

   $  help profile-update
   usage: automation profile-update <architecture-id> <profile-id> <profile-file>

   Update a profile by architecture.

   Positional arguments:
    <architecture-id>  ID of the architecture.
    <profile-id>       ID of the profile to update.
    <profile-file>     File with extension .json describing the profile to
                     modify.


   $ profile-update 1 2 profile-cli.json 
   +------------+----------------------------------+
   |  Property  |              Value               |
   +------------+----------------------------------+
   | components |                {                 |
   |            |         "name": "rabbitmq",      |
   |            |           "properties": {        |
   |            |               "install": {       |
   |            |              "cluster": false,   |
   |            |             "password": "guest"  |
   |            |                    },            |
   |            |               "start": {},       |
   |            |               "stop": {},        |
   |            |              "validate": {       |
   |            |                 "host": "",      |
   |            |              "rpassword": null,  |
   |            |                "rport": null,    |
   |            |                "ruser": null,    |
   |            |             "service_type": "",  |
   |            |             "virtual_host": null |
   |            |                    }             |
   |            |                  }               |
   |            |                }                 |
   |     id     |                2                 |
   |    name    |                                  |
   | properties |                {}                |
   +------------+----------------------------------+

Remove a specific profile
^^^^^^^^^^^^^^^^^^^^^^^^^

To delete you must to specific the ID architecture and the ID of the profile.

.. code-block:: bash

   $ profile-delete 1 2

Generate a JSON output from a specific profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is one of the most useful operations in the CLI given that to operate with the profiles' options most of times must be used a JSON profile file, also as input at the moment to create a zone.

To generate a JSON output you must to specific the ID architecture and the ID of the profile.

.. code-block:: bash 

   $ profile-json 1 1
   {
    "profile": {
        "id": 1,
        "name": "profile-doc",
        "components": [
            {
                "name": "mysql",
                "properties": {
                    "set_quantum": {
                        "root_pass": "stackops",
                        "quantum_password": "stackops",
                        "quantum_user": "quantum"
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
                        "glance_user": "glance",
                        "nova_user": "nova",
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
                }
            },
            {
                "name": "rabbitmq",
                "properties": {
                    "start": {},
                    "validate": {
                        "rpassword": null,
                        "virtual_host": null,
                        "host": "",
                        "ruser": null,
                        "service_type": "",
                        "rport": null
                    },
                    "stop": {},
                    "install": {
                        "cluster": false,
                        "password": "guest"
                    }
                }
            }
        ],
        "properties": {
            "fake_property_key": "fake_property_value"
        }
     }
   }

Create a profile property
^^^^^^^^^^^^^^^^^^^^^^^^^

To create a profile property you must to specific the ID architecture and the ID of the profile are mandatories, thus as the key and value of it

.. code-block:: bash

   $ help profile-property-create
   usage: automation profile-property-create <architecture-id> <profile-id>
                                             <property-key> <property-value>

   Create a profile property by architecture.

   Positional arguments:
     <architecture-id>  ID of the architecture to create a new property profile
                        on it
     <profile-id>       ID of the profile to create a property.
     <property-key>     The key property.
     <property-value>   The value property

   $ profile-property-create 1 1 cli-key-property cli-value-propery
   +------------+------------------------------------------------+
   |  Property  |                     Value                      |
   +------------+------------------------------------------------+
   | components |                       {                        |
   |            |                "name": "rabbitmq",             |
   |            |                  "properties": {               |
   |            |                      "install": {              |
   |            |                     "cluster": false,          |
   |            |                    "password": "guest"         |
   |            |                           },                   |
   |            |                      "start": {},              |
   |            |                      "stop": {},               |
   |            |                     "validate": {              |
   |            |                        "host": "",             |
   |            |                     "rpassword": null,         |
   |            |                       "rport": null,           |
   |            |                       "ruser": null,           |
   |            |                    "service_type": "",         |
   |            |                    "virtual_host": null        |
   |            |                           }                    |
   |            |                         }                      |
   |            |                       }                        |
   |     id     |                       1                        |
   |    name    |                  profile-doc                   |
   | properties |                       {                        |
   |            |      "cli-key-property": "cli-value-propery",  |
   |            |     "fake_property_key": "fake_property_value" |
   |            |                       }                        |
   +------------+------------------------------------------------+

Modify specifc profile property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To update a profile property you must to specific the ID architecture, the ID of the profile are mandatories and the key of it.

.. code-block:: bash
   
   $ help profile-property-update
   usage: automation profile-property-update <architecture-id> <profile-id>
                                             <property-key> <property-value>

   Update a profile property by architecture.

   Positional arguments:
     <architecture-id>  ID of the architecture to update a new property profile
                        on it
     <profile-id>       ID of the profile to update a property.
     <property-key>     The key property.
     <property-value>   The value property

  $ profile-property-update 1 1 cli-key-property cli-value-property_update
  +------------+------------------------------------------------------+
  |  Property  |                        Value                         |
  +------------+------------------------------------------------------+
  | components |                          {                           |
  |            |                   "name": "rabbitmq",                |
  |            |                     "properties": {                  |
  |            |                         "install": {                 |
  |            |                        "cluster": false,             |
  |            |                       "password": "guest"            |
  |            |                              },                      |
  |            |                         "start": {},                 |
  |            |                         "stop": {},                  |
  |            |                        "validate": {                 |
  |            |                           "host": "",                |
  |            |                        "rpassword": null,            |
  |            |                          "rport": null,              |
  |            |                          "ruser": null,              |
  |            |                       "service_type": "",            |
  |            |                       "virtual_host": null           |
  |            |                              }                       |
  |            |                            }                         |
  |            |                          }                           |
  |     id     |                          1                           |
  |    name    |                     profile-doc                      |
  | properties |                          {                           |
  |            |     "cli-key-property": "cli-value-property_update", |
  |            |        "fake_property_key": "fake_property_value"    |
  |            |                          }                           |
  +------------+------------------------------------------------------+

Remove a specific profile property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To delete a profile property you must to specific the ID architecture, the ID of the profile and the key of it

.. code-block:: bash

   $ help profile-property-delete
   usage: automation profile-property-delete <architecture-id> <profile-id>
                                             <property-key>

   Delete a profile property by architecture.

   Positional arguments:
     <architecture-id>  ID of the architecture to delete a new property profile
                     on it
     <profile-id>       ID of the profile to delete a property.
     <property-key>     The key property.

  $ profile-property-delete 1 1 cli-key-property
  +------------+------------------------------------------------+
  |  Property  |                     Value                      |
  +------------+------------------------------------------------+
  | components |                       {                        |
  |            |                "name": "rabbitmq",             |
  |            |                  "properties": {               |
  |            |                      "install": {              |
  |            |                     "cluster": false,          |
  |            |                    "password": "guest"         |
  |            |                           },                   |
  |            |                      "start": {},              |
  |            |                      "stop": {},               |
  |            |                     "validate": {              |
  |            |                        "host": "",             |
  |            |                     "rpassword": null,         |
  |            |                       "rport": null,           |
  |            |                       "ruser": null,           |
  |            |                    "service_type": "",         |
  |            |                    "virtual_host": null        |
  |            |                           }                    |
  |            |                         }                      |
  |            |                       }                        |
  |     id     |                       1                        |
  |    name    |                  profile-doc                   |
  | properties |                       {                        |
  |            |     "fake_property_key": "fake_property_value" |
  |            |                       }                        |
  +------------+------------------------------------------------+
