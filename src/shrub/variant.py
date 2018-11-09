from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY


class Variant(EvergreenBuilder):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Variant only accepts a str")

        self._build_name = name
        self._build_display_name = None
        self._batch_time_secs = None
        self._task_specs = []
        self._distro_run_on = []
        self._expansions = {}
        self._display_task_specs = []

    def _yaml_map(self):
        return {
            "_build_name": {NAME_KEY: "name", RECURSE_KEY: False},
            "_build_display_name": {NAME_KEY: "display_name",
                                    RECURSE_KEY: False},
            "_batch_time_secs": {NAME_KEY: "batchtime", RECURSE_KEY: False},
            "_task_specs": {NAME_KEY: "tasks", RECURSE_KEY: True},
            "_distro_run_on": {NAME_KEY: "run_on", RECURSE_KEY: False},
            "_expansions": {NAME_KEY: "expansions", RECURSE_KEY: False},
            "_display_task_specs": {NAME_KEY: "display_tasks",
                                    RECURSE_KEY: True},
        }

    def get_name(self):
        return self._build_name

    def display_name(self, name):
        if not isinstance(name, str):
            raise TypeError("display_name only accepts a str")

        self._build_display_name = name
        return self

    def batch_time(self, batch_time_secs):
        if not isinstance(batch_time_secs, int):
            raise TypeError("batch_time only accepts an int")

        self._batch_time_secs = batch_time_secs
        return self

    def run_on(self, distro):
        if not isinstance(distro, str):
            raise TypeError("run_on only accepts a str")

        self._distro_run_on = [distro]
        return self

    def expansions(self, expansions):
        if not isinstance(expansions, dict):
            raise TypeError("expansions only accepts a dict")

        for k in expansions:
            self.expansion(k, expansions[k])
        return self

    def expansion(self, k, v):
        if not isinstance(k, str):
            raise TypeError("expansion only accepts a str")

        if not isinstance(v, str):
            raise TypeError("expansion only accepts a str")

        self._expansions[k] = v
        return self

    def task(self, t):
        if not isinstance(t, TaskSpec):
            raise TypeError("task only accepts TaskSpec objects")

        self._task_specs.append(t)
        return self

    def tasks(self, tasks):
        if not isinstance(tasks, list):
            raise TypeError("tasks only accepts a list")

        for t in tasks:
            self.task(t)

        return self

    def display_task(self, display_task):
        if not isinstance(display_task, DisplayTaskDefinition):
            raise TypeError(
                "display_task only accepts a DisplayTaskDefinition")

        self._display_task_specs.append(display_task)
        return self

    def display_tasks(self, display_tasks):
        if not isinstance(display_tasks, list):
            raise TypeError("display_tasks only accepts a list")

        for dt in display_tasks:
            self.display_task(dt)

        return self


class TaskSpec(EvergreenBuilder):
    def __init__(self, name):
        self._name = name
        self._stepback = None
        self._distro = []

    def _yaml_map(self):
        return {
            "_name": {NAME_KEY: "name", RECURSE_KEY: False},
            "_stepback": {NAME_KEY: "stepback", RECURSE_KEY: False},
            "_distro": {NAME_KEY: "distros", RECURSE_KEY: False},
        }

    def stepback(self, stepback):
        if not isinstance(stepback, bool):
            raise TypeError("stepback only accepts a bool")

        self._stepback = stepback
        return self

    def distro(self, distro):
        if not isinstance(distro, str):
            raise TypeError("distro only accepts a str")

        self._distro = [distro]


class DisplayTaskDefinition(EvergreenBuilder):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("DisplayTaskDefinition only accepts a str")

        self._name = name
        self._components = []

    def _yaml_map(self):
        return {
            "_name": {NAME_KEY: "name", RECURSE_KEY: False},
            "_components": {NAME_KEY: "execution_tasks", RECURSE_KEY: False},
        }

    def component(self, component):
        if not isinstance(component, str):
            raise TypeError("component only accepts a str")

        self._components.append(component)
        return self

    def components(self, components):
        if not isinstance(components, list):
            raise TypeError("components only accepts a list")

        for c in components:
            self.component(c)

        return self
