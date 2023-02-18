"""Declare app actions."""

from typing import TypedDict

from app.util_types import RunAction
from .test import run


class __Actions(TypedDict):
    test: RunAction


actions = __Actions(
    test=run
)
