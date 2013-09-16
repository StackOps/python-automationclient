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


def _stub_device(**kwargs):
    device = {
        "ip": "180.10.10.123",
        "updated": "None",
        "megaherzs": 0,
        "id": 1,
        "management_network_gateway": None,
        "certified": False,
        "memory": 515497984,
        "management_network_ip": "180.10.10.123",
        "status": "INSTALLING",
        "product": "VirtualBox ()",
        "vendor": "innotek GmbH",
        "mac": "08:00:27:68:1c:62",
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
    # Pool (Devices)
    #
    def get_pool_devices(self, **kw):
        return (200, {}, {"nodes": [
            {'id': 1234, 'name': 'sample-device1'},
            {'id': 5678, 'name': 'sample-device2'}
        ]})

    def get_pool_devices_1234(self, **kw):
        return (200, {}, {'node': _stub_device(id='1234')})
