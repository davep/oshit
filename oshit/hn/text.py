"""Utility code for working with text from HackerNews."""

##############################################################################
# Python imports.
from html import unescape
from re import compile as compile_re
from re import sub
from typing import Pattern

##############################################################################
# Backward-compatible typing.
from typing_extensions import Final

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


HREF: Final[Pattern[str]] = compile_re(r'href="([^"]+)"')
"""Regular expression for finding links in some text."""


##############################################################################
def text_urls(text: str) -> list[str]:
    """Find any links in the given text.

    Args:
        text: The text to look in.

    Returns:
        The list of links found in the text.
    """
    return HREF.findall(unescape(text))


### text.py ends here
