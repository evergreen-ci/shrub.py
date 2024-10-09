"""Unit tests for shrub_service.py."""

import json
import pytest

from pydantic import BaseModel, ConfigDict
from yaml.representer import RepresenterError
from shrub.v3.evg_task import EvgTask, EvgTaskDependency
from shrub.v3.evg_build_variant import BuildVariant, DisplayTask
from shrub.v3.evg_command import FunctionCall, shell_exec, subprocess_exec
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
                shell_exec("a=1\nb=2", env=dict(foo="true", bar="1")),
                shell_exec("a=1\nb=2\n", env=dict(fizz=True, buzz=1)),
                subprocess_exec("bash", command="a=1\nb=2\n\n"),
            ],
            tags=[f"tag{i}" for i in range(index)],
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


EXPECTED_YAML1 = """
buildvariants:
  - name: linux-64
    tasks: []
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
tasks:
  - name: task_name_0
    commands:
      - func: do setup
      - func: run test generator
        vars:
          parameter_1: value 1
          parameter_2: value 2
      - func: run tests
      - command: shell.exec
        params:
          script: |-
            a=1
            b=2
          env:
            foo: "true"
            bar: "1"
      - command: shell.exec
        params:
          script: |
            a=1
            b=2
          env:
            fizz: true
            buzz: 1
      - command: subprocess.exec
        params:
          binary: bash
          command: |+
            a=1
            b=2

    depends_on: [{ name: compile }]
    tags: []
""".strip()

EXPECTED_YAML2 = """
    tags: [tag0, tag1, tag2]
  - name: task_name_4
"""

EXPECTED_YAML3 = """
    tags:
      - tag0
      - tag1
      - tag2
      - tag3
  - name: task_name_5
"""


def test_project_yaml(project):
    out = ShrubService.generate_yaml(project)
    assert EXPECTED_YAML1 in out
    assert EXPECTED_YAML2 in out
    assert EXPECTED_YAML3 in out


class CustomClass:
    pass


class UnsafeModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    prop: CustomClass


def test_safe_yaml():
    model = UnsafeModel(prop=CustomClass(), arbitrary_types_allowed=True)
    with pytest.raises(RepresenterError):
        ShrubService.generate_yaml(model)
