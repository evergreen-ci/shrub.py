"""Unit tests for evg_command.py."""

import shrub.v3.evg_command as under_test


class TestCacheRestore:
    def test_required_params(self):
        cmd = under_test.cache_restore(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}-${revision}"],
        )

        assert cmd.command == "cache.restore"
        assert cmd.params["name"] == "my-cache"
        assert cmd.params["bucket"] == "my-bucket"
        assert cmd.params["remote_path"] == "path/to/cache"
        assert cmd.params["key_expansions"] == ["${task_name}-${revision}"]

    def test_optional_params(self):
        cmd = under_test.cache_restore(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            key_files=["go.sum"],
            aws_key="${aws_key}",
            aws_secret="${aws_secret}",
            aws_session_token="${aws_token}",
            region="us-west-2",
        )

        assert cmd.params["key_files"] == ["go.sum"]
        assert cmd.params["aws_key"] == "${aws_key}"
        assert cmd.params["aws_secret"] == "${aws_secret}"
        assert cmd.params["aws_session_token"] == "${aws_token}"
        assert cmd.params["region"] == "us-west-2"

    def test_role_arn(self):
        cmd = under_test.cache_restore(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            role_arn="arn:aws:iam::123456789012:role/my-role",
        )

        assert cmd.params["role_arn"] == "arn:aws:iam::123456789012:role/my-role"

    def test_command_type(self):
        cmd = under_test.cache_restore(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            command_type=under_test.EvgCommandType.SYSTEM,
        )

        assert cmd.type == under_test.EvgCommandType.SYSTEM


class TestCacheSave:
    def test_required_params(self):
        cmd = under_test.cache_save(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}-${revision}"],
            paths=["src", "vendor"],
        )

        assert cmd.command == "cache.save"
        assert cmd.params["name"] == "my-cache"
        assert cmd.params["bucket"] == "my-bucket"
        assert cmd.params["remote_path"] == "path/to/cache"
        assert cmd.params["key_expansions"] == ["${task_name}-${revision}"]
        assert cmd.params["paths"] == ["src", "vendor"]

    def test_optional_params(self):
        cmd = under_test.cache_save(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            paths=["src"],
            key_files=["go.sum"],
            aws_key="${aws_key}",
            aws_secret="${aws_secret}",
            aws_session_token="${aws_token}",
            region="us-west-2",
        )

        assert cmd.params["key_files"] == ["go.sum"]
        assert cmd.params["aws_key"] == "${aws_key}"
        assert cmd.params["aws_secret"] == "${aws_secret}"
        assert cmd.params["aws_session_token"] == "${aws_token}"
        assert cmd.params["region"] == "us-west-2"

    def test_role_arn(self):
        cmd = under_test.cache_save(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            paths=["src"],
            role_arn="arn:aws:iam::123456789012:role/my-role",
        )

        assert cmd.params["role_arn"] == "arn:aws:iam::123456789012:role/my-role"

    def test_command_type(self):
        cmd = under_test.cache_save(
            name="my-cache",
            bucket="my-bucket",
            remote_path="path/to/cache",
            key_expansions=["${task_name}"],
            paths=["src"],
            command_type=under_test.EvgCommandType.SYSTEM,
        )

        assert cmd.type == under_test.EvgCommandType.SYSTEM


class TestBuiltInCommands:
    def test_specifying_params(self):
        cmd = under_test.git_get_project(
            directory="src", command_type=under_test.EvgCommandType.SYSTEM
        )

        assert cmd.command == "git.get_project"
        assert cmd.params["directory"] == "src"
        assert cmd.type == under_test.EvgCommandType.SYSTEM

    def test_specifying_params_again(self):
        cmd = under_test.timeout_update(timeout_secs=60)

        assert cmd.command == "timeout.update"
        assert cmd.params["timeout_secs"] == 60

    def test_expansions_update(self):
        cmd = under_test.expansions_update(
            updates=[under_test.KeyValueParam(key=f"key_{i}", value=f"value_{i}") for i in range(5)]
        )

        assert cmd.model_dump(exclude_none=True, exclude_unset=True) == {
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

    def test_display_name(self):
        """Test that the display_name property is serialized"""
        cmd = under_test.BuiltInCommand(
            command="subprocess.exec",
            params={},
            type="setup",
            display_name="foo",
        )
        data = cmd.model_dump(exclude_none=True)
        assert data == {
            "command": "subprocess.exec",
            "params": {},
            "type": "setup",
            "display_name": "foo",
        }
