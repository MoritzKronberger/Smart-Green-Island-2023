import tkinter as tk
from typing import Literal, TypeVar
from app.logger import logger

TkVar = tk.IntVar | tk.DoubleVar | tk.StringVar | tk.BooleanVar
TTkVar = TypeVar('TTkVar', tk.IntVar, tk.DoubleVar, tk.StringVar, tk.BooleanVar)
TkVarVal = int | float | str | bool
TkTraceMode = Literal['write', 'read', 'unset']


class GUI():
    """tkinter GUI interface."""
    root: tk.Tk
    tk_vars: dict[str, tk.Variable] = {}

    def __init__(self) -> None:
        """Create new GUI."""
        self.root = tk.Tk()

    def update(self) -> None:
        """Update tkinter UI."""
        self.root.update()

    def destroy(self) -> None:
        """Destroy tkinter UI."""
        self.root.destroy()

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
