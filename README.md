# gh-commander

GitHub Commander is a tool to access the
[GitHub API v3](https://developer.github.com/v3/)
from the CLI and automate otherwise tedious tasks.

![Apache 2.0 licensed](http://img.shields.io/badge/license-Apache_2.0-red.svg)
[![Travis CI](https://api.travis-ci.org/jhermann/gh-commander.svg)](https://travis-ci.org/jhermann/gh-commander)


## Overview

GitHub Commander implements the ``gh`` command line tool,
which provides a ‘fluent’ interface
using [click](https://github.com/mitsuhiko/click)
(see [Usage](#usage) below).
It allows to access the
[GitHub API v3](https://developer.github.com/v3/)
from a shell prompt for things usually done in the browser,
and also automates otherwise tasks that are tedious at best,
when done by clicking around on a web page.
GitHub Commander is powered by [PyGithub](https://github.com/PyGithub/PyGithub).

:information_source: | Initially, the focus of the project will be to provide task automation, not completeness of covering every API aspect!
---- | :----


## Installation

See [Contributing](#contributing) for now.


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

…
