from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY
from shrub.command import CommandSequence
from shrub.task import Task
from shrub.task import TaskGroup
from shrub.variant import Variant


def _find_name_in_list(name_list, name):
    """Call get_name() on all items in the given list to find a match."""
    for l in name_list:
        if l.get_name() == name:
            return l

    return None


class Configuration(EvergreenBuilder):
    """An Evergreen configuration.

    Can be converted into json or yaml.
    """

    def __init__(self):
        self._functions = {}
        self._tasks = []
        self._groups = []
        self._variants = []
        self._pre = None
        self._post = None
        self._timeout = None

        self._exec_timeout_secs = None
        self._batch_time_secs = None
        self._stepback = None
        self._command_type = None
        self._ignore_files = []

    def _yaml_map(self):
        return {
            "_tasks": {NAME_KEY: "tasks", RECURSE_KEY: True},
            "_groups": {NAME_KEY: "task_groups", RECURSE_KEY: True},
            "_variants": {NAME_KEY: "buildvariants", RECURSE_KEY: True},
            "_pre": {NAME_KEY: "pre", RECURSE_KEY: True},
            "_post": {NAME_KEY: "post", RECURSE_KEY: True},
            "_timeout": {NAME_KEY: "timeout", RECURSE_KEY: False},
            "_exec_timeout_secs": {NAME_KEY: "timeout", RECURSE_KEY: False},
            "_batch_time_secs": {NAME_KEY: "batchtime", RECURSE_KEY: False},
            "_stepback": {NAME_KEY: "stepback", RECURSE_KEY: False},
            "_command_type": {NAME_KEY: "command_type", RECURSE_KEY: False},
            "_ignore_files": {NAME_KEY: "ignore", RECURSE_KEY: False},
        }

    def task(self, name):
        if not isinstance(name, str):
            raise TypeError("task only accepts strings")

        t = _find_name_in_list(self._tasks, name)
        if t:
            return t

        t = Task(name)
        self._tasks.append(t)
        return t

    def task_group(self, name):
        if not isinstance(name, str):
            raise TypeError("task_group only accepts strings")

        g = _find_name_in_list(self._groups, name)
        if g:
            return g

        g = TaskGroup(name)
        self._groups.append(g)
        return g

    def function(self, name):
        if not isinstance(name, str):
            raise TypeError("function only accepts strings")

        if name in self._functions:
            return self._functions[name]

        seq = CommandSequence()
        self._functions[name] = seq
        return seq

    def variant(self, name):
        if not isinstance(name, str):
            raise TypeError("variant only accepts strings")

        v = _find_name_in_list(self._variants, name)
        if v:
            return v

        v = Variant(name)
        self._variants.append(v)
        return v

    def pre(self, cmds):
        if not isinstance(cmds, CommandSequence):
            raise TypeError("pre only accepts a Sequence")

        self._pre = cmds
        return self

    def post(self, cmds):
        if not isinstance(cmds, CommandSequence):
            raise TypeError("pre only accepts a Sequence")

        self._post = cmds
        return self

    def exec_timeout(self, duration):
        if not isinstance(duration, int):
            raise TypeError("exec_timeout only accepts an int")

        self._exec_timeout_secs = duration
        return self

    def batch_time(self, duration):
        if not isinstance(duration, int):
            raise TypeError("batch_time only accepts an int")

        self._batch_time_secs = duration
        return self

    def stepback(self, stepback):
        if not isinstance(stepback, bool):
            raise TypeError("stepback only accepts a bool")

        self._stepback = stepback
        return self

    def command_type(self, t):
        if t not in ["system", "setup", "task"]:
            raise ValueError("Bad Command Type")

        self._command_type = t
        return self

    def ignore_file(self, filename):
        if not isinstance(filename, str):
            raise TypeError("ignore_file only accepts a str")

        self._ignore_files.append(filename)
        return self

    def ignore_files(self, filenames):
        if not isinstance(filenames, list):
            raise TypeError("ignore_file only accepts a Sequence")

        for f in filenames:
            self.ignore_file(f)

        return self

    def to_map(self):
        obj = {}
        self._add_defined_attribs(obj, self._yaml_map().keys())

        obj["functions"] = {}
        for k in self._functions:
            obj["functions"][k] = self._functions[k].to_map()

        return obj
