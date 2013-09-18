# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.

# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import fixtures
import os

from automationclient import client
from automationclient import shell
from automationclient.tests.v1_1 import fakes
from automationclient.tests import utils


def _profile(name, key_property, value_property):
    return {
        "profile": {
            "name": "%s" % name,
            "properties": {
                "%s" % key_property: "%s" % value_property
            },
            "_links": None,
            "components": [
                {
                    "name": "mysql",
                    "properties": [
                        {
                            "set_quantum": {
                                "root_pass": "$globals.root.pass",
                                "quantum_password": "stackops",
                                "quantum_user": "quantum"
                            },
                            "set_keystone": {
                                "root_pass": "$globals.root.pass",
                                "keystone_password": "stackops",
                                "keystone_user": "keystone"
                            },
                            "teardown": {},
                            "set_cinder": {
                                "cinder_user": "cinder",
                                "root_pass": "$globals.root.pass",
                                "cinder_password": "stackops"
                            },
                            "set_automation": {
                                "automation_password": "stackops",
                                "root_pass": "$globals.root.pass",
                                "automation_user": "automation"
                            },
                            "set_accounting": {
                                "accounting_user": "activity",
                                "root_pass": "$globals.root.pass",
                                "accounting_password": "stackops"
                            },
                            "set_nova": {
                                "root_pass": "$globals.root.pass",
                                "nova_password": "stackops",
                                "nova_user": "nova"
                            },
                            "install": {
                                "root_pass": "$globals.root.pass",
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
                                "root_pass": "$globals.root.pass",
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
                                "root_pass": "$globals.root.pass",
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


class ShellTest(utils.TestCase):
    FAKE_ENV = {
        'AUTOMATION_USERNAME': 'username',
        'AUTOMATION_PASSWORD': 'password',
        'AUTOMATION_PROJECT_ID': 'project_id',
        'OS_AUTOMATION_API_VERSION': '1.1',
        'AUTOMATION_URL': 'http://no.where',
    }

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        """Run before each test."""
        super(ShellTest, self).setUp()
        for var in self.FAKE_ENV:
            self.useFixture(fixtures.EnvironmentVariable(var,
                                                         self.FAKE_ENV[var]))

        self.shell = shell.StackopsAutomationShell()

        #HACK(bcwaldon): replace this when we start using stubs
        self.old_get_client_class = client.get_client_class
        client.get_client_class = lambda *_: fakes.FakeClient

    def tearDown(self):
        # For some method like test_image_meta_bad_action we are
        # testing a SystemExit to be thrown and object self.shell has
        # no time to get instantatiated which is OK in this case, so
        # we make sure the method is there before launching it.
        if hasattr(self.shell, 'cs'):
            self.shell.cs.clear_callstack()

        #HACK(bcwaldon): replace this when we start using stubs
        client.get_client_class = self.old_get_client_class
        super(ShellTest, self).tearDown()

    def run_command(self, cmd):
        self.shell.main(cmd.split())

    def assert_called(self, method, url, body=None, **kwargs):
        return self.shell.cs.assert_called(method, url, body, **kwargs)

    def assert_called_anytime(self, method, url, body=None):
        return self.shell.cs.assert_called_anytime(method, url, body)

    #
    # Components
    #
    def test_component_list(self):
        self.run_command('component-list')
        self.assert_called('GET', '/components')

    def test_component_show(self):
        self.run_command('component-show 1234')
        self.assert_called('GET', '/components/1234')

    def test_component_services(self):
        self.run_command('component-services 1234')
        self.assert_called('GET', '/components/1234/services')

    #
    # Pool (Devices)
    #
    def test_devices_list(self):
        self.run_command('device-list')
        self.assert_called('GET', '/pool/devices')

    def test_device_show(self):
        self.run_command('device-show 1234')
        self.assert_called('GET', '/pool/devices/1234')

    def test_device_delete(self):
        self.run_command('device-delete 1234')
        self.assert_called('POST', '/pool/devices/1234/delete')

    def test_device_delete_filter_action(self):
        self.run_command('device-delete 1234 --action soft_reboot')
        expected = {'action': 'soft_reboot'}
        self.assert_called('POST', '/pool/devices/1234/delete', body=expected)

    def test_device_delete_filter_user_and_password(self):
        self.run_command('device-delete 1234 '
                         '--lom-user stackops --lom-password stackops')
        expected = {"action": "nothing", "lom_password": "stackops",
                    "lom_user": "stackops"}
        self.assert_called('POST', '/pool/devices/1234/delete', body=expected)

    def test_device_update(self):
        self.run_command('device-update 1234 '
                         '0.0.0.0 '
                         '00:00:00:00 '
                         '180.10.10.119 '
                         '255.255.255.0 '
                         '180.10.10.1 '
                         '8.8.8.8')
        expected = {"management_network_dns": "8.8.8.8",
                    "management_network_netmask": "255.255.255.0",
                    "management_network_ip": "180.10.10.119",
                    "lom_mac": "00:00:00:00",
                    "lom_ip": "0.0.0.0",
                    "management_network_gateway": "180.10.10.1"}
        self.assert_called('PUT', '/pool/devices/1234', body=expected)

    def test_device_power_on(self):
        self.run_command('device-power-on 1234 '
                         'stackops stackops')
        expected = {"lom_password": "stackops", "lom_user": "stackops"}
        self.assert_called('POST', '/pool/devices/1234/poweron', body=expected)

    def test_device_power_off(self):
        self.run_command('device-power-off 1234 '
                         'stackops stackops')
        expected = {"lom_password": "stackops", "lom_user": "stackops"}
        self.assert_called('POST', '/pool/devices/1234/poweroff',
                           body=expected)

    def test_device_reboot(self):
        self.run_command('device-reboot 1234 '
                         'stackops stackops')
        expected = {"lom_password": "stackops", "lom_user": "stackops"}
        self.assert_called('POST', '/pool/devices/1234/reboot', body=expected)

    def test_device_shutdown(self):
        self.run_command('device-shutdown 1234')
        self.assert_called('POST', '/pool/devices/1234/shutdown')

    def test_device_soft_reboot(self):
        self.run_command('device-soft-reboot 1234')
        self.assert_called('POST', '/pool/devices/1234/soft_reboot')

    def test_device_activate(self):
        self.run_command('device-activate 1234 1')
        self.assert_called('POST', '/pool/devices/1234/activate')

    def test_device_activate_filter_user_and_password(self):
        self.run_command('device-activate 1234 1 '
                         '--lom-user stackops --lom-password stackops')
        expected = {"lom_password": "stackops",
                    "lom_user": "stackops",
                    "zone_id": 1}
        self.assert_called('POST', '/pool/devices/1234/activate',
                           body=expected)

    #
    # Architecture
    #
    def test_architecture_list(self):
        self.run_command('architecture-list')
        self.assert_called('GET', '/archs')

    def test_architecture_show(self):
        self.run_command('architecture-show 1234')
        self.assert_called('GET', '/archs/1234')

    def test_architecture_create(self):
        file = os.path.join(os.getcwd(),
                            "automationclient/tests/v1_1/"
                            "fake_files/fake_architecture_create.arc")
        self.run_command('architecture-create %s' % file)
        expected = {
            "architecture": {
                "_links": None,
                "id": 1234,
                "roles": [
                    {
                        "steps": [
                            {
                                "1": [
                                    "mysql"
                                ]
                            },
                            {
                                "2": [
                                    "rabbitmq"
                                ]
                            }
                        ],
                        "name": "controller"
                    }
                ],
                "name": "sample-architecture1"
            }
        }
        self.assert_called('POST', '/archs', body=expected)

    def test_architecture_delete(self):
        self.run_command('architecture-delete 1234')
        self.assert_called('DELETE', '/archs/1234')

    def test_architecture_template(self):
        self.run_command('architecture-template 1234')
        self.assert_called('GET', '/archs/1234/get_template')

    #
    # Profiles
    #
    def test_profile_list(self):
        self.run_command('profile-list 1234')
        self.assert_called('GET', '/archs/1234/profiles')

    def test_profile_show(self):
        self.run_command('profile-show 1234 1234')
        self.assert_called('GET', '/archs/1234/profiles/1234')

    def test_profile_create(self):
        file = os.path.join(os.getcwd(),
                            "automationclient/tests/v1_1/"
                            "fake_files/fake_profile_create.json")
        self.run_command('profile-create 1234 %s' % file)
        expected = _profile("profile_create", "property_key_create",
                            "property_value_create")
        self.assert_called('POST', '/archs/1234/profiles', body=expected)

    def test_profile_update(self):
        file = os.path.join(os.getcwd(),
                            "automationclient/tests/v1_1/"
                            "fake_files/fake_profile_update.json")
        self.run_command('profile-update 1234 1234 %s' % file)
        expected = _profile("profile_update", "property_key_update",
                            "property_value_update")
        self.assert_called('PUT', '/archs/1234/profiles/1234', body=expected)

    def test_profile_delete(self):
        self.run_command('profile-delete 1234 1234')
        self.assert_called('DELETE', '/archs/1234/profiles/1234')

    def test_profile_json(self):
        self.run_command('profile-json 1234 1234')
        self.assert_called('GET', '/archs/1234/profiles/1234')

    def test_profile_property_create(self):
        self.run_command('profile-property-create '
                         '1234 1234 new_property_key new_property_value')
        expected = _profile(None, "new_property_key", "new_property_value")
        #TODO(jvalderrama) Check options as body expected
        self.assert_called('PUT', '/archs/1234/profiles/1234')

    def test_profile_property_update(self):
        self.run_command('profile-property-update '
                         '1234 1234 property_key property_value')
        expected = _profile(None, "property_key", "property_value")
        #TODO(jvalderrama) Check options as body expected
        self.assert_called('PUT', '/archs/1234/profiles/1234')

    def test_profile_property_delete(self):
        self.run_command('profile-property-delete '
                         '1234 1234 property_key')
        expected = _profile(None, "property_key", "property_value")
        #TODO(jvalderrama) Check options as body expected
        self.assert_called('PUT', '/archs/1234/profiles/1234')
