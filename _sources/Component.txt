Components
==========

What is a Component?
--------------------

A component is the most fundamental configuration element in **FABuloso**, where each component has a set of gathered services, these services have methods that define a specific configuration of an **Openstack or Stackops Service**, previously a set of properties that define to itself.

`FABuloso <http://fabuloso.stackops.org/index.html>`_ is a python tool to easily organize and deploy an OpenStack architecture using Fabric. FABuloso manages configuration with components within **catalogs**.

.. figure:: /images/openstackComponents.png
    :width: 800pt
    :align: center
    :alt: Some Openstack Components

    **Some Openstack Components**


What is Catalog Components?
------------------------------

The Catalog components are a set of components by itself, used to deploy an Openstack Architecture, this catalog are hosted in github as an open project `here <https://github.com/StackOps/fabuloso-catalog>`_

Mananing Components
-------------------

The operations allowed in the python-automatioclient are:

.. code-block:: bash

   component-list      List all the components that are available on
                       automation.
   component-show      Show details about a component
   component-services  List all the services by a component

List components
^^^^^^^^^^^^^^^

.. code-block:: bash

   $ component-list
   +-----------------+
   |       name      |
   +-----------------+
   |    accounting   |
   |      apache     |
   |    automation   |
   |      cinder     |
   |     compute     |
   |       fake      |
   |      glance     |
   |     keystone    |
   |      mysql      |
   |       nova      |
   |        os       |
   |       portal    |
   |     quantum     |
   | quantum_plugins |
   |     rabbitmq    |
   |     storage     |
   |      swift      |
   +-----------------+


Show a specific component
^^^^^^^^^^^^^^^^^^^^^^^^^

To show details about a specific component this one must be reference by its name

.. code-block:: bash

   $ component-show mysql
   +------------+--------------------------------------------+
   |  Property  |                   Value                    |
   +------------+--------------------------------------------+
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

List services by a specific component
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To list the set of services of a component this one must be reference by its name


.. code-block:: bash

   $ component-services mysql
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
