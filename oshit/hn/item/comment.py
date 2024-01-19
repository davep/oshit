"""Provides the class that holds details of a HackerNews comment."""

##############################################################################
# Python imports.
from typing import Any

from typing_extensions import Self

##############################################################################
# Local imports.
from ..text import text_urls, tidy_text
from .base import ParentItem
from .loader import Loader


##############################################################################
@Loader.loads("comment")
class Comment(ParentItem):
    """Class that holds the details of a HackerNews comment."""

    raw_text: str = ""
    """The raw text of the comment."""

    parent: int = 0
    """The ID of the parent of the comment."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.raw_text = data.get("text", "")
        self.parent = data["parent"]
        return super().populate_with(data)

    @property
    def text(self) -> str:
        """The text for the comment."""
        return tidy_text(self.raw_text)

    @property
    def urls(self) -> list[str]:
        """The URLs in the comment."""
        return text_urls(self.raw_text)

    @property
    def flagged(self) -> bool:
        """Does the comment appear to be flagged?"""
        return self.raw_text == "[flagged]"

    @property
    def dead(self) -> bool:
        """Does the comment appear to be dead?"""
        return self.raw_text == "[dead]"


### comment.py ends here
