"""Helper functions for components."""

from pathlib import Path


def create_dir_if_not_exists(dirname: str) -> None:
    """Create cache directory if not exists."""
    Path(dirname).mkdir(parents=True, exist_ok=True)
