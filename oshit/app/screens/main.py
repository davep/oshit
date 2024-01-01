"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ...hn import HN
from ..data.config import load_configuration
from ..commands import ShowComments, ShowUser
from ..widgets import HackerNews, Items
from .comments import Comments
from .help import Help
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
    | <kbd>F12</kbd> | Quit the application. |
    | <kbd>t</kbd> | View the top stories. |
    | <kbd>n</kbd> | View the new stories. |
    | <kbd>b</kbd> | View the best stories. |
    | <kbd>a</kbd> | View the AskHN stories. |
    | <kbd>s</kbd> | View the ShowHN stories. |
    | <kbd>j</kbd> | View the jobs. |
    """

    CSS = """
    TabbedContent, LoadingIndicator {
        background: $panel;
    }
    """

    TITLE = f"Orange Site Hit v{__version__}"

    BINDINGS = [
        Binding("f1", "help", "Help"),
        Binding("f2", "compact", "Compact/Relaxed"),
        Binding("f3", "toggle_dark"),
        Binding("f12", "quit", "Quit"),
        Binding("t", "go('top')"),
        Binding("n", "go('new')"),
        Binding("b", "go('best')"),
        Binding("a", "go('ask')"),
        Binding("s", "go('show')"),
        Binding("j", "go('jobs')"),
        Binding("down, enter", "pane"),
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

    def compose(self) -> ComposeResult:
        """Compose the main screen's layout."""
        yield Header()
        with HackerNews():
            yield Items("top", "t", self._hn.top_stories)
            yield Items("new", "n", self._hn.new_stories)
            yield Items("best", "b", self._hn.best_stories)
            yield Items("ask", "a", self._hn.latest_ask_stories)
            yield Items("show", "s", self._hn.latest_show_stories)
            yield Items("jobs", "j", self._hn.latest_job_stories)
        yield Footer()

    def _refresh_subtitle(self) -> None:
        """Refresh the subtitle of the screen."""
        self.sub_title = self.query_one(HackerNews).description

    def on_mount(self) -> None:
        """Configure things once the DOM is ready."""
        self.set_interval(0.95, self._refresh_subtitle)

    def action_help(self) -> None:
        """Show the help screen."""
        self.app.push_screen(Help(self))

    def action_go(self, items: str) -> None:
        """Go to the given list of items.

        Args:
            items: The name of the list of items to go to.
        """
        self.query_one(HackerNews).active = items
        self.query_one(HackerNews).focus_active_pane()

    def action_compact(self) -> None:
        """Toggle the compact display."""
        news = self.query_one(HackerNews)
        news.compact = not news.compact

    @on(ShowUser)
    def show_user(self, event: ShowUser) -> None:
        """Handle a request to show the details of a user."""
        self.app.push_screen(UserDetails(self._hn, event.user))

    @on(ShowComments)
    def show_comments(self, event: ShowComments) -> None:
        """Handle a request to show the comments for an article."""
        self.app.push_screen(Comments(self._hn, event.article))


### main.py ends here
