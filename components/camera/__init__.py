"""Load an image as a mock camera capture."""

import cv2
import numpy as np
from logger import logger
from pool import Pool
from observer import Observer

__mock_image_path = 'assets/pool.png'


def render_capture(observer: Observer, pool: Pool, refresh_rate_ms: int = 15) -> None:
    """Render an image as a mock camera capture using OpenCV."""
    logger.info('Start rendering mock camera capture')

    # Run indefinitely until `esc`-key is pressed or error is reached
    while True:
        try:
            # Create fake capture
            mock_capture = cv2.imread(__mock_image_path)
            # Render pool
            pool.visualize(mock_capture)
            # Show mock camera feed
            cv2.imshow('Mock camera feed', mock_capture)

            def __handle_mouse(event: int, x: float, y: float, flags: int, param: int) -> None:
                mouse_pos = np.array([x, y])
                observer.handle_mouse_click(event, mouse_pos, pool)

            cv2.setMouseCallback('Mock camera feed', __handle_mouse)

            # Await keypress
            keypress = cv2.waitKey(refresh_rate_ms)

            # Close window on `esc`-press
            if keypress == 27:
                break
        # Close window on error
        except Exception as e:
            logger.error(e)
            break

    # Cleanup after ending imshow-loop
    cv2.destroyAllWindows()

    logger.info('Stopped rendering mock camera capture')
