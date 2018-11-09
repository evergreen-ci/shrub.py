import abc

from shrub.command import CommandDefinition


ARCHIVE_FORMAT_ZIP = 'zip'
ARCHIVE_FORMAT_TAR = 'tarball'
ARCHIVE_FORMAT_AUTO = 'auto'


class EvergreenCommand:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self):
        """Ensure the command is valid."""

    @abc.abstractmethod
    def _command_type(self):
        """Return the type of this command."""

    @abc.abstractmethod
    def _param_list(self):
        """Return a map of the params supported by this command."""

    def _export_params(self):
        """Return a map of the parameters for this command."""
        obj = {}
        self._add_defined_attribs(obj, self._param_list().keys())
        return obj

    def _add_if_defined(self, obj, prop):
        """Add the specified property to the given object if it exists."""
        value = getattr(self, prop)
        if value:
            obj[self._param_list()[prop]] = value

    def _add_defined_attribs(self, obj, attrib_list):
        """Add any defined attributes in the given list to the given map."""
        for attrib in attrib_list:
            self._add_if_defined(obj, attrib)

    def resolve(self):
        """Create a CommandDefinition from this object."""
        cmd = CommandDefinition().command(self._command_type())
        return cmd.params(self._export_params())


class CmdExec(EvergreenCommand):
    def __init__(self):
        self._background = False
        self._silent = False
        self._continue_on_err = False
        self._system_log = False
        self._combine_output = False
        self._ignore_stderr = False
        self._ignore_stdout = False
        self._keep_empty_args = False
        self._working_dir = None
        self._command = None
        self._binary = None
        self._args = []
        self._env = {}

    def _command_type(self):
        return 'subprocess.exec'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_background': 'background',
            '_silent': 'silent',
            '_continue_on_err': 'continue_on_err',
            '_system_log': 'system_log',
            '_combine_output': 'redirect_standard_error_to_output',
            '_ignore_stderr': 'ignore_standard_error',
            '_ignore_stdout': 'ignore_standard_out',
            '_working_dir': 'working_dir',
            '_command': 'command',
            '_binary': 'binary',
            '_args': 'args',
            '_env': 'env',
        }

    def background(self, background):
        self._background = background
        return self

    def silent(self, silent):
        self._silent = silent
        return self

    def continue_on_err(self, cont):
        self._continue_on_err = cont
        return self

    def system_log(self, log):
        self._system_log = log
        return self

    def combine_output(self, combine):
        self._combine_output = combine
        return self

    def ignore_stderr(self, ignore):
        self._ignore_stderr = ignore
        return self

    def ignore_stdout(self, ignore):
        self._ignore_stdout = ignore
        return self

    def working_dir(self, working_dir):
        self._working_dir = working_dir
        return self

    def command(self, command):
        self._command = command
        return self

    def binary(self, binary):
        self._binary = binary
        return self

    def arg(self, arg):
        self._args.append(arg)
        return self

    def args(self, args):
        self._args += args
        return self

    def env(self, k, v):
        self._env[k] = v
        return self

    def envs(self, kvs):
        for k in kvs:
            self._env[k] = kvs[k]

        return self


class CmdExecShell(EvergreenCommand):
    def __init__(self):
        self._background = False
        self._silent = False
        self._continue_on_err = False
        self._system_log = False
        self._combine_output = False
        self._ignore_stderr = False
        self._ignore_stdout = False
        self._working_directory = None
        self._script = None

    def _command_type(self):
        return 'shell.exec'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_background': 'background',
            '_silent': 'silent',
            '_continue_on_err': 'continue_on_err',
            '_system_log': 'system_log',
            '_combine_output': 'redirect_standard_error_to_output',
            '_ignore_stderr': 'ignore_standard_error',
            '_ignore_stdout': 'ignore_standard_out',
            '_working_directory': 'working_dir',
            '_script': 'script',
        }

    def background(self, background):
        self._background = background
        return self

    def silent(self, silent):
        self._silent = silent
        return self

    def continue_on_err(self, cont):
        self._continue_on_err = cont
        return self

    def system_log(self, log):
        self._system_log = log
        return self

    def combine_output(self, combine):
        self._combine_output = combine
        return self

    def ignore_stderr(self, ignore):
        self._ignore_stderr = ignore
        return self

    def ignore_stdout(self, ignore):
        self._ignore_stdout = ignore
        return self

    def working_dir(self, working_dir):
        self._working_directory = working_dir
        return self

    def script(self, script):
        self._script = script
        return self


