"""Detect floating garbage using blob detection and perspective correction."""

import cv2
from app.components.blob_detection import BlobDetection
from app.components.blob_detection.gui import BlobDetectionGUI
from app.components.blob_detection.params import BlobDetectionParams
from app.components.camera import Camera
from app.components.main_loop import MainLoop
from app.components.opencv_ui import UI
from app.settings import CAMERA, MOCK_IMAGE_PATH


def __loop(camera: Camera,
           window_name: str,
           preprocessed_window_name: str,
           ui: UI,
           blob_detection: BlobDetection) -> None:
    # Read capture
    image = camera.read_capture()

    # Detect floating trash blobs
    blob_detection.detect(image)
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
        mock=False,
        perspective_correction_from_cache=True,
    )
    blob_detection_params = BlobDetectionParams()
    blob_detection = BlobDetection(blob_detection_params)

    # Compose UI
    ui = UI()

    # Blob detection GUI
    gui = BlobDetectionGUI(blob_detection)

    window_name = 'Overhead capture'
    preprocessed_window_name = 'Preprocessed capture'

    # Run main loop
    main_loop = MainLoop(
        ui,
        window_name,
        gui=gui
    )
    main_loop.run(
        __loop,
        camera,
        window_name,
        preprocessed_window_name,
        ui,
        blob_detection
    )
