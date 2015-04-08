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

import os

import click
from click.exceptions import UsageError
import tablib

# TODO: clear up license situation before a final release, or switch to something else
import qstatpretty.ttyutil.color as ttycolor
import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.shrink as ttyshrink
import qstatpretty.ttyutil.size as ttysize

from .. import config, github
from .._compat import string_types
from ..util import dclick


SERIALIZERS_1LINE = ('dict', 'json', 'html')
SERIALIZERS_TEXT  = SERIALIZERS_1LINE + ('yaml', 'csv', 'tsv')
SERIALIZERS_BINARY = ('ods', 'xls', 'xlsx')
SERIALIZERS = SERIALIZERS_TEXT + SERIALIZERS_BINARY  # TODO: export to 'tty'

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


def get_labels(api, repo):
    """Get label dataset for a repo."""
    if '/' in repo:
        user, repo = repo.split('/', 1)
    else:
        user = api.gh_config.user
    gh_repo = api.repository(user, repo)
    data = sorted((label.name, '#' + label.color) for label in gh_repo.labels())
    headers = ('Name', 'Color')
    return user, repo, headers, data


def dump_labels(api, repo):
    """Dump labels of a repo."""
    def padded(rows):
        "Helper"
        for row in rows:
            yield tuple(' {} '.format(cell) for cell in row)

    user, repo, headers, data = get_labels(api, repo)
    data = padded([headers] + list(data))

    #terminal_width = ttysize.terminal_size()[0]
    table_format = DEFAULT_TABLE_FORMAT
    delimiters = ttytable.DELIMITERS_DEFAULT

    table = list(data)
    #table = ttyshrink.grow_table(data, terminal_width, table_format, delimiters)
    click.secho('⎇   {}/{}'.format(user, repo), fg='white', bg='blue', bold=True)
    click.echo(ttytable.pretty_table(table, table_format, delimiters=delimiters))


class LabelAliases(dclick.AliasedGroup):
    """Alias mapping for 'label' commands."""
    MAP = dict(
        ls='list',
    )


@config.cli.group(cls=LabelAliases)
def label():
    """Managing issue labels."""


@label.command(name='list')
@click.argument('repo', nargs=-1)
def label_list(repo=None):
    """Dump labels within the given repo(s)."""
    api = github.api(config=None)  # TODO: config object

    for idx, reponame in enumerate(repo or []):
        if idx:
            click.echo('')
        dump_labels(api, reponame)


@label.command()
@click.option('--format', 'serializer', default=None, type=click.Choice(SERIALIZERS),
    help="Output format (defaults to extension of `outfile`).",
)
@click.argument('repo', nargs=-1)
@click.argument('outfile', type=click.File('wb'))
@click.pass_context
def export(ctx, repo, outfile, serializer):
    """Export labels of the given repo(s) to a file."""
    api = github.api(config=None)  # TODO: config object
    tabdata = tablib.Dataset()
    if repo and repo[-1].lower() == 'to':
        repo = repo[:-1]
    if not repo:
        raise UsageError("You provided no repository names!", ctx=ctx)
    if serializer is None:
        outname = getattr(outfile, 'name', None)
        _, ext = os.path.splitext(outname or '<stream>')
        ext = ext.lstrip('.')
        if ext in SERIALIZERS:
            serializer = ext
        else:
            raise UsageError('No --format given, and extension of "{}" is not one of {}.'
                             .format(outname, ', '.join(SERIALIZERS)), ctx=ctx)

    for idx, reponame in enumerate(repo):
        user, repo, headers, data = get_labels(api, reponame)
        if not idx:
            tabdata.headers = headers
        tabdata.append_separator('⎇   {}/{}'.format(user, repo).encode('utf-8'))
        for row in data:
            tabdata.append(tuple(i.encode('utf-8') for i in row))

    text = getattr(tabdata, serializer)
    if not isinstance(text, string_types):
        text = repr(text)
    if serializer in SERIALIZERS_1LINE:
        text += '\n'
    outfile.write(text)
