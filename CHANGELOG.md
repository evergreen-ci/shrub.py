# Changelog

## 3.10.0 - 2025-04-10
- Relax field requirements in ``perf_send``.

## 3.9.0 - 2025-04-02
- Add support for ``aws_session_token`` in s3 commands.

## 3.8.0 - 2025-04-01
- Add missing fields to `EvgTaskDependency`.

## 3.7.0 - 2025-03-18
- Add support for `ec2.assume_role` to the list of `AvailableCommands`.

## 3.6.0 - 2024-11-18
- Address Python 3.12+ compatibility issues.
- Address pydantic v2 compatibility issues.
- Raise minimum required Python version to 3.8.
- Raise minimum required `pydantic` version to 2.0.

## 3.5.0 - 2024-11-12
- Add `batchtime` and `depends_on` fields to `shrub.v3.evg_task.EvgTaskRef`.

## 3.4.0 - 2024-10-30
- Added additional `*_can_fail_task` and `*_timeout_secs` fields to `shrub.v3.evg_task_group.EvgTaskGroup`.
- Restrict the type of `*_timeout_secs` fields to `Optional[int]` instead of `Optional[Union[int, str]]`.

## 3.3.2 - 2024-10-30
- Revert support for `batchtime` field in `shrub.v3.evg_task.EvgTask`

## 3.3.1 - 2024-10-16
- Added default value `None` to optional fields for pydantic 2.0 compatibility.

## 3.3.0 - 2024-10-10
- Added `run_on`, `batchtime`, and `patchable` fields to `shrub.v3.evg_task.EvgTask`

## 3.2.0 - 2024-10-09
- Added custom yaml output for `shrub.v3.shrub_service.ShrubService.generate_yaml`

## 3.1.5 - 2024-10-07
- Updated README example to use v3 API

## 3.1.4 - 2024-09-30
- Added command for generating github tokens

## 3.1.3 - 2024-08-07
- Upgrade pydantic to 2.0

## 3.1.2 - 2024-03-27
- Switch to GitHub merge queue (no code changes)

## 3.1.1 - 2024-02-09
- Refactor deploy task

## 3.1.0 - 2023-09-14
- Remove git-url-parse dependency

## 3.0.7 - 2023-07-14
- Added cron field to v2 and v3 API

## 3.0.6 - 2023-06-27
- Added cron field to v1 API

## 3.0.5 - 2023-04-26
- Added activate field to v1 API

## 3.0.4 - 2022-6-17
- Added check for version update

## 3.0.3 - 2022-6-16
- Added command for setting downstream expansions  

## 3.0.2 - 2022-6-9
- Add support for tags on the build variant level

## 3.0.1 - 2022-2-9
- Add support for Python 3.7 by using typing extensions.

## 3.0.0 - 2021-10-25
- Add support for pydantic model based workflow.

## 1.1.4 - 2021-06-17
- Add 'activate' support to for tasks in display tasks.

## 1.1.3 - 2021-06-08
- Add 'activate' support to build variants and tasks.

## 1.1.2 - 2021-02-04
- Add py.typed for PEP 561 compliance.

## 1.1.1 - 2020-09-16
- Fix a bug where 'exec_timeout_secs' set the wrong key.

## 1.1.0 - 2020-05-08
* Add python 3.6 support.

## 1.0.3 - 2020-04-16
- Fix missing display names from build variants.

## 1.0.2 - 2020-04-01
- Add support for specifying distros on display tasks.
- Add build variant options for 'run_on' and 'modules'.

## 1.0.1 - 2020-03-30
- Add support for adding existing tasks to v2 API.

## 1.0.0 - 2020-03-26
- Implement v2 api to be more pythonic and provide type hints.

## 0.2.2 - 2019-03-25
- Fix S3 copy build_variant option.

## 0.2.1 - 2019-03-22
- Add optional support for CmdS3Copy operation.
