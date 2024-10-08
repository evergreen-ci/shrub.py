"""Unit tests for shrub_service.py."""

import json
import pytest

from shrub.v3.evg_task import EvgTask, EvgTaskDependency
from shrub.v3.evg_build_variant import BuildVariant, DisplayTask
from shrub.v3.evg_command import FunctionCall
from shrub.v3.evg_project import EvgProject
from shrub.v3.shrub_service import ShrubService


@pytest.fixture
def project():
    n_tasks = 10

    def define_task(index):
        name = f"task_name_{index}"

        return EvgTask(
            name=name,
            commands=[
                FunctionCall(func="do setup"),
                FunctionCall(
                    func="run test generator",
                    vars={"parameter_1": "value 1", "parameter_2": "value 2"},
                ),
                FunctionCall(func="run tests"),
            ],
            depends_on=[EvgTaskDependency(name="compile")],
        )

    tasks = [define_task(i) for i in range(n_tasks)]
    display_task = DisplayTask(name="test_suite", execution_tasks=[t.name for t in tasks])
    variant = BuildVariant(name="linux-64", tasks=[], display_tasks=[display_task])
    return EvgProject(buildvariants=[variant], tasks=tasks)


def test_project_json(project):
    out = ShrubService.generate_json(project)
    data = json.loads(out)
    assert "buildvariants" in data
    assert "tasks" in data


EXPECTED_YAML = """
buildvariants:
  - name: linux-64
    display_tasks:
      - name: test_suite
        execution_tasks:
          - task_name_0
          - task_name_1
          - task_name_2
          - task_name_3
          - task_name_4
          - task_name_5
          - task_name_6
          - task_name_7
          - task_name_8
          - task_name_9
    tasks: []
tasks:
  - name: task_name_0
    depends_on: [{ name: compile }]
    commands:
      - func: do setup
      - func: run test generator
        vars:
          parameter_1: value 1
          parameter_2: value 2
      - func: run tests
""".strip()


def test_project_yaml(project):
    out = ShrubService.generate_yaml(project)
    assert EXPECTED_YAML in out, out
