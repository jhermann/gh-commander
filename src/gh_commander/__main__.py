# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Command line interface.
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
import sys

import click


__app_name__ = 'gh'
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)
try:
    CLI_PATH = sys.modules['__main__'].__file__
except (KeyError, AttributeError):
    CLI_PATH = __file__
CLI_PATH = os.path.dirname(CLI_PATH)
if CLI_PATH.endswith('/bin'):
    CLI_PATH = CLI_PATH[:-4]
VERSION_INFO = '%(prog)s %(version)s from {} [Python {}]'.format(
    re.sub('^' + os.path.expanduser('~'), '~', CLI_PATH),
    ' '.join(sys.version.split()[:1]),
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(message=VERSION_INFO)
@click.option('-q', '--quiet', is_flag=True, default=False, help='Be quiet (show only errors).')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Create extra verbose output.')
def cli(quiet=False, verbose=False):  # pylint: disable=unused-argument
    """'gh' command line tool."""


@cli.command(name='help')
def help_command():
    """Print some helpful message."""
    appdir = click.get_app_dir(__app_name__)  # noqa  pragma: no cover
    click.secho('The configuration can be found at {0}'.format(appdir), fg='white', bg='blue', bold=True)


if __name__ == "__main__":  # imported via "python -m"?
    __package__ = 'gh_commander'  # pylint: disable=redefined-builtin
    cli()  # pylint: disable=no-value-for-parameter
