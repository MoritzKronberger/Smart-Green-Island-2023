"""Handle blob detection."""

import cv2
import numpy as np
from app.components.blob_detection.params import BlobDetectionParams
from app.components.tkinter_gui import TkVarVal
from app.util_types import VecFloat


class BlobDetection():
    """Wrapper for OpenCV blob detection."""
    detector: cv2.SimpleBlobDetector
    keypoints: list[cv2.KeyPoint] = []
    params: BlobDetectionParams

    def __init__(self, params: BlobDetectionParams) -> None:
        """Create new OpenCv blob detection."""
        # Set detection parameters
        self.params = params
        # Create detector
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detect(self, image: cv2.Mat) -> None:
        """Detect blob keypoints in OpenCV image."""
        # Preprocess image for better blob detection
        preprocessed = self.preprocess_image(image)
        # Detect blob keypoint in image
        self.keypoints = self.detector.detect(preprocessed)

    def update_parameter(self, name: str, value: TkVarVal) -> None:
        """Update a detection parameter during execution."""
        # Update the parameter
        setattr(self.params, name, value)
        # Refresh the detectors parameters
        self.detector.setParams(self.params)

    def visualize(self, image: cv2.Mat, color: tuple[int, int, int] = (0, 0, 255)) -> None:
        """Render detected keypoints to OpenCV image."""
        # Render keypoint circles
        cv2.drawKeypoints(
            image,
            self.keypoints,
            image,
            color=color,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )
        # Render blob Ids as text
        for i, keypoint in enumerate(self.keypoints):
            cv2.putText(
                image,
                str(i),
                np.array(keypoint.pt, dtype=int),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=color,
                thickness=1
            )

    def preprocess_image(self, image: cv2.Mat) -> cv2.Mat:
        """Preprocess the image for blob detection."""
        # Extract single color channel
        if self.params.extractColorChannel:
            b, g, r = cv2.split(image)
            channels: dict[str, VecFloat] = {
                'r': r,
                'g': g,
                'b': b,
            }
            greyscale = channels[self.params.colorChannel]
        # Or convert to greyscale
        else:
            greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blur image
        if self.params.useBlur:
            blur = int(self.params.blurAmount)
            # Ensure blur value is even
            blur = blur if blur % 2 == 1 else blur+1
            greyscale = cv2.GaussianBlur(
                greyscale,
                [blur, blur],
                int(blur * 0.25)
            )

        # Binary threshold
        if self.params.useBinaryThresholds:
            greyscale = self.__get_binary_threshold(greyscale)

        # Convert back to regular OpenCV image
        return cv2.cvtColor(greyscale, cv2.COLOR_GRAY2BGR)

    def __get_binary_threshold(self, greyscale: cv2.Mat) -> cv2.Mat:
        """Calculate binary pixel matrix using thresholds."""
        # Regular OpenCV threshold:
        # All values < thresh will be set to 0
        # All other values will be set to 255
        #
        # Min threshold:
        # Throw away (set to 0) all values < thresh
        # -> Regular threshold
        #
        # Max threshold:
        # Throw away all values > thresh
        # -> Inverse threshold
        _, min_thresh = cv2.threshold(
            greyscale,
            thresh=int(self.params.minThreshold),
            maxval=255,
            type=cv2.THRESH_BINARY
        )
        _, max_thresh = cv2.threshold(
            greyscale,
            int(self.params.maxThreshold),
            255,
            cv2.THRESH_BINARY_INV
        )
        # Multiply both thresholds to combine them
        # -> "0 values have priority"
        binary_matrix: VecFloat = cv2.multiply(min_thresh, max_thresh)

        return binary_matrix
