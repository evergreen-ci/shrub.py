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
        if not isinstance(fun_name, str):
            raise TypeError("function only accepts a str")

        self._function_name = fun_name
        return self

    def type(self, execution_type):
        if not isinstance(execution_type, str):
            raise TypeError("type only accepts a str")

        self._execution_type = execution_type
        return self

    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name only accepts a str")

        self._display_name = name
        return self

    def command(self, name):
        if not isinstance(name, str):
            raise TypeError("command only accepts a str")

        self._command_name = name
        return self

    def timeout(self, timeout):
        if not isinstance(timeout, int):
            raise TypeError("timeout only accepts an int")

        self._timeout = timeout
        return self

    def variant(self, variant):
        if not isinstance(variant, str):
            raise TypeError("variant only accepts a str")

        self._variants.append(variant)
        return self

    def variants(self, variants):
        if not isinstance(variants, list):
            raise TypeError("variants only accepts a list")

        for v in variants:
            self.variant(v)

        return self

    def var(self, k, v):
        if not isinstance(k, str):
            raise TypeError("var only accepts a str")

        self._vars[k] = v
        return self

    def vars(self, vs):
        if not isinstance(vs, dict):
            raise TypeError("vars only accepts a dict")

        for k in vs:
            self.var(k, vs[k])

        return self

    def param(self, k, v):
        if not isinstance(k, str):
            raise TypeError("param only accepts a str")

        self._params[k] = v
        return self

    def params(self, ps):
        if not isinstance(ps, dict):
            raise TypeError("params only accepts a dict")

        for k in ps:
            self.param(k, ps[k])

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
        if not isinstance(cmd, CommandDefinition):
            raise TypeError("add only accepts a CommandDefinition")

        self._cmd_seq.append(cmd)
        return self

    def extend(self, cmds):
        if not isinstance(cmds, list):
            raise TypeError("extend only accepts a list")

        for c in cmds:
            self.add(c)

        return self

    def to_map(self):
        return [c.to_map() for c in self._cmd_seq]
