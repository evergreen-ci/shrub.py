"""Unit tests for evg_project.py."""

import pytest

import shrub.v3.evg_project as under_test
from shrub.v3.evg_command import BuiltInCommand
from shrub.v3.evg_task import EvgTask


class TestGetRepositoryName:
    @pytest.mark.parametrize(
        "repo_url,repo_name",
        [
            ("git@github.com:wiredtiger/wiredtiger.git", "wiredtiger"),
            ("https://github.com/mongodb/mongo.git", "mongo"),
            ("/path/to/repo.git", "repo"),
        ],
    )
    def test_repository_name_can_be_parsed(self, repo_url, repo_name):
        module = under_test.EvgModule(
            **{"name": "my module", "repo": repo_url, "branch": "main", "prefix": "src/thirdparty"}
        )

        assert module.get_repository_name() == repo_name


def test_evg_project_command_display_name():
    """Test that a project's tasks' commands' displaly names are included in model serialization"""
    proj = under_test.EvgProject(
        tasks=[
            EvgTask(
                name="my-task",
                commands=[
                    BuiltInCommand(
                        command="subprocess.exec",
                        type="setup",
                        params={},
                        display_name="bar",
                    )
                ],
            )
        ]
    )
    assert proj.model_dump(exclude_unset=True) == {
        "tasks": [
            {
                "name": "my-task",
                "commands": [
                    {
                        "command": "subprocess.exec",
                        "type": "setup",
                        "params": {},
                        "display_name": "bar",
                    }
                ],
            }
        ]
    }
