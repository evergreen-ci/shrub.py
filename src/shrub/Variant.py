
class Variant:
    def __init__(self, name):
        self._build_name = name
        self._build_display_name = None
        self._batch_time_secs = None
        self._task_specs = []
        self._distro_runs_on = []
        self._expansions = []
        self._display_task_specs = []

        self._yaml_map = {
            "_build_display_name": "display_name",
            "_batch_time_secs": "batchtime",
            "_task_specs": "tasks",
            "_distro_runs_on": "run_on",
            "_expansions": "expansions",
            "_display_task_specs": "display_tasks",
        }

    def get_name(self):
        return self._build_name

    def name(self, name):
        self._build_name = name
        return self

    def display_name(self, name):
        self._build_display_name = name
        return self

    def run_on(self, distro):
        self._distro_runs_on = [distro]
        return self

    def task_spec(self, spec):
        self._task_specs.append(spec)
        return self

    def set_expansions(self, expansions):
        self._expansions = expansions
        return self

    def expansion(self, k, v):
        self._expansions[k] = v
        return self

    def add_tasks(self, names):
        for name in [name for name in names if names != ""]:
            self._task_specs.append(TaskSpec(name))

    def display_tasks(self, display_task):
        self._display_task_specs.append(display_task)
        return self

    def _add_if_defined(self, obj, prop):
        value = getattr(self, prop)
        if value and len(value) > 0:
            obj[self._yaml_map[prop]] = value

    def to_obj(self):
        obj = {}

        self._add_if_defined(obj, "_build_name")
        self._add_if_defined(obj, "_build_display_name")
        self._add_if_defined(obj, "_batch_time_secs")
        self._add_if_defined(obj, "_task_specs")
        self._add_if_defined(obj, "_distro_runs_on")
        self._add_if_defined(obj, "_expansions")
        self._add_if_defined(obj, "_display_task_specs")

        return obj


class TaskSpec:
    def __init__(self, name):
        self._name = name
        self._stepback = None
        self._distro = []


class DisplayTaskDefinition:
    def __init__(self):
        self._name = ""
        self._components = []
