"""Class for holding an article pulled from HackerNews.

An article is defined as something that has a title, a score and
descendants.
"""

##############################################################################
# Python imports.
from typing import Any

##############################################################################
# Typing extensions imports.
from typing_extensions import Self

##############################################################################
# Local imports.
from .base import ParentItem


##############################################################################
class Article(ParentItem):
    """Base class for all types of articles on HackerNews."""

    descendants: int = 0
    """The number of descendants of the article."""

    score: int = 0
    """The score of the article."""

    title: str = ""
    """The title of the article."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.descendants = data.get("descendants", 0)
        self.score = data.get("score", 0)
        self.title = data.get("title", "")
        return super().populate_with(data)

    def __contains__(self, search_for: str) -> bool:
        return (
            super().__contains__(search_for)
            or search_for.casefold() in self.title.casefold()
        )


### article.py ends here
