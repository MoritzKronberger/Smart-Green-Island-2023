"""Parameters for blob detection."""

import cv2
from typing import Literal

ColorChannel = Literal['r', 'g', 'b']


class BlobDetectionParams(cv2.SimpleBlobDetector_Params):  # type: ignore
    """Extended parameters for blob detection.

    Extend blob detection parameters for custom preprocessing and add typing for useful params.

    Reference:
    https://docs.opencv.org/3.4/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
    """
    # OpenCV BLOB DETECTION PARAMS
    # Color thresholds
    minThreshold: int
    maxThreshold: int
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

    # CUSTOM PREPROCESSING PARAMS
    useBinaryThresholds: bool
    # Color channel
    extractColorChannel: bool
    colorChannel: ColorChannel
    # Blur
    useBlur: bool
    blurAmount: int

    def __init__(self,
                 useBinaryThresholds: bool = False,
                 extractColorChannel: bool = False,
                 colorChannel: ColorChannel = 'g',
                 useBlur: bool = False,
                 blurAmount: int = 5) -> None:
        """Create new blob detection parameters."""
        super().__init__()
        self.useBinaryThresholds = useBinaryThresholds
        self.extractColorChannel = extractColorChannel
        self.colorChannel = colorChannel
        self.useBlur = useBlur
        self.blurAmount = blurAmount
