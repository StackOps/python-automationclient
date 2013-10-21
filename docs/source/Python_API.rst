Python API
==========

In order to use the python api directly, you must first obtain an auth token and identify which endpoint you wish to speak to. Once you have done so, you can use the API like so:

>>> from automationclient import Client
>>> automation = Client('1', endpoint=OS_AUTOMATION_ENDPOINT, token=OS_AUTH_TOKEN)
>>> components = automation.componentes.list()