class CmdS3Put(EvergreenCommand):
    def __init__(self):
        self._optional = False
        self._local_file = None
        self._local_file_include_filter = []
        self._bucket = None
        self._remote_file = None
        self._display_name = None
        self._content_type = None
        self._aws_key = None
        self._aws_secret = None
        self._permissions = None
        self._visibility = None
        self._build_variants = []

    def _command_type(self):
        return 's3.put'

    def validate(self):
        if not self._aws_key and not self._aws_secret:
            raise ValueError('must specify aws credentials')

        if not self._local_file and len(self._local_file_include_filter) == 0:
            raise ValueError('must specify a local file to upload')

        return self

    def _param_list(self):
        return {
            '_optional': 'optional',
            '_local_file': 'local_file',
            '_local_file_include_filter': 'local_file_include_filter',
            '_bucket': 'bucket',
            '_remote_file': 'remote_file',
            '_display_name': 'display_name',
            '_content_type': 'content_type',
            '_aws_key': 'aws_key',
            '_aws_secret': 'aws_secret',
            '_permissions': 'permissions',
            '_visibility': 'visibility',
            '_build_variants': 'build_variants',
        }

    def optional(self, opt):
        self._optional = opt
        return self

    def local_file(self, file):
        self._local_file = file
        return self

    def include_filter(self, f):
        self._local_file_include_filter.append(f)
        return self

    def include_filters(self, filters):
        self._local_file_include_filter += filters
        return self

    def bucket(self, b):
        self._bucket = b
        return self

    def remote_file(self, f):
        self._remote_file = f
        return self

    def display_name(self, name):
        self._display_name = name
        return self

    def content_type(self, ct):
        self._content_type = ct
        return self

    def aws_key(self, key):
        self._aws_key = key
        return self

    def aws_secret(self, secret):
        self._aws_secret = secret
        return self

    def permissions(self, perm):
        self._permissions = perm
        return self

    def visibility(self, vis):
        self._visibility = vis
        return self

    def build_variant(self, bv):
        self._build_variants.append(bv)
        return self

    def build_variants(self, bvs):
        self._build_variants += bvs
        return self


class CmdS3Get(EvergreenCommand):
    def __init__(self):
        self._aws_key = None
        self._aws_secret = None
        self._remote_file = None
        self._bucket = None
        self._local_file = None
        self._extract_to = None
        self._build_variants = []

    def _command_type(self):
        return 's3.get'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_aws_key': 'aws_key',
            '_aws_secret': 'aws_secret',
            '_remote_file': 'remote_file',
            '_bucket': 'bucket',
            '_local_file': 'local_file',
            '_extract_to': 'extract_to',
            '_build_variants': 'build_variants',
        }

    def aws_key(self, key):
        self._aws_key = key
        return self

    def aws_secret(self, secret):
        self._aws_secret = secret
        return self

    def remote_file(self, file):
        self._remote_file = file
        return self

    def bucket(self, bucket):
        self._bucket = bucket
        return self

    def local_file(self, file):
        self._local_file = file
        return self

    def extract_to(self, to):
        self._extract_to = to
        return self

    def build_variant(self, bv):
        self._build_variants.append(bv)
        return self

    def build_variants(self, bvs):
        self._build_variants += bvs
        return self


class AwsCopyFile:
    def __init__(self):
        self._optional = False
        self._display_name = None
        self._build_variants = []
        self._source = {}
        self._destination = {}

    def optional(self, opt):
        self._optional = opt
        return self

    def display_name(self, name):
        self._display_name = name
        return self

    def build_variant(self, bv):
        self._build_variants.append(bv)
        return self

    def build_variants(self, bvs):
        self._build_variants += bvs
        return self

    def source(self, bucket, path):
        self._source = {
            'bucket': bucket,
            'path': path,
        }
        return self

    def destination(self, bucket, path):
        self._destination = {
            'bucket': bucket,
            'path': path,
        }
        return self

    def to_map(self):
        obj = {}
        if self._optional:
            obj['optional'] = self._optional
        if self._display_name:
            obj['display_name'] = self._display_name
        if self._build_variants:
            obj['buildvariants'] = self._build_variants
        if self._source:
            obj['source'] = self._source
        if self._destination:
            obj['destination'] = self._destination

        return obj


class CmdS3Copy(EvergreenCommand):
    def __init__(self):
        self._aws_key = None
        self._aws_secret = None
        self._files = []

    def _command_type(self):
        return 's3Copy.copy'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_aws_key': 'aws_key',
            '_aws_secret': 'aws_secret',
        }

    def _export_params(self):
        obj = super(CmdS3Copy, self)._export_params()
        if self._files:
            obj['s3_copy_files'] = [f.to_map() for f in self._files]

        return obj

    def aws_key(self, key):
        self._aws_key = key
        return self

    def aws_secret(self, secret):
        self._aws_secret = secret
        return self

    def file(self, file):
        self._files.append(file)
        return self

    def files(self, files):
        self._files += files
        return self


