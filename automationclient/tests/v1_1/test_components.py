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
from automationclient.v1_1.components import Component
from automationclient.v1_1.services import Service


cs = fakes.FakeClient()


class ComponentsTest(utils.TestCase):

    def test_component_list(self):
        components = cs.components.list()
        cs.assert_called('GET', '/components')
        self.assertEqual(len(components), 2)
        [self.assertTrue(isinstance(comp, Component)) for comp in components]

    def test_component_show(self):
        component = cs.components.get(1234)
        cs.assert_called('GET', '/components/1234')
        self.assertIsInstance(component, Component)

    def test_component_services(self):
        component = cs.components.get(1234)
        cs.assert_called('GET', '/components/1234')
        services = cs.services.list(component)
        cs.assert_called('GET', '/components/1234/services')
        self.assertEqual(len(services), 11)
        [self.assertTrue(isinstance(ser, Service)) for ser in services]
