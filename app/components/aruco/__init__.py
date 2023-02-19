"""Handle tracking of ArUco markers."""

from collections import deque
import cv2
import numpy as np
import numpy.typing as npt
from PIL import Image
from cv2 import aruco
from scipy.spatial import distance
from uuid import uuid4

from app.components.helpers import create_dir_if_not_exists
from app.util_types import VecFloat
from app.logger import logger


class ArUco():
    """Wrapper for OpenCV ArUco functionality."""
    __dictionary: aruco.Dictionary
    __detector_parameters: aruco.DetectorParameters
    detector: aruco.ArucoDetector

    def __init__(self, aruco_dict: int = aruco.DICT_7X7_50) -> None:
        """Create OpenCV ArUco wrapper."""
        self.__dictionary = aruco.getPredefinedDictionary(aruco_dict)
        self.__detector_parameters = aruco.DetectorParameters()
        self.detector = aruco.ArucoDetector(self.__dictionary, self.__detector_parameters)

    def get_marker_pixels(self, marker_id: int, size_px: int = 200) -> npt.NDArray[np.uint8]:
        """Get pixel matrix for ArUco marker using its Id."""
        return np.array(self.__dictionary.generateImageMarker(marker_id, size_px), dtype=np.uint8)

    def generate_marker_image(self, marker_id: int, name: str | None = None, size_px: int = 1200) -> None:
        """Generate image for ArUco marker using its Id."""
        marker_pixels = self.get_marker_pixels(marker_id, size_px)
        pil_image = Image.fromarray(marker_pixels)
        create_dir_if_not_exists('app/out')
        filename = f'app/out/{name or uuid4()}_ID_{marker_id}.png'
        pil_image.save(filename)
        logger.info(f'Generated new ArUco marker: {filename}')

    def render_marker(self, image: cv2.Mat, marker_id: int, size: int, x_pos: int, y_pos: int) -> None:
        """Render ArUco marker to OpenCV image."""
        marker_pixels = self.get_marker_pixels(marker_id, size)
        marker_rgb = cv2.cvtColor(marker_pixels, cv2.COLOR_GRAY2RGB)
        image[x_pos:size+x_pos, y_pos:size+y_pos] = marker_rgb


class Marker():
    """Handle OpenCV ArUco marker."""
    id: int
    corners: VecFloat | None
    center: VecFloat | None
    debug: bool
    __corner_buffer: deque[VecFloat] | None

    def __init__(self, id: int, smooth_steps: int = 0, debug: bool = False) -> None:
        """Create ArUco marker instance.

        Use previous marker positions for smoothing by setting `smooth_steps` > 1.
        (Intended for static markers)
        """
        self.id = id
        self.debug = debug
        if smooth_steps > 1:
            self.__corner_buffer = deque([], maxlen=smooth_steps)

    def detect(self, image: cv2.Mat, aruco: ArUco, disable_smooth: bool = False) -> None:
        """Detect ArUco marker in OpenCV image."""
        # Detect all image markers
        corners, ids, _ = aruco.detector.detectMarkers(image)
        try:
            # Get index of the marker Id in list of all detected marker Ids
            marker_ids: list[int] = ids[0].tolist()
            marker_index = marker_ids.index(self.id)
            # Get corners for the marker from list of all detected corners
            marker_corners = np.array(
                corners[0][marker_index],
                dtype=np.float32
            )
            # Set new corners as mean of corner buffer if smoothing is enabled
            if self.__corner_buffer is not None and not disable_smooth:
                self.__corner_buffer.append(marker_corners)
                self.corners = np.mean(np.array(self.__corner_buffer), axis=0)
            # Else set the new corners directly
            else:
                self.corners = marker_corners
            # Center as midpoint between diagonal corners
            if self.corners is not None:
                self.center = (self.corners[0] + self.corners[2]) * 0.5
        except Exception as e:
            if self.debug:
                logger.warn(f'Could not detect marker with id {self.id}', e)
            self.corners = None
            self.center = None

    def visualize(self, image: cv2.Mat, radius: int = 4, color: tuple[int, int, int] = (0, 255, 0)) -> None:
        """Render detected marker to OpenCV image."""
        if self.corners is not None and self.center is not None:
            # Draw circle for each corner and add index number
            for i, corner in enumerate(self.corners):
                cv2.circle(
                    image,
                    corner.astype(int),
                    radius,
                    color=(0, 0, 255) if i == 0 else color,  # top.left: red
                    thickness=-1
                )
                cv2.putText(
                    image,
                    text=str(i),
                    org=corner.astype(int),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=color,
                    thickness=1,
                )
            # Draw marker Id on the marker center
            text_origin = self.center - np.array([10, -10])
            cv2.putText(
                image,
                text=str(self.id),
                org=text_origin.astype(int),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=color,
                thickness=2,
            )
        elif self.debug:
            logger.warn('Cannot render marker: no position exists')

    def get_perspective_transform_matrix(self) -> VecFloat | None:
        """Generate perspective transform matrix from ArUco marker corners."""
        def __get_corrected_corners(top_left: VecFloat, width: int) -> VecFloat:
            top_left_x, top_left_y = top_left
            # Set corners at perfect `width`-distance from `top_left`
            return np.array(
                [
                    top_left,
                    [top_left_x+width, top_left_y],
                    [top_left_x+width, top_left_y+width],
                    [top_left_x, top_left_y+width],
                ],
                dtype=np.float32
            )

        if self.corners is not None:
            # Estimate marker width
            marker_width_px = int(distance.euclidean(self.corners[0], self.corners[1]))

            # Get perspective transform matrix
            M = cv2.getPerspectiveTransform(
                # Current corner locations
                self.corners,
                # Desired corner locations
                __get_corrected_corners(self.corners[0], marker_width_px)
            )

            return np.array(M, dtype=np.float32)
        else:
            return None
