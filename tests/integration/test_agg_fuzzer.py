import json
import yaml

from shrub.config import Configuration
from shrub.task import TaskDependency
from shrub.variant import TaskSpec
from shrub.command import CommandDefinition
from shrub.variant import DisplayTaskDefinition


def read_test_data_file(filename):
    with open("tests/integration/data/" + filename) as f:
        return f.read()


def compare_json(expected, actual):
    expected_json = json.loads(expected)
    actual_json = json.loads(actual)

    assert expected_json == actual_json


def compare_yaml(expected, actual):
    expected_yaml = yaml.safe_load(expected)
    actual_yaml = yaml.safe_load(actual)

    assert expected_yaml == actual_yaml


class TestAggregationFuzzer:
    @staticmethod
    def configure():
        n_tasks = 10
        c = Configuration()

        task_names = []
        task_specs = []

        for i in range(n_tasks):
            name = "aggregation_multiversion_fuzzer_{0:03d}".format(i)
            task_names.append(name)
            task_specs.append(TaskSpec(name))
            t = c.task(name)
            t.dependency(TaskDependency("compile")).commands([
                CommandDefinition().function("do setup"),
                CommandDefinition().function("do multiversion setup"),
                CommandDefinition().function("run jstestfuzz").vars({
                    "jstestfuzz_var": "--numGeneratedFiles 5",
                    "npm_command": "agg-fuzzer",
                }),
                CommandDefinition().function("run tests").vars({
                    "continue_on_failure": "false",
                    "resmoke_args": "--suites=generational_fuzzer",
                    "should_shuffle": "false",
                    "task_path_suffix": "false",
                    "timeout_secs": "1800",
                })
            ])

        dt = DisplayTaskDefinition("aggregation_multiversion_fuzzer")\
            .execution_tasks(task_names)
        c.variant("linux-64").tasks(task_specs).display_task(dt)

        return c

    def test_generate_agg_fuzzer_json(self):
        config = self.configure()

        config_output = config.to_json().strip()
        expected_output = read_test_data_file("agg_fuzzer.json").strip()

        compare_json(expected_output, config_output)

    def test_generate_agg_fuzzer_yaml(self):
        config = self.configure()

        config_output = config.to_yaml().strip()
        expected_output = read_test_data_file("agg_fuzzer.yml").strip()

        compare_yaml(expected_output, config_output)
