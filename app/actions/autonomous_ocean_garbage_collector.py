"""Execute autonomous ocean garbage collection."""

import cv2
from app.components.aruco import ArUco
from app.components.boat import Boat, BoatUI
from app.components.camera import Camera
from app.components.floating_garbage import FloatingGarbageUI, FloatingGarbage
from app.components.main_loop import MainLoop
from app.components.opencv_ui import UI
from app.settings import ARUCO_DICT, BOAT_MARKER_ID, BOAT_MARKER_SIZE_MM, CAMERA, MOCK_IMAGE_PATH


def __loop(camera: Camera,
           window_name: str,
           ui: UI,
           aruco: ArUco,
           boat: Boat,
           floating_garbage: FloatingGarbage) -> None:
    # Read capture
    image = camera.read_corrected_capture()

    # Calculate boat position, rotation and velocity
    boat.update_location_and_velocity(image, aruco, 15)
    # Render marker
    boat.visualize(image)

    # Detect the floating garbage position
    floating_garbage.detect(image)
    # Render garbage visualization
    floating_garbage.visualize(image)

    # Render the UI
    ui.render(image)

    # Show capture
    cv2.imshow(window_name, image)


def autonomous_ocean_garbage_collector() -> None:
    """Execute autonomous ocean garbage collection."""
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
    floating_garbage = FloatingGarbage(
        blob_id_from_cache=True
    )

    # Compose UI
    ui = UI()
    boat_ui = BoatUI(boat)
    garbage_ui = FloatingGarbageUI(floating_garbage)
    ui.add_ui_state(boat_ui)
    ui.add_ui_state(garbage_ui)

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
        boat,
        floating_garbage
    )
