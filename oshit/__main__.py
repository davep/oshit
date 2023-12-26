"""The main entry point for the application."""

import asyncio

from .hn.client import HN

##############################################################################
async def run() -> None:
    """Run the application."""
    async for story in await HN().top_stories():
        print(f"{story.item_type} - {story.url}")

##############################################################################
if __name__ == "__main__":
    asyncio.run(run())

### __main__.py ends here
