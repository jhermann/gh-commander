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
import re

import click
from click.exceptions import UsageError
import tablib

# TODO: clear up license situation before a final release, or switch to something else
import qstatpretty.ttyutil.color as ttycolor
import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.shrink as ttyshrink
# import qstatpretty.ttyutil.size as ttysize

from .. import config, github
from .._compat import text_type, string_types
from ..util import dclick


DESERIALIZERS = ('json', 'yaml', 'csv', 'tsv')
SERIALIZERS_NEED_NL = ('dict', 'json', 'html')
SERIALIZERS_TEXT = SERIALIZERS_NEED_NL + ('yaml', 'csv', 'tsv')
SERIALIZERS_BINARY = ('ods', 'xls')  # this just doesn't work right (Unicode issues): , 'xlsx')
SERIALIZERS = SERIALIZERS_TEXT + SERIALIZERS_BINARY  # TODO: export to 'tty'
HEADERS = ('Name', 'Color')

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


def get_labels(api, repo, raw=False):
    """Get label dataset for a repo."""
    if '/' in repo:
        user, repo = repo.split('/', 1)
    else:
        user = api.gh_config.user
    gh_repo = api.repository(user, repo)
    if raw:
        return user, repo, gh_repo.labels()
    else:
        data = sorted((label.name, '#' + label.color) for label in gh_repo.labels())
        return user, repo, data


def dump_labels(api, repo):
    """Dump labels of a repo."""
    def padded(rows):
        "Helper"
        for row in rows:
            yield tuple(' {} '.format(cell) for cell in row)

    user, repo, data = get_labels(api, repo)
    data = padded([HEADERS] + list(data))

    # terminal_width = ttysize.terminal_size()[0]
    table_format = DEFAULT_TABLE_FORMAT
    delimiters = ttytable.DELIMITERS_DEFAULT

    table = list(data)
    # table = ttyshrink.grow_table(data, terminal_width, table_format, delimiters)
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
@click.option('-f', '--format', 'serializer', default=None, type=click.Choice(SERIALIZERS),
    help="Output format (defaults to extension of OUTFILE).",
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
    outname = getattr(outfile, 'name', None)
    if serializer is None:
        _, ext = os.path.splitext(outname or '<stream>')
        ext = ext.lstrip('.')
        if ext in SERIALIZERS:
            serializer = ext
        else:
            raise UsageError('No --format given, and extension of "{}" is not one of {}.'
                             .format(outname, ', '.join(SERIALIZERS)), ctx=ctx)

    for idx, reponame in enumerate(repo):
        user, repo, data = get_labels(api, reponame)
        if not idx:
            tabdata.headers = HEADERS
        tabdata.append_separator('⎇   {}/{}'.format(user, repo))
        tabdata.extend(data)

    text = getattr(tabdata, serializer)
    if not isinstance(text, string_types):
        text = repr(text)
    if serializer in SERIALIZERS_NEED_NL:
        text += '\n'
    if isinstance(text, text_type):
        text = text.encode('utf-8')
    try:
        outfile.write(text)
    except EnvironmentError as cause:
        raise dclick.LoggedFailure('Error while writing "{}" ({})'.format(outname, cause))


@label.command(name='import')
@click.option('-f', '--format', 'serializer', default=None, type=click.Choice(DESERIALIZERS),
    help="Input format (defaults to extension of INFILE).",
)
@click.argument('repo', nargs=-1)
@click.argument('infile', type=click.File('rb'))
@click.pass_context
def label_import(ctx, repo, infile, serializer):
    """Import labels to the given repo(s) out of a file."""
    # TODO: refactor prep code to function, see export for dupe code
    api = github.api(config=None)  # TODO: config object
    tabdata = tablib.Dataset()
    if repo and repo[-1].lower() == 'from':
        repo = repo[:-1]
    if not repo:
        raise UsageError("You provided no repository names!", ctx=ctx)
    inname = getattr(infile, 'name', None)
    if serializer is None:
        _, ext = os.path.splitext(inname or '<stream>')
        ext = ext.lstrip('.')
        if ext in SERIALIZERS:
            serializer = ext
        else:
            raise UsageError('No --format given, and extension of "{}" is not one of {}.'
                             .format(inname, ', '.join(DESERIALIZERS)), ctx=ctx)

    try:
        data = infile.read()
    except EnvironmentError as cause:
        raise dclick.LoggedFailure('Error while reading "{}" ({})'.format(outname, cause))

    # Read label data, and make it unique
    setattr(tabdata, serializer, data)
    import_labels = {}
    for label in tabdata.dict:
        name, color = label[HEADERS[0]], label[HEADERS[1]].lstrip('#').lower()
        if not re.match("[0-9a-f]{6}", color):
            raise dclick.LoggedFailure('Bad color <{}> for label "{}"'.format(color, name))
        if name in import_labels and color != import_labels[name]:
            click.echo('INFO Changing color from #{} to #{} for duplicate import label "{}"'
                       .format(import_labels[name], color, name))
        import_labels[name] = color

    # Update given repos
    for reponame in repo:
        labels = import_labels.copy()
        changed = False
        unique = {}
        user, repo, repo_labels = get_labels(api, reponame, raw=True)
        click.secho('⎇   {}/{}'.format(user, repo), fg='white', bg='blue', bold=True)
        gh_repo = api.repository(user, repo)
        if not gh_repo:
            click.secho('ERR  Non-existing repo!', fg='black', bg='yellow', bold=True)
            continue

        # Check if existing labels need updating
        for existing in repo_labels:
            if existing.name in labels:
                if existing.color != labels[existing.name]:
                    status = 'OK' if existing.update(existing.name, labels[existing.name]) else 'ERR'
                    click.echo('{:4s} Updated label "{}" with color #{}'
                               .format(status, existing.name, labels[existing.name]))
                    changed = True
                del labels[existing.name]
            else:
                unique[existing.name] = existing

        # Create any remaining labels
        if labels:
            for name, color in sorted(labels.items()):
                status = 'OK' if gh_repo.create_label(name, color) else 'ERR'
                click.echo('{:4s} Created label "{}" with color #{}'.format(status, name, color))
        elif not changed:
            click.echo('INFO No changes.')

        # Show info on labels not in the import set
        if unique:
            click.echo("INFO Unique labels in this repo: {}".format(', '.join(sorted(unique.keys()))))
