# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Services interface."""

from automationclient import base

__author__ = 'jvalderrama'


class Service(base.Resource):
    """A Service is an extension of a Component class."""
    def __repr__(self):
        return "<Service: %s>" % self.name


class ServiceManager(base.ManagerWithFind):
    """Manage :class:`Service` resources."""
    resource_class = Service

    def list(self, component):
        """Get a list of services by a specific component.

        :param component: The ID (Name of the component) of the :class:
        `Component` to get its services.
        :rtype: :class:`Component`
        """
        return self._list("/components/%s/services" % component.name,
                          "services")

    def list_zone_role_component(self, zone, role, component):
        """Get all services by zone, role and component.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`

        :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`
        """
        return self._list("/zones/%s/roles/%s/components/%s/services"
                          % (base.getid(zone),
                             base.getid(role),
                             component.name),
                          "services")

    def get_zone_role_component(self, zone, role, component, service):
        """Get a service by zone, role and component.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`

         :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`

        :param role: The ID of the :class: `Service` to get.
        :rtype: :class:`Service`
        """
        return self._get("/zones/%s/roles/%s/components/%s/services/%s"
                         % (base.getid(zone),
                            base.getid(role),
                            component.name,
                            service),
                         "service")
