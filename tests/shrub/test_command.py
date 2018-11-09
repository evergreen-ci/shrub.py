import pytest

from shrub.command import CommandDefinition
from shrub.command import CommandSequence


class TestCommandDefinition:
    def test_empty_command_definition(self):
        cd = CommandDefinition()

        assert {} == cd.to_map()

    def test_flat_values_in_map(self):
        cd = CommandDefinition()
        cd.function("function name") \
            .type("test") \
            .name("display name") \
            .command("command name") \
            .timeout(300)

        obj = cd.to_map()
        assert "function name" == obj["func"]
        assert "test" == obj["type"]
        assert "display name" == obj["display_name"]
        assert "command name" == obj["command"]
        assert 300 == obj["timeout_secs"]

    def test_variants_can_be_added(self):
        cd = CommandDefinition()
        cd.variant("variant 0").variants(["variant 1", "variant 2"])

        obj = cd.to_map()
        assert "variant 0" in obj["variants"]
        assert "variant 1" in obj["variants"]
        assert "variant 2" in obj["variants"]

    def test_variables_can_be_added(self):
        cd = CommandDefinition()
        cd.var("x", 5).vars({"y": 6, "z": 7})

        obj = cd.to_map()
        assert 5 == obj["vars"]["x"]
        assert 6 == obj["vars"]["y"]
        assert 7 == obj["vars"]["z"]

    def test_parameters_can_be_added(self):
        cd = CommandDefinition()
        cd.param("x", 5).params({"y": 6, "z": 7})

        obj = cd.to_map()
        assert 5 == obj["params"]["x"]
        assert 6 == obj["params"]["y"]
        assert 7 == obj["params"]["z"]

    def test_invalid_stepback(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.function(42)

    def test_invalid_type(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.type(42)

    def test_invalid_name(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.name(42)

    def test_invalid_command(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.command(42)

    def test_invalid_timeout(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.timeout("hello world")

    def test_invalid_variant(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.variant(42)

    def test_invalid_variants(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.variants(42)

    def test_invalid_var(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.var(42, 'v')

    def test_invalid_vars(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.vars(42)

    def test_invalid_param(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.param(42, 'v')

    def test_invalid_params(self):
        cd = CommandDefinition()
        with pytest.raises(TypeError):
            cd.params(42)


class TestCommandSequence:

    def test_invalid_add(self):
        cs = CommandSequence()
        with pytest.raises(TypeError):
            cs.add("hello world")

    def test_invalid_extend(self):
        cs = CommandSequence()
        with pytest.raises(TypeError):
            cs.extend("hello world")
