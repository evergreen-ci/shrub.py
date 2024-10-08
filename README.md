# shrub.py

A python based Evergreen project config generation library

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shrub.py)
[![PyPI version](https://badge.fury.io/py/shrub.py.svg)](https://pypi.org/project/shrub.py/)

## Overview

Based on [shrub](https://github.com/evergreen-ci/shrub/), shrub.py is a library for programatically
building Evergreen project configurations described [here](https://github.com/evergreen-ci/evergreen/wiki/Project-Files).

## Example

The following snippet will create a set of parallel tasks reported under a single display task. It
would generate json used by ```generate.tasks```:

```python
from shrub.v3.evg_task import EvgTask, EvgTaskDependency
from shrub.v3.evg_build_variant import BuildVariant, DisplayTask
from shrub.v3.evg_command import FunctionCall
from shrub.v3.evg_project import EvgProject
from shrub.v3.shrub_service import ShrubService


n_tasks = 10
def define_task(index):
    name = f"task_name_{index}"

    return EvgTask(
        name=name,
        commands=[
            FunctionCall(func="do setup"),
            FunctionCall(
                func="run test generator",
                vars={"parameter_1": "value 1", "parameter_2": "value 2"}
            ),
            FunctionCall(func="run tests")
        ],
        depends_on=[EvgTaskDependency(name="compile")]
    )

tasks = [define_task(i) for i in range(n_tasks)]
display_task = DisplayTask(name="test_suite", execution_tasks=[t.name for t in tasks])
variant = BuildVariant(name="linux-64", tasks=[], display_tasks=[display_task])
project = EvgProject(buildvariants=[variant], tasks=tasks)

print(ShrubService.generate_json(project))
```

## Run tests

```
poetry run pytest
```
