"""Unit tests for shrub.v2.variant."""

from shrub.v2 import Task

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

    def test_tasks_with_with_distros(self):
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
