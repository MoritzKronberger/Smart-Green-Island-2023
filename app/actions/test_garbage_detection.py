"""Detect floating garbage using blob detection and perspective correction."""

import cv2
from app.components.blob_detection import BlobDetection
from app.components.camera import Camera
from app.components.capture_loop import CaptureLoop
from app.components.ui import UI
from app.settings import CAMERA, MOCK_IMAGE_PATH


def __loop(camera: Camera,
           window_name: str,
           preprocessed_window_name: str,
           ui: UI,
           blob_detection: BlobDetection) -> None:
    # Read capture
    image = camera.read_capture()

    # Detect floating trash blobs
    blob_detection.detect(image, overwrite_if_empty=False)
    # Visualize the preprocessed image used for blob detection
    preprocessed_image = blob_detection.preprocess_image(image)
    # Visualize detected blobs
    blob_detection.visualize(image)
    blob_detection.visualize(preprocessed_image)

    # Render the UI
    ui.render(image)

    # Show capture
    cv2.imshow(window_name, image)
    # Show preprocessed image used for blob detection
    cv2.imshow(preprocessed_window_name, preprocessed_image)


def detect_garbage() -> None:
    """Detect floating garbage using blob detection and perspective correction."""
    # Create components
    camera = Camera(
        mock_image_path=MOCK_IMAGE_PATH,
        camera=CAMERA,
        mock=True,
        perspective_correction_from_cache=True,
    )
    blob_detection = BlobDetection(
        color_channel='g',
        blur=51
    )

    # Compose UI
    ui = UI()

    window_name = 'Overhead capture'
    preprocessed_window_name = 'Preprocessed capture'

    # Run capture loop
    capture_loop = CaptureLoop(
        ui,
        window_name,
        refresh_rate_ms=500
    )
    capture_loop.run(
        __loop,
        camera,
        window_name,
        preprocessed_window_name,
        ui,
        blob_detection
    )
