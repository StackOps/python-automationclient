# Copyright 2013 OpenStack LLC

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
from functools import reduce

import os
import re
import sys
import uuid
import operator
import cStringIO

import six
import prettytable
import json

from automationclient import exceptions
from automationclient.openstack.common import strutils


def arg(*args, **kwargs):
    """Decorator for CLI args."""

    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def env(*vars, **kwargs):
    """
    returns the first environment variable set
    if none are non-empty, defaults to '' or keyword arg default
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def add_arg(f, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(f, 'arguments'):
        f.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in f.arguments:
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))


def add_resource_manager_extra_kwargs_hook(f, hook):
    """Adds hook to bind CLI arguments to ResourceManager calls.

    The `do_foo` calls in shell.py will receive CLI args and then in turn pass
    them through to the ResourceManager. Before passing through the args, the
    hooks registered here will be called, giving us a chance to add extra
    kwargs (taken from the command-line) to what's passed to the
    ResourceManager.
    """
    if not hasattr(f, 'resource_manager_kwargs_hooks'):
        f.resource_manager_kwargs_hooks = []

    names = [h.__name__ for h in f.resource_manager_kwargs_hooks]
    if hook.__name__ not in names:
        f.resource_manager_kwargs_hooks.append(hook)


def get_resource_manager_extra_kwargs(f, args, allow_conflicts=False):
    """Return extra_kwargs by calling resource manager kwargs hooks."""
    hooks = getattr(f, "resource_manager_kwargs_hooks", [])
    extra_kwargs = {}
    for hook in hooks:
        hook_name = hook.__name__
        hook_kwargs = hook(args)

        conflicting_keys = set(hook_kwargs.keys()) & set(extra_kwargs.keys())
        if conflicting_keys and not allow_conflicts:
            msg = ("Hook '%(hook_name)s' is attempting to redefine attributes "
                   "'%(conflicting_keys)s'" % {
                       'hook_name': hook_name,
                       'conflicting_keys': conflicting_keys
                   })
            raise Exception(msg)

        extra_kwargs.update(hook_kwargs)

    return extra_kwargs


def unauthenticated(f):
    """
    Adds 'unauthenticated' attribute to decorated function.
    Usage:
        @unauthenticated
        def mymethod(f):
            ...
    """
    f.unauthenticated = True
    return f


def isunauthenticated(f):
    """
    Checks to see if the function is marked as not requiring authentication
    with the @unauthenticated decorator. Returns True if decorator is
    set to True, False otherwise.
    """
    return getattr(f, 'unauthenticated', False)


def service_type(stype):
    """
    Adds 'service_type' attribute to decorated function.
    Usage:
        @service_type('automation')
        def mymethod(f):
            ...
    """

    def inner(f):
        f.service_type = stype
        return f

    return inner


def get_service_type(f):
    """
    Retrieves service type from function
    """
    return getattr(f, 'service_type', None)


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def _print(pt, order):
    if sys.version_info >= (3, 0):
        print(pt.get_string(sortby=order))
    else:
        print(strutils.safe_encode(pt.get_string(sortby=order)))


def print_list(objs, fields, formatters={}, order_by=None, pretty=None):
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.aligns = ['l' for f in fields]

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                field_name = field.lower().replace(' ', '_')
                data = getattr(o, field_name, '')
                if isinstance(data, dict):
                    if pretty:
                        row.append(json.dumps(data, sort_keys=True, indent=4,
                                              separators=(',', ': ')))
                    else:
                        row.append(json.dumps(data))
                else:
                    row.append(data)
        pt.add_row(row)

    if order_by is None:
        order_by = fields[0]
    _print(pt, order_by)


def print_indent_list(rows, hasHeader=False, headerChar='-', delim=' | ',
                      justify='left', separateRows=False, prefix='',
                      postfix='', wrapfunc=lambda x: x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column.
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in map(None,
                                                                  *newRows)]

        # break each logical row into one or more physical ones

    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None, *reduce(operator.add, logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column])
                 for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths)
                                 + len(delim) * (len(maxWidths) - 1))
    # select the appropriate justify method
    justify = {'center': str.center, 'right': str.rjust,
               'left': str.ljust}[justify.lower()]
    output = cStringIO.StringIO()
    if separateRows:
        print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, prefix + delim.join([justify(str(item), width)
                                                  for (item, width) in
                                                  zip(row,
                                                      maxWidths)]) + postfix
        if separateRows or hasHeader:
            print >> output, rowSeparator
        hasHeader = False
    return output.getvalue()


def print_dict(d, property="Property"):
    """

    :param d:
    :param property:
    """
    pt = prettytable.PrettyTable([property, 'Value'], caching=False)
    pt.aligns = ['l', 'l']
    [pt.add_row(list(r)) for r in six.iteritems(d)]
    _print(pt, property)


def remove_values_from_manager_dict(manager, keys):
    final_dict = {}
    for key, value in manager._info.items():
        if key not in keys:
            final_dict.update({key: value})
    return final_dict


def check_json_value_for_dict(data):
    final_dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            final_dict.update({key: json.dumps(value)})
        else:
            final_dict.update({key: value})
    return final_dict


def check_json_pretty_value_for_dict(data):
    final_dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            final_dict.update({key: json.dumps(value, sort_keys=True, indent=4,
                                               separators=(',', ': '))})
        elif isinstance(value, list):
            for val in value:
                final_dict.update({key: json.dumps(val, sort_keys=True,
                                                   indent=4,
                                                   separators=(',', ': '))})
        else:
            final_dict.update({key: value})
    return final_dict


def find_resource(manager, name_or_id):
    """Helper for the _find_* methods."""
    # first try to get entity as integer id
    try:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            return manager.get(int(name_or_id))
    except exceptions.NotFound:
        pass

    if sys.version_info <= (3, 0):
        name_or_id = strutils.safe_decode(name_or_id)

    # now try to get entity as uuid
    try:
        uuid.UUID(name_or_id)
        return manager.get(name_or_id)
    except (ValueError, exceptions.NotFound):
        pass

    try:
        try:
            return manager.find(human_id=name_or_id)
        except exceptions.NotFound:
            pass

        # finally try to find entity by name
        try:
            return manager.find(name=name_or_id)
        except exceptions.NotFound:
            try:
                return manager.find(display_name=name_or_id)
            except (UnicodeDecodeError, exceptions.NotFound):
                try:
                    # Volumes does not have name, but display_name
                    return manager.find(display_name=name_or_id)
                except exceptions.NotFound:
                    msg = "No %s with a name or ID of '%s' exists." % \
                          (manager.resource_class.__name__.lower(), name_or_id)
                    raise exceptions.CommandError(msg)
    except exceptions.NoUniqueMatch:
        msg = ("Multiple %s matches found for '%s', use an ID to be more"
               " specific." % (manager.resource_class.__name__.lower(),
                               name_or_id))
        raise exceptions.CommandError(msg)


def _format_servers_list_networks(server):
    output = []
    for (network, addresses) in list(server.networks.items()):
        if len(addresses) == 0:
            continue
        addresses_csv = ', '.join(addresses)
        group = "%s=%s" % (network, addresses_csv)
        output.append(group)

    return '; '.join(output)


class HookableMixin(object):
    """Mixin so classes can register and run hooks."""
    _hooks_map = {}

    @classmethod
    def add_hook(cls, hook_type, hook_func):
        if hook_type not in cls._hooks_map:
            cls._hooks_map[hook_type] = []

        cls._hooks_map[hook_type].append(hook_func)

    @classmethod
    def run_hooks(cls, hook_type, *args, **kwargs):
        hook_funcs = cls._hooks_map.get(hook_type) or []
        for hook_func in hook_funcs:
            hook_func(*args, **kwargs)


def safe_issubclass(*args):
    """Like issubclass, but will just return False if not a class."""

    try:
        if issubclass(*args):
            return True
    except TypeError:
        pass

    return False


def import_class(import_str):
    """Returns a class from a string including module and class."""
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    return getattr(sys.modules[mod_str], class_str)


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


# http://code.activestate.com/recipes/
#   577257-slugify-make-a-string-usable-in-a-url-or-filename/
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata

    if not isinstance(value, six.text_type):
        value = six.text_type(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = six.text_type(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)
