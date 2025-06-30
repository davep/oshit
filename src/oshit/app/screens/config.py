"""Configuration dialog for the application."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.validation import Number
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

        & > Vertical {
            width: 60%;
            height: auto;
            background: $surface;
            border: panel $primary;
            border-title-color: $accent;
            padding: 1 2;

            Grid {
                grid-size: 3;
                grid-rows: auto;
                height: 12;

                Label {
                    margin-left: 1;
                    width: 1fr;
                }

                Input {
                    width: 1fr;
                }
            }

            Checkbox {
                margin-top: 1;
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
        with Vertical() as dialog:
            dialog.border_title = "OSHit Configuration"
            with Grid():
                with Vertical():
                    yield Label("Maximum Concurrency:")
                    yield Input(
                        str(config.maximum_concurrency),
                        id="max-con",
                        type="integer",
                        validators=[Number(minimum=1, maximum=500)],
                    )
                with Vertical():
                    yield Label("Connection Timeout:")
                    yield Input(
                        str(config.connection_timeout),
                        id="timeout",
                        type="integer",
                        validators=[Number(minimum=1, maximum=60)],
                    )
                with Vertical():
                    yield Label("Maximum Top Items:")
                    yield Input(
                        str(config.maximum_top),
                        id="max-top",
                        type="integer",
                        validators=[Number(minimum=1, maximum=500)],
                    )
                with Vertical():
                    yield Label("Maximum New Items:")
                    yield Input(
                        str(config.maximum_new),
                        id="max-new",
                        type="integer",
                        validators=[Number(minimum=1, maximum=500)],
                    )
                with Vertical():
                    yield Label("Maximum Best Items:")
                    yield Input(
                        str(config.maximum_best),
                        id="max-best",
                        type="integer",
                        validators=[Number(minimum=1, maximum=200)],
                    )
                with Vertical():
                    yield Label("Maximum Ask Items:")
                    yield Input(
                        str(config.maximum_ask),
                        id="max-ask",
                        type="integer",
                        validators=[Number(minimum=1, maximum=200)],
                    )
                with Vertical():
                    yield Label("Maximum Show Items:")
                    yield Input(
                        str(config.maximum_show),
                        id="max-show",
                        type="integer",
                        validators=[Number(minimum=1, maximum=200)],
                    )
                with Vertical():
                    yield Label("Maximum Jobs Items:")
                    yield Input(
                        str(config.maximum_jobs),
                        id="max-jobs",
                        type="integer",
                        validators=[Number(minimum=1, maximum=200)],
                    )
            yield Checkbox("Load other tabs in background", config.background_load_tabs)
            with Horizontal():
                yield Button("OK [dim]\\[F2][/]", id="ok")
                yield Button("Cancel [dim]\\[Esc][/]", id="cancel")

    @property
    def dialog_valid(self) -> bool:
        """Is the dialog as a whole valid?"""
        for field in self.query(Input).results():
            if not field.is_valid:
                return False
        return True

    @on(Button.Pressed, "#ok")
    def action_save(self) -> None:
        """Save the configuration."""
        if self.dialog_valid:
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

    @on(Input.Changed)
    def allow_okay(self) -> None:
        """Enable or disable the OK button based on the dialog validity."""
        self.query_one("#ok").disabled = not self.dialog_valid

    def on_mount(self) -> None:
        """Configure the dialog on mount."""
        self.allow_okay()


### config.py ends here
