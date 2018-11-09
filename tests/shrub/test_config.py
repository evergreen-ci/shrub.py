import pytest

from shrub.config import Configuration
from shrub.command import CommandDefinition
from shrub.command import CommandSequence


class TestConfiguration:

    def test_invalid_config_throws_exception(self):
        c = Configuration()
        with pytest.raises(ValueError):
            c.command_type("bad command type")

    def test_config_with_non_recurse_values(self):
        c = Configuration()
        c.exec_timeout(20)\
            .batch_time(300)\
            .ignore_file("file1")\
            .ignore_files(["file2", "file3"])
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
        c.task("new task")

        obj = c.to_map()

        assert "new task" == obj["tasks"][0]["name"]

    def test_get_existing_task(self):
        c = Configuration()
        c.task('task 0')
        t1 = c.task('task 1')
        c.task('task 2')

        t1.priority(42)

        assert 42 == c.task('task 1').to_map()["priority"]
        assert 3 == len(c.to_map()["tasks"])

    def test_task_groups(self):
        c = Configuration()
        c.task_group('tg 0')
        c.task_group('tg 1')
        tg2 = c.task_group('tg 2')

        tg2.max_hosts(5)

        assert 5 == c.task_group('tg 2').to_map()['max_hosts']
        assert 3 == len(c.to_map()['task_groups'])

    def test_functions(self):
        c = Configuration()
        f = c.function('func 0')
        c.function('func 1')
        c.function('func 2')

        f.add(CommandDefinition().function('f'))

        assert 'f' == c.function('func 0').to_map()[0]['func']
        assert 3 == len(c.to_map()['functions'])

    def test_variants(self):
        c = Configuration()
        c.variant('variant 0')
        v1 = c.variant('variant 1')
        c.variant('variant 2')

        v1.batch_time(100)

        assert 100 == c.variant('variant 1').to_map()['batchtime']
        assert 3 == len(c.to_map()['buildvariants'])

    def test_pre(self):
        c = Configuration()
        cs = CommandSequence()
        cs.command().function('func 0')
        cs.command().function('func 1')
        c.pre(cs)

        assert 'func 0' == c.to_map()['pre'][0]['func']
        assert 2 == len(c.to_map()['pre'])

    def test_post(self):
        c = Configuration()
        cs = CommandSequence()
        cs.command().function('func 0')
        cs.command().function('func 1')
        c.post(cs)

        assert 'func 0' == c.to_map()['post'][0]['func']
        assert 2 == len(c.to_map()['post'])
