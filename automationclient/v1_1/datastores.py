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


"""Datastores interface."""

from automationclient import base


class Datastore(base.Resource):
    """Datastores is a pool of resources to be used in the platform
    """

    def __repr__(self):
        return "<Datastore: %s>" % self.name


class DatastoreManager(base.ManagerWithFind):
    """Manage :class:`Datastore` resources."""
    resource_class = Datastore

    def list(self):
        """Get a list of all pool.

        :rtype: list of :class:`Datastore`.
        """

        return self._list('/datastores', 'datastores')

    def get(self, datastore):
        """Get a specific datastore from pool.

        :param datastore: The ID of the :class: `Datastore` to get.
        :rtype: :class:`Datastore`
        """

        return self._get('/datastores/%s' % base.getid(datastore), 'datastore')

    def discovery(self, **kwargs):
        """
        Discovery NFS datastores
        """

        return self._list('/datastores/discovery', response_key='datastores',
                          body=kwargs)

    def space(self, datastore):
        """Get a specific datastore and its space

        :param datastore: The ID of the :class: `Datastore` to get.
        :rtype: :class:`Datastore`
        """
        return self._get('/datastores/%s/space' % base.getid(datastore),
                         'datastore')

    def content(self, datastore):
        """Get a specific datastore and its content

        :param datastore: The ID of the :class: `Datastore` to get.
        :rtype: :class:`Datastore`
        """

        return self._get('/datastores/%s/content' % base.getid(datastore),
                         'datastore')

    def validate(self, **kwargs):
        """
        Prepare a datastore
        """

        return self.api.client.post('/datastores/validate', body=kwargs)

    def prepare(self, **kwargs):
        """
        Prepare a datastore
        """

        return self.api.client.post('/datastores/prepare', body=kwargs)

    def update(self, datastore, **kwargs):
        """
        Update the parameters of the datastore
        """

        if not kwargs:
            return

        return self._update("/datastores/%s" % base.getid(datastore), kwargs)

    def delete(self, datastore):
        """
       Delete an datastore.

       :param datastore: The :class:`Datastore` to delete.
       """
        self._delete("/datastores/%s" % base.getid(datastore))

    def attach(self, datastore, **kwargs):
        """
        Attach a datastore.

        :param datastore: The ID of the :class: `Datastore` to attach.
        :rtype: :class:`Datastore`
        """
        return self._update("/datastores/%s/attach" % base.getid(datastore),
                            kwargs)

    def detach(self, datastore, **kwargs):
        """
        Attach a datastore.

        :param datastore: The ID of the :class: `Datastore` to detach.
        :rtype: :class:`Datastore`
        """
        return self._update("/datastores/%s/detach" % base.getid(datastore),
                            kwargs)
