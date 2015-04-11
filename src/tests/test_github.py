# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name
""" Test 'github' module.
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

import unittest

# import pytest
from bunch import Bunch

from gh_commander import github


class PrettyCauseTest(unittest.TestCase):

    cause = Bunch(code=42, msg='MSG', errors=[])

    def test_pretty_cause_formats_an_exception(self):
        text = github.pretty_cause(self.cause)
        assert text == 'Status 42 "MSG"'


    def test_pretty_cause_uses_errors_attribute(self):
        cause = Bunch(self.cause)
        cause.errors = ['ERR']
        text = github.pretty_cause(cause)
        assert text == 'Status 42 "MSG"\n    ERR'


    def test_pretty_cause_uses_a_prefix(self):
        text = github.pretty_cause(self.cause, prefix='PREFIX')
        assert text == 'PREFIX: Status 42 "MSG"'
