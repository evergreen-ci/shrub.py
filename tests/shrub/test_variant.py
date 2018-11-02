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
        dt = DisplayTaskDefinition()

        obj = dt.to_map()

        assert {} == obj

    def test_items_added_to_display_task(self):
        dt = DisplayTaskDefinition()
        dt.name('display task name')\
            .component('comp0')\
            .components(['comp1', 'comp2'])

        obj = dt.to_map()
        assert 'display task name' == obj['name']
        assert 'comp0' in obj['execution_tasks']
        assert 'comp1' in obj['execution_tasks']
        assert 'comp2' in obj['execution_tasks']
