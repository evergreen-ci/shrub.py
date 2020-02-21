"""Configuration for tasks in evergreen."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence, Set, Union

from shrub.v2.command import ShrubCommand
from shrub.v2.dict_creation_util import add_if_exists, add_existing_from_dict


@dataclass(frozen=True)
class TaskDependency(object):
    """A dependency on another task."""

    task_name: str
    build_variant: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        """Convert the dependency to a dictionary."""
        obj = {
            "name": self.task_name,
        }
        add_if_exists(obj, "variant", self.build_variant)

        return obj


class Task(object):
    """A representation of an evergreen task."""

    def __init__(
        self,
        name: str,
        commands: Sequence[ShrubCommand],
        dependencies: Optional[Set[TaskDependency]] = None,
    ) -> None:
        """
        Create a new evergreen task.

        :param name: Name of task.
        :param commands: List of commands comprising the task.
        :param dependencies: Any dependencies the task has.
        """
        self.name = name
        self.commands = commands
        self.dependencies = dependencies if dependencies else set()

    def dependency(self, task_name: str, build_variant: Optional[str] = None) -> Task:
        """
        Add a dependency on the task.

        :param task_name: Name of task to depend on.
        :param build_variant: Name of build variant to where dependent task is run.
        :return: this task.
        """
        self.dependencies.add(TaskDependency(task_name, build_variant))
        return self

    def task_spec(self, distros: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        """
        Create a task spec for this task.

        A task spec describes how the task should be added to a build variant.

        :param distros: What distros the task should run on.
        :return: Dictionary representing task spec.
        """
        obj: Dict[str, Any] = {
            "name": self.name,
        }
        add_if_exists(obj, "distros", distros)

        return obj

    def as_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of this task."""
        obj = {
            "name": self.name,
            "commands": [cmd.as_dict() for cmd in self.commands],
        }

        if self.dependencies:
            obj["depends_on"] = [dep.as_dict() for dep in self.dependencies]

        return obj


class TaskGroup(object):
    """A representation of an evergreen task group."""

    def __init__(
        self,
        name: str,
        tasks: Sequence[Task],
        max_hosts: Optional[int] = None,
        setup_group: Optional[Sequence[ShrubCommand]] = None,
        setup_task: Optional[Sequence[ShrubCommand]] = None,
        teardown_group: Optional[Sequence[ShrubCommand]] = None,
        teardown_task: Optional[Sequence[ShrubCommand]] = None,
        setup_group_can_fail_task: Optional[bool] = None,
        setup_group_timeout_secs: Optional[int] = None,
    ) -> None:
        """
        Create a new task group.

        :param name: Name of task group.
        :param tasks: List of tasks comprising task group.
        :param max_hosts: Number of hosts across which to distribute the tasks in this group.
        """
        self.name = name
        self.tasks = tasks
        self.max_hosts = max_hosts
        self.setup_group = setup_group
        self.setup_task = setup_task
        self.teardown_group = teardown_group
        self.teardown_task = teardown_task
        self.setup_group_can_fail_task = setup_group_can_fail_task
        self.setup_group_timeout_secs = setup_group_timeout_secs

    def task_spec(self, distros: Optional[Sequence[str]] = None) -> Dict[str, Any]:
        """
        Create a task spec for this task group.

        A task spec describes how the task should be added to a build variant.

        :param distros: What distros the task should run on.
        :return: Dictionary representing task spec.
        """
        obj: Dict[str, Any] = {
            "name": self.name,
        }
        add_if_exists(obj, "distros", distros)

        return obj

    @staticmethod
    def __cmd_list_as_dict(cmd_list: Optional[Sequence[ShrubCommand]]) -> Optional[Sequence[Dict]]:
        """
        Convert a list of commands into a dictionary representation.

        :param cmd_list: List of commands to convert.
        :return: Dictionary version of command list.
        """
        if cmd_list:
            return [c.as_dict() for c in cmd_list]
        return None

    def as_dict(self) -> Dict[str, Any]:
        """Get a dictionary representation of this task group."""
        obj = {"name": self.name, "tasks": sorted([task.name for task in self.tasks])}
        add_existing_from_dict(
            obj,
            {
                "max_hosts": self.max_hosts,
                "setup_group": self.__cmd_list_as_dict(self.setup_group),
                "setup_task": self.__cmd_list_as_dict(self.setup_task),
                "teardown_group": self.__cmd_list_as_dict(self.teardown_group),
                "teardown_task": self.__cmd_list_as_dict(self.teardown_task),
                "setup_group_can_fail_task": self.setup_group_can_fail_task,
                "setup_group_timeout_secs": self.setup_group_timeout_secs,
            },
        )

        return obj


RunnableTask = Union[Task, TaskGroup]
RunnableTaskSet = Union[Set[Task], Set[TaskGroup]]
