"""Unit tests for shrub.v2.task."""

import shrub.v2.task as under_test


class TestTaskDependencies:
    def test_no_dependency(self):
        task = under_test.Task("task_name", [])

        d = task.as_dict()

        assert d["name"] == "task_name"
        assert "depends_on" not in d

    def test_multiple_dependencies(self):
        task = under_test.Task(
            "task_name", [], dependencies={under_test.TaskDependency("dep_task")}
        )
        task.dependency("dep_task_2")

        d = task.as_dict()

        assert d["name"] == "task_name"
        assert len(d["depends_on"]) == 2
        assert d["depends_on"][0]["name"] in {"dep_task", "dep_task_2"}
        assert d["depends_on"][1]["name"] in {"dep_task", "dep_task_2"}
        assert d["depends_on"][0]["name"] != d["depends_on"][1]["name"]

    def test_dependency_with_build_variant(self):
        task = under_test.Task(
            "task_name", [], dependencies={under_test.TaskDependency("dep_task", "build_variant")}
        )

        d = task.as_dict()

        assert d["name"] == "task_name"
        assert len(d["depends_on"]) == 1
        assert d["depends_on"][0]["name"] == "dep_task"
        assert d["depends_on"][0]["variant"] == "build_variant"


class TestTaskSpec:
    def test_spec_on_default_distro(self):
        task = under_test.Task("task_name", [])

        spec = task.task_spec()

        assert spec["name"] == "task_name"
        assert "distros" not in spec

    def test_spec_on_distro(self):
        task = under_test.Task("task_name", [])

        spec = task.task_spec("a distro")

        assert spec["name"] == "task_name"
        assert "a distro" in spec["distros"]
