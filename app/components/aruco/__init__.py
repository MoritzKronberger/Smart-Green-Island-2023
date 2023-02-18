"""Handle tracking of ArUco markers."""

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


class Marker():
    """Detected ArUco marker."""
    id: int
    corners: VecFloat
    center: VecFloat

    def __init__(self, id: int, corners: VecFloat) -> None:
        """Create ArUco marker instance."""
        self.id = id
        self.corners = corners
        # Center as midpoint between diagonal corners
        self.center = (corners[0] + corners[2]) * 0.5

    def visualize(self, image: cv2.Mat, radius: int = 4, color: tuple[int, int, int] = (0, 255, 0)) -> None:
        """Render detected marker to OpenCv image."""
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

    def get_perspective_transform_matrix(self) -> VecFloat:
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


class ArUco():
    """Wrapper for OpenCV ArUco functionality."""
    __dictionary: aruco.Dictionary
    __detector_parameters: aruco.DetectorParameters
    __detector: aruco.ArucoDetector

    def __init__(self, aruco_dict: int = aruco.DICT_7X7_50) -> None:
        """Create OpenCV ArUco wrapper."""
        self.__dictionary = aruco.getPredefinedDictionary(aruco_dict)
        self.__detector_parameters = aruco.DetectorParameters()
        self.__detector = aruco.ArucoDetector(self.__dictionary, self.__detector_parameters)

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

    def detect_marker(self, image: cv2.Mat, marker_id: int, debug: bool = False) -> Marker | None:
        """Detect specific ArUco marker in image using its Id."""
        corners, ids, _ = self.__detector.detectMarkers(image)
        try:
            # Get index of specified marker Id in list of all detected marker Ids
            marker_ids: list[int] = ids[0].tolist()
            marker_index = marker_ids.index(marker_id)
            # Get corners for specified marker from list of all detected corners
            marker_corners = np.array(
                corners[0][marker_index],
                dtype=np.float32
            )
            return Marker(
                id=marker_id,
                corners=marker_corners,
            )
        except Exception:
            if debug:
                logger.warn(f'Could not detect marker with id {marker_id}')
            return None

    def render_marker(self, image: cv2.Mat, marker_id: int, size: int, x_pos: int, y_pos: int) -> None:
        """Render ArUco marker to OpenCV image."""
        marker_pixels = self.get_marker_pixels(marker_id, size)
        marker_rgb = cv2.cvtColor(marker_pixels, cv2.COLOR_GRAY2RGB)
        image[x_pos:size+x_pos, y_pos:size+y_pos] = marker_rgb
