"""Declare app actions."""

from app.util_types import RunAction
from .generate_acuco_marker_image import generate_marker
from .configure_perspective_correction import configure_perspective_correction


actions: dict[str, RunAction] = {
    'Generate ArUco marker image': generate_marker,
    'Configure perspective correction': configure_perspective_correction
}
