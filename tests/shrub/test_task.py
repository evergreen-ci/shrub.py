import pytest

from shrub.operations import CmdResultsGoTest
from shrub.operations import CmdGetProject
from shrub.task import Task
from shrub.task import TaskDependency
from shrub.task import TaskGroup


class TestTask:

    def test_task_with_flat_values(self):
        t = Task('task 0')
        t.priority(42)

        obj = t.to_map()
        assert 'task 0' == t.get_name()
        assert 'task 0' == obj['name']
        assert 42 == obj['priority']

    def test_adding_dependencies(self):
        t = Task('task 0')
        t.dependency(TaskDependency('dep 0', 'var 0'))\
            .dependency(TaskDependency('dep 1', 'var 1'))\
            .dependency(TaskDependency('dep 2', 'var 2'))

        obj = t.to_map()
        assert 3 == len(obj['depends_on'])
        assert 'dep 1' == obj['depends_on'][1]['name']

    def test_adding_command(self):
        t = Task('task 0')
        t.command(CmdGetProject())

        obj = t.to_map()
        assert 'git.get_project' == obj['commands'][0]['command']

    def test_adding_commands(self):
        t = Task('task 0')
        t.commands([CmdGetProject(), CmdGetProject()])

        obj = t.to_map()
        assert 2 == len(obj['commands'])
        assert 'git.get_project' == obj['commands'][0]['command']

    def test_adding_unvalidating_command(self):
        t = Task('task 0')

        with pytest.raises(ValueError):
            t.command(CmdResultsGoTest())

    def test_adding_unvalidating_commands(self):
        t = Task('task 0')

        with pytest.raises(ValueError):
            t.commands([CmdResultsGoTest()])

    def test_functions(self):
        t = Task('task 0')
        t.function('fn 0')
        t.functions(['fn 1', 'fn 2'])

        obj = t.to_map()
        assert 3 == len(obj['commands'])
        assert 'fn 0' == obj['commands'][0]['func']
        assert 'fn 1' == obj['commands'][1]['func']
        assert 'fn 2' == obj['commands'][2]['func']

    def test_function_with_vars(self):
        t = Task('task 0')
        t.function_with_vars('fn 0', {'x': 'y'})

        obj = t.to_map()
        assert 'fn 0' == obj['commands'][0]['func']
        assert 'y' == obj['commands'][0]['vars']['x']


class TestTaskDependency:
    def test_flat_values(self):
        td = TaskDependency('dep0', 'var0')

        obj = td.to_map()
        assert 'dep0' == obj['name']
        assert 'var0' == obj['variant']


class TestTaskGroup:
    def test_flat_value(self):
        tg = TaskGroup('task group 0')
        tg.max_hosts(5)\
            .timeout(42)

        obj = tg.to_map()
        assert 'task group 0' == tg.get_name()
        assert 'task group 0' == obj['name']
        assert 5 == obj['max_hosts']
        assert 42 == obj['timeout']

    def test_changing_name(self):
        tg = TaskGroup('task group 0')
        tg.name('new name')

        assert 'new name' == tg.get_name()
        assert 'new name' == tg.to_map()['name']

    def test_adding_tasks(self):
        tg = TaskGroup('task group 0')
        tg.task('task 0').tasks(['task 1', 'task 2'])

        obj = tg.to_map()
        assert 'task 0' in obj['tasks']
        assert 'task 1' in obj['tasks']
        assert 'task 2' in obj['tasks']
