"""Provides a modal screen for showing the comments for an item."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Click
from textual.message import Message
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
from .user import UserDetails


##############################################################################
class CommentCard(Vertical, can_focus=True):
    """Widget that displays a comment."""

    DEFAULT_CSS = """
    CommentCard {
        border: dashed $primary;
        padding: 0 1 1 1;
        margin-left: 1;
        margin-right: 1;
        height: auto;
    }

    CommentCard.deleted {
        color: $error;
        text-style: italic;
        border: dashed $error 20%;
        padding: 0;
    }

    CommentCard.deleted Label {
        width: 1fr;
        text-align: center;
    }

    CommentCard.flagged Label, CommentCard.dead Label {
        color: $text-disabled;
        text-style: italic;
    }

    CommentCard:focus {
        border: dashed $accent;
        background: $boost;
    }

    CommentCard Label {
        width: 1fr;
    }

    CommentCard .byline {
        margin-top: 1;
        text-align: right;
        color: $text-muted;
        text-style: italic;
    }
    """

    BINDINGS = [
        ("v", "view_online", "View on HN"),
        ("u", "view_user", "View User"),
        ("enter", "load_replies"),
    ]

    def __init__(self, client: HN, comment: Comment) -> None:
        """Initialise the comment card.

        Args:
            client: The HackerNews client object.
            comment: The comment display.
        """
        super().__init__(id=f"comment-{comment.item_id}")
        self.border_subtitle = f"#{comment.item_id}"
        self._hn = client
        """The HackerNews client object."""
        self._comment = comment
        """The comment to display."""
        self.set_class(self._comment.deleted, "deleted")
        self.set_class(self._comment.flagged, "flagged")
        self.set_class(self._comment.dead, "dead")

    def compose(self) -> ComposeResult:
        """Compose the content of the comment card."""
        if self._comment.deleted:
            self.can_focus = False
            yield Label("Deleted")
            return
        yield Label(self._comment.text, markup=False)
        yield Label(
            f"{self._comment.by}, {naturaltime(self._comment.time)}", classes="byline"
        )

    def action_view_online(self) -> None:
        """View the comment on HackerNews."""
        open_url(self._comment.orange_site_url)

    def action_view_user(self) -> None:
        """View the details of the user who wrote the comment."""
        self.app.push_screen(UserDetails(self._hn, self._comment.by))

    def on_click(self, event: Click) -> None:
        """Ensure we get focus when we're clicked within anywhere."""
        self.focus()
        event.stop()


##############################################################################
class RepliesLabel(Label):
    """A label for showing the replies.

    Mostly here to work around:
    https://github.com/Textualize/textual/issues/3690
    """

    class LoadRequested(Message):
        """A message to say that the user requested a load."""

    def action_load_replies(self) -> None:
        """Pass up the request to load."""
        self.post_message(self.LoadRequested())


##############################################################################
class CommentCardWithReplies(CommentCard):
    """A comment card that also has replies."""

    BINDINGS = [
        ("enter", "load_replies", "Replies"),
    ]

    DEFAULT_CSS = """
    CommentCardWithReplies .replies {
        margin-top: 0;
        link-color: $text-muted;
        link-style: italic;
    }
    """

    @dataclass
    class LoadReplies(Message):
        """Message to request that replies are loaded."""

        card: "CommentCard"
        """The card to load the comments into."""

        comment: Comment
        """The comment to load the replies for."""

    def __init__(self, client: HN, comment: Comment) -> None:
        super().__init__(client, comment)
        self._replies_loaded = False
        """Have replies been loaded?"""

    def compose(self) -> ComposeResult:
        yield from super().compose()
        count = len(self._comment.kids)
        yield RepliesLabel(
            f"[@click=load_replies]{count} {'reply' if count == 1 else 'replies'}[/]",
            classes="byline replies",
        )

    @on(RepliesLabel.LoadRequested)
    def action_load_replies(
        self, event: RepliesLabel.LoadRequested | None = None
    ) -> None:
        """Load the replies for this comment."""
        if event is not None:
            event.stop()
        if self._replies_loaded:
            # We've already loaded the comments so let's just bounce into
            # the first one.
            self.query(CommentCard).first().focus()
        else:
            self.post_message(self.LoadReplies(self, self._comment))
            self._replies_loaded = True


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
        background: $panel;
        border: panel $primary;
        border-title-color: $accent;
    }

    Comments #info {
        padding: 1;
        background: $boost;
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

    Comments #no-comments {
        width: 1fr;
        text-align: center;
        color: $text-muted;
        text-style: italic;
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
                    f"by {self._article.by} {naturaltime(self._article.time)}",
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
            (CommentCardWithReplies if comment.kids else CommentCard)(self._hn, comment)
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
        self._load_comments(event.card, event.comment)


### comments.py ends here
