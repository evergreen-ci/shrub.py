from shrub.Task import Task


def _find_name_in_list(list, name):
    for l in list:
        if l.get_name() == name:
            return l

    return None


class Configuration:

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

        seq = CommandSeq()
        self._functions[name] = seq
        return seq

    def variant(self, name):
        v = _find_name_in_list(self._variants, name)
        if v:
            return v

        v = Variant(name)
        self._variants.append(v)
        return v

    def exec_timeout(self, duration):
        self._exec_timeout_secs = duration
        return self

    def batch_time(self, duration):
        self._batch_time_secs = duration
        return self

    def set_command_type(self, t):
        if t not in ["system", "setup", "task"]:
            raise ValueError("Bad Command Type")
        self._command_type = t
        return self
