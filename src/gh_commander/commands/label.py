# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" 'label' command.

    See http://github3py.readthedocs.org/en/master/issues.html#github3.issues.label.Label
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

# TODO: clear up license situation before a final release, or switch to something else
import qstatpretty.ttyutil.color as ttycolor
import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.size as ttysize

from .. import config, github


DEFAULT_TABLE_FORMAT = [
    {
        'key': 'name',
        'title': 'name',
        'color': lambda x: ttycolor.COLOR_GREEN,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=10, overflow=2),
    },
    {
        'key': 'color',
        'title': 'user',
        'color': lambda x: ttycolor.COLOR_YELLOW,
        'ellipsis': ttyshrink.simple_ellipsis(),
        'fval': ttyshrink.simple_value(factor=3),
    },
]


def dump_labels(api, repo):
    """Dump labels of a repo."""
    def pad(cell):
        "Helper"
        return ' {} '.format(cell)

    if '/' in repo:
        user, repo = repo.split('/', 1)
    else:
        user = api.gh_config.user
    gh_repo = api.repository(user, repo)
    data = sorted((pad(label.name), pad('#' + label.color)) for label in gh_repo.labels())
    data = [(pad('Name'), pad('Color'))] + list(data)

    terminal_width = ttysize.terminal_size()[0]
    table_format = DEFAULT_TABLE_FORMAT
    delimiters = ttytable.DELIMITERS_DEFAULT

    table = data
    #table = ttyshrink.grow_table(data, terminal_width, table_format, delimiters)
    click.secho('⎇   {}/{}'.format(user, repo), fg='white', bg='blue', bold=True)
    click.echo(ttytable.pretty_table(table, table_format, delimiters=delimiters))


@config.cli.group()
def label():
    """Managing issue labels."""


@label.command(name='list')
@click.argument('repo', nargs=-1)
def label_list(repo=None):
    """Dump labels within the given repo(s)."""
    api = github.api(config=None)  # TODO: config object

    for idx, repo in enumerate(repo or []):
        if idx:
            click.echo('')
        dump_labels(api, repo)