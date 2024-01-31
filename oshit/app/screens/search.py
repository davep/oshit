"""Provides a dialog for prompting for a search string."""

##############################################################################
# Backward compatibility
from __future__ import annotations

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input


##############################################################################
class Search(ModalScreen[str | None]):
    """A modal dialog for getting a string to search for."""

    DEFAULT_CSS = """
    Search {
        align: center middle;
    }

    Search Input, Search Input:focus {
        border: round $accent;
        width: 60%;
        padding: 1;
        height: auto;
    }
    """

    BINDINGS = [("escape", "escape")]

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield Input(placeholder="Enter text to look for in locally-loaded items")

    @on(Input.Submitted)
    def search(self) -> None:
        """Perform the search."""
        self.dismiss(self.query_one(Input).value.strip())

    def action_escape(self) -> None:
        """Escape out without searching."""
        self.dismiss(None)


### search.py ends here
