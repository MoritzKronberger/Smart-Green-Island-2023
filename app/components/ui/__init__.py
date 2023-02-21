"""Handle user input and UI states."""

import cv2
from .text import TextBox
from app.util_types import VecFloat
from app.logger import logger


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

    header_text = 'Press "KEY" to toggle the menus'
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
        # Render default UI
        if self.__ui_state is None:
            # List of UI state text lines
            ui_states_text = [f'"{state.keyname}" -> {state.name}' for state in self.__ui_states]
            # Prepend header text to UI states text
            ui_text = [self.header_text] + ui_states_text
            # Draw UI text as textbox
            ui_states_textbox = TextBox(
                ui_text,
                x_pos=0,
                y_pos=0
            )
            ui_states_textbox.render(image)

        # Render UI state
        else:
            # UI state name and instructions
            ui_state_textbox = TextBox(
                [self.__ui_state.name, self.__ui_state.instructions],
                x_pos=0,
                y_pos=0
            )
            ui_state_textbox.render(image)

            # UI state rendering
            self.__ui_state.render(image)

    def add_ui_state(self, ui_state: UIState) -> None:
        """Add executable UI state."""
        if ui_state.keycode in self.__get_ui_state_keycodes():
            logger.warn(f'Already exists UI state with key code {ui_state.keycode}!')
        self.__ui_states.append(ui_state)
