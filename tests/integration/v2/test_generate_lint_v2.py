from shrub.v2 import (
    Task,
    FunctionCall,
    BuildVariant,
    ShrubProject,
    TaskGroup,
    git_get_project,
    CommandType,
)


class TestGenerateLint:
    @staticmethod
    def gen_lint_config():
        targets = ["src", "test"]
        max_hosts = 5
        task_group_name = "lint group"
        variant_name = "lint variant"

        def define_task(target):
            name = f"make-lint-{target}"
            return Task(name, [FunctionCall("run-make", {"target": name})])

        task_group = TaskGroup(
            task_group_name,
            [define_task(target) for target in targets],
            max_hosts=max_hosts,
            setup_group=[
                git_get_project("src").set_type(CommandType.SYSTEM),
                FunctionCall("set-up-credentials"),
            ],
            teardown_group=[
                FunctionCall("attach-test-results"),
                FunctionCall("remove-test-results"),
            ],
        )

        variant = BuildVariant(variant_name).add_task_group(task_group)
        project = ShrubProject({variant})
        return project

    def test_generate_lint_json(self, compare_json):
        config = self.gen_lint_config()

        config_output = config.json().strip()

        compare_json("lint.json", config_output)

    def test_generate_lint_yaml(self, compare_yaml):
        config = self.gen_lint_config()

        config_output = config.yaml().strip()

        compare_yaml("lint.yml", config_output)
