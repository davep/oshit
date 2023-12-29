"""Provides command messages for the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message


##############################################################################
@dataclass
class ShowUser(Message):
    """Command message for requesting that a user's details be shown."""

    user: str
    """The ID of the user to show."""


### commands.py ends here
