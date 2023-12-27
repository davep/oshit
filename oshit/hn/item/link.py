"""The class that holds HackerNews items that are some sort of link."""

##############################################################################
# Python imports.
from typing import Any
from typing_extensions import Self

##############################################################################
# Local imports.
from .article import Article
from .loader import Loader

##############################################################################
class Link(Article):
    """Class for holding an article that links to something."""

    url: str = ""
    """The URL associated with the article."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.url = data.get("url", "")
        return super().populate_with(data)

##############################################################################
@Loader.loads("story")
class Story(Link):
    """Class for holding a story."""

##############################################################################
@Loader.loads("job")
class Job(Link):
    """Class for holding a job."""


### link.py ends here
