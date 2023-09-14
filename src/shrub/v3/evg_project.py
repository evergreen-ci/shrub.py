"""Evergreen configuration models for projects."""
from __future__ import annotations

import re
from typing import List, Optional, Dict, Union

import yaml
from pydantic import BaseModel

from shrub.v3.evg_build_variant import BuildVariant
from shrub.v3.evg_command import EvgCommandType, EvgCommand
from shrub.v3.evg_task import EvgTask
from shrub.v3.evg_task_group import EvgTaskGroup

REPO_NAME_REGEX = re.compile(r"[/|:](?P<repo_name>[\w\-.]+?)(\.git|/)?$")


class EvgParameter(BaseModel):
    """
    A parameter that can be updated by users for a patch build.

    * key: Name of parameter.
    * value: Default value for parameter.
    * description: Documentation for what the parameter does.
    """

    key: str
    value: Optional[str]
    description: str


class EvgModule(BaseModel):
    """
    An evergreen module that can be included in the project.

    * name: Name to reference the module.
    * repo: Repository containing the module code.
    * branch: Branch of repository to use.
    * prefix: Directory to place module.
    """

    name: str
    repo: str
    branch: str
    prefix: str

    def get_repository_name(self) -> Optional[str]:
        """Get the repository name of the module."""
        match = REPO_NAME_REGEX.search(self.repo)
        if match:
            return match.groupdict().get("repo_name")
        return None


FunctionDefinition = Union[EvgCommand, List[EvgCommand]]


class EvgProject(BaseModel):
    """
    Configuration for an evergreen project.

    * buildvariants: List of build variant configurations for project.
    * tasks: List of task definitions for project.
    * task_groups: List of task group definitions for project.
    * functions: Definition of functions used in the project.
    * pre: List of commands to run at the start of every task.
    * post: List of commands to run at the end of every task.
    * timeout: List of commands to run if a task times out.
    * modules: Definition of modules to use in the project.
    * stepback: Whether stepback should be used.
    * pre_error_fails_task: Whether an error running pre commands should cause task to fail.
    * oom_tracker: Whether Out of Memory errors should be tracked.
    * command_type: How failures should be represented by default.
    * ignore: List of files that should not trigger tests to run.
    * parameters: Definition of available patch build parameters for the project.
    """

    buildvariants: Optional[List[BuildVariant]]
    tasks: Optional[List[EvgTask]]
    functions: Optional[Dict[str, FunctionDefinition]] = None
    task_groups: Optional[List[EvgTaskGroup]] = None
    pre: Optional[List[EvgCommand]] = None
    post: Optional[List[EvgCommand]] = None
    timeout: Optional[List[EvgCommand]] = None
    modules: Optional[List[EvgModule]] = None
    stepback: Optional[bool] = None
    pre_error_fails_task: Optional[bool] = None
    oom_tracker: Optional[bool] = None
    command_type: Optional[EvgCommandType] = None
    ignore: Optional[List[str]] = None
    parameters: Optional[List[EvgParameter]] = None

    @classmethod
    def from_file(cls, file_location: str) -> EvgProject:
        """Read and parse the evergreen configuration of the given file."""
        with open(file_location) as contents:
            return cls(**yaml.safe_load(contents))
