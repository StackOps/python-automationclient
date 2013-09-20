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


"""Properties interface."""

from automationclient import base
from automationclient import exceptions


class Property(base.Resource):
    """A Property is a Stackops or Openstack service to be deployed."""
    def __repr__(self):
        return "<Property: %s>" % self.name


class PropertyManager(base.ManagerWithFind):
    """Manage :class:`Component` resources."""
    resource_class = Property

    def list(self):
        """Get a list of all properties.

        :rtype: list of :class:`Property`.
        """
        return self._list("/properties", "properties")

    def create(self, property_key, property_value):
        """
        Create a property.

        :param property_key: the key of the property
        :param property_value: the value the tue property
        """
        properties = self.list()
        if property_key not in properties:
            properties[property_key] = property_value
        else:
            msg = "A %s with a key: '%s' exists." % \
                  (self.resource_class.__name__.lower(), property_key)
            raise exceptions.CommandError(msg)

        return self._update("/properties", properties)

    def update(self, property_key, property_value):
        """
        Update the property key, property value

        :param property_key: the key of the property
        :param property_value: the value the tue property
        """
        properties = self.list()
        if property_key in properties:
            properties[property_key] = property_value
            return self._update("/properties", properties)
        else:
            msg = "No %s with a key '%s' exists." % \
                  (self.resource_class.__name__.lower(), property_key)
            raise exceptions.CommandError(msg)

    def delete(self, property_key):
        """
        Delete the property key, property value

        :param property_key: the key of the property
        :param property_value: the value the tue property
        """
        properties = self.list()
        if property_key in properties:
            del properties[property_key]
            return self._update("/properties", properties)
        else:
            msg = "No %s with a key '%s' exists." % \
                  (self.resource_class.__name__.lower(), property_key)
            raise exceptions.CommandError(msg)

    def _list(self, url, response_key, obj_class=None, body=None):
        resp = None
        if body:
            resp, body = self.api.client.post(url, body=body)
        else:
            resp, body = self.api.client.get(url)

        data = body[response_key]
        return data

    def _update(self, url, body):
        resp, body = self.api.client.put(url, body=body)
        return body
