"""Unit tests for evg_command.py."""

import shrub.v3.evg_command as under_test


class TestBuiltInCommands:
    def test_specifying_params(self):
        cmd = under_test.git_get_project(
            directory="src", command_type=under_test.EvgCommandType.SYSTEM
        )

        assert cmd.command == "git.get_project"
        assert cmd.params["directory"] == "src"
        assert cmd.command_type == under_test.EvgCommandType.SYSTEM

    def test_specifying_params_again(self):
        cmd = under_test.timeout_update(timeout_secs=60)

        assert cmd.command == "timeout.update"
        assert cmd.params["timeout_secs"] == 60

    def test_expansions_update(self):
        cmd = under_test.expansions_update(
            updates=[under_test.KeyValueParam(key=f"key_{i}", value=f"value_{i}") for i in range(5)]
        )

        assert cmd.dict(exclude_none=True, exclude_unset=True) == {
            "command": "expansions.update",
            "params": {
                "updates": [
                    {"key": "key_0", "value": "value_0"},
                    {"key": "key_1", "value": "value_1"},
                    {"key": "key_2", "value": "value_2"},
                    {"key": "key_3", "value": "value_3"},
                    {"key": "key_4", "value": "value_4"},
                ]
            },
        }
