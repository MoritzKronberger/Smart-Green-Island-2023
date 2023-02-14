"""Load an image as a mock camera capture."""

import cv2
import numpy as np
from logger import logger
from util_types import VecFloat


class Camera():
    """Handle (mock) OpenCV camera capture."""
    __mock_image_path: str
    __camera: int
    __capture: cv2.VideoCapture
    __mock_capture: cv2.Mat
    __mock: bool

    def __init__(self, mock_image_path: str, camera: int, mock: bool) -> None:
        """Set up (mock) camera instance."""
        self.__mock_image_path = mock_image_path
        self.__camera = camera
        self.__mock = mock

        # Create (mock) capture
        self.__create_capture()

        logger.info(
            f'Created camera capture'
            f' {f"using mock image {self.__mock_image_path}" if self.__mock else f"using camera {self.__camera}"}'
        )

    def __create_capture(self) -> None:
        """Create (mock) OpenCV capture using camera Id."""
        if self.__mock:
            self.__mock_capture = cv2.imread(self.__mock_image_path)
        else:
            self.__capture = cv2.VideoCapture(self.__camera)

    def read_capture(self) -> cv2.Mat:
        """Read (mock) OpenCV capture."""
        if self.__mock:
            return self.__mock_capture.copy()
        else:
            _, image = self.__capture.read()
            return image.copy()

    def read_corrected_capture(self,
                               top_left: VecFloat,
                               top_right: VecFloat,
                               bottom_left: VecFloat,
                               bottom_right: VecFloat,
                               corrected_width: int = 1000,
                               corrected_height: int = 1000) -> cv2.Mat:
        """Read capture and correct perspective."""
        # Get transformation matrix
        M = cv2.getPerspectiveTransform(
            # Current corner locations
            np.array([
                top_left,
                top_right,
                bottom_left,
                bottom_right
            ], dtype=np.float32),
            # Desired corner locations
            np.array([
                (0, 0),
                (corrected_width, 0),
                (0, corrected_height),
                (corrected_width, corrected_height)
            ], dtype=np.float32)
        )
        # Transform current capture
        image = self.read_capture()
        transformed_image = cv2.warpPerspective(
            image,
            M,
            (corrected_width, corrected_height),
            flags=cv2.INTER_LINEAR
        )

        return transformed_image
