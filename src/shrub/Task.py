from Command import CommandSequence
from Command import Command


class Task:
    def __init__(self, name):
        self._name = name
        self._priority = None
        self._dependencies = []
        self._commands = CommandSequence

        self._yaml_map = {
            "_priority": "priority",
            "_dependencies": "depends_on",
        }

    def get_name(self):
        return self._name

    def priority(self, value):
        self._priority = value
        return self

    def command(self, cmds):
        for c in cmds:
            self._commands.add(c.validate())

        return self

    def add_command(self):
        c = Command()
        self._commands.add(c)
        return c

    def dependency(self, deps):
        self._dependencies += deps
        return self

    def function(self, fns):
        for fn in fns:
            self._commands.add(CommandDefinition(fn))

        return self

    def _add_if_defined(self, obj, prop):
        value = getattr(self, prop)
        if value and len(value) > 0:
            obj[self._yaml_map[prop]] = value

    def to_obj(self):
        obj = {
            "name": self._name,
            "commands": self._commands.to_obj()
        }

        self._add_if_defined(obj, "_priority")
        self._add_if_defined(obj, "_dependencies")

        return obj




class TaskDependency:
    def __init__(self, name, variant):
        self.name = name
        self.variant = variant

def add_to_object(obj, property, marshall_map):
    if getattr(obj, property):
        obj.[marshall_map[property]] = value

    return obj


class TaskGroup:
    def __init__(self):
        self._group_name = ""
        self._max_hosts = None
        self._setup_group = None
        self._setup_task = None
        self._tasks = []
        self._teardown_task = None
        self._teardown_group = None
        self._timeout = None

        self._yaml_map = {
            "_max_hosts": "max_hosts",
            "_setup_group": "setup_group",
            "_setup_task": "setup_task",
            "_teardown_task": "teardown_task",
            "_teardown_group": "teardown_group",
            "_timeout": "timeout",
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

    def _add_if_defined(self, obj, prop):
        value = getattr(self, prop)
        if value and len(value) > 0:
            obj[self._yaml_map[prop]] = value

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
