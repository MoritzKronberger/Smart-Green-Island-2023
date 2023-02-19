"""Configure perspective correction using ArUco marker."""

import json
import cv2
from app.components.aruco import ArUco, Marker
from app.components.camera import Camera
from app.components.capture_loop import CaptureLoop
from app.components.ui import UI, UIState
from app.components.helpers import create_dir_if_not_exists
from app.settings import ARUCO_DICT, CAMERA, MARKER_BUFFER_SIZE, MOCK_IMAGE_PATH, PERSPECTIVE_CORRECTION_MARKER_ID
from app.logger import logger


# Create UI state for saving the perspective correction
class CorrectionUI(UIState):
    """User interface for perspective correction."""
    camera: Camera

    def __init__(self, camera: Camera) -> None:
        """Create Correction UI."""
        super().__init__(
            keycode=99,
            keyname='C',
            name='Save Perspective Correction',
            instructions='Press "S" to save the current perspective correction.'
        )
        self.camera = camera

    def on_key(self, keypress: int) -> None:
        """Save perspective correction."""
        if keypress == 115:  # s
            # Get current transform matrix
            perspective_transform_matrix = self.camera.perspective_transform_matrix
            if perspective_transform_matrix is not None:
                # Try saving matrix to cache
                try:
                    create_dir_if_not_exists('app/cache')
                    with open('app/cache/perspective_correction.json', 'w+') as f:
                        json.dump(
                            perspective_transform_matrix.tolist(),
                            f
                        )
                    logger.info('Wrote perspective correction to cache')
                except Exception:
                    logger.warn('Failed writing perspective correction to cache')
            else:
                logger.warn('Failed writing perspective correction to cache: no correction matrix exists')

            print(perspective_transform_matrix)


# Create Components
camera = Camera(
    mock_image_path=MOCK_IMAGE_PATH,
    camera=CAMERA,
    mock=False
)
aruco = ArUco(
    aruco_dict=ARUCO_DICT
)
# Enable smoothing for static marker
marker = Marker(
    PERSPECTIVE_CORRECTION_MARKER_ID,
    smooth_steps=MARKER_BUFFER_SIZE
)

# Compose UI
ui = UI()
c_ui = CorrectionUI(camera)
ui.add_ui_state(c_ui)

# CONSTANTS
MAIN_WINDOW_NAME = 'Camera capture'
CORRECTED_WINDOW_NAME = 'Corrected capture'


def __loop() -> None:
    # Read capture
    image = camera.read_capture()

    # Detect marker
    marker.detect(image, aruco)
    # Render marker
    marker.visualize(image)
    # Update the camera's perspective correction
    M = marker.get_perspective_transform_matrix()
    if M is not None:
        camera.perspective_transform_matrix = M

    # Render the UI
    ui.render(image)

    # Show capture
    cv2.imshow(MAIN_WINDOW_NAME, image)

    # Show corrected capture
    corrected_capture = camera.read_corrected_capture()
    cv2.imshow(CORRECTED_WINDOW_NAME, corrected_capture)


def configure_perspective_correction() -> None:
    """Configure perspective correction using ArUco marker."""
    capture_loop = CaptureLoop(
        __loop,
        ui,
        MAIN_WINDOW_NAME
    )
    capture_loop.run()
