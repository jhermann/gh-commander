# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" 'user' command.
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

import click

from .. import config, github
from ..util import dclick


def dump_user(api, username):
    """Dump user information to console."""
    gh_user = api.user(username)
    if not gh_user:
        dclick.serror("Unknown user '{}'".format(username))
        return

    userdict = gh_user.as_dict()
    userdict.setdefault('name', '‹N/A›')
    userdict.setdefault('total_private_repos', -1)
    userdict.setdefault('private_gists', -1)
    userdict.setdefault('disk_usage', -1)

    # TODO: Use Jinja2
    click.echo("ACCOUNT     %(name)s [%(login)s / %(type)s #%(id)s]" % userdict)
    click.echo("SINCE/LAST  %(created_at)s / %(updated_at)s" % userdict)
    click.echo("URL         %(html_url)s" % userdict)
    if gh_user.email:
        click.echo("EMAIL       %(email)s" % userdict)
    if gh_user.location:
        click.echo("LOCATION    %(location)s" % userdict)
    click.echo("REPOS/GISTS %(public_repos)s ☑ ⎇  / %(total_private_repos)s ☒ ⎇  "
               "/ %(public_gists)s ☑ ✍ / %(private_gists)s ☒ ✍" % userdict)
    click.echo("STATS       ⇦ ⋮ %(followers)s / ⇨ ⋮ %(following)s / %(disk_usage)s ◔" % userdict)


@config.cli.group()
def user():
    """Managing user accounts."""


@user.command(name='show')
@click.argument('username', nargs=-1)
def user_show(username=None):
    """Dump information about the logged-in or given user(s)."""
    with github.open(config=None) as api: # TODO: config object
        for idx, username in enumerate(username or [api.gh_config.user]):
            if idx:
                click.echo('')
            dump_user(api, username)
