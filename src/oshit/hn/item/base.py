"""Base class for items pulled from HackerNews."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, TypeVar

##############################################################################
# Backward-compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..text import tidy_text


##############################################################################
@dataclass
class Item:
    """Base class of an item found in the HackerNews API."""

    item_id: int = 0
    """The ID of the item."""

    by: str = ""
    """The author of the item."""

    item_type: str = ""
    """The API's name for the type of the item."""

    time: datetime = datetime(1970, 1, 1)
    """The time of the item."""

    raw_text: str = ""
    """The raw text of the of the item, if it has text."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.item_id = data["id"]
        self.by = data.get("by", "")
        self.item_type = data["type"]
        self.time = datetime.fromtimestamp(data["time"])
        self.raw_text = data.get("text", "")
        return self

    @property
    def orange_site_url(self) -> str:
        """The URL of the item on HackerNews."""
        return f"https://news.ycombinator.com/item?id={self.item_id}"

    @property
    def visitable_url(self) -> str:
        """A visitable URL for the item."""
        return self.orange_site_url

    @property
    def text(self) -> str:
        """The text for the item, if it has text."""
        return tidy_text(self.raw_text)

    @property
    def has_text(self) -> bool:
        """Does the item have any text?"""
        return bool(self.text.strip())

    @property
    def looks_valid(self) -> bool:
        """Does the item look valid?"""
        return bool(self.item_id) and bool(self.item_type)

    def __contains__(self, search_for: str) -> bool:
        return (
            search_for.casefold() in self.by.casefold()
            or search_for.casefold() in self.text
        )


##############################################################################
@dataclass
class ParentItem(Item):
    """Base class for items that can have children."""

    kids: list[int] = field(default_factory=list)
    """The children of the item."""

    deleted: bool = False
    """Has this item been deleted?"""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.kids = data.get("kids", [])
        self.deleted = data.get("deleted", False)
        return super().populate_with(data)


##############################################################################
ItemType = TypeVar("ItemType", bound="Item")
"""Generic type for an item pulled from the API."""

### base.py ends here
