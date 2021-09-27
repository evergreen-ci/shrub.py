"""Integration test for agg fuzzer creation."""

from shrub.v3.evg_build_variant import BuildVariant, DisplayTask
from shrub.v3.evg_command import FunctionCall
from shrub.v3.evg_project import EvgProject
from shrub.v3.evg_task import EvgTask, EvgTaskDependency
from shrub.v3.shrub_service import ShrubService


class TestAggregationFuzzerV3:
    @staticmethod
    def configure():
        n_tasks = 10

        def define_task(index):
            name = f"aggregation_multiversion_fuzzer_{index:03d}"
            return EvgTask(
                name=name,
                commands=[
                    FunctionCall(func="do setup"),
                    FunctionCall(func="do multiversion setup"),
                    FunctionCall(
                        func="run jstestfuzz",
                        vars={
                            "jstestfuzz_var": "--numGeneratedFiles 5",
                            "npm_command": "agg-fuzzer",
                        },
                    ),
                    FunctionCall(
                        func="run tests",
                        vars={
                            "continue_on_failure": "false",
                            "resmoke_args": "--suites=generational_fuzzer",
                            "should_shuffle": "false",
                            "task_path_suffix": "false",
                            "timeout_secs": "1800",
                        },
                    ),
                ],
                depends_on=[EvgTaskDependency(name="compile")],
            )

        tasks = [define_task(i) for i in range(n_tasks)]
        variant = BuildVariant(
            name="linux-64",
            tasks=[task.get_task_ref() for task in tasks],
            display_tasks=[
                DisplayTask(
                    name="aggregation_multiversion_fuzzer",
                    execution_tasks=[task.name for task in tasks],
                )
            ],
        )

        project = EvgProject(buildvariants=[variant], tasks=tasks,)

        return project

    def test_generate_agg_fuzzer_json(self, compare_json):
        config = self.configure()
        shrub_service = ShrubService()

        config_output = shrub_service.generate_json(config)

        compare_json("agg_fuzzer.json", config_output)

    def test_generate_agg_fuzzer_yaml(self, compare_yaml):
        config = self.configure()
        shrub_service = ShrubService()

        config_output = shrub_service.generate_yaml(config)

        compare_yaml("agg_fuzzer.yml", config_output)
