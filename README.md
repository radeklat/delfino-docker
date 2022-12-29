<h1 align="center" style="border-bottom: none;"> 🔌&nbsp;&nbsp;Delfino Docker&nbsp;&nbsp; 🔌</h1>
<h3 align="center">A delfino plugin with helper scripts for working with docker.</h3>

<p align="center">
    <a href="https://app.circleci.com/pipelines/github/radeklat/delfino-docker?branch=main">
        <img alt="CircleCI" src="https://img.shields.io/circleci/build/github/radeklat/delfino-docker">
    </a>
    <a href="https://app.codecov.io/gh/radeklat/delfino-core/">
        <img alt="Codecov" src="https://img.shields.io/codecov/c/github/radeklat/delfino-docker">
    </a>
    <a href="https://github.com/radeklat/delfino-core/tags">
        <img alt="GitHub tag (latest SemVer)" src="https://img.shields.io/github/tag/radeklat/delfino-docker">
    </a>
    <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2022">
    <a href="https://github.com/radeklat/delfino-docker/commits/main">
        <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/radeklat/delfino-docker">
    </a>
    <a href="https://www.python.org/doc/versions/">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/delfino-docker">
    </a>
    <a href="https://pypistats.org/packages/delfino-docker">
        <img alt="Downloads" src="https://img.shields.io/pypi/dm/delfino-docker">
    </a>
</p>

# Commands
  
| Command               | Description             |
|-----------------------|-------------------------|
| demo                  | An example demo command |

# Installation

- pip: `pip install delfino-docker`
- Poetry: `poetry add -D delfino-docker`
- Pipenv: `pipenv install -d delfino-docker`

<!-- PUT DEPENDENCIES OF INDIVIDUAL COMMANDS AS EXTRAS -->
<!--
## Optional dependencies

Each project may use different sub-set of [commands](#commands). Therefore, dependencies of all commands are optional and checked only when the command is executed.

Using `[all]` installs all the [optional dependencies](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies) used by all the commands. If you want only a sub-set of those dependencies, there are finer-grained groups available:

- `demo`
-->

# Configuration

Delfino doesn't load any plugins by default. To enable this plugin, add the following config into `pyproject.toml`:

```toml
[tool.delfino.plugins.delfino-docker]

```

<!-- PLUGIN MAY NEED CONFIGURATION -->
<!--
## Plugin configuration

This plugin has several options. All the values are optional and defaults are shown below: 

```toml
[tool.delfino.plugins.delfino-docker]
# Config option description
config_option_name = "default value"
```
-->

<!-- INDIVIDUAL COMMANDS MAY NEED CONFIGURATION -->
<!--
## Commands configuration

Several commands have their own configuration as well:

```toml
[tool.delfino.plugins.delfino-docker.demo]
# Config option description
config_option_name = "default value"
```
-->

# Usage

Run `delfino --help`.
