"""Provides a tab pane for showing items from HackerNews."""

##############################################################################
# Python imports.
from datetime import datetime
from typing import Awaitable, Callable

##############################################################################
# Textual imports.
from textual import work
from textual.app import ComposeResult
from textual.widgets import OptionList, TabPane

##############################################################################
# Humanize imports.
from humanize import naturaltime

##############################################################################
# Local imports.
from oshit.hn.item import Job, Link, Story

##############################################################################
class Items(TabPane):
    """The pane that displays the top stories."""

    DEFAULT_CSS = """
    Items OptionList {
        height: 1fr;
        border: none;
        padding: 0;
        background: $panel;
    }

    Items OptionList:focus {
        border: none;
        background: $panel;
    }
    """

    # TODO: The typing is kinda funky. Make it less funky.
    def __init__(self, title: str, key: str, source: Callable[[], Awaitable[list[Link]] | Awaitable[list[Story]] | Awaitable[list[Job]]], id: str):
        """Initialise the pane.

        Args:
            title: The title for the pane.
            source: The source of items for the pane.
        """
        super().__init__(f"{title} [dim]\\[{key}][/]", id=id)
        self._description = title
        """The description of the pane."""
        self._snarfed: datetime | None = None
        """The time when the data was snarfed."""
        self._source = source
        """The source of items to show."""
        self._items: list[Link] | list[Story] | list[Job] = []
        """The items to show."""

    def compose(self) -> ComposeResult:
        """Compose the content of the pane."""
        yield OptionList()

    @property
    def description(self) -> str:
        """The description for this pane."""
        return (
            f"{self._description} - Updated {naturaltime(self._snarfed)}"
            if self._snarfed is not None
            else
            f"{self._description} - Loading..."
        )

    @work
    async def _load(self) -> None:
        """Load up the items and display them."""
        display = self.query_one(OptionList)
        display.loading = True
        self._items = await self._source()
        self._snarfed = datetime.now()
        display.clear_options().add_options(
            [item.title for item in self._items]
        )
        if self._items:
            display.highlighted = 0
        display.loading = False
        self._refresh_description()

    def _refresh_description(self) -> None:
        """Force a refresh of the description."""
        self.screen.sub_title = self.description

    def on_show(self) -> None:
        """Handle being shown."""
        if not self._items:
            self._load()
        self._refresh_description()

    def steal_focus(self) -> None:
        """Steal focus for the item list within."""
        self.query_one(OptionList).focus()

### items.py ends here
