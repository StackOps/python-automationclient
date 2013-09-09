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

__author__ = 'jvalderrama'

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
        """Get a list of tasks by a specific zone.

        :param zone: The ID of the :class: `Zone` to get
        its tasks.
        :rtype: :class:`Zone`
        """
        return self._list("/zones/%s/tasks" % zone.id, "tasks")

    def deploy(self, zone, role, body):
        """
        Deploy a role.

        :param zone: The ID of the :class: `Zone` to get.
        :rtype: :class:`Zone`

        :param role: Profile JSON format define
        """

        body = body

        return self._create("/zones/%s/roles/%s/deploy" % (base.getid(zone),
                                                           base.getid(role)),
                            body, 'tasks')
