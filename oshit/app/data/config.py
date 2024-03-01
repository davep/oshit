"""Code relating to the application's configuration file."""

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass
from functools import lru_cache
from json import dumps, loads
from pathlib import Path

##############################################################################
# Local imports.
from .locations import config_dir


##############################################################################
@dataclass
class Configuration:
    """The configuration data for the application."""

    dark_mode: bool = True
    """Should we run in dark mode?"""

    compact_mode: bool = True
    """Should the items display in compact mode?"""

    item_numbers: bool = False
    """Should we show numbers against items in the lists?"""

    show_data_age: bool = True
    """Should we show the age of the data in the lists?"""

    maximum_concurrency: int = 50
    """The maximum number of connections to use when getting items."""

    connection_timeout: int | None = 20
    """The timeout (in seconds) to use when connecting to the HackerNews API."""

    maximum_top: int = 500
    """The maximum number of top stories to show."""

    maximum_new: int = 500
    """The maximum number of new stories to show."""

    maximum_best: int = 200
    """The maximum number of best stories to show."""

    maximum_ask: int = 200
    """The maximum number of AskHN stories to show."""

    maximum_show: int = 200
    """The maximum number of ShowHN stories to show."""

    maximum_jobs: int = 200
    """The maximum number of jobs to show."""

    background_load_tabs: bool = True
    """Should the content of the tabs try and load in the background?"""


##############################################################################
def configuration_file() -> Path:
    """The path to the file that holds the application configuration.

    Returns:
        The path to the configuration file.
    """
    return config_dir() / "configuration.json"


##############################################################################
def save_configuration(configuration: Configuration) -> Configuration:
    """Save the given configuration.

    Args:
        The configuration to store.

    Returns:
        The configuration.
    """
    load_configuration.cache_clear()
    configuration_file().write_text(
        dumps(asdict(configuration), indent=4), encoding="utf-8"
    )
    return load_configuration()


##############################################################################
@lru_cache(maxsize=None)
def load_configuration() -> Configuration:
    """Load the configuration.

    Returns:
        The configuration.

    Note:
        As a side-effect, if the configuration doesn't exist a default one
        will be saved to storage.

        This function is designed so that it's safe and low-cost to
        repeatedly call it. The configuration is cached and will only be
        loaded from storage when necessary.
    """
    source = configuration_file()
    return (
        Configuration(**loads(source.read_text(encoding="utf-8")))
        if source.exists()
        else save_configuration(Configuration())
    )


### config.py ends here
