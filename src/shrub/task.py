from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY
from shrub.command import CommandSequence
from shrub.command import CommandDefinition


class Task(EvergreenBuilder):
    def __init__(self, name):
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
        self._priority = value
        return self

    def command(self, cmd):
        cmd.validate()
        self._commands.add(cmd.resolve())
        return self

    def commands(self, cmds):
        for c in cmds:
            c.validate()
            self._commands.add(c.resolve())

        return self

    def dependency(self, dep):
        self._dependencies.append(dep)
        return self

    def function(self, fn):
        self._commands.add(CommandDefinition().function(fn))
        return self

    def functions(self, fns):
        for fn in fns:
            self.function(fn)

        return self

    def function_with_vars(self, name, var_map):
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

    def name(self, name):
        self._group_name = name
        return self

    def max_hosts(self, num):
        self._max_hosts = num
        return self

    def timeout(self, timeout):
        self._timeout = timeout
        return self

    def task(self, id):
        self._tasks.append(id)
        return self

    def tasks(self, ids):
        self._tasks += ids
        return self

    def to_map(self):
        obj = {
            "name": self._group_name,
            "tasks": self._tasks
        }
        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj
