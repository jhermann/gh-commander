# gh-commander

GitHub Commander is a tool to access the GitHub APIv3 from the CLI and automate otherwise tedious tasks.

 [![Travis CI](https://api.travis-ci.org/jhermann/gh-commander.svg)](https://travis-ci.org/jhermann/gh-commander)
 [![Coveralls](https://img.shields.io/coveralls/jhermann/gh-commander.svg)](https://coveralls.io/r/jhermann/gh-commander)
 [![GitHub Issues](https://img.shields.io/github/issues/jhermann/gh-commander.svg)](https://github.com/jhermann/gh-commander/issues)
 [![License](https://img.shields.io/pypi/l/gh-commander.svg)](https://github.com/jhermann/gh-commander/blob/master/LICENSE)
 [![Development Status](https://pypip.in/status/gh-commander/badge.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Latest Version](https://img.shields.io/pypi/v/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Download format](https://pypip.in/format/gh-commander/badge.svg)](https://pypi.python.org/pypi/gh-commander/)
 [![Downloads](https://img.shields.io/pypi/dw/gh-commander.svg)](https://pypi.python.org/pypi/gh-commander/)


## Overview

…


## Installation

*GH Commander* can be installed via ``pip install gh-commander`` as usual,
see [releases](https://github.com/jhermann/gh-commander/releases) for an overview of available versions.
To get a bleeding-edge version from source, use these commands:

```sh
repo="jhermann/gh-commander"
pip install -r "https://raw.githubusercontent.com/$repo/master/requirements.txt"
pip install -UI -e "git+https://github.com/$repo.git#egg=${repo#*/}"
```

See [Contributing](#contributing) on how to create a full development environment.

To add bash completion, read the [Click docs](http://click.pocoo.org/4/bashcomplete/#activation) about it,
or just follow these instructions:

```sh
cmdname=gh-commander
mkdir -p ~/.bash_completion.d
( export _$(tr a-z- A-Z_ <<<"$cmdname")_COMPLETE=source ; \
  $cmdname >~/.bash_completion.d/$cmdname.sh )
grep /.bash_completion.d/$cmdname.sh ~/.bash_completion >/dev/null \
    || echo >>~/.bash_completion ". ~/.bash_completion.d/$cmdname.sh"
. "/etc/bash_completion"
```


## Usage

…


## Contributing

To create a working directory for this project, call these commands:

```sh
git clone "https://github.com/jhermann/gh-commander.git"
cd "gh-commander"
. .env --yes --develop
invoke build --docs test check
```

See [CONTRIBUTING](https://github.com/jhermann/gh-commander/blob/master/CONTRIBUTING.md) for more.


## References

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

* [Rituals](https://jhermann.github.io/rituals)
* [Click](http://click.pocoo.org/)


## Acknowledgements

…
