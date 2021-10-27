"""Evergreen models for tasks."""
from typing import List, Optional

from pydantic import BaseModel

from shrub.v3.evg_command import EvgCommand


class EvgTaskDependency(BaseModel):
    """
    Specification of what a task depends on.

    * name: Name of task to depend on.
    * variant: Name of build variant depending task should run on.
    """

    name: str
    variant: Optional[str] = None


class EvgTaskRef(BaseModel):
    """
    Reference to an evergreen task.

    * name: Name of task.
    * distros: Distro that task should be run on.
    """

    name: str
    distros: Optional[List[str]] = None


class EvgTask(BaseModel):
    """
    Definition of a task.

    * name: Name of task.
    * commands: List of commands that make up task.
    * depends_on: Other tasks that must be successful for this task to run.
    * exec_timeout_secs: Time task can run before being considered timing out.
    * tags: List of tags to attach to task.
    * patchable: Whether this task can run in patch builds.
    * stepback: Whether this task should run stepback.
    """

    name: str
    commands: Optional[List[EvgCommand]] = None
    depends_on: Optional[List[EvgTaskDependency]] = None
    exec_timeout_secs: Optional[int] = None
    tags: Optional[List[str]] = None
    patchable: Optional[bool] = None
    stepback: Optional[bool] = None

    def get_task_ref(self, distros: Optional[List[str]] = None) -> EvgTaskRef:
        """
        Get a reference to this task.

        :param distros: List of distros this task should be run on.
        :return: Reference to this task.
        """
        return EvgTaskRef(name=self.name, distros=distros)
