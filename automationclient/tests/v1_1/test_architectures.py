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
from automationclient.v1_1.profiles import Profile


cs = fakes.FakeClient()


class DevicesTest(utils.TestCase):

    def test_architecture_list(self):
        architectures = cs.architectures.list()
        cs.assert_called('GET', '/archs')
        self.assertEqual(len(architectures), 2)
        [self.assertTrue(isinstance(arc, Architecture))
         for arc in architectures]

    def test_architecture_show(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)

    def test_architecture_create(self):
        options = {
            "architecture": {
                "name": "singlenode_test",
                "roles": [
                    {
                        "name": "controller",
                        "steps": [
                            {
                                "1": [
                                    "storage"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        architecture = cs.architectures.create(options)
        cs.assert_called('POST', '/archs', body=options)
        self.assertIsInstance(architecture, Architecture)

    def test_architecture_delete(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        cs.architectures.delete(architecture)
        cs.assert_called('DELETE', '/archs/1234')

    def test_architecture_template(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.template(architecture)
        cs.assert_called('GET', '/archs/1234/get_template')
        self.assertIsInstance(profile, Profile)
