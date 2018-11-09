import pytest

from shrub.operations import ArchiveFormat
from shrub.operations import AwsCopyFile
from shrub.operations import CmdExec
from shrub.operations import CmdExecShell
from shrub.operations import CmdS3Put
from shrub.operations import CmdS3Get
from shrub.operations import CmdS3Copy
from shrub.operations import CmdGetProject
from shrub.operations import CmdResultsJSON
from shrub.operations import CmdResultsXunit
from shrub.operations import CmdResultsGoTest
from shrub.operations import CmdArchiveCreate
from shrub.operations import CmdArchiveExtract
from shrub.operations import CmdAttachArtifacts


def command_name(c):
    return c.resolve().to_map()["command"]


def params(c):
    return c.resolve().to_map()["params"]


class TestCmdExec:
    def test_command_basics(self):
        c = CmdExec()

        assert c.validate()
        assert "subprocess.exec" == command_name(c)

    def test_parameters(self):
        c = CmdExec()
        c.background(True) \
            .silent(True) \
            .continue_on_err(True) \
            .system_log(True) \
            .combine_output(True) \
            .ignore_stderr(True) \
            .ignore_stdout(True) \
            .working_dir("/tmp") \
            .command("echo")\
            .binary("/bin/echo")\
            .arg("arg 0")\
            .args(["arg 1", "arg 2"])\
            .env("k 0", "v 0")\
            .envs({"k 1": "v 1", "k 2": "v 2"})

        p = params(c)
        assert p["background"]
        assert p["silent"]
        assert p["continue_on_err"]
        assert p["system_log"]
        assert p["redirect_standard_error_to_output"]
        assert p["ignore_standard_error"]
        assert p["ignore_standard_out"]
        assert "/tmp" == p["working_dir"]
        assert "echo" == p["command"]
        assert "/bin/echo" == p["binary"]
        assert "arg 0" in p["args"]
        assert "arg 1" in p["args"]
        assert "arg 2" in p["args"]
        assert "v 0" == p["env"]["k 0"]
        assert "v 1" == p["env"]["k 1"]
        assert "v 2" == p["env"]["k 2"]


class TestCmdExecShell:
    def test_command_basics(self):
        c = CmdExecShell()

        assert c.validate()
        assert "shell.exec" == command_name(c)

    def test_parameters(self):
        c = CmdExecShell()
        c.background(True)\
            .silent(True)\
            .continue_on_err(True)\
            .system_log(True)\
            .combine_output(True)\
            .ignore_stderr(True)\
            .ignore_stdout(True)\
            .working_dir("/tmp")\
            .script("echo Hello World")

        p = params(c)
        assert p["background"]
        assert p["silent"]
        assert p["continue_on_err"]
        assert p["system_log"]
        assert p["redirect_standard_error_to_output"]
        assert p["ignore_standard_error"]
        assert p["ignore_standard_out"]
        assert "/tmp" == p["working_dir"]
        assert "echo Hello World" == p["script"]


class TestCmdS3Put:
    def test_command_basics(self):
        c = CmdS3Put()

        assert "s3.put" == command_name(c)

    def test_parameters(self):
        c = CmdS3Put()
        c.aws_key("key") \
            .aws_secret("secret") \
            .optional(True)\
            .remote_file("remote") \
            .bucket("bucket") \
            .local_file("local") \
            .build_variant("var 0") \
            .build_variants(["var 1", "var 2"])\
            .display_name("name")\
            .content_type("ct")\
            .permissions("perms")\
            .visibility("high")\
            .include_filter("*.zip")\
            .include_filters(["*.tgz"])

        p = params(c)
        assert p["optional"]
        assert "name" == p["display_name"]
        assert "ct" == p["content_type"]
        assert "perms" == p["permissions"]
        assert "high" == p["visibility"]
        assert "key" == p["aws_key"]
        assert "secret" == p["aws_secret"]
        assert "remote" == p["remote_file"]
        assert "bucket" == p["bucket"]
        assert "local" == p["local_file"]
        assert "var 0" in p["build_variants"]
        assert "var 1" in p["build_variants"]
        assert "var 2" in p["build_variants"]
        assert "*.zip" in p["local_file_include_filter"]
        assert "*.tgz" in p["local_file_include_filter"]

    def test_validation(self):
        c = CmdS3Put()
        with pytest.raises(ValueError):
            c.validate()

        c.aws_key("key")
        with pytest.raises(ValueError):
            c.validate()

        c.local_file("file")
        assert c.validate()

        c2 = CmdS3Put()
        c2.aws_secret("secret").include_filter("filter")
        assert c2.validate()


