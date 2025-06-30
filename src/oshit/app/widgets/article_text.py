"""A widget for showing the text of an article."""

##############################################################################
# Textual imports.
from textual.widgets import Label

##############################################################################
# Local imports.
from ...hn.item import Article


##############################################################################
class ArticleText(Label, can_focus=True):
    """A widget for showing the text of an article."""

    DEFAULT_CSS = """
    ArticleText {
        width: 1fr;
    }
    """

    def __init__(
        self,
        article: Article,
        *,
        id: str | None = None,  # pylint:disable=redefined-builtin
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the widget.

        Args:
            article: The article whose text should be displayed.
            id: The ID of the widget description in the DOM.
            classes: The CSS classes of the widget description.
            disabled: Whether the widget description is disabled or not.
        """
        super().__init__(
            article.text, markup=False, id=id, classes=classes, disabled=disabled
        )


### article_text.py ends here
