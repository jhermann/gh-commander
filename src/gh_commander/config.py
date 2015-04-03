# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Configuration utilities.
"""
# Copyright ©  2015 Jürgen Hermann <jh@web.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

import os
import sys

import click

from ._compat import iteritems


# These will be filled by `__main__`
APP_NAME = None
cli = None


def version_info(ctx=None):
    """Return version information just like --version does."""
    from .__main__ import VERSION_INFO, __app_name__, __name__ as main_name
    from . import __version__

    prog = ctx.find_root().info_name if ctx else __app_name__
    version = __version__
    try:
        import pkg_resources
    except ImportError:
        pass
    else:
        for dist in pkg_resources.working_set:
            scripts = dist.get_entry_map().get('console_scripts') or {}
            for script_name, entry_point in iteritems(scripts):
                if entry_point.module_name == main_name:
                    version = dist.version
                    break

    return VERSION_INFO % dict(prog=prog, version=version)


def envvar(name, default=None):
    """Return an environment variable specific for this application (using a prefix)."""
    varname = (APP_NAME + '-' + name).upper().replace('-', '_')
    return os.environ.get(varname, default)


def locations(exists=True, extras=None):
    """Return the location of the config file(s)."""
    result = []
    candidates = [
        os.path.join(click.get_app_dir(APP_NAME), "config.ini"),
    ] + (extras and list(extras) or [])

    for config_file  in candidates:
        if config_file and (not exists or os.path.exists(config_file)):
            result.append(config_file)

    return result
