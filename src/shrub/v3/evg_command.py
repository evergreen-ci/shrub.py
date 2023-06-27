"""Evergreen models for commands."""
from enum import Enum
from typing import Any, Dict, Optional, Union, List
from typing_extensions import Literal

from pydantic import BaseModel, Field


AvailableCommands = Literal[
    "archive.targz_extract",
    "archive.targz_pack",
    "archive.auto_extract",
    "attach.artifacts",
    "attach.results",
    "attach.xunit_results",
    "downstream_expansions.set",
    "expansions.update",
    "expansions.write",
    "generate.tasks",
    "git.get_project",
    "gotest.parse_files",
    "host.create",
    "host.list",
    "json.send",
    "keyval.inc",
    "manifest.load",
    "perf.send",
    "s3.get",
    "s3.put",
    "s3Copy.copy",
    "shell.exec",
    "subprocess.exec",
    "subprocess.scripting",
    "timeout.update",
]


class CloudProvider(str, Enum):
    """Cloud provider of a host."""

    EC2 = "ec2"
    DOCKER = "docker"


class S3Visibility(str, Enum):
    """Visibility of an S3 upload."""

    PUBLIC = "public"
    PRIVATE = "private"
    SIGNED = "signed"
    NONE = "none"


class HostScope(str, Enum):
    """When evergreen will tear down a host."""

    TASK = "task"
    BUILD = "build"


class ScriptingHarness(str, Enum):
    """Environment to use to subprocess.scripting."""

    PYTHON = "python"
    PYTHON2 = "python2"
    GOLANG = "golang"
    ROSWELL = "roswell"


class ScriptingTestOptions(BaseModel):
    """
    Options for executing a scripting test.

    * name: the name of the test.
    * args: any additional arguments to the test binary.
    * pattern: filter names of tests to run based on this pattern.
    * timeout_secs: Time to wait before timing out.
    * count: the number of times the test should be run.
    """

    name: Optional[str] = None
    args: Optional[List[str]] = None
    pattern: Optional[str] = None
    timeout_secs: Optional[int] = None
    count: Optional[int] = None


class KeyValueParam(BaseModel):
    """A key/value pair."""

    key: str
    value: str


class S3Location(BaseModel):
    """
    Location of an S3 file.

    * bucket: S3 bucket of file.
    * path: Path to file in bucket.
    """

    bucket: str
    path: str


class S3CopyFile(BaseModel):
    """
    Description of an S3 copy.

    * source: Source file to copy.
    * destination: Destination to place copy.
    * display_name: Display name of copy.
    * build_variants: List of build variants copy applies to.
    * optional: If True, missing source will not trigger a failure.
    """

    source: S3Location
    destination: S3Location
    display_name: Optional[str] = None
    build_variants: Optional[List[str]] = None
    optional: Optional[bool] = None


class EbsDevice(BaseModel):
    """
    EBS block device description.

    * device_name: Name of device.
    * ebs_iops: IOPS provisioned for device.
    * ebs_size: Size provisioned for device.
    * ebs_snapshot_id: ID of snapshot for device.
    """

    device_name: str
    ebs_iops: int
    ebs_size: int
    ebs_snapshot_id: str


class RegistrySettings(BaseModel):
    """
    Description of a registry to pull images from.

    * registry_name: Name of registry.
    * registry_username: User name to access registry with.
    * registry_password: Password to access registry with.
    """

    registry_name: str
    registry_username: Optional[str] = None
    registry_password: Optional[str] = None


class EvgCommandType(str, Enum):
    """How a failure should be represented."""

    TEST = "test"
    SYSTEM = "system"
    SETUP = "setup"


class FunctionCall(BaseModel):
    """
    Make a call to a defined function.

    * func: Name of function to call.
    * vars: Values of variables to use in call.
    * timeout_secs: Timeout to use for function call.
    """

    func: str
    vars: Optional[Dict[str, Any]] = None
    timeout_secs: Optional[int] = None


