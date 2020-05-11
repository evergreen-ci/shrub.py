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

```
from shrub.v2 import ShrubProject, Task, BuildVariant

n_tasks = 10
def define_task(index):
    name = f"task_name_{index}"

    return Task(
        name,
        [
            FunctionCall("do setup"),
            FunctionCall(
                "run test generator",
                {"parameter_1": "value 1", "parameter_2": "value 2"}
            ),
            FunctionCall("run tests")
        ],
    ).dependency("compile")

tasks = {define_task(i) for i in range(n_tasks)}
variant = BuildVariant("linux-64").display_task("test_suite", tasks)
project = ShrubProject({variant})

project.json()
```

## Run tests

```
poetry run pytest
```
