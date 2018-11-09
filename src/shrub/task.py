from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY
from shrub.command import CommandSequence
from shrub.command import CommandDefinition
from shrub.operations import EvergreenCommand


class Task(EvergreenBuilder):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Task only accepts a str")

        self._name = name
        self._priority = None
        self._dependencies = []
        self._commands = CommandSequence()

    def _yaml_map(self):
        return {
            "_priority": {NAME_KEY: "priority", RECURSE_KEY: False},
            "_dependencies": {NAME_KEY: "depends_on", RECURSE_KEY: True},
        }

    def get_name(self):
        return self._name

    def priority(self, value):
        if not isinstance(value, int):
            raise TypeError("priority only accepts an int")

        self._priority = value
        return self

    def command(self, cmd):
        if not isinstance(cmd, EvergreenCommand):
            raise TypeError("command only accepts an EvergreenCommand")

        cmd.validate()
        self._commands.add(cmd.resolve())
        return self

    def commands(self, cmds):
        if not isinstance(cmds, list):
            raise TypeError("commands only accepts a list")

        for c in cmds:
            self.command(c)

        return self

    def dependency(self, dep):
        if not isinstance(dep, TaskDependency):
            raise TypeError("dependency only accepts a TaskDependency")

        self._dependencies.append(dep)
        return self

    def function(self, fn):
        if not isinstance(fn, str):
            raise TypeError("function only accepts a str")

        self._commands.add(CommandDefinition().function(fn))
        return self

    def functions(self, fns):
        if not isinstance(fns, list):
            raise TypeError("function only accepts a list")

        for fn in fns:
            self.function(fn)

        return self

    def function_with_vars(self, name, var_map):
        if not isinstance(name, str):
            raise TypeError("function_with_vars only accepts a str")

        if not isinstance(var_map, dict):
            raise TypeError("function_with_vars only accepts a dict")

        self._commands.add(CommandDefinition().function(name).vars(var_map))
        return self

    def to_map(self):
        obj = {
            "name": self._name,
            "commands": self._commands.to_map(),
        }

        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj


class TaskDependency(EvergreenBuilder):
    def __init__(self, name, variant):
        if not isinstance(name, str):
            raise TypeError("TaskDependency only accepts a str")

        if not isinstance(variant, str):
            raise TypeError("TaskDependency only accepts a str")

        self._name = name
        self._variant = variant

    def _yaml_map(self):
        return {}

    def to_map(self):
        return {
            "name": self._name,
            "variant": self._variant,
        }


class TaskGroup(EvergreenBuilder):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("TaskGroup only accepts a str")

        self._group_name = name
        self._max_hosts = None
        self._setup_group = None
        self._setup_task = None
        self._tasks = []
        self._teardown_task = None
        self._teardown_group = None
        self._timeout = None

    def _yaml_map(self):
        return {
            "_max_hosts": {NAME_KEY: "max_hosts", RECURSE_KEY: False},
            "_setup_group": {NAME_KEY: "setup_group", RECURSE_KEY: True},
            "_setup_task": {NAME_KEY: "setup_task", RECURSE_KEY: True},
            "_teardown_task": {NAME_KEY: "teardown_task", RECURSE_KEY: True},
            "_teardown_group": {NAME_KEY: "teardown_group", RECURSE_KEY: True},
            "_timeout": {NAME_KEY: "timeout", RECURSE_KEY: False},
        }

    def get_name(self):
        return self._group_name

    def max_hosts(self, num):
        if not isinstance(num, int):
            raise TypeError("max_hosts only accepts an int")

        self._max_hosts = num
        return self

    def timeout(self, timeout):
        if not isinstance(timeout, int):
            raise TypeError("timeout only accepts an int")

        self._timeout = timeout
        return self

    def task(self, id):
        if not isinstance(id, str):
            raise TypeError("task only accepts a str")

        self._tasks.append(id)
        return self

    def tasks(self, ids):
        if not isinstance(ids, list):
            raise TypeError("task only accepts a list")

        self._tasks += ids
        return self

    def setup_group(self):
        if not self._setup_group:
            self._setup_group = CommandSequence()

        c = CommandDefinition()

        self._setup_group.add(c)
        return c

    def teardown_group(self):
        if not self._teardown_group:
            self._teardown_group = CommandSequence()

        c = CommandDefinition()

        self._teardown_group.add(c)
        return c

    def to_map(self):
        obj = {
            "name": self._group_name,
            "tasks": self._tasks
        }
        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj
