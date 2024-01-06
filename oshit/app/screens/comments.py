"""Provides a modal screen for showing the comments for an item."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Label, Footer

##############################################################################
# Humanize imports.
from humanize import intcomma, naturaltime

##############################################################################
# Local imports.
from ...hn import HN
from ...hn.item import Article, Comment
from ..widgets import CommentCard, CommentCardWithReplies


##############################################################################
class Comments(ModalScreen[None]):
    """Dialog for navigating the comments of an item from HackerNews."""

    DEFAULT_CSS = """
    Comments {
        align: center middle;

        &> Vertical {
            width: 90%;
            height: 90%;
            background: $panel;
            border: panel $primary;
            border-title-color: $accent;
        }

        #info {
            padding: 1;
            background: $boost;
            height: auto;
            margin-bottom: 1;
            border-bottom: solid $primary;
        }

        #buttons {
            padding: 1 1 0 1;
            height: auto;
            border-top: solid $primary;
            align-horizontal: right;

            Button {
                margin-left: 1;
            }
        }

        VerticalScroll {
            height: 1fr;
        }

        #no-comments {
            width: 1fr;
            text-align: center;
            color: $text-muted;
            text-style: italic;
        }
    }
    """

    BINDINGS = [("escape", "close")]

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
                    f"point{'' if self._article.score == 1 else 's'} "
                    f"by {self._article.by} {naturaltime(self._article.time)}, "
                    f"{intcomma(self._article.descendants)} comment{'' if self._article.descendants == 1 else 's'}",
                )
            with VerticalScroll() as comments:
                comments.can_focus = False
                yield Label("No comments", id="no-comments")
            with Horizontal(id="buttons"):
                yield Button("Okay [dim]\\[Esc][/]", id="close")
        yield Footer()

    @work
    async def _load_comments(self, within: Widget, item: Article | Comment) -> None:
        """Load the given list of comments into the display.

        Args:
            within: The container to load the comments into.
            item: The item to load the comments for.
        """
        await within.mount_all(
            (CommentCardWithReplies if comment.kids else CommentCard)(
                self._hn, item, comment
            )
            for comment in await self._hn.comments(item)
        )

    async def on_mount(self) -> None:
        """Start the comment loading process once the DOM is ready."""
        if self._article.kids:
            await self.query_one("#no-comments").remove()
            self._load_comments(self.query_one(VerticalScroll), self._article)

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss(None)

    @on(CommentCardWithReplies.LoadReplies)
    def load_replies(self, event: CommentCardWithReplies.LoadReplies) -> None:
        """Load the replies for a comment.

        Args:
            event: The event to handle.
        """
        self._load_comments(event.load_into, event.comment)


### comments.py ends here
