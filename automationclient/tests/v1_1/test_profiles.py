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


def _profile():
    return {
        "profile": {
            "name": "fake_profile",
            "properties": {
                "fake_property_key": "fake_property_value"
            },
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


class ProfilesTest(utils.TestCase):

    def test_profile_list(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profiles = cs.profiles.list(architecture)
        cs.assert_called('GET', '/archs/1234/profiles')
        self.assertEqual(len(profiles), 2)
        [self.assertTrue(isinstance(pro, Profile))
         for pro in profiles]

    def test_profile_show(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)

    def test_profile_create(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        options = _profile()
        profile = cs.profiles.create(architecture, options)
        cs.assert_called('POST', '/archs/1234/profiles', body=options)
        self.assertIsInstance(profile, Profile)

    def test_profile_update(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        options = _profile()
        profile = cs.profiles.update(architecture, profile, options)
        cs.assert_called('PUT', '/archs/1234/profiles/1234', body=options)
        self.assertIsInstance(profile, dict)

    def test_profile_delete(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        cs.profiles.delete(architecture, profile)
        cs.assert_called('DELETE', '/archs/1234/profiles/1234')

    def test_profile_json(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        json_profile = utils.from_manager_to_dict(profile)
        self.assertIsInstance(json_profile, dict)

    def test_profile_property_create(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        #TODO(jvalderrama) Check options as body expected
        #options = _profile()
        profile = cs.profiles.property_create(architecture,
                                              profile,
                                              'new_fake_property_key',
                                              'new_fake_property_key_value')
        cs.assert_called('PUT', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, dict)

    def test_profile_property_update(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        #TODO(jvalderrama) Check options as body expected
        #options = _profile()
        profile = cs.profiles.property_update(architecture,
                                              profile,
                                              'fake_property_key',
                                              'fake_property_value')
        cs.assert_called('PUT', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, dict)

    def test_profile_property_delete(self):
        architecture = cs.architectures.get(1234)
        cs.assert_called('GET', '/archs/1234')
        self.assertIsInstance(architecture, Architecture)
        profile = cs.profiles.get(architecture, 1234)
        cs.assert_called('GET', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, Profile)
        #TODO(jvalderrama) Check options as body expected
        #options = _profile()
        profile = cs.profiles.property_delete(architecture,
                                              profile,
                                              'fake_property_key')
        cs.assert_called('PUT', '/archs/1234/profiles/1234')
        self.assertIsInstance(profile, dict)
