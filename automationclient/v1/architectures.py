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


"""Architecture interface."""

from automationclient import base

__author__ = 'jvalderrama'


class Architecture(base.Resource):
    """An Architecture is reference structure of components defined by
    Stackops or Openstack to create a deploy.
    """
    def __repr__(self):
        return "<Architecture: %s>" % self.name


class ArchitectureManager(base.ManagerWithFind):
    """Manage :class:`Architecture` resources."""
    resource_class = Architecture

    def list(self):
        """Get a list of all architectures.

        :rtype: list of :class:`Architectures`.
        """
        return self._list("/archs", "architectures")

    def get(self, architecture):
        """Get a specific architecture.

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`
        """
        return self._get("/archs/%s" % base.getid(architecture),
                         "architecture")

    def create(self, architecture):
        """
        Create a volume.

        :param architecture: Architecture JSON format define
        """

        body = architecture

        return self._create('/archs', body, 'architecture')

    def delete(self, architecture):
        """
        Delete an architecture.

        :param architecture: The :class:`Architecture` to delete.
        """
        self._delete("/archs/%s" % base.getid(architecture))
