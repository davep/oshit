"""Provides a tab pane for showing items from HackerNews."""

##############################################################################
# Python imports.
from datetime import datetime
from typing import Awaitable, Callable, TypeVar, Generic
from urllib.parse import urlparse

##############################################################################
# Textual imports.
from textual import work
from textual.app import ComposeResult
from textual.reactive import var
from textual.widgets import OptionList, TabPane
from textual.widgets.option_list import Option

##############################################################################
# Rich imports.
from rich.console import Group

##############################################################################
# Humanize imports.
from humanize import naturaltime

##############################################################################
# Local imports.
from oshit.hn.item import Article, Link

##############################################################################
ArticleType = TypeVar("ArticleType", bound=Article)
"""Generic type for the items pane."""


##############################################################################
class HackerNewsArticle(Option):
    """An article from HackerNews."""

    def __init__(self, article: Article, compact: bool) -> None:
        """Initialise the hacker news article.

        Args:
            article: The article to show.
            compact: Should we use a compact or relaxed display?
        """
        self.article = article
        self._compact = compact
        """The article being shown."""
        super().__init__(self.prompt, id=str(article.item_id))

    @property
    def prompt(self) -> Group:
        """The prompt for the article."""
        domain = ""
        if isinstance(self.article, Link) and self.article.has_url:
            if domain := urlparse(self.article.url).hostname:
                domain = f" [dim italic]({domain})[/]"
        return Group(
            f"[dim italic]{self.article.__class__.__name__[0]}[/] {self.article.title}{domain}",
            f"  [dim italic]{self.article.score} points by {self.article.by} {naturaltime(self.article.time)}[/]",
            *([] if self._compact else [""]),
        )


##############################################################################
class Items(Generic[ArticleType], TabPane):
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

    compact: var[bool] = var(True)
    """Should we use a compact display?"""

    def __init__(
        self, title: str, key: str, source: Callable[[], Awaitable[list[ArticleType]]]
    ) -> None:
        """Initialise the pane.

        Args:
            title: The title for the pane.
            key: The key used to switch to this pane.
            source: The source of items for the pane.
        """
        super().__init__(f"{title.capitalize()} [dim]\\[{key}][/]", id=title)
        self._description = title
        """The description of the pane."""
        self._snarfed: datetime | None = None
        """The time when the data was snarfed."""
        self._source = source
        """The source of items to show."""
        self._items: list[ArticleType] = []
        """The items to show."""

    def compose(self) -> ComposeResult:
        """Compose the content of the pane."""
        yield OptionList()

    @property
    def description(self) -> str:
        """The description for this pane."""
        return (
            f"{self._description.capitalize()} - Updated {naturaltime(self._snarfed)}"
            if self._snarfed is not None
            else f"{self._description.capitalize()} - Loading..."
        )

    def _redisplay(self) -> None:
        """Redisplay the items."""
        display = self.query_one(OptionList)
        display.clear_options().add_options(
            [HackerNewsArticle(item, self.compact) for item in self._items]
        )
        if self._items:
            display.highlighted = 0

    @work
    async def _load(self) -> None:
        """Load up the items and display them."""
        display = self.query_one(OptionList)
        display.loading = True
        self._items = await self._source()
        self._snarfed = datetime.now()
        self._redisplay()
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

    def _watch_compact(self) -> None:
        """React to the compact setting being changed."""
        if self._items:
            self._redisplay()


### items.py ends here
