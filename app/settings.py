"""Declare application settings."""

import os
from cv2 import aruco
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Declare sttings
ARUCO_DICT: int = aruco.DICT_7X7_50
MOCK_IMAGE_PATH = os.getenv('MOCK_IMAGE_PATH') or 'app/assets/pool.jpg'
CAMERA = int(os.getenv('CAMERA') or 0)
PERSPECTIVE_CORRECTION_MARKER_ID = int(os.getenv('PERSPECTIVE_CORRECTION_MARKER_ID') or 1)
PERSPECTIVE_CORRECTION_MARKER_BUFFER_SIZE = int(os.getenv('PERSPECTIVE_CORRECTION_MARKER_BUFFER_SIZE') or 100)
