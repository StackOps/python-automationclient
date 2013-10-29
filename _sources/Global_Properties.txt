Global Properties
=================

What are Global Properties?
---------------------------

A global property is a global variable that is stored in **Automation** and can be referenced by zone or architecture properties. The contents of a global property can vary, but they often include sensitive information (such as database passwords).

Global properties is a high level repository that keeps a set of properties of the key/value form and are **defined by Stackops or the same User**; help to define a **component of the catalog** and its properties previously, but also these properties (used in the catalog components: mysql, rabbitmq, keystone, etc) can be modified as much as you want taken into account the next consideration:

	- The global property must be a reference of the whole componets that use it, that means if the property is called **globals.user** in the global properties and we going to work 
          with the **mysql component or rabbitmq component** and this two components have a property called **user** the default value will be the given at the moment to define the global 
          property:

.. code-block:: bash
  
   'mysql': {'automation_user': '$globals.user'}
   'rabbitmq': {'user': '$globals.user'}


How global properties can be referenced?
----------------------------------------

The basic way to use a global property is using the **$globals prefix** when setting a property. For instance, if a property **mysql.host** wants to use the global property **database_password**, the content of **mysql.root_password** should be:

.. code-block:: bash
  
   {... : {"mysql": {"root_password": $globals.database_password}}}

In some situations, we want that general properties be referenced automatically by global properties. For example, if we want that every component property **root_password** had the same password content, we should first create a global property called **root.property**:

.. code-block:: bash
  
   {... :{"mysql": {"root_password": my_secret}}}

Secondly, when the user will create a **profile**, every property matching **component.root_password** will be filled with **$globals.root.password**.


Managing Global Properties
--------------------------

The operations allowed in the python-automatioclient are:

.. code-block:: bash
    
   global-property-list
                       List all the properties that are available on
   global-property-create
                       Add a new property.
   global-property-update
                       Updates a property.
                       automation.
   global-property-delete
                       Delete a property.

List global properties
^^^^^^^^^^^^^^^^^^^^^^

List alli global properties that are available in automation.


.. code-block:: bash

   $ global-property-list
   +----------------+-----------------+
   |    Property    |      Value      |
   +----------------+-----------------+
   | key_docu_cli_1 | key_value_cli_1 |
   | key_docu_cli_2 | key_value_cli_2 |
   +----------------+-----------------+ 

Create a new global property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a new global property you must provide its key and value as mandatories

.. code-block:: bash

   $ help global-property-create
   usage: automation global-property-create <property-key> <property-value>

   Add a new property. :param cs: :param args:

   Positional arguments:
     <property-key>    The key property.
     <property-value>  The value property

   $ global-property-create key_docu_cli_3 key_value_cli_3
   +----------------+-----------------+
   |    Property    |      Value      |
   +----------------+-----------------+
   | key_docu_cli_1 | key_value_cli_1 |
   | key_docu_cli_2 | key_value_cli_2 |
   | key_docu_cli_3 | key_value_cli_3 |
   +----------------+-----------------+ 

Update a specific global property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To modify a global property you must provide its key and its new value as mandatories

.. code-block:: bash

   $ help global-property-update
   usage: automation global-property-update <property-key> <property-value>

   Updates a property. :param cs: :param args:

   Positional arguments:
     <property-key>    The key property.
     <property-value>  The value property

   $ global-property-update key_docu_cli_3 key_value_cli_3_update
   +----------------+------------------------+
   |    Property    |         Value          |
   +----------------+------------------------+
   | key_docu_cli_1 |    key_value_cli_1     |
   | key_docu_cli_2 |    key_value_cli_2     |
   | key_docu_cli_3 | key_value_cli_3_update |
   +----------------+------------------------+

Delete a specific global property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To delete a global property you must provide its key as mandatory

.. code-block:: bash

   $ help global-property-delete
   usage: automation global-property-delete <property-key>

   Delete a property. :param cs: :param args:

   Positional arguments:
     <property-key>  The key property.

   $ global-property-delete key_docu_cli_3
   +----------------+------------------------+
   |    Property    |         Value          |
   +----------------+------------------------+
   | key_docu_cli_1 |    key_value_cli_1     |
   | key_docu_cli_2 |    key_value_cli_2     |
   +----------------+------------------------+
