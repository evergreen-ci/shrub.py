import pytest
from shrub.Config import Configuration


class TestConfiguration:

    def test_invalid_config_throws_exception(self):
        c = Configuration()
        with pytest.raises(ValueError):
            c.set_command_type("bad command type")
