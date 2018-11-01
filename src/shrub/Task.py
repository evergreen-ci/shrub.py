from shrub.Base import EvergreenBuilder
from shrub.Base import NAME_KEY
from shrub.Base import RECURSE_KEY
from shrub.Command import CommandSequence
from shrub.Command import CommandDefinition


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

    def commands(self, cmds):
        for c in cmds:
            self._commands.add(c.validate())

        return self

    def add_command(self):
        c = CommandDefinition()
        self._commands.add(c)
        return c

    def dependency(self, dep):
        self._dependencies.append(dep)
        return self

    def functions(self, fns):
        for fn in fns:
            self._commands.add(fn)

        return self

    def function_with_vars(self, name, var_map):
        self._commands.add(CommandDefinition().name(name).vars(var_map))
        return self

    def to_map(self):
        obj = {
            "name": self._name,
            "commands": self._commands.to_map(),
        }

        self._add_if_defined(obj, "_priority")
        self._add_if_defined(obj, "_dependencies")

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
    def __init__(self):
        self._group_name = ""
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

    def task(self, ids):
        self._tasks += ids
        return self

    def to_map(self):
        obj = {
            "name": self._group_name,
            "tasks": self._tasks
        }

        self._add_if_defined(obj, "_max_hosts")
        self._add_if_defined(obj, "_setup_group")
        self._add_if_defined(obj, "_max_hosts")
        self._add_if_defined(obj, "_setup_group")
        self._add_if_defined(obj, "_setup_task")
        self._add_if_defined(obj, "_teardown_task")

        return obj
