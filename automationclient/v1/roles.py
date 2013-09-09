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


"""Roles interface."""

__author__ = 'jvalderrama'

from automationclient import base


class Role(base.Resource):
    """A Role is 'label' of a instance with some Openstack and/or Stackops
    components deployed"""

    def __repr__(self):
        return "<Role: %s>" % self.name


class RoleManager(base.ManagerWithFind):
    """Manage :class:`Role` resources."""
    resource_class = Role

    def list(self, zone):
        """Get a list of roles by a specific zone.

        :param zone: The ID of the :class: `Zone` to get
        its roles.
        :rtype: :class:`Zone`
        """
        return self._list("/zones/%s/roles" % zone.id, "roles")

    def get(self, zone, role):
        """Get a specific role by zone.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Role`
        """
        return self._get("/zones/%s/roles/%s" % (base.getid(zone), role),
                         "role")
