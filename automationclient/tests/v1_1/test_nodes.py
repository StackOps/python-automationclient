# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from automationclient.tests import utils
from automationclient.tests.v1_1 import fakes
from automationclient.v1_1.zones import Zone
from automationclient.v1_1.nodes import Node
from automationclient.v1_1.tasks import Task

cs = fakes.FakeClient()


class NodeTest(utils.TestCase):

    def test_node_list(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        nodes = cs.nodes.list(zone)
        cs.assert_called('GET', '/zones/1234/nodes')
        self.assertEqual(len(nodes), 2)
        [self.assertTrue(isinstance(node, Node)) for node in nodes]

    def test_node_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        node = cs.nodes.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/nodes/1234')
        self.assertIsInstance(node, Node)

    def test_node_tasks_list(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        node = cs.nodes.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/nodes/1234')
        self.assertIsInstance(node, Node)
        tasks = cs.tasks.list_node(zone, node)
        cs.assert_called('GET', '/zones/1234/nodes/1234/tasks')
        self.assertEqual(len(tasks), 2)
        [self.assertTrue(isinstance(task, Task)) for task in tasks]

    def test_node_task_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        node = cs.nodes.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/nodes/1234')
        self.assertIsInstance(node, Node)
        task = cs.tasks.get_node(zone, node, 1234)
        cs.assert_called('GET', '/zones/1234/nodes/1234/tasks/1234')
        self.assertIsInstance(task, Task)

    def test_node_task_cancel(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        node = cs.nodes.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/nodes/1234')
        self.assertIsInstance(node, Node)
        task = cs.tasks.cancel(zone, node, 1234)
        cs.assert_called('POST', '/zones/1234/nodes/1234/tasks/1234/cancel')
        self.assertIsInstance(task, tuple)
