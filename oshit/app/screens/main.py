"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from oshit import __version__
from oshit.hn import HN
from oshit.app.widgets import HackerNews, Items


##############################################################################
class Main(Screen[None]):
    """The main screen of the application."""

    CSS = """
    TabbedContent {
        background: $panel;
    }
    """

    TITLE = "Orange Site Hit"
    SUB_TITLE = f"v{__version__}"
    AUTO_FOCUS = "#top > *"

    BINDINGS = [
        ("t", "go('top')"),
        ("n", "go('new')"),
        ("a", "go('ask')"),
        ("s", "go('show')"),
        ("j", "go('jobs')"),
        ("escape", "tabs"),
        ("down, enter", "pane"),
        ("d", "compact"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the main screen's layout."""
        yield Header()
        with HackerNews():
            yield Items("top", "t", HN().top_stories)
            yield Items("new", "n", HN().new_stories)
            yield Items("ask", "a", HN().latest_ask_stories)
            yield Items("show", "s", HN().latest_show_stories)
            yield Items("jobs", "j", HN().latest_job_stories)
        yield Footer()

    def _refresh_subtitle(self) -> None:
        """Refresh the subtitle of the screen."""
        self.sub_title = self.query_one(HackerNews).description

    def on_mount(self) -> None:
        """Configure things once the DOM is ready."""
        self.set_interval(0.95, self._refresh_subtitle)
        self.call_after_refresh(self.query_one(HackerNews).focus_active_pane)

    def action_go(self, items: str) -> None:
        """Go to the given list of items.

        Args:
            items: The name of the list of items to go to.
        """
        self.query_one(HackerNews).active = items
        self.query_one(HackerNews).focus_active_pane()

    def action_compact(self) -> None:
        """Toggle the compact display."""
        self.query_one(HackerNews).compact = not self.query_one(HackerNews).compact


### main.py ends here
