"""Central item type to item class type matching code."""

##############################################################################
# Python imports.
from typing import Any, Callable

##############################################################################
# Local imports.
from .base import Item
from .unknown import UnknownItem

##############################################################################
class Loader:
    """Helper class for loading up HackerNews items."""

    _map: dict[str, type[Item]] = {}
    """The map of type names to actual types."""

    @classmethod
    def loads(cls, item_type: str) -> Callable[[type[Item]], type[Item]]:
        """Decorator for declaring that a class loads a particular item type."""
        def _register(handler: type[Item]) -> type[Item]:
            cls._map[item_type] = handler
            return handler
        return _register

    @classmethod
    def load(cls, data: dict[str, Any]) -> Item:
        """Load the JSON data into the desired type.

        Args:
            data: The JSON data to load up.

        Returns:
            An instance of a item class, of the best-fit type.
        """
        return cls._map.get(data["type"], UnknownItem)().populate_with(data)

### loader.py ends here
