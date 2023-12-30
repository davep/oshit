"""Utility code for working with text from HackerNews."""

##############################################################################
# Python imports.
from re import sub
from html import unescape

##############################################################################
# TODO! Throw in some proper HTML parsing here.
##############################################################################


##############################################################################
def tidy_text(text: str) -> str:
    """Tidy up some text from the HackerNews API.

    Args:
        text: The text to tidy up.

    Returns:
        The text tidied up for use in the terminal rather than on the web.
    """
    return sub("<[^<]+?>", "", unescape(text.replace("<p>", "\n\n")))


### text.py ends here
