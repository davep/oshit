"""Provides a modal screen for showing the details of a user."""

##############################################################################
# Python imports.
from html import unescape

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

##############################################################################
# Humanize imports.
from humanize import intcomma, naturaltime

##############################################################################
# Local imports.
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
class UserDetails(ModalScreen):
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
    """

    BINDINGS = [("escape", "close")]

    def __init__(self, user: User) -> None:
        """Initialise the user details dialog.

        Args:
            user: The user details to display.
        """
        super().__init__()
        self._user = user

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
            yield Data(self._user.user_id)
            if self._user.about:
                yield Title("About:")
                yield Data(self._tidy_about(self._user.about))
            yield Title("Karma:")
            yield Data(intcomma(self._user.karma))
            yield Title("Account created:")
            yield Data(
                f"{naturaltime(self._user.created)} [dim]({self._user.created})[/]"
            )
            yield Title("Submission count:")
            yield Data(f"{intcomma(len(self._user.submitted))}")
            with Horizontal():
                yield Button("Okay [dim]\\[Esc]")

    @on(Button.Pressed)
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss(None)


### user.py ends here
