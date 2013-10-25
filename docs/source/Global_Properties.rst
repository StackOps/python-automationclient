Global Properties
=================

What are Global Properties?
---------------------------

Global properties is a high level repository that keeps a set of properties of the key/value form and are **defined by Stackops or the same User**; helps to define a **component of the catalog** and its properties previously, but also these properties (used in the catalog components: mysql, rabbitmq, keystone, etc) can be modified once again but setting its own value; but take into account the next:

	- The global property must be a reference of the whole componets that use it, that means if the property is **called automation.user** in the global properties and we going to work 
          with the mysql component or rabbitmq component and this two components have a property called user the default value will be the given at the moment to define the global property:

.. code-block:: bash
  
   'mysql': {'automation_user': '$automation.user'}
   'rabbitmq': {'user': '$automation.user'}

Managing Global Properties
--------------------------

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

List all the properties that are available on automation.

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

To create a new global property you must to provide its key and value as mandatories

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

To modify a global property you must to provide its key and its new value as mandatories

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

To delete a global property you must to provide its key as mandatory

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

