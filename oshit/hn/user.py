"""Class that holds the details of a HackerNews user."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

##############################################################################
# Backward-compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from .text import tidy_text


##############################################################################
@dataclass
class User:
    """Details of a HackerNews user."""

    user_id: str = ""
    """The ID of the user."""

    raw_about: str = ""
    """The raw version of the user's about text."""

    karma: int = 0
    """The user's karma."""

    created: datetime = datetime(1970, 1, 1)
    """The time the user was created."""

    submitted: list[int] = field(default_factory=list)
    """The stories, polls and comments the user has submitted."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the user with details from the given data.

        Args:
            data: The data to populate from.

        Returns:
            Self.
        """
        self.user_id = data["id"]
        self.raw_about = data.get("about", "").strip()
        self.karma = data["karma"]
        self.created = datetime.fromtimestamp(data["created"])
        self.submitted = data.get("submitted", [])
        return self

    @property
    def has_about(self) -> bool:
        """Does the user have an about text?"""
        return bool(self.raw_about)

    @property
    def about(self) -> str:
        """A clean version of the about text for the user."""
        return tidy_text(self.raw_about)

    @property
    def url(self) -> str:
        """The HackerNews URL for the user."""
        return f"https://news.ycombinator.com/user?id={self.user_id}"


### user.py ends here
