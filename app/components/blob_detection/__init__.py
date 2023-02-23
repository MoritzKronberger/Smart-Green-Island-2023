"""Handle blob detection."""

import cv2
import numpy as np
from typing import Literal, TypedDict

from app.util_types import VecFloat

ColorChannel = Literal['r', 'g', 'b']


class DetectionParams(TypedDict):
    """Parameters for blob detection.

    Reference:
    https://docs.opencv.org/3.4/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
    """
    # Color thresholds
    minThreshold: float | None
    maxThreshold: float | None
    thresholdStep: float
    # Color filter
    filterByColor: bool
    blobColor: float
    # Area
    filterByArea: bool
    minArea: float
    maxArea: float
    # Circularity
    filterByCircularity: bool
    minCircularity: float
    maxCircularity: float
    # Convexity
    filterByConvexity: bool
    minConvexity: float
    maxConvexity: float
    # Inertia ("elongatedness")
    filterByInertia: bool
    minInertiaRatio: float
    maxInertiaRatio: float
    # Misc
    minDistBetweenBlobs: float


default_parameters: DetectionParams = {
    # Color thresholds
    'minThreshold': 100,
    'maxThreshold': None,
    'thresholdStep': 1,
    # Color filter
    'filterByColor': False,
    'blobColor': 255,
    # Area
    'filterByArea': False,
    'minArea': 5 * 5,
    'maxArea': 800 * 800,
    # Circularity
    'filterByCircularity': False,
    'minCircularity': 0.1,
    'maxCircularity': 1,
    # Convexity
    'filterByConvexity': False,
    'minConvexity': 0.1,
    'maxConvexity': 1,
    # Inertia ("elongatedness")
    'filterByInertia': False,
    'minInertiaRatio': 0.1,
    'maxInertiaRatio': 1,
    # Misc
    'minDistBetweenBlobs': 1,
}


class Blob():
    """Wrapper for OpenCV blob keypoint."""
    keypoint: cv2.KeyPoint
    id: int

    def __init__(self, keypoint: cv2.KeyPoint, id: int) -> None:
        """Create new blob."""
        self.keypoint = keypoint
        self.id = id


class BlobDetection():
    """Wrapper for OpenCV blob detection."""
    detector: cv2.SimpleBlobDetector
    color_channel: ColorChannel | None
    blur: int | None
    blobs: list[Blob] | None = None

    def __init__(self,
                 detection_params: DetectionParams | None = None,
                 color_channel: ColorChannel | None = None,
                 blur: int | None = None) -> None:
        """Create new OpenCv blob detection."""
        # Set detection attributes
        params = cv2.SimpleBlobDetector_Params()
        for p, value in (detection_params or default_parameters).items():
            setattr(params, p, value)
        if color_channel is not None:
            # Filter light blobs (for compatibility with single color channel)
            params.filterByColor = True
            params.blobColor = 255
        # Create detector
        self.detector = cv2.SimpleBlobDetector_create(params)
        # Set preprocessing parameters
        self.color_channel = color_channel
        self.blur = blur

    def detect(self, image: cv2.Mat, overwrite_if_empty: bool = True) -> None:
        """Detect blob keypoints in OpenCV image."""
        # Preprocess image for better blob detection
        preprocessed = self.preprocess_image(image)
        # Detect blob keypoint in image
        keypoints = self.detector.detect(preprocessed, cv2.IMREAD_GRAYSCALE)
        # Update blobs
        # (If no blobs were detected and empty overwrite is disabled: don't upadte)
        if overwrite_if_empty or len(keypoints) > 0:
            self.blobs = [Blob(kpt, i) for i, kpt in enumerate(keypoints)]

    def visualize(self, image: cv2.Mat, color: tuple[int, int, int] = (0, 0, 255)) -> None:
        """Render detected keypoints to OpenCV image."""
        if self.blobs:
            # Render keypoint circles
            keypoints = [blob.keypoint for blob in self.blobs]
            cv2.drawKeypoints(
                image,
                keypoints,
                image,
                color=color,
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
            # Render blob Ids as text
            for blob in self.blobs:
                cv2.putText(
                    image,
                    str(blob.id),
                    np.array(blob.keypoint.pt, dtype=int),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=color,
                    thickness=1
                )

    def preprocess_image(self, image: cv2.Mat) -> cv2.Mat:
        """Preprocess the image for blob detection."""
        # Extract single color channel
        if self.color_channel is not None:
            b, g, r = cv2.split(image)
            channels: dict[str, VecFloat] = {
                'r': r,
                'g': g,
                'b': b,
            }
            greyscale = channels[self.color_channel]
        # Or convert to greyscale
        else:
            greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur image
        if self.blur is not None:
            greyscale = cv2.GaussianBlur(
                greyscale,
                [self.blur, self.blur],
                int(self.blur * 0.25)
            )

        # Convert back to regular OpenCV image
        return cv2.cvtColor(greyscale, cv2.COLOR_GRAY2BGR)
