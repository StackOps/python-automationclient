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
from automationclient import exceptions


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

    def delete(self, zone):
        """
        Delete a zone.

        :param profile: The ID of the :class: `Zone` to delete.
        :rtype: :class:`Zone`
        """

        self._delete("/zones/%s" % base.getid(zone))

    def property_create(self, zone, property_key,
                        property_value):

        zone_dict = zone._info
        props_dict = zone_dict['properties']

        if property_key not in props_dict:
            props_dict[property_key] = property_value
        else:
            msg = "A zone property with a key: '%s' exists." % property_key
            raise exceptions.CommandError(msg)

        zone_dict['properties'] = props_dict
        del zone_dict['_links']
        zone_body = {"zone": zone_dict}

        return self._update("/zones/%s" % base.getid(zone), zone_body)

    def property_update(self, zone, property_key,
                        property_value):

        zone_dict = zone._info
        props_dict = zone_dict['properties']
        if property_key in props_dict:
            props_dict[property_key] = property_value
        else:
            msg = "No zone property with a key: '%s' exists." % property_key
            raise exceptions.CommandError(msg)

        zone_dict['properties'] = props_dict
        del zone_dict['_links']
        zone_body = {"zone": zone_dict}

        return self._update("/zones/%s" % base.getid(zone), zone_body)

    def property_delete(self, zone, property_key):

        zone_dict = zone._info
        props_dict = zone_dict['properties']

        if property_key in props_dict:
            del props_dict[property_key]
        else:
            msg = "No zone property with a key: '%s' exists." % property_key
            raise exceptions.CommandError(msg)

        zone_dict['properties'] = props_dict
        del zone_dict['_links']
        zone_body = {"zone": zone_dict}

        return self._update("/zones/%s" % base.getid(zone), zone_body)
