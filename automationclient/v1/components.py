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


"""Component interface."""

from automationclient import base

__author__ = 'jvalderrama'


class Component(base.Resource):
    """A Component is a Stackops or Openstack service to be deployed."""
    def __repr__(self):
        return "<Component: %s>" % self.name


class ComponentManager(base.ManagerWithFind):
    """Manage :class:`Component` resources."""
    resource_class = Component

    def list(self):
        """Get a list of all component.

        :rtype: list of :class:`Component`.
        """
        return self._list("/components", "components")

    def get(self, component):
        """Get a specific component.

        :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`
        """
        return self._get("/components/%s" % base.getid(component), "component")

    def list_zone_role(self, zone, role):
        """Get all components by zone and role.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`
        """
        return self._list("/zones/%s/roles/%s/components" % (base.getid(zone),
                                                             base.getid(role)),
                          "components")

    def get_zone_role(self, zone, role, component):
        """Get a component by zone and role.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`

         :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`
        """

        return self._get("/zones/%s/roles/%s/components/%s"
                         % (base.getid(zone),
                            base.getid(role),
                            component.name),
                         "component")

    def update_zone_role(self, zone, role, component, component_file):
        """Update a component by zone and role.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`

         :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`
        """

        if not component_file:
            return

        return self._update("/zones/%s/roles/%s/components/%s"
                            % (base.getid(zone),
                               base.getid(role),
                               component.name),
                            component_file)
