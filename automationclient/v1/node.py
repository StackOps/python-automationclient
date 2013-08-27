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


"""Node interface."""

from automationclient import base


class Node(base.Resource):
    """Node is a device in the pool
    """
    def __repr__(self):
        return "<Node: %s>" % self.name


class NodeManager(base.ManagerWithFind):
    """Manage :class:`Node` resources."""
    resource_class = Node

    def list(self):
        """Get a list of all pool.

        :rtype: list of :class:`Node`.
        """
        return self._list("/pool/devices", "nodes")

    def get(self, node):
        """Get a specific node from pool.

        :param node: The ID of the :class: `Node` to get.
        :rtype: :class:`Node`
        """
        return self._get("/pool/devices/%s" % base.getid(node), "node")

    def activate(self, node):
        """
        Activate a node.

        :param node: Node to activate
        """
        return self._action('activate', node, {'node': node})

    def power_on(self, node):
        """
        Power on a node.

        :param node: Node to power on
        """

        return self._action('poweron', node, {'node': node})

    def power_off(self, node):
        """
        Power off a node.

        :param node: Node to power off
        """

        return self._action('poweroff', node, {'node': node})

    def reboot(self, node):
        """
        Reboot a node.

        :param node: Node to reboot
        """

        return self._action('reboot', node, {'node': node})

    def update(self, node, **kwargs):
        """
        Update the lom_ip or lom_mac for a node.

        :param node: The :class:`Node` to update.
        """
        if not kwargs:
            return

        body = {"node": kwargs}

        self._update("/pool/devices/%s" % base.getid(node), body)

    def delete(self, node):
        """
        Delete a node in the pool.

        :param node: The :class:`Node` to delete.
        """
        self._delete("/pool/devices/%s" % base.getid(node))

    def _action(self, action, node, info=None, **kwargs):
        """
        Perform a node action.
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/pool/devices/%s/%s' % (base.getid(node), action)
        return self.api.client.post(url, body=body)
