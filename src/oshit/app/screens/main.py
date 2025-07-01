"""The main screen for the application."""

##############################################################################
# Python imports.
from functools import partial

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ...hn import HN
from ...hn.item.article import Article
from ..commands import ShowComments, ShowUser
from ..data.config import load_configuration
from ..widgets import HackerNews, Items
from .comments import Comments
from .config import ConfigurationDialog
from .help import Help
from .search import Search
from .user import UserDetails


##############################################################################
class Main(Screen[None]):
    """The main screen of the application."""

    CONTEXT_HELP = """
    ## Application keys

    | Key | Description |
    | - | - |
    | <kbd>F1</kbd> | This help screen. |
    | <kbd>F2</kbd> | Toggle compact/relaxed display. |
    | <kbd>F3</kbd> | Toggle dark/light mode. |
    | <kbd>F4</kbd> | Toggle numbers against items. |
    | <kbd>F5</kbd> | Toggle showing age of data. |
    | <kbd>F12</kbd> | Quit the application. |
    | <kbd>/</kbd> | Search* and open tab with results. |
    | <kbd>t</kbd> | View the top stories. |
    | <kbd>n</kbd> | View the new stories. |
    | <kbd>b</kbd> | View the best stories. |
    | <kbd>a</kbd> | View the AskHN stories. |
    | <kbd>s</kbd> | View the ShowHN stories. |
    | <kbd>j</kbd> | View the jobs. |

    \\* Note that the search only looks at already-downloaded items.
    """

    TITLE = f"Orange Site Hit v{__version__}"

    BINDINGS = [
        Binding("f1", "help", "Help"),
        Binding("f2", "compact", "Compact/Relaxed"),
        Binding("f3", "app.toggle_dark"),
        Binding("f4", "numbered"),
        Binding("f5", "show_age"),
        Binding("f11", "config", "Configure"),
        Binding("f12", "app.quit", "Quit"),
        Binding("t", "go('top')"),
        Binding("n", "go('new')"),
        Binding("b", "go('best')"),
        Binding("a", "go('ask')"),
        Binding("s", "go('show')"),
        Binding("j", "go('jobs')"),
        Binding("r", "go('search')"),
        Binding("/", "local_search"),
    ]

    def __init__(self) -> None:
        """Initialise the screen."""
        super().__init__()
        config = load_configuration()
        self._hn = HN(
            max_concurrency=config.maximum_concurrency,
            timeout=config.connection_timeout,
        )
        """The HackerNews client object."""
        self._title_interval: Timer | None = None

    def compose(self) -> ComposeResult:
        """Compose the main screen's layout."""
        yield Header()
        with HackerNews():
            config = load_configuration()
            yield Items("top", "t", partial(self._hn.top_stories, config.maximum_top))
            yield Items("new", "n", partial(self._hn.new_stories, config.maximum_new))
            yield Items(
                "best", "b", partial(self._hn.best_stories, config.maximum_best)
            )
            yield Items(
                "ask", "a", partial(self._hn.latest_ask_stories, config.maximum_ask)
            )
            yield Items(
                "show", "s", partial(self._hn.latest_show_stories, config.maximum_show)
            )
            yield Items(
                "jobs", "j", partial(self._hn.latest_job_stories, config.maximum_jobs)
            )
        yield Footer()

    @on(HackerNews.TabActivated)
    @on(Items.Loading)
    @on(Items.Loaded)
    def _refresh_subtitle(self) -> None:
        """Refresh the subtitle of the screen."""
        try:
            self.sub_title = self.query_one(HackerNews).description
        except NoMatches:
            # There's a rare situation, it seems, where we can be on the way
            # out, the DOM is being pulled down, and we get a message being
            # processed too late that causes this method to fire. The result
            # is that the `Header` widget will be asked to update something
            # that doesn't exist any more. This guards against that.
            pass

    def _set_title_refresh(self, refresh: bool) -> None:
        """Set the state of the title refresh interval.

        Args:
            refresh: The state to set it to.
        """
        if refresh:
            if self._title_interval is None:
                self._title_interval = self.set_interval(0.95, self._refresh_subtitle)
        else:
            if self._title_interval is not None:
                self._title_interval.stop()
                self._title_interval = None
        self._refresh_subtitle()

    def on_mount(self) -> None:
        """Configure things once the DOM is ready."""
        self._set_title_refresh(load_configuration().show_data_age)

    def action_help(self) -> None:
        """Show the help screen."""
        self.app.push_screen(Help(self))

    def action_go(self, items: str) -> None:
        """Go to the given list of items.

        Args:
            items: The name of the list of items to go to.
        """
        before = self.query_one(HackerNews).active
        try:
            self.query_one(HackerNews).active = items
        except ValueError:
            self.query_one(HackerNews).active = before
            return
        self.query_one(HackerNews).focus_active_pane()

    def action_compact(self) -> None:
        """Toggle the compact display."""
        news = self.query_one(HackerNews)
        news.compact = not news.compact

    def action_numbered(self) -> None:
        """Toggle the numbers display."""
        news = self.query_one(HackerNews)
        news.numbered = not news.numbered

    def action_show_age(self) -> None:
        """Toggle the display of the age of the data in the lists."""
        news = self.query_one(HackerNews)
        news.show_age = not news.show_age
        self._set_title_refresh(news.show_age)

    async def _search(self, search_text: str) -> list[Article]:
        hits: dict[int, Article] = {}
        for item_list in self.query(Items).results():
            for item in item_list.items:
                if search_text in item:
                    hits[item.item_id] = item
        return list(hits.values())

    @work
    async def action_local_search(self) -> None:
        """Perform a local search."""
        if search_text := await self.app.push_screen_wait(Search()):
            await self.query_one(HackerNews).remove_pane("search")
            await self.query_one(HackerNews).add_pane(
                Items("search", "r", partial(self._search, search_text))
            )
            self.query_one(HackerNews).active = "search"

    def action_config(self) -> None:
        """Show the configuration dialog."""
        self.app.push_screen(ConfigurationDialog())

    @on(ShowUser)
    def show_user(self, event: ShowUser) -> None:
        """Handle a request to show the details of a user."""
        self.app.push_screen(UserDetails(self._hn, event.user))

    @on(ShowComments)
    def show_comments(self, event: ShowComments) -> None:
        """Handle a request to show the comments for an article."""
        self.app.push_screen(Comments(self._hn, event.article))


### main.py ends here
