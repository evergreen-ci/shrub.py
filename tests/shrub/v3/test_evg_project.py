"""Unit tests for evg_project.py."""
import pytest

import shrub.v3.evg_project as under_test


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
