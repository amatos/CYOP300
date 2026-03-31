"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: misc. helper functions for lab3.
"""

import sys
from typing import TypeVar, Type

try:
    import lab3prompt
    import lab3search_states
    import lab3states
    import lab3graph
    import lab3modify_pop
except ImportError:
    from . import lab3prompt
    from . import lab3search_states
    from . import lab3states
    from . import lab3graph
    from . import lab3modify_pop


T = TypeVar("T")


def get_input(input_type: Type[T], prompt: str) -> T:
    """
    Prompts for user input, converts it to the specified type, and handles invalid inputs.

    :param input_type: The desired type to which the user's input should be converted.
    :type input_type: type
    :param prompt: The message displayed to the user when requesting input.
    :type prompt: str
    :return: The user's input converted to the specified type.
    :rtype: Any
    """
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def get_yes_no_input(prompt: str) -> str:
    """
    Prompts the user for a 'yes' or 'no' input and validates the response.

    This function continually requests input until a valid response ('y' or 'n')
    is provided. It uses case-insensitive comparison to validate input and informs
    the user of invalid inputs. The validated response is returned in lower-case.

    :param prompt: The message displayed to the user when requesting input.
    :type prompt: str
    :return: A validated response, either 'y' or 'n', entered by the user.
    :rtype: str
    """
    response = get_input(str, prompt).lower()
    while response not in ("y", "n"):
        print("Invalid input. Please enter 'y' or 'n'.")
        response = get_input(str, prompt).lower()
    return response


def exit_program() -> None:
    """Exits the program.

    :return: None
    :rtype: None
    """
    print("Exiting program. Thank you for using me!")
    sys.exit(0)
