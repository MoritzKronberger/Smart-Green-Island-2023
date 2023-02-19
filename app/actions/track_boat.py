"""Track the boat using ArUco markers and perspective correction."""

import cv2
from app.components.aruco import ArUco, Marker
from app.components.camera import Camera
from app.components.capture_loop import CaptureLoop
from app.components.ui import UI
from app.settings import ARUCO_DICT, BOAT_MARKER_ID, CAMERA, MOCK_IMAGE_PATH


def __loop(camera: Camera, window_name: str, ui: UI, aruco: ArUco, boat_marker: Marker) -> None:
    # Read capture
    image = camera.read_corrected_capture()

    # Detect marker
    boat_marker.detect(image, aruco)
    # Render marker
    boat_marker.visualize(image)

    # Render the UI
    ui.render(image)

    # Show capture
    cv2.imshow(window_name, image)


def track_boat() -> None:
    """Track the boat using ArUco markers and perspective correction."""
    # Create components
    camera = Camera(
        mock_image_path=MOCK_IMAGE_PATH,
        camera=CAMERA,
        mock=False,
        perspective_correction_from_cache=True
    )
    aruco = ArUco(
        aruco_dict=ARUCO_DICT
    )
    marker = Marker(
        BOAT_MARKER_ID
    )

    # Compose UI
    ui = UI()

    window_name = 'Overhead capture'

    # Run capture loop
    capture_loop = CaptureLoop(
        ui,
        window_name
    )
    capture_loop.run(
        __loop,
        camera,
        window_name,
        ui,
        aruco,
        marker
    )
