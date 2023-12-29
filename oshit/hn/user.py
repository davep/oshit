"""Class that holds the details of a HackerNews user."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from typing_extensions import Self


##############################################################################
@dataclass
class User:
    """Details of a HackerNews user."""

    user_id: str = ""
    """The ID of the user."""

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
        self.karma = data["karma"]
        self.created = datetime.fromtimestamp(data["created"])
        self.submitted = data.get("submitted", [])
        return self


### user.py ends here
