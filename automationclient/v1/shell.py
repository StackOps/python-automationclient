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
import os
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


def _validate_extension_file(file, extension):
    ext = os.path.splitext(file)[-1].lower()
    if ext == ".%s" % extension:
        pass
    else:
        print("\nError: The file %s must have .%s extension"
              % (file, extension))
        raise SystemExit


def _find_device(cs, device):
    """Get a device by ID."""
    return utils.find_resource(cs.devices, device)


def _find_component(cs, component):
    """Get a component by ID."""
    return utils.find_resource(cs.components, component)


def _find_architecture(cs, architecture):
    """Get a architecture by ID."""
    return utils.find_resource(cs.architectures, architecture)


def _find_profile(cs, architecture, profile):
    """Get a profile by architecture."""
    architecture = _find_architecture(cs, architecture)
    return cs.profiles.get(architecture, profile)


def _find_zone(cs, zone):
    """Get a zone by ID."""
    return utils.find_resource(cs.zones, zone)


def _find_role(cs, zone, role):
    """Get a role by zone."""
    zone = _find_zone(cs, zone)
    return cs.roles.get(zone, role)


def _find_node(cs, zone, node):
    """Get a node by zone."""
    zone = _find_zone(cs, zone)
    return cs.nodes.get(zone, node)


@utils.service_type('automation')
def do_device_list(cs, args):
    """List all the devices in the pool."""
    devices = cs.devices.list()
    utils.print_list(devices, ['id', 'name', 'mac', 'status',
                               'connection_data'], pretty='pretty')


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
@utils.arg('management_network_netmask',
           metavar='<management-network-netmask>',
           default=None,
           help='New netmask for the management network of the device')
@utils.arg('management_network_gateway',
           metavar='<management-network-gateway>',
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
        'management_network_ip': args.management_network_ip,
        'management_network_netmask': args.management_network_netmask,
        'management_network_gateway': args.management_network_gateway,
        'management_network_dns': args.management_network_dns
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
           help='Mac of the device to activate.')
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


@utils.arg('component', metavar='<component>', help='Name of the component.')
@utils.service_type('automation')
def do_component_show(cs, args):
    """Show details about a component."""
    component = _find_component(cs, args.component)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(component, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('component', metavar='<component>', help='Name of the component.')
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
    utils.print_list(architectures, ['id', 'name'])


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
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
    _validate_extension_file(args.architecture, 'arc')

    with open(args.architecture) as f:
        architecture = cs.architectures.create(json.load(f))

    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(architecture, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to delete.')
@utils.service_type('automation')
def do_architecture_delete(cs, args):
    """Remove a specific architecture."""
    architecture = _find_architecture(cs, args.architecture)
    cs.architectures.delete(architecture)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to get its template.')
@utils.service_type('automation')
def do_architecture_template(cs, args):
    """Get template from a specific architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = cs.profiles.template(architecture)
    print (json.dumps({'profile': profile._info}))


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture.')
@utils.service_type('automation')
def do_profile_list(cs, args):
    """List all the profiles by architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profiles = cs.profiles.list(architecture)
    utils.print_list(profiles, ['id', 'name', 'components'], pretty='pretty')


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture.')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile.')
@utils.service_type('automation')
def do_profile_show(cs, args):
    """Show details about a profile by architecture."""
    profile = _find_profile(cs, args.architecture, args.profile)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(profile, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to create a new profile on it')
@utils.arg('profile', metavar='<profile-file>',
           help='File with extension *.json describing the '
                'new profile to create.')
@utils.service_type('automation')
def do_profile_create(cs, args):
    """Add a new profile by architecture."""
    _validate_extension_file(args.profile, 'json')

    architecture = _find_architecture(cs, args.architecture)

    with open(args.profile) as f:
        profile = cs.profiles.create(architecture, json.load(f))

    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(profile, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture.')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile to update.')
@utils.arg('profile_file', metavar='<profile-file>',
           help='File with extension *.json describing the '
                'profile to modify.')
@utils.service_type('automation')
def do_profile_update(cs, args):
    """Update a profile by architecture."""
    _validate_extension_file(args.profile_file, 'json')

    architecture = _find_architecture(cs, args.architecture)
    profile = _find_profile(cs, args.architecture, args.profile)

    with open(args.profile_file) as f:
        cs.profiles.update(architecture, profile, json.load(f))

    do_profile_show(cs, args)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to get an specific profile to delete.')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile to delete.')
@utils.service_type('automation')
def do_profile_delete(cs, args):
    """Remove a specific profile by architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = _find_profile(cs, args.architecture, args.profile)
    cs.profiles.delete(architecture, profile)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to create a new '
                'property profile on it')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile to create a property.')
@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.arg('property_value', metavar='<property-value>',
           help='The value property')
@utils.service_type('automation')
def do_profile_property_create(cs, args):
    """Create a profile property by architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = _find_profile(cs, args.architecture, args.profile)
    property_key = args.property_key
    property_value = args.property_value
    cs.profiles.property_create(architecture, profile, property_key,
                                property_value)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to update a new property '
                'profile on it')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile to update a property.')
