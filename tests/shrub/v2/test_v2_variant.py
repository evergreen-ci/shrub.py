"""Unit tests for shrub.v2.variant."""
from itertools import chain

from shrub.v2 import Task, TaskGroup, ExistingTask

import shrub.v2.variant as under_test


class TestBuildVariant:
    def test_tasks_with_no_distros(self):
        bv = under_test.BuildVariant("build variant")

        task_1 = Task("task 1", [])
        task_2 = Task("task 2", [])

        bv.add_task(task_1)
        bv.add_tasks({task_2})

        d = bv.as_dict()

        assert d["name"] == "build variant"
        assert len(d["tasks"]) == 2
        assert d["tasks"][0]["name"] == "task 1"
        assert "distros" not in d["tasks"][0]
        assert d["tasks"][1]["name"] == "task 2"
        assert "distros" not in d["tasks"][1]

    def test_tasks_with_distros(self):
        bv = under_test.BuildVariant("build variant")

        task_1 = Task("task 1", [])
        task_2 = Task("task 2", [])

        bv.add_task(task_1, ["distro 1"])
        bv.add_tasks({task_2}, ["distro 2"])

        d = bv.as_dict()

        assert d["name"] == "build variant"
        assert len(d["tasks"]) == 2
        assert d["tasks"][0]["name"] == "task 1"
        assert d["tasks"][0]["distros"][0] == "distro 1"
        assert d["tasks"][1]["name"] == "task 2"
        assert d["tasks"][1]["distros"][0] == "distro 2"

    def test_tasks_with_activate(self):
        bv = under_test.BuildVariant("build variant")

        task_1 = Task("task 1", [])
        task_2 = Task("task 2", [])
        task_3 = Task("task 3", [])

        bv.add_task(task_1, activate=True)
        bv.add_tasks({task_2}, activate=False)
        bv.display_task("my display task", execution_tasks={task_3}, activate=False)

        d = bv.as_dict()

        assert d["name"] == "build variant"
        assert len(d["tasks"]) == 3
        assert d["tasks"][0]["name"] == "task 1"
        assert d["tasks"][0]["activate"] is True
        assert d["tasks"][1]["name"] == "task 2"
        assert d["tasks"][1]["activate"] is False
        assert d["tasks"][2]["name"] == "task 3"
        assert d["tasks"][2]["activate"] is False

    def test_display_tasks(self):
        bv = under_test.BuildVariant("build variant")

        n_tasks = 5
        tasks = {Task(f"task {i}", []) for i in range(n_tasks)}
        bv.display_task("display", tasks)

        d = bv.as_dict()

        assert d["name"] == "build variant"
        assert len(d["tasks"]) == n_tasks
        assert len(d["display_tasks"]) == 1
        assert d["display_tasks"][0]["name"] == "display"
        assert len(d["display_tasks"][0]["execution_tasks"]) == n_tasks

    def test_display_task_with_different_task_types(self):
        bv = under_test.BuildVariant("build variant")

        n_tasks = 5
        tasks = {Task(f"task {i}", []) for i in range(n_tasks)}
        n_task_groups = 3
        task_groups = {TaskGroup(f"task group {i}", []) for i in range(n_task_groups)}
        n_existing_tasks = 4
        existing_tasks = {ExistingTask(f"existing task {i}") for i in range(n_existing_tasks)}

        bv.display_task(
            "display",
            execution_tasks=tasks,
            execution_task_groups=task_groups,
            execution_existing_tasks=existing_tasks,
            distros=["the distro"],
        )

        d = bv.as_dict()

        assert d["name"] == "build variant"
        assert len(d["tasks"]) == n_tasks + n_task_groups  # Existing tasks should already exist.
        assert len(d["display_tasks"]) == 1
        display_task = d["display_tasks"][0]
        assert display_task["name"] == "display"
        assert len(display_task["execution_tasks"]) == n_tasks + n_task_groups + n_existing_tasks

        all_generated_execution_tasks = {t for t in display_task["execution_tasks"]}
        for task in chain(tasks, task_groups, existing_tasks):
            assert task.name in all_generated_execution_tasks

        for task in d["tasks"]:
            assert "the distro" in task["distros"]

    def test_run_on_option(self):
        bv = under_test.BuildVariant("build variant", run_on=["distro 1"])

        d = bv.as_dict()

        assert "distro 1" in d["run_on"]

    def test_modules_option(self):
        bv = under_test.BuildVariant("build variant", modules=["module 1"])

        d = bv.as_dict()

        assert "module 1" in d["modules"]

    def test_display_name(self):
        display_name = "Variant Name"
        bv = under_test.BuildVariant("build variant", display_name=display_name)

        d = bv.as_dict()

        assert d["display_name"] == display_name

    def test_activate(self):
        bv = under_test.BuildVariant("build variant", activate=False)

        d = bv.as_dict()

        assert d["activate"] is False
