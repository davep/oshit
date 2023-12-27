"""The main application class."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .screens import Main

##############################################################################
class OSHit(App[None]):
    """The Orange Site Hit application."""

    def on_mount(self) -> None:
        """Get things going once the app is up and running."""
        self.push_screen(Main())

### oshit.py ends here
