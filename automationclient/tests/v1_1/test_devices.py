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

    def test_device_list(self):
        devices = cs.devices.list()
        cs.assert_called('GET', '/pool/devices')
        self.assertEqual(len(devices), 2)
        [self.assertTrue(isinstance(dev, Device)) for dev in devices]

    def test_device_show(self):
        device = cs.devices.get(1234)
        cs.assert_called('GET', '/pool/devices/1234')
        self.assertIsInstance(device, Device)

    def test_device_update(self):
        device = cs.devices.get(1234)
        cs.assert_called('GET', '/pool/devices/1234')
        options = {"management_network_dns": "8.8.8.8",
                   "management_network_netmask": "255.255.255.0",
                   "management_network_ip": "180.10.10.119",
                   "lom_mac": "00:00:00:00",
                   "lom_ip": "0.0.0.0",
                   "management_network_gateway": "180.10.10.1"}
        device = cs.devices.update(device, **options)
        cs.assert_called('PUT', '/pool/devices/1234', body=options)
        self.assertIsInstance(device, dict)

    def test_device_delete(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        options = {"action": "nothing",
                   "lom_password": "stackops",
                   "lom_user": "stackops"}
        cs.devices.delete(device, **options)
        cs.assert_called('POST', '/pool/devices/%s/delete' % device.mac)

    def test_device_power_on(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        options = {"lom_password": "stackops", "lom_user": "stackops"}
        cs.devices.power_on(device, **options)
        cs.assert_called('POST', '/pool/devices/1234/poweron', body=options)

    def test_device_power_off(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        options = {"lom_password": "stackops", "lom_user": "stackops"}
        cs.devices.power_off(device, **options)
        cs.assert_called('POST', '/pool/devices/1234/poweroff', body=options)

    def test_device_reboot(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        options = {"lom_password": "stackops", "lom_user": "stackops"}
        cs.devices.reboot(device, **options)
        cs.assert_called('POST', '/pool/devices/1234/reboot', body=options)

    def test_device_shutdown(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        cs.devices.shutdown(device)
        cs.assert_called('POST', '/pool/devices/1234/shutdown')

    def test_device_soft_reboot(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        cs.devices.soft_reboot(device)
        cs.assert_called('POST', '/pool/devices/1234/soft_reboot')

    def test_device_activate(self):
        device = cs.devices.list()[0]
        cs.assert_called('GET', '/pool/devices')
        options = {"lom_password": "stackops",
                   "lom_user": "stackops",
                   "zone_id": 1}
        cs.devices.activate(device, **options)
        cs.assert_called('POST', '/pool/devices/1234/activate', body=options)
