from shrub.config import Configuration
from shrub.variant import TaskSpec


def read_test_data_file(filename):
    with open('tests/integration/data/' + filename) as f:
        return f.read()


class TestGenerateLint:
    @staticmethod
    def gen_lint_config():
        targets = ["src", "test"]
        max_hosts = 5
        variant_name = "lint variant"
        task_group_name = "lint group"
        config = Configuration()
        tasks = []

        for t in targets:
            name = "make-lint-" + t
            config.task(name).function_with_vars("run-make", {"target": name})
            tasks.append(t)

        group = config.task_group(task_group_name).max_hosts(max_hosts)
        group.setup_group().type("system") \
            .command("git.get_project").param("directory", "src")
        group.setup_group().function("set-up-credentials")
        group.teardown_group().function("attach-test-results")
        group.teardown_group().function("remove-test-results")
        group.tasks(tasks)

        config.variant(variant_name).task(TaskSpec(task_group_name))

        return config

    def test_generate_lint_json(self):
        config = self.gen_lint_config()

        config_output = config.to_json().strip()
        expected_output = read_test_data_file("lint.json").strip()

        assert expected_output == config_output

    def test_generate_lint_yaml(self):
        config = self.gen_lint_config()

        config_output = config.to_yaml().strip()
        expected_output = read_test_data_file("lint.yml").strip()

        assert expected_output == config_output
