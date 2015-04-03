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
from netrc import netrc
from urlparse import urlparse

from github import *  # pylint: disable=wildcard-import

from ._compat import iteritems


def pretty_cause(cause, prefix=None):
    """Format a GitHub exception nicely."""
    data = cause.data.copy()
    doc_url = data.pop('documentation_url', 'N/A')
    msg = "Status {} <{}>, see {}".format(
        cause.status,
        ' '.join("{}={}".format(key, val) for key, val in sorted(iteritems(data))),
        doc_url,
    )
    if prefix:
        msg = "{}: {}".format(prefix, msg)
    return msg


class GitHubConfig(object):
    """ Holds the configuraton values for GitHub API usage.

        Regarding authentication, see https://developer.github.com/v3/#authentication
    """

    NETRC_FILE = None  # use the default, unless changed for test purposes


    def __init__(self, config=None):
        """Load configuration, especially authetication."""
        # TODO: look into config for non-default values
        self.base_url = 'https://api.github.com'
        self.user = None
        self.login_or_token = None
        self.password = None
        self.timeout = 10
        # client_id – string
        # client_secret – string

        self._get_auth(config)


    def auth_valid(self):
        """Return bool indicating whether credentials were provided."""
        return bool(self.login_or_token)


    def _get_auth(self, config):
        """Try to get login auth from either base URL or netrc."""
        auth_url = urlparse(self.base_url)
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

        auth = None
        if self.user:
            # Try to find specific `user@host` credentials
            auth = hostauth.hosts.get(self.user + '@' + hostname, None)
        if not auth:
            auth = hostauth.hosts.get(hostname, None)

        if auth:
            login, account, password = auth  # pylint: disable=unpacking-non-sequence
            if login:
                self.user = login
            if password == 'token':
                self.login_or_token = account
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
    key = '~'.join([cfg.login_or_token, cfg.password or '', cfg.base_url])
    if key in api.conns:
        return api.conns[key]
    else:
        apiobj = Github(cfg.login_or_token, cfg.password, cfg.base_url, timeout=cfg.timeout)
        apiobj.gh_config = cfg
        api.conns[key] = apiobj
        return apiobj

api.conns = {}