@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.arg('property_value', metavar='<property-value>',
           help='The value property')
@utils.service_type('automation')
def do_profile_property_update(cs, args):
    """Update a profile property by architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = _find_profile(cs, args.architecture, args.profile)
    property_key = args.property_key
    property_value = args.property_value
    cs.profiles.property_update(architecture, profile, property_key,
                                property_value)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to delete a new property '
                'profile on it')
@utils.arg('profile', metavar='<profile-id>',
           type=int,
           help='ID of the profile to delete a property.')
@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.arg('property_value', metavar='<property-value>',
           help='The value property')
@utils.service_type('automation')
def do_profile_property_delete(cs, args):
    """Delete a profile property by architecture."""
    architecture = _find_architecture(cs, args.architecture)
    profile = _find_profile(cs, args.architecture, args.profile)
    property_key = args.property_key
    property_value = args.property_value
    cs.profiles.property_delete(architecture, profile, property_key,
                                property_value)


@utils.service_type('automation')
def do_global_property_list(cs, args):
    """List all the properties that are available on automation."""
    properties = cs.properties.list()
    utils.print_dict(properties)


@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.arg('property_value', metavar='<property-value>',
           help='The value property')
@utils.service_type('automation')
def do_global_property_create(cs, args):
    """Add a new property.
    :param cs:
    :param args:
    """
    property_key = args.property_key
    property_value = args.property_value
    cs.properties.create(property_key, property_value)


@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.arg('property_value', metavar='<property-value>',
           help='The value property')
@utils.service_type('automation')
def do_global_property_update(cs, args):
    """Updates a property.
    :param cs:
    :param args:
    """
    property_key = args.property_key
    property_value = args.property_value
    cs.properties.update(property_key, property_value)
    do_global_property_list(cs, args)


@utils.arg('property_key', metavar='<property-key>',
           help='The key property.')
@utils.service_type('automation')
def do_global_property_delete(cs, args):
    """Delete a property.
    :param cs:
    :param args:
    """
    property_key = args.property_key
    cs.properties.delete(property_key)


@utils.service_type('automation')
def do_zone_list(cs, args):
    """List all the zones."""
    zones = cs.zones.list()
    utils.print_list(zones, ['id', 'name'])


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.service_type('automation')
def do_zone_show(cs, args):
    """Show details about a zone."""
    zone = _find_zone(cs, args.zone)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(zone, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('architecture', metavar='<architecture-id>',
           type=int,
           help='ID of the architecture to create a new zone based on it')
@utils.arg('zone', metavar='<zone-file>',
           help='File with extension *.json describing the '
                'new zone to create.')
@utils.service_type('automation')
def do_zone_create(cs, args):
    """Add a new zone by architecture."""
    _validate_extension_file(args.zone, 'json')

    architecture = _find_architecture(cs, args.architecture)

    with open(args.zone) as f:
        zone = cs.zones.create(architecture, json.load(f))

    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(zone, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone to delete.')
@utils.service_type('automation')
def do_zone_delete(cs, args):
    """Remove a specific zone."""
    zone = _find_zone(cs, args.zone)
    cs.zones.delete(zone)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.service_type('automation')
def do_zone_tasks(cs, args):
    """List all tasks by zone."""
    zone = _find_zone(cs, args.zone)
    tasks = cs.tasks.list(zone)
    utils.print_list(tasks, ['Name', 'description', '_links'])


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.service_type('automation')
def do_node_list(cs, args):
    """List all activate nodes in a zone."""
    zone = _find_zone(cs, args.zone)
    nodes = cs.nodes.list(zone)
    utils.print_list(nodes, ['id', 'name'])


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.service_type('automation')
def do_node_show(cs, args):
    """Show details about a node in a zone."""
    node = _find_node(cs, args.zone, args.node)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(node, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.service_type('automation')
def do_node_task(cs, args):
    """Show tasks from a node in a zone."""
    zone = _find_zone(cs, args.zone)
    node = _find_node(cs, args.zone, args.node)
    tasks = cs.tasks.list_node(zone, node)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.service_type('automation')
def do_role_list(cs, args):
    """List all the roles by zone."""
    zone = _find_zone(cs, args.zone)
    roles = cs.roles.list(zone)
    utils.print_list(roles, ['id', 'name'])


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('role', metavar='<role-id>',
           type=int,
           help='ID of the role.')
@utils.service_type('automation')
def do_role_show(cs, args):
    """Show details about a role."""
    role = _find_role(cs, args.zone, args.role)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(role, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('role', metavar='<role-id>',
           type=int,
           help='ID of the role.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.service_type('automation')
def do_role_deploy(cs, args):
    """Associate a role to a node."""
    zone = _find_zone(cs, args.zone)
    role = _find_role(cs, args.zone, args.role)
    tasks = cs.tasks.deploy(zone, role, args.node)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(tasks, keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('role', metavar='<role-id>',
           type=int,
           help='ID of the role.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.service_type('automation')
def do_component_zone_role_list(cs, args):
    """List all components by zone and role."""
    zone = _find_zone(cs, args.zone)
    role = _find_role(cs, args.zone, args.role)
    components = cs.components.list_zone_role(zone, role)
    utils.print_list(components, ['name', 'properties'], pretty='pretty')


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('role', metavar='<role-id>',
           type=int,
           help='ID of the role.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.arg('component', metavar='<component>',
           help='Name of the component.')
@utils.service_type('automation')
def do_component_zone_role_show(cs, args):
    """Show details about a component by zone and role."""
    zone = _find_zone(cs, args.zone)
    role = _find_role(cs, args.zone, args.role)
    component = _find_component(cs, args.component)
    component_zone_role = cs.components.get_zone_role(zone, role, component)
    keys = ['_links']
    final_dict = utils.remove_values_from_manager_dict(component_zone_role,
                                                       keys)
    final_dict = utils.check_json_pretty_value_for_dict(final_dict)
    utils.print_dict(final_dict)


@utils.arg('zone', metavar='<zone-id>',
           type=int,
           help='ID of the zone.')
@utils.arg('role', metavar='<role-id>',
           type=int,
           help='ID of the role.')
@utils.arg('node', metavar='<node-id>',
           type=int,
           help='ID of the node.')
@utils.arg('component', metavar='<component>',
           help='Name of the component.')
@utils.arg('component_file', metavar='<component-file>',
           help='File with extension *.json describing the'
                'component to update')
@utils.service_type('automation')
def do_component_zone_role_update(cs, args):
    """Update a component by zone and role ."""
    _validate_extension_file(args.zone, 'json')
    zone = _find_zone(cs, args.zone)
    role = _find_role(cs, args.zone, args.role)
    component = _find_component(cs, args.component)

    with open(args.component_file) as f:
        cs.components.update_zone_role(zone, role, component, json.load(f))

    do_component_zone_role_show(cs, args)


def do_endpoints(cs, args):
    """Discover endpoints that get returned from the authenticate services."""
    catalog = cs.client.service_catalog.catalog
    for e in catalog['access']['serviceCatalog']:
        utils.print_dict(e['endpoints'][0], e['name'])
