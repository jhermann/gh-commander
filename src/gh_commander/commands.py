# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" CLI commands.
"""
# Copyright ©  2015 Jürgen Hermann <jh@web.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

import os
import re

import click

from . import config


def pretty_path(path, _home_re=re.compile('^' + re.escape(os.path.expanduser('~') + os.sep))):
    """Prettify path for humans."""
    path = _home_re.sub('~' + os.sep, path)
    return path



@config.cli.command(name='help')
@click.pass_context
def help_command(ctx):
    """Print some information on the system environment."""
    app_name = ctx.find_root().info_name
    click.secho('*** "{}" Help & Information ***'.format(app_name), fg='white', bg='blue', bold=True)
    click.echo('')
    click.echo(config.version_info(ctx))

    locations = config.locations(exists=False, extras=ctx.find_root().params.get('config', None))
    locations = [(u'✔' if os.path.exists(i) else u'✘', pretty_path(i)) for i in locations]
    click.echo(u'\nThe following configuration files are merged in order, if they exist:\n    {0}'.format(
        u'\n    '.join(u'{}   {}'.format(*i) for i in locations),
    ))
    click.echo("\nCall '{} --help' to get a list of available commands & options.".format(app_name))
    click.echo("Call '{} «command» --help' to get help on a specific command.".format(app_name))
    click.echo("Call '{} --version' to get the above version information separately.".format(app_name))
    click.echo("Call '{} --license' to get licensing informatioon.".format(app_name))

    #click.echo('\ncontext = {}'.format(repr(vars(ctx))))
    #click.echo('\nparent = {}'.format(repr(vars(ctx.parent))))