class BuiltInCommand(BaseModel):
    """
    Make a call to a built-in evergreen command.

    * command: Name of command to call.
    * params: Value of parameters to pass to call.
    * command_type: How failures should be represented.
    * params_yaml: Value of parameters in yaml format.
    """

    command: AvailableCommands
    params: Optional[Dict[str, Any]] = None
    command_type: Optional[EvgCommandType] = Field(None, alias="type")
    params_yaml: Optional[str] = None

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize the built-in command."""
        # We override the constructor here in order to clear out any `None` values in the
        # params.
        if kwargs.get("params") is not None:
            kwargs["params"] = {k: v for k, v in kwargs["params"].items() if v is not None}
        super().__init__(**kwargs)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


EvgCommand = Union[
    FunctionCall,
    BuiltInCommand,
]


# Built in commands


def archive_targz_extract(
    path: str,
    destination: str,
    exclude_files: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to extract an archived tgz file.

    :param path: Path to tgz file.
    :param destination: Location to extract tgz contents to.
    :param exclude_files: List of files that should not be extracted.
    :param command_type: How failures should be reported.
    :return: archive.targz_extract command.
    """
    return BuiltInCommand(
        command="archive.targz_extract",
        params={"path": path, "destination": destination, "exclude_files": exclude_files},
        command_type=command_type,
    )


