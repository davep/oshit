"""The main entry point for the application."""

import asyncio

from .hn.client import HN

##############################################################################
async def run() -> None:
    """Run the application."""
    print(await HN().item(await HN().max_item_id()))

##############################################################################
if __name__ == "__main__":
    asyncio.run(run())

### __main__.py ends here
