"""Autonomous Ocean Garbage Collector backend."""

import cv2
import numpy as np
from typing import Any
from app.components.aruco import ArUco
from app.components.camera import Camera
from app.components.ui import UI
from app.components.pool import Pool, PoolUI
from app.logger import logger


WINDOW_NAME = 'Camera capture'
MOCK_IMAGE_PATH = 'assets/pool.jpg'


def render(camera: Camera, ui: UI, pool: Pool, aruco: ArUco, refresh_rate_ms: int = 15) -> None:
    """Render event loop using OpenCV."""
    logger.info('Start rendering camera capture')

    # Run indefinitely until `esc`-key is pressed or error is reached
    while True:
        try:
            ################
            # Render image #
            ################

            # Read capture
            image = camera.read_capture()

            # Detect marker
            marker = aruco.detect_marker(image, 1)
            if marker:
                marker.visualize(image)

            # Render pool boundaries
            pool.visualize(image)

            # Render the UI
            ui.render(image)

            # Show capture
            cv2.imshow(WINDOW_NAME, image)

            # Read corrected capture
            corrected_image = camera.read_corrected_capture(
                pool.top_left,
                pool.top_right,
                pool.bottom_left,
                pool.bottom_right
            )

            # Detect marker in corrected image
            corrected_marker = aruco.detect_marker(corrected_image, 1)
            if corrected_marker:
                corrected_marker.visualize(corrected_image)

            # Show corrected capture
            cv2.imshow('Corrected capture', corrected_image)

            #################
            # Handle inputs #
            #################

            # Handle mouse events
            def __handle_mouse_event(event: int, x_pos: int, y_pos: int, *_: Any) -> None:  # type: ignore
                # Process mouse event using UI
                ui.handle_mouse_event(event, np.array([x_pos, y_pos]))
            cv2.setMouseCallback(WINDOW_NAME, __handle_mouse_event)

            # Await keypress
            keypress = cv2.waitKey(refresh_rate_ms)

            # Process keypress using UI
            ui.handle_keypress(keypress)

            # Close window on `esc`-press
            if keypress == 27:
                break
        # Close window on error
        except Exception as e:
            logger.error(e)
            break

    # Cleanup after ending imshow-loop
    cv2.destroyAllWindows()

    logger.info('Stopped rendering camera capture')


def main() -> None:
    """Run Autonomous Ocean Garbage Collector backend."""
    # Create components
    camera = Camera(
        mock_image_path=MOCK_IMAGE_PATH,
        camera=1,
        mock=True
    )
    pool = Pool(
        top_left=np.array([20, 20]),
        top_right=np.array([400, 20]),
        bottom_left=np.array([20, 400]),
        bottom_right=np.array([400, 400]),
        top_left_bottom_right_distance_cm=1_000
    )
    aruco = ArUco()

    # Compose UI
    ui = UI()
    pool_ui = PoolUI(pool)
    ui.add_ui_state(pool_ui)

    # Start render loop
    render(camera, ui, pool, aruco)


if __name__ == "__main__":
    main()
