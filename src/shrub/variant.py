from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY


class Variant(EvergreenBuilder):
    def __init__(self, name):
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
            "_build_display_name": {NAME_KEY: "display_name", RECURSE_KEY: False},
            "_batch_time_secs": {NAME_KEY: "batchtime", RECURSE_KEY: False},
            "_task_specs": {NAME_KEY: "tasks", RECURSE_KEY: True},
            "_distro_run_on": {NAME_KEY: "run_on", RECURSE_KEY: False},
            "_expansions": {NAME_KEY: "expansions", RECURSE_KEY: False},
            "_display_task_specs": {NAME_KEY: "display_tasks", RECURSE_KEY: True},
        }

    def get_name(self):
        return self._build_name

    def display_name(self, name):
        self._build_display_name = name
        return self

    def batch_time(self, batch_time_secs):
        self._batch_time_secs = batch_time_secs
        return self

    def run_on(self, distro):
        self._distro_run_on = [distro]
        return self

    def expansions(self, expansions):
        for k in expansions:
            self._expansions[k] = expansions[k]
        return self

    def expansion(self, k, v):
        self._expansions[k] = v
        return self

    def task(self, t):
        self._task_specs.append(t)
        return self

    def tasks(self, tasks):
        self._task_specs += tasks
        return self

    def display_task(self, display_task):
        self._display_task_specs.append(display_task)
        return self

    def display_tasks(self, display_tasks):
        self._display_task_specs += display_tasks
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
        self._stepback = stepback
        return self

    def distro(self, distro):
        self._distro = [distro]


class DisplayTaskDefinition(EvergreenBuilder):
    def __init__(self, name):
        self._name = name
        self._components = []

    def _yaml_map(self):
        return {
            "_name": {NAME_KEY: "name", RECURSE_KEY: False},
            "_components": {NAME_KEY: "execution_tasks", RECURSE_KEY: False},
        }

    def component(self, component):
        self._components.append(component)
        return self

    def components(self, components):
        self._components += components
        return self
