# Copyright 2013 OpenStack LLC

# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from automationclient import client
from automationclient.v1_1 import devices
from automationclient.v1_1 import components
from automationclient.v1_1 import services
from automationclient.v1_1 import architectures
from automationclient.v1_1 import profiles
from automationclient.v1_1 import properties
from automationclient.v1_1 import zones
from automationclient.v1_1 import tasks
from automationclient.v1_1 import roles
from automationclient.v1_1 import nodes


class Client(object):
    """
    Top-level object to access the Stackops Automation API.

    Create an instance with your creds::

        >>> client = Client(USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)

    Then call methods on its managers::

        >>> client.components.list()
        ...

    """

    def __init__(self, username, api_key, project_id=None, auth_url='',
                 insecure=False, timeout=None, tenant_id=None,
                 proxy_tenant_id=None, proxy_token=None, region_name=None,
                 endpoint_type='publicURL', extensions=None,
                 service_type='automation', service_name=None,
                 retries=None, http_log_debug=False,
                 cacert=None):
        # FIXME(comstud): Rename the api_key argument above when we
        # know it's not being used as keyword argument
        password = api_key

        # extensions
        self.devices = devices.DeviceManager(self)
        self.components = components.ComponentManager(self)
        self.services = services.ServiceManager(self)
        self.architectures = architectures.ArchitectureManager(self)
        self.profiles = profiles.ProfileManager(self)
        self.properties = properties.PropertyManager(self)
        self.zones = zones.ZoneManager(self)
        self.nodes = nodes.NodeManager(self)
        self.tasks = tasks.TaskManager(self)
        self.roles = roles.RoleManager(self)

        # Add in any extensions...
        if extensions:
            for extension in extensions:
                if extension.manager_class:
                    setattr(self, extension.name,
                            extension.manager_class(self))

        self.client = client.HTTPClient(
            username,
            password,
            project_id,
            auth_url,
            insecure=insecure,
            timeout=timeout,
            tenant_id=tenant_id,
            proxy_token=proxy_token,
            proxy_tenant_id=proxy_tenant_id,
            region_name=region_name,
            endpoint_type=endpoint_type,
            service_type=service_type,
            service_name=service_name,
            retries=retries,
            http_log_debug=http_log_debug,
            cacert=cacert)

    def authenticate(self):
        """
        Authenticate against the server.

        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.

        Returns on success; raises :exc:`exceptions.Unauthorized` if the
        credentials are wrong.
        """
        self.client.authenticate()

    def get_automation_api_version_from_endpoint(self):
        return self.client.get_automation_api_version_from_endpoint()
