"""Declare app actions."""

from app.util_types import RunAction
from .test import run
from .generate_acuco_marker_image import generate_marker


actions: dict[str, RunAction] = {
    'test': run,
    'Generate ArUco marker image': generate_marker
}
