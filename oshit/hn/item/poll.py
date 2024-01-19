"""Class for holding a poll pulled from HackerNews."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from typing import Any

##############################################################################
# Backward-compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from .article import Article
from .base import Item
from .loader import Loader


##############################################################################
@dataclass
@Loader.loads("poll")
class Poll(Article):
    """Class that holds the details of a HackerNews poll."""

    parts: list[int] = field(default_factory=list)
    """The list of IDs for the parts of the poll."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.parts = data.get("parts", [])
        return super().populate_with(data)


##############################################################################
@dataclass
@Loader.loads("pollopt")
class PollOption(Item):
    """Class for holding the details of a poll option."""

    poll: int = 0
    """The ID of the poll that the option belongs to."""

    score: int = 0
    """The score of the poll option."""

    text: str = ""
    """The text for the poll option."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.poll = data.get("poll", 0)
        self.score = data.get("score", 0)
        self.text = data.get("text", "")
        return super().populate_with(data)


### poll.py ends here
