# gh-commander

GitHub Commander is a tool to access the
[GitHub API v3](https://developer.github.com/v3/)
from the CLI and automate otherwise tedious tasks.

![logo](https://raw.githubusercontent.com/jhermann/gh-commander/master/docs/_static/logo-64.png)
 
 [![Travis CI](https://api.travis-ci.org/jhermann/gh-commander.svg)](https://travis-ci.org/jhermann/gh-commander)
 [![GitHub Issues](https://img.shields.io/github/issues/jhermann/gh-commander.svg)](https://github.com/jhermann/gh-commander/issues)
 [![License](https://img.shields.io/pypi/l/gh-commander.svg)](https://github.com/jhermann/gh-commander/blob/master/LICENSE)
 [![Development Status](https://pypip.in/status/gh-commander/badge.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Latest Version](https://img.shields.io/pypi/v/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Download format](https://pypip.in/format/gh-commander/badge.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Downloads](https://img.shields.io/pypi/dw/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)


## Overview

*GitHub Commander* implements the ``gh`` command line tool,
which provides a ‘fluent’ interface
using [click](https://github.com/mitsuhiko/click)
(see [Usage](#usage) below).
It allows to access the
[GitHub API v3](https://developer.github.com/v3/)
from a shell prompt for things usually done in the browser,
and also automates tasks that otherwise are tedious at best,
when done by clicking around on a web page.
*GitHub Commander* is powered by [github3.py](https://github.com/sigmavirus24/github3.py).

:information_source: | Initially, the focus of the project will be to provide task automation, not completeness of covering every API aspect!
---- | :----


## Installation

See [Contributing](#contributing) for now.

To add bash completion, read the [Click docs](http://click.pocoo.org/4/bashcomplete/#activation) about it,
or just follow these instructions:

```sh
cmdname=gh
mkdir -p ~/.bash_completion.d
_$(tr a-z A-Z <<<"$cmdname")_COMPLETE=source $cmdname >~/.bash_completion.d/$cmdname.sh
grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
    || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
. "/etc/bash_completion"
```


## A Practical Example

**TODO** Bash script that syncs issue labels in all of a user's projects with a master project.


## Configuration

### Login Credentials
Before you can use *GitHub Commander*, you have to provide some minimal configuration,
most importantly credentials for API access. The recommended way for doing so is this:

 1. In the [Settings › Applications](https://github.com/settings/applications) of your GitHub account,
    press the “Generate new token” button of the “Personal access tokens” section, and follow the instructions.
    Copy the generated token to the clipboard, for use in the next step.
 2. Create the file ``~/.netrc`` with the following contents (or add that to the existing file):

        machine api.github.com
            user «your GitHub username»
            password token
            account «your personal access token»

 3. Call ``chmod 600 ~/.netrc`` to protect your sensitive data.

This way, the sensitive authentication information is separate from the rest of the configuration.
Use the ``gh help`` command to check whether your credentials actually work
– if they do, your GitHub user information is displayed, otherwise you'll get an error indicator.


### Main Configuration File

**TODO**


## Usage

Most of the commands are intentionally self-explanatory,
so usually they are just listed without further details,
in the hope that it's quite obvious what they do.


### General Options

 * ``--user ‹account name›`` – Override account name from config.
 * ``--token ‹API token›`` – Override API token from config.
 * ``--site ‹base URL›`` – Override site URL for on-premise installations of GitHub.

### Common Arguments

 * ``‹repo›`` – A repository name, either fully qualified in the form ``‹account›/‹repo›``, or else a plain repository name assumed to be owned by the current user.


### Labels

 * :heavy_check_mark: ``gh label list ‹repo›…``
 * :soon: ``gh label export ‹repo› [to] ‹filename›``
 * :soon: ``gh label import ‹repo› [from] ‹filename›``


### Users

 * :heavy_check_mark: ``gh user show [‹username›…]``


### Miscellaneous

 * :heavy_check_mark: ``gh help`` – Show information about the installation & configuration, and how to get further help.


## Contributing

To create a working directory for this project, call these commands:

```sh
git clone "https://github.com/jhermann/gh-commander.git"
cd "gh-commander"
. .env --yes --develop
invoke ci
```

See [CONTRIBUTING](https://github.com/jhermann/gh-commander/blob/master/CONTRIBUTING.md) for more.

[![Throughput Graph](https://graphs.waffle.io/jhermann/gh-commander/throughput.svg)](https://waffle.io/jhermann/gh-commander/metrics)


## References

**General**
* [GitHub API v3](https://developer.github.com/v3/)

**Similar Projects**
* [sigmavirus24/github-cli](https://github.com/sigmavirus24/github-cli)

**Tools**

* [Cookiecutter](http://cookiecutter.readthedocs.org/en/latest/)
* [PyInvoke](http://www.pyinvoke.org/)
* [pytest](http://pytest.org/latest/contents.html)
* [tox](https://tox.readthedocs.org/en/latest/)
* [Pylint](http://docs.pylint.org/)
* [twine](https://github.com/pypa/twine#twine)
* [bpython](http://docs.bpython-interpreter.org/)
* [yolk3k](https://github.com/myint/yolk#yolk)

**Packages**

* [github3.py](http://github3py.readthedocs.org/)
* [Rituals](https://jhermann.github.io/rituals)
* [Click](http://click.pocoo.org/)
* [sh](http://amoffat.github.io/sh/)


## Acknowledgements

 * Logo elements from [clker.com Free Clipart](http://www.clker.com/).
