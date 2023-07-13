from shrub.v2 import ShrubProject, FunctionCall, Task, BuildVariant


class TestAggregationFuzzerV2:
    @staticmethod
    def configure():
        n_tasks = 10

        def define_task(index):
            name = f"aggregation_multiversion_fuzzer_{index:03d}"
            return Task(
                name,
                [
                    FunctionCall("do setup"),
                    FunctionCall("do multiversion setup"),
                    FunctionCall(
                        "run jstestfuzz",
                        {"jstestfuzz_var": "--numGeneratedFiles 5", "npm_command": "agg-fuzzer"},
                    ),
                    FunctionCall(
                        "run tests",
                        {
                            "continue_on_failure": "false",
                            "resmoke_args": "--suites=generational_fuzzer",
                            "should_shuffle": "false",
                            "task_path_suffix": "false",
                            "timeout_secs": "1800",
                        },
                    ),
                ],
            ).dependency("compile")

        tasks = {define_task(i) for i in range(n_tasks)}
        variant = BuildVariant(name="linux-64").display_task(
            "aggregation_multiversion_fuzzer", tasks
        )

        project = ShrubProject({variant})

        return project

    def test_generate_agg_fuzzer_json(self, compare_json):
        config = self.configure()

        config_output = config.json().strip()

        compare_json("agg_fuzzer.json", config_output)

    def test_generate_agg_fuzzer_yaml(self, compare_yaml):
        config = self.configure()

        config_output = config.yaml().strip()

        compare_yaml("agg_fuzzer.yml", config_output)
