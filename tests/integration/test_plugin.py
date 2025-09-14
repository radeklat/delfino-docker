from types import ModuleType

import pytest
from delfino.click_utils.command import CommandRegistry
from delfino.models.pyproject_toml import PluginConfig

from delfino_docker import docker_build


@pytest.fixture(scope="session")
def plugin_config(pyproject_toml):
    return {pyproject_toml.project.name: PluginConfig.empty()}


@pytest.mark.usefixtures("build_and_install_plugin")
class TestPlugin:
    @staticmethod
    def test_should_be_discoverable_by_delfino(pyproject_toml, plugin_config):
        command_packages = CommandRegistry._discover_command_packages(plugin_config)
        assert len(command_packages) == 1
        plugin_names = {command_package.plugin_name for command_package in command_packages}
        assert pyproject_toml.project.name in plugin_names

        plugin_package = next(
            filter(
                lambda command_package: command_package.plugin_name == pyproject_toml.project.name, command_packages
            ),
            None,
        )
        assert plugin_package
        assert isinstance(plugin_package.package, ModuleType)
        assert isinstance(plugin_package.package.__package__, str)
        assert pyproject_toml.project.name.replace("-", "_") in plugin_package.package.__package__

    @staticmethod
    def test_should_be_visible_in_delfino(plugin_config):
        command_registry = CommandRegistry(plugin_config, CommandRegistry._discover_command_packages(plugin_config))
        assert docker_build.name in {command.name for command in command_registry.visible_commands}
