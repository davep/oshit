"""The HackerNews API client."""

##############################################################################
# Python imports.
from asyncio import gather
from json import loads
from typing import Any
from typing_extensions import Final

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, RequestError, HTTPStatusError

##############################################################################
# Local imports.
from .item import ItemType, Job, Link, Story, UnknownItem

##############################################################################
class HN:
    """HackerNews API client."""

    AGENT: Final[str] = "OSHit (https://github.com/davep/oshit)"
    """The agent string to use when talking to the API."""

    _BASE: Final[str] = "https://hacker-news.firebaseio.com/v0/"
    """The base of the URL for the API."""

    def __init__(self) -> None:
        """Initialise the API client object."""
        self._client_: AsyncClient | None = None

    @property
    def _client(self) -> AsyncClient:
        """The API client."""
        if self._client_ is None:
            self._client_ = AsyncClient()
        return self._client_

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
        try:
            response = await self._client.get(
                self._api_url(*path),
                params=params,
                headers={"user-agent": self.AGENT},
            )
        except RequestError as error:
            raise error     # TODO

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
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

    async def item(self, item_type: type[ItemType], item_id: int) -> ItemType:
        """Get an item by its ID.

        Args:
            item_type: The type of the item to get from the API.
            item_id: The ID of the item to get.

        Returns:
            The item.
        """
        if isinstance(item := {
                "story": Story,
                "job": Job
        }.get((data := await self._raw_item(item_id))["type"], UnknownItem)().populate_with(data), item_type):
            return item
        raise ValueError(f"The item of ID '{item_id}' is of type '{item.item_type}', not {item_type.__name__}")

    async def top_story_ids(self) -> list[int]:
        """Get the list of top story IDs.

        Returns:
            The list of the top story IDs.
        """
        return loads(await self._call("topstories.json"))

    async def _items_from_ids(self, item_type: type[ItemType], item_ids: list[int]) -> list[ItemType]:
        """Turn a list of item IDs into a list of items.

        Args:
            item_type: The type of the item we'll be getting.
            item_ids: The IDs of the items to get.

        Returns:
            The list of items.
        """
        return await gather(*[self.item(item_type, item_id) for item_id in item_ids])

    async def top_stories(self) -> list[Link]:
        """Get the IDs of the top stories.

        Returns:
            The list of the top stories.
        """
        return await self._items_from_ids(Link, await self.top_story_ids())

### client.py ends here
