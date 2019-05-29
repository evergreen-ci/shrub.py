# shrub.py -- A python based Evergreen project config generation library

## Overview

Based on [shrub](https://github.com/evergreen-ci/shrub/), shrub.py is a library for programatically 
building Evergreen project configurations described [here](https://github.com/evergreen-ci/evergreen/wiki/Project-Files).

## Example

The following snippet will create a set of parallel tasks reported under a single display task. It
would generate json used by ```generate.tasks```:

```
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
            .components(task_names)
        c.variant("linux-64").tasks(task_specs).display_task(dt)
        
        c.to_json()
```

## Run tests

```
pip install tox
tox
```
