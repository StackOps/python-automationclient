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

from automationclient import client
from automationclient import shell
from automationclient.v1_1 import shell as shell_v1
from automationclient.tests.v1_1 import fakes
from automationclient.tests import utils


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

    def test_devices_list(self):
        self.run_command('device-list')
        self.assert_called('GET', '/pool/devices')

    def test_device_show(self):
        self.run_command('device-show 1234')
        self.assert_called('GET', '/pool/devices/1234')

    '''def test_device_delete(self):
        self.run_command('device-delete 1234')
        self.assert_called('POST', '/device/1234')'''
