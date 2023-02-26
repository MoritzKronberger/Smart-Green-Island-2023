"""tkinter GUI interface."""

import tkinter as tk
from tkinter import ttk
from typing import Literal, TypeVar
from app.logger import logger

TkVar = tk.IntVar | tk.DoubleVar | tk.StringVar | tk.BooleanVar
TTkVar = TypeVar('TTkVar', tk.IntVar, tk.DoubleVar, tk.StringVar, tk.BooleanVar)
TkVarVal = int | float | str | bool
TkTraceMode = Literal['write', 'read', 'unset']


class GUI():
    """tkinter GUI interface."""
    __root: tk.Tk
    frame: tk.Frame
    tk_vars: dict[str, tk.Variable] = {}

    def __init__(self, title: str, width: int, height: int) -> None:
        """Create new GUI."""
        self.__root = tk.Tk()
        self.__root.title(title)
        self.__root.geometry(f'{width}x{height}')

        # Make tkinter widget scrollable.
        # Reference:
        # https://www.youtube.com/watch?v=0WafQCaok6g

        # Main frame that fills the entire widget
        main_frame = tk.Frame(self.__root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Add canvas to frame (because canvases are scrollable)
        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient=tk.VERTICAL,
            command=canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to be scrollable
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Frame that will be scrolled
        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # Attach all UI elements to the scrollable frame
        self.frame = scrollable_frame

    def update(self) -> None:
        """Update tkinter UI."""
        self.__root.update()

    def destroy(self) -> None:
        """Destroy tkinter UI."""
        self.__root.destroy()

    def trace_var(self, var: TTkVar, trace: TkTraceMode = 'write') -> TTkVar:
        """Add tracing to tkinter Vars."""
        # Keep var from being garbage collected
        self.tk_vars[var._name] = var  # type: ignore
        # Add var trace
        var.trace_add(
            trace,
            # Pass variable itself to callback via lambda
            # Reference: https://stackoverflow.com/a/23986161/14906871
            lambda name, idx, mode: self.trace_callback(var, name, idx, mode)
        )

        return var

    def trace_callback(self, var: TkVar, name: str, index: str, mode: str) -> None:
        """Callback function for tkinter Var trace."""
        logger.info(f'Traced {name}={var.get()} - {index} - {mode}')
