"""Track the boat using ArUco markers and perspective correction."""

import cv2
from app.components.aruco import ArUco
from app.components.boat import Boat, BoatUI
from app.components.camera import Camera
from app.components.main_loop import MainLoop
from app.components.ui import UI
from app.settings import ARUCO_DICT, BOAT_MARKER_ID, BOAT_MARKER_SIZE_MM, CAMERA, MOCK_IMAGE_PATH


def __loop(camera: Camera, window_name: str, ui: UI, aruco: ArUco, boat: Boat) -> None:
    # Read capture
    image = camera.read_corrected_capture()

    # Calculate boat position, rotation and velocity
    boat.update_location_and_velocity(image, aruco, 15)
    # Render marker
    boat.visualize(image)

    # Render the UI
    ui.render(image)

    # Show capture
    cv2.imshow(window_name, image)


def track_boat() -> None:
    """Track the boat using ArUco markers and perspective correction."""
    # Create components
    camera = Camera(
        mock_image_path=MOCK_IMAGE_PATH,
        camera=CAMERA,
        mock=False,
        perspective_correction_from_cache=True
    )
    aruco = ArUco(
        aruco_dict=ARUCO_DICT
    )
    boat = Boat(
        BOAT_MARKER_ID,
        BOAT_MARKER_SIZE_MM
    )

    # Compose UI
    ui = UI()
    boat_ui = BoatUI(boat)
    ui.add_ui_state(boat_ui)

    window_name = 'Overhead capture'

    # Run main loop
    main_loop = MainLoop(
        ui,
        window_name
    )
    main_loop.run(
        __loop,
        camera,
        window_name,
        ui,
        aruco,
        boat
    )
