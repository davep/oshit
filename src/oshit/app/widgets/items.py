"""Provides a tab pane for showing items from HackerNews."""

##############################################################################
# Python imports.
from datetime import datetime
from typing import Awaitable, Callable, Generic, TypeVar, cast
from webbrowser import open as open_url

##############################################################################
# Humanize imports.
from humanize import intcomma, naturaltime

##############################################################################
# Rich imports.
from rich.console import Group
from rich.table import Table

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.reactive import var
from textual.widgets import OptionList, TabPane
from textual.widgets.option_list import Option

##############################################################################
# Local imports.
from ...hn import HN
from ...hn.item import Article, Job, Link
from ..commands import ShowComments, ShowUser

##############################################################################
ArticleType = TypeVar("ArticleType", bound=Article)
"""Generic type for the items pane."""


##############################################################################
class HackerNewsArticle(Option):
    """An article from HackerNews."""

    def __init__(
        self, article: Article, compact: bool, number: int | None = None
    ) -> None:
        """Initialise the hacker news article.

        Args:
            article: The article to show.
            compact: Should we use a compact or relaxed display?
        """
        self.article = article
        """The article being shown."""
        self._compact = compact
        """Should we show a compact form?"""
        self._number = number
        """The number to show for this article, if at all."""
        super().__init__(self.prompt, id=str(article.item_id))

    @property
    def prompt(self) -> Group:
        """The prompt for the article."""
        prefix = (
            f"[dim italic{' green' if isinstance(self.article, Job) else ''}]"
            f"{self.article.__class__.__name__[0]}"
            "[/]"
        )
        domain = ""
        if isinstance(self.article, Link):
            if domain := self.article.domain:
                domain = f" [dim italic]({domain})[/]"
        info = Table.grid(expand=True)
        info.add_column(no_wrap=True, ratio=1)
        info.add_column(no_wrap=True, justify="right", width=6)
        info.add_row(
            f"{' ' if self._compact else prefix} [dim italic]{intcomma(self.article.score)} "
            f"point{'' if self.article.score == 1 else 's'} "
            f"by {self.article.by} {naturaltime(self.article.time)}, "
            f"{intcomma(self.article.descendants)} comment{'' if self.article.descendants == 1 else 's'}[/]",
            "" if self._number is None else f" [dim italic]#{self._number}[/]",
        )
        return Group(
            f"{prefix if self._compact else ' '} {self.article.title}{domain}",
            info,
            *([] if self._compact else [""]),
        )


##############################################################################
class ArticleList(OptionList):
    """Widget to show a list of articles."""

    DEFAULT_CSS = """
    ArticleList {
        background: transparent;
    }
    """

    CONTEXT_HELP = """
    ## Highlighted item keys

    | Key | Description |
    | - | - |
    | <kbd>Enter</kbd> | Open the URL for the item in your browser. |
    | <kbd>c</kbd> | View the comments for the item. |
    """

    BINDINGS = [
        Binding("c", "comments", "Comments"),
        Binding("v", "view_online", "View on HN"),
        Binding("u", "user", "View User"),
    ]

    def on_focus(self) -> None:
        """Ensure the first item is highlighted if nothing is until now."""
        if self.highlighted is None and self.option_count:
            self.highlighted = 0

    def action_comments(self) -> None:
        """Visit the comments for the given"""
        if self.highlighted is not None:
            self.post_message(
                ShowComments(
                    cast(
                        HackerNewsArticle, self.get_option_at_index(self.highlighted)
                    ).article
                )
            )

    def action_view_online(self) -> None:
        """View an article online."""
        if self.highlighted is not None:
            open_url(
                cast(
                    HackerNewsArticle, self.get_option_at_index(self.highlighted)
                ).article.orange_site_url
            )

    def action_user(self) -> None:
        """Show the details of the user."""
        if self.highlighted is not None:
            self.post_message(
                ShowUser(
                    cast(
                        HackerNewsArticle, self.get_option_at_index(self.highlighted)
                    ).article.by
                )
            )


##############################################################################
class Items(Generic[ArticleType], TabPane):
    """The pane that displays the top stories."""

    CONTEXT_HELP = """
    ## View keys

    | Key | Description |
    | - | - |
    | <kbd>Ctrl</kbd>+<knd>r</kbd> | Reload. |
    """

    DEFAULT_CSS = """
    Items OptionList {
        height: 1fr;
        border: none;
        padding: 0;

        & > .option-list--option {
            padding: 0 1 0 0;
        }

        &:focus {
            border: none;
        }
    }
    """

    BINDINGS = [
        ("ctrl+r", "reload"),
    ]

    compact: var[bool] = var(True)
    """Should we use a compact display?"""

    numbered: var[bool] = var(False)
    """Should we show numbers against the items?"""

    show_age: var[bool] = var(True)
    """Should we show the age of the data?"""

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
        yield ArticleList()

    @property
    def description(self) -> str:
        """The description for this pane."""
        suffix = ""
        if self._snarfed is None:
            suffix = " - Loading..."
        elif not self._items:
            suffix = " - Reloading..."
        elif self.show_age:
            suffix = f" - Updated {naturaltime(self._snarfed)}"
        return f"{self._description.capitalize()}{suffix}"

    def _redisplay(self) -> None:
        """Redisplay the items."""
        display = self.query_one(OptionList)
        remember = display.highlighted
        display.clear_options().add_options(
            [
                HackerNewsArticle(item, self.compact, number if self.numbered else None)
                for number, item in enumerate(self._items)
                if item.looks_valid
            ]
        )
        display.highlighted = remember

    class Loading(Message):
        """Message sent when items start loading."""

    class Loaded(Message):
        """Message sent when items are loaded."""

    @work
    async def _load(self) -> None:
        """Load up the items and display them."""
        display = self.query_one(OptionList)
        display.loading = True
        self.post_message(self.Loading())
        try:
            self._items = await self._source()
        except HN.RequestError as error:
            self.app.bell()
            self.notify(
                str(error),
                title=f"Error loading items for '{self._description.capitalize()}'",
                timeout=8,
                severity="error",
            )
        else:
            self._snarfed = datetime.now()
            self._redisplay()
        display.loading = False
        self.post_message(self.Loaded())

    def maybe_load(self) -> bool:
        """Start loading the items if they're not loaded and aren't currently loading.

        Returns:
            `True` if it was decided to load the items, `False` if not.
        """
        if not self.loaded and not self.query_one(OptionList).loading:
            self._load()
            return True
        return False

    @property
    def items(self) -> list[ArticleType]:
        """The items."""
        return self._items

    @property
    def loaded(self) -> bool:
        """Has this tab loaded its items?"""
        return bool(self._items)

    def on_show(self) -> None:
        """Handle being shown."""
        if not self.loaded:
            self._load()

    def steal_focus(self) -> None:
        """Steal focus for the item list within."""
        self.query_one(ArticleList).focus()

    def _watch_compact(self) -> None:
        """React to the compact setting being changed."""
        if self.loaded:
            self._redisplay()

    def _watch_numbered(self) -> None:
        """React to the numbered setting being changed."""
        if self.loaded:
            self._redisplay()

    @on(OptionList.OptionSelected)
    def visit(self, event: OptionList.OptionSelected) -> None:
        """Handle an option list item being selected."""
        assert isinstance(option := event.option, HackerNewsArticle)
        open_url(option.article.visitable_url)

    def action_reload(self) -> None:
        """Reload the items"""
        self._items = []
        self._load()


### items.py ends here
