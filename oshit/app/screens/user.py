"""Provides a modal screen for showing the details of a user."""

##############################################################################
# Python imports.
from html import unescape
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
from ...hn.user import User


##############################################################################
class Title(Label):
    """Widget for showing the title of some data."""

    DEFAULT_CSS = """
    Title {
        color: $accent;
    }
    """


##############################################################################
class Data(Label):
    """Widget for showing some data."""

    DEFAULT_CSS = """
    Data {
        margin-bottom: 1;
    }
    """


##############################################################################
class UserDetails(ModalScreen[None]):
    """Modal dialog for showing the details of a user."""

    DEFAULT_CSS = """
    UserDetails {
        align: center middle;
    }

    UserDetails Vertical {
        padding: 1 2;
        height: auto;
        width: auto;
        min-width: 40%;
        max-width: 80vw;
        background: $surface;
        border: panel $primary;
        border-title-color: $accent;
    }

    UserDetails VerticalScroll {
        max-height: 20;
        height: auto;
        width: auto;
    }

    UserDetails Data {
        max-width: 70vw;
    }

    UserDetails Horizontal {
        height: auto;
        width: 100%;
        align-horizontal: right;
        border-top: solid $primary;
        padding-top: 1;
    }

    UserDetails Button {
        margin-left: 1;
    }

    UserDetails .hidden {
        display: none;
    }
    """

    BINDINGS = [("space", "visit"), ("escape", "close")]

    AUTO_FOCUS = "#close"

    def __init__(self, client: HN, user_id: str) -> None:
        """Initialise the user details dialog.

        Args:
            client: The HackerNews client object.
            user_id: The ID of the user to display.
        """
        super().__init__()
        self._hn = client
        self._user = User(user_id)
        self._user_id = user_id

    @staticmethod
    def _tidy_about(about: str) -> str:
        """Tidy the about string.

        Args:
            about: The about test for a user.

        Returns:
            The about text tidied up for display.

        The about text for a user, as pulled back from the API, is some
        unholy HTML mess. This function does a quick and dirty attempt to
        fix that up.
        """
        return unescape(about.replace("<p>", "\n"))

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Vertical() as dialog:
            dialog.border_title = "User details"
            yield Title("User ID:")
            yield Data(self._user_id)
            yield Title("About:", classes="about hidden")
            with VerticalScroll(classes="about hidden"):
                yield Data(id="about", markup=False)
            yield Title("Karma:")
            yield Data(id="karma")
            yield Title("Account created:")
            yield Data(id="created")
            yield Title("Submission count:")
            yield Data(id="submissions")
            with Horizontal():
                yield Button("Visit [dim]\\[Space][/]", id="visit")
                yield Button("Okay [dim]\\[Esc][/]", id="close")

    def _set(self, field: str, value: str) -> None:
        """Set the value of a field on the form.

        Args:
            field: The field to set.
            value: The value to set the field to.
        """
        self.query_one(f"#{field}", Data).update(value)

    @work
    async def _load_user(self) -> None:
        """Load up the details for the user."""
        self.query_one(Vertical).border_subtitle = "Loading..."
        self._user = await self._hn.user(self._user_id)
        self._set("about", self._tidy_about(self._user.about))
        self._set("karma", intcomma(self._user.karma))
        self._set(
            "created",
            f"{naturaltime(self._user.created)} [dim]({self._user.created})[/]",
        )
        self._set("submissions", f"{intcomma(len(self._user.submitted))}")
        self.query(".about").set_class(
            not bool(self._tidy_about(self._user.about)), "hidden"
        )
        self.query_one(Vertical).border_subtitle = ""

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is ready."""
        self._load_user()

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss(None)

    @on(Button.Pressed, "#visit")
    def action_visit(self) -> None:
        """Visit the page for the user."""
        open_url(self._user.url)


### user.py ends here
