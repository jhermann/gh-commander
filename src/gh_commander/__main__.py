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
from __future__ import absolute_import

import sys

import click

from . import __version__


__app_name__ = 'gh'
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(#version=__version__, prog_name=__app_name__,
    message='%(prog)s %(version)s [Python {}]'.format(' '.join(sys.version.split())),
)
@click.option('-q', '--quiet', is_flag=True, default=False, help='Be quiet (show only errors).')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Create extra verbose output.')
def cli(quiet=False, verbose=False): # pylint: disable=unused-argument
    """'gh' command line tool."""
    appdir = click.get_app_dir(__app_name__)
    #click.secho('appdir = {0}'.format(appdir), fg='yellow')


@cli.command()
def help():
    """Print some helpful message."""
    click.echo('Helpful message.')


if __name__ == "__main__": # imported via "python -m"?
    __package__ = 'gh_commander' # pylint: disable=redefined-builtin
    cli() # pylint: disable=no-value-for-parameter
