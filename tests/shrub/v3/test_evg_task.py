from shrub.v3.evg_project import EvgProject
from shrub.v3.evg_task import EvgTask, EvgTaskDependency
from shrub.v3.shrub_service import ShrubService
from shrub.v3.evg_command import FunctionCall, subprocess_exec


def _test_task_field(field, value, content):
    # Test both implicit and explicit `None`.
    if value is None:
        assert content is None

        task = EvgTask(name="test task")
        out = ShrubService.generate_yaml(EvgProject(tasks=[task], buildvariants=[]))
        assert field not in out

        args = {field: value}
        task = EvgTask(name="test task", **args)
        out = ShrubService.generate_yaml(EvgProject(tasks=[task], buildvariants=[]))
        assert field not in out

    # Test presence of expected values.
    else:
        args = {field: value}
        task = EvgTask(name="test task", **args)
        out = ShrubService.generate_yaml(EvgProject(tasks=[task], buildvariants=[]))

        for value in content:
            assert value in out


class TestTaskFields:
    def test_task_name(self):
        task = EvgTask(name="task name")
        out = ShrubService.generate_yaml(EvgProject(tasks=[task], buildvariants=[]))
        assert "task name" in out

    def test_task_commands(out):
        _test_task_field("commands", None, None)
        _test_task_field("commands", [], ["commands: []"])

        _test_task_field(
            "commands",
            [FunctionCall(func="func")],
            [
                "commands:",
                "func: func",
            ],
        )

        _test_task_field(
            "commands",
            [subprocess_exec(binary="binary")],
            [
                "commands:",
                "command: subprocess.exec",
                "binary: binary",
            ],
        )

        _test_task_field(
            "commands",
            [FunctionCall(func="one"), FunctionCall(func="two")],
            [
                "commands:",
                "func: one",
                "func: two",
            ],
        )

    def test_task_depends_on(self):
        _test_task_field("depends_on", None, None)
        _test_task_field("depends_on", [], ["depends_on: []"])

        _test_task_field(
            "depends_on",
            [EvgTaskDependency(name="task")],
            [
                "depends_on:",
                "name: task",
            ],
        )

        _test_task_field(
            "depends_on",
            [EvgTaskDependency(name="one"), EvgTaskDependency(name="two")],
            [
                "depends_on:",
                "name: one",
                "name: two",
            ],
        )

    def test_task_run_on(self):
        _test_task_field("run_on", None, None)
        _test_task_field("run_on", [], ["run_on: []"])
        _test_task_field("run_on", str(), ['run_on: ""'])
        _test_task_field("run_on", "distro name", ["run_on: distro name"])

        _test_task_field(
            "run_on",
            ["distro name"],
            [
                "run_on:",
                "- distro name",
            ],
        )

        _test_task_field(
            "run_on",
            ["one", "two"],
            [
                "run_on:",
                "- one",
                "- two",
            ],
        )

    def test_task_exec_timeout_secs(self):
        _test_task_field("exec_timeout_secs", None, None)
        _test_task_field("exec_timeout_secs", 0, ["exec_timeout_secs: 0"])
        _test_task_field("exec_timeout_secs", 123, ["exec_timeout_secs: 123"])

    def test_task_tags(self):
        _test_task_field("tags", None, None)
        _test_task_field("tags", [], "tags: []")
        _test_task_field("tags", ["tag"], "tags: [tag]")
        _test_task_field("tags", ["one", "two"], "tags: [one, two]")
        _test_task_field("tags", ["one", "two", "three"], "tags: [one, two, three]")

        # See `ConfigDumper.FLOW_TAG_COUNT` in src/shrub/v3/shrub_service.py.
        _test_task_field(
            "tags",
            ["one", "two", "three", "four"],
            [
                "tags:",
                "- one",
                "- two",
                "- three",
                "- four",
            ],
        )

    def test_task_disable(self):
        _test_task_field("disable", None, None)
        _test_task_field("disable", False, "disable: false")
        _test_task_field("disable", True, "disable: true")

    def test_task_patchable(self):
        _test_task_field("patchable", None, None)
        _test_task_field("patchable", False, ["patchable: false"])
        _test_task_field("patchable", True, ["patchable: true"])

    def test_task_batchtime(self):
        _test_task_field("batchtime", None, None)
        _test_task_field("batchtime", 0, ["batchtime: 0"])
        _test_task_field("batchtime", 123, ["batchtime: 123"])

    def test_task_stepback(self):
        _test_task_field("stepback", None, None)
        _test_task_field("stepback", False, ["stepback: false"])
        _test_task_field("stepback", True, ["stepback: true"])
