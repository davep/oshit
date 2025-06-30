"""Provides a dialog for viewing and visiting links."""

##############################################################################
# Python imports.
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, OptionList


##############################################################################
class Links(ModalScreen[None]):
    """Modal dialog for showing and visiting links."""

    DEFAULT_CSS = """
    Links {
        align: center middle;

        Vertical {
            padding: 1 2;
            height: auto;
            width: auto;
            max-width: 50%;
            background: $surface;
            border: panel $primary;
            border-title-color: $accent;
        }

        Horizontal {
            height: auto;
            width: 100%;
            align-horizontal: right;
            border-top: solid $primary;
            padding-top: 1;

            Button {
                margin-left: 1;
            }
        }
    }
    """

    BINDINGS = [("escape", "close")]

    def __init__(self, links: list[str]) -> None:
        """Initialise the links dialog.

        Args:
            links: The links to show the user.
        """
        super().__init__()
        self._links = links

    def compose(self) -> ComposeResult:
        """Compose the content of the dialog."""
        with Vertical() as dialog:
            dialog.border_title = "Available links"
            yield OptionList(*self._links)
            with Horizontal():
                yield Button("Okay [dim]\\[Esc][/]", id="close")

    @on(OptionList.OptionSelected)
    def visit(self, event: OptionList.OptionSelected) -> None:
        """Visit the selected link."""
        open_url(self._links[event.option_index])

    @on(Button.Pressed, "#close")
    def action_close(self) -> None:
        """Close the dialog screen."""
        self.dismiss()


### links.py ends here