class TestCmdS3Get:
    def test_command_basics(self):
        c = CmdS3Get()

        assert c.validate()
        assert "s3.get" == command_name(c)

    def test_parameters(self):
        c = CmdS3Get()
        c.aws_key("key")\
            .aws_secret("secret")\
            .remote_file("remote")\
            .bucket("bucket")\
            .local_file("local")\
            .extract_to("extract")\
            .build_variant("var 0")\
            .build_variants(["var 1", "var 2"])

        p = params(c)
        assert "key" == p["aws_key"]
        assert "secret" == p["aws_secret"]
        assert "remote" == p["remote_file"]
        assert "bucket" == p["bucket"]
        assert "local" == p["local_file"]
        assert "extract" == p["extract_to"]
        assert "var 0" in p["build_variants"]
        assert "var 1" in p["build_variants"]
        assert "var 2" in p["build_variants"]


class TestAwsCopyFile:
    def test_flat_parameters(self):
        cf = AwsCopyFile()
        cf.optional(True)\
            .display_name("name")\
            .build_variant("bv 0")\
            .build_variants(["bv 1", "bv 2"])

        obj = cf.to_map()
        assert obj["optional"]
        assert "name" == obj["display_name"]
        assert "bv 0" in obj["buildvariants"]
        assert "bv 1" in obj["buildvariants"]
        assert "bv 2" in obj["buildvariants"]

    def test_source(self):
        cf = AwsCopyFile()
        cf.source("bucket", "path")

        obj = cf.to_map()
        assert "bucket" == obj["source"]["bucket"]
        assert "path" == obj["source"]["path"]

    def test_destination(self):
        cf = AwsCopyFile()
        cf.destination("bucket", "path")

        obj = cf.to_map()
        assert "bucket" == obj["destination"]["bucket"]
        assert "path" == obj["destination"]["path"]


class TestCmdS3Copy:
    def test_command_basics(self):
        c = CmdS3Copy()

        assert c.validate()
        assert "s3Copy.copy" == command_name(c)

    def test_parameters(self):
        c = CmdS3Copy()
        f0 = AwsCopyFile()\
            .display_name("f0 name")\
            .source("bucket 0", "path 0")\
            .destination("bucket 1", "path 1")
        f1 = AwsCopyFile()\
            .display_name("f1 name")\
            .source("bucket 2", "path 2")\
            .destination("bucket 3", "path 3")
        c.aws_key("aws key").aws_secret("aws secret").file(f0).files([f1])

        p = params(c)
        assert "aws key" == p["aws_key"]
        assert "aws secret" == p["aws_secret"]
        assert "bucket 0" == p["s3_copy_files"][0]["source"]["bucket"]
        assert "path 0" == p["s3_copy_files"][0]["source"]["path"]
        assert "bucket 3" == p["s3_copy_files"][1]["destination"]["bucket"]
        assert "path 3" == p["s3_copy_files"][1]["destination"]["path"]


class TestCmdGetProject:
    def test_command_basics(self):
        c = CmdGetProject()

        assert c.validate()
        assert "git.get_project" == command_name(c)

    def test_parameters(self):
        c = CmdGetProject()
        c.token("token")\
            .directory("src")\
            .revision("k 0", "v 0")\
            .revisions({"k 1": "v 1", "k 2": "v 2"})

        p = params(c)
        assert "token" == p["token"]
        assert "src" == p["directory"]
        assert "v 0" == p["revisions"]["k 0"]
        assert "v 1" == p["revisions"]["k 1"]
        assert "v 2" == p["revisions"]["k 2"]


class TestCmdResultsJSON:
    def test_command_basics(self):
        c = CmdResultsJSON()

        assert c.validate()
        assert "attach.results" == command_name(c)

    def test_parameters(self):
        c = CmdResultsJSON()
        c.file("file")

        p = params(c)
        assert "file" == p["file_location"]


