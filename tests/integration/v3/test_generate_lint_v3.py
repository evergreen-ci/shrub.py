"""Test generating a lint project."""
from shrub.v3.evg_build_variant import BuildVariant
from shrub.v3.evg_command import FunctionCall, EvgCommandType, git_get_project
from shrub.v3.evg_project import EvgProject
from shrub.v3.evg_task import EvgTask
from shrub.v3.evg_task_group import EvgTaskGroup
from shrub.v3.shrub_service import ShrubService


class TestGenerateLintV3:
    @staticmethod
    def gen_lint_config():
        targets = ["src", "test"]
        max_hosts = 5
        task_group_name = "lint group"
        variant_name = "lint variant"

        def define_task(target):
            name = f"make-lint-{target}"
            return EvgTask(
                name=name, commands=[FunctionCall(func="run-make", vars={"target": name})]
            )

        tasks = [define_task(target) for target in targets]
        task_group = EvgTaskGroup(
            name=task_group_name,
            tasks=[task.name for task in tasks],
            max_hosts=max_hosts,
            setup_group=[
                git_get_project(directory="src", command_type=EvgCommandType.SYSTEM),
                FunctionCall(func="set-up-credentials"),
            ],
            teardown_group=[
                FunctionCall(func="attach-test-results"),
                FunctionCall(func="remove-test-results"),
            ],
        )

        variant = BuildVariant(name=variant_name, tasks=[task_group.get_task_ref()])
        project = EvgProject(buildvariants=[variant], tasks=tasks, task_groups=[task_group],)
        return project

    def test_generate_lint_json(self, compare_json):
        config = self.gen_lint_config()
        shrub_service = ShrubService()

        config_output = shrub_service.generate_json(config)

        compare_json("lint.json", config_output)

    def test_generate_lint_yaml(self, compare_yaml):
        config = self.gen_lint_config()
        shrub_service = ShrubService()

        config_output = shrub_service.generate_yaml(config)

        compare_yaml("lint.yml", config_output)
