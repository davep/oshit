"""Configuration dialog for the application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label

##############################################################################
# Local imports.
from ..data import load_configuration, save_configuration


##############################################################################
class ConfigurationDialog(ModalScreen[None]):
    """Configuration dialog for the OSHit settings."""

    DEFAULT_CSS = """
    ConfigurationDialog {

        align: center middle;

        Vertical {
            width: 60%;
            height: auto;
            background: $surface;
            border: panel $primary;
            border-title-color: $accent;
            padding: 1 2;

            Label {
                margin-left: 1;
            }
        }

        Horizontal {
            height: auto;
            align-horizontal: right;

            Button {
                margin-left: 1;
            }
        }
    }
    """

    BINDINGS = [
        ("f2", "save"),
        ("escape", "cancel"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the layout of the dialog."""
        config = load_configuration()
        with Vertical():
            yield Label("Maximum Concurrency:")
            yield Input(str(config.maximum_concurrency), id="max-con", type="integer")
            yield Label("Connection Timeout:")
            yield Input(str(config.connection_timeout), id="timeout", type="integer")
            yield Label("Maximum Top Items:")
            yield Input(str(config.maximum_top), id="max-top", type="integer")
            yield Label("Maximum New Items:")
            yield Input(str(config.maximum_new), id="max-new", type="integer")
            yield Label("Maximum Best Items:")
            yield Input(str(config.maximum_best), id="max-best", type="integer")
            yield Label("Maximum Ask Items:")
            yield Input(str(config.maximum_ask), id="max-ask", type="integer")
            yield Label("Maximum Show Items:")
            yield Input(str(config.maximum_show), id="max-show", type="integer")
            yield Label("Maximum Jobs Items:")
            yield Input(str(config.maximum_jobs), id="max-jobs", type="integer")
            yield Checkbox("Load other tabs in background", config.background_load_tabs)
            with Horizontal():
                yield Button("OK [dim]\\[F2][/]", id="ok")
                yield Button("Cancel [dim]\\[Esc][/]", id="cancel")

    @on(Button.Pressed, "#ok")
    def action_save(self) -> None:
        """Save the configuration."""
        config = load_configuration()
        config.maximum_concurrency = int(self.query_one("#max-con", Input).value)
        config.connection_timeout = int(self.query_one("#timeout", Input).value)
        config.maximum_top = int(self.query_one("#max-top", Input).value)
        config.maximum_new = int(self.query_one("#max-new", Input).value)
        config.maximum_best = int(self.query_one("#max-best", Input).value)
        config.maximum_ask = int(self.query_one("#max-ask", Input).value)
        config.maximum_show = int(self.query_one("#max-show", Input).value)
        config.maximum_jobs = int(self.query_one("#max-jobs", Input).value)
        config.background_load_tabs = self.query_one(Checkbox).value
        save_configuration(config)
        self.dismiss(None)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel the editing of the configuration."""
        self.dismiss(None)


### config.py ends here
