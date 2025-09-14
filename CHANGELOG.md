# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
Types of changes are:

- **Breaking changes** for breaking changes.
- **Features** for new features or changes in existing functionality.
- **Fixes** for any bug fixes.
- **Deprecated** for soon-to-be removed features.

## [Unreleased]

## [5.0.0] - 2025-09-14

### Breaking changes

- Drop support for Python 3.8 and 3.9.
- Bump minimum supported `delfino` version from 3.0 to 5.0.

### Features

- Add support for Python 3.13.
- Add support for `uv` / PEP 621.

## [4.0.1] - 2023-10-12

### Fixes

- Dependencies update.

## [4.0.0] - 2023-09-15

### Breaking changes

- Upgrade from `pydantic` 1.x to 2.x.

### Fixes

- Dependencies update.
- Update parameters deprecated in `pydantic` 2.x.

## [3.0.0] - 2023-06-25

### Breaking changes

- Drops Python 3.7 support.

### Fixes

- Pass full Python version to `Dockerfile` if available.

## [2.0.0] - 2022-12-29

### Breaking changes

- Renamed command from `build-docker` to `docker-build`.
- Renamed config option from `dockerhub` to `docker_build`.
- Renamed config option key from `username` to `dockerhub_username`.

### Fixes

- Add missing dependency on `packaging`.

## [1.1.0] - 2022-12-29

### Features

- Port `docker-build` command from [`delfino-core`](https://github.com/radeklat/delfino-core).

## [1.0.0] - 2022-12-29

### Features

- Initial source code

[Unreleased]: https://github.com/radeklat/delfino-docker/compare/5.0.0...HEAD
[5.0.0]: https://github.com/radeklat/delfino-docker/compare/4.0.1...5.0.0
[4.0.1]: https://github.com/radeklat/delfino-docker/compare/4.0.0...4.0.1
[4.0.0]: https://github.com/radeklat/delfino-docker/compare/3.0.0...4.0.0
[3.0.0]: https://github.com/radeklat/delfino-docker/compare/2.0.1...3.0.0
[2.0.1]: https://github.com/radeklat/delfino-docker/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/radeklat/delfino-docker/compare/1.1.0...2.0.0
[1.1.0]: https://github.com/radeklat/delfino-docker/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/radeklat/delfino-docker/compare/initial...1.0.0
