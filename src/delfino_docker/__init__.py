from getpass import getpass
from os import getenv
from pathlib import Path

import click
from delfino.constants import PackageManager
from delfino.execution import OnError, run
from delfino.models import AppContext, PyprojectToml
from delfino.terminal_output import print_header
from delfino.utils import ArgsList
from delfino.validation import assert_package_manager_is_known, assert_pip_package_installed, pyproject_toml_key_missing

from delfino_docker.config import Dockerhub, DockerPluginConfig, pass_plugin_app_context

try:
    from packaging.version import Version
except ImportError:
    pass


def _install_emulators(build_for_platforms: list[str]) -> None:
    """See https://github.com/tonistiigi/binfmt#installing-emulators."""
    emulators = []
    if "linux/arm64" in build_for_platforms:
        emulators.append("arm64")
    if "linux/arm/v7" in build_for_platforms:
        emulators.append("arm")

    if emulators:
        print_header("Installing emulators", level=2, icon="⬇")
        run(
            ["docker", "run", "--privileged", "--rm", "tonistiigi/binfmt", "--install", *emulators],
            on_error=OnError.EXIT,
        )


def _docker_build(
    project_name: str,
    dockerhub: Dockerhub,
    flags: ArgsList,
    platform: str,
    tag: str = "latest",
    push: bool = False,
):
    _flags = list(flags)
    _flags.extend(["--platform", platform])
    if tag != "latest" and push:
        _flags.extend(["--cache-to", f"type=registry,ref={dockerhub.dockerhub_username}/{project_name}"])

    run(
        [
            "docker",
            "buildx",
            "build",
            "--cache-from",
            f"type=registry,ref={dockerhub.dockerhub_username}/{project_name}",
            "--tag",
            f"{dockerhub.dockerhub_username}/{project_name}:{tag}",
            *_flags,
            ".",
        ],
        on_error=OnError.EXIT,
    )


def _get_python_version_from_pyproject(pyproject_toml: PyprojectToml, package_manager: PackageManager) -> str:
    if (
        (python_version := pyproject_toml.project.model_extra.get("requires-python", None)) is None
        and package_manager == PackageManager.POETRY
        and pyproject_toml.tool.poetry
    ):
        python_version = pyproject_toml.tool.poetry.dependencies.get("python", None)

    assert python_version, "Python version is not set in pyproject.toml"

    cleaned_version = python_version.split(",")[0].strip("<>=~^! ")
    return Version(cleaned_version).public


@click.command()
@click.option(
    "--push",
    is_flag=True,
    help="Push the built image and cache to remote docker image registry. Login is "
    "required and Personal Access Token will be requested from STDIN if "
    "`DOCKERHUB_PERSONAL_ACCESS_TOKEN` environment variable is not set.",
)
@click.option("--serialized", is_flag=True, help="Do not build multiple platforms concurrently.")
@pass_plugin_app_context
def docker_build(app_context: AppContext[DockerPluginConfig], push: bool, serialized: bool):
    """Build and push a docker image."""
    plugin_config = app_context.plugin_config
    dockerfile = Path("Dockerfile")

    assert_package_manager_is_known(app_context.package_manager)
    assert_pip_package_installed("packaging")
    assert dockerfile.exists() and dockerfile.is_file(), "File 'Dockerfile' not found but required by this command."
    assert plugin_config.docker_build, pyproject_toml_key_missing("tool.delfino-docker.docker_build")

    project_name = app_context.pyproject_toml.project_name
    project_version = app_context.pyproject_toml.project_version
    assert project_name, "Project name is not set in pyproject.toml"
    assert project_version, "Project version is not set in pyproject.toml"

    python_version = _get_python_version_from_pyproject(app_context.pyproject_toml, app_context.package_manager)

    print_header("Running Docker build")

    flags: ArgsList = []

    flags.extend(["--build-arg", f"PYTHON_VERSION={python_version}"])

    command_config = plugin_config.docker_build

    if push:
        dockerhub_password = getenv("DOCKERHUB_PERSONAL_ACCESS_TOKEN")
        if not dockerhub_password:
            click.secho("⚠ The 'DOCKERHUB_PERSONAL_ACCESS_TOKEN' environment variable is not set.", fg="yellow")
            dockerhub_password = getpass("Dockerhub Personal Access Token: ")
        run(
            f"docker login --username {command_config.dockerhub_username} --password {dockerhub_password}",
            on_error=OnError.EXIT,
        )

    if getenv("CI"):  # https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables
        flags.extend(["--progress", "plain"])

    joined_build_platforms = ",".join(command_config.build_for_platforms)
    if serialized:
        build_platforms: list[str] = command_config.build_for_platforms
    else:
        build_platforms = [joined_build_platforms]
        _install_emulators(command_config.build_for_platforms)

    # If serialized build is selected, run build individually. Results are cached so the second
    # build below will only push and not build again.
    for platform in build_platforms:
        if serialized:
            _install_emulators([platform])
        print_header(
            f"Build {command_config.dockerhub_username}/{project_name}:latest for {platform}", level=2, icon="🔨"
        )
        _docker_build(project_name, command_config, flags, platform)

    if not push:
        return

    flags.extend(["--output", "type=image,push=true"])

    # While `docker buildx build` supports multiple `--tag` flags, push of them fails to expose
    # all architectures in `latest`. Multiple pushes fix this.
    for tag in [project_version, "latest"]:
        print_header(f"Push {command_config.dockerhub_username}/{project_name}:{tag}", level=2, icon="🔨")
        _docker_build(project_name, command_config, flags, joined_build_platforms, tag, push)

    run("docker logout", on_error=OnError.EXIT)
