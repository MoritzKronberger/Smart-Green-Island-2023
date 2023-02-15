"""Helper functions for components."""

from pathlib import Path


def create_cache_dir_if_not_exists() -> None:
    """Create cache directory if not exists."""
    Path('cache').mkdir(parents=True, exist_ok=True)
