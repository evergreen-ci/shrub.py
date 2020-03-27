"""Shrub configuration for an evergreen build variant."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import Any, Dict, Optional, Set, FrozenSet, Sequence, List

from shrub.v2.task import Task, TaskGroup, RunnableTask, RunnableTaskSet


@dataclass(frozen=True)
class _DisplayTask(object):
    """Representation of a Display Task."""

    display_name: str
    execution_tasks: FrozenSet[Task]

    def as_dict(self) -> Dict[str, Any]:
        """Get a dictionary of this display task."""
        return {
            "name": self.display_name,
            "execution_tasks": sorted([task.name for task in self.execution_tasks]),
        }


class BuildVariant(object):
    """Representation of a Build Variant."""

    def __init__(
        self,
        name: str,
        display_name: Optional[str] = None,
        batch_time: Optional[int] = None,
        expansions: Dict[str, Any] = None,
    ) -> None:
        """
        Create a new build variant.

        :param name: Name of build variant.
        :param display_name: Display name of build variant.
        :param batch_time: Interval of time in minutes that evergreen should wait before activating
            this variant.
        :param expansions: A set of key-value expansions pairs.
        """
        self.name = name
        self.display_name = display_name if display_name else name
        self.batch_time = batch_time
        self.tasks: Set[Task] = set()
        self.task_groups: Set[TaskGroup] = set()
        self.display_tasks: Set[_DisplayTask] = set()
        self.expansions: Dict[str, Any] = expansions if expansions else {}
        self.task_to_distro_map: Dict[str, Sequence[str]] = {}

    def add_task(self, task: Task, distros: Optional[Sequence[str]] = None) -> BuildVariant:
        """
        Add the given task to this build variant.

        :param task: Task to add to build variant.
        :param distros: Distros to run task on.
        :return: This build variant.
        """
        self.tasks.add(task)
        if distros:
            self.task_to_distro_map[task.name] = distros
        return self

    def add_tasks(
        self, task_set: Set[Task], distros: Optional[Sequence[str]] = None
    ) -> BuildVariant:
        """
        Add the given set of tasks to this build variant.

        :param task_set: Set of tasks to add to build variant.
        :param distros: Distros to run task on.
        :return: This build variant.
        """
        self.tasks.update(task_set)
        if distros:
            for task in task_set:
                self.task_to_distro_map[task.name] = distros
        return self

    def add_task_group(
        self, task_group: TaskGroup, distros: Optional[Sequence[str]] = None
    ) -> BuildVariant:
        """
        Add the given task group to the set of tasks in this build variant.

        :param task_group: Task group to add to build variant.
        :param distros: Distros to run task group on.
        :return: This build variant.
        """
        self.task_groups.add(task_group)
        if distros:
            self.task_to_distro_map[task_group.name] = distros
        return self

    def add_task_groups(
        self, task_group_set: Set[TaskGroup], distros: Optional[Sequence[str]] = None
    ) -> BuildVariant:
        """
        Add the given set of task groups to this build variant.

        :param task_group_set: Set of task groups to add to build variant.
        :param distros: Distros to run task on.
        :return: This build variant.
        """
        self.task_groups.update(task_group_set)
        if distros:
            for task_group in task_group_set:
                self.task_to_distro_map[task_group.name] = distros
        return self

    def display_task(self, display_name: str, execution_tasks: Set[Task]) -> BuildVariant:
        """
        Add a new display task to this build variant.

        :param display_name: Name of display task.
        :param execution_tasks: Set of tasks that should be part of the display task.
        :return: This build variant configuration.
        """
        self.tasks.update(execution_tasks)
        self.display_tasks.add(_DisplayTask(display_name, frozenset(execution_tasks)))
        return self

    def all_tasks(self) -> Set[Task]:
        """Get a set of all tasks that are part of this build variant."""
        tasks = self.tasks
        tg_tasks = [set(tg.tasks) for tg in self.task_groups]
        return tasks.union(chain.from_iterable(tg_tasks))

    def __task_spec_for_task(self, task: RunnableTask) -> Dict[str, Any]:
        """
        Create a task spec to run the given task on this variant.

        :param task: Task to run.
        :return: Task spec for running task.
        """
        return task.task_spec(self.task_to_distro_map.get(task.name))

    def __get_task_specs(self, task_list: RunnableTaskSet) -> List[Dict[str, Any]]:
        """
        Get a dictionary representation of task specs for the tasks given.

        :param task_list: List of tasks or task groups.
        :return: Dictionary representation of task specs for given list.
        """
        return sorted([self.__task_spec_for_task(t) for t in task_list], key=lambda t: t["name"])

    def as_dict(self) -> Dict[str, Any]:
        """Get the dictionary representation of this build variant."""
        obj: Dict[str, Any] = {
            "name": self.name,
            "tasks": self.__get_task_specs(self.tasks) + self.__get_task_specs(self.task_groups),
        }
        if self.display_tasks:
            obj["display_tasks"] = sorted(
                [dt.as_dict() for dt in self.display_tasks], key=lambda d: d["name"]
            )
        if self.expansions:
            obj["expansions"] = self.expansions

        return obj
