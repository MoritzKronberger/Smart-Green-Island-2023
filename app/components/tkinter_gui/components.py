"""tkinter component presets."""

import tkinter as tk

Number = int | float
TkNumberVar = tk.IntVar | tk.DoubleVar


class HorizontalSlider(tk.Scale):
    """Horizontal slider base on `tkinter.Scale`."""

    def __init__(self,
                 master: tk.Frame,
                 label: str,
                 from_: Number,
                 to: Number,
                 resolution: Number,
                 variable: TkNumberVar) -> None:
        """Create new horizontal slider."""
        super().__init__(
            master,
            label=label,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=tk.HORIZONTAL,
            variable=variable,
            length=500
        )


class Checkbox(tk.Checkbutton):
    """Checkbox base on `tkinter.Checkbutton`."""
    def __init__(self, master: tk.Frame, label: str, variable: tk.BooleanVar) -> None:
        """Create new checkbox."""
        super().__init__(
            master,
            text=label,
            onvalue=True,
            offvalue=False,
            variable=variable
        )
