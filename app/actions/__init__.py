"""Declare app actions."""

from app.util_types import RunAction
from .generate_acuco_marker_image import generate_marker
from .configure_perspective_correction import configure_perspective_correction
from .autonomous_ocean_garbage_collector import autonomous_ocean_garbage_collector
from .configure_blob_detection import configure_blob_detection


actions: dict[str, RunAction] = {
    'Generate ArUco marker image': generate_marker,
    'Configure perspective correction': configure_perspective_correction,
    'Configure blob detection': configure_blob_detection,
    'Autonomous Ocean Garbage Collector': autonomous_ocean_garbage_collector,
}
