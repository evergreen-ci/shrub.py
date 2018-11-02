import abc
import collections

import yaml


RECURSE_KEY = "recurse"
NAME_KEY = "name"


class EvergreenBuilder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _yaml_map(self):
        """A map of values to yaml decorators."""

    def to_map(self):
        """Convert this object to a pythonic map."""
        obj = {}
        self._add_defined_attribs(obj, self._yaml_map().keys())
        return obj

    def _add_if_defined(self, obj, prop):
        """Add the specified property to the given object if it exists."""
        value = getattr(self, prop)
        if value:
            if self._yaml_map()[prop][RECURSE_KEY]:
                if isinstance(value, collections.Sequence):
                    value = [v.to_map() for v in value]
                else:
                    value = value.to_map()
            obj[self._yaml_map()[prop][NAME_KEY]] = value

    def _add_defined_attribs(self, obj, attrib_list):
        """Add any defined attributes in the given list to the given map."""
        for attrib in attrib_list:
            self._add_if_defined(obj, attrib)

    def to_yaml(self):
        return yaml.dump(self.to_map(), default_flow_style=False)
