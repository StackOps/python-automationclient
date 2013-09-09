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


"""Zones interface."""

from automationclient import base

__author__ = 'jvalderrama'


class Zone(base.Resource):
    """A Zone is a deployment of Openstack and Stackops components."""

    def __repr__(self):
        return "<Zone: %s>" % self.name


class ZoneManager(base.ManagerWithFind):
    """Manage :class:`Zone` resources."""
    resource_class = Zone

    def list(self):
        """Get a list of all zones.

        :rtype: :class:`Zone`
        """
        return self._list("/zones", "zones")

    def get(self, zone):
        """Get a specific zone .

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`
        """
        return self._get("/zones/%s" % base.getid(zone), "zone")

    def create(self, architecture, zone):
        """
        Create a zone.

        :param architecture: The ID of the :class: `Architecture` to take as
        base for the new zone.
        :rtype: :class:`Architecture`

        :param zone: Zone JSON format define
        """

        body = zone

        return self._create("/archs/%s/apply" % (base.getid(architecture)),
                            body, 'zone')

    def update(self, architecture, profile, profile_file):
        """
        Update the name, components

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`

        :param profile: The ID of the :class: `Profile` to update.
        :rtype: :class:`Zone`

        :param profile: Profile JSON format define with updates
        """
        if not profile_file:
            return

        self._update("/archs/%s/profiles/%s" % (base.getid(architecture),
                                                base.getid(profile)),
                     profile_file)

    def delete(self, zone):
        """
        Delete a zone.

        :param profile: The ID of the :class: `Zone` to delete.
        :rtype: :class:`Zone`
        """

        self._delete("/zones/%s" % base.getid(zone))
