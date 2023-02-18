"""Declare app actions."""

from app.util_types import RunAction
from .test import run


actions: dict[str, RunAction] = {
    'test': run,
}