class TestCmdResultsXunit:
    def test_command_basics(self):
        c = CmdResultsXunit()

        assert c.validate()
        assert "attach.xunit_results" == command_name(c)

    def test_parameters(self):
        c = CmdResultsXunit()
        c.file("file")

        p = params(c)
        assert "file" == p["file"]


class TestCmdResultsGoTest:
    def test_command_basics_json(self):
        c = CmdResultsGoTest(json=True)

        assert c.validate()
        assert "gotest.parse_json" == command_name(c)

    def test_command_basics_legacy(self):
        c = CmdResultsGoTest(legacy=True)

        assert c.validate()
        assert "gotest.parse_files" == command_name(c)

    def test_command_basics_both(self):
        c = CmdResultsGoTest(legacy=True, json=True)

        with pytest.raises(ValueError):
            c.validate()

    def test_command_basics_none(self):
        c = CmdResultsGoTest()

        with pytest.raises(ValueError):
            c.validate()

    def test_parameters(self):
        c = CmdResultsGoTest(json=True)
        c.file("file 0").files(["file 1", "file 2"])

        p = params(c)
        assert "file 0" in p["files"]
        assert "file 1" in p["files"]
        assert "file 2" in p["files"]


class TestCmdArchiveCreate:
    def test_command_basics_zip(self):
        c = CmdArchiveCreate(ArchiveFormat.zip())

        assert c.validate()
        assert "archive.zip_pack" == command_name(c)

    def test_command_basics_tar(self):
        c = CmdArchiveCreate(ArchiveFormat.tar())

        assert c.validate()
        assert "archive.targz_pack" == command_name(c)

    def test_command_throws_with_invalid_type(self):
        with pytest.raises(ValueError):
            CmdArchiveCreate(ArchiveFormat.auto()).validate()

    def test_parameters(self):
        c = CmdArchiveCreate(ArchiveFormat.zip())
        c.target("target")\
            .source_dir("src")\
            .include("include 0")\
            .includes(["include 1", "include 2"])\
            .exclude("exclude 0")\
            .excludes(["exclude 1", "exclude 2"])

        p = params(c)

        assert "target" == p["target"]
        assert "src" == p["source_dir"]
        assert "include 0" in p["include"]
        assert "include 1" in p["include"]
        assert "include 2" in p["include"]
        assert "exclude 0" in p["exclude_files"]
        assert "exclude 1" in p["exclude_files"]
        assert "exclude 2" in p["exclude_files"]


class TestCmdArchiveExtract:
    def test_command_basics_zip(self):
        c = CmdArchiveExtract(ArchiveFormat.zip())

        assert c.validate()
        assert "archive.zip_extract" == command_name(c)

    def test_command_basics_tar(self):
        c = CmdArchiveExtract(ArchiveFormat.tar())

        assert c.validate()
        assert "archive.targz_extract" == command_name(c)

    def test_command_basics_auto(self):
        c = CmdArchiveExtract(ArchiveFormat.auto())

        assert c.validate()
        assert "archive.auto_extract" == command_name(c)

    def test_command_throws_with_invalid_type(self):
        with pytest.raises(ValueError):
            CmdArchiveExtract(ArchiveFormat("invalid")).validate()

    def test_parameters(self):
        c = CmdArchiveExtract(ArchiveFormat.zip())
        c.path("path")\
            .target("target")\
            .exclude("exclude 0")\
            .excludes(["exclude 1", "exclude 2"])

        p = params(c)

        assert "path" == p["path"]
        assert "target" == p["destination"]
        assert "exclude 0" in p["exclude_files"]
        assert "exclude 1" in p["exclude_files"]
        assert "exclude 2" in p["exclude_files"]


class TestCmdAttachArtifacts:
    def test_command_basics(self):
        c = CmdAttachArtifacts()

        assert "attach.artifacts" == command_name(c)
        assert c.validate()

    def test_params(self):
        c = CmdAttachArtifacts()
        c.optional(True).file("file 0").files(["file 1", "file 2"])

        p = params(c)
        assert p["optional"]
        assert "file 0" in p["files"]
        assert "file 1" in p["files"]
        assert "file 2" in p["files"]
