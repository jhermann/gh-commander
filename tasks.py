# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, bad-continuation
""" Project automation for Invoke.
"""
from __future__ import absolute_import, unicode_literals

import os

from invoke import run, task
from rituals.invoke_tasks import * # pylint: disable=redefined-builtin


@task(help={
    'verbose': "Make 'tox' more talkative",
    'env-list': "Override list of environments to use (e.g. 'py27,py34')",
    'opts': "Extra flags for tox",
    'pty': "Whether to run tox under a pseudo-tty",
})
def tox(verbose=False, env_list='', opts='', pty=True):
    """Perform multi-environment tests."""
    snakepits = ['/opt/pyenv/bin'] # TODO: config value
    cmd = []

    snakepits = [i for i in snakepits if os.path.isdir(i)]
    if snakepits:
        cmd += ['PATH="{}:$PATH"'.format(os.pathsep.join(snakepits),)]

    cmd += ['tox']
    if verbose:
        cmd += ['-v']
    if env_list:
        cmd += ['-e', env_list]
    cmd += opts
    cmd += ['2>&1']
    run(' '.join(cmd), echo=True)


@task
def ci(): # pylint: disable=invalid-name
    """Perform continuous integration tasks."""
    run("invoke clean --all build --docs test check --reports tox 2>&1", echo=True)
