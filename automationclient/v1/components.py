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


"""Component Type interface."""

from automationclient import base


class Component(base.Resource):
    """A Component is a Stackops or Openstack service to be deployed."""
    def __repr__(self):
        return "<ComponentType: %s>" % self.name


class ComponentManager(base.ManagerWithFind):
    """Manage :class:`VolumeType` resources."""
    resource_class = Component

    def list(self):
        """Get a list of all volume types.

        :rtype: list of :class:`Component`.
        """
        return self._list("/types", "volume_types")

    def get(self, volume_type):
        """Get a specific volume type.

        :param volume_type: The ID of the :class:`VolumeType` to get.
        :rtype: :class:`Component`
        """
        return self._get("/types/%s" % base.getid(volume_type), "volume_type")

    def delete(self, volume_type):
        """Delete a specific volume_type.

        :param volume_type: The ID of the :class:`VolumeType` to get.
        """
        self._delete("/types/%s" % base.getid(volume_type))

    def create(self, name):
        """Create a volume type.

        :param name: Descriptive name of the volume type
        :rtype: :class:`Component`
        """

        body = {
            "volume_type": {
                "name": name,
            }
        }

        return self._create("/types", body, "volume_type")

