import cv2
from components.camera import Camera
from logger import logger


WINDOW_NAME = 'Camera capture'
MOCK_IMAGE_PATH = 'assets/pool.png'


def render(camera: Camera, refresh_rate_ms: int = 15) -> None:
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

            # Show rendered image
            cv2.imshow(WINDOW_NAME, image)

            #################
            # Handle inputs #
            #################

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

    logger.info('Stopped rendering camera capture')


def main() -> None:
    camera = Camera(
        mock_image_path=MOCK_IMAGE_PATH,
        camera=1,
        mock=True
    )

    render(camera)


if __name__ == "__main__":
    main()
