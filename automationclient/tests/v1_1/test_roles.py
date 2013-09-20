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

cs = fakes.FakeClient()


def _component():
    return {
        "component": {
            "properties": {
                "set_quantum": {
                    "root_pass": "stackops",
                    "quantum_user": "quantum",
                    "quantum_password": "stackops"
                },
                "set_keystone": {
                    "root_pass": "stackops",
                    "keystone_password": "stackops",
                    "keystone_user": "keystone"
                },
                "teardown": {},
                "set_cinder": {
                    "cinder_user": "cinder",
                    "root_pass": "stackops",
                    "cinder_password": "stackops"
                },
                "set_automation": {
                    "automation_password": "stackops",
                    "root_pass": "stackops",
                    "automation_user": "automation"
                },
                "set_accounting": {
                    "accounting_user": "activity",
                    "root_pass": "stackops",
                    "accounting_password": "stackops"
                },
                "set_nova": {
                    "root_pass": "stackops",
                    "nova_password": "stackops",
                    "nova_user": "nova"
                },
                "install": {
                    "root_pass": "stackops",
                    "keystone_user": "keystone",
                    "cinder_user": "cinder",
                    "quantum_password": "stackops",
                    "glance_password": "stackops",
                    "automation_user": "automation",
                    "quantum_user": "quantum",
                    "automation_password": "stackops",
                    "keystone_password": "stackops",
                    "cinder_password": "stackops",
                    "nova_user": "nova",
                    "glance_user": "glance",
                    "nova_password": "stackops"
                },
                "set_glance": {
                    "root_pass": "stackops",
                    "glance_password": "stackops",
                    "glance_user": "glance"
                },
                "validate": {
                    "username": "",
                    "drop_schema": None,
                    "install_database": None,
                    "database_type": "",
                    "host": "",
                    "password": "",
                    "port": "",
                    "schema": ""
                },
                "set_portal": {
                    "root_pass": "stackops",
                    "portal_user": "portal",
                    "portal_password": "stackops"
                }
            },
            "name": "mysql",
            "id": 1234
        }
    }


class RolesTest(utils.TestCase):

    def test_role_list(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        roles = cs.roles.list(zone)
        cs.assert_called('GET', '/zones/1234/roles')
        self.assertEqual(len(roles), 2)
        [self.assertTrue(isinstance(role, Role)) for role in roles]

    def test_role_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)

    def test_role_component_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get_zone_role(zone, role, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234/components/1234')
        self.assertIsInstance(component, Component)

    def test_role_component_update(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get_zone_role(zone, role, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234/components/1234')
        self.assertIsInstance(component, Component)
        options = _component()
        component = cs.components.update_zone_role(zone, role, component.id,
                                                   options)
        cs.assert_called('PUT', '/zones/1234/roles/1234/components/1234',
                         body=options)
        self.assertIsInstance(component, dict)

    def test_role_component_json(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        components = cs.components.list_zone_role(zone, role)
        cs.assert_called('GET', '/zones/1234/roles/1234/components')
        self.assertEqual(len(components), 2)
        [self.assertTrue(isinstance(component, Component)) for component in components]
        json_components = utils.from_manager_to_dict(components)
        [self.assertTrue(isinstance(comp, dict)) for comp in json_components]
