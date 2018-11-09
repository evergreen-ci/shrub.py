import pytest

from shrub.variant import DisplayTaskDefinition
from shrub.variant import TaskSpec
from shrub.variant import Variant


class TestVariant:
    def test_empty_command_definition(self):
        v = Variant('variant name')

        assert 'variant name' == v.get_name()
        assert {'name': 'variant name'} == v.to_map()

    def test_flat_values_in_map(self):
        v = Variant('variant name')
        v.display_name('display name') \
            .run_on('distro') \
            .batch_time(100)

        obj = v.to_map()
        assert 'variant name' == obj['name']
        assert 'display name' == obj['display_name']
        assert ['distro'] == obj['run_on']
        assert 100 == obj['batchtime']

    def test_expansions_can_be_added(self):
        v = Variant('variant name')
        v.expansion('k0', 'v0')
        v.expansions({'k1': 'v1', 'k2': 'v2'})

        obj = v.to_map()
        assert 'v0' in obj['expansions']['k0']
        assert 'v1' in obj['expansions']['k1']
        assert 'v2' in obj['expansions']['k2']

    def test_tasks_can_be_added(self):
        v = Variant('variant name')
        v.task(TaskSpec('task 0')) \
            .tasks([TaskSpec('task 1'), TaskSpec('task 2')])

        obj = v.to_map()
        assert 'task 0' == obj['tasks'][0]['name']
        assert 'task 1' == obj['tasks'][1]['name']
        assert 'task 2' == obj['tasks'][2]['name']

    def test_invalid_tasks_cannot_be_added(self):
        v = Variant('variant name')
        with pytest.raises(TypeError):
            v.task("I'm not really a task")

        with pytest.raises(TypeError):
            v.tasks(TaskSpec('not array'))

    def test_display_tasks_can_be_added(self):
        v = Variant('variant name')
        v.display_task(DisplayTaskDefinition('display task 0'))\
            .display_tasks([DisplayTaskDefinition('display task 1'),
                            DisplayTaskDefinition('display task 2')])

        obj = v.to_map()
        assert 'display task 0' == obj['display_tasks'][0]['name']
        assert 'display task 1' == obj['display_tasks'][1]['name']
        assert 'display task 2' == obj['display_tasks'][2]['name']


class TestTaskSpec:
    def test_task_spec(self):
        ts = TaskSpec('task name')
        ts.stepback(True)
        ts.distro('linux')

        obj = ts.to_map()
        assert 'task name' == obj['name']
        assert obj['stepback']
        assert ['linux'] == obj['distros']


class TestDisplayTaskDefinition:
    def test_empty_display_task(self):
        dt = DisplayTaskDefinition('name')

        obj = dt.to_map()
        assert {'name': 'name'} == obj

    def test_items_added_to_display_task(self):
        dt = DisplayTaskDefinition('display task name')
        dt.component('comp0')\
            .components(['comp1', 'comp2'])

        obj = dt.to_map()
        assert 'display task name' == obj['name']
        assert 'comp0' in obj['execution_tasks']
        assert 'comp1' in obj['execution_tasks']
        assert 'comp2' in obj['execution_tasks']
