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


"""Nodes interface."""

from automationclient import base


__author__ = 'jvalderrama'


class Node(base.Resource):
    """A Node is activate device from pool in a zone."""

    def __repr__(self):
        return "<Node: %s>" % self.name


class NodeManager(base.ManagerWithFind):
    """Manage :class:`Node` resources."""
    resource_class = Node

    def list(self, zone):
        """Get a list of nodes by a specific zone.

        :param zone: The ID of the :class: `Zone` to get its nodes.
        :rtype: :class:`Zone`
        """
        return self._list("/zones/%s/nodes" % base.getid(zone),
                          "nodes")

    def get(self, zone, node):
        """Get a specific node by zone.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param profile: The ID of the :class: `Node` to get.
        :rtype: :class:`Node`
        """
        return self._get("/zones/%s/nodes/%s" % (base.getid(zone), node),
                         "node")
