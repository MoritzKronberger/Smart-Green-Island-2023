"""Run selected app actions."""

import inquirer
from .actions import actions


def main() -> None:
    """Prompt action selection and run selected action."""
    # Define selection for app actions using inquirer
    # Reference: https://github.com/magmax/python-inquirer
    actions_list = inquirer.List(
        'action',
        message='Launch Autonomous Ocean Garbage Collector action',
        choices=actions.keys()
    )
    # Prompt selection
    print(
        '\n'
        '######################################\n'
        '# Autonomous Ocean Garbage Collector #\n'
        '######################################\n'
    )
    answers = inquirer.prompt([actions_list])
    # Run selected action
    if answers:
        action = answers['action']
        actions[action]()
