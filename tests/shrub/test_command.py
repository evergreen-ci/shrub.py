from shrub.command import CommandDefinition


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
