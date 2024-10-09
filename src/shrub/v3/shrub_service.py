"""Service for working with shrub."""

import yaml
from pydantic import BaseModel


class ConfigDumper(yaml.SafeDumper):
    # The max number of tags to flow.
    FLOW_TAG_COUNT = 3

    # Represent multiline strings in the form:
    #     key: |
    #       multiline string
    #       multiline string
    #       multiline string
    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and "\n" in value:
            style = "|"
        return super().represent_scalar(tag, value, style)

    # Prefer using double quotes when able.
    def analyze_scalar(self, scalar):
        res = super().analyze_scalar(scalar)
        if res.allow_single_quoted and res.allow_double_quoted:
            res.allow_single_quoted = False
        return res

    # Represent flow mappings with space after left brace:
    #     node: { key: value }
    #            ^
    def expect_flow_mapping(self):
        super().expect_flow_mapping()
        self.write_indicator("", False)

    # Represent flow mappings with space before right brace:
    #     node: { key: value }
    #                       ^
    def expect_flow_mapping_key(self):
        if isinstance(self.event, yaml.MappingEndEvent):
            self.write_indicator(" ", False)
        super().expect_flow_mapping_key()

    # Allow for special-casing depending on parent node.
    def represent_special_mapping(self, tag, mapping, flow_style):
        value = []

        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)

            if item_key == "tags" and len(item_value) <= self.FLOW_TAG_COUNT:
                # Represent task tags using flow style to reduce line count:
                #     - name: task-name
                #       tags: [A, B, C]
                node_value = self.represent_sequence(
                    "tag:yaml.org,2002:seq", item_value, flow_style=True
                )
            elif item_key == "depends_on" and len(item_value) == 1:
                # Represent task depends_on using flow style when only one
                # dependency is given to reduce line count:
                #     - name: task-name
                #       depends_on: [{ name: dependency }]
                node_value = self.represent_sequence(
                    "tag:yaml.org,2002:seq", item_value, flow_style=True
                )
            else:
                # Use default behavior.
                node_value = self.represent_data(item_value)

            value.append((node_key, node_value))

        node = yaml.MappingNode(tag, value, flow_style=flow_style)

        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node

        return node

    # Represent updates mapping for expansions.update commands using flow
    # style to reduce line count:
    #    - command: expansions.update
    #      params:
    #        updates:
    #          - { key: KEY, value: VALUE }
    #          - { key: KEY, value: VALUE }
    #          - { key: KEY, value: VALUE }
    def represent_mapping(self, tag, mapping, flow_style=False):
        if len(mapping) == 2 and "key" in mapping and "value" in mapping:
            flow_style = True

        return self.represent_special_mapping(tag, mapping.items(), flow_style)

    # Ensure a block sequence is indented relative to its parent node::
    #     key:
    #       - a
    #       - b
    #       - c
    # instead of::
    #     key:
    #     - a
    #     - b
    #     - c
    def increase_indent(self, flow=None, indentless=None):
        indentless = False
        return super().increase_indent(flow=flow, indentless=indentless)


class ShrubService:
    """A service for working with shrub."""

    @staticmethod
    def generate_yaml(shrub_config: BaseModel) -> str:
        """
        Generate a yaml version of the given configuration.

        :param shrub_config: Shrub configuration to generate.
        :return: YAML version of given shrub configuration.
        """
        return yaml.dump(
            shrub_config.dict(exclude_none=True, exclude_unset=True, by_alias=True),
            Dumper=ConfigDumper,
            default_flow_style=False,
            width=float("inf"),
        )

    @staticmethod
    def generate_json(shrub_config: BaseModel) -> str:
        """
        Generate a json version of the given configuration.

        :param shrub_config: Shrub configuration to generate.
        :return: JSON version of given shrub configuration.
        """
        return shrub_config.json(exclude_none=True, exclude_unset=True, by_alias=True)
