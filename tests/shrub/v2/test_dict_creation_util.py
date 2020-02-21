"""Unit tests for shrub.v2.dict_creation_util."""

import shrub.v2.dict_creation_util as under_test


class TestAddIfExists:
    def test_value_does_not_exit(self):
        obj = {}

        under_test.add_if_exists(obj, "key", None)

        assert obj == {}

    def test_value_does_exist(self):
        obj = {}

        under_test.add_if_exists(obj, "key", "value")

        assert obj == {"key": "value"}


class TestAddExistingFromDict:
    def test_add_a_mix_of_items(self):
        obj = {}

        under_test.add_existing_from_dict(
            obj, {"item 1": "an item", "item 2": None, "item 3": [], "item 4": "another item"}
        )

        assert obj == {"item 1": "an item", "item 4": "another item"}