class CmdGetProject(EvergreenCommand):
    def __init__(self):
        self._token = None
        self._dir = None
        self._revisions = {}

    def _command_type(self):
        return 'git.get_project'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_token': 'token',
            '_dir': 'directory',
            '_revisions': 'revisions',
        }

    def token(self, token):
        self._token = token
        return self

    def directory(self, dir):
        self._dir = dir
        return self

    def revision(self, k, v):
        self._revisions[k] = v
        return self

    def revisions(self, revs):
        for k in revs:
            self._revisions[k] = revs[k]

        return self


class CmdResultsJSON(EvergreenCommand):
    def __init__(self):
        self._file = None

    def _command_type(self):
        return 'attach.results'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_file': 'file_location'
        }

    def file(self, file):
        self._file = file
        return self


class CmdResultsXunit(EvergreenCommand):
    def __init__(self):
        self._file = None

    def _command_type(self):
        return 'attach.xunit_results'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_file': 'file'
        }

    def file(self, file):
        self._file = file
        return self


class CmdResultsGoTest(EvergreenCommand):
    def __init__(self, json=False, legacy=False):
        self._json_format = json
        self._legacy_format = legacy
        self._files = []

    def _command_type(self):
        if self._json_format:
            return 'gotest.parse_json'
        if self._legacy_format:
            return 'gotest.parse_files'

    def validate(self):
        if self._legacy_format == self._json_format:
            raise ValueError('Invalid format specified')

        return self

    def _param_list(self):
        return {
            '_files': 'files'
        }

    def file(self, file):
        self._files.append(file)
        return self

    def files(self, files):
        self._files += files
        return self


class CmdArchiveCreate(EvergreenCommand):
    def __init__(self, archive_format):
        self._archive_format = archive_format
        self._target = None
        self._source_dir = None
        self._include = []
        self._exclude = []

    def _command_type(self):
        return self._archive_format.create_cmd_name()

    def validate(self):
        return self._archive_format.validate('create')

    def _param_list(self):
        return {
            '_target': 'target',
            '_source_dir': 'source_dir',
            '_include': 'include',
            '_exclude': 'exclude_files',
        }

    def target(self, target):
        self._target = target
        return self

    def source_dir(self, source_dir):
        self._source_dir = source_dir
        return self

    def include(self, include):
        self._include.append(include)
        return self

    def includes(self, includes):
        self._include += includes
        return self

    def exclude(self, exclude):
        self._exclude.append(exclude)
        return self

    def excludes(self, excludes):
        self._exclude += excludes


class CmdArchiveExtract(EvergreenCommand):
    def __init__(self, archive_format):
        self._archive_format = archive_format
        self._path = None
        self._target = None
        self._exclude = []

    def _command_type(self):
        return self._archive_format.extract_cmd_name()

    def validate(self):
        return self._archive_format.validate('extract')

    def _param_list(self):
        return {
            '_path': 'path',
            '_target': 'destination',
            '_exclude': 'exclude_files',
        }

    def path(self, path):
        self._path = path
        return self

    def target(self, target):
        self._target = target
        return self

    def exclude(self, exclude):
        self._exclude.append(exclude)
        return self

    def excludes(self, excludes):
        self._exclude += excludes
        return self


class CmdAttachArtifacts(EvergreenCommand):
    def __init__(self):
        self._optional = False
        self._files = []

    def _command_type(self):
        return 'attach.artifacts'

    def validate(self):
        return self

    def _param_list(self):
        return {
            '_optional': 'optional',
            '_files': 'files',
        }

    def optional(self, optional):
        self._optional = optional
        return self

    def file(self, f):
        self._files.append(f)
        return self

    def files(self, fs):
        self._files += fs
        return self


class ArchiveFormat():
    def __init__(self, archive_format):
        self._format = archive_format

    def validate(self, operation):
        valid_formats = {
            'create': [ARCHIVE_FORMAT_ZIP, ARCHIVE_FORMAT_TAR],
            'extract': [ARCHIVE_FORMAT_ZIP, ARCHIVE_FORMAT_TAR,
                        ARCHIVE_FORMAT_AUTO],
        }

        if self._format not in valid_formats[operation]:
            raise ValueError('Invalid archive format: ' + self._format)

        return self

    def create_cmd_name(self):
        if self._format == ARCHIVE_FORMAT_ZIP:
            return 'archive.zip_pack'

        if self._format == ARCHIVE_FORMAT_TAR:
            return 'archive.targz_pack'

        return self.validate()

    def extract_cmd_name(self):
        if self._format == ARCHIVE_FORMAT_ZIP:
            return 'archive.zip_extract'

        if self._format == ARCHIVE_FORMAT_TAR:
            return 'archive.targz_extract'

        if self._format == 'auto':
            return 'archive.auto_extract'

        return self.validate()

    @staticmethod
    def zip():
        return ArchiveFormat(ARCHIVE_FORMAT_ZIP)

    @staticmethod
    def tar():
        return ArchiveFormat(ARCHIVE_FORMAT_TAR)

    @staticmethod
    def auto():
        return ArchiveFormat(ARCHIVE_FORMAT_AUTO)
