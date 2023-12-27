"""The main entry point for the application."""

import asyncio

from .hn import HN

##############################################################################
async def run() -> None:
    """Run the application."""
    for story in await HN().top_stories():
        print(f"{story.item_type} - {story.title} - {story.url}")

##############################################################################
if __name__ == "__main__":
    asyncio.run(run())

### __main__.py ends here
