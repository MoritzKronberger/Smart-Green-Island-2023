"""Load an image as a mock camera capture."""

import cv2
from logger import logger

__mock_image_path = 'assets/pool.png'


def render_capture():
    """Render an image as a mock camera capture using OpenCV."""
    mock_capture = cv2.imread(__mock_image_path)

    logger.info('Start rendering mock camera capture')

    # Run indefinitely until `esc`-key is pressed or error is reached
    while True:
        try:
            # Show mock camera feed
            cv2.imshow('Mock camera feed', mock_capture)

            # Await keypress
            keypress = cv2.waitKey(0)

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
