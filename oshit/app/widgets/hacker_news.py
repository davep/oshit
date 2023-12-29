"""Widget that displays the HackerNews content."""

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var
from textual.widgets import TabbedContent, Tabs

##############################################################################
# Local imports.
from ...hn.item import Article
from ..data import load_configuration, save_configuration
from .items import Items


##############################################################################
class HackerNews(TabbedContent):
    """The HackerNews content."""

    BINDINGS = [
        ("escape", "escape"),
        ("down, enter", "pane"),
        ("left", "previous"),
        ("right", "next"),
    ]

    compact: var[bool] = var(True)
    """Should we use a compact or relaxed display?"""

    def on_mount(self) -> None:
        """Configure the widget once the DOM is ready."""
        self.compact = load_configuration().compact_mode

    @property
    def active_items(self) -> Items[Article]:
        """The active items."""
        assert isinstance(items := self.get_pane(self.active), Items)
        return items

    def focus_active_pane(self) -> None:
        """Give focus to the active pane."""
        self.active_items.steal_focus()

    def action_escape(self) -> None:
        """Handle escape being pressed."""
        if self.screen.focused == (tabs := self.query_one(Tabs)):
            self.app.exit()
        else:
            tabs.focus()

    def action_pane(self) -> None:
        """Focus on the current pane."""
        if self.screen.focused == self.query_one(Tabs):
            self.focus_active_pane()

    def action_previous(self) -> None:
        """Move to the previous pane of items."""
        if self.screen.focused != self.query_one(Tabs):
            self.query_one(Tabs).action_previous_tab()

    def action_next(self) -> None:
        """Move to the next pane of items."""
        if self.screen.focused != self.query_one(Tabs):
            self.query_one(Tabs).action_next_tab()

    @on(TabbedContent.TabActivated)
    def _settle_focus(self) -> None:
        """Settle the focus in the best place possible when a tab is activated."""
        if self.active_items.loaded:
            self.active_items.steal_focus()
        else:
            self.query_one(Tabs).focus()

    @property
    def description(self) -> str:
        """The description of the current display."""
        return self.active_items.description

    def _watch_compact(self) -> None:
        """React to the compact value being changed."""
        for pane in self.query(Items).results():
            pane.compact = self.compact
        configuration = load_configuration()
        configuration.compact_mode = self.compact
        save_configuration(configuration)


### hacker_news.py ends here
