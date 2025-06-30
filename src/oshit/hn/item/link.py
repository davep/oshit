"""The class that holds HackerNews items that are some sort of link."""

##############################################################################
# Python imports.
from typing import Any
from urllib.parse import urlparse

##############################################################################
# Backward-compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from .article import Article
from .loader import Loader


##############################################################################
class Link(Article):
    """Class for holding an article that potentially links to something."""

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

    @property
    def has_url(self) -> bool:
        """Does this article actually have a link.

        Some stories fall under the banner of being linkable, but don't
        really have a link. This can be used to test if there really is a
        link or not.
        """
        return bool(self.url.strip())

    @property
    def visitable_url(self) -> str:
        """A visitable URL for the item."""
        return self.url if self.has_url else super().visitable_url

    @property
    def domain(self) -> str:
        """The domain from the URL, if there is one."""
        return urlparse(self.url).hostname or ""

    def __contains__(self, search_for: str) -> bool:
        return (
            super().__contains__(search_for)
            or search_for.casefold() in self.domain.casefold()
        )


##############################################################################
@Loader.loads("story")
class Story(Link):
    """Class for holding a story."""


##############################################################################
@Loader.loads("job")
class Job(Link):
    """Class for holding a job."""


### link.py ends here
