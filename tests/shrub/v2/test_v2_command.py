"""Unit tests for shrub.v2.command.py."""
import pytest

import shrub.v2.command as under_test


class TestS3Get:
    def test_no_destination(self):
        with pytest.raises(TypeError):
            under_test.s3_get("aws_key", "aws_secret", "remote_file", "bucket")

    def test_both_local_file_and_extract_to(self):
        with pytest.raises(TypeError):
            under_test.s3_get(
                "aws_key",
                "aws_secret",
                "remote_file",
                "bucket",
                local_file="local_file",
                extract_to="extract.here",
            )

    def test_using_local_file(self):
        command = under_test.s3_get(
            "aws_key",
            "aws_secret",
            "remote_file",
            "bucket",
            local_file="local_file",
        )

        d = command.as_dict()
        assert d["command"] == "s3.get"
        assert d["params"]["local_file"] == "local_file"

    def test_using_extract_to(self):
        command = under_test.s3_get(
            "aws_key",
            "aws_secret",
            "remote_file",
            "bucket",
            extract_to="extract to",
        )

        d = command.as_dict()
        assert d["command"] == "s3.get"
        assert d["params"]["extract_to"] == "extract to"


class TestS3Put:
    def test_no_input(self):
        with pytest.raises(TypeError):
            under_test.s3_put(
                "aws_key", "aws_secret", "remote_file", "bucket", "permissions", "content_type"
            )

    def test_both_inputs(self):
        with pytest.raises(TypeError):
            under_test.s3_put(
                "aws_key",
                "aws_secret",
                "remote_file",
                "bucket",
                "permissions",
                "content_type",
                local_file="local_file",
                local_files_include_filter="filter",
            )

    def test_local_file(self):
        command = under_test.s3_put(
            "aws_key",
            "aws_secret",
            "remote_file",
            "bucket",
            "permissions",
            "content_type",
            local_file="local_file",
            optional=True,
        )

        d = command.as_dict()
        assert d["command"] == "s3.put"
        assert d["params"]["local_file"] == "local_file"

    def test_local_file_with_prefix(self):
        with pytest.raises(TypeError):
            under_test.s3_put(
                "aws_key",
                "aws_secret",
                "remote_file",
                "bucket",
                "permissions",
                "content_type",
                local_file="local_file",
                local_files_include_filter_prefix="prefix",
            )

    def test_file_filter(self):
        command = under_test.s3_put(
            "aws_key",
            "aws_secret",
            "remote_file",
            "bucket",
            "permissions",
            "content_type",
            local_files_include_filter="filter",
            local_files_include_filter_prefix="prefix",
        )

        d = command.as_dict()
        assert d["command"] == "s3.put"
        assert d["params"]["local_files_include_filter"] == "filter"
        assert d["params"]["local_files_include_filter_prefix"] == "prefix"

    def test_file_filter_with_optional(self):
        with pytest.raises(TypeError):
            under_test.s3_put(
                "aws_key",
                "aws_secret",
                "remote_file",
                "bucket",
                "permissions",
                "content_type",
                local_files_include_filter="filter",
                optional=True,
            )


class TestS3Copy:
    def test_s3_copy_command(self):
        command = under_test.s3_copy(
            "aws_key",
            "aws_secret",
            [
                under_test.S3CopyFile(
                    "source_bucket",
                    "source_path",
                    "dest_bucket",
                    "dest_path",
                ),
                under_test.S3CopyFile(
                    "source_bucket 2",
                    "source_path 2",
                    "dest_bucket 2",
                    "dest_path 2",
                ),
            ],
        )

        d = command.as_dict()

        assert d["command"] == "s3Copy.copy"
        assert len(d["params"]["s3_copy_files"]) == 2
        assert d["params"]["s3_copy_files"][1]["source"]["path"] == "source_path 2"


class TestSubprocessExec:
    def test_no_options(self):
        with pytest.raises(TypeError):
            under_test.subprocess_exec()

    def test_binary_and_command(self):
        with pytest.raises(TypeError):
            under_test.subprocess_exec(binary="binary", command="command")

    def test_command_with_args(self):
        with pytest.raises(TypeError):
            under_test.subprocess_exec(command="command", args=["one", "two", "three"])

    def test_binary_option(self):
        command = under_test.subprocess_exec(binary="binary", args=["one", "two", "three"])

        d = command.as_dict()

        assert d["command"] == "subprocess.exec"
        assert d["params"]["binary"] == "binary"
        assert len(d["params"]["args"]) == 3

    def test_command_option(self):
        command = under_test.subprocess_exec(command="command")

        d = command.as_dict()

        assert d["command"] == "subprocess.exec"
        assert d["params"]["command"] == "command"
