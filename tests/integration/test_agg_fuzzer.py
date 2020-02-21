from shrub.config import Configuration
from shrub.task import TaskDependency
from shrub.variant import TaskSpec
from shrub.command import CommandDefinition
from shrub.variant import DisplayTaskDefinition


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
            t.dependency(TaskDependency("compile")).commands(
                [
                    CommandDefinition().function("do setup"),
                    CommandDefinition().function("do multiversion setup"),
                    CommandDefinition()
                    .function("run jstestfuzz")
                    .vars({"jstestfuzz_var": "--numGeneratedFiles 5", "npm_command": "agg-fuzzer"}),
                    CommandDefinition()
                    .function("run tests")
                    .vars(
                        {
                            "continue_on_failure": "false",
                            "resmoke_args": "--suites=generational_fuzzer",
                            "should_shuffle": "false",
                            "task_path_suffix": "false",
                            "timeout_secs": "1800",
                        }
                    ),
                ]
            )

        dt = DisplayTaskDefinition("aggregation_multiversion_fuzzer").execution_tasks(task_names)
        c.variant("linux-64").tasks(task_specs).display_task(dt)

        return c

    def test_generate_agg_fuzzer_json(self, compare_json):
        config = self.configure()

        config_output = config.to_json().strip()

        compare_json("agg_fuzzer.json", config_output)

    def test_generate_agg_fuzzer_yaml(self, compare_yaml):
        config = self.configure()

        config_output = config.to_yaml().strip()

        compare_yaml("agg_fuzzer.yml", config_output)
