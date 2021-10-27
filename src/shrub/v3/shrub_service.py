"""Service for working with shrub."""
import yaml
from pydantic import BaseModel


class ShrubService:
    """A service for working with shrub."""

    @staticmethod
    def generate_yaml(shrub_config: BaseModel) -> str:
        """
        Generate a yaml version of the given configuration.

        :param shrub_config: Shrub configuration to generate.
        :return: YAML version of given shrub configuration.
        """
        return yaml.safe_dump(
            shrub_config.dict(exclude_none=True, exclude_unset=True, by_alias=True)
        )

    @staticmethod
    def generate_json(shrub_config: BaseModel) -> str:
        """
        Generate a json version of the given configuration.

        :param shrub_config: Shrub configuration to generate.
        :return: JSON version of given shrub configuration.
        """
        return shrub_config.json(exclude_none=True, exclude_unset=True, by_alias=True)
