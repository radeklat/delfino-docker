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

## [2.0.1] - 2022-12-30

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

[Unreleased]: https://github.com/radeklat/delfino-docker/compare/2.0.1...HEAD
[2.0.1]: https://github.com/radeklat/delfino-docker/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/radeklat/delfino-docker/compare/1.1.0...2.0.0
[1.1.0]: https://github.com/radeklat/delfino-docker/compare/1.0.0...1.1.0
[1.0.0]: https://github.com/radeklat/delfino-docker/compare/initial...1.0.0
