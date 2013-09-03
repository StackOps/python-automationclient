# Copyright 2010 Jacob Kaplan-Moss

# Copyright 2011 OpenStack LLC.
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

from __future__ import print_function

import argparse
import os
import sys
import time
import logging
import json

from automationclient import utils


def _poll_for_status(poll_fn, obj_id, action, final_ok_states,
                     poll_period=5, show_progress=True):
    """Block while an action is being performed, periodically printing
    progress.
    """
    def print_progress(progress):
        if show_progress:
            msg = ('\rInstance %(action)s... %(progress)s%% complete'
                   % dict(action=action, progress=progress))
        else:
            msg = '\rInstance %(action)s...' % dict(action=action)

        sys.stdout.write(msg)
        sys.stdout.flush()

    print()
    while True:
        obj = poll_fn(obj_id)
        status = obj.status.lower()
        progress = getattr(obj, 'progress', None) or 0
        if status in final_ok_states:
            print_progress(100)
            print("\nFinished")
            break
        elif status == "error":
            print("\nError %(action)s instance" % {'action': action})
            break
        else:
            print_progress(progress)
            time.sleep(poll_period)


def _find_component(cs, component):
    """Get a component by ID."""
    return utils.find_resource(cs.components, component)


def _find_architecture(cs, architecture):
    """Get a architecture by ID."""
    return utils.find_resource(cs.architectures, architecture)


def _find_node(cs, node):
    """Get a node by ID."""
    return utils.find_resource(cs.nodes, node)


@utils.service_type('automation')
def do_component_list(cs, args):
    """List all the components that are available on automation."""
    components = cs.components.list()
    utils.print_list(components, ['name', 'properties'])


@utils.arg('component', metavar='<component-id>', help='ID of the component.')
@utils.service_type('automation')
def do_component_show(cs, args):
    """Show details about a component."""
    component = _find_component(cs, args.component)
    utils.print_dict(component._info)


@utils.arg('component', metavar='<component-id>', help='ID of the component.')
@utils.service_type('automation')
def do_component_services(cs, args):
    """List all the services by a component."""
    component = cs.components.get_services(args.component)
    utils.print_list(component, ['Name', 'description'])


@utils.service_type('automation')
def do_architecture_list(cs, args):
    """List all the architectures that are available on automation."""
    architectures = cs.architectures.list()
    utils.print_list(architectures, ['id', 'name', 'profiles', '_links'])


@utils.arg('architecture', metavar='<architecture-id>',
           help='ID of the architecture.')
@utils.service_type('automation')
def do_architecture_show(cs, args):
    """Show details about an architecture."""
    architecture = _find_architecture(cs, args.architecture)
    utils.print_dict(architecture._info)


@utils.arg('architecture', metavar='<architecture-file>',
           help='File with extension *.archs describing the '
                'new architecture to create.')
@utils.service_type('automation')
def do_architecture_create(cs, args):
    """Add a new architecture."""
    architecture = cs.architectures.create(args.architecture)
    utils.print_list(architecture, ['_links', 'name', 'profiles', 'id',
                                    'profiles'])


@utils.arg('architecture', metavar='<architecture>',
           help='ID of the architecture to delete.')
@utils.service_type('automation')
def do_architecture_delete(cs, args):
    """Remove a specific architecture."""
    architecture = _find_architecture(cs, args.architecture)
    architecture.delete()


@utils.service_type('automation')
def do_device_list(cs, args):
    """List all the devices in the pool."""
    nodes = cs.nodes.list()
    utils.print_list(nodes, ['id', 'name', 'mac', 'status', 'connection_data'])


@utils.arg('mac', metavar='<mac>', help='Mac of the node.')
@utils.service_type('automation')
def do_device_show(cs, args):
    """Show details about a device."""
    node = _find_node(cs, args.mac)
    keys = ['_links', 'hardware_profile']
    final_dict = utils.remove_values_from_manager_dict(node, keys)
    final_dict = utils.check_json_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('mac', metavar='<mac>', help='MAC of the node.')
@utils.arg('lom_ip', metavar='<lom-ip>',
           default=None,
           help='New lom_ip for the node.')
@utils.arg('lom_mac', metavar='<lom-mac>',
           default=None,
           help='New lom_mac for the node')
@utils.service_type('automation')
def do_device_update(cs, args):
    """Update a device."""

    options = {
        'lom_ip': args.lom_ip,
        'lom_mac': args.lom_mac
    }

    node = _find_node(cs, args.mac)
    cs.nodes.update(node, **options)
    do_device_show(cs, args)


@utils.arg('mac', metavar='<mac>',
           help='MAC of the node to delete.')
@utils.arg('--action', metavar='<action>', default='nothing',
           help='Action to perform after node is deleted')
@utils.arg('--lom-user', metavar='<lom-user>',
           help='Out-of-band user')
@utils.arg('--lom-password', metavar='<lom-password>',
           help='Out-of-Band user password')
@utils.service_type('automation')
def do_device_delete(cs, args):
    """Remove a specific device from pool."""

    options = {'action': args.action}

    if args.lom_user is not None:
        options['lom_user'] = args.lom_user

    if args.lom_password is not None:
        options['lom_password'] = args.lom_password

    node = _find_node(cs, args.mac)
    cs.nodes.delete(node, **options)


@utils.arg('mac', metavar='<mac>',
           help='ID of the node to activate.')
@utils.arg('zone_id', metavar='<zone-id>',
           type=int,
           help='ID of the zone to activate the node')
@utils.service_type('automation')
def do_device_activate(cs, args):
    """Activate a specific device in the pool."""
    kwargs = {'zone_id': args.zone_id}
    node = _find_node(cs, args.mac)
    cs.nodes.activate(node, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the node to power on.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_power_on(cs, args):
    """Power on a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.mac)
    cs.nodes.power_on(node, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the node to power off.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_power_off(cs, args):
    """Power off a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.mac)
    cs.nodes.power_off(node, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the node to reboot.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_reboot(cs, args):
    """Reboot a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.mac)
    cs.nodes.reboot(node, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the node to shutdown.')
@utils.service_type('automation')
def do_device_shutdown(cs, args):
    """Shutdown a specific device in the pool."""
    node = _find_node(cs, args.mac)
    cs.nodes.shutdown(node)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the node to soft reboot.')
@utils.service_type('automation')
def do_device_soft_reboot(cs, args):
    """Soft reboot a specific device in the pool."""
    node = _find_node(cs, args.mac)
    cs.nodes.soft_reboot(node)


def do_endpoints(cs, args):
    """Discover endpoints that get returned from the authenticate services."""
    catalog = cs.client.service_catalog.catalog
    for e in catalog['access']['serviceCatalog']:
        utils.print_dict(e['endpoints'][0], e['name'])
