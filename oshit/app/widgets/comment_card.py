"""Provides a card for displaying a HackerNews comment."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.events import Click
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label

##############################################################################
# Humanize imports.
from humanize import naturaltime

##############################################################################
# Local imports.
from ...hn import HN
from ...hn.item import Article, Comment
from ..screens.user import UserDetails


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
        Binding("enter", "gndn"),
        Binding("s", "next(1)", "Next Sibling"),
        Binding("S", "next(-1)", "Prev Sibling", key_display="Sh+S"),
        Binding("p", "goto_parent", "Parent"),
        Binding("r", "goto_root", "Go Root"),
        Binding("u", "view_user", "View User"),
        Binding("v", "view_online", "View on HN"),
    ]

    def __init__(
        self, client: HN, parent_item: Article | Comment, comment: Comment
    ) -> None:
        """Initialise the comment card.

        Args:
            parent_item: The parent item of the comment.
            client: The HackerNews client object.
            comment: The comment display.
        """
        super().__init__(id=f"comment-{comment.item_id}")
        self.border_subtitle = f"#{comment.item_id}"
        self._hn = client
        """The HackerNews client object."""
        self.parent_item = parent_item
        """The item that is the parent of this comment."""
        self.comment = comment
        """The comment to display."""
        self.set_class(self.comment.deleted, "deleted")
        self.set_class(self.comment.flagged, "flagged")
        self.set_class(self.comment.dead, "dead")

    def compose(self) -> ComposeResult:
        """Compose the content of the comment card."""
        if self.comment.deleted:
            self.can_focus = False
            yield Label("Deleted")
            return
        yield Label(self.comment.text, markup=False)
        yield Label(
            f"{self.comment.by}, {naturaltime(self.comment.time)}", classes="byline"
        )

    def action_view_online(self) -> None:
        """View the comment on HackerNews."""
        open_url(self.comment.orange_site_url)

    def action_view_user(self) -> None:
        """View the details of the user who wrote the comment."""
        self.app.push_screen(UserDetails(self._hn, self.comment.by))

    def action_goto_parent(self) -> None:
        """Go to the parent of the current comment."""
        if isinstance(self.parent_item, Comment):
            self.screen.query_one(f"#comment-{self.comment.parent}").focus()
        else:
            self.notify("Already at the top level", severity="warning")

    def action_next(self, direction: int) -> None:
        """Move amongst sibling comments.

        Args:
            direction: The direction to move in.
        """
        if self.parent is None:
            return
        children = [
            child
            for child in self.parent.children
            if isinstance(child, CommentCard) and child.can_focus
        ]
        try:
            current = children.index(self)
        except ValueError:
            return
        candidate = current + direction
        if -1 < candidate < len(children):
            children[candidate].focus()

    def action_goto_root(self) -> None:
        """Navigate up to the root comment."""
        candidate = self
        while True:
            try:
                candidate = self.screen.query_one(
                    f"#comment-{candidate.comment.parent}", CommentCard
                )
            except NoMatches:
                if candidate == self:
                    self.notify("Already at the top level", severity="warning")
                else:
                    candidate.focus()
                return

    def action_gndn(self) -> None:
        """Swallow up enter.

        This stops any press of enter bubbling up to any possible comment
        that does have replies.
        """

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
    CommentCardWithReplies > .replies {
        margin-top: 0;
        link-color: $text-muted;
        link-style: italic;
    }

    CommentCardWithReplies > #replies {
        height: auto;
        margin-top: 1;
        display: none;
    }

    CommentCardWithReplies > #replies.loaded {
        display: block;
    }
    """

    @dataclass
    class LoadReplies(Message):
        """Message to request that replies are loaded."""

        load_into: Widget
        """The card to load the comments into."""

        comment: Comment
        """The comment to load the replies for."""

    def __init__(
        self, client: HN, parent_item: Article | Comment, comment: Comment
    ) -> None:
        """Initialise the comment card.

        Args:
            parent_item: The parent item of the comment.
            client: The HackerNews client object.
            comment: The comment display.
        """
        super().__init__(client, parent_item, comment)
        self._replies_loaded = False
        """Have replies been loaded?"""

    def compose(self) -> ComposeResult:
        yield from super().compose()
        count = len(self.comment.kids)
        yield RepliesLabel(
            f"[@click=load_replies]{count} {'reply' if count == 1 else 'replies'}[/]",
            classes="byline replies",
        )
        yield Vertical(id="replies")

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
            self.post_message(
                self.LoadReplies(self.query_one("#replies"), self.comment)
            )
            self._replies_loaded = True
            self.query_one("#replies").set_class(True, "loaded")


### comment_card.py ends here
