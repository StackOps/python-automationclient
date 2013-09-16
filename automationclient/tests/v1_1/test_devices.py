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
from automationclient.v1_1.devices import Device


cs = fakes.FakeClient()


class DevicesTest(utils.TestCase):

    def test_device_show(self):
        device = cs.devices.get(1234)
        cs.assert_called('GET', '/pool/devices/1234')
        self.assertIsInstance(device, Device)

    '''def test_device_delete(self):
        dev = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        cs.devices.delete(dev)
        cs.assert_called('DELETE', '/pool/devices/%s' % dev._info['id'])'''
