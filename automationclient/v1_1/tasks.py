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


"""Tasks interface."""

from automationclient import base


class Task(base.Resource):
    """A Task is set of steps to deploy an Openstack or Stackops
    component on a zone.
    """

    def __repr__(self):
        return "<Task: %s>" % self.name


class TaskManager(base.ManagerWithFind):
    """Manage :class:`Zone` resources."""
    resource_class = Task

    def list(self, zone):
        """Get a list of tasks by zone.

        :param zone: The ID of the :class: `Zone` to get
        its tasks.
        :rtype: :class:`Zone`
        """
        return self._list("/zones/%s/tasks" % zone.id, "tasks")

    def get(self, zone, task):
        """Get a specific task by zone.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param task: The ID of the :class: `Task` to get.
        :rtype: :class:`Task`
        """
        return self._get("/zones/%s/tasks/%s" % (base.getid(zone),
                                                 base.getid(task)),
                         "task")

    def deploy(self, zone, role, node):
        """Deploy a role ().

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param zone: The ID of the :class: `Role` to get.
        :rtype: :class:`Role`

        :param node: Node JSON format define
        """

        body = {
            'node': {
                'href': "http://localhost:8089/v1.1/zones/%s/nodes/%s"
                        % (base.getid(zone), base.getid(node))
            }
        }
        return self._list("/zones/%s/roles/%s/deploy"
                          % ((base.getid(zone),
                              base.getid(role))),
                          'tasks', body=body)

    def cancel(self, zone, node, task):
        """Cancel a task by zone and node.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Node` to get.
        :rtype: :class:`Node`

        :param role: The ID of the :class: `Task` to get.
        :rtype: :class:`Task`
        """

        return self.api.client.post("/zones/%s/nodes/%s/tasks/%s/cancel"
                                    % (base.getid(zone),
                                       base.getid(node),
                                       base.getid(task)))

    def list_node(self, zone, node):
        """Get all tasks by zone and node.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param profile: The ID of the :class: `Node` to get.
        :rtype: :class:`Node`
        """
        return self._list("/zones/%s/nodes/%s/tasks" % (base.getid(zone),
                                                        base.getid(node)),
                          "tasks")

    def get_node(self, zone, node, task):
        """Get a specific task by zone and node.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param profile: The ID of the :class: `Node` to get.
        :rtype: :class:`Node`

        :param profile: The ID of the :class: `Task` to get.
        :rtype: :class:`Task`
        """
        return self._get("/zones/%s/nodes/%s/tasks/%s" % (base.getid(zone),
                                                          base.getid(node),
                                                          task),
                         "task")

    def execute_service(self, zone, role, component, service):
        """Execute a specific service by zone, role, component

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: The ID of the :class: `Role` to get.
        :rtype: :class:`Zone`

        :param component: The ID (Name of the component) of the :class:
        `Component` to get.
        :rtype: :class:`Component`

        :param component: The ID of the :class: `Service` to get.
        :rtype: :class:`Service`
        """

        return self._list("/zones/%s/roles/%s/components/%s/services/%s"
                          % (base.getid(zone),
                             base.getid(role),
                             component.name,
                             service.name), "tasks", customize=True)
