from shrub.Base import EvergreenBuilder
from shrub.Base import NAME_KEY
from shrub.Base import RECURSE_KEY
from shrub.Command import CommandSequence
from shrub.Task import Task
from shrub.Task import TaskGroup
from shrub.Variant import Variant


def _find_name_in_list(name_list, name):
    for l in name_list:
        if l.get_name() == name:
            return l

    return None


class Configuration(EvergreenBuilder):

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
            "_functions": {NAME_KEY: "functions", RECURSE_KEY: True},
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
        t = _find_name_in_list(self._tasks, name)
        if t:
            return t

        t = Task(name)
        self._tasks.append(t)
        return t

    def task_group(self, name):
        g = _find_name_in_list(self._groups, name)
        if g:
            return g

        g = TaskGroup(name)
        self._groups.append(g)
        return g

    def function(self, name):
        f = _find_name_in_list(self._functions, name)
        if f:
            return f

        seq = CommandSequence()
        self._functions[name] = seq
        return seq

    def variant(self, name):
        v = _find_name_in_list(self._variants, name)
        if v:
            return v

        v = Variant(name)
        self._variants.append(v)
        return v

    def pre(self, cmds):
        if not self._pre:
            self._pre = CommandSequence()

        self._pre = cmds
        return self

    def post(self, cmds):
        self._post = cmds
        return self

    def exec_timeout(self, duration):
        self._exec_timeout_secs = duration
        return self

    def batch_time(self, duration):
        self._batch_time_secs = duration
        return self

    def stepback(self, stepback):
        self._stepback = stepback
        return self

    def command_type(self, t):
        if t not in ["system", "setup", "task"]:
            raise ValueError("Bad Command Type")
        self._command_type = t
        return self

    def ignore_file(self, filename):
        self._ignore_files.append(filename)
        return self

    def ignore_files(self, filenames):
        self._ignore_files += filenames
        return self

    def to_map(self):
        obj = {}
        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj
