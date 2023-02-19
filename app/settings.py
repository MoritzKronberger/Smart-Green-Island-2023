"""Declare application settings."""

from cv2 import aruco

########
# MAIN #
########
ARUCO_DICT: int = aruco.DICT_7X7_50
MOCK_IMAGE_PATH = 'app/assets/pool.jpg'
CAMERA = 0

##########################
# PERSPECTIVE CORRECTION #
##########################

PERSPECTIVE_CORRECTION_MARKER_ID = 1
MARKER_BUFFER_SIZE = 100
