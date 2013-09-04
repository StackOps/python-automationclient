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


"""Services interface."""

from automationclient import base


class Service(base.Resource):
    """A Service is an extension of Component Class."""
    def __repr__(self):
        return "<Service: %s>" % self.name


class ServiceManager(base.ManagerWithFind):
    """Manage :class:`Service` resources."""
    resource_class = Service

    def list(self, component):
        """Get a list of services by a specific component.

        :param component: The ID (Name of the component) of the :class:
        `Component` to get its services.
        :rtype: :class:`Component`
        """
        return self._list("/components/%s/services" % component.name,
                          "services")
