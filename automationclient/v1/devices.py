# Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Device interface."""

from automationclient import base


class Device(base.Resource):
    """Device is a device in the pool
    """
    def __repr__(self):
        return "<Device: %s>" % self.name


class DeviceManager(base.ManagerWithFind):
    """Manage :class:`Device` resources."""
    resource_class = Device

    def list(self):
        """Get a list of all pool.

        :rtype: list of :class:`Device`.
        """
        return self._list("/pool/devices", "nodes")

    def get(self, device):
        """Get a specific device from pool.

        :param device: The ID of the :class: `Device` to get.
        :rtype: :class:`Device`
        """
        return self._get("/pool/devices/%s" % base.getid(device), "node")

    def activate(self, device, **kwargs):
        """
        Activate a device.

        :param device: Device to activate
        """
        return self._action('activate', device, **kwargs)

    def power_on(self, device, **kwargs):
        """
        Power on a device.

        :param device: Device to power on
        """

        return self._action('poweron', device, **kwargs)

    def power_off(self, device, **kwargs):
        """
        Power off a device.

        :param device: Device to power off
        """

        return self._action('poweroff', device, **kwargs)

    def reboot(self, device, **kwargs):
        """
        Reboot a device.

        :param device: Device to reboot
        """

        return self._action('reboot', device, **kwargs)

    def shutdown(self, device):
        """
        Shutdown a device.

        :param device: Device to shutdown
        """

        return self._action('shutdown', device)

    def soft_reboot(self, device):
        """
        Soft reboot a device.

        :param device: Device to soft reboot
        """

        return self._action('soft_reboot', device)

    def update(self, device, **kwargs):
        """
        Update the lom_ip or lom_mac for a device.

        :param device: The :class:`Device` to update.
        """
        if not kwargs:
            return

        self._update("/pool/devices/%s" % device.mac, kwargs)

    def delete(self, device, **kwargs):
        """
        Delete a device in the pool.

        :param device: The :class:`Device` to delete.
        """

        self._action('delete', device, **kwargs)

    def _action(self, url, device, **kwargs):
        """
        Perform a device action.
        """

        url = '/pool/devices/%s/%s' % (device.mac, url)
        return self.api.client.post(url, body=kwargs)
