# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
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

from . import config, github


def pretty_path(path, _home_re=re.compile('^' + re.escape(os.path.expanduser('~') + os.sep))):
    """Prettify path for humans."""
    path = _home_re.sub('~' + os.sep, path)
    return path


class AttributeMapping(object):
    """Access attributes of an object via the mapping protocol."""
    def __init__(self, obj):
        self._obj = obj

    def __getitem__(self, key, default=None):
        return getattr(self._obj, key, default)


def dump_user(api, username):
    """Dump user information to console."""
    gh_user = api.get_user(username)
    userdict = AttributeMapping(gh_user)
    click.echo("ACCOUNT     %(name)s [%(login)s / %(type)s #%(id)s]" % userdict)
    click.echo("SINCE/LAST  %(created_at)s / %(updated_at)s" % userdict)
    click.echo("URL         %(url)s" % userdict)
    if gh_user.email:
        click.echo("EMAIL       %(email)s" % userdict)
    if gh_user.location:
        click.echo("LOCATION    %(location)s" % userdict)
    click.echo("REPOS/GISTS %(public_repos)s ☑ ⎇  / %(private_repos)s ☒ ⎇  "
               "/ %(public_gists)s ☑ ✍ / %(private_gists)s ☒ ✍" % userdict)
    click.echo("STATS       ⇦ ⋮ %(followers)s / ⇨ ⋮ %(following)s / %(disk_usage)s ◔" % userdict)


@config.cli.command(name='help')
@click.pass_context
def help_command(ctx):
    """Print some information on the system environment."""
    def banner(title):
        "Helper"
        click.echo('')
        click.secho('~~~ {} ~~~'.format(title), fg='green', bg='black', bold=True)

    app_name = ctx.find_root().info_name
    click.secho('*** "{}" Help & Information ***'.format(app_name), fg='white', bg='blue', bold=True)

    banner('Version Information')
    click.echo(config.version_info(ctx))

    banner('Configuration')
    locations = config.locations(exists=False, extras=ctx.find_root().params.get('config', None))
    locations = [(u'✔' if os.path.exists(i) else u'✘', pretty_path(i)) for i in locations]
    click.echo(u'The following configuration files are merged in order, if they exist:\n    {0}'.format(
        u'\n    '.join(u'{}   {}'.format(*i) for i in locations),
    ))

    banner('Active Login')
    try:
        api = github.api(config=None)  # TODO: config object
    except AssertionError as cause:
        click.secho("AUTH: {}".format(cause), fg='white', bg='red', bold=True)
    else:
        try:
            dump_user(api, api.gh_config.user)
        except github.BadCredentialsException as cause:
            click.secho(github.pretty_cause(cause, "API"), fg='white', bg='red', bold=True)

    banner('More Help')
    click.echo("Call '{} --help' to get a list of available commands & options.".format(app_name))
    click.echo("Call '{} «command» --help' to get help on a specific command.".format(app_name))
    click.echo("Call '{} --version' to get the above version information separately.".format(app_name))
    click.echo("Call '{} --license' to get licensing informatioon.".format(app_name))

    #click.echo('\ncontext = {}'.format(repr(vars(ctx))))
    #click.echo('\nparent = {}'.format(repr(vars(ctx.parent))))


@config.cli.group()
def user():
    """Managing GitHub user accounts."""


@user.command(name='show')
@click.argument('username', nargs=-1)
def user_show(username=None):
    """Dump information about the logged-in user."""
    api = github.api(config=None)  # TODO: config object

    for username in username or [api.gh_config.user]:
        dump_user(api, username)
