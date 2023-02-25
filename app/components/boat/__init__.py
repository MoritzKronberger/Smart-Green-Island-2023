"""Autonomous boat controls."""

import cv2
import numpy as np
from scipy.spatial import distance
from app.components.aruco import ArUco, Marker
from app.components.opencv_ui import UIState
from app.components.opencv_ui.text import TextBox
from app.util_types import VecFloat


class Boat():
    """Autonomous boat controls."""
    marker: Marker
    __marker_size_mm: float
    __center: VecFloat | None = None
    direction: VecFloat | None = None
    velocity_m_per_s: float = 0
    __steps: int = 0

    def __init__(self, marker_id: int, marker_size_mm: float) -> None:
        """Create new autonomous boat controls."""
        self.marker = Marker(
            marker_id
        )
        self.__marker_size_mm = marker_size_mm

    def update_location_and_velocity(self, image: cv2.Mat, aruco: ArUco, step_duration_ms: int) -> None:
        """Calculate the boat's position, direction and velocity."""
        # Add calculation step
        self.__steps += 1

        # Previous position
        p_center = self.__center

        # Detect boat marker
        self.marker.detect(image, aruco)
        corners = self.marker.corners
        center = self.marker.center

        # If marker is detected
        if corners is not None and center is not None:
            # Update boat position
            self.__center = center

            # Calculate new direction
            self.direction = self.__calculate_direction(corners)

            # If previous position was recorded
            if p_center is not None:
                # Calculate velocity
                moved_distance_px = distance.euclidean(p_center, center)
                moved_distance_mm = self.__px_to_mm(moved_distance_px, corners)
                d_time_ms = self.__steps * step_duration_ms
                velocity_mm_per_ms = moved_distance_mm / d_time_ms
                # mm/ms = m/s
                self.velocity_m_per_s = velocity_mm_per_ms

                # Reset steps if all calculations were successful
                self.__steps = 0
        else:
            # Reset direction if marker is not detected
            self.direction = None

    def visualize(self, image: cv2.Mat, direction_line_length_px: int = 100) -> None:
        """Visualize the boat position and direction."""
        # Render marker position
        self.marker.visualize(image, render_id=False)
        # Render boat direction
        center = self.__center
        direction = self.direction
        if center is not None and direction is not None:
            # Render center point
            cv2.circle(
                image,
                np.array(center, dtype=int),
                radius=4,
                color=(0, 0, 255),
                thickness=-1
            )
            # Render line from center along direction vector
            direction_line_end = center + direction * direction_line_length_px
            cv2.line(
                image,
                np.array(center, dtype=int),
                np.array(direction_line_end, dtype=int),
                color=(0, 0, 255),
                thickness=2
            )

    def __calculate_direction(self, corners: VecFloat) -> VecFloat:
        """Calculate the boat's direction vector.

        Only valid for top-down perspective!
        """
        # Assume top-down perspective:
        # Direction: vector from bottom- to top-corner
        # Average corner positions for better results
        direction_base: VecFloat = np.mean([corners[3], corners[2]], axis=0)
        direction_end: VecFloat = np.mean([corners[0], corners[1]], axis=0)
        direction = direction_end - direction_base

        # Calculate unit vector as `v / len(v)`
        direction_hat = direction / np.linalg.norm(direction)
        return direction_hat

    def __px_to_mm(self, px: float, corners: VecFloat) -> float:
        """Calculate millimeters from pixels using known marker size."""
        # Marker side lengths in px
        l_top = distance.euclidean(corners[0], corners[1])
        l_bottom = distance.euclidean(corners[3], corners[2])
        l_left = distance.euclidean(corners[0], corners[3])
        l_right = distance.euclidean(corners[1], corners[2])

        # Average marker side length
        l_mean_px = float(np.mean([l_top, l_bottom, l_left, l_right]))

        # Convert pixel length to millimeters
        mm_per_px = self.__marker_size_mm / l_mean_px
        return px * mm_per_px


class BoatUI(UIState):
    """UI for visualizing the boat's parameters."""
    __boat: Boat

    def __init__(self, boat: Boat) -> None:
        """Create new boat UI."""
        super().__init__(
            keycode=98,
            keyname='B',
            name='Live boat parameters',
            instructions='Parameters:'
        )
        self.__boat = boat

    def render(self, image: cv2.Mat) -> None:
        """Render boat parameters."""
        # Limit velocity string to 3 decimals
        velocity_cm_per_s = self.__boat.velocity_m_per_s * 100
        parameters_text = [
            f'Velocity [m/s]: {"{:.3f}".format(self.__boat.velocity_m_per_s)}',
            f'Velocity [cm/s]: {"{:.2f}".format(velocity_cm_per_s)}'
        ]
        params_text_box = TextBox(parameters_text, 0, 200)
        params_text_box.render(image)
