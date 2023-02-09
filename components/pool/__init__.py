"""Set up pool dimensions."""

import cv2
from util_types import VecFloat


class Pool():
    """Keep track of pool dimensions."""
    top_left: VecFloat
    top_right: VecFloat
    bottom_left: VecFloat
    bottom_right: VecFloat
    top_left_bottom_right_distance_cm: float

    def __init__(self,
                 top_left: VecFloat,
                 top_right: VecFloat,
                 bottom_left: VecFloat,
                 bottom_right: VecFloat,
                 top_left_bottom_right_distance_cm: float) -> None:
        """Create pool with specific dimensions."""
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.top_left_bottom_right_distance_cm = top_left_bottom_right_distance_cm

    def visualize(self, image: cv2.Mat, color: tuple[int, int, int] = (0, 0, 255), thickness: float = 2) -> None:
        """Render pool boundaries to OpenCV image."""
        # Top-left to top-right
        cv2.line(image, self.top_left, self.top_right, color, thickness)
        # Bottom-left to bottom-right
        cv2.line(image, self.bottom_left, self.bottom_right, color, thickness)
        # Top-left to bottom-left
        cv2.line(image, self.top_left, self.bottom_left, color, thickness)
        # Top-right to bottom-right
        cv2.line(image, self.top_right, self.bottom_right, color, thickness)
