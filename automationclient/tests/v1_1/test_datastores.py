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
from automationclient.v1_1.datastores import Datastore
from automationclient.v1_1.zones import Zone
from automationclient.v1_1.roles import Role
from automationclient.v1_1.components import Component

cs = fakes.FakeClient()


def _datastore():
    return {
        "datastore": {
            "status": "AVAILABLE",
            "id_nova_zone": 2,
            "updated_at": "2013-11-26 14:16:14",
            "actions": [],
            "href": "http://0.0.0.0:8089/v1.1/datastores/1",
            "id": "1",
            "endpoint": "192.168.1.52",
            "parameters": "defaults",
            "id_storage_types": "NFS",
            "store": "/mnt/ada42",
            "identifier": "nfs1",
            "resource_type": "VOLUMES"
        }
    }


class DatastoreTest(utils.TestCase):

    def test_datastore_list(self):
        datastores = cs.datastores.list()
        cs.assert_called('GET', '/datastores')
        self.assertEqual(len(datastores), 2)
        [self.assertTrue(isinstance(datastore, Datastore)) for datastore in
         datastores]

    def test_datastore_show(self):
        datastore = cs.datastores.get(1234)
        cs.assert_called('GET', '/datastores/1234')
        self.assertIsInstance(datastore, Datastore)

    def test_datastore_space(self):
        datastore = cs.datastores.space(1234)
        cs.assert_called('GET', '/datastores/1234/space')
        self.assertIsInstance(datastore, Datastore)

    def test_datastore_content(self):
        datastore = cs.datastores.content(1234)
        cs.assert_called('GET', '/datastores/1234/content')
        self.assertIsInstance(datastore, Datastore)

    def test_datastore_delete(self):
        cs.datastores.delete(1234)
        cs.assert_called('DELETE', '/datastores/1234')

    def test_datastore_update(self):
        datastore = cs.datastores.get(1234)
        cs.assert_called('GET', '/datastores/1234')
        self.assertIsInstance(datastore, Datastore)
        options = {'parameters': "par1 par2"}
        datastore = cs.datastores.update(datastore, **options)
        cs.assert_called('PUT', '/datastores/1234')
        self.assertIsInstance(datastore, dict)

    def test_datastore_discovery(self):
        options = {'storage_type': 'NFS', 'endpoint': '127.0.0.1'}
        datastores = cs.datastores.discovery(**options)
        cs.assert_called('POST', '/datastores/discovery', options)
        self.assertEqual(len(datastores), 2)
        [self.assertTrue(isinstance(datastore, Datastore)) for datastore in
         datastores]

    def test_datastore_attach(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get_zone_role(zone, role, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234/components/1234')
        self.assertIsInstance(component, Component)
        datastore = cs.datastores.get(1234)
        cs.assert_called('GET', '/datastores/1234')
        self.assertIsInstance(datastore, Datastore)
        options = {'id_zone': 1234, 'id_role': 1234, 'resource': 'images',
                   'secure': '', 'component_name': 1234}
        datastore = cs.datastores.attach(datastore, **options)
        cs.assert_called('PUT', '/datastores/1234/attach', options)
        self.assertIsInstance(datastore, dict)

    def test_datastore_detach(self):
        zone = cs.zones.get(1234)
        cs.assert_called('GET', '/zones/1234')
        self.assertIsInstance(zone, Zone)
        role = cs.roles.get(zone, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234')
        self.assertIsInstance(role, Role)
        component = cs.components.get_zone_role(zone, role, 1234)
        cs.assert_called('GET', '/zones/1234/roles/1234/components/1234')
        self.assertIsInstance(component, Component)
        datastore = cs.datastores.get(1234)
        cs.assert_called('GET', '/datastores/1234')
        self.assertIsInstance(datastore, Datastore)
        options = {'force': None, 'id_role': 4, 'component_name': 1234}
        datastore = cs.datastores.detach(datastore, **options)
        cs.assert_called('PUT', '/datastores/1234/detach', options)
        self.assertIsInstance(datastore, dict)