def archive_targz_pack(
    target: str,
    source_dir: str,
    include: List[str],
    exclude_files: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to create an archived tgz file.

    :param target: Path of tgz file to create.
    :param source_dir: Directory containing files to include in archive.
    :param include: List of globs to include in archive.
    :param exclude_files: List of file to exclude from archive.
    :param command_type: How failures should be reported.
    :return: archive.targz_pack command.
    """
    return BuiltInCommand(
        command="archive.targz_pack",
        params={
            "target": target,
            "source_dir": source_dir,
            "include": include,
            "exclude_files": exclude_files,
        },
        command_type=command_type,
    )


def attach_artifacts(
    files: List[str],
    prefix: Optional[str] = None,
    optional: Optional[bool] = None,
    ignore_artifacts_for_spawn: Optional[bool] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to attach files to the evergreen task results.

    :param files: List of files to attach.
    :param prefix: Path to where files exist.
    :param optional: If True, missing files will not cause a task failure.
    :param ignore_artifacts_for_spawn: Do not include artifacts in spawn hosts.
    :param command_type: How failures should be reported.
    :return: attach.artifacts command.
    """
    return BuiltInCommand(
        command="attach.artifacts",
        params={
            "files": files,
            "prefix": prefix,
            "optional": optional,
            "ignore_artifacts_for_spawn": ignore_artifacts_for_spawn,
        },
        command_type=command_type,
    )


def attach_results(
    file_location: str,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to attach test results to the task results.

    :param file_location: Location of test results to attach.
    :param command_type: How failures should be reported.
    :return: attach.results command.
    """
    return BuiltInCommand(
        command="attach.results",
        params={"file_location": file_location},
        command_type=command_type,
    )


def attach_xunit_results(
    file: Optional[str] = None,
    files: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to attach x-unit test results to the task results.

    :param file: File containing x-unit test results.
    :param files: List of files containing x-unit test results.
    :param command_type: How failures should be reported.
    :return: attach.xunit_results command.
    """
    return BuiltInCommand(
        command="attach.xunit_results",
        params={"file": file, "files": files},
        command_type=command_type,
    )


def downstream_expansions_set(
    file: Optional[str] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command used by parent patches to pass key-value pairs to its children patches.

    :param file: File containg key-value pairs for the child.
    :param command_type: How failures should be reported.
    :return:  downstream_expansions.set command.
    """
    return BuiltInCommand(
        command="downstream_expansions.set",
        params={"file": file},
        command_type=command_type,
    )


def expansions_update(
    updates: Optional[List[KeyValueParam]] = None,
    file: Optional[str] = None,
    ignore_missing_file: Optional[bool] = None,
    env: Optional[Dict[str, str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to update expansions.

    :param updates: List of updates to make.
    :param file: File containing list of updates to make.
    :param ignore_missing_file: If True, a missing file will not cause task failures.
    :param env:
    :param command_type: How failures should be reported.
    :return: expansions.update command.
    """
    return BuiltInCommand(
        command="expansions.update",
        params={
            "updates": updates,
            "file": file,
            "ignore_missing_file": ignore_missing_file,
            "env": env,
        },
        command_type=command_type,
    )


def expansions_write(
    file: str,
    redacted: Optional[bool] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to write expansion definitions to a file.

    :param file: File to write expansions to.
    :param redacted: If True, redacted expansions will be included.
    :param command_type: How failures should be reported.
    :return: expansions.write command.
    """
    return BuiltInCommand(
        command="expansions.write",
        params={"file": file, "redacted": redacted},
        command_type=command_type,
    )


def generate_tasks(
    files: List[str],
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to generate tasks dynamically.

    :param files: List of files containing evergreen json configuration to generate.
    :param command_type: How failures should be reported.
    :return: generate.tasks command.
    """
    return BuiltInCommand(
        command="generate.tasks",
        params={"files": files},
        command_type=command_type,
    )


def git_get_project(
    directory: str,
    token: Optional[str] = None,
    revisions: Optional[Dict[str, str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to get the git repository of a project.

    :param directory: Directory to checkout project to.
    :param token: Token to use to clone the project.
    :param revisions: Map of git hashes to check modules out to.
    :param command_type: How failures should be reported.
    :return: git.get_project command.
    """
    return BuiltInCommand(
        command="git.get_project",
        params={"directory": directory, "token": token, "revisions": revisions},
        command_type=command_type,
    )


def gotest_parse_files(
    files: List[str],
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Parameters to attach gotest test results to the task results.

    :param files: List of files containing gotest test results.
    :param command_type: How failures should be reported.
    :return: gotest.parse_files command.
    """
    return BuiltInCommand(
        command="gotest.parse_files",
        params={"files": files},
        command_type=command_type,
    )


def host_create(
    provider: CloudProvider,
    security_group_ids: List[str],
    file: Optional[str] = None,
    num_hosts: Optional[int] = None,
    retries: Optional[int] = None,
    scope: Optional[HostScope] = None,
    timeout_setup_secs: Optional[int] = None,
    timeout_teardown_secs: Optional[int] = None,
    ami: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    device_name: Optional[str] = None,
    distro: Optional[str] = None,
    ebs_block_device: Optional[EbsDevice] = None,
    instance_type: Optional[str] = None,
    ipv6: Optional[bool] = None,
    region: Optional[str] = None,
    spot: Optional[bool] = None,
    subnet_id: Optional[str] = None,
    userdata_file: Optional[str] = None,
    userdata_command: Optional[str] = None,
    key_name: Optional[str] = None,
    image: Optional[str] = None,
    command: Optional[str] = None,
    publish_ports: Optional[bool] = None,
    registry: Optional[RegistrySettings] = None,
    background: Optional[bool] = None,
    container_wait_timeout_secs: Optional[int] = None,
    pool_frequency_secs: Optional[int] = None,
    stdout_file_name: Optional[str] = None,
    stderr_file_name: Optional[str] = None,
    environment_vars: Optional[Dict[str, str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to create a host.

    :param file: Path to file containing configuration.
    :param num_hosts: Number of hosts to start.
    :param provider: Which provider hosts should be provisioned under.
    :param retries: How many attempts should be made to create the host.
    :param scope: When the host should be torn down.
    :param timeout_setup_secs: Time to wait for setup.
    :param timeout_teardown_secs: Time to wait for teardown.
    :param ami: Amazon AMI to start.
    :param aws_access_key_id: Access key fo AMI
    :param aws_secret_access_key: Secret for AMI.
    :param device_name: Name of EBS device.
    :param distro: Distro to start on host.
    :param ebs_block_device: EBS configuration for host.
    :param instance_type: Type of EC2 instance to start.
    :param ipv6: If True, only use IPV6
    :param region: EC2 regions to start host in.
    :param security_group_ids: List of security groups to configure on host.
    :param spot: If true, use a spot instance.
    :param subnet_id: Subnet ID to use for VPC.
    :param userdata_file: Path to file with userdata to load.
    :param userdata_command:
    :param key_name: EC2 keyname to use.
    :param image: Docker image to use
    :param command: Command to run on docker container
    :param publish_ports: Should ports to exposed from the container.
    :param registry: Docker registry to pull from.
    :param background: If True, Wait for logs in the background.
    :param container_wait_timeout_secs: Time to wait for container to run.
    :param pool_frequency_secs: How frequently to check container logs.
    :param stdout_file_name: Path to write stdout logs from the container.
    :param stderr_file_name: Path to write stderr logs from the container.
    :param environment_vars: Environment to pass to host.
    :param command_type: How failures should be reported.
    :return: host.create command.
    """
    return BuiltInCommand(
        command="host.create",
        params={
            "provider": provider,
            "security_group_ids": security_group_ids,
            "file": file,
            "num_hosts": num_hosts,
            "retries": retries,
            "scope": scope,
            "timeout_setup_secs": timeout_setup_secs,
            "timeout_teardown_secs": timeout_teardown_secs,
            "ami": ami,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "device_name": device_name,
            "distro": distro,
            "ebs_block_device": ebs_block_device,
            "instance_type": instance_type,
            "ipv6": ipv6,
            "region": region,
            "spot": spot,
            "subnet_id": subnet_id,
            "userdata_file": userdata_file,
            "userdata_command": userdata_command,
            "key_name": key_name,
            "image": image,
            "command": command,
            "publish_ports": publish_ports,
            "registry": registry,
            "background": background,
            "container_wait_timeout_secs": container_wait_timeout_secs,
            "pool_frequency_secs": pool_frequency_secs,
            "stdout_file_name": stdout_file_name,
            "stderr_file_name": stderr_file_name,
            "environment_vars": environment_vars,
        },
        command_type=command_type,
    )


def host_list(
    num_hosts: int,
    timeout_seconds: int,
    wait: bool,
    path: Optional[str] = None,
    silent: Optional[bool] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to list hosts.

    :param num_hosts: Number of hosts to wait for before returning.
    :param path: Path to write host details to.
    :param timeout_seconds: Time to wait before timing out.
    :param wait: If True, wait for the given number of hosts to be running before returning.
    :param silent: If True, do not log host info to task logs.
    :param command_type: How failures should be reported.
    :return: host list command.
    """
    return BuiltInCommand(
        command="host.list",
        params={
            "num_hosts": num_hosts,
            "timeout_seconds": timeout_seconds,
            "wait": wait,
            "path": path,
            "silent": silent,
        },
        command_type=command_type,
    )


def json_send(
    file: str,
    name: str,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Send json data to the task results.

    :param file: File containing json data to send.
    :param name: Name of the file to save.
    :param command_type: How failures should be reported.
    :return: json send command.
    """
    return BuiltInCommand(
        command="json.send",
        params={"file": file, "name": name},
        command_type=command_type,
    )


def key_val_inc(
    destination: str,
    key: str,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command for key/val increment.

    :param destination:
    :param key:
    :param command_type: How failures should be reported.
    :return: key/val increment command.
    """
    return BuiltInCommand(
        command="keyval.inc",
        params={"destination": destination, "key": key},
        command_type=command_type,
    )


def perf_send(
    file: str,
    aws_key: str,
    aws_secret: str,
    bucket: str,
    prefix: str,
    region: Optional[str] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Send perf data to cedar.

    :param file: Path to file containing data to send.
    :param aws_key: AWS key to use for authentication.
    :param aws_secret: AWS secret to use for authentication.
    :param bucket: S3 bucket to store data in.
    :param prefix: Location to place file in bucket.
    :param region: AWS region to use.
    :param command_type: How failures should be reported.
    :return: perf.send command.
    """
    return BuiltInCommand(
        command="perf.send",
        params={
            "file": file,
            "aws_key": aws_key,
            "aws_secret": aws_secret,
            "bucket": bucket,
            "prefix": prefix,
            "region": region,
        },
        command_type=command_type,
    )


def s3_get(
    remote_file: str,
    aws_key: str,
    aws_secret: str,
    bucket: str,
    local_file: Optional[str] = None,
    extract_to: Optional[str] = None,
    build_variants: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to get a file from S3.

    :param local_file: Location to save file to.
    :param extract_to: Location to extract file to.
    :param remote_file: Path to file in S3.
    :param aws_key: AWS key to use for authentication.
    :param aws_secret: AWS secret to use for authentication.
    :param bucket: S3 Bucket where file is stored.
    :param build_variants: List of build variants command should be run on.
    :param command_type: How failures should be reported.
    :return: s3.get command.
    """
    return BuiltInCommand(
        command="s3.get",
        params={
            "remote_file": remote_file,
            "aws_key": aws_key,
            "aws_secret": aws_secret,
            "bucket": bucket,
            "local_file": local_file,
            "extract_to": extract_to,
            "build_variants": build_variants,
        },
        command_type=command_type,
    )


def s3_put(
    remote_file: str,
    aws_key: str,
    aws_secret: str,
    bucket: str,
    permissions: str,
    content_type: str,
    local_file: Optional[str] = None,
    local_files_include_filter: Optional[List[str]] = None,
    local_files_include_filter_prefix: Optional[str] = None,
    display_name: Optional[str] = None,
    optional: Optional[bool] = None,
    region: Optional[str] = None,
    visibility: Optional[S3Visibility] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to upload a file to S3.

    :param local_file: List of files to upload.
    :param local_files_include_filter: List of filters to find files to upload.
    :param local_files_include_filter_prefix: Path to apply filter to.
    :param remote_file: Location in S3 to upload files to.
    :param aws_key: AWS key to use for authentication.
    :param aws_secret: AWS secret to use for authentication.
    :param bucket: S3 bucket to upload to.
    :param permissions: Permissions to upload with.
    :param content_type: Content type of files.
    :param display_name: Name to store files under.
    :param optional: If True, missing files will not cause a failure.
    :param region: AWS region to upload to.
    :param visibility: S3 visibility to upload with.
    :param command_type: How failures should be reported.
    :return: s3.put command.
    """
    return BuiltInCommand(
        command="s3.put",
        params={
            "remote_file": remote_file,
            "aws_key": aws_key,
            "aws_secret": aws_secret,
            "bucket": bucket,
            "local_file": local_file,
            "permissions": permissions,
            "content_type": content_type,
            "local_files_include_filter": local_files_include_filter,
            "local_files_include_filter_prefix": local_files_include_filter_prefix,
            "display_name": display_name,
            "optional": optional,
            "region": region,
            "visibility": visibility,
        },
        command_type=command_type,
    )


def s3_copy(
    s3_copy_files: List[S3CopyFile],
    aws_key: str,
    aws_secret: str,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to copy files in S3.

    :param s3_copy_files: Description of how files should be copied.
    :param aws_key: AWS key to use for authentication.
    :param aws_secret: AWS secret to use for authentication.
    :param command_type: How failures should be reported.
    :return: s3.copy command.
    """
    return BuiltInCommand(
        command="s3Copy.copy",
        params={"s3_copy_files": s3_copy_files, "aws_key": aws_key, "aws_secret": aws_secret},
        command_type=command_type,
    )


def shell_exec(
    script: str,
    working_dir: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    add_expansions_to_env: Optional[bool] = None,
    include_expansions_in_env: Optional[List[str]] = None,
    background: Optional[bool] = None,
    silent: Optional[bool] = None,
    continue_on_err: Optional[bool] = None,
    system_log: Optional[bool] = None,
    shell: Optional[str] = None,
    ignore_standard_out: Optional[bool] = None,
    ignore_standard_error: Optional[bool] = None,
    redirect_standard_error_to_output: Optional[bool] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command for executing shell in a task.

    :param script: Contents of script to execute.
    :param working_dir: Directory to execute script in.
    :param env: Environment to run script in.
    :param add_expansions_to_env: Include all expansions in env.
    :param include_expansions_in_env: Expansions that should be included in env.
    :param background: If True, do not wait for script to complete before running next command.
    :param silent: Do not include script output in logs.
    :param continue_on_err: Script failures will not cause task to fail.
    :param system_log: If True, include output in system logs rather than task logs.
    :param shell: Shell to execute script under.
    :param ignore_standard_out: Do not include stdout in logs.
    :param ignore_standard_error: Do not include stderr in logs.
    :param redirect_standard_error_to_output: Redirect stderr to stdout.
    :param command_type: How failures should be reported.
    :return: shell.exec command.
    """
    return BuiltInCommand(
        command="shell.exec",
        params={
            "script": script,
            "working_dir": working_dir,
            "env": env,
            "add_expansions_to_env": add_expansions_to_env,
            "include_expansions_in_env": include_expansions_in_env,
            "background": background,
            "silent": silent,
            "continue_on_err": continue_on_err,
            "system_log": system_log,
            "shell": shell,
            "ignore_standard_out": ignore_standard_out,
            "ignore_standard_error": ignore_standard_error,
            "redirect_standard_error_to_output": redirect_standard_error_to_output,
        },
        command_type=command_type,
    )


def subprocess_exec(
    binary: Optional[str] = None,
    args: Optional[List[str]] = None,
    command: Optional[str] = None,
    working_dir: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    background: Optional[bool] = None,
    shell: Optional[str] = None,
    silent: Optional[bool] = None,
    continue_on_err: Optional[bool] = None,
    system_log: Optional[bool] = None,
    ignore_standard_out: Optional[bool] = None,
    ignore_standard_error: Optional[bool] = None,
    redirect_standard_error_to_output: Optional[bool] = None,
    add_to_path: Optional[List[str]] = None,
    add_expansions_to_env: Optional[bool] = None,
    include_expansions_in_env: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to run subprocess.exec.

    :param binary: Path to binary to execute.
    :param args: List of arguments to pass to binary.
    :param command: Command to execute.
    :param working_dir: Directory to execute from.
    :param env: Environment to run process under.
    :param background: If True, do not wait for script to complete before running next command.
    :param shell: Shell to execute under.
    :param silent: Do not include script output in logs.
    :param continue_on_err: Script failures will not cause task to fail.
    :param system_log: If True, include output in system logs rather than task logs.
    :param ignore_standard_out: Do not include stdout in logs.
    :param ignore_standard_error: Do nog include stderr in logs.
    :param redirect_standard_error_to_output: Redirect stderr to stdout.
    :param add_to_path: List of paths to include in PATH.
    :param add_expansions_to_env: Include all expansions in env.
    :param include_expansions_in_env: Expansions that should be included in env.
    :param command_type: How failures should be reported.
    :return: subprocess.exec command.
    """
    return BuiltInCommand(
        command="subprocess.exec",
        params={
            "binary": binary,
            "args": args,
            "command": command,
            "working_dir": working_dir,
            "env": env,
            "background": background,
            "shell": shell,
            "silent": silent,
            "continue_on_err": continue_on_err,
            "system_log": system_log,
            "ignore_standard_out": ignore_standard_out,
            "ignore_standard_error": ignore_standard_error,
            "redirect_standard_error_to_output": redirect_standard_error_to_output,
            "add_to_path": add_to_path,
            "add_expansions_to_env": add_expansions_to_env,
            "include_expansions_in_env": include_expansions_in_env,
        },
        command_type=command_type,
    )


def subprocess_scripting(
    harness: ScriptingHarness,
    command: Optional[str] = None,
    args: Optional[List[str]] = None,
    test_dir: Optional[str] = None,
    test_options: Optional[ScriptingTestOptions] = None,
    cache_duration_secs: Optional[int] = None,
    cleanup_harness: Optional[bool] = None,
    lock_file: Optional[str] = None,
    packages: Optional[List[str]] = None,
    harness_path: Optional[str] = None,
    silent: Optional[bool] = None,
    continue_on_err: Optional[bool] = None,
    system_log: Optional[bool] = None,
    ignore_standard_out: Optional[bool] = None,
    ignore_standard_error: Optional[bool] = None,
    redirect_standard_error_to_output: Optional[bool] = None,
    add_to_path: Optional[List[str]] = None,
    add_expansions_to_env: Optional[bool] = None,
    include_expansions_in_env: Optional[List[str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to run subprocess.scripting.

    :param harness: Scripting harness to use.
    :param command: Command to run.
    :param args: List of arguments to pass to command.
    :param test_dir: Directory to run from.
    :param test_options: Options to run tests with.
    :param cache_duration_secs: Duration to cache the configuration for.
    :param cleanup_harness: If True, cleanup before the next command runs.
    :param lock_file: Lock file containing required dependencies.
    :param packages: List of packages to install in environment.
    :param harness_path: Path to where harness is located.
    :param args: List of arguments to pass to binary.
    :param command: Command to execute.
    :param silent: Do not include script output in logs.
    :param continue_on_err: Script failures will not cause task to fail.
    :param system_log: If True, include output in system logs rather than task logs.
    :param ignore_standard_out: Do not include stdout in logs.
    :param ignore_standard_error: Do nog include stderr in logs.
    :param redirect_standard_error_to_output: Redirect stderr to stdout.
    :param add_to_path: List of paths to include in PATH.
    :param add_expansions_to_env: Include all expansions in env.
    :param include_expansions_in_env: Expansions that should be included in env.
    :param command_type: How failures should be reported.
    :return: subprocess.scripting command.
    """
    return BuiltInCommand(
        command="subprocess.scripting",
        params={
            "harness": harness,
            "args": args,
            "command": command,
            "test_dir": test_dir,
            "test_options": test_options,
            "cache_duration_secs": cache_duration_secs,
            "cleanup_harness": cleanup_harness,
            "lock_file": lock_file,
            "packages": packages,
            "harness_path": harness_path,
            "silent": silent,
            "continue_on_err": continue_on_err,
            "system_log": system_log,
            "ignore_standard_out": ignore_standard_out,
            "ignore_standard_error": ignore_standard_error,
            "redirect_standard_error_to_output": redirect_standard_error_to_output,
            "add_to_path": add_to_path,
            "add_expansions_to_env": add_expansions_to_env,
            "include_expansions_in_env": include_expansions_in_env,
        },
        command_type=command_type,
    )


def timeout_update(
    exec_timeout_secs: Optional[Union[int, str]] = None,
    timeout_secs: Optional[Union[int, str]] = None,
    command_type: Optional[EvgCommandType] = None,
) -> BuiltInCommand:
    """
    Command to update timeouts.

    :param exec_timeout_secs: Update to make to exec timeout.
    :param timeout_secs: Update to make to idle timeout.
    :param command_type: How failures should be reported.
    :return: timeout update command.
    """
    return BuiltInCommand(
        command="timeout.update",
        params={"exec_timout_secs": exec_timeout_secs, "timeout_secs": timeout_secs},
        command_type=command_type,
    )
