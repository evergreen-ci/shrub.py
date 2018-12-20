import pytest

from shrub.operations import CmdGetProject
from shrub.task import Task
from shrub.task import TaskDependency
from shrub.task import TaskGroup


class TestTask:

    def test_task_with_flat_values(self):
        t = Task("task 0")
        t.priority(42)

        obj = t.to_map()
        assert "task 0" == t.get_name()
        assert "task 0" == obj["name"]
        assert 42 == obj["priority"]

    def test_adding_dependencies(self):
        t = Task("task 0")
        t.dependency(TaskDependency("dep 0"))\
            .dependency(TaskDependency("dep 1"))\
            .dependency(TaskDependency("dep 2"))

        obj = t.to_map()
        assert 3 == len(obj["depends_on"])
        assert "dep 1" == obj["depends_on"][1]["name"]

    def test_adding_requires(self):
        t = Task("task 0")
        t.requires(TaskDependency("dep 0")) \
            .requires(TaskDependency("dep 1")) \
            .requires(TaskDependency("dep 2"))

        obj = t.to_map()
        assert 3 == len(obj["requires"])
        assert "dep 1" == obj["requires"][1]["name"]

    def test_adding_command(self):
        t = Task("task 0")
        t.command(CmdGetProject().resolve())

        obj = t.to_map()
        assert "git.get_project" == obj["commands"][0]["command"]

    def test_adding_commands(self):
        t = Task("task 0")
        t.commands([CmdGetProject().resolve(), CmdGetProject().resolve()])

        obj = t.to_map()
        assert 2 == len(obj["commands"])
        assert "git.get_project" == obj["commands"][0]["command"]

    def test_functions(self):
        t = Task("task 0")
        t.function("fn 0")
        t.functions(["fn 1", "fn 2"])

        obj = t.to_map()
        assert 3 == len(obj["commands"])
        assert "fn 0" == obj["commands"][0]["func"]
        assert "fn 1" == obj["commands"][1]["func"]
        assert "fn 2" == obj["commands"][2]["func"]

    def test_function_with_vars(self):
        t = Task("task 0")
        t.function_with_vars("fn 0", {"x": "y"})

        obj = t.to_map()
        assert "fn 0" == obj["commands"][0]["func"]
        assert "y" == obj["commands"][0]["vars"]["x"]

    def test_invalid_priority(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.priority("hello world")

    def test_invalid_command(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.command("hello world")

    def test_invalid_commands(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.commands("hello world")

    def test_invalid_dependency(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.dependency("hello world")

    def test_invalid_function(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.dependency(42)

    def test_invalid_functions(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.dependency("function")

    def test_invalid_function_with_vars(self):
        t = Task("task 0")

        with pytest.raises(TypeError):
            t.function_with_vars(42, {})

        with pytest.raises(TypeError):
            t.function_with_vars("function", 42)

    def test_invalid_name(self):
        with pytest.raises(TypeError):
            Task(42)


class TestTaskDependency:
    def test_flat_values(self):
        td = TaskDependency("dep0")

        obj = td.to_map()
        assert "dep0" == obj["name"]

    def test_variant(self):
        td = TaskDependency("dep 0")
        td.variant("var0")

        obj = td.to_map()
        assert "var0" == obj["variant"]

    def test_invalid_name(self):
        with pytest.raises(TypeError):
            TaskDependency(42, "variant")

    def test_invalid_variant(self):
        td = TaskDependency("dep 0")

        with pytest.raises(TypeError):
            td.variant(42)


class TestTaskGroup:
    def test_flat_value(self):
        tg = TaskGroup("task group 0")
        tg.max_hosts(5)\
            .timeout(42)

        obj = tg.to_map()
        assert "task group 0" == tg.get_name()
        assert "task group 0" == obj["name"]
        assert 5 == obj["max_hosts"]
        assert 42 == obj["timeout"]

    def test_adding_tasks(self):
        tg = TaskGroup("task group 0")
        tg.task("task 0").tasks(["task 1", "task 2"])

        obj = tg.to_map()
        assert "task 0" in obj["tasks"]
        assert "task 1" in obj["tasks"]
        assert "task 2" in obj["tasks"]

    def test_setup_group(self):
        tg = TaskGroup("task group 0")
        tg.setup_group().function("func 0")

        obj = tg.to_map()
        assert "func 0" == obj["setup_group"][0]["func"]

    def test_teardown_group(self):
        tg = TaskGroup("task group 0")
        tg.teardown_group().function("func 0")

        obj = tg.to_map()
        assert "func 0" == obj["teardown_group"][0]["func"]

    def test_invalid_name(self):
        with pytest.raises(TypeError):
            TaskGroup(42)

    def test_invalid_max_hosts(self):
        tg = TaskGroup("task group 0")

        with pytest.raises(TypeError):
            tg.max_hosts("hello world")

    def test_invalid_timeout(self):
        tg = TaskGroup("task group 0")

        with pytest.raises(TypeError):
            tg.timeout("hello world")

    def test_invalid_task(self):
        tg = TaskGroup("task group 0")

        with pytest.raises(TypeError):
            tg.task(42)

    def test_invalid_tasks(self):
        tg = TaskGroup("task group 0")

        with pytest.raises(TypeError):
            tg.tasks("hello world")
