"""Set up pool dimensions."""

import json
import cv2
import numpy as np
import pyshine as ps
from typing import Literal
from components.helpers import create_cache_dir_if_not_exists
from components.ui import UIState
from util_types import VecFloat
from logger import logger


class Pool():
    """Keep track of pool dimensions."""
    top_left: VecFloat
    top_right: VecFloat
    bottom_left: VecFloat
    bottom_right: VecFloat
    top_left_bottom_right_distance_cm: float
    cache_constraints: bool

    def __init__(self,
                 top_left: VecFloat,
                 top_right: VecFloat,
                 bottom_left: VecFloat,
                 bottom_right: VecFloat,
                 top_left_bottom_right_distance_cm: float,
                 cache_constraints: bool = True) -> None:
        """Create pool with specific dimensions."""
        self.top_left_bottom_right_distance_cm = top_left_bottom_right_distance_cm
        self.cache_constraints = cache_constraints
        # Try loading constraints from cache
        if cache_constraints:
            try:
                with open('cache/pool_constraints.json', 'r') as f:
                    constraints = json.load(f)
                    self.top_left = np.array(constraints.get('top_left'))
                    self.top_right = np.array(constraints.get('top_right'))
                    self.bottom_left = np.array(constraints.get('bottom_left'))
                    self.bottom_right = np.array(constraints.get('bottom_right'))
                    # Skip setting constraints from parameters if successful
                    return
            except Exception:
                logger.warn('Failed reading pool constraints from cache')
        # Set constraints from parameters if cache could not be loaded
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

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

    def write_constraints(self) -> None:
        """Write pool constraints to cache if cache is enabled for pool instance."""
        if self.cache_constraints:
            try:
                create_cache_dir_if_not_exists()
                with open('cache/pool_constraints.json', 'w+') as f:
                    json.dump(
                        {
                            'top_left': self.top_left.tolist(),
                            'top_right': self.top_right.tolist(),
                            'bottom_left': self.bottom_left.tolist(),
                            'bottom_right': self.bottom_right.tolist(),
                        },
                        f
                    )
            except Exception:
                logger.warn('Failed writing pool constraints to cache')


# Enum for corner shorthands
ECorner = Literal['tl', 'tr', 'bl', 'br']


class PoolUI(UIState):
    """UI for setting the pool boundaries."""
    pool: Pool
    corner: ECorner | None = None
    __key_map: dict[int, ECorner] = {
        49: 'tl',
        50: 'tr',
        51: 'bl',
        52: 'br',
    }

    def __init__(self, pool: Pool) -> None:
        """Create new PoolUI instance."""
        super().__init__(
            keycode=112,
            keyname='P',
            name='Set Pool Boundaries',
            instructions='Select the corner by pressing the corresponding key and set its position by double-clicking.'
        )
        self.pool = pool

    def on_key(self, keypress: int) -> None:
        """Set adjustable corner via keypress."""
        # Set adjustable corner to the presses key
        self.corner = self.__key_map.get(keypress)

    def on_mouse(self, event: int, mouse_pos: VecFloat) -> None:
        """Set corner position using mouse double-click."""
        # Update the adjustable corner's position on double-click
        if event == cv2.EVENT_LBUTTONDBLCLK and self.corner is not None:
            if self.corner == 'tl':
                self.pool.top_left = mouse_pos
            elif self.corner == 'tr':
                self.pool.top_right = mouse_pos
            elif self.corner == 'bl':
                self.pool.bottom_left = mouse_pos
            elif self.corner == 'br':
                self.pool.bottom_right = mouse_pos
            # Try writing constraints to cache
            self.pool.write_constraints()

    def render(self, image: cv2.Mat) -> None:
        """Render corner labels."""
        def __add_corner_label(label: str, corner: ECorner, pos: VecFloat) -> None:
            PADDING = 5
            ps.putBText(
                image,
                label,
                text_offset_x=pos[0] + PADDING,
                text_offset_y=pos[1] + PADDING,
                vspace=PADDING,
                hspace=PADDING,
                background_RGB=(255, 255, 255),
                text_RGB=(255, 0, 0),
                font_scale=0.75,
                thickness=2,
                font=cv2.FONT_HERSHEY_SIMPLEX,
                # Highlight selected corner
                alpha=0 if self.corner == corner else 0.6
            )
        # Add number (= key to select) for every corner
        __add_corner_label('1', 'tl', self.pool.top_left)
        __add_corner_label('2', 'tr', self.pool.top_right)
        __add_corner_label('3', 'bl', self.pool.bottom_left)
        __add_corner_label('4', 'br', self.pool.bottom_right)
