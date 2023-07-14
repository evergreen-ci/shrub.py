"""Evergreen configuration models for build variants."""
from typing import List, Optional, Dict

from pydantic import BaseModel

from shrub.v3.evg_task import EvgTaskRef


class DisplayTask(BaseModel):
    """
    A display task groups several tasks under a single visual task.

    * name: Name of display task.
    * execution_tasks: List of tasks to group under the display task.
    """

    name: str
    execution_tasks: List[str]


class BuildVariant(BaseModel):
    """
    Build variant is a configuration to run a set to tests run.

    * name: ID of build variant.
    * tasks: List of tasks to run on this build variant.
    * display_name: Name of build variant.
    * run_on: Distros that tasks should be run on.
    * display_tasks: Display tasks that are part of the build variant.
    * batchtime: How frequent this build variant should be run.
    * cron: What cron schedule this build variant should run on.
    * expansions: Definition of expansions for this build variant.
    * stepback: If stepback should be run on this build variant.
    * module: List of modules to include in this build variant.
    """

    name: str
    tasks: List[EvgTaskRef]
    display_name: Optional[str] = None
    run_on: Optional[List[str]] = None
    display_tasks: Optional[List[DisplayTask]] = None
    batchtime: Optional[int] = None
    cron: Optional[str] = None
    expansions: Optional[Dict[str, str]] = None
    stepback: Optional[bool] = None
    modules: Optional[List[str]] = None
    tags: Optional[List[str]] = None
