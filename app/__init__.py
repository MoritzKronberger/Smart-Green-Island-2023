"""Run specified app action."""

from .actions import actions


def main() -> None:
    """Run app action."""
    actions['test']()
