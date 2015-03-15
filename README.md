# gh-commander

GitHub Commander is a tool to access the
[GitHub API v3](https://developer.github.com/v3/)
from the CLI and automate otherwise tedious tasks.

![logo](https://raw.githubusercontent.com/jhermann/gh-commander/master/docs/_static/logo-64.png)
 
 [![Travis CI](https://api.travis-ci.org/jhermann/gh-commander.svg)](https://travis-ci.org/jhermann/gh-commander)
 [![GitHub Issues](https://img.shields.io/github/issues/jhermann/gh-commander.svg)](https://github.com/jhermann/gh-commander/issues)
 [![License](https://img.shields.io/pypi/l/gh-commander.svg)](https://github.com/jhermann/gh-commander/blob/master/LICENSE)
 [![Latest Version](https://img.shields.io/pypi/v/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Downloads](https://img.shields.io/pypi/dw/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)


## Overview

GitHub Commander implements the ``gh`` command line tool,
which provides a ‘fluent’ interface
using [click](https://github.com/mitsuhiko/click)
(see [Usage](#usage) below).
It allows to access the
[GitHub API v3](https://developer.github.com/v3/)
from a shell prompt for things usually done in the browser,
and also automates tasks that otherwise are tedious at best,
when done by clicking around on a web page.
GitHub Commander is powered by [PyGithub](https://github.com/PyGithub/PyGithub).

:information_source: | Initially, the focus of the project will be to provide task automation, not completeness of covering every API aspect!
---- | :----


## Installation

See [Contributing](#contributing) for now.


## A Practical Example

**TODO** Bash script that syncs issue labels in all of a user's projects with a master project.


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

 * ``gh labels list ‹repo›…``
 * ``gh labels export ‹repo› [to] ‹filename›``
 * ``gh labels import ‹repo› [from] ‹filename›``


## Contributing

To create a working directory for this project, call these commands:

```sh
git clone "https://github.com/jhermann/gh-commander.git"
cd "gh-commander"
. .env # answer the prompt with (y)es
invoke build --docs
```

See [CONTRIBUTING.md](https://github.com/jhermann/gh-commander/blob/master/CONTRIBUTING.md) for more.


## References

 * [GitHub API v3](https://developer.github.com/v3/)
 * [PyGithub](https://github.com/PyGithub/PyGithub)
 * [click](https://github.com/mitsuhiko/click)


## Acknowledgements

 * Logo elements from [clker.com Free Clipart](http://www.clker.com/).
