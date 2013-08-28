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
def do_node_list(cs, args):
    """List all the nodes in the pool."""
    nodes = cs.nodes.list()
    utils.print_list(nodes, ['id', 'name', 'mac', 'status', 'connection_data'])


@utils.arg('node', metavar='<mac>', help='Mac of the node.')
@utils.service_type('automation')
def do_node_show(cs, args):
    """Show details about a node."""
    node = _find_node(cs, args.node)
    utils.print_dict(node._info)


@utils.arg('node', metavar='<node-id>', help='ID of the node.')
@utils.arg('lom_ip', metavar='<lom-ip>',
           default=None,
           help='New lom_ip for the node.')
@utils.arg('lom_mac', metavar='<lom-mac>',
           default=None,
           help='New lom_mac for the node')
@utils.service_type('automation')
def do_node_update(cs, args):
    """Update a node."""
    kwargs = {}
    if args.lomp_ip is not None:
        kwargs['lom_ip'] = args.lomp_ip
    if args.lom_mac is not None:
        kwargs['lom_mac'] = args.lom_mac
    _find_node(cs, args.node).update(**kwargs)


@utils.arg('node', metavar='<node>',
           help='ID of the node to delete.')
@utils.service_type('automation')
def do_node_delete(cs, args):
    """Remove a specific node from pool."""
    node = _find_node(cs, args.node)
    node.delete()


@utils.arg('node', metavar='<node>',
           help='ID of the node to activate.')
@utils.service_type('automation')
def do_node_activate(cs, args):
    """Activate a specific node in the pool."""
    node = _find_node(cs, args.node)
    cs.nodes.activate()


@utils.arg('node', metavar='<mac>',
           help='Mac of the node to power on.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_node_power_on(cs, args):
    """Power on a specific node in the pool."""
    kwargs = {'lom_user': args.lomp_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.node)
    cs.nodes.poweron(node, **kwargs)


@utils.arg('node', metavar='<node-mac>',
           help='Mac of the node to power off.')
@utils.arg('lom-user', metavar='<lom-user>',
           help='lom-user credential.')
@utils.arg('lom-password', metavar='<lom-password>',
           help='lom-password for lom_user credential')
@utils.service_type('automation')
def do_node_power_off(cs, args):
    """Power off a specific node in the pool."""
    kwargs = {'lom_user': args.lomp_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.node)
    cs.nodes.poweroff(node, **kwargs)


@utils.arg('node', metavar='<mac>',
           help='Mac of the node to reboot.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_node_reboot(cs, args):
    """Reboot a specific node in the pool."""
    kwargs = {'lom_user': args.lomp_user, 'lom_password': args.lom_password}
    node = _find_node(cs, args.node)
    cs.nodes.reboot(node, **kwargs)


@utils.arg('node', metavar='<mac>',
           help='Mac of the node to shutdown.')
@utils.service_type('automation')
def do_node_shutdown(cs, args):
    """Shutdown a specific node in the pool."""
    node = _find_node(cs, args.node)
    node.shutdown()
    cs.nodes.shutdown(node)

@utils.arg('node', metavar='<mac>',
           help='Mac of the node to soft reboot.')
@utils.service_type('automation')
def do_node_soft_reboot(cs, args):
    """Soft reboot a specific node in the pool."""
    node = _find_node(cs, args.node)
    cs.node.soft_reboot(node)


def do_endpoints(cs, args):
    """Discover endpoints that get returned from the authenticate services."""
    catalog = cs.client.service_catalog.catalog
    for e in catalog['access']['serviceCatalog']:
        utils.print_dict(e['endpoints'][0], e['name'])
