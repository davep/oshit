"""The HackerNews API client."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from datetime import datetime
from json import loads
from typing import Any
from typing_extensions import Final, Self

##############################################################################
# HTTPX imports.
import httpx

##############################################################################
@dataclass
class ItemBase:
    """Base class of an item found in the HackerNews API."""

    item_id: int = 0
    """The ID of the item."""

    by: str = ""
    """The author of the item."""

    item_type: str = ""
    """The API's name for the type of the item."""

    time: datetime = datetime(1970, 1, 1)
    """The time of the item."""

    kids: list[int] = field(default_factory=list)
    """The children of the item."""

    def populate_with(self, data: dict[str, Any]) -> Self:
        """Populate the item with the data from the given JSON value.

        Args:
            data: The data to populate from.

        Returns:
            Self
        """
        self.item_id = data["id"]
        self.by = data["by"]
        self.item_type = data["type"]
        self.time = datetime.fromtimestamp(data["time"])
        self.kids = data.get("kids", [])
        return self

##############################################################################
class UnknownItem(ItemBase):
    """A fallback while I work on this. This will go away."""

##############################################################################
class Article(ItemBase):
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
        self.descendants = data["descendants"]
        self.score = data["score"]
        self.title = data["title"]
        return super().populate_with(data)

##############################################################################
class Story(Article):
    """Class for holding a story."""

    url: str = ""
    """The URL associated with the story."""

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
class HN:
    """HackerNews API client."""

    AGENT: Final[str] = "Oshit (https://github.com/davep/oshit)"
    """The agent string to use when talking to the API."""

    _BASE: Final[str] = "https://hacker-news.firebaseio.com/v0/"
    """The base of the URL for the API."""

    def _api_url(self, *path: str) -> str:
        """Construct a URL for calling on the API.

        Args:
            *path: The path to the endpoint.

        Returns:
            The URL to use.
        """
        return f"{self._BASE}{'/'.join(path)}"

    async def _call(self, *path: str, **params: str) -> str:
        """Call on the Pinboard API.

        Args:
            path: The path for the API call.
            params: The parameters for the call.

        Returns:
            The text returned from the call.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._api_url(*path),
                    params=params,
                    headers={"user-agent": self.AGENT},
                )
            except httpx.RequestError as error:
                raise error     # TODO
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                raise error     # TODO
            return response.text

    async def max_item_id(self) -> int:
        """Get the current maximum item ID.

        Returns:
            The ID of the maximum item on HackerNews.
        """
        return loads(await self._call("maxitem.json"))

    async def _raw_item(self, item_id: int) -> dict[str, Any]:
        """Get the raw data of an item from the API.

        Args:
            item_id: The ID of the item to get.

        Returns:
            The JSON data of that item as a `dict`.
        """
        return loads(await self._call("item", f"{item_id}.json"))

    async def item(self, item_id) -> ItemBase:
        """Get an item by its ID.

        Args:
            item_id: The ID of the item to get.

        Returns:
            The item.
        """
        return {
            "story": Story,
        }.get((item := await self._raw_item(item_id))["type"], UnknownItem)().populate_with(item)

    async def top_story_ids(self) -> list[int]:
        """Get the IDs of the top stories.

        Returns:
            A list of the top story IDs.
        """
        return loads(await self._call("topstories.json"))

### client.py ends here
