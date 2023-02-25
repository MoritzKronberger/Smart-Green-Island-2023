"""Parameters for blob detection."""

import json
import cv2
from typing import Literal
from app.components.helpers import create_dir_if_not_exists
from app.logger import logger

ColorChannel = Literal['r', 'g', 'b']


class BlobDetectionParams(cv2.SimpleBlobDetector_Params):  # type: ignore
    """Extended parameters for blob detection.

    Extend blob detection parameters for custom preprocessing and add typing for useful params.

    Reference:
    https://docs.opencv.org/3.4/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
    """
    # OpenCV BLOB DETECTION PARAMS
    # Color
    filterByColor: bool
    blobColor: int
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

    __CACHE_FILNAME = 'blob_detection_parameters.json'

    def __init__(self,
                 useBinaryThresholds: bool = False,
                 extractColorChannel: bool = False,
                 colorChannel: ColorChannel = 'g',
                 useBlur: bool = False,
                 blurAmount: int = 5,
                 params_from_cache: bool = False) -> None:
        """Create new blob detection parameters."""
        super().__init__()
        self.useBinaryThresholds = useBinaryThresholds
        self.extractColorChannel = extractColorChannel
        self.colorChannel = colorChannel
        self.useBlur = useBlur
        self.blurAmount = blurAmount

        if params_from_cache:
            self.__read_parameters()

    def __read_parameters(self) -> None:
        """Read blob detection parameters from cache."""
        try:
            with open(f'app/cache/{self.__CACHE_FILNAME}', 'r') as f:
                params = json.load(f)
                for key, value in params.items():
                    setattr(self, key, value)
        except Exception as e:
            logger.warn(f'Failed reading blob detection parameters from cache: {e}')

    def __write_parameters__(self) -> None:
        """Write blob detection parameters to cache."""
        try:
            # Dirty hack to access the OpenCV base-class-attributes (IMPROVE ME!)
            attribute_names = dir(self)
            public_attribute_names = [name for name in attribute_names if name[0] != '_']
            parameter_dict = {name: self.__getattribute__(name) for name in public_attribute_names}

            # Write parameters to JSON file
            create_dir_if_not_exists('app/cache')
            with open(f'app/cache/{self.__CACHE_FILNAME}', 'w+') as f:
                json.dump(parameter_dict, f)
            logger.info('Wrote blob detection parameters to cache')
        except Exception as e:
            logger.warn(f'Failed writing blob detection parameters to cache: {e}')
