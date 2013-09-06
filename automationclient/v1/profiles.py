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


"""Profiles interface."""

from automationclient import base


class Profile(base.Resource):
    """A Profile is an extension of an Architecture class."""

    def __repr__(self):
        return "<Profile: %s>" % self.name


class ProfileManager(base.ManagerWithFind):
    """Manage :class:`Profile` resources."""
    resource_class = Profile

    def list(self, architecture):
        """Get a list of profile by a specific architecture.

        :param architecture: The ID of the :class: `Architecture` to get
        its services.
        :rtype: :class:`Architecture`
        """
        return self._list("/archs/%s/profiles" % architecture.id,
                          "profiles")

    def get(self, architecture, profile):
        """Get a specific profile by architecture.

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`

        :param profile: The ID of the :class: `Profile` to get.
        :rtype: :class:`Profile`
        """
        return self._get("/archs/%s/profiles/%s" % (base.getid(architecture),
                                                    profile),
                         "profile")

    def create(self, architecture, profile):
        """
        Create a profile.

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`

        :param profile: Profile JSON format define
        """

        body = profile

        return self._create("/archs/%s/profiles" % (base.getid(architecture)),
                            body, 'profile')

    def update(self, architecture, profile, profile_file):
        """
        Update the name, components

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`

        :param profile: The ID of the :class: `Profile` to update.
        :rtype: :class:`Profile`

        :param profile: Profile JSON format define with updates
        """
        if not profile_file:
            return

        self._update("/archs/%s/profiles/%s" % (base.getid(architecture),
                                                base.getid(profile)),
                     profile_file)

    def delete(self, architecture, profile):
        """
        Delete a profile.

        :param architecture: The ID of the :class: `Architecture` to get.
        :rtype: :class:`Architecture`

        :param profile: The ID of the :class: `Profile` to delete.
        :rtype: :class:`Profile`
        """

        self._delete("/archs/%s/profiles/%s" % (base.getid(architecture),
                                                base.getid(profile)))

    #TODO: Use /archs/<arch_id>/template
    def template(self, architecture):
        """Get a specific template (Profile) by architecture.

        :param architecture: The ID of the :class: `Architecture` to get its
        template.
        :rtype: :class:`Architecture`
        """
        return self._get("/archs/%s/get_template" % base.getid(architecture),
                         "profile")
