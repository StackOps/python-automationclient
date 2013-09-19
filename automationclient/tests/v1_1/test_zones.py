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
from automationclient.v1_1.architectures import Architecture
from automationclient.v1_1.zones import Zone
from automationclient.v1_1.tasks import Task


cs = fakes.FakeClient()


def _zone():
    return {
        "zone": {
            "name": "fake_zone",
            "properties": {
                    "fake_property_key": "fake_property_value"
            },
            "_links": None,
            "components": [
                {
                    "name": "mysql",
                    "properties": [
                        {
                            "set_quantum": {
                                "root_pass": "stackops",
                                "quantum_password": "stackops",
                                "quantum_user": "quantum"
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
                                "glance_user": "glance",
                                "nova_user": "nova",
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
                        }
                    ]
                },
                {
                    "name": "rabbitmq",
                    "properties": [
                        {
                            "start": {},
                            "validate": {
                                "rpassword": None,
                                "virtual_host": None,
                                "host": "",
                                "ruser": None,
                                "service_type": "",
                                "rport": None
                            },
                            "stop": {},
                            "install": {
                                "cluster": False,
                                "password": "guest"
                            }
                        }
                    ]
                }
            ]
        }
    }


class ZonesTest(utils.TestCase):

    def test_zone_list(self):
        zones = cs.zones.list()
        cs.assert_called('GET', '/zones')
        self.assertEqual(len(zones), 2)
        [self.assertTrue(isinstance(zone, Zone)) for zone in zones]

    def test_zone_show(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)

    def test_zone_create(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        options = _zone()
        zone = cs.zones.create(architecture, options)
        cs.assert_called('POST', '/archs/1234/apply', body=options)
        self.assertIsInstance(zone, Zone)

    def test_zone_delete(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        cs.zones.delete(zone)
        cs.assert_called('DELETE', '/zones/1234')

    def test_zone_json(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        json_zone = utils.from_manager_to_dict(zone)
        self.assertIsInstance(json_zone, dict)

    def test_zone_tasks(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        tasks = zone = cs.tasks.list(zone)
        cs.assert_called('GET', '/zones/1234/tasks')
        self.assertEqual(len(tasks), 2)
        [self.assertTrue(isinstance(task, Task)) for task in tasks]

    def test_zone_propery_create(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        #TODO(jvalderrama) Check options as body expected
        #options = _zone()
        zone = cs.zones.property_create(zone,
                                        'new_fake_property_key',
                                        'new_fake_property_key')
        cs.assert_called('PUT', '/zones/1234')
        self.assertIsInstance(zone, dict)

    def test_zone_propery_update(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        #TODO(jvalderrama) Check options as body expected
        #options = _zone()
        zone = cs.zones.property_update(zone,
                                        'fake_property_key',
                                        'fake_property_value')
        cs.assert_called('PUT', '/zones/1234')
        self.assertIsInstance(zone, dict)

    def test_zone_propery_delete(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        #TODO(jvalderrama) Check options as body expected
        #options = _zone()
        zone = cs.zones.property_delete(zone, 'fake_property_key')
        cs.assert_called('PUT', '/zones/1234')
        self.assertIsInstance(zone, dict)
