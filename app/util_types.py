"""Utility types for the entire application."""

import numpy as np
import numpy.typing as npt
from typing import Callable

VecFloat = npt.NDArray[np.float32]
RunAction = Callable[[], None]
