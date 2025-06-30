"""Provides command messages for the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Textual imports.
from textual.message import Message

##############################################################################
# Local imports.
from ..hn.item import Article


##############################################################################
@dataclass
class ShowUser(Message):
    """Command message for requesting that a user's details be shown."""

    user: str
    """The ID of the user to show."""


##############################################################################
@dataclass
class ShowComments(Message):
    """Command message for requesting that an article's comments be shown."""

    article: Article
    """The article to show the comments for."""


### commands.py ends here
