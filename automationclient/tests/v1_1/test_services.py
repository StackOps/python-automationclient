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
from automationclient.v1_1.roles import Role
from automationclient.v1_1.components import Component
from automationclient.v1_1.services import Service
from automationclient.v1_1.tasks import Task

cs = fakes.FakeClient()


class ServiceTest(utils.TestCase):

    def test_service_list(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get(1234)
        cs.assert_called('GET', '/components/1234')
        self.assertIsInstance(component, Component)
        services = cs.services.list_zone_role_component(zone, role, component)
        self.assertEqual(len(services), 2)
        [self.assertTrue(isinstance(service, Service)) for service in services]

    def test_service_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get(1234)
        cs.assert_called('GET', '/components/1234')
        self.assertIsInstance(component, Component)
        service = cs.services.\
            get_zone_role_component(zone, role, component, 1234)
        cs.assert_called(
            'GET', '/zones/1234/roles/1234/components/1234/services/1234')
        self.assertIsInstance(service, Service)

    def test_service_execute(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get(1234)
        cs.assert_called('GET', '/components/1234')
        self.assertIsInstance(component, Component)
        service = cs.services.\
            get_zone_role_component(zone, role, component, 1234)
        cs.assert_called(
            'GET', '/zones/1234/roles/1234/components/1234/services/1234')
        self.assertIsInstance(service, Service)
        tasks = cs.tasks.execute_service(zone, role, component, service)
        self.assertEqual(len(tasks), 2)
        [self.assertTrue(isinstance(task, Task)) for task in tasks]
