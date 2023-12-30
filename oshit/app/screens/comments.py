"""Provides a modal screen for showing the comments for an item."""

##############################################################################
# Python imports.
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Collapsible, Label

##############################################################################
# Humanize imports.
from humanize import intcomma, naturaltime

##############################################################################
# Local imports.
from ...hn import HN
from ...hn.item import Article


##############################################################################
class Comments(ModalScreen[None]):
    """Dialog for navigating the comments of an item from HackerNews."""

    DEFAULT_CSS = """
    Comments {
        align: center middle;
    }

    Comments > Vertical {
        width: 90%;
        height: 90%;
        background: $surface;
        border: panel $primary;
        border-title-color: $accent;
    }

    Comments #info {
        padding: 1 1 0 1;
        height: auto;
        margin-bottom: 1;
        border-bottom: solid $primary;
    }

    Comments #buttons {
        padding: 1 1 0 1;
        height: auto;
        border-top: solid $primary;
        align-horizontal: right;
    }

    Comments #buttons Button {
        margin-left: 1;
    }

    Comments VerticalScroll {
        height: 1fr;
    }
    """

    BINDINGS = [("space", "visit"), ("escape", "close")]

    def __init__(self, client: HN, article: Article) -> None:
        """Initialise the comments screen.

        Args:
            client: The HackerNews client object.
            article: The article to show the comments for.
        """
        super().__init__()
        self._hn = client
        """The HackerNews client object."""
        self._article = article
        """The article to show the comments for."""

    def compose(self) -> ComposeResult:
        """Compose the comments screen."""
        with Vertical() as dialog:
            dialog.border_title = f"Comments for article #{self._article.item_id}"
            with Vertical(id="info"):
                yield Label(self._article.title, markup=False)
                yield Label(
                    f"{intcomma(self._article.score)} "
                    f"points{'' if self._article.score == 1 else 's'} "
                    f"by {self._article.by} {naturaltime(self._article.time)}",
                )
            yield VerticalScroll(Label("Comments go here"))
            with Horizontal(id="buttons"):
                yield Button("Visit [dim]\\[Space][/]", id="visit")
                yield Button("Okay [dim]\\[Esc][/]", id="close")

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss(None)

    @on(Button.Pressed, "#visit")
    def action_visit(self) -> None:
        """Visit the page for the comments."""
        open_url(self._article.orange_site_url)


### comments.py ends here
