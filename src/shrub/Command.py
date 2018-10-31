class CommandDefinition:

    def __init__(self):
        self.function_name = ""
        self.execution_type = ""
        self.display_name = ""
        self.command_name = ""
        self.timeout = 0
        self.variants = []
        self.vars = {}
        self.params = {}

    def validate(self):
        return self

    def resolve(self):
        return self

    def function(self, fun_name):
        self.function_name = fun_name
        return self

    def type(self, execution_type):
        self.execution_type = execution_type
        return self

    def name(self, name):
        self.display_name = name
        return self

    def command(self, name):
        self.command_name = name
        return self

    def timeout(self, timeout):
        self.timeout = timeout
        return self

    def variants(self, variants):
        self.variants += variants
        return self

    def reset_vars(self):
        self.vars = {}
        return self

    def reset_params(self):
        self.params = {}
        return self

    def replace_vars(self, new_vars):
        self.vars = new_vars
        return self

    def replace_params(self, new_params):
        self.params = new_params
        return self

    def param(self, k, v):
        self.params[k] = v
        return self

    def extend_params(self, ps):
        for k, v in ps:
            self.params[k] = v

        return self

    def var(self, k, v):
        self.vars[k] = v
        return self

    def extend_vars(self, vs):
        for k, v in vs:
            self.vars[k] = v

        return self


class CommandSequence:
    def __init__(self, cs=[]):
        self.cmd_seq = cs

    def len(self):
        return len(self.cmd_seq)

    def command(self):
        c = CommandDefinition()
        self.cmd_seq.append(c)
        return c

    def add(self, cmd):
        self.cmd_seq.append(cmd)
        return self

    def extend(self, cmds):
        self.cmd_seq += cmds
        return self
