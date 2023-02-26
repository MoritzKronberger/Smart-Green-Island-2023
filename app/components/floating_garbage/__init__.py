"""Detect floating garbage."""

import json
import cv2
import numpy as np
from app.components.blob_detection import BlobDetection
from app.components.blob_detection.params import BlobDetectionParams
from app.components.helpers import create_dir_if_not_exists
from app.components.opencv_ui import UIState
from app.util_types import VecFloat
from app.logger import logger


class FloatingGarbage():
    """Detect floating garbage."""
    blob_detection: BlobDetection
    blob_id: int | None = None
    center: VecFloat | None = None
    size: float | None = None

    CACHE_FILENAME = 'floating_garbage.json'

    def __init__(self, detection_params: BlobDetectionParams | None = None, blob_id_from_cache: bool = False) -> None:
        """Create new floating garbage detector."""
        params = detection_params or BlobDetectionParams(
            params_from_cache=True
        )
        self.blob_detection = BlobDetection(params)

        if blob_id_from_cache:
            try:
                with open(f'app/cache/{self.CACHE_FILENAME}', 'r') as f:
                    cache_data = json.load(f)
                    self.blob_id = int(cache_data.get('blob_id'))
            except Exception:
                logger.warn('Failed reading floating garbage blob Id from cache.')

    def detect(self, image: cv2.Mat, debug: bool = False) -> None:
        """Detect floating garbage using OPenCV blob detection."""
        def __reset_detection() -> None:
            self.center = None
            self.size = None

        if self.blob_id is not None:
            try:
                self.blob_detection.detect(image)
                garbage_blob = self.blob_detection.keypoints[self.blob_id]
                self.center = garbage_blob.pt
                self.size = garbage_blob.size
            except Exception:
                if debug:
                    logger.warn(f'Could not detect floating garbage with blob Id {self.blob_id}')
                __reset_detection()
        else:
            __reset_detection()

    def visualize(self, image: cv2.Mat, size: int = 4) -> None:
        """Render detected garbage position and size to OPenCV image."""
        if self.center is not None and self.size is not None:
            center = np.array(self.center, dtype=int)
            # Render circle indicating the garbage size
            cv2.circle(
                image,
                center=center,
                radius=int(self.size * 0.5),
                color=(0, 255, 0),
                thickness=2
            )
            # Render circle indicating the garbage center
            cv2.circle(
                image,
                center=center,
                radius=size,
                color=(0, 0, 255),
                thickness=-1
            )


class FloatingGarbageUI(UIState):
    """UI for setting the garbage blob Id."""
    floating_garbage: FloatingGarbage

    def __init__(self, garbage_detection: FloatingGarbage) -> None:
        """Create new FloatingGarbageUI instance."""
        super().__init__(
            keycode=103,
            keyname='G',
            name='Set floating garbage Id',
            instructions='Select the blob to treat as floating garbage by pressing the corresponding number key.'
        )
        self.floating_garbage = garbage_detection

    def on_key(self, keypress: int) -> None:
        """Set the floating garbage's blob Id."""
        # Currently only Ids from 0 to 9 are selectable
        # TODO: Extend if needed
        zero_keycode = 48
        num = keypress - zero_keycode
        if 0 <= num <= 9:
            self.floating_garbage.blob_id = num
            try:
                create_dir_if_not_exists('app/cache')
                with open(f'app/cache/{self.floating_garbage.CACHE_FILENAME}', 'w+') as f:
                    json.dump(
                        {'blob_id': num},
                        f
                    )
            except Exception:
                logger.warn('Failed writing floating garbage blob Id to cache.')

    def render(self, image: cv2.Mat) -> None:
        """Visualize all detected blobs."""
        self.floating_garbage.blob_detection.visualize(image)
