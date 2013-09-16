# Copyright 2011 OpenStack LLC.

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


import automationclient.client
import automationclient.v1_1.client
import automationclient.v2.client
from automationclient.tests import utils


class ClientTest(utils.TestCase):

    def test_get_client_class_v1_1(self):
        output = automationclient.client.get_client_class('1.1')
        self.assertEqual(output, automationclient.v1_1.client.Client)

    def test_get_client_class_v2(self):
        output = automationclient.client.get_client_class('2')
        self.assertEqual(output, automationclient.v2.client.Client)

    def test_get_client_class_unknown(self):
        self.assertRaises(automationclient.exceptions.UnsupportedVersion,
                          automationclient.client.get_client_class, '0')
