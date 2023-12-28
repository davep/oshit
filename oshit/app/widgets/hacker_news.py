"""Widget that displays the HackerNews content."""

##############################################################################
# Textual imports.
from textual.widgets import TabbedContent
from textual.widgets import Tabs

##############################################################################
# Local imports.
from .items import Items

##############################################################################
class HackerNews(TabbedContent):
    """The HackerNews content."""

    BINDINGS = [
        ("escape", "tabs"),
        ("down, enter", "pane"),
        ("left", "previous"),
        ("right", "next"),
    ]

    @property
    def active_items(self) -> Items:
        """The active items."""
        assert isinstance(items := self.get_pane(self.active), Items)
        return items

    def focus_active_pane(self) -> None:
        """Give focus to the active pane."""
        self.active_items.steal_focus()

    def action_tabs(self) -> None:
        """Focus on the tabs."""
        self.query_one(Tabs).focus()

    def action_pane(self) -> None:
        """Focus on the current pane."""
        if self.screen.focused == self.query_one(Tabs):
            self.focus_active_pane()

    def action_previous(self) -> None:
        """Move to the previous pane of items."""
        if self.screen.focused != self.query_one(Tabs):
            self.query_one(Tabs).action_previous_tab()
            self.call_after_refresh(self.focus_active_pane)

    def action_next(self) -> None:
        """Move to the next pane of items."""
        if self.screen.focused != self.query_one(Tabs):
            self.query_one(Tabs).action_next_tab()
            self.call_after_refresh(self.focus_active_pane)

    @property
    def description(self) -> str:
        """The description of the current display."""
        return self.active_items.description

### hacker_news.py ends here
