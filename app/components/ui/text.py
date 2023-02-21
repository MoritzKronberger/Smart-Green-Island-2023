"""Helpers for rendering text to OpenCV image."""

import cv2
import pyshine as ps


class Text():
    """Helper class for rendering regular UI text."""
    # Appearance constants
    text: str
    x_pos: int
    y_pos: int
    font_scale: float
    font_thickness: int
    vspace: int
    hspace: int
    background_color_RGB: tuple[int, int, int]
    text_color_RGB: tuple[int, int, int]

    def __init__(self,
                 text: str,
                 x_pos: int,
                 y_pos: int,
                 font_scale: float = 0.5,
                 font_thickness: int = 1,
                 vspace: int = 50,
                 hspace: int = 15,
                 background_color_RGB: tuple[int, int, int] = (0, 0, 0),
                 text_color_RGB: tuple[int, int, int] = (255, 255, 255)) -> None:
        """Create new text helper."""
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font_scale = font_scale
        self.font_thickness = font_thickness
        self.vspace = vspace
        self.hspace = hspace
        self.background_color_RGB = background_color_RGB
        self.text_color_RGB = text_color_RGB

    def render(self, image: cv2.Mat) -> None:
        """Render text to OpenCV image."""
        ps.putBText(
            image,
            self.text,
            text_offset_x=self.x_pos + self.hspace,
            text_offset_y=self.y_pos + self.vspace,
            vspace=self.vspace,
            hspace=self.hspace,
            background_RGB=self.background_color_RGB,
            text_RGB=self.text_color_RGB,
            font_scale=self.font_scale,
            thickness=self.font_thickness,
            font=cv2.FONT_HERSHEY_SIMPLEX
        )


class TextBox():
    """Render text lines in box."""
    lines: list[Text]

    def __init__(self, lines: list[str], x_pos: int, y_pos: int, vspace: int = 15, hspace: int = 50) -> None:
        """Create new text box."""
        # Vertical padding + text
        CONTAINER_HEIGHT = vspace * 2 + 12
        self.lines = [
            Text(line,
                 x_pos=x_pos,
                 # Space underneath ech other
                 y_pos=y_pos + (CONTAINER_HEIGHT * i),
                 vspace=vspace,
                 hspace=hspace)
            for i, line
            in enumerate(lines)
        ]

    def render(self, image: cv2.Mat) -> None:
        """Render text box to OpenCV image."""
        for line in self.lines:
            line.render(image)
