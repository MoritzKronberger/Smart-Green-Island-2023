"""Generate ArUco marker as PNG image."""

import inquirer
from app.components.aruco import ArUco


def __is_int(x: str) -> bool:
    try:
        int(x)
        return True
    except Exception:
        return False


def generate_marker() -> None:
    """Generate ArUco marker as PNG image."""
    # Prompt user for marker parameters
    questions = [
        inquirer.Text(
            'Id',
            message='Marker Id',
            validate=lambda _, x: __is_int(x),
        ),
        inquirer.Text(
            'Size',
            message='Marker size [px]',
            validate=lambda _, x: __is_int(x),
            default=1200
        ),
        inquirer.Text(
            'Filename',
            message='Marker filename (optional)',
            default=None
        )
    ]
    answers = inquirer.prompt(questions)
    # Generate marker using prompt answers
    if answers:
        marker_id = int(answers['Id'])
        filename = answers['Filename']
        marker_size = int(answers['Size'])
        aruco = ArUco()
        aruco.generate_marker_image(marker_id, filename, marker_size)
