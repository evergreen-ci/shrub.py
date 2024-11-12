"""Evergreen configuration models for task groups."""
from typing import List, Optional

from pydantic import BaseModel

from shrub.v3.evg_command import EvgCommand
from shrub.v3.evg_task import EvgTaskRef


class EvgTaskGroup(BaseModel):
    """
    A group of tasks that share certain properties.

    * name: Name of task group.
    * tasks: List of tasks that belong to the task group.
    * max_hosts: Max number of hosts to run the tasks in the group on.
    * share_processes: If true, host is not cleaned up between task executions.
    * setup_group_can_fail_task: Whether a task group setup failure should make a task fail.
    * setup_group_timeout_secs: Time to wait until task group setup commands are stopped.
    * setup_group: List of commands to run before any task is run.
    * teardown_group_timeout_secs: Time to wait until task group teardown commands are stopped.
    * teardown_group: List of commands to run after tasks finish on a host.
    * setup_task_can_fail_task: Whether a task setup failure should make a task fail.
    * setup_task_timeout_secs: Time to wait until setup commands are stopped.
    * setup_task: List of commands to run before a task is run.
    * teardown_task_can_fail_task: Whether a task teardown failure should make a task fail.
    * teardown_task_timeout_secs: Time to wait until teardown commands are stopped.
    * teardown_task: List of commands to run after a task is run.
    * timeout: List of commands to run when a timeout is encountered.
    * tags: Tags that should be applied to the task group.
    """

    name: str
    tasks: List[str]
    max_hosts: Optional[int] = None
    share_processes: Optional[bool] = None
    setup_group_can_fail_task: Optional[bool] = None
    setup_group_timeout_secs: Optional[int] = None
    setup_group: Optional[List[EvgCommand]] = None
    teardown_group_timeout_secs: Optional[int] = None
    teardown_group: Optional[List[EvgCommand]] = None
    setup_task_can_fail_task: Optional[bool] = None
    setup_task_timeout_secs: Optional[int] = None
    setup_task: Optional[List[EvgCommand]] = None
    teardown_task_can_fail_task: Optional[bool] = None
    teardown_task_timeout_secs: Optional[int] = None
    teardown_task: Optional[List[EvgCommand]] = None
    timeout: Optional[List[EvgCommand]] = None
    tags: Optional[List[str]] = None

    def get_task_ref(self, distros: Optional[List[str]] = None) -> EvgTaskRef:
        """
        Get a reference to this task group.

        :param distros: List of distros this task should be run on.
        :return: Reference to this task group.
        """
        return EvgTaskRef(name=self.name, distros=distros)
