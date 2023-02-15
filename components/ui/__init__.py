"""Handle user input and UI states."""

import cv2
import pyshine as ps
from util_types import VecFloat
from logger import logger


class UIState():
    """Executable UI state that will be entered for the specified keycode."""
    keycode: int
    keyname: str
    name: str
    instructions: str

    def __init__(self, keycode: int, keyname: str, name: str, instructions: str) -> None:
        """Create new executable UI state."""
        self.keycode = keycode
        self.name = name
        self.keyname = keyname
        self.instructions = instructions

    def on_key(self, keypress: int) -> None:
        """Handle keypress with UI state."""

    def on_mouse(self, event: int, mouse_pos: VecFloat) -> None:
        """Handle mouse event with UI state."""

    def render(self, image: cv2.Mat) -> None:
        """Handle UI state rendering."""


class UI():
    """Handle user input and UI states."""

    background_color_RGB: tuple[int, int, int] = (0, 0, 0)
    text_color_RGB: tuple[int, int, int] = (255, 255, 255)
    header_text = 'Available actions:'
    __ui_states: list[UIState] = []
    __ui_state: UIState | None = None

    def __init__(self) -> None:
        """Create UI instance."""

    def __get_ui_state_keycodes(self) -> list[int]:
        """Get keycodes for all ui states."""
        return [state.keycode for state in self.__ui_states]

    def handle_mouse_event(self, event: int, mouse_pos: VecFloat) -> None:
        """Handle UI-specific mouse event."""
        # Forward mouse event to UI state and run it
        if self.__ui_state is not None:
            self.__ui_state.on_mouse(event, mouse_pos)

    def handle_keypress(self, keypress: int) -> None:
        """Handle UI-specific keypress."""
        # Break if no key was pressed
        if keypress == -1:
            return

        # Handle UI state
        ui_state_keycodes = self.__get_ui_state_keycodes()
        if keypress in ui_state_keycodes:
            # Reset UI state if specified UI state is already activated
            if self.__ui_state is not None and keypress == self.__ui_state.keycode:
                self.__ui_state = None
            # Activate specified UI state
            else:
                self.__ui_state = [state for state in self.__ui_states if state.keycode == keypress][0]

        # Forward keypress to UI state and run it
        if self.__ui_state is not None:
            self.__ui_state.on_key(keypress)

    def render(self, image: cv2.Mat) -> None:
        """Render UI (and all UI states) to OpenCV image."""
        # Appearance constants
        FONT_SCALE = 0.5
        FONT_THICKNESS = 1
        VSPACE = 15
        HSPACE = 50
        # Vertical padding + text
        CONTAINER_HEIGHT = VSPACE * 2 + 12

        def __add_text(text: str, x_pos: int, y_pos: int) -> None:
            ps.putBText(
                image,
                text,
                text_offset_x=x_pos,
                text_offset_y=y_pos,
                vspace=VSPACE,
                hspace=HSPACE,
                background_RGB=self.background_color_RGB,
                text_RGB=self.text_color_RGB,
                font_scale=FONT_SCALE,
                thickness=FONT_THICKNESS,
                font=cv2.FONT_HERSHEY_SIMPLEX
            )

        # Render default UI
        if self.__ui_state is None:
            # Draw header text
            __add_text(
                'Press "KEY" to toggle the menus',
                x_pos=HSPACE,
                y_pos=VSPACE
            )

            # Draw list of selectable UI states
            for i, state in enumerate(self.__ui_states):
                __add_text(
                    f'"{state.keyname}" -> {state.name}',
                    x_pos=HSPACE,
                    # Space underneath ech other
                    y_pos=CONTAINER_HEIGHT * (i+1) + VSPACE
                )
        # Render UI state
        else:
            # UI state name
            __add_text(
                self.__ui_state.name,
                x_pos=HSPACE,
                y_pos=VSPACE
            )
            # UI state instructions
            __add_text(
                self.__ui_state.instructions,
                x_pos=HSPACE,
                y_pos=CONTAINER_HEIGHT + VSPACE
            )
            self.__ui_state.render(image)

    def add_ui_state(self, ui_state: UIState) -> None:
        """Add executable UI state."""
        if ui_state.keycode in self.__get_ui_state_keycodes():
            logger.warn(f'Already exists UI state with key code {ui_state.keycode}!')
        self.__ui_states.append(ui_state)
