"""Load an image as a mock camera capture."""

import json
import cv2
import numpy as np
from app.logger import logger
from app.util_types import VecFloat


class Camera():
    """Handle (mock) OpenCV camera capture."""
    __mock_image_path: str
    __camera: int
    __capture: cv2.VideoCapture
    __mock_capture: cv2.Mat
    __mock: bool
    perspective_transform_matrix: VecFloat | None = None

    def __init__(self,
                 mock_image_path: str,
                 camera: int,
                 mock: bool,
                 perspective_correction_from_cache: bool = False) -> None:
        """Set up (mock) camera instance."""
        self.__mock_image_path = mock_image_path
        self.__camera = camera
        self.__mock = mock

        # Create (mock) capture
        self.__create_capture()

        if perspective_correction_from_cache:
            try:
                with open('app/cache/perspective_correction.json', 'r') as f:
                    self.perspective_transform_matrix = np.array(json.load(f))
            except Exception:
                logger.warn('Failed reading perspective correction matrix from cache')

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

    def read_corrected_capture(self) -> cv2.Mat:
        """Read capture and correct perspective."""
        image = self.read_capture()
        height, width = image.shape[:2]
        if self.perspective_transform_matrix is not None:
            # Transform current capture
            return cv2.warpPerspective(
                image,
                self.perspective_transform_matrix,
                (width, height),
                flags=cv2.INTER_LINEAR
            )
        else:
            return image
