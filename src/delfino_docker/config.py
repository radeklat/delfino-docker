from typing import List, Optional

from delfino.decorators import pass_app_context
from delfino.models.pyproject_toml import PluginConfig
from pydantic import BaseModel, Field


class Dockerhub(BaseModel):
    build_for_platforms: List[str] = Field(["linux/amd64", "linux/arm64", "linux/arm/v7"], min_items=1)
    dockerhub_username: str


class DockerPluginConfig(PluginConfig):
    docker_build: Optional[Dockerhub] = None


pass_plugin_app_context = pass_app_context(plugin_config_type=DockerPluginConfig)
