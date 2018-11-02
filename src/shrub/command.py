from shrub.base import EvergreenBuilder
from shrub.base import NAME_KEY
from shrub.base import RECURSE_KEY


class CommandDefinition(EvergreenBuilder):

    def __init__(self):
        self._function_name = None
        self._execution_type = None
        self._display_name = None
        self._command_name = None
        self._timeout = None
        self._variants = []
        self._vars = {}
        self._params = {}

    def _yaml_map(self):
        return {
            "_function_name": {NAME_KEY: "func", RECURSE_KEY: False},
            "_execution_type": {NAME_KEY: "type", RECURSE_KEY: False},
            "_display_name": {NAME_KEY: "display_name", RECURSE_KEY: False},
            "_command_name": {NAME_KEY: "command", RECURSE_KEY: False},
            "_timeout": {NAME_KEY: "timeout_secs", RECURSE_KEY: False},
            "_variants": {NAME_KEY: "variants", RECURSE_KEY: False},
            "_vars": {NAME_KEY: "vars", RECURSE_KEY: False},
            "_params": {NAME_KEY: "params", RECURSE_KEY: False},
        }

    def function(self, fun_name):
        self._function_name = fun_name
        return self

    def type(self, execution_type):
        self._execution_type = execution_type
        return self

    def name(self, name):
        self._display_name = name
        return self

    def command(self, name):
        self._command_name = name
        return self

    def timeout(self, timeout):
        self._timeout = timeout
        return self

    def variant(self, variant):
        self._variants.append(variant)
        return self

    def variants(self, variants):
        self._variants += variants
        return self

    def var(self, k, v):
        self._vars[k] = v
        return self

    def vars(self, vs):
        for k in vs:
            self._vars[k] = vs[k]

        return self

    def param(self, k, v):
        self._params[k] = v
        return self

    def params(self, ps):
        for k in ps:
            self._params[k] = ps[k]

        return self

    def to_map(self):
        obj = {}
        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj


class CommandSequence(EvergreenBuilder):
    def __init__(self):
        self._cmd_seq = []

    def _yaml_map(self):
        return {}

    def len(self):
        return len(self._cmd_seq)

    def command(self):
        c = CommandDefinition()
        self._cmd_seq.append(c)
        return c

    def add(self, cmd):
        self._cmd_seq.append(cmd)
        return self

    def extend(self, cmds):
        self._cmd_seq += cmds
        return self

    def to_map(self):
        return [c.to_map() for c in self._cmd_seq]
