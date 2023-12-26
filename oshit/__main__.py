"""The main entry point for the application."""

import asyncio

from .hn.client import HN

##############################################################################
async def run() -> None:
    """Run the application."""
    for story in await HN().top_story_ids():
        if not (story := await HN().item(story)).url:
            print(story)

##############################################################################
if __name__ == "__main__":
    asyncio.run(run())

### __main__.py ends here
