"""Provides a modal screen for showing the comments for an item."""

##############################################################################
# Python imports.
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Humanize imports.
from humanize import intcomma, naturaltime

##############################################################################
# Local imports.
from ...hn import HN
from ...hn.item import Article, Comment


##############################################################################
class CommentCard(Vertical, can_focus=True):
    """Widget that displays a comment."""

    DEFAULT_CSS = """
    CommentCard {
        border-top: blank;
        border-left: blank;
        margin-left: 1;
        margin-right: 1;
        height: auto;
    }

    CommentCard.deleted {
        color: $error;
        text-style: italic;
    }

    CommentCard:focus {
        border-top: vkey $primary;
        border-left: vkey $primary;
        background: $panel;
    }

    CommentCard Label {
        width: 1fr;
    }
    """

    def __init__(self, comment: Comment) -> None:
        """Initialise the comment card.

        Args:
            comment: The comment display.
        """
        super().__init__(id=f"comment-{comment.item_id}")
        self._comment = comment
        """The comment to display."""
        self.set_class(self._comment.deleted, "deleted")

    def compose(self) -> ComposeResult:
        """Compose the content of the comment card."""
        yield Label("Deleted" if self._comment.deleted else self._comment.text)


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
            yield VerticalScroll(Label("[dim][i]No comments[/]", id="no-comments"))
            with Horizontal(id="buttons"):
                yield Button("Visit [dim]\\[Space][/]", id="visit")
                yield Button("Okay [dim]\\[Esc][/]", id="close")

    @work
    async def _load_comments(self, item: Article | Comment) -> None:
        """Load the given list of comments into the display.

        Args:
            item: The item to load the comments for.
        """
        await self.query_one(VerticalScroll).mount_all(
            CommentCard(comment) for comment in await self._hn.comments(item)
        )

    async def on_mount(self) -> None:
        """Start the comment loading process once the DOM is ready."""
        if self._article.kids:
            await self.query_one("#no-comments").remove()
            self._load_comments(self._article)

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss(None)

    @on(Button.Pressed, "#visit")
    def action_visit(self) -> None:
        """Visit the page for the comments."""
        open_url(self._article.orange_site_url)


### comments.py ends here
