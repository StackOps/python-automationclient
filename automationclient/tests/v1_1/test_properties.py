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

cs = fakes.FakeClient()


class PropertiesTest(utils.TestCase):

    def test_global_property_list(self):
        properties = cs.properties.list()
        cs.assert_called('GET', '/properties')
        self.assertIsInstance(properties, dict)

    def test_global_property_create(self):
        properties = cs.properties.create('new_fake_property_key',
                                          'new_fake_property_value')
        #TODO(jvalderrama) Check options as body expected
        #expected = {"properties": {
        #    "sample-property1": 1234,
        #    "sample-property2": 5678,
        #    "new_fake_property_key": "new_fake_property_value"
        #}}
        cs.assert_called('PUT', '/properties')
        self.assertIsInstance(properties, dict)

    def test_global_property_update(self):
        properties = cs.properties.update('sample-property2', '9870')
        #TODO(jvalderrama) Check options as body expected
        #expected = {"properties": {
        #    "sample-property1": 1234,
        #    "sample-property2": 9870
        #}}
        cs.assert_called('PUT', '/properties')
        self.assertIsInstance(properties, dict)

    def test_global_property_delete(self):
        properties = cs.properties.delete('sample-property2')
        #TODO(jvalderrama) Check options as body expected
        #expected = {"properties": {
        #    "sample-property1": 1234
        #}}
        cs.assert_called('PUT', '/properties')
        self.assertIsInstance(properties, dict)
