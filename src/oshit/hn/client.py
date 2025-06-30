"""The HackerNews API client."""

##############################################################################
# Python imports.
from asyncio import Semaphore, gather
from json import loads
from ssl import SSLCertVerificationError
from typing import Any, Final, cast

##############################################################################
# HTTPX imports.
from httpx import AsyncClient, HTTPStatusError, RequestError

##############################################################################
# Local imports.
from .item import (
    Article,
    Comment,
    ItemType,
    Job,
    Loader,
    ParentItem,
    Poll,
    PollOption,
    Story,
)
from .user import User


##############################################################################
class HN:
    """HackerNews API client."""

    AGENT: Final[str] = "Orange Site Hit (https://github.com/davep/oshit)"
    """The agent string to use when talking to the API."""

    _BASE: Final[str] = "https://hacker-news.firebaseio.com/v0/"
    """The base of the URL for the API."""

    class Error(Exception):
        """Base class for HackerNews errors."""

    class RequestError(Error):
        """Exception raised if there was a problem making an API request."""

    class NoSuchUser(Error):
        """Exception raised if no such user exists."""

    def __init__(self, max_concurrency: int = 50, timeout: int | None = 5) -> None:
        """Initialise the API client object.

        Args:
            max_concurrency: The maximum number of concurrent connections to use.
            timeout: The timeout for an attempted connection.
        """
        self._client_: AsyncClient | None = None
        """The HTTPX client."""
        self._max_concurrency = max_concurrency
        """The maximum number of concurrent connections to use."""
        self._timeout = timeout
        """The timeout to use on connections."""

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
                timeout=self._timeout,
            )
        except (RequestError, SSLCertVerificationError) as error:
            raise self.RequestError(str(error))

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            raise self.RequestError(str(error))

        return response.text

    async def max_item_id(self) -> int:
        """Get the current maximum item ID.

        Returns:
            The ID of the maximum item on HackerNews.
        """
        return int(loads(await self._call("maxitem.json")))

    async def _raw_item(self, item_id: int) -> dict[str, Any]:
        """Get the raw data of an item from the API.

        Args:
            item_id: The ID of the item to get.

        Returns:
            The JSON data of that item as a `dict`.
        """
        # TODO: Possibly cache this.
        return cast(dict[str, Any], loads(await self._call("item", f"{item_id}.json")))

    async def item(self, item_type: type[ItemType], item_id: int) -> ItemType:
        """Get an item by its ID.

        Args:
            item_type: The type of the item to get from the API.
            item_id: The ID of the item to get.

        Returns:
            The item.
        """
        # If we can get the item but it comes back with no data at all...
        if not (data := await self._raw_item(item_id)):
            # ...as https://hacker-news.firebaseio.com/v0/item/41050801.json
            # does for some reason, just make an empty version of the item.
            return item_type()
        if isinstance(item := Loader.load(data), item_type):
            return item
        raise ValueError(
            f"The item of ID '{item_id}' is of type '{item.item_type}', not {item_type.__name__}"
        )

    async def _items_from_ids(
        self, item_type: type[ItemType], item_ids: list[int]
    ) -> list[ItemType]:
        """Turn a list of item IDs into a list of items.

        Args:
            item_type: The type of the item we'll be getting.
            item_ids: The IDs of the items to get.

        Returns:
            The list of items.
        """
        concurrency_limit = Semaphore(self._max_concurrency)

        async def item(item_id: int) -> ItemType:
            """Get an item, with a limit on concurrent requests.

            Args:
                item_id: The ID of the item to get.

            Returns:
                The item.
            """
            async with concurrency_limit:
                return await self.item(item_type, item_id)

        return await gather(*[item(item_id) for item_id in item_ids])

    async def _id_list(self, list_type: str, max_count: int | None = None) -> list[int]:
        """Get a given ID list.

        Args:
            list_type: The type of list to get.
            max_count: Maximum number of IDs to fetch.

        Returns:
            The list of item IDs.
        """
        return cast(
            list[int], loads(await self._call(f"{list_type}.json"))[0:max_count]
        )

    async def top_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of top story IDs.

        Args:
            max_count: Maximum number of IDs to fetch.

        Returns:
            The list of the top story IDs.
        """
        return await self._id_list("topstories", max_count)

    async def top_stories(self, max_count: int | None = None) -> list[Article]:
        """Get the top stories.

        Args:
            max_count: Maximum number of stories to fetch.

        Returns:
            The list of the top stories.
        """
        return await self._items_from_ids(Article, await self.top_story_ids(max_count))

    async def new_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of new story IDs.

        Args:
            max_count: Maximum number of story IDs to fetch.

        Returns:
            The list of the new story IDs.
        """
        return await self._id_list("newstories", max_count)

    async def new_stories(self, max_count: int | None = None) -> list[Article]:
        """Get the new stories.

        Args:
            max_count: Maximum number of stories to fetch.

        Returns:
            The list of the new stories.
        """
        return await self._items_from_ids(Article, await self.new_story_ids(max_count))

    async def best_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of best story IDs.

        Args:
            max_count: Maximum number of story IDs to fetch.

        Returns:
            The list of the best story IDs.
        """
        return await self._id_list("beststories", max_count)

    async def best_stories(self, max_count: int | None = None) -> list[Article]:
        """Get the best stories.

        Args:
            max_count: Maximum number of stories to fetch.

        Returns:
            The list of the best stories.
        """
        return await self._items_from_ids(Article, await self.best_story_ids(max_count))

    async def latest_ask_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of the latest ask story IDs.

        Args:
            max_count: Maximum number of story IDs to fetch.

        Returns:
            The list of the latest ask story IDs.
        """
        return await self._id_list("askstories", max_count)

    async def latest_ask_stories(self, max_count: int | None = None) -> list[Story]:
        """Get the latest AskHN stories.

        Args:
            max_count: Maximum number of stories to fetch.

        Returns:
            The list of the latest AskHN stories.
        """
        return await self._items_from_ids(
            Story, await self.latest_ask_story_ids(max_count)
        )

    async def latest_show_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of the latest show story IDs.

        Args:
            max_count: Maximum number of story IDs to fetch.

        Returns:
            The list of the latest show story IDs.
        """
        return await self._id_list("showstories", max_count)

    async def latest_show_stories(self, max_count: int | None = None) -> list[Story]:
        """Get the latest ShowHN stories.

        Args:
            max_count: Maximum number of stories to fetch.

        Returns:
            The list of the latest ShowHN stories.
        """
        return await self._items_from_ids(
            Story, await self.latest_show_story_ids(max_count)
        )

    async def latest_job_story_ids(self, max_count: int | None = None) -> list[int]:
        """Get the list of the latest job story IDs.

        Args:
            max_count: Maximum number of job IDs to fetch.

        Returns:
            The list of the latest job story IDs.
        """
        return await self._id_list("jobstories", max_count)

    async def latest_job_stories(self, max_count: int | None = None) -> list[Job]:
        """Get the latest job stories.

        Args:
            max_count: Maximum number of jobs to fetch.

        Returns:
            The list of the latest job stories.
        """
        return await self._items_from_ids(
            Job, await self.latest_job_story_ids(max_count)
        )

    async def user(self, user_id: str) -> User:
        """Get the details of the given user.

        Args:
            user_id: The ID of the user.

        Returns:
            The details of the user.

        Raises:
            HN.NoSuchUser: If the user is not known.
        """
        if user := loads(await self._call("user", f"{user_id}.json")):
            return User().populate_with(user)
        raise self.NoSuchUser(f"Unknown user: {user_id}")

    async def comments(self, item: ParentItem) -> list[Comment]:
        """Get the comments for the given item.

        Args:
            item: The item to get the comments for.

        Returns:
            The list of comments for the item.
        """
        return await self._items_from_ids(Comment, item.kids)

    async def poll_options(self, poll: Poll) -> list[PollOption]:
        """Get the options for the given poll.

        Args:
            item: The poll to get the options for.

        Returns:
            The list of options for the poll.
        """
        return await self._items_from_ids(PollOption, poll.parts)


### client.py ends here
