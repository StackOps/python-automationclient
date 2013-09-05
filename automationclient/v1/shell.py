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

from __future__ import print_function


import sys
import time
import ast

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


def _find_device(cs, device):
    """Get a device by ID."""
    return utils.find_resource(cs.devices, device)


@utils.service_type('automation')
def do_device_list(cs, args):
    """List all the devices in the pool."""
    devices = cs.devices.list()
    utils.print_list(devices, ['id', 'name', 'mac', 'status',
                               'connection_data'])


@utils.arg('mac', metavar='<mac>', help='Mac of the device.')
@utils.service_type('automation')
def do_device_show(cs, args):
    """Show details about a device."""
    device = _find_device(cs, args.mac)
    keys = ['_links', 'hardware_profile']
    final_dict = utils.remove_values_from_manager_dict(device, keys)
    final_dict = utils.check_json_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('mac', metavar='<mac>', help='MAC of the device.')
@utils.arg('lom_ip', metavar='<lom-ip>',
           default=None,
           help='New lom_ip for the device.')
@utils.arg('lom_mac', metavar='<lom-mac>',
           default=None,
           help='New lom_mac for the device')
@utils.arg('management_network_ip', metavar='<management-network-ip>',
           default=None,
           help='New IP for management network of the device')
@utils.arg('management_network_netmask', metavar='<management-network-netmask>',
           default=None,
           help='New netmask for the management network of the device')
@utils.arg('management_network_gateway', metavar='<management-network-gateway>',
           default=None,
           help='New gateway for the management network of the device')
@utils.arg('management_network_dns', metavar='<management-network-dns>',
           default=None,
           help='New DNS for the management network of the device')

@utils.service_type('automation')
def do_device_update(cs, args):
    """Update a device."""

    options = {
        'lom_ip': args.lom_ip,
        'lom_mac': args.lom_mac,
        'management_network_ip':args.management_network_ip,
        'management_network_netmask': args.management_network_netmask,
        'management_network_gateway': args.management_network_gateway,
        'management_network_dns' : args.management_network_dns
    }

    device = _find_device(cs, args.mac)
    cs.devices.update(device, **options)
    do_device_show(cs, args)


@utils.arg('mac', metavar='<mac>',
           help='MAC of the device to delete.')
@utils.arg('--action', metavar='<action>', default='nothing',
           help='Action to perform after device is deleted')
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

    device = _find_device(cs, args.mac)
    cs.devices.delete(device, **options)


@utils.arg('mac', metavar='<mac>',
           help='ID of the device to activate.')
@utils.arg('zone_id', metavar='<zone-id>',
           type=int,
           help='ID of the zone to activate the device')
@utils.service_type('automation')
def do_device_activate(cs, args):
    """Activate a specific device in the pool."""
    kwargs = {'zone_id': args.zone_id}
    device = _find_device(cs, args.mac)
    cs.devices.activate(device, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the device to power on.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_power_on(cs, args):
    """Power on a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    device = _find_device(cs, args.mac)
    cs.devices.power_on(device, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the device to power off.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_power_off(cs, args):
    """Power off a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    device = _find_device(cs, args.mac)
    cs.devices.power_off(device, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the device to reboot.')
@utils.arg('lom_user', metavar='<lom-user>',
           help='lom_user credential.')
@utils.arg('lom_password', metavar='<lom-password>',
           help='lom_password for lom_user credential')
@utils.service_type('automation')
def do_device_reboot(cs, args):
    """Reboot a specific device in the pool."""
    kwargs = {'lom_user': args.lom_user, 'lom_password': args.lom_password}
    device = _find_device(cs, args.mac)
    cs.devices.reboot(device, **kwargs)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the device to shutdown.')
@utils.service_type('automation')
def do_device_shutdown(cs, args):
    """Shutdown a specific device in the pool."""
    device = _find_device(cs, args.mac)
    cs.devices.shutdown(device)


@utils.arg('mac', metavar='<mac>',
           help='Mac of the device to soft reboot.')
@utils.service_type('automation')
def do_device_soft_reboot(cs, args):
    """Soft reboot a specific device in the pool."""
    device = _find_device(cs, args.mac)
    cs.devices.soft_reboot(device)


@utils.service_type('automation')
def do_component_list(cs, args):
    """List all the components that are available on automation."""
    components = cs.components.list()
    utils.print_list(components, ['name', 'properties'], pretty='pretty')


@utils.arg('component', metavar='<component-id>', help='ID of the component.')
@utils.service_type('automation')
def do_component_show(cs, args):
    """Show details about a component."""
    component = _find_component(cs, args.component)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(component, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('component', metavar='<component-id>', help='ID of the component.')
@utils.service_type('automation')
def do_component_services(cs, args):
    """List all the services by a component."""
    component = _find_component(cs, args.component)
    services = cs.services.list(component)
    utils.print_list(services, ['Name', 'description', '_links'])


@utils.service_type('automation')
def do_architecture_list(cs, args):
    """List all the architectures that are available on automation."""
    architectures = cs.architectures.list()
    utils.print_list(architectures, ['id', 'name', 'profiles'])


@utils.arg('architecture', metavar='<architecture-id>',
           help='ID of the architecture.')
@utils.service_type('automation')
def do_architecture_show(cs, args):
    """Show details about an architecture."""
    architecture = _find_architecture(cs, args.architecture)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(architecture, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture-file>',
           help='File with extension *.arc describing the '
                'new architecture to create.')
@utils.service_type('automation')
def do_architecture_create(cs, args):
    """Add a new architecture.
    :param cs:
    :param args:
    """
    contents = open(args.architecture)
    lines = contents.readlines()
    architecture_file = ''.join([line.strip() for line in lines])
    architecture_file = ast.literal_eval(architecture_file)
    architecture = cs.architectures.create(architecture_file)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(architecture, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture>',
           help='ID of the architecture to delete.')
@utils.service_type('automation')
def do_architecture_delete(cs, args):
    """Remove a specific architecture."""
    architecture = _find_architecture(cs, args.architecture)
    cs.architectures.delete(architecture)


@utils.arg('architecture', metavar='<architecture>',
           help='ID of the architecture to get its template.')
@utils.service_type('automation')
def do_architecture_template(cs, args):
    """Get template from a specific architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = cs.profiles.template(architecture)
    final_dict = utils.check_json_pretty_value_for_dict(profile._info)
    utils.print_dict(final_dict)


def do_endpoints(cs, args):
    """Discover endpoints that get returned from the authenticate services."""
    catalog = cs.client.service_catalog.catalog
    for e in catalog['access']['serviceCatalog']:
        utils.print_dict(e['endpoints'][0], e['name'])
