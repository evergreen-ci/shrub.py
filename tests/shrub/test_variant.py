import pytest

from shrub.variant import DisplayTaskDefinition
from shrub.variant import TaskSpec
from shrub.variant import Variant


class TestVariant:
    def test_empty_command_definition(self):
        v = Variant("variant name")

        assert "variant name" == v.get_name()
        assert {"name": "variant name"} == v.to_map()

    def test_flat_values_in_map(self):
        v = Variant("variant name")
        v.display_name("display name").run_on("distro").batch_time(100)

        obj = v.to_map()
        assert "variant name" == obj["name"]
        assert "display name" == obj["display_name"]
        assert ["distro"] == obj["run_on"]
        assert 100 == obj["batchtime"]

    def test_expansions_can_be_added(self):
        v = Variant("variant name")
        v.expansion("k0", "v0")
        v.expansions({"k1": "v1", "k2": "v2"})

        obj = v.to_map()
        assert "v0" in obj["expansions"]["k0"]
        assert "v1" in obj["expansions"]["k1"]
        assert "v2" in obj["expansions"]["k2"]

    def test_tasks_can_be_added(self):
        v = Variant("variant name")
        v.task(TaskSpec("task 0")).tasks([TaskSpec("task 1"), TaskSpec("task 2")])

        obj = v.to_map()
        assert "task 0" == obj["tasks"][0]["name"]
        assert "task 1" == obj["tasks"][1]["name"]
        assert "task 2" == obj["tasks"][2]["name"]

    def test_invalid_tasks_cannot_be_added(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.task("I'm not really a task")

        with pytest.raises(TypeError):
            v.tasks(TaskSpec("not array"))

    def test_module_can_be_added(self):
        v = Variant("variant name")
        v.module("enterprise")

        obj = v.to_map()
        assert ["enterprise"] == obj["modules"]

    def test_modules_can_be_added(self):
        v = Variant("variant name")
        v.modules(["enterprise", "enterprise2"])

        obj = v.to_map()
        assert "enterprise" in obj["modules"]
        assert "enterprise2" in obj["modules"]

    def test_invalid_modules_cannot_be_added(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.module(25)

        with pytest.raises(TypeError):
            v.modules(TaskSpec("not array"))

    def test_display_tasks_can_be_added(self):
        v = Variant("variant name")
        v.display_task(DisplayTaskDefinition("display task 0")).display_tasks(
            [DisplayTaskDefinition("display task 1"), DisplayTaskDefinition("display task 2")]
        )

        obj = v.to_map()
        assert "display task 0" == obj["display_tasks"][0]["name"]
        assert "display task 1" == obj["display_tasks"][1]["name"]
        assert "display task 2" == obj["display_tasks"][2]["name"]

    def test_invalid_name(self):
        with pytest.raises(TypeError):
            Variant(42)

    def test_invalid_display_name(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.display_name(42)

    def test_invalid_batch_time(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.batch_time("hello World")

    def test_invalid_run_on(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.run_on(42)

    def test_invalid_expansion(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.expansion(42, "v")

        with pytest.raises(TypeError):
            v.expansion("k", 42)

    def test_invalid_expansions(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.expansions(42)

    def test_invalid_display_task(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.display_task("hello world")

    def test_invalid_display_tasks(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.display_tasks("hello world")

    def test_variant_activate(self):
        v = Variant("variant name")
        obj = v.to_map()
        assert "activate" not in obj

        v.activate(True)
        obj = v.to_map()
        assert obj["activate"] is True

        v.activate(False)
        obj = v.to_map()
        assert obj["activate"] is False

        v.activate(None)
        obj = v.to_map()
        assert "activate" not in obj

    def test_variant_cron(self):
        v = Variant("variant name")
        obj = v.to_map()
        assert "cron" not in obj

        v.cron("0 * * * *")
        obj = v.to_map()
        assert obj["cron"] == "0 * * * *"

    def test_variant_invalid_cron(self):
        v = Variant("variant name")
        with pytest.raises(TypeError):
            v.cron(5)


class TestTaskSpec:
    def test_task_spec(self):
        ts = TaskSpec("task name").stepback().distro("linux")

        obj = ts.to_map()
        assert "task name" == obj["name"]
        assert obj["stepback"]
        assert ["linux"] == obj["distros"]

    def test_task_spec_activate(self):
        ts = TaskSpec("task name")
        obj = ts.to_map()
        assert "activate" not in obj

        ts.activate(True)
        obj = ts.to_map()
        assert obj["activate"] is True

        ts.activate(False)
        obj = ts.to_map()
        assert obj["activate"] is False

        ts.activate(None)
        obj = ts.to_map()
        assert "activate" not in obj

    def test_invalid_distro(self):
        ts = TaskSpec("task name")
        with pytest.raises(TypeError):
            ts.distro(42)

    def test_task_spec_cron(self):
        ts = TaskSpec("task name")
        obj = ts.to_map()
        assert "cron" not in obj

        ts.cron("0 * * * *")
        obj = ts.to_map()
        assert obj["cron"] == "0 * * * *"

    def test_task_spec_invalid_cron(self):
        ts = TaskSpec("task name")
        with pytest.raises(TypeError):
            ts.cron(5)


class TestDisplayTaskDefinition:
    def test_empty_display_task(self):
        dt = DisplayTaskDefinition("name")

        obj = dt.to_map()
        assert {"name": "name"} == obj

    def test_items_added_to_display_task(self):
        dt = DisplayTaskDefinition("display task name")
        dt.execution_task("comp0").execution_tasks(["comp1", "comp2"])

        obj = dt.to_map()
        assert "display task name" == obj["name"]
        assert "comp0" in obj["execution_tasks"]
        assert "comp1" in obj["execution_tasks"]
        assert "comp2" in obj["execution_tasks"]

    def test_invalid_name(self):
        with pytest.raises(TypeError):
            DisplayTaskDefinition(42)

    def test_invalid_component(self):
        dt = DisplayTaskDefinition("display task")
        with pytest.raises(TypeError):
            dt.execution_task(42)

    def test_invalid_components(self):
        dt = DisplayTaskDefinition("display task")
        with pytest.raises(TypeError):
            dt.execution_tasks(42)
