from delfino.decorators import pass_app_context
from delfino.models.pyproject_toml import PluginConfig
from pydantic import BaseModel, Field


class Dockerhub(BaseModel):
    build_for_platforms: list[str] = Field(["linux/amd64", "linux/arm64", "linux/arm/v7"], min_length=1)
    dockerhub_username: str


class DockerPluginConfig(PluginConfig):
    docker_build: Dockerhub | None = None


pass_plugin_app_context = pass_app_context(plugin_config_type=DockerPluginConfig)
