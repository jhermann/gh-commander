# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, missing-docstring
# pylint: disable=redefined-outer-name, no-self-use, bad-continuation
# pylint: disable=unused-argument, bad-whitespace, invalid-name, protected-access
""" Test 'label' sub-commands.

    See http://click.pocoo.org/3/testing/
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

import pytest
import tablib
from bunch import Bunch
from click.testing import CliRunner

from markers import *
from gh_commander import github
from gh_commander._compat import text_type
from gh_commander.commands import label

#
# Helpers
#

MOCK_DATA = [
    Bunch(name='this-is-a-mocked-test', color='123456'),
    Bunch(name='duplicate', color='cccccc'),
    Bunch(name='enhancement', color='84b6eb'),
]


@pytest.fixture
def apimock():
    """Mocked GitHub API."""
    recorder = []
    github.api.memo.__dict__.setdefault('conns', {})
    github.api.memo.conns[None] = Bunch(
        _recorder = recorder,
        gh_config = Bunch(user='jhermann'),
        repository = lambda user, repo: Bunch(
            labels = lambda: MOCK_DATA,
            create_label = lambda *args: recorder.append(('create', args)) or True,
        ),
    )
    return github.api.memo.conns[None]


#
# 'label list'
#

@cli
def test_command_label_list_uses_the_mocked_data(tmpdir, apimock):
    runner = CliRunner()
    result = runner.invoke(label.label_list, ("jhermann/waif",))
    linecount = len(result.output.splitlines())

    assert result.exit_code == 0, "Exit code OK for 'label list'"
    assert linecount == 5 + len(MOCK_DATA), "Line count is OK"
    assert 'this-is-a-mocked-test' in result.output, "Mocked name appears in output"
    assert '#123456' in result.output, "Mocked color appears in output"


#
# 'label export'
#

@cli
def test_command_label_export_takes_all_explicit_formats_correctly(tmpdir, apimock):
    runner = CliRunner()
    for serializer in label.SERIALIZERS:
        testfile = tmpdir.join("explicit-{}.dat".format(serializer))
        assert str(testfile).endswith('.dat')
        if testfile.exists():
            testfile.remove()
        result = runner.invoke(label.export, ('--format', serializer, "jhermann/waif", "to", str(testfile)))
        # print(serializer, result); print(vars(result))

        assert result.exit_code == 0, "Exit code OK for " + serializer
        assert len(result.output) == 0, "Empty stdout for " + serializer
        assert testfile.ensure(), "Output file created for " + serializer
        assert testfile.size() > 0, "Output file non-empty for " + serializer
        if serializer in label.SERIALIZERS_TEXT:
            content = testfile.read_text('utf-8')
            assert content.endswith('\n'), "Output terminated by newline for " + serializer
            if serializer in label.SERIALIZERS_NEED_NL:
                assert content.splitlines()[-1] != '', "Last line is not empty for " + serializer


@cli
def test_command_label_export_detects_yaml_extension(tmpdir, apimock):
    # testing only one format as a representative here
    runner = CliRunner()
    testfile = tmpdir.join("implicit.yaml")
    assert str(testfile).endswith('.yaml')
    if testfile.exists():
        testfile.remove()
    result = runner.invoke(label.export, ("waif", str(testfile)))

    assert result.exit_code == 0, "Exit code OK for implicit YAML"
    content = testfile.read_text('utf-8')
    assert content.startswith('- {'), "Output file is YAML"


@cli
def test_command_label_export_to_dash_writes_to_stdout(apimock):
    runner = CliRunner()
    result = runner.invoke(label.export, ('--format', 'yaml', "waif", '-'))
    linecount = len(result.output.splitlines())

    assert result.exit_code == 0, "Exit code OK for YAML to stdout"
    assert linecount == len(MOCK_DATA), "Number of dumped lines OK for YAML to stdout"
    assert result.output.startswith('- {'), "stdout is YAML"


@cli
def test_command_label_export_to_dash_without_format_fails(apimock):
    runner = CliRunner()
    result = runner.invoke(label.export, ("waif", '-'))

    assert result.exit_code > 0, "Exit code indicates error for unknown format with stdout"


#
# 'label import'
#

@cli
def test_command_label_import_takes_all_explicit_formats_correctly(tmpdir, apimock):
    runner = CliRunner()
    for serializer in label.DESERIALIZERS:
        tabdata = tablib.Dataset()
        tabdata.headers = label.HEADERS
        tabdata.extend((i.name, i.color) for i in MOCK_DATA)

        testfile = tmpdir.join("explicit-{}.dat".format(serializer))
        with testfile.open('wb') as handle:
            text = getattr(tabdata, serializer)
            if isinstance(text, text_type):
                text = text.encode('utf-8')
            handle.write(text)

        result = runner.invoke(label.label_import, ('--format', serializer, "jhermann/sandbox", "from", str(testfile)))
        # print(serializer, result); print(vars(result)); print(result.output)

        assert result.exit_code == 0, "Exit code OK for " + serializer
        assert len(result.output) >= 0, "Non-empty stdout for " + serializer
        assert 'No changes' in result.output, "Labels are unmodified"


@cli
def test_command_label_import_reports_non_existing_repo(apimock):
    runner = CliRunner()
    apimock.repository = lambda user, repo: None

    result = runner.invoke(label.label_import, ('--format', 'csv', "does-not/exist", "from", os.devnull))
    # print(result); print(vars(result)); print(result.output)

    assert result.exit_code == 0, "Exit code OK for non-existing repo"
    assert 'Non-existing repo' in result.output, "Warning 'Non-existing repo' is printed"


@cli
def test_command_label_import_creates_a_new_label_and_reports_unique_ones(tmpdir, apimock):
    runner = CliRunner()

    testfile = tmpdir.join("create.yaml")
    with testfile.open('wb') as handle:
        handle.write(b"- {Color: '#123456', Name: 'new-test-label'}")

    result = runner.invoke(label.label_import, ("what/ever", "from", str(testfile)))
    # print(result); print(vars(result)); print(result.output); print(apimock._recorder)

    assert result.exit_code == 0, "Exit code OK for new + unqiue label check"
    assert len(apimock._recorder) == 1
    assert apimock._recorder[0] == ('create', ('new-test-label', u'123456')), "Label is added"
    assert 'Created label "new-test-label" with color #123456' in result.output, "Added label is reported"
    assert 'Unique labels in this repo: duplicate, enhancement, this-is-a-mocked-test' in result.output, \
           "Unique label names are reported"
