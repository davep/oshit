"""The main application class."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .data import load_configuration, save_configuration
from .screens import Main


##############################################################################
class OSHit(App[None]):
    """The Orange Site Hit application."""

    ENABLE_COMMAND_PALETTE = False

    def __init__(self) -> None:
        """Initialise the application."""
        super().__init__()
        self.dark = load_configuration().dark_mode

    def on_mount(self) -> None:
        """Get things going once the app is up and running."""
        self.push_screen(Main())

    def _watch_dark(self) -> None:
        """Save the light/dark mode configuration choice."""
        configuration = load_configuration()
        configuration.dark_mode = self.dark
        save_configuration(configuration)


### oshit.py ends here
