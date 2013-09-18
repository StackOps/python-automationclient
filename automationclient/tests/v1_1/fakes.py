# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2011 OpenStack, LLC

# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from automationclient import client as base_client
from automationclient.tests import fakes
import automationclient.tests.utils as utils
from automationclient.v1_1 import client


class FakeClient(fakes.FakeClient, client.Client):
    def __init__(self, *args, **kwargs):
        client.Client.__init__(self, 'username', 'password',
                               'project_id', 'auth_url',
                               extensions=kwargs.get('extensions'))
        self.client = FakeHTTPClient(**kwargs)

    def get_automation_api_version_from_endpoint(self):
        return self.client.get_automation_api_version_from_endpoint()


def _stub_component(**kwargs):
    component = \
        {
            "_links": None,
            "name": "1234",
            "properties": {
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
                    "glance_password": "stackops",
                    "glance_user": "glance",
                    "cinder_user": "cinder",
                    "quantum_password": "stackops",
                    "keystone_user": "keystone",
                    "automation_user": "automation",
                    "quantum_user": "quantum",
                    "automation_password": "stackops",
                    "keystone_password": "stackops",
                    "cinder_password": "stackops",
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
        }
    component.update(kwargs)
    return component


def _stub_services_by_component():
    services = \
        [
            {
                "_links": None,
                "name": "set_quantum",
                "description": "Creates a new database for quantum and grants "
                               "privileges on it"
            },
            {
                "_links": None,
                "name": "set_keystone",
                "description": "Creates a new database for keystone and "
                               "grants privileges on it"
            },
            {
                "_links": None,
                "name": "teardown",
                "description": "Stop the mysql service"
            },
            {
                "_links": None,
                "name": "set_cinder",
                "description": "Creates a new database for cinder and grants "
                               "privileges on it"
            },
            {
                "_links": None,
                "name": "set_automation",
                "description": "Creates a new database for automation and "
                               "grants privileges on it"
            },
            {
                "_links": None,
                "name": "set_accounting",
                "description": "Creates a new database for accounting and "
                               "grants privileges on it"
            },
            {
                "_links": None,
                "name": "set_nova",
                "description": "Creates a new database for nova and grants "
                               "privileges on it"
            },
            {
                "_links": None,
                "name": "install",
                "description": "Prepares a database and a user password for "
                               "each StackOps schemas"
            },
            {
                "_links": None,
                "name": "set_glance",
                "description": "Creates a new database for glance and grants "
                               "privileges on it"
            },
            {
                "_links": None,
                "name": "validate",
                "description": "Validates main database to operate with it"
            },
            {
                "_links": None,
                "name": "set_portal",
                "description": "Creates a new database for portal and grants "
                               "privileges on it"
            }
        ]

    return services


def _stub_device(**kwargs):
    device = \
        {
            "ip": "180.10.10.123",
            "updated": "None",
            "megaherzs": 0,
            "id": 1,
            "_links": None,
            "management_network_gateway": None,
            "certified": False,
            "memory": 515497984,
            "management_network_ip": "180.10.10.123",
            "status": "INSTALLING",
            "product": "VirtualBox ()",
            "vendor": "innotek GmbH",
            "mac": "1234",
            "threads": 1,
            "connection_data": {
                "username": "stackops",
                "host": "180.10.10.123",
                "ssh_key_file": "/var/lib/stackops-head/etc/nonsecureid_rsa",
                "port": 22
            },
            "lom_mac": None,
            "lom_ip": None,
            "zone_id": None,
            "management_network_dns": None,
            "disk_size": 8589934592,
            "name": "08:00:27:68:1c:62",
            "created": "2013-09-16 13:56:32",
            "management_network_netmask": None,
            "cores": 1,
            "ports": 1
        }
    device.update(kwargs)
    return device


def _stub_architecture(**kwargs):
    architecture = \
        {
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
    return architecture


def _stub_template():
    template = \
        {
            "profile": {
                "name": "",
                "components": [],
                "properties": {}
            }
        }

    return template


class FakeHTTPClient(base_client.HTTPClient):
    def __init__(self, **kwargs):
        self.username = 'username'
        self.password = 'password'
        self.auth_url = 'auth_url'
        self.callstack = []
        self.management_url = 'http://10.0.2.15:8089/v1.1/fake'

    def _cs_request(self, url, method, **kwargs):
        # Check that certain things are called correctly
        if method in ['GET', 'DELETE']:
            assert 'body' not in kwargs
        elif method == 'PUT':
            assert 'body' in kwargs

        # Call the method
        args = urlparse.parse_qsl(urlparse.urlparse(url)[4])
        kwargs.update(args)
        munged_url = url.rsplit('?', 1)[0]
        munged_url = munged_url.strip('/').replace('/', '_').replace('.', '_')
        munged_url = munged_url.replace('-', '_')

        callback = "%s_%s" % (method.lower(), munged_url)

        if not hasattr(self, callback):
            raise AssertionError('Called unknown API method: %s %s, '
                                 'expected fakes method name: %s' %
                                 (method, url, callback))

        # Note the call
        self.callstack.append((method, url, kwargs.get('body', None)))
        status, headers, body = getattr(self, callback)(**kwargs)
        r = utils.TestResponse({
            "status_code": status,
            "text": body,
            "headers": headers,
        })
        return r, body

        if hasattr(status, 'items'):
            return utils.TestResponse(status), body
        else:
            return utils.TestResponse({"status": status}), body

    def get_automation_api_version_from_endpoint(self):
        magic_tuple = urlparse.urlsplit(self.management_url)
        scheme, netloc, path, query, frag = magic_tuple
        return path.lstrip('/').split('/')[0][1:]

    #
    # Component
    #
    def get_components(self, **kw):
        return (200, {}, {"components": [
            {'name': '1234'},
            {'name': 'rabbitmq'}
        ]})

    def get_components_1234(self, **kw):
        return (200, {},
                {'component': _stub_component(name='1234')})

    def get_components_1234_services(self, **kw):
        return (200, {}, {'services': _stub_services_by_component()})

    #
    # Pool (Devices)
    #
    def get_pool_devices(self, **kw):
        return (200, {}, {"devices": [
            {'id': 1234, 'name': 'sample-device1', 'mac': 1234},
            {'id': 5678, 'name': 'sample-device2', 'mac': 5678}
        ]})

    def get_pool_devices_1234(self, **kw):
        return (200, {}, {'device': _stub_device(id='1234')})

    def post_pool_devices_1234_delete(self, **kw):
        return (204, {}, {})

    def put_pool_devices_1234(self, **kw):
        device = _stub_device(id='1234')
        device.update(kw)
        return (200, {}, {'device': device})

    def post_pool_devices_1234_poweron(self, **kw):
        return (204, {}, {})

    def post_pool_devices_1234_poweroff(self, **kw):
        return (204, {}, {})

    def post_pool_devices_1234_reboot(self, **kw):
        return (204, {}, {})

    def post_pool_devices_1234_shutdown(self, **kw):
        return (204, {}, {})

    def post_pool_devices_1234_soft_reboot(self, **kw):
        return (204, {}, {})

    def post_pool_devices_1234_activate(self, **kw):
        device = _stub_device(id='1234')
        return (204, {}, {'device': _stub_device(id='1234')})

    #
    # Architecture
    #
    def get_archs(self, **kw):
        return (200, {}, {"architectures": [
            {'id': 1234, 'name': 'sample-architecture1'},
            {'id': 5678, 'name': 'sample-architecture2'}
        ]})

    def get_archs_1234(self, **kw):
        return (200, {},
                {'architecture': _stub_architecture(id='1234')})

    def post_archs(self, **kw):
        return (201, {},
                {'architecture': _stub_architecture(id='1234')})

    def delete_archs_1234(self, **kw):
        return (204, {}, {})

    def get_archs_1234_get_template(self, **kw):
        _stub_architecture(id='1234')
        return (201, {},
                {'profile': _stub_template()})
