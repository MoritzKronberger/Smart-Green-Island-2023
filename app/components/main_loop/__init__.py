"""Main application loop for handling OpenCV captures and tkinter GUIs."""

import cv2
import numpy as np
from typing import Any, Callable, ParamSpec
from app.components.tkinter_gui import GUI
from app.components.ui import UI
from app.logger import logger

P = ParamSpec('P')


class MainLoop():
    """Main application loop for handling OpenCV captures and tkinter GUIs."""
    __ui: UI
    refresh_rate_ms: int
    interactive_window: str
    gui: GUI | None

    def __init__(self, ui: UI, interactive_window: str, gui: GUI | None = None, refresh_rate_ms: int = 15) -> None:
        """Create new OpenCV capture loop."""
        self.__ui = ui
        self.refresh_rate_ms = refresh_rate_ms
        self.interactive_window = interactive_window
        self.gui = gui

    def run(self, func: Callable[P, None], *args: P.args, **kwargs: P.kwargs) -> None:
        """Run capture loop."""
        # Run indefinitely until `esc`-key is pressed or error is reached
        while True:
            try:
                ##########
                # OpenCV #
                ##########

                # Run loop callback
                func(*args, **kwargs)

                # Handle mouse events
                def __handle_mouse_event(event: int, x_pos: int, y_pos: int, *_: Any) -> None:  # type: ignore
                    # Process mouse event using UI
                    self.__ui.handle_mouse_event(event, np.array([x_pos, y_pos]))
                cv2.setMouseCallback(self.interactive_window, __handle_mouse_event)

                # Await keypress
                keypress = cv2.waitKey(self.refresh_rate_ms)

                # Process keypress using UI
                self.__ui.handle_keypress(keypress)

                # Close window on `esc`-press
                if keypress == 27:
                    break

                ###########
                # tkinter #
                ###########
                if self.gui is not None:
                    self.gui.update()
            # Close window on error
            except Exception as e:
                logger.error(e)
                break

        # Cleanup after ending loop
        cv2.destroyAllWindows()
        if self.gui:
            self.gui.destroy()
