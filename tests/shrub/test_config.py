import pytest
from shrub.config import Configuration


class TestConfiguration:

    def test_invalid_config_throws_exception(self):
        c = Configuration()
        with pytest.raises(ValueError):
            c.command_type("bad command type")

    def test_config_with_non_recurse_values(self):
        c = Configuration()
        c.exec_timeout(20).batch_time(300).ignore_file("file1").ignore_files(["file2", "file3"])
        c.stepback(True).command_type("setup")

        obj = c.to_map()

        assert obj["timeout"] == 20
        assert obj["batchtime"] == 300
        assert "file1" in obj["ignore"]
        assert "file2" in obj["ignore"]
        assert "file3" in obj["ignore"]
        assert obj["stepback"]
        assert obj["command_type"] == "setup"
        assert "tasks" not in obj

    def test_configuration_tasks(self):
        c = Configuration()
        t = c.task("new task")

        obj = c.to_map()

        assert "new task" == obj["tasks"][0]["name"]
