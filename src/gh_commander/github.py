# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods, unused-wildcard-import
""" GitHub API helpers.
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

import errno
from netrc import netrc, NetrcParseError

from github3 import *  # pylint: disable=wildcard-import

from ._compat import urlparse


def pretty_cause(cause, prefix=None):
    """Format a GitHub exception nicely."""
    msg = 'Status {} "{}"'.format(cause.code, cause.msg)
    if cause.errors:
        msg += '\n    ' + '\n    '.join(cause.errors)
    if prefix:
        msg = "{}: {}".format(prefix, msg)
    return msg


class GitHubConfig(object):
    """ Holds the configuraton values for GitHub API usage.

        Regarding authentication, see https://developer.github.com/v3/#authentication
    """

    DEFAULT_URL = 'https://api.github.com'
    NETRC_FILE = None  # use the default, unless changed for test purposes


    def __init__(self, config=None):
        """Load configuration, especially authetication."""
        # TODO: look into config for non-default values
        self.base_url = None
        self.user = None
        self.login_or_token = None
        self.password = None
        # self.timeout = 10
        # client_id – string
        # client_secret – string

        self._get_auth(config)


    def auth_valid(self):
        """Return bool indicating whether credentials were provided."""
        return bool(self.login_or_token)


    def _get_auth(self, config):
        """Try to get login auth from either base URL or netrc."""
        auth_url = urlparse(self.base_url or self.DEFAULT_URL)
        if auth_url.username:
            self.user = auth_url.username
        if auth_url.password:
            self.password = auth_url.password
        if self.user and self.password:
            self.login_or_token = self.user
        else:
            self._get_auth_from_netrc(auth_url.hostname)


    def _get_auth_from_netrc(self, hostname):
        """Try to find login auth in ``~/.netrc``."""
        try:
            hostauth = netrc(self.NETRC_FILE)
        except IOError as cause:
            if cause.errno != errno.ENOENT:
                raise
            return
        except NetrcParseError as cause:
            raise  # TODO: Make this log nicely, not produce a stack trace

        auth = None
        if self.user:
            # Try to find specific `user@host` credentials
            auth = hostauth.hosts.get(self.user + '@' + hostname, None)
        if not auth:
            auth = hostauth.hosts.get(hostname, None)

        if auth:
            username, account, password = auth  # pylint: disable=unpacking-non-sequence
            if username:
                self.user = username
            if password == 'token':
                self.login_or_token = account
                self.password = password
            elif password:
                self.login_or_token = self.user
                self.password = password


def api(config=None):
    """ Return an authorized GitHub API connection, based on the given configuration.

        See http://jacquev6.net/PyGithub/v1/github.html for more details.
    """
    cfg = GitHubConfig(config)
    assert cfg.auth_valid(), \
        "Attempt to connect to GitHub API with insufficient credentials! Check your configuration."
    key = '~'.join([cfg.login_or_token, cfg.password or '', cfg.base_url or cfg.DEFAULT_URL])
    if key in api.conns:
        return api.conns[key]
    else:
        if cfg.password == 'token':
            kwargs = dict(token=cfg.login_or_token)
        else:
            kwargs = dict(username=cfg.login_or_token, password=cfg.password)
        if cfg.base_url:
            auth_method = enterprise_login
            kwargs['url'] = cfg.base_url
        else:
            auth_method = login

        # print("AUTH", kwargs)
        apiobj = auth_method(**kwargs)
        apiobj.gh_config = cfg
        api.conns[key] = apiobj
        return apiobj

api.conns = {}
